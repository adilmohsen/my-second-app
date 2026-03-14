import streamlit as st
import os

# إعدادات الصفحة
st.set_page_config(page_title="تطبيق مريوم الحِلوه", page_icon="🎀")

# إضافة الخلفية الوردية وتنسيق فقاعات المراسلة
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
        background-attachment: fixed;
    }}
    /* تنسيق فقاعة المرسل على اليمين */
    [data-testid="stChatMessage"]:nth-child(even) {{
        background-color: #fce4ec !important;
        flex-direction: row-reverse !important;
        text-align: right !important;
    }}
    </style>
    """, unsafe_allow_html=True)

st.title("🎀 تطبيق مريوم الحِلوه")

# نظام الدخول
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.username:
    name = st.text_input("ادخلي اسمج المميز لبدء المراسلة:")
    if st.button("دخول"):
        if name:
            st.session_state.username = name
            st.rerun()
else:
    # القائمة الجانبية للملفات
    with st.sidebar:
        st.header(f"👤 {st.session_state.username}")
        st.divider()
        uploaded_file = st.file_uploader("📎 إرسال ملف أو صورة", type=['png', 'jpg', 'jpeg', 'pdf'])
        if uploaded_file:
            st.success(f"تم تحميل الملف بنجاح")

    # خزن وعرض الرسائل
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(f"**{msg['user']}:** {msg['content']}")

    # صندوق المراسلة (بدون رد تلقائي)
    if prompt := st.chat_input("اكتبي رسالتج هنا..."):
        # إضافة الرسالة فقط بدون أي إشعار أو رد
        st.session_state.messages.append({"role": "user", "user": st.session_state.username, "content": prompt})
        st.rerun()
