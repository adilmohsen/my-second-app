import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta

# 1. إعدادات الصفحة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")
st_autorefresh(interval=1000, key="datarefresh")

# 2. التنسيقات (إخفاء كل شيء وبقاء علامة + فقط)
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

    /* ستايل علامة الـ + السحرية */
    section[data-testid="stSidebar"] .stFileUploader label {{
        font-size: 40px !important; color: #888 !important; display: block !important; text-align: center; cursor: pointer;
    }}
    section[data-testid="stSidebar"] .stFileUploader section {{ padding: 0 !important; border: none !important; background: transparent !important; }}
    /* إخفاء زر Browse وكل النصوص المزعجة */
    section[data-testid="stSidebar"] .stFileUploader section > div {{ display: none !important; }}
    section[data-testid="stSidebar"] .stFileUploader [data-testid="stMarkdownContainer"] {{ display: none !important; }}
    </style>
    """, unsafe_allow_html=True)

# 3. المخزن المشترك
@st.cache_resource
def get_global_messages(): return []
all_msgs = get_global_messages()

# وظيفة الإرسال التلقائي للصور
def upload_callback():
    if st.session_state.up_files:
        now = (datetime.now() + timedelta(hours=3)).strftime("%I:%M %p")
        for f in st.session_state.up_files:
            all_msgs.append({
                "name": st.session_state.my_name, 
                "msg": "", 
                "file": f.getvalue(), 
                "is_image": True, 
                "time": now, 
                "seen": False
            })
        # تصفير الأداة بعد الرفع كبل
        st.session_state.up_files = []

# --- تسجيل الدخول ---
if "my_name" not in st.session_state:
    st.title("🎀 أهلاً بيج بالچات الوردي")
    name_input = st.text_input("اسمج هنا:")
    if st.button("دخول"):
        if name_input: st.session_state.my_name = name_input; st.rerun()
    st.stop()

# --- القائمة الجانبية (علامة + فقط) ---
st.sidebar.title(f"الملكة {st.session_state.my_name}")

# أداة الرفع السحرية (بدون فورم وبدون أزرار)
st.sidebar.file_uploader("+", key="up_files", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True, on_change=upload_callback)

st.sidebar.divider()
if st.sidebar.button("حذف الكل 🗑️"): all_msgs.clear(); st.rerun()
if st.sidebar.button("خروج ⬅️"): del st.session_state.my_name; st.rerun()

st.title("Canım 🎀")

# --- عرض المحادثة ---
for i, chat in enumerate(all_msgs):
    if chat['name'] != st.session_state.my_name: chat['seen'] = True
    col_msg, col_options = st.columns([0.85, 0.15])
    
    with col_msg:
        with st.chat_message("user"):
            # الاسم والرسالة بنفس السطر
            if chat["msg"]:
                st.write(f"**{chat['name']}:** {chat['msg']}")
            else:
                st.write(f"**{chat['name']}:**")
            
            if "file" in chat and chat["is_image"]:
                st.image(chat["file"], use_container_width=True)
                st.download_button("حفظ 📥", chat["file"], file_name=f"Canim_{i}.png", key=f"dl_{i}")
            
            t, s = chat.get('time', ''), ("v v" if chat.get('seen', False) else "v")
            st.markdown(f'<div class="chat-info">{t} <span class="status-icon">{s}</span></div>', unsafe_allow_html=True)
            
    if chat['name'] == st.session_state.my_name:
        with col_options:
            if st.button("⋮", key=f"menu_{i}"):
                st.session_state[f"opt_{i}"] = not st.session_state.get(f"opt_{i}", False)
            if st.session_state.get(f"opt_{i}", False):
                if st.button("🗑️", key=f"del_{i}"): all_msgs.pop(i); st.rerun()
                if chat["msg"] and st.button("✏️", key=f"ed_{i}"):
                    st.session_state.edit_idx = i
                    st.session_state.edit_val = chat['msg']
                    st.session_state[f"opt_{i}"] = False; st.rerun()

# --- واجهة التعديل ---
if "edit_idx" in st.session_state:
    st.divider()
    new_txt = st.text_input("تعديل الرسالة:", value=st.session_state.edit_val)
    if st.button("حفظ ✅"):
        all_msgs[st.session_state.edit_idx]['msg'] = new_txt
        del st.session_state.edit_idx; st.rerun()

# إرسال نص جديد
if prompt := st.chat_input("اكتبي رسالتج هنا..."):
    now = (datetime.now() + timedelta(hours=3)).strftime("%I:%M %p")
    all_msgs.append({"name": st.session_state.my_name, "msg": prompt, "time": now, "seen": False})
    st.rerun()
