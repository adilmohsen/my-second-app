import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="مريوم الحِلوه", page_icon="🎀", layout="centered")

# إضافة الخلفية الوردية وتعديل شكل الفقاعات لتشبه التليجرام
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
        background-attachment: fixed;
    }}
    .stChatMessage {{
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }}
    /* تعديل جهة رسالة المستخدم لتكون على اليمين مثل التلي */
    [data-testid="stChatMessage"]:nth-child(even) {{
        flex-direction: row-reverse;
        text-align: right;
        background-color: #dcf8c6; /* لون أخضر فاتح للمرسل */
    }}
    </style>
    """, unsafe_allow_html=True)

st.title("🎀 تطبيق مريوم الحِلوه")

# نظام الاسم (الخاص)
if "username" not in st.session_state:
    st.session_state.username = st.text_input("ادخلي اسمج المميز للدخول (ما يصير يتكرر):", "")

if st.session_state.username:
    st.sidebar.header(f"👤 الملف الشخصي: {st.session_state.username}")
    st.sidebar.write("هنا تكدرين تبحثين عن الأصدقاء (قريباً)")
    
    # خزن المحادثة
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض المحادثة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(f"**{msg['user']}:** {msg['content']}")

    # إرسال الرسائل (تدعم الايموجيات تلقائياً)
    if prompt := st.chat_input("اكتبي رسالتج هنا مريوم... 🎀✨"):
        # إضافة رسالة المستخدم
        st.session_state.messages.append({"role": "user", "user": st.session_state.username, "content": prompt})
        
        # رد تلقائي بسيط (محاكاة للمستلم)
        st.session_state.messages.append({"role": "assistant", "user": "النظام", "content": f"وصلت رسالتج يا {st.session_state.username}!"})
        st.rerun()

    # ميزة إرسال الملفات
    with st.sidebar:
        st.divider()
        uploaded_file = st.file_uploader("📎 إرسال ملفات (صور، PDF)", type=['png', 'jpg', 'pdf'])
        if uploaded_file:
            st.success(f"تم تحميل: {uploaded_file.name}")
