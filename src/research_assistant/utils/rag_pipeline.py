from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.vectorstores import FAISS
from langchain_classic.retrievers.ensemble import  EnsembleRetriever
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors.cross_encoder_rerank import CrossEncoderReranker
from langchain_community.retrievers import BM25Retriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document as LCDocument
from langsmith import traceable #type: ignore
from src.research_assistant.utils.cached_models import get_cross_encoder_model,get_embedding_model

@traceable(name="PDFQA_init")
class PDFQA:
    def __init__(self, text: str):
        self.text = text
        self.vector_store = None
        self.retriever = None
        self.embedding_model = get_embedding_model()
        self.cross_encoder_model = get_cross_encoder_model()
        self._process_pdf()

    @traceable(name="PDFQA_rag_text_split")
    def _split_text(self, text: str) -> list[LCDocument]:
        """Hybrid chunking: semantic chunker first, then recursive splitter for finer granularity"""

        try:
            # SemanticChunker: captures high-level semantic splits
            semantic_splitter = SemanticChunker(
                embeddings=self.embedding_model,
                buffer_size=2,  #Previous : 4
                add_start_index=False,
                breakpoint_threshold_type="percentile",
                breakpoint_threshold_amount=75, #Previous :85
                number_of_chunks=None,
                sentence_split_regex=r"(?<=[.?!])\s+"
            )
            semantic_docs = semantic_splitter.create_documents([text]) #type: ignore

            # RecursiveCharacterTextSplitter: further split large semantic chunks
            final_chunks: list[LCDocument] = []
            recursive_splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,     
                chunk_overlap=150
            )
            for doc in semantic_docs:
                small_chunks = recursive_splitter.split_text(doc.page_content)
                for chunk in small_chunks:
                    final_chunks.append(LCDocument(
                        page_content = chunk,
                        metadata = doc.metadata   #type: ignore
                    ))

            if not final_chunks:
                raise ValueError("No text chunks were created from the input text.")
                
            return final_chunks
        except Exception as e:
            raise ValueError(f"Text chunking failed: {str(e)}") from e
        
    @traceable(name="PDFQA_text_embedding")
    def _embed_texts(self, splits: list[LCDocument]) -> FAISS:
        """Embed and create FAISS vector store"""
        try:
            if not splits:
                raise ValueError("No text splits provided for embedding.")
            vector_store = FAISS.from_documents(splits, self.embedding_model)
            return vector_store
        except Exception as e:
            raise ValueError(f"Embedding creation failed: {str(e)}") from e

    @traceable(name="PDFQA_rag_retreiver_setup")
    def _process_pdf(self):
        """Split, embed, create hybrid retriever, and apply reranker"""
        try:
            splits = self._split_text(self.text)
            self.vector_store = self._embed_texts(splits)

            # Dense FAISS retriever
            dense_retriever = self.vector_store.as_retriever(
                search_type="mmr",
                search_kwargs={"k": 10, "fetch_k": 30, "lambda_mult": 0.7}
            )

            # Sparse BM25 retriever
            bm25_retriever = BM25Retriever.from_documents(splits)
            bm25_retriever.k = 8

            # Hybrid ensemble retriever
            hybrid_retriever = EnsembleRetriever(
                retrievers=[bm25_retriever, dense_retriever],
                weights=[0.35, 0.65]  # adjust weighting as needed
            )

            # Cross-encoder reranker
            reranker = CrossEncoderReranker(model=self.cross_encoder_model, top_n=3)

            # Final Contextual Compression Retriever
            self.retriever = ContextualCompressionRetriever(
                base_compressor=reranker,
                base_retriever=hybrid_retriever
            )
        except Exception as e:
            raise ValueError(f"Retriever setup failed: {str(e)}") from e
