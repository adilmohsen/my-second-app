import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta

# 1. إعدادات الصفحة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")
st_autorefresh(interval=1000, key="datarefresh")

# 2. التنسيقات (تنسيق الصور وزر الحفظ)
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
    }}
    .stChatMessage {{ background-color: rgba(255, 255, 255, 0.8) !important; border-radius: 15px; }}
    
    .chat-info {{ color: #888888 !important; font-size: 8px !important; float: right; margin-top: 5px; }}
    .status-icon {{ color: #888888 !important; margin-left: 2px; font-size: 9px !important; }}
    
    /* ستايل علامة الـ + */
    section[data-testid="stSidebar"] .stFileUploader label {{
        font-size: 30px !important;
        color: #888 !important;
        display: block !important;
        text-align: center;
    }}
    section[data-testid="stSidebar"] .stFileUploader section > div {{ display: none !important; }}
    
    /* تنسيق زر الحفظ ليكون نازك تحت الصورة */
    .stDownloadButton button {{
        font-size: 10px !important;
        padding: 2px 10px !important;
        background-color: rgba(255, 255, 255, 0.5) !important;
        border-radius: 10px !important;
        color: #888 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. المخزن المشترك
@st.cache_resource
def get_global_messages(): return []
all_msgs = get_global_messages()

# --- تسجيل الدخول ---
if "my_name" not in st.session_state:
    st.title("🎀 أهلاً بيج بالچات الوردي")
    name_input = st.text_input("اسمج هنا:")
    if st.button("دخول"):
        if name_input: st.session_state.my_name = name_input; st.rerun()
    st.stop()

# --- السايدبار ---
st.sidebar.title(f"الملكة {st.session_state.my_name}")
uploaded_file = st.sidebar.file_uploader("+", key="auto_uploader")

if uploaded_file is not None:
    iraq_time = datetime.now() + timedelta(hours=3)
    now = iraq_time.strftime("%I:%M %p")
    file_bytes = uploaded_file.getvalue()
    is_image = uploaded_file.type.startswith("image")
    
    all_msgs.append({
        "name": st.session_state.my_name, 
        "msg": "", 
        "file": file_bytes,
        "is_image": is_image,
        "time": now, 
        "seen": False
    })
    st.rerun()

st.sidebar.divider()
if st.sidebar.button("تسجيل الخروج ⬅️"):
    del st.session_state.my_name; st.rerun()

st.title("🎀 محادثة مريوم المشتركة")

# --- عرض الرسائل ---
for i, chat in enumerate(all_msgs):
    if chat['name'] != st.session_state.my_name: chat['seen'] = True
    col_msg, col_options = st.columns([0.9, 0.1])
    with col_msg:
        with st.chat_message("user"):
            st.write(f"**{chat['name']}:**")
            
            if "file" in chat:
                if chat["is_image"]:
                    # عرض الصورة مع ميزة التكبير التلقائية في المتصفح
                    st.image(chat["file"], use_container_width=True)
                    # زر الحفظ تحت الصورة
                    st.download_button(label="حفظ 📥", data=chat["file"], file_name=f"meryoum_image_{i}.png", mime="image/png")
                else:
                    st.download_button("تحميل الملف", chat["file"])

            msg_time = chat.get('time', '') 
            status_text = "v v" if chat.get('seen', False) else "v"
            st.markdown(f'<div class="chat-info">{msg_time} <span class="status-icon">{status_text}</span></div>', unsafe_allow_html=True)
            
    if chat['name'] == st.session_state.my_name:
        with col_options:
            if st.button("⋮", key=f"menu_{i}"):
                st.session_state[f"show_options_{i}"] = not st.session_state.get(f"show_options_{i}", False)
            if st.session_state.get(f"show_options_{i}", False):
                if st.button("🗑️", key=f"del_{i}"): all_msgs.pop(i); st.rerun()

if prompt := st.chat_input("اكتبي رسالتج هنا..."):
    iraq_time = datetime.now() + timedelta(hours=3)
    now = iraq_time.strftime("%I:%M %p")
    all_msgs.append({"name": st.session_state.my_name, "msg": prompt, "time": now, "seen": False})
    st.rerun()
