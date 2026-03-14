import streamlit as st
import datetime

# إعدادات الصفحة
st.set_page_config(page_title="محادثة مريوم الحِلوه", page_icon="🎀")

# الخلفية الوردية (نفس مالتج)
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
    }}
    </style>
    """, unsafe_allow_html=True)

st.title("🎀 چات مريوم الحِلوه المباشر")

# ميزة خزن الرسايل لكل المستخدمين (Global Chat)
# ملاحظة: هاي الطريقة تخزن الرسايل ما دام السيرفر شغال
if "all_messages" not in st.session_state:
    st.session_state.all_messages = []

# نظام تسجيل الاسم
if "my_name" not in st.session_state:
    st.session_state.my_name = st.text_input("سجلي اسمج مريوم (أو أي شخص يدخل):", "")

if st.session_state.my_name:
    st.write(f"المستخدم الحالي: **{st.session_state.my_name}**")
    
    # عرض الرسايل القديمة
    for m in st.session_state.all_messages:
        with st.chat_message("user"):
            st.write(f"**{m['user']}:** {m['text']}  \n*{m['time']}*")

    # صندوق الإرسال
    if prompt := st.chat_input("اكتبي رسالة للكل..."):
        now = datetime.datetime.now().strftime("%H:%M")
        # إضافة الرسالة للمخزن العام (هنا السحر!)
        st.session_state.all_messages.append({"user": st.session_state.my_name, "text": prompt, "time": now})
        st.rerun()

else:
    st.warning("لازم تكتبين اسمج حتى تدخلين للچات!")
