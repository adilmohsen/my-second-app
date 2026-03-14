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
    /* تنسيق فقاعة المستخدم (المرسل) على اليمين */
    .stChatMessage:nth-child(even) {{
        background-color: #fce4ec !important;
        border-radius: 15px 15px 0px 15px !important;
        margin-left: auto !important;
        width: fit-content !important;
        max-width: 80% !important;
    }}
    /* تنسيق فقاعة الرد (المستلم) على اليسار */
    .stChatMessage:nth-child(odd) {{
        background-color: #ffffff !important;
        border-radius: 15px 15px 15px 0px !important;
        width: fit-content !important;
        max-width: 80% !important;
    }}
    </style>
    """, unsafe_allow_html=True)

st.title("🎀 تطبيق مريوم الحِلوه")

# نظام الهوية
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.username:
    with st.container():
        name = st.text_input("ادخلي اسمج المميز لبدء المراسلة:")
        if st.button("دخول إلى الدردشة"):
            if name:
                st.session_state.username = name
                st.rerun()
else:
    # القائمة الجانبيه لإرسال الملفات
    with st.sidebar:
        st.header(f"👤 {st.session_state.username}")
        st.divider()
        uploaded_file = st.file_uploader("📎 إرسال ملف أو صورة", type=['png', 'jpg', 'jpeg', 'pdf'])
        if uploaded_file:
            st.success(f"تم إرسال الملف: {uploaded_file.name}")

    # خزن وعرض الرسائل
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض المحادثة بأسلوب التليجرام
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(f"**{msg['user']}:** {msg['content']}")

    # صندوق المراسلة الفوري
    if prompt := st.chat_input("اكتبي رسالتج هنا مريوم..."):
        # إضافة رسالتج
        st.session_state.messages.append({"role": "user", "user": st.session_state.username, "content": prompt})
        
        # محاكاة رد النظام (حتى تبين المراسلة شغالة)
        st.session_state.messages.append({"role": "assistant", "user": "مريوم بوت", "content": f"وصلت رسالتج: {prompt} ✨"})
        st.rerun()
