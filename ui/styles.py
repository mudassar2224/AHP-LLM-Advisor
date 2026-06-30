"""
styles.py — Dark glass theme with animated orbs + particles (pure CSS).
Pass use_css_orbs=False when using Vanta Birds to avoid double backgrounds.
"""

def get_css(avatar_b64: str = "", use_css_orbs: bool = True) -> str:
    orb_css = """
/* ── Three animated colour orbs ── */
.stApp::before, .stApp::after {
    content: "";
    position: fixed;
    border-radius: 50%;
    filter: blur(90px);
    z-index: 0;
    pointer-events: none;
    opacity: 0.75;
}
.stApp::before {
    width: 700px; height: 700px;
    background: radial-gradient(circle, #7c3aed 0%, #4f46e5 40%, transparent 70%);
    top: -200px; left: -200px;
    animation: driftA 14s ease-in-out infinite alternate;
}
.stApp::after {
    width: 650px; height: 650px;
    background: radial-gradient(circle, #f093fb 0%, #f5576c 40%, transparent 70%);
    bottom: -180px; right: -180px;
    animation: driftB 17s ease-in-out infinite alternate;
}
.bg-orb3 {
    position: fixed; width: 500px; height: 500px; border-radius: 50%;
    background: radial-gradient(circle, #43e97b 0%, #38f9d7 40%, transparent 70%);
    filter: blur(90px); bottom: 10%; left: 10%;
    z-index: 0; pointer-events: none; opacity: 0.45;
    animation: driftC 20s ease-in-out infinite alternate;
}
@keyframes driftA {
    0%   { transform: translate(0,0)       scale(1);    opacity:.70; }
    33%  { transform: translate(120px,80px) scale(1.08); opacity:.80; }
    66%  { transform: translate(60px,160px) scale(.95);  opacity:.65; }
    100% { transform: translate(200px,120px)scale(1.12); opacity:.78; }
}
@keyframes driftB {
    0%   { transform: translate(0,0)        scale(1);    opacity:.70; }
    33%  { transform: translate(-90px,-60px) scale(1.1);  opacity:.82; }
    66%  { transform: translate(-40px,-130px)scale(.93);  opacity:.60; }
    100% { transform: translate(-160px,-90px)scale(1.15); opacity:.75; }
}
@keyframes driftC {
    0%   { transform: translate(0,0)   scale(1);    opacity:.40; }
    50%  { transform: translate(80px,-60px)scale(1.12);opacity:.55; }
    100% { transform: translate(-50px,80px)scale(.90);opacity:.35; }
}""" if use_css_orbs else ""

    return f"""
<style>

/* ════ 0. HIDE STREAMLIT CHROME ════ */
#MainMenu {{ visibility: hidden; }}
header    {{ visibility: hidden; }}
footer    {{ visibility: hidden; }}

/* ════ 1. DARK BASE ════ */
.stApp {{
    background: #0f0c29 !important;
    min-height: 100vh;
    overflow-x: hidden;
}}
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {{ background: transparent !important; }}
{orb_css}

/* ════ 2. PARTICLES ════ */
.particles {{
    position: fixed; top:0; left:0;
    width:100vw; height:100vh;
    z-index:0; pointer-events:none; overflow:hidden;
}}
.particle {{
    position:absolute; border-radius:50%;
    opacity:0; animation:floatUp linear infinite;
}}
.particle:nth-child(1)  {{ width:6px; height:6px; left:5%;  background:#a78bfa; animation-duration:9s;  animation-delay:0s;   }}
.particle:nth-child(2)  {{ width:4px; height:4px; left:15%; background:#f0abfc; animation-duration:12s; animation-delay:1.5s; }}
.particle:nth-child(3)  {{ width:8px; height:8px; left:25%; background:#6ee7b7; animation-duration:10s; animation-delay:3s;   }}
.particle:nth-child(4)  {{ width:5px; height:5px; left:35%; background:#7c3aed; animation-duration:14s; animation-delay:0.5s; }}
.particle:nth-child(5)  {{ width:7px; height:7px; left:45%; background:#f093fb; animation-duration:11s; animation-delay:2s;   }}
.particle:nth-child(6)  {{ width:4px; height:4px; left:55%; background:#a78bfa; animation-duration:13s; animation-delay:4s;   }}
.particle:nth-child(7)  {{ width:6px; height:6px; left:65%; background:#34d399; animation-duration:9s;  animation-delay:1s;   }}
.particle:nth-child(8)  {{ width:9px; height:9px; left:72%; background:#f5576c; animation-duration:15s; animation-delay:2s;   }}
.particle:nth-child(9)  {{ width:5px; height:5px; left:80%; background:#a78bfa; animation-duration:10s; animation-delay:0.8s; }}
.particle:nth-child(10) {{ width:4px; height:4px; left:88%; background:#f0abfc; animation-duration:12s; animation-delay:3.5s; }}
.particle:nth-child(11) {{ width:7px; height:7px; left:92%; background:#6ee7b7; animation-duration:11s; animation-delay:1.2s; }}
.particle:nth-child(12) {{ width:5px; height:5px; left:98%; background:#7c3aed; animation-duration:13s; animation-delay:0.3s; }}
@keyframes floatUp {{
    0%   {{ transform:translateY(100vh) scale(.5); opacity:0;   }}
    10%  {{ opacity:.8; }}
    90%  {{ opacity:.5; }}
    100% {{ transform:translateY(-10vh) scale(1.2); opacity:0; }}
}}

/* ════ 3. CONTENT LAYER ════ */
.block-container {{
    padding-top:1rem !important;
    padding-bottom:5rem !important;
    max-width:900px !important;
    background:transparent !important;
    position:relative; z-index:1;
}}

/* ════ 4. WELCOME SCREEN ════ */
.welcome-wrapper {{
    position:relative; display:flex;
    flex-direction:column; align-items:center; justify-content:center;
    min-height:78vh; padding:40px 20px 60px;
    text-align:center; z-index:1;
}}
.avatar-orb {{
    position:relative; z-index:2;
    width:96px; height:96px; border-radius:50%;
    background:rgba(255,255,255,.12);
    display:flex; align-items:center; justify-content:center;
    margin:0 auto 28px;
    box-shadow:0 8px 40px rgba(0,0,0,.40),
               0 0 0 4px rgba(255,255,255,.20),
               0 0 0 8px rgba(167,139,250,.20);
    padding:5px;
    animation:orbFloat 3.5s ease-in-out infinite;
    backdrop-filter:blur(10px);
}}
.welcome-avatar {{ width:86px; height:86px; border-radius:50%; object-fit:cover; }}
@keyframes orbFloat {{
    0%,100% {{ transform:translateY(0);  }}
    50%     {{ transform:translateY(-9px); }}
}}
.welcome-content {{ position:relative; z-index:2; max-width:640px; }}
.welcome-heading {{
    font-size:2.9rem !important; font-weight:800 !important;
    color:white !important;
    text-shadow:0 4px 32px rgba(0,0,0,.40) !important;
    line-height:1.18 !important; margin-bottom:16px !important;
    letter-spacing:-0.5px !important;
}}
.welcome-sub {{
    font-size:1.05rem; color:rgba(255,255,255,.78);
    text-shadow:0 1px 12px rgba(0,0,0,.35);
    margin-bottom:36px; line-height:1.6;
}}
.welcome-sub strong {{ color:#c4b5fd; }}
.quick-prompts {{
    display:flex; flex-wrap:wrap; gap:10px;
    justify-content:center; margin-top:8px;
}}
.qp-tag {{
    background:rgba(255,255,255,.10); color:rgba(255,255,255,.90);
    padding:9px 18px; border-radius:50px;
    font-size:.875rem; font-weight:500;
    backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px);
    border:1.5px solid rgba(255,255,255,.20);
    box-shadow:0 2px 16px rgba(0,0,0,.18);
    transition:all .22s ease;
}}
.qp-tag:hover {{
    background:rgba(255,255,255,.18); border-color:rgba(255,255,255,.38);
    transform:translateY(-2px); box-shadow:0 6px 24px rgba(0,0,0,.25);
}}

/* ════ 5. CHAT MESSAGES ════ */
[data-testid="stChatMessage"] {{
    background:transparent !important; border:none !important;
    padding:4px 0 !important; gap:14px !important;
    position:relative; z-index:1;
}}
[data-testid="stChatMessageContent"] > div {{
    background:rgba(255,255,255,.08) !important;
    border-radius:22px !important; padding:14px 20px !important;
    box-shadow:0 4px 28px rgba(0,0,0,.30) !important;
    border:1.5px solid rgba(255,255,255,.15) !important;
    backdrop-filter:blur(18px) !important; -webkit-backdrop-filter:blur(18px) !important;
    font-size:15px !important; line-height:1.68 !important;
    color:rgba(255,255,255,.92) !important; max-width:88% !important;
}}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"])
[data-testid="stChatMessageContent"] > div {{
    background:rgba(124,58,237,.20) !important;
    border:1.5px solid rgba(167,139,250,.30) !important;
    color:rgba(255,255,255,.95) !important;
}}
[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] {{
    border-radius:50% !important; overflow:hidden !important;
    box-shadow:0 3px 14px rgba(0,0,0,.35) !important;
    min-width:40px !important; min-height:40px !important;
    border:2.5px solid rgba(255,255,255,.22) !important;
}}

/* ════ 6. CHAT INPUT ════ */
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"] {{
    background:transparent !important; padding:0 !important;
    margin: 0 auto !important;
    position:relative; z-index:2;
}}
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] textarea {{
    background: rgba(28, 14, 38, 0.6) !important;
}}
[data-testid="stChatInput"] {{
    border-radius: 35px !important; 
    border: 1.5px solid rgba(255, 255, 255, 0.15) !important; 
    backdrop-filter: blur(22px) !important; 
    -webkit-backdrop-filter: blur(22px) !important; 
    box-shadow: 0 6px 32px rgba(0,0,0,.28) !important; 
    padding: 4px 10px !important; 
    overflow: hidden !important;
    margin-bottom: 15px !important;
}}
[data-testid="stChatInput"] textarea {{
    color: rgba(255,255,255,.92) !important;
    font-size: 15px !important; 
    caret-color: #a78bfa !important;
}}
[data-testid="stChatInput"] textarea::placeholder {{
    color: rgba(255,255,255,.38) !important; 
    font-size: 14px !important;
}} 

/* ════ 7. SIDEBAR ════ */
[data-testid="stSidebar"] {{
    background:rgba(15,12,41,.72) !important;
    backdrop-filter:blur(28px) !important; -webkit-backdrop-filter:blur(28px) !important;
    border-right:1.5px solid rgba(255,255,255,.10) !important;
    box-shadow:4px 0 32px rgba(0,0,0,.28) !important;
}}
[data-testid="stSidebar"] > div:first-child {{
    padding-top:22px !important; display:flex !important;
    flex-direction:column !important; gap:4px !important;
}}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {{ color:rgba(255,255,255,.80) !important; }}
.sidebar-brand {{ display:flex; align-items:center; gap:11px; padding:8px 18px 18px; }}

.sidebar-icon {{ font-size:1.7rem; }}
.sidebar-title {{
font-size:1.15rem; font-weight:750;
background:linear-gradient(135deg,#a78bfa 0%,#f0abfc 100%);
-webkit-background-clip:text; -webkit-text-fill-color:transparent;
background-clip:text; letter-spacing:-0.3px;
}}
.sidebar-divider {{
height:1px;
background:linear-gradient(90deg,transparent,rgba(255,255,255,.15),transparent);
margin:0 14px 16px;
}}
.sidebar-section-label {{
font-size:.68rem; font-weight:700;
color:rgba(255,255,255,.35) !important;
letter-spacing:1.8px; text-transform:uppercase;
padding:8px 18px 6px;
}}
[data-testid="stSidebar"] .stButton:first-of-type > button {{
background:linear-gradient(135deg,#7c3aed 0%,#a855f7 100%) !important;
color:white !important; border:none !important;
border-radius:16px !important; padding:12px 20px !important;
font-weight:650 !important; font-size:.95rem !important;
transition:all .22s ease !important;
box-shadow:0 4px 22px rgba(124,58,237,.45) !important;
margin-bottom:6px !important; width:100% !important;
}}
[data-testid="stSidebar"] .stButton:first-of-type > button:hover {{
transform:translateY(-2px) !important;
box-shadow:0 8px 28px rgba(124,58,237,.58) !important;
}}
[data-testid="stSidebar"] .stButton:not(:first-of-type) > button {{
background:transparent !important; color:rgba(255,255,255,.70) !important;
border:none !important; border-radius:13px !important;
padding:10px 14px !important; font-weight:400 !important;
font-size:.88rem !important; text-align:left !important;
box-shadow:none !important; margin-bottom:2px !important;
transition:background .18s !important; width:100% !important;
}}
[data-testid="stSidebar"] .stButton:not(:first-of-type) > button:hover {{
background:rgba(167,139,250,.15) !important;
color:rgba(255,255,255,.95) !important;
transform:none !important; box-shadow:none !important;
}}
.stat-pill {{
display:inline-block; background:rgba(167,139,250,.18);
color:#c4b5fd; border-radius:20px;
padding:3px 10px; font-size:.76rem; font-weight:600; margin:2px;
}}
.sidebar-footer {{
position:fixed; bottom:20px; width:inherit;
text-align:center; font-size:.73rem;
color:rgba(255,255,255,.28) !important;
line-height:1.7; padding:0 10px;
}}
/* ════ 8. MARKDOWN INSIDE BUBBLES ════ */
[data-testid="stChatMessageContent"] p {{ margin:0 0 8px; color:inherit !important; }}
[data-testid="stChatMessageContent"] ul {{ padding-left:20px; }}
[data-testid="stChatMessageContent"] li {{ margin-bottom:4px; color:inherit !important; }}
[data-testid="stChatMessageContent"] strong {{ color:#e9d5ff !important; }}
[data-testid="stChatMessageContent"] code {{
background:rgba(167,139,250,.18); border-radius:5px;
padding:1px 5px; font-size:.88em; color:#ddd6fe !important;
}}
/* ════ 9. SPINNER ════ */
.stSpinner > div > div {{ border-top-color:#a78bfa !important; }}
/* ════ 10. SCROLLBAR ════ */
::-webkit-scrollbar {{ width:5px; height:5px; }}
::-webkit-scrollbar-track {{ background:transparent; }}
::-webkit-scrollbar-thumb {{ background:rgba(167,139,250,.30); border-radius:4px; }}

"""
