import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. إعدادات الصفحة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀", layout="centered")
st_autorefresh(interval=2000, key="datarefresh")

# 2. CSS مخصص لترتيب منطقة الإرسال في الأسفل ومنع التشتت
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
    }}
    /* تنسيق منطقة الإرسال لتكون ثابتة ومرتبة */
    .footer-container {{
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 800px;
        background: rgba(255, 255, 255, 0.95);
        padding: 10px 20px;
        border-radius: 50px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .stChatMessage {{ background-color: rgba(255, 255, 255, 0.9) !important; border-radius: 15px; }}
    </style>
    """, unsafe_allow_html=True)

# 3. المخزن والبيانات
@st.cache_resource
def get_global_messages(): return []
all_msgs = get_global_messages()

# تهيئة النصوص
if "input_val" not in st.session_state: st.session_state.input_val = ""

# --- شاشة تسجيل الدخول ---
if "my_name" not in st.session_state:
    st.title("👸 مملكة مريوم")
    name = st.text_input("اسمج الملكي:")
    if st.button("دخول ✨"):
        if name: st.session_state.my_name = name; st.rerun()
    st.stop()

# --- عرض المحادثة ---
st.title("👸 The Queen Meryoum Chat 🌸")
st.write("---")

# حاوية الرسايل (نضيف مساحة بالأسفل حتى لا تغطيها الخانة)
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
                if st.button("✏️", key=f"e_{i}"): st.session_state.edit_idx = i; st.session_state.edit_txt = chat['msg']; st.rerun()

# نافذة التعديل
if "edit_idx" in st.session_state:
    with st.container(border=True):
        new_val = st.text_input("تعديل:", value=st.session_state.edit_txt)
        if st.button("حفظ ✅"):
            all_msgs[st.session_state.edit_idx]['msg'] = new_val
            del st.session_state.edit_idx; st.rerun()

st.markdown("<br><br><br><br><br>", unsafe_allow_html=True) # فراغ إضافي

# --- منطقة الإرسال (الترتيب الصحيح بالـ Columns) ---
with st.container():
    # عرض الإيموجيات فوق الخانة إذا طلبناها
    if st.session_state.get("show_emo", False):
        emojis = ["🌸", "👑", "💖", "✨", "🎀", "😂", "🔥", "💀"]
        emo_cols = st.columns(8)
        for idx, emo in enumerate(emojis):
            if emo_cols[idx].button(emo, key=f"emo_{idx}"):
                st.session_state.input_val += emo
                st.rerun()

    # سطر الإرسال: ايموجي | خانة نص | ارسال
    c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
    with c1:
        if st.button("😊"):
            st.session_state.show_emo = not st.session_state.get("show_emo", False)
            st.rerun()
    with c2:
        # نستخدم الكي للتزامن
        msg = st.text_input("Message", value=st.session_state.input_val, label_visibility="collapsed", placeholder="اكتبي هنا...")
    with c3:
        if st.button("🚀"):
            if msg:
                all_msgs.append({"name": st.session_state.my_name, "msg": msg})
                st.session_state.input_val = ""
                st.rerun()
