import os

# ─────────────────────────────────────────────
# GROQ API  (fast open-source LLM inference)
# ─────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Best available Groq models (fallback chain)
GROQ_MODEL        = "llama-3.3-70b-versatile"
GROQ_MODEL_FAST   = "llama3-70b-8192"
GROQ_MODEL_LIGHT  = "mixtral-8x7b-32768"

# ─────────────────────────────────────────────
# APP SETTINGS
# ─────────────────────────────────────────────
APP_TITLE         = "AHP LLM Advisor"
APP_ICON          = "🧠"
TOP_K_MODELS      = 5      # how many models to surface in context
MAX_TOKENS        = 1024
TEMPERATURE       = 0.7

# ─────────────────────────────────────────────
# AHP CRITERIA LABELS
# ─────────────────────────────────────────────
AHP_CRITERIA = ["Performance", "Cost Efficiency", "Safety & Trust", "Domain Fit"]

# Domain → AHP weight profiles  [Perf, Cost, Safety, DomainFit]
DOMAIN_WEIGHT_PROFILES = {
    "banking":       [0.25, 0.15, 0.52, 0.08],
    "healthcare":    [0.25, 0.15, 0.52, 0.08],
    "legal":         [0.25, 0.18, 0.50, 0.07],
    "coding":        [0.52, 0.22, 0.14, 0.12],
    "creative":      [0.30, 0.28, 0.10, 0.32],
    "video":         [0.28, 0.28, 0.10, 0.34],
    "education":     [0.36, 0.30, 0.22, 0.12],
    "research":      [0.40, 0.26, 0.22, 0.12],
    "ecommerce":     [0.35, 0.38, 0.18, 0.09],
    "cybersecurity": [0.40, 0.20, 0.32, 0.08],
    "chatbot":       [0.34, 0.34, 0.20, 0.12],
    "multilingual":  [0.28, 0.30, 0.18, 0.24],
    "default":       [0.35, 0.30, 0.22, 0.13],
}

# Keywords that signal each domain profile
DOMAIN_KEYWORDS = {
    "banking":       ["bank","finance","payment","invoice","trading","fintech","accounting","tax","audit","insurance","wallet"],
    "healthcare":    ["hospital","medical","doctor","health","clinical","patient","pharmacy","diagnosis","surgery","nurse","ehr","telemedicine"],
    "legal":         ["lawyer","legal","contract","law","court","compliance","regulation","attorney","policy","gdpr","lawsuit"],
    "coding":        ["code","coding","programming","software","app","website","api","debug","python","javascript","git","devops","microservices","database","backend","frontend"],
    "creative":      ["write","story","novel","poem","blog","article","creative","script","lyrics","copywriting","content","marketing","advertising","seo","social media","caption","hashtag","instagram","facebook","twitter","linkedin","pinterest"],
    "video":         ["video","youtube","tiktok","reel","vlog","animation","film","movie","shorts","streaming","broadcast","channel"],
    "education":     ["teach","tutor","education","course","homework","exam","quiz","lecture","textbook","curriculum","school","university","student","assignment"],
    "research":      ["research","analyze","analysis","data","report","summary","insight","survey","study","journal","paper"],
    "ecommerce":     ["shop","store","ecommerce","product","cart","checkout","dropshipping","inventory","fulfillment","review","pricing"],
    "cybersecurity": ["security","cybersecurity","hack","penetration","vulnerability","firewall","encryption","forensics","malware","threat"],
    "chatbot":       ["chatbot","assistant","customer support","helpdesk","virtual agent","support bot","customer service"],
    "rag":           ["rag","retrieval augmented","vector database","vector store","embeddings","llamaindex","langchain",
                      "chromadb","pinecone","knowledge base","knowledge graph","document qa","semantic search"],
    "multilingual":  ["translate","translation","arabic","chinese","spanish","french","urdu","japanese","hindi","multilingual","localization","subtitle"],
}
