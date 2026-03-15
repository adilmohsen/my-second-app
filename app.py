import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta # ضفنا timedelta هنا

st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")
st_autorefresh(interval=1000, key="datarefresh")

st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
    }}
    .stChatMessage {{ background-color: rgba(255, 255, 255, 0.8) !important; border-radius: 15px; }}
    .time-style {{ font-size: 10px; color: #888; float: right; margin-top: 5px; }}
    .status-style {{ font-size: 12px; color: #34B7F1; float: right; margin-left: 5px; }}
    .stButton button {{ border: none !important; background: transparent !important; color: #888 !important; font-size: 20px !important; }}
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def get_global_messages(): return []
all_msgs = get_global_messages()

if "my_name" not in st.session_state:
    st.title("🎀 أهلاً بيج بالچات الوردي")
    name_input = st.text_input("اسمج هنا:")
    if st.button("دخول"):
        if name_input: st.session_state.my_name = name_input; st.rerun()
    st.stop()

st.sidebar.title(f"الملكة {st.session_state.my_name}")
if st.sidebar.button("حذف كل الرسايل للكل 🗑️"):
    all_msgs.clear(); st.rerun()

st.title("🎀 محادثة مريوم المشتركة")

for i, chat in enumerate(all_msgs):
    if chat['name'] != st.session_state.my_name: chat['seen'] = True
    col_msg, col_options = st.columns([0.9, 0.1])
    with col_msg:
        with st.chat_message("user"):
            st.write(f"**{chat['name']}:** {chat['msg']}")
            msg_time = chat.get('time', '') 
            status_icon = "✔️✔️" if chat.get('seen', False) else "✔️"
            st.markdown(f'<div class="time-style">{msg_time} <span class="status-style">{status_icon}</span></div>', unsafe_allow_html=True)
            
    if chat['name'] == st.session_state.my_name:
        with col_options:
            if st.button("⋮", key=f"menu_{i}"):
                st.session_state[f"show_options_{i}"] = not st.session_state.get(f"show_options_{i}", False)
            if st.session_state.get(f"show_options_{i}", False):
                if st.button("🗑️", key=f"del_{i}"): all_msgs.pop(i); st.rerun()

if prompt := st.chat_input("اكتبي رسالتج هنا..."):
    # هنا التعديل: إضافة 3 ساعات لتوقيت العراق
    iraq_time = datetime.now() + timedelta(hours=3)
    now = iraq_time.strftime("%I:%M %p")
    
    all_msgs.append({"name": st.session_state.my_name, "msg": prompt, "time": now, "seen": False})
    st.rerun()
