import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. إعدادات الصفحة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")
st_autorefresh(interval=2000, key="datarefresh")

# 2. سحر الـ CSS (الخلفية الوردية + المستطيل الوردي المرتب)
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
    }}
    
    /* تنسيق مستطيل الكتابة الوردي */
    .stTextInput input {{
        background-color: #FFD1DC !important; /* وردي ملكي */
        border-radius: 15px !important;
        border: 2px solid #FFB6C1 !important;
        color: #4B0082 !important;
        height: 45px;
    }}

    /* تنسيق الرسائل */
    .stChatMessage {{ 
        background-color: rgba(255, 255, 255, 0.9) !important; 
        border-radius: 15px; 
    }}

    /* حاوية الإرسال في الأسفل مع مسافة بسيطة */
    .footer-fixed {{
        position: fixed;
        bottom: 20px;
        left: 10%;
        right: 10%;
        z-index: 1000;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. المخزن والبيانات
@st.cache_resource
def get_global_messages(): return []
all_msgs = get_global_messages()

# تهيئة النص في الـ session_state
if "input_val" not in st.session_state: st.session_state.input_val = ""

# --- شاشة تسجيل الدخول ---
if "my_name" not in st.session_state:
    st.title("👸 مملكة مريوم")
    name = st.text_input("اسمج الملكي للدخول:")
    if st.button("انطلاق للمملكة ✨"):
        if name: st.session_state.my_name = name; st.rerun()
    st.stop()

# --- القائمة الجانبية (اليسار) ---
with st.sidebar:
    st.title(f"👑 {st.session_state.my_name}")
    st.write("---")
    if st.button("🗑️ حذف كل الرسائل", use_container_width=True):
        all_msgs.clear(); st.rerun()
    if st.button("⬅️ تسجيل الخروج", use_container_width=True):
        del st.session_state.my_name; st.rerun()

# --- واجهة الچات ---
st.title("👸 The Queen Meryoum Chat 🌸")

# عرض الرسائل
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

st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True) # فراغ للرسايل

# --- منطقة الإرسال (المستطيل الوردي + الإيموجي بصف الصاروخ) ---
with st.container():
    # قائمة الإيموجيات (تظهر فوق المستطيل عند الضغط)
    if st.session_state.get("show_emo", False):
        emojis = ["🌸", "👑", "💖", "✨", "🎀", "😂", "🔥", "💀"]
        emo_cols = st.columns(8)
        for idx, emo in enumerate(emojis):
            if emo_cols[idx].button(emo, key=f"e_{idx}"):
                st.session_state.input_val += emo
                st.rerun()

    # السطر الأساسي: مستطيل وردي | صاروخ | إيموجي
    c1, c2, c3 = st.columns([0.7, 0.15, 0.15])
    
    with c1:
        msg_input = st.text_input("Message", value=st.session_state.input_val, key="main_input", label_visibility="collapsed", placeholder="اكتبي رسالتج هنا...")

    with c2:
        if st.button("🚀"):
            if msg_input:
                all_msgs.append({"name": st.session_state.my_name, "msg": msg_input})
                st.session_state.input_val = "" # تصفير
                st.rerun()
    
    with c3:
        if st.button("😊"):
            st.session_state.show_emo = not st.session_state.get("show_emo", False)
            st.rerun()
