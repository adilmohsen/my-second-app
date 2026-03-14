import streamlit as st
import time

# إعدادات الصفحة - مريوم الحلوة
st.set_page_config(page_title="محادثة مريوم", page_icon="💬", layout="centered")

# تصميم الواجهة
st.title("💬 غرفة محادثة مريوم")
st.subheader("أهلاً بيكم في تطبيقي الثاني - نظام دردشة ذكي")
st.divider()

# خزن الرسايل في الجلسة (حتى لا تروح عند التحديث)
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسايل السابقة بستايل الفقاعات
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# مكان كتابة الرسالة (Input)
if prompt := st.chat_input("اكتب رسالتك هنا يا مريوم..."):
    # 1. عرض رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. محاكاة رد الجهاز (مثل البوت)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = f"عاشت إيدج مريوم! وصلت رسالتج: ({prompt}) ✨"
        
        # تأثير الكتابة التدريجي
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
