import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta

# 1. إعدادات الصفحة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")
st_autorefresh(interval=1000, key="datarefresh")

# 2. التنسيقات (تصليح شكل الـ + كرسالة وبدون نصوص)
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
    }}
    .stChatMessage {{ background-color: rgba(255, 255, 255, 0.8) !important; border-radius: 15px; }}
    
    .chat-info {{ color: #888888 !important; font-size: 8px !important; float: right; margin-top: 5px; font-family: sans-serif; }}
    .status-icon {{ color: #888888 !important; margin-left: 2px; font-size: 9px !important; }}
    
    .stButton button {{ border: none !important; background: transparent !important; color: #888 !important; font-size: 20px !important; }}

    /* ستايل علامة الـ + الاحترافي في السايدبار كرسالة */
    section[data-testid="stSidebar"] .stFileUploader label {{
        font-size: 35px !important;
        color: #888 !important;
        display: block !important;
        text-align: center;
        cursor: pointer;
    }}
    section[data-testid="stSidebar"] .stFileUploader section {{ padding: 0 !important; border: none !important; background: transparent !important; }}
    /* إخفاء نصوص الـ Drag and Drop والنصوص الإضافية */
    section[data-testid="stSidebar"] .stFileUploader section > div {{ display: none !important; }}
    section[data-testid="stSidebar"] .stFileUploader [data-testid="stMarkdownContainer"] {{ display: none !important; }}
    
    /* إخفاء أي نصوص إضافية فوق الصور */
    [data-testid="stImageCaption"] {{ display: none !important; }}
    
    /* تنسيق زر "إرسال كرسالة" ليكون نازك */
    [data-testid="stSidebar"] [data-testid="stForm"] > [data-testid="stButton"] button {{
        font-size: 14px !important;
        background-color: transparent !important;
        border: 1px solid #ddd !important;
        border-radius: 10px !important;
        color: #888 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. المخزن المشترك للرسايل
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

# --- القائمة الجانبية (السايدبار) ---
st.sidebar.title(f"الملكة {st.session_state.my_name}")

# ميزة رفع الصور كرسالة (الحل النهائي للتكرار ولغوة السايدبار)
with st.sidebar.form(key='meryoum_super_up_form'):
    # أداة الرفع المتعدد بعلامة (+) فقط
    uploaded_files = st.file_uploader("+", key="final_up_meryoum", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
    # زر الإرسال كرسالة لضمان الإرسال لمرة واحدة وتصفير السايدبار
    submit_button = st.form_submit_button(label='إرسال كرسالة 📤')

    if submit_button and uploaded_files:
        iraq_time = datetime.now() + timedelta(hours=3)
        now = iraq_time.strftime("%I:%M %p")
        
        # إضافة كل الصور المختارة للمحادثة فوراً كرسائل
        for uploaded_file in uploaded_files:
            all_msgs.append({
                "name": st.session_state.my_name, 
                "msg": "", 
                "file": uploaded_file.getvalue(),
                "is_image": True,
                "time": now, 
                "seen": False
            })
        st.session_state["final_up_meryoum"] = [] # تصفير أداة الرفع لضمان عدم بقائها في السايدبار
        st.rerun()

st.sidebar.divider()
if st.sidebar.button("حذف كل الرسايل للكل 🗑️"):
    all_msgs.clear(); st.rerun()
if st.sidebar.button("تسجيل الخروج ⬅️"):
    del st.session_state.my_name; st.rerun()

st.title("Canım 🎀")

# --- عرض المحادثة ---
for i, chat in enumerate(all_msgs):
    if chat['name'] != st.session_state.my_name: chat['seen'] = True
    col_msg, col_options = st.columns([0.9, 0.1])
    with col_msg:
        with st.chat_message("user"):
            # إذا جان اكو نص نطلعه، وإذا فقط صورة نطلع الاسم
            if chat["msg"]:
                st.write(f"**{chat['name']}:** {chat['msg']}")
            else:
                st.write(f"**{chat['name']}:**")
            
            # عرض الصور الصافية كرسائل وبدون لغوة
            if "file" in chat and chat["is_image"]:
                st.image(chat["file"], use_container_width=True)
                st.download_button("حفظ 📥", chat["file"], file_name=f"Canim_{i}.png", key=f"dl_{i}")

            # الوقت والصحين الرمادية
            t = chat.get('time', '')
            s = "v v" if chat.get('seen', False) else "v"
            st.markdown(f'<div class="chat-info">{t} <span class="status-icon">{s}</span></div>', unsafe_allow_html=True)
            
    if chat['name'] == st.session_state.my_name:
        with col_options:
            if st.button("⋮", key=f"menu_{i}"):
                st.session_state[f"show_options_{i}"] = not st.session_state.get(f"show_options_{i}", False)
            if st.session_state.get(f"show_options_{i}", False):
                if st.button("🗑️", key=f"del_{i}"): all_msgs.pop(i); st.rerun()

# إرسال النص
if prompt := st.chat_input("اكتبي رسالتج هنا..."):
    iraq_time = datetime.now() + timedelta(hours=3)
    now = iraq_time.strftime("%I:%M %p")
    all_msgs.append({"name": st.session_state.my_name, "msg": prompt, "time": now, "seen": False})
    st.rerun()
