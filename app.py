"""
app.py  —  AHP LLM Advisor
Complete version: dark theme + Vanta Birds + greeting detection + follow-up context + 5 models
"""

import streamlit as st
import base64
import time
from pathlib import Path

from core.ahp_engine       import compute_ahp_scores
from core.keyword_detector import load_keyword_map
from core.rag_engine       import load_dataset, format_context, get_dataset_stats
from core.groq_client      import GroqClient
from ui.styles             import get_css
import config

# ── Page config (must be first) ────────────────────────────────────────────
st.set_page_config(
    page_title            = config.APP_TITLE,
    page_icon             = config.APP_ICON,
    layout                = "wide",
    initial_sidebar_state = "expanded",
)

BASE        = Path(__file__).parent
AVATAR_PATH = BASE / "assets" / "avatar.png"
DATA_DIR    = BASE / "data"

# ══════════════════════════════════════════════════════════════════════════
# TOGGLE: set True for Vanta Birds, False for pure-CSS animated orbs
# ══════════════════════════════════════════════════════════════════════════
USE_VANTA = False   # flip to True once you confirm CDN loads in your env

# ══════════════════════════════════════════════════════════════════════════
# GREETING / CASUAL CHAT DETECTOR  — skips AHP for "hi", "thanks", etc.
# ══════════════════════════════════════════════════════════════════════════
CASUAL_GREETINGS = {
    "hi","hello","hey","hiya","sup","yo","howdy","greetings",
    "thanks","thank you","ty","thx","thankyou",
    "ok","okay","k","got it","understood","noted","alright",
    "bye","goodbye","cya","see you","take care","later",
    "good morning","good evening","good night","good afternoon",
    "how are you","how r u","who are you","what are you",
    "what can you do","tell me about yourself",
    "nice","great","awesome","cool","wow","interesting","amazing",
    "lol","haha","hehe","yes","no","sure","nope","yep","nah",
    "welcome","you're welcome","np","no problem","sounds good",
}

TASK_TRIGGERS = {
    "build","make","create","code","need","want","help","use",
    "which","what","why","how","should","recommend","best",
    "compare","tell","explain","guide","show","suggest","select",
    "choose","pick","find","generate","develop","design","write",
    "deploy","train","analyze","analyse","predict","classify",
    "tool","model","llm","ai","api","app","website","system",
}

def is_casual(text: str) -> bool:
    """True = greeting/small-talk → skip AHP, just chat."""
    t     = text.lower().strip().rstrip("!?.,:;")
    words = t.split()
    if t in CASUAL_GREETINGS:
        return True
    if len(words) <= 3 and not any(w in TASK_TRIGGERS for w in words):
        return True
    return False


def build_context_query(messages: list, current: str) -> str:
    """
    For short follow-ups ('why not Claude?', 'what about GPT?'),
    prepend the previous user message so AHP keeps the right domain.
    E.g. after 'build a flutter game' → 'build a flutter game why not Claude?'
    """
    FOLLOWUP_STARTS = {
        "why not","what about","how about","and what","but what",
        "compare","vs","versus","is it","can i","can we",
        "what if","should i","would","difference","instead",
        "but why","and why","also","so what","then what",
    }
    t          = current.lower().strip()
    is_followup = (
        any(t.startswith(ft) for ft in FOLLOWUP_STARTS)
        or len(current.split()) <= 5
    )

    if is_followup and len(messages) >= 2:
        prev = [m["content"] for m in messages[:-1] if m["role"] == "user"]
        if prev:
            return prev[-1] + " " + current

    return current


# ══════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════
def img_to_b64(path: Path) -> str:
    if path.exists():
        return base64.b64encode(path.read_bytes()).decode()
    return ""


def get_groq_key() -> str:
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return config.GROQ_API_KEY


# ══════════════════════════════════════════════════════════════════════════
# CACHED RESOURCES
# ══════════════════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner="Loading AHP engine & dataset…")
def load_resources():
    dataset     = load_dataset(str(DATA_DIR / "llm_master_dataset.csv"))
    keyword_map = load_keyword_map(str(DATA_DIR / "keyword_capability_map.csv"))
    client      = GroqClient(get_groq_key(), config.GROQ_MODEL)
    return dataset, keyword_map, client


dataset, keyword_map, groq_client = load_resources()
stats      = get_dataset_stats(dataset)
avatar_b64 = img_to_b64(AVATAR_PATH)

