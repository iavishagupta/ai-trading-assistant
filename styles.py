STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* BASE */
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: #0B0E11 !important;
    color: #EAECEF !important;
    font-family: 'Inter', sans-serif !important;
}

/* ANIMATED GRADIENT BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #0B0E11 0%, #0d1117 50%, #0B0E11 100%) !important;
}

/* HEADER */
header[data-testid="stHeader"],
[data-testid="stToolbar"] {
    background: transparent !important;
}

/* LAYOUT */
.block-container {
    max-width: 900px;
    padding-top: 3rem;
    padding-bottom: 8rem;
}

/* TITLE — Electric Gold Glow */
/* NEON TITLE */
h1 {
    text-align: left;
    font-size: 3.6rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.04em !important;
    background: linear-gradient(90deg, #F0B90B, #FFD700, #F0B90B) !important;
    background-size: 200% auto !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    animation: shine 3s linear infinite !important;
    filter: drop-shadow(0 0 12px #F0B90B88) drop-shadow(0 0 30px #F0B90B44) !important;
}

@keyframes shine {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}

/* CAPTION */
[data-testid="stCaptionContainer"] {
    color: #848E9C !important;
    font-size: 0.97rem !important;
    margin-bottom: 2rem !important;
}

/* CHAT MESSAGE CARDS */
[data-testid="stChatMessage"] {
    background: rgba(22, 27, 39, 0.75) !important;
    border: 1px solid #2A3040 !important;
    border-radius: 18px !important;
    padding: 1rem 1.2rem !important;
    margin-bottom: 0.85rem !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3) !important;
    transition: border-color 0.2s ease !important;
}

/* AMBIENT GLOW BEHIND CHAT CARDS */
[data-testid="stChatMessage"] {
    position: relative !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"])::before {
    content: '';
    position: absolute;
    inset: -1px;
    border-radius: 18px;
    background: radial-gradient(ellipse at left, #F0B90B11, transparent 70%);
    z-index: -1;
    pointer-events: none;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"])::before {
    content: '';
    position: absolute;
    inset: -1px;
    border-radius: 18px;
    background: radial-gradient(ellipse at left, #02C07611, transparent 70%);
    z-index: -1;
    pointer-events: none;
}
[data-testid="stChatMessage"]:hover {
    border-color: #F0B90B44 !important;
}

/* USER MESSAGE — subtle gold left border */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    border-left: 3px solid #F0B90B !important;
}

/* ASSISTANT MESSAGE — subtle green left border */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    border-left: 3px solid #02C076 !important;
}

/* MESSAGE TEXT */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.97rem !important;
    line-height: 1.7 !important;
    color: #EAECEF !important;
}

[data-testid="stMarkdownContainer"] strong {
    color: #F5F5F5 !important;
    font-weight: 600 !important;
}

