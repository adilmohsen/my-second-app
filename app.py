import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. إعدادات الصفحة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")
st_autorefresh(interval=1000, key="chat_refresh_timer")

# 2. سحر الـ CSS (الخلفية الوردية وكل التفاصيل)
st.markdown(f"""
    <style>
    /* الخلفية الوردية للصفحة بالكامل */
    [data-testid="stAppViewContainer"] {{
        background-color: #FFDEE9;
        background-image: linear-gradient(0deg, #FFDEE9 0%, #B5FFFC 100%); /* تدرج وردي هادئ */
        background-size: cover;
    }}
    
    /* جعل السايدبار (اليسار) وردي أيضاً */
    [data-testid="stSidebar"] {{
        background-color: #FFC0CB !important;
    }}

    /* تنسيق المستطيل الوردي للكتابة */
    .stTextInput input {{
        background-color: #FFD1DC !important;
        border-radius: 20px !important;
        border: 2px solid #FFB6C1 !important;
        color: #4B0082 !important;
        height: 45px;
    }}

    /* تنسيق فقاعات الدردشة */
    .stChatMessage {{ 
        background-color: rgba(255, 255, 255, 0.8) !important; 
        border-radius: 15px; 
        border: 1px solid #FFB6C1;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. المخزن والبيانات
@st.cache_resource
def get_global_messages(): return []
all_msgs = get_global_messages()

if "chat_msg" not in st.session_state: st.session_state.chat_msg = ""
if "show_emo" not in st.session_state: st.session_state.show_emo = False

# --- شاشة تسجيل الدخول ---
if "my_name" not in st.session_state:
    st.title("👸 مملكة مريوم")
    name = st.text_input("اسمج الملكي للدخول:", key="login_name")
    if st.button("انطلاق ✨"):
        if name: st.session_state.my_name = name; st.rerun()
    st.stop()

# --- السايدبار (اليسار) ---
with st.sidebar:
    st.title(f"👑 {st.session_state.my_name}")
    st.write("---")
    if st.button("🗑️ حذف كل الرسائل", use_container_width=True):
        all_msgs.clear(); st.rerun()
    if st.button("⬅️ تسجيل الخروج", use_container_width=True):
        del st.session_state.my_name; st.rerun()

# --- واجهة الچات ---
st.header("The Queen Meryoum Chat 🌸")

for i, chat in enumerate(all_msgs):
    col_msg, col_opt = st.columns([0.85, 0.15])
    with col_msg:
        with st.chat_message("user"): st.write(f"**{chat['name']}:** {chat['msg']}")
    
    if chat['name'] == st.session_state.my_name:
        with col_opt:
            if st.button("⋮", key=f"m_{i}"):
                st.session_state[f"o_{i}"] = not st.session_state.get(f"o_{i}", False)
            
            if st.session_state.get(f"o_{i}", False):
                if st.button("🗑️", key=f"d_{i}"): all_msgs.pop(i); st.rerun()
                if st.button("✏️", key=f"e_{i}"):
                    st.session_state.edit_idx = i
                    st.session_state.edit_txt = chat['msg']
                    st.rerun()

# نافذة التعديل
if "edit_idx" in st.session_state:
    with st.container(border=True):
        st.write("📝 تعديل رسالتج:")
        new_val = st.text_input("النص الجديد:", value=st.session_state.edit_txt)
        col_s1, col_s2 = st.columns(2)
        if col_s1.button("حفظ ✅", key="save_edit"):
            all_msgs[st.session_state.edit_idx]['msg'] = new_val
            del st.session_state.edit_idx; st.rerun()
        if col_s2.button("إلغاء ❌", key="cancel_edit"):
            del st.session_state.edit_idx; st.rerun()

st.markdown("<br><br><br><br>", unsafe_allow_html=True)

# --- منطقة الإرسال ---
if st.session_state.show_emo:
    emojis = ["🌸", "👑", "💖", "✨", "🎀", "😂", "🔥", "💀"]
    emo_cols = st.columns(8)
    for idx, emo in enumerate(emojis):
        if emo_cols[idx].button(emo, key=f"e_{idx}"):
            st.session_state.chat_msg += emo
            st.rerun()

with st.form(key="main_chat_form", clear_on_submit=True):
    c1, c2, c3 = st.columns([0.7, 0.15, 0.15])
    with c1:
        msg_input = st.text_input("Message", value=st.session_state.chat_msg, label_visibility="collapsed", placeholder="اكتبي هنا...")
    with c2:
        submit = st.form_submit_button("🚀")
    with c3:
        emo_trigger = st.form_submit_button("😊")

    if submit and msg_input:
        all_msgs.append({"name": st.session_state.my_name, "msg": msg_input})
        st.session_state.chat_msg = ""
        st.rerun()
    
    if emo_trigger:
        st.session_state.show_emo = not st.session_state.show_emo
        st.session_state.chat_msg = msg_input
        st.rerun()
