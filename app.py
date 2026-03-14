import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. إعدادات الصفحة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")
st_autorefresh(interval=2000, key="datarefresh")

# 2. سحر الـ CSS (للتنسيق وتثبيت الأزرار بصف الخانة)
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
    }}
    /* تنسيق الخانة الصفراء */
    [data-testid="stChatInput"] textarea {{
        background-color: #F0E68C !important;
        border-radius: 20px !important;
    }}
    /* زر الصاروخ */
    [data-testid="stChatInput"] button {{
        background-color: #F0E68C !important;
        border-radius: 50% !important;
    }}
    .stChatMessage {{ background-color: rgba(255, 255, 255, 0.9) !important; border-radius: 15px; }}
    
    /* جعل القائمة المنسدلة تبدو كأنها جزء من منطقة الإرسال */
    .stExpander {{
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 15px !important;
        border: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. المخزن والبيانات
@st.cache_resource
def get_global_messages(): return []
all_msgs = get_global_messages()

# --- شاشة تسجيل الدخول ---
if "my_name" not in st.session_state:
    st.title("👸 مملكة مريوم")
    name = st.text_input("اسمج الملكي:")
    if st.button("دخول ✨"):
        if name: st.session_state.my_name = name; st.rerun()
    st.stop()

# --- القائمة الجانبية (جهة اليسار كما طلبتِ) ---
with st.sidebar:
    st.title(f"👑 {st.session_state.my_name}")
    st.write("---")
    if st.button("🗑️ حذف كل الرسائل", use_container_width=True):
        all_msgs.clear(); st.rerun()
    if st.button("⬅️ تسجيل الخروج", use_container_width=True):
        del st.session_state.my_name; st.rerun()

# --- واجهة الچات ---
st.title("👸 The Queen Meryoum Chat 🌸")

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

# --- منطقة الإرسال مع الإيموجي الذكي ---

# سوينا حاوية وحدة تجمع الإيموجي والخانة
input_container = st.container()

with input_container:
    # 1. زر الإيموجي الواحد اللي يفتح الباقين (استخدمنا Expander)
    with st.expander("😊"):
        emojis = ["🌸", "👑", "💖", "✨", "🎀", "😂", "🔥", "💀"]
        emo_cols = st.columns(8)
        for idx, emo in enumerate(emojis):
            if emo_cols[idx].button(emo, key=f"emo_{idx}"):
                st.toast(f"نسختِ {emo}؟ ضيفيه لرسالتج!")

    # 2. خانة الإرسال (تلقائياً بصفها سهم الإرسال)
    if prompt := st.chat_input("اكتبي رسالتج هنا..."):
        all_msgs.append({"name": st.session_state.my_name, "msg": prompt})
        st.rerun()

# نافذة التعديل
if "edit_idx" in st.session_state:
    with st.container(border=True):
        new_val = st.text_input("تعديل:", value=st.session_state.edit_txt)
        if st.button("حفظ ✅"):
            all_msgs[st.session_state.edit_idx]['msg'] = new_val
            del st.session_state.edit_idx; st.rerun()