/* AVATARS */
[data-testid="stChatMessageAvatarUser"] {
    background: linear-gradient(135deg, #F0B90B, #FFD700) !important;
    border-radius: 12px !important;
    box-shadow: 0 0 12px #F0B90B55 !important;
}

[data-testid="stChatMessageAvatarAssistant"] {
    background: linear-gradient(135deg, #02C076, #00A86B) !important;
    border-radius: 12px !important;
    box-shadow: 0 0 12px #02C07655 !important;
}

/* BOTTOM INPUT AREA */
div[data-testid="stBottom"],
div[data-testid="stBottom"] > div,
div[data-testid="stBottomBlockContainer"] {
    background: #0B0E11 !important;
    border-top: 0px !important;
}

div[class="st-emotion-cache-hzygls eqt0gmo3"] {
    height: 100px;
}

.st-emotion-cache-hzygls {
    position: fixed;
    height: 100px;
}

/* CHAT INPUT WRAPPER */
div[data-testid="stChatInput"] {
    max-width: 1500px !important;
    margin: 0 auto 1.2rem auto !important;
    padding: 0 !important;
    background: transparent !important;
}

/* INPUT BOX */
div[data-testid="stChatInput"] > div {
    background: #1C2030 !important;
    border: 1px solid #F0B90B55 !important;
    border-radius: 16px !important;
    padding: 0.45rem 0.7rem !important;
    box-shadow: 0 0 20px #F0B90B11 !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}

div[data-testid="stChatInput"] > div:focus-within {
    border-color: #F0B90B !important;
    box-shadow: 0 0 25px #F0B90B33 !important;
}

/* TEXTAREA */
textarea[data-testid="stChatInputTextArea"] {
    background: #1C2030 !important;
    color: #EAECEF !important;
    border: none !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.97rem !important;
    min-height: 44px !important;
    max-height: 44px !important;
    padding-top: 0.6rem !important;
}

textarea[data-testid="stChatInputTextArea"]::placeholder {
    color: #474D57 !important;
}

/* SEND BUTTON */
button[data-testid="stChatInputSubmitButton"] {
    background: linear-gradient(135deg, #F0B90B, #FFD700) !important;
    color: #0B0E11 !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    box-shadow: 0 0 15px #F0B90B44 !important;
    transition: box-shadow 0.2s ease !important;
    position: relative;
    align-self: center;
}

button[data-testid="stChatInputSubmitButton"]:hover {
    box-shadow: 0 0 25px #F0B90B88 !important;
}

.st-emotion-cache-vlkg2l {
    padding-right: 15px;
}

/* CONFIRM / CANCEL BUTTONS */
.stButton > button {
    background: linear-gradient(135deg, #F0B90B, #FFD700) !important;
    color: #0B0E11 !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.65rem 1rem !important;
    box-shadow: 0 0 15px #F0B90B33 !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    box-shadow: 0 0 25px #F0B90B77 !important;
    transform: translateY(-1px) !important;
}

/* CODE */
code {
    color: #F0B90B !important;
    background: #1E2329 !important;
    border: 1px solid #2A3040 !important;
    border-radius: 6px !important;
    padding: 0.15rem 0.4rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.87rem !important;
}

/* LINKS */
a { color: #F0B90B !important; }

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #0B0E11 !important;
    border-right: 1px solid #1C2030 !important;
}

/* SCROLLBAR */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0B0E11; }
::-webkit-scrollbar-thumb {
    background: #F0B90B44;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: #F0B90B; }

/* SELECTION */
::selection {
    background: #F0B90B44;
    color: #EAECEF;
}

/* HIDE STREAMLIT DECORATION */
#MainMenu, footer { visibility: hidden; }

/* ROBOTIC BACKGROUND SYMBOLS */
.bg-symbols {
    position: fixed;
    top: 0; left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}

.bg-symbols span {
    position: absolute;
    font-size: 1.4rem;
    color: #F0B90B;
    animation: drift linear infinite;
    user-select: none;
}

.bg-symbols span:nth-child(1)  { left: 5%;  top: 10%; animation-duration: 18s; font-size: 1.8rem; }
.bg-symbols span:nth-child(2)  { left: 15%; top: 70%; animation-duration: 22s; color: #02C076; }
.bg-symbols span:nth-child(3)  { left: 25%; top: 30%; animation-duration: 15s; font-size: 1.2rem; }
.bg-symbols span:nth-child(4)  { left: 38%; top: 80%; animation-duration: 20s; color: #02C076; }
.bg-symbols span:nth-child(5)  { left: 50%; top: 15%; animation-duration: 25s; font-size: 2rem; }
.bg-symbols span:nth-child(6)  { left: 62%; top: 55%; animation-duration: 17s; }
.bg-symbols span:nth-child(7)  { left: 72%; top: 25%; animation-duration: 21s; color: #02C076; }
.bg-symbols span:nth-child(8)  { left: 82%; top: 75%; animation-duration: 19s; font-size: 1.6rem; }
.bg-symbols span:nth-child(9)  { left: 90%; top: 40%; animation-duration: 23s; }
.bg-symbols span:nth-child(10) { left: 45%; top: 60%; animation-duration: 16s; color: #02C076; }
.bg-symbols span:nth-child(11) { left: 8%;  top: 50%; animation-duration: 24s; font-size: 1.1rem; }
.bg-symbols span:nth-child(12) { left: 55%; top: 90%; animation-duration: 20s; }

@keyframes drift {
    0%   { transform: translateY(0px) rotate(0deg); opacity: 0; }
    10%  { opacity: 1; }
    90%  { opacity: 1; }
    100% { transform: translateY(-80px) rotate(15deg); opacity: 0; }
}
</style>
"""