import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. إعدادات الصفحة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")

# 2. التحديث التلقائي
st_autorefresh(interval=2000, key="datarefresh")

# 3. الستايل (CSS) للجمالية والوضوح
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
    }}
    .stChatMessage {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px;
        padding: 10px;
        color: #4B0082;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. المخزن المشترك
@st.cache_resource
def get_global_messages():
    return []

all_msgs = get_global_messages()

# --- الدخول ---
if "my_name" not in st.session_state:
    st.title("👸 مملكة مريوم")
    name_input = st.text_input("اسمج الملكي:")
    if st.button("دخول ✨"):
        if name_input:
            st.session_state.my_name = name_input
            st.rerun()
    st.stop()

# --- القائمة الجانبية ---
st.sidebar.title(f"الملكة {st.session_state.my_name} ✨")
if st.sidebar.button("مسح السجل 🗑️"):
    all_msgs.clear()
    st.rerun()

# --- واجهة الچات ---
st.title("👸 The Queen Meryoum Chat 🌸")

for i, chat in enumerate(all_msgs):
    col_msg, col_opt = st.columns([0.85, 0.15])
    
    with col_msg:
        with st.chat_message("user"):
            st.write(f"**{chat['name']}:** {chat['msg']}")
            
    # خاصية الـ 3 نقاط (تظهر فقط لصاحب الرسالة)
    if chat['name'] == st.session_state.my_name:
        with col_opt:
            if st.button("⋮", key=f"menu_{i}"):
                st.session_state[f"show_options_{i}"] = not st.session_state.get(f"show_options_{i}", False)
            
            if st.session_state.get(f"show_options_{i}", False):
                if st.button("🗑️ حذف", key=f"real_del_{i}"):
                    all_msgs.pop(i)
                    del st.session_state[f"show_options_{i}"]
                    st.rerun()
                if st.button("✏️ تعديل", key=f"real_edit_{i}"):
                    st.session_state.edit_index = i
                    st.session_state.edit_text = chat['msg']
                    del st.session_state[f"show_options_{i}"]
                    st.rerun()

# نافذة التعديل
if "edit_index" in st.session_state:
    st.info("تعديل الرسالة ✍️")
    new_text = st.text_input("النص الجديد:", value=st.session_state.edit_text)
    if st.button("حفظ ✅"):
        all_msgs[st.session_state.edit_index]['msg'] = new_text
        del st.session_state.edit_index
        st.rerun()

st.divider()

# --- زر الإيموجيات المدمج بصف الإرسال ---
col_emoji, col_input = st.columns([0.1, 0.9])

with col_emoji:
    if st.button("😊", help="إيموجيات"):
        st.session_state.show_emojis = not st.session_state.get("show_emojis", False)

if st.session_state.get("show_emojis", False):
    emojis = ["🌸", "👑", "💖", "✨", "🎀", "😂", "🔥", "💀"]
    emo_cols = st.columns(8)
    for idx, emo in enumerate(emojis):
        if emo_cols[idx].button(emo, key=f"q_emo_{idx}"):
            st.toast(f"تم نسخ {emo}!") # تذكير للملكة بالنسخ

with col_input:
    if prompt := st.chat_input("اكتبي رسالتج هنا يا ملكة..."):
        all_msgs.append({"name": st.session_state.my_name, "msg": prompt})
        st.rerun()
