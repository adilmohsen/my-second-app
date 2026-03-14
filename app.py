import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. إعدادات الصفحة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")
st_autorefresh(interval=1000, key="chat_refresh_timer")

# 2. سحر الـ CSS (الوردي الكامل)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #FFDEE9;
        background-image: linear-gradient(0deg, #FFDEE9 0%, #B5FFFC 100%);
        background-size: cover;
    }
    [data-testid="stSidebar"] {
        background-color: #FFC0CB !important;
    }
    /* جعل مربع الدردشة وردي ناعم */
    [data-testid="stChatInput"] {
        background-color: #FFD1DC !important;
        border-radius: 20px !important;
    }
    .stChatMessage { 
        background-color: rgba(255, 255, 255, 0.8) !important; 
        border-radius: 15px; 
    }
    </style>
    """, unsafe_allow_html=True)

# 3. المخزن
@st.cache_resource
def get_global_messages(): return []
all_msgs = get_global_messages()

# تهيئة المتغيرات
if "chat_msg" not in st.session_state: st.session_state.chat_msg = ""

# --- تسجيل الدخول ---
if "my_name" not in st.session_state:
    st.title("👸 مملكة مريوم")
    name = st.text_input("اسمج الملكي:")
    if st.button("انطلاق ✨"):
        if name: st.session_state.my_name = name; st.rerun()
    st.stop()

# --- السايدبار (رجوع تسجيل الخروج والحذف) ---
with st.sidebar:
    st.title(f"👑 {st.session_state.my_name}")
    st.write("---")
    if st.button("🗑️ حذف الكل", use_container_width=True):
        all_msgs.clear(); st.rerun()
    if st.button("⬅️ تسجيل الخروج", use_container_width=True):
        del st.session_state.my_name; st.rerun()

# --- واجهة الچات ---
st.header("The Queen Meryoum Chat 🌸")

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
                if st.button("✏️", key=f"e_{i}"):
                    st.session_state.edit_idx = i; st.session_state.edit_txt = chat['msg']; st.rerun()

# نافذة التعديل
if "edit_idx" in st.session_state:
    with st.container(border=True):
        new_val = st.text_input("عدلي رسالتج:", value=st.session_state.edit_txt)
        if st.button("حفظ ✅"):
            all_msgs[st.session_state.edit_idx]['msg'] = new_val
            del st.session_state.edit_idx; st.rerun()

# --- منطقة الإرسال (الإيموجيات + المربع الثابت) ---

# قائمة الإيموجيات السريعة (تظهر فوق مربع الكتابة)
st.write("---")
emojis = ["🌸", "👑", "💖", "✨", "🎀", "😂", "🔥", "💀"]
emo_cols = st.columns(8)
for idx, emo in enumerate(emojis):
    if emo_cols[idx].button(emo, key=f"emo_{idx}"):
        # ملاحظة: st.chat_input مبيها ميزة إضافة نص برمجياً بسهولة، 
        # بس تكدرين تضغطين الإيموجي ويندز فوراً كرسالة سريعة!
        all_msgs.append({"name": st.session_state.my_name, "msg": emo})
        st.rerun()

# مربع الكتابة الثابت (st.chat_input يضمن عدم النزول جوه)
prompt = st.chat_input("اكتبي رسالتج هنا يا ملكة مريوم...")
if prompt:
    all_msgs.append({"name": st.session_state.my_name, "msg": prompt})
    st.rerun()