# ══════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════
if "chats"        not in st.session_state:
    st.session_state.chats        = {"Chat 1": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"
if "chat_counter" not in st.session_state:
    st.session_state.chat_counter = 1

# ══════════════════════════════════════════════════════════════════════════
# BACKGROUND & CSS
# ══════════════════════════════════════════════════════════════════════════
# Inject CSS (orbs disabled when Vanta is on to avoid double backgrounds)
st.markdown(get_css(avatar_b64, use_css_orbs=not USE_VANTA), unsafe_allow_html=True)

# Vanta Birds (optional — loads three.js + vanta from CDN)
if USE_VANTA:
    from ui.vanta_bg import inject_vanta_birds
    inject_vanta_birds()
else:
    # Pure-CSS animated background: third orb + rising particles
    st.markdown("""
        <div class="bg-orb3"></div>
        <div class="particles">
            <div class="particle"></div><div class="particle"></div>
            <div class="particle"></div><div class="particle"></div>
            <div class="particle"></div><div class="particle"></div>
            <div class="particle"></div><div class="particle"></div>
            <div class="particle"></div><div class="particle"></div>
            <div class="particle"></div><div class="particle"></div>
        </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════
with st.sidebar:

    st.markdown("""
        <div class="sidebar-brand">
            <span class="sidebar-icon">🧠</span>
            <span class="sidebar-title">LLM Advisor</span>
        </div>
        <div class="sidebar-divider"></div>
    """, unsafe_allow_html=True)

    if st.button("✨  Start New Chat", use_container_width=True, key="new_chat"):
        st.session_state.chat_counter += 1
        name = f"Chat {st.session_state.chat_counter}"
        st.session_state.chats[name] = []
        st.session_state.current_chat = name
        st.rerun()

    st.markdown('<div class="sidebar-section-label">RECENT CHATS</div>',
                unsafe_allow_html=True)

    for chat_name in reversed(list(st.session_state.chats.keys())):
        msgs    = st.session_state.chats[chat_name]
        preview = msgs[0]["content"][:28] + "…" if msgs else "Empty chat"
        active  = chat_name == st.session_state.current_chat
        label   = f"{'▶  ' if active else '    '}{chat_name}  —  {preview}"
        if st.button(label, key=f"sel_{chat_name}", use_container_width=True):
            st.session_state.current_chat = chat_name
            st.rerun()

    st.markdown('<div class="sidebar-divider" style="margin-top:18px;"></div>',
                unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-label">DATASET</div>',
                unsafe_allow_html=True)
    st.markdown(f"""
        <div style="padding:4px 14px 10px; line-height:2;">
            <span class="stat-pill">🤖 {stats['total_models']} Models</span>
            <span class="stat-pill">🏢 {stats['companies']} Companies</span>
            <span class="stat-pill">🔓 {stats['open_source']} Open Source</span>
            <span class="stat-pill">🆓 {stats['free_tier']} Free tier</span>
            <span class="stat-pill">📊 275 Keywords</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-footer">
            Powered by <strong>Groq</strong> × <strong>AHP Engine</strong><br/>
            🔥 Fast LLM Inference · 50 Models · 12 Domains
        </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════
messages = st.session_state.chats[st.session_state.current_chat]

# ── Welcome screen ──────────────────────────────────────────────────────
if not messages:
    avatar_tag = (
        f'<img src="data:image/png;base64,{avatar_b64}" class="welcome-avatar" />'
        if avatar_b64 else "🧠"
    )
    st.markdown(f"""
        <div class="welcome-wrapper">
            <div class="welcome-content">
                <div class="avatar-orb">{avatar_tag}</div>
                <h1 class="welcome-heading">
                    How can I help you<br/>choose the right LLM?
                </h1>
                <p class="welcome-sub">
                    Tell me what you want to build — I'll use
                    <strong>AHP scoring</strong> across 50 models
                    to give you a data-driven recommendation.
                </p>
                <div class="quick-prompts">
                    <span class="qp-tag">🔍 Build a RAG chatbot</span>
                    <span class="qp-tag">🏦 Banking app with fraud detection</span>
                    <span class="qp-tag">💻 Flutter game development</span>
                    <span class="qp-tag">🎥 YouTube / Pinterest content</span>
                    <span class="qp-tag">🛒 E-commerce store</span>
                    <span class="qp-tag">🏥 Medical diagnosis assistant</span>
                    <span class="qp-tag">⚖️ Legal contract analyzer</span>
                    <span class="qp-tag">🌍 Multilingual support bot</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ── Chat history ────────────────────────────────────────────────────────
else:
    for msg in messages:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👩‍💻"):
                st.markdown(msg["content"])
        else:
            avatar = str(AVATAR_PATH) if AVATAR_PATH.exists() else "🧠"
            with st.chat_message("assistant", avatar=avatar):
                st.markdown(msg["content"])


# ══════════════════════════════════════════════════════════════════════════
# CHAT INPUT + RESPONSE
# ══════════════════════════════════════════════════════════════════════════
user_input = st.chat_input("Chat with me, I'm here for you…")

if user_input:

    # 1 ── show user bubble immediately
    with st.chat_message("user", avatar="👩‍💻"):
        st.markdown(user_input)
    messages.append({"role": "user", "content": user_input})

    # 2 ── decide whether to run AHP
    context = ""

    if not is_casual(user_input):
        # Build query — combines with prev message for follow-ups
        context_query = build_context_query(messages, user_input)

        top_models, cap_weights, ahp_weights, domain, cr = compute_ahp_scores(
            context_query, dataset, keyword_map, top_k=config.TOP_K_MODELS
        )
        context = format_context(
            top_models, context_query, cap_weights, ahp_weights, domain, cr
        )

    # 3 ── stream AI response
    avatar = str(AVATAR_PATH) if AVATAR_PATH.exists() else "🧠"
    with st.chat_message("assistant", avatar=avatar):
        placeholder   = st.empty()
        full_response = ""

        for chunk in groq_client.stream_chat(
            history      = messages[:-1],
            user_message = user_input,
            context      = context,
        ):
            full_response += chunk
            placeholder.markdown(full_response + "▌")
            time.sleep(0.004)

        placeholder.markdown(full_response)

    # 4 ── save to session
    messages.append({"role": "assistant", "content": full_response})
    st.session_state.chats[st.session_state.current_chat] = messages
