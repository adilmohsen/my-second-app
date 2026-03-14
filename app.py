import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. إعدادات الصفحة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")
st_autorefresh(interval=1000, key="chat_refresh_timer")

# 2. سحر الـ CSS (لضبط الألوان الوردية وموقع الإيموجي)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #FFDEE9;
        background-image: linear-gradient(0deg, #FFDEE9 0%, #B5FFFC 100%);
        background-size: cover;
    }
    /* جعل مربع الدردشة وردي فاتح مثل طلبج */
    [data-testid="stChatInput"] {
        background-color: #FFF0F5 !important;
        border-radius: 25px !important;
        border: 1px solid #FFB6C1 !important;
    }
    .stChatMessage { 
        background-color: rgba(255, 255, 255, 0.8) !important; 
        border-radius: 15px; 
    }
    /* تحسين شكل أزرار الإيموجي السريعة */
    .stButton button {
        border-radius: 50% !important;
        padding: 5px !important;
        background-color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. المخزن
@st.cache_resource
def get_global_messages(): return []
all_msgs = get_global_messages()

if "show_emojis" not in st.session_state: st.session_state.show_emojis = False

# --- تسجيل الدخول ---
if "my_name" not in st.session_state:
    st.title("👸 مملكة مريوم")
    name = st.text_input("اسمج الملكي:")
    if st.button("انطلاق ✨"):
        if name: st.session_state.my_name = name; st.rerun()
    st.stop()

# --- السايدبار (تسجيل الخروج وحذف الكل) ---
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

# --- منطقة الإرسال (مستطيل وردي + إيموجي جانبي) ---

# حاوية الإيموجيات تظهر فقط عند الطلب
if st.session_state.show_emojis:
    st.write("---")
    emo_cols = st.columns(8)
    emojis = ["🌸", "👑", "💖", "✨", "🎀", "😂", "🔥", "💀"]
    for idx, emo in enumerate(emojis):
        if emo_cols[idx].button(emo, key=f"emo_{idx}"):
            all_msgs.append({"name": st.session_state.my_name, "msg": emo})
            st.session_state.show_emojis = False # إغلاق القائمة بعد الاختيار
            st.rerun()

# ترتيب المربع مع زر الإيموجي بجانبه
c1, c2 = st.columns([0.9, 0.1])
with c2:
    # زر الإيموجي الدائري بجانب المربع بالضبط مثل طلبج
    if st.button("😊", key="emoji_trigger"):
        st.session_state.show_emojis = not st.session_state.show_emojis
        st.rerun()

with c1:
    prompt = st.chat_input("اكتبي رسالتج هنا يا ملكة...")
    if prompt:
        all_msgs.append({"name": st.session_state.my_name, "msg": prompt})
        st.rerun()
