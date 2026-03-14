import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. إعدادات الصفحة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")
st_autorefresh(interval=2000, key="datarefresh")

# 2. سحر الـ CSS لتحويل الشكل إلى آيفون وردي
st.markdown(f"""
    <style>
    /* الخلفية الوردية العامة */
    [data-testid="stAppViewContainer"] {{
        background-color: #FFE4E1; /* لون وردي ناعم */
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
    }}

    /* تعديل خانة الـ chat_input لتشبه الصورة */
    [data-testid="stChatInput"] {{
        bottom: 20px;
        background-color: transparent !important;
    }}
    
    [data-testid="stChatInput"] textarea {{
        background-color: #F0E68C !important; /* لون الفقاعة اللي بالصورة */
        border-radius: 25px !important;
        color: black !important;
        border: none !important;
    }}

    /* زر الإرسال الدائري */
    [data-testid="stChatInput"] button {{
        background-color: #F0E68C !important;
        border-radius: 50% !important;
        color: black !important;
        bottom: 5px !important;
    }}

    .stChatMessage {{ background-color: rgba(255, 255, 255, 0.8) !important; border-radius: 15px; }}
    </style>
    """, unsafe_allow_html=True)

# 3. المخزن والبيانات
@st.cache_resource
def get_global_messages(): return []
all_msgs = get_global_messages()

# --- شاشة تسجيل الدخول ---
if "my_name" not in st.session_state:
    st.title("👸 مملكة مريوم")
    name = st.text_input("اسمج الملكي:")
    if st.button("دخول ✨"):
        if name: st.session_state.my_name = name; st.rerun()
    st.stop()

# --- عرض المحادثة ---
st.title("👸 The Queen Meryoum Chat 🌸")

for i, chat in enumerate(all_msgs):
    col_msg, col_opt = st.columns([0.9, 0.1])
    with col_msg:
        with st.chat_message("user"): st.write(f"**{chat['name']}:** {chat['msg']}")
    if chat['name'] == st.session_state.my_name:
        with col_opt:
            if st.button("⋮", key=f"m_{i}"):
                st.session_state[f"o_{i}"] = not st.session_state.get(f"o_{i}", False)
            if st.session_state.get(f"o_{i}", False):
                if st.button("🗑️", key=f"d_{i}"): all_msgs.pop(i); st.rerun()
                if st.button("✏️", key=f"e_{i}"): st.session_state.edit_idx = i; st.session_state.edit_txt = chat['msg']; st.rerun()

# --- منطقة الإرسال (ثابتة + Enter) ---
# استخدمنا chat_input لأنها تدعم Enter وتثبت بالأسفل تلقائياً
if prompt := st.chat_input("اكتبي رسالتج هنا..."):
    all_msgs.append({"name": st.session_state.my_name, "msg": prompt})
    st.rerun()

# --- زر الإيموجي (يبقى طافي فوق الخانة) ---
with st.sidebar:
    st.write("إيموجيات سريعة:")
    emojis = ["🌸", "👑", "💖", "✨", "🎀", "😂", "🔥", "💀"]
    for emo in emojis:
        if st.button(emo):
            st.warning(f"انسخي الإيموجي {emo} واستخدميه بالچات!")
