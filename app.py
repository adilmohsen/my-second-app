import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. إعدادات الصفحة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")
st_autorefresh(interval=2000, key="datarefresh")

# 2. ستايل الـ CSS لتثبيت منطقة الإرسال في الأسفل
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
    }}
    .stChatMessage {{ background-color: rgba(255, 255, 255, 0.9) !important; border-radius: 15px; }}
    
    /* ستايل لتثبيت منطقة الإرسال في الأسفل */
    .fixed-bottom {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: white;
        padding: 20px;
        border-top: 1px solid #FFB6C1;
        z-index: 1000;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. المخزن والبيانات
@st.cache_resource
def get_global_messages(): return []
all_msgs = get_global_messages()

# تهيئة النص في الـ session_state
if "user_input" not in st.session_state: st.session_state.user_input = ""

# --- شاشة تسجيل الدخول ---
if "my_name" not in st.session_state:
    st.title("👸 مملكة مريوم")
    name = st.text_input("اسمج الملكي:")
    if st.button("دخول ✨"):
        if name: st.session_state.my_name = name; st.rerun()
    st.stop()

# --- واجهة الچات ---
st.title("👸 The Queen Meryoum Chat 🌸")

# عرض الرسائل (نخليها بداخل حاوية حتى تترتب)
chat_container = st.container()
with chat_container:
    for i, chat in enumerate(all_msgs):
        col_msg, col_opt = st.columns([0.85, 0.15])
        with col_msg:
            with st.chat_message("user"): st.write(f"**{chat['name']}:** {chat['msg']}")
        
        if chat['name'] == st.session_state.my_name:
            with col_opt:
                if st.button("⋮", key=f"menu_{i}"):
                    st.session_state[f"opt_{i}"] = not st.session_state.get(f"opt_{i}", False)
                if st.session_state.get(f"opt_{i}", False):
                    if st.button("🗑️", key=f"del_{i}"):
                        all_msgs.pop(i); st.rerun()
                    if st.button("✏️", key=f"ed_{i}"):
                        st.session_state.edit_idx = i; st.session_state.edit_txt = chat['msg']; st.rerun()

# نافذة التعديل (تظهر فوق منطقة الإرسال)
if "edit_idx" in st.session_state:
    with st.container(border=True):
        new_val = st.text_input("تعديل الرسالة:", value=st.session_state.edit_txt)
        if st.button("حفظ التعديل ✅"):
            all_msgs[st.session_state.edit_idx]['msg'] = new_val
            del st.session_state.edit_idx; st.rerun()

st.write("---") # فاصل قبل منطقة الإرسال

# --- منطقة الإرسال (تلقائياً تكون في الأسفل بـ Streamlit) ---
with st.container(border=True):
    # الإيموجيات تظهر وتختفي
    if st.button("😊 إيموجيات"):
        st.session_state.show_emo = not st.session_state.get("show_emo", False)

    if st.session_state.get("show_emo", False):
        emojis = ["🌸", "👑", "💖", "✨", "🎀", "😂", "🔥", "💀"]
        emo_cols = st.columns(8)
        for idx, emo in enumerate(emojis):
            if emo_cols[idx].button(emo, key=f"e_{idx}"):
                # تحديث النص وإضافة الإيموجي مباشرة
                st.session_state.user_input = st.session_state.main_input + emo
                st.rerun()

    # خانة الكتابة (مربوطة بالـ session_state)
    msg_txt = st.text_input("اكتبي رسالتج هنا...", value=st.session_state.user_input, key="main_input")

    if st.button("إرسال الرسالة 🚀", use_container_width=True):
        if msg_txt:
            all_msgs.append({"name": st.session_state.my_name, "msg": msg_txt})
            st.session_state.user_input = "" # تصفير
            st.rerun()
