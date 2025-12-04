banned_keywords = [
            "bomb", "explosive", "detonate", "c4", "tnt", "grenade",
            "weapon", "gun", "rifle", "pistol", "ammunition", "bullet",
            "knife", "stab", "shoot", "kill", "murder", "assassinate",
            "hack", "hacker", "hacking", "exploit", "vulnerability",
            "ddos", "malware", "ransomware", "trojan", "virus",
            "crack password", "brute force",
            "suicide", "kill myself", "end my life", "self-harm",
            "cocaine", "heroin", "meth", "fentanyl",
            "terrorist", "terrorism", "attack", "assault",
            "how to steal""forget everything","ignore previous","system prompt","act as",
            "pretend you are","break the rules","override","jailbreak"
        ]
        
        
injection_patterns = [
            r"ignore\s+(all\s+)?(previous|prior|above|system)\s+instructions?",
            r"disregard\s+(all\s+)?(previous|prior|rules|instructions)",
            r"forget\s+(all\s+)?(previous|prior|above)\s+(instructions?|rules?|prompts?)",
            r"override\s+(system|safety|security|rules|instructions)",
            r"bypass\s+(restrictions?|rules?|safety|security)",
            r"act\s+as\s+(if|though|a|an)\s+\w+",
            r"pretend\s+(you\s+are|to\s+be)",
            r"roleplay\s+as",
            r"simulate\s+(being|a|an)",
            r"you\s+are\s+now\s+(a|an|in)\s+\w+",
            r"enter\s+(developer|admin|debug|god)\s+mode",
            r"sudo\s+mode",
            r"jailbreak",
            r"DAN\s+mode",
            r"do\s+anything\s+now",
            r"new\s+instructions?:",
            r"system\s*:\s*",
            r"<\|im_start\|>",
            r"<\|endoftext\|>",
            r"%%\s*instructions?",
            r"\[SYSTEM\]",
            r"\[INST\]"
        ]