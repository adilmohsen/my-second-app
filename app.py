import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="محادثة مريوم الحِلوه", page_icon="🎀")

# الخلفية الوردية
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
    }}
    </style>
    """, unsafe_allow_html=True)

st.title("🎀 محادثة مريوم")

# اسم المستخدم
user_name = st.sidebar.text_input("اسمج مريوم:", "مريوم")

# خزن الرسايل (بصورة مؤقتة للكل)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# عرض الرسايل القديمة
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(f"**{chat['name']}:** {chat['msg']}")

# صندوق الكتابة
if prompt := st.chat_input("اكتبي رسالتج هنا..."):
    st.session_state.chat_history.append({"name": user_name, "msg": prompt})
    st.rerun()
