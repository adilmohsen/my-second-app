import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. إعدادات الصفحة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")
st_autorefresh(interval=2000, key="datarefresh")

# 2. سحر الـ CSS (لتثبيت الخانة أسفل الشاشة وتنسيق الأزرار)
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
        padding-bottom: 100px; /* مسافة حتى الرسايل ما تختفي ورا الخانة الثابتة */
    }}
    .stChatMessage {{ background-color: rgba(255, 255, 255, 0.9) !important; border-radius: 15px; }}
    
    /* تثبيت حاوية الإرسال في الأسفل */
    div[data-testid="stVerticalBlock"] > div:last-child {{
        position: fixed;
        bottom: 10px;
        background: white;
        padding: 10px;
        border-radius: 30px;
        box-shadow: 0px -2px 10px rgba(0,0,0,0.1);
        z-index: 1000;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. المخزن والبيانات
@st.cache_resource
def get_global_messages(): return []
all_msgs = get_global_messages()

# تهيئة الحالات
if "temp_msg" not in st.session_state: st.session_state.temp_msg = ""

# --- شاشة تسجيل الدخول ---
if "my_name" not in st.session_state:
    st.title("👸 مملكة مريوم")
    name = st.text_input("اسمج الملكي:")
    if st.button("دخول ✨"):
        if name: st.session_state.my_name = name; st.rerun()
    st.stop()

# --- عرض المحادثة ---
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
                if st.button("✏️", key=f"e_{i}"): st.session_state.edit_idx = i; st.session_state.edit_txt = chat['msg']; st.rerun()

# نافذة التعديل
if "edit_idx" in st.session_state:
    with st.container(border=True):
        new_val = st.text_input("تعديل:", value=st.session_state.edit_txt)
        if st.button("حفظ ✅"):
            all_msgs[st.session_state.edit_idx]['msg'] = new_val
            del st.session_state.edit_idx; st.rerun()

# --- منطقة الإرسال الثابتة (مثل التليجرام) ---
st.markdown("---") # فاصل بصري
footer = st.container()
with footer:
    # عرض الإيموجيات إذا تم الضغط على الزر
    if st.session_state.get("show_emo", False):
        emojis = ["🌸", "👑", "💖", "✨", "🎀", "😂", "🔥", "💀"]
        emo_cols = st.columns(8)
        for idx, emo in enumerate(emojis):
            if emo_cols[idx].button(emo, key=f"btn_e_{idx}"):
                st.session_state.temp_msg += emo
                st.rerun()

    # السطر الأخير: إيموجي + نص + إرسال
    c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
    with c1:
        if st.button("😊", help="إيموجيات"):
            st.session_state.show_emo = not st.session_state.get("show_emo", False)
            st.rerun()
    with c2:
        # الخانة الوحيدة للكتابة
        msg_input = st.text_input("Message", value=st.session_state.temp_msg, label_visibility="collapsed", placeholder="اكتبي رسالتج هنا...")
    with c3:
        if st.button("🚀"):
            if msg_input:
                all_msgs.append({"name": st.session_state.my_name, "msg": msg_input})
                st.session_state.temp_msg = "" # تصفير
                st.rerun()
