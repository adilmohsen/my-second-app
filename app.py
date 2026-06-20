import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta
import os

# --- إعداد مجلد الصور المؤقت لمنع تعليق الذاكرة ---
TEMP_IMAGE_DIR = "temp_images"
if not os.path.exists(TEMP_IMAGE_DIR):
    os.makedirs(TEMP_IMAGE_DIR)

# --- إعداد الباسورد ---
PASSWORD = "261239"

# 1. إعدادات الصفحة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")
st_autorefresh(interval=1000, key="datarefresh")

# 2. التنسيقات
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
    }}
    .stChatMessage {{ background-color: rgba(255, 255, 255, 0.8) !important; border-radius: 15px; }}
    .chat-info {{ color: #888888 !important; font-size: 8px !important; float: right; margin-top: 5px; font-family: sans-serif; }}
    .status-icon {{ color: #888888 !important; margin-left: 2px; font-size: 9px !important; }}
    </style>
    """, unsafe_allow_html=True)

# 3. المخزن المشترك
@st.cache_resource
def get_global_messages(): return []
all_msgs = get_global_messages()

def upload_callback():
    if st.session_state.up_files:
        now = (datetime.now() + timedelta(hours=3)).strftime("%I:%M %p")
        for f in st.session_state.up_files:
            file_path = os.path.join(TEMP_IMAGE_DIR, f.name)
            with open(file_path, "wb") as f_out:
                f_out.write(f.getvalue())
            all_msgs.append({
                "name": st.session_state.my_name, 
                "msg": "", "file_path": file_path, "is_image": True, 
                "time": now, "seen": False
            })
        st.session_state.up_files = []

# --- الحماية والاسم ---
if "authenticated" not in st.session_state:
    st.title("🎀 منطقة خاصة للملكات")
    pass_input = st.text_input("كلمة المرور:", type="password")
    if st.button("دخول"):
        if pass_input == PASSWORD: st.session_state.authenticated = True; st.rerun()
        else: st.error("غلط! ❌")
    st.stop()

if "my_name" not in st.session_state:
    st.title("🎀 أهلاً بيج")
    name_input = st.text_input("اسمج:")
    if st.button("تأكيد"):
        if name_input: st.session_state.my_name = name_input; st.rerun()
    st.stop()

# --- القائمة الجانبية ---
st.sidebar.title(f"الملكة {st.session_state.my_name}")
st.sidebar.file_uploader("+", key="up_files", type=['png', 'jpg'], accept_multiple_files=True, on_change=upload_callback)

if st.sidebar.button("حذف الكل 🗑️"): all_msgs.clear(); st.rerun()

st.title("Canım 🎀")

# --- عرض المحادثة ---
for i, chat in enumerate(all_msgs):
    if chat['name'] != st.session_state.my_name: chat['seen'] = True
    with st.chat_message("user"):
        st.write(f"**{chat['name']}:** {chat.get('msg', '')}")
        if chat.get("is_image") and os.path.exists(chat["file_path"]):
            st.image(chat["file_path"], use_container_width=True)
        t = chat.get('time', '')
        st.markdown(f'<div class="chat-info">{t}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("اكتبي رسالتج..."):
    now = (datetime.now() + timedelta(hours=3)).strftime("%I:%M %p")
    all_msgs.append({"name": st.session_state.my_name, "msg": prompt, "time": now, "seen": False})
    st.rerun()
