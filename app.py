import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta

# 1. إعدادات الصفحة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")
st_autorefresh(interval=1000, key="datarefresh")

# 2. التنسيقات (إجبار اللون الرمادي)
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
    }}
    .stChatMessage {{ background-color: rgba(255, 255, 255, 0.8) !important; border-radius: 15px; }}
    
    /* ستايل الوقت والصحين باللون الرمادي الموحد */
    .chat-info {{
        color: #888888 !important;
        font-size: 8px !important;
        float: right;
        margin-top: 5px;
        font-family: sans-serif;
    }}
    .status-icon {{
        color: #888888 !important;
        margin-left: 2px;
        font-size: 9px !important;
    }}
    
    .stButton button {{ border: none !important; background: transparent !important; color: #888 !important; font-size: 20px !important; }}
    </style>
    """, unsafe_allow_html=True)

# 3. المخزن المشترك
@st.cache_resource
def get_global_messages(): return []
all_msgs = get_global_messages()

# --- شاشة تسجيل الدخول ---
if "my_name" not in st.session_state:
    st.title("🎀 أهلاً بيج بالچات الوردي")
    name_input = st.text_input("اسمج هنا:")
    if st.button("دخول"):
        if name_input: st.session_state.my_name = name_input; st.rerun()
    st.stop()

# --- القائمة الجانبية ---
st.sidebar.title(f"الملكة {st.session_state.my_name}")
if st.sidebar.button("حذف كل الرسايل للكل 🗑️"):
    all_msgs.clear(); st.rerun()
if st.sidebar.button("تسجيل الخروج ⬅️"):
    del st.session_state.my_name; st.rerun()

st.title("🎀 محادثة مريوم المشتركة")

# --- عرض الرسائل ---
for i, chat in enumerate(all_msgs):
    if chat['name'] != st.session_state.my_name: chat['seen'] = True
    col_msg, col_options = st.columns([0.9, 0.1])
    with col_msg:
        with st.chat_message("user"):
            st.write(f"**{chat['name']}:** {chat['msg']}")
            msg_time = chat.get('time', '') 
            # استخدمنا رمز v بدلاً من الإيموجي لضمان ثبات اللون
            status_text = "v v" if chat.get('seen', False) else "v"
            
            st.markdown(f'''
                <div class="chat-info">
                    {msg_time} <span class="status-icon">{status_text}</span>
                </div>
            ''', unsafe_allow_html=True)
            
    if chat['name'] == st.session_state.my_name:
        with col_options:
            if st.button("⋮", key=f"menu_{i}"):
                st.session_state[f"show_options_{i}"] = not st.session_state.get(f"show_options_{i}", False)
            if st.session_state.get(f"show_options_{i}", False):
                if st.button("🗑️", key=f"del_{i}"): all_msgs.pop(i); st.rerun()
                if st.button("✏️", key=f"edit_{i}"):
                    st.session_state.edit_index = i
                    st.session_state.edit_text = chat['msg']
                    st.session_state[f"show_options_{i}"] = False; st.rerun()

if "edit_index" in st.session_state:
    st.divider()
    new_text = st.text_input("تعديل رسالتج:", value=st.session_state.edit_text)
    if st.button("حفظ التعديل ✅"):
        all_msgs[st.session_state.edit_index]['msg'] = new_text
        del st.session_state.edit_index; st.rerun()

if prompt := st.chat_input("اكتبي رسالتج هنا..."):
    iraq_time = datetime.now() + timedelta(hours=3)
    now = iraq_time.strftime("%I:%M %p")
    all_msgs.append({"name": st.session_state.my_name, "msg": prompt, "time": now, "seen": False})
    st.rerun()
