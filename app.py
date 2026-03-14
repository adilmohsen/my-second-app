import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. إعدادات الصفحة الفخمة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")

# 2. التحديث التلقائي (كل ثانيتين)
st_autorefresh(interval=2000, key="datarefresh")

# 3. ستايل الـ CSS للخلفية والفقاعات والوضوح
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
        background-position: center;
    }}
    /* تنسيق الرسائل لتكون واضحة جداً */
    .stChatMessage {{
        background-color: rgba(255, 255, 255, 0.85) !important;
        border: 1px solid #FFB6C1;
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 5px;
        color: #4B0082;
    }}
    /* تنسيق أزرار الإيموجيات */
    .stButton>button {{
        border-radius: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. مخزن الرسائل المشترك
@st.cache_resource
def get_global_messages():
    return []

all_msgs = get_global_messages()

# --- شاشة تسجيل الدخول ---
if "my_name" not in st.session_state:
    st.title("👸 مملكة مريوم الورديّة")
    name_input = st.text_input("اكتبي اسمج الملكي للدخول:")
    if st.button("انطلاق للچات 🚀"):
        if name_input:
            st.session_state.my_name = name_input
            st.rerun()
        else:
            st.warning("لازم تكتبين اسمج أولاً! 🌸")
    st.stop()

# --- القائمة الجانبية (Sidebar) ---
st.sidebar.title(f"الملكة {st.session_state.my_name} ✨")
st.sidebar.markdown("---")
if st.sidebar.button("مسح السجل بالكامل 🗑️"):
    all_msgs.clear()
    st.rerun()

if st.sidebar.button("تسجيل الخروج ⬅️"):
    del st.session_state.my_name
    st.rerun()

# --- واجهة الچات الرئيسية ---
st.title("👸 The Queen Meryoum Chat 🌸")

# عرض الرسائل مع أزرار التحكم
for i, chat in enumerate(all_msgs):
    col1, col2, col3 = st.columns([0.74, 0.13, 0.13])
    
    with col1:
        with st.chat_message("user"):
            st.write(f"**{chat['name']}:** {chat['msg']}")
            
    # أزرار الحذف والتعديل تظهر فقط لصاحب الرسالة
    if chat['name'] == st.session_state.my_name:
        with col2:
            if st.button("🗑️", key=f"del_{i}", help="حذف"):
                all_msgs.pop(i)
                st.rerun()
        with col3:
            if st.button("✏️", key=f"edit_{i}", help="تعديل"):
                st.session_state.edit_index = i
                st.session_state.edit_text = chat['msg']

# نافذة التعديل (تظهر عند الضغط على القلم)
if "edit_index" in st.session_state:
    st.info("وضع التعديل نشط الآن ✍️")
    new_text = st.text_input("عدلي رسالتج هنا:", value=st.session_state.edit_text)
    c_edit1, c_edit2 = st.columns(2)
    if c_edit1.button("حفظ التعديل ✅"):
        all_msgs[st.session_state.edit_index]['msg'] = new_text
        del st.session_state.edit_index
        st.rerun()
    if c_edit2.button("إلغاء ❌"):
        del st.session_state.edit_index
        st.rerun()

st.divider()

# --- قسم الإيموجيات السريعة ---
st.write("إيموجيات سريعة للملكة 🎀:")
emo_cols = st.columns(8)
quick_emojis = ["🌸", "👑", "💖", "✨", "🎀", "🦄", "🍭", "🦋"]
for i, emo in enumerate(quick_emojis):
    if emo_cols[i].button(emo, key=f"quick_emo_{i}"):
        st.toast(f"تم اختيار {emo}، انسخيه وضيفيه لرسالتج!")

# --- خانة الكتابة ---
if prompt := st.chat_input("اكتبي رسالتج هنا يا ملكة..."):
    all_msgs.append({"name": st.session_state.my_name, "msg": prompt})
    st.rerun()
