import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. إعدادات الصفحة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")
st_autorefresh(interval=2000, key="datarefresh")

# 2. سحر الـ CSS (الخلفية الوردية + المستطيل الوردي جوه)
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
    }}
    
    /* تثبيت منطقة الإرسال في الأسفل وتنسيقها */
    [data-testid="stVerticalBlock"] > div:last-child {{
        position: fixed;
        bottom: 0px;
        background-color: white;
        padding: 10px;
        z-index: 1000;
    }}

    /* تحويل لون مستطيل الكتابة للوردي مثل ما ردتِ */
    .stTextInput input {{
        background-color: #FFC0CB !important; /* وردي فاتح */
        border-radius: 20px !important;
        color: black !important;
        border: 2px solid #FFB6C1 !important;
    }}

    .stChatMessage {{ background-color: rgba(255, 255, 255, 0.9) !important; border-radius: 15px; }}
    </style>
    """, unsafe_allow_html=True)

# 3. المخزن
@st.cache_resource
def get_global_messages(): return []
all_msgs = get_global_messages()

# تهيئة النص في الـ session_state
if "input_text" not in st.session_state: st.session_state.input_text = ""

# --- شاشة تسجيل الدخول ---
if "my_name" not in st.session_state:
    st.title("👸 مملكة مريوم")
    name = st.text_input("اسمج الملكي للدخول:")
    if st.button("انطلاق ✨"):
        if name: st.session_state.my_name = name; st.rerun()
    st.stop()

# --- القائمة الجانبية (اليسار) ---
with st.sidebar:
    st.title(f"👑 {st.session_state.my_name}")
    if st.button("🗑️ حذف الكل", use_container_width=True):
        all_msgs.clear(); st.rerun()
    if st.button("⬅️ خروج", use_container_width=True):
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

# --- منطقة الإرسال (مثل الصورة بالضبط) ---
st.markdown("<br><br><br><br>", unsafe_allow_html=True) # مسافة للرسايل

# عرض الإيموجيات فوق الزر إذا ضغطتِ عليه
if st.session_state.get("show_emo", False):
    emojis = ["🌸", "👑", "💖", "✨", "🎀", "😂", "🔥", "💀"]
    emo_cols = st.columns(8)
    for idx, emo in enumerate(emojis):
        if emo_cols[idx].button(emo, key=f"e_{idx}"):
            st.session_state.input_text += emo
            st.rerun()

# السطر الأخير: المستطيل الوردي | سهم الإرسال | زر الإيموجي
c1, c2, c3 = st.columns([0.75, 0.1, 0.15])

with c1:
    # المستطيل الوردي (ينكتب بي الإيموجي فوراً)
    msg_input = st.text_input("Message", value=st.session_state.input_text, key="main_input", label_visibility="collapsed", placeholder="اكتبي رسالتج هنا...")

with c2:
    # زر الإرسال (الصاروخ)
    if st.button("🚀"):
        if msg_input:
            all_msgs.append({"name": st.session_state.my_name, "msg": msg_input})
            st.session_state.input_text = ""
            st.rerun()

with c3:
    # زر الإيموجي بصف الصاروخ (مثل الرسمة مالتج)
    if st.button("😊"):
        st.session_state.show_emo = not st.session_state.get("show_emo", False)
        st.rerun()
