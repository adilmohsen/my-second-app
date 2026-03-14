import streamlit as st
import datetime
from google.cloud import firestore

# إعدادات الصفحة
st.set_page_config(page_title="محادثة مريوم الحِلوه المباشرة", page_icon="🎀")

# الخلفية الوردية ותنسيق الفقاعات (محاولة تقريب للتصميم مالتج)
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
    }}
    /* تنسيق فقاعة الطرف الثاني (على اليسار، لون أبيض) */
    [data-testid="stChatMessage"]:nth-child(even) {{
        background-color: #ffffff !important;
        flex-direction: row-reverse !important;
        text-align: right !important;
        border-radius: 15px 15px 15px 0px !important;
    }}
    /* تنسيق فقاعة مريوم (على اليمين، لون وردي) */
    [data-testid="stChatMessage"]:nth-child(odd) {{
        background-color: #fce4ec !important;
        border-radius: 15px 15px 0px 15px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ربط Firebase ---
# مريوم، هنا تخلي المفتاح السري اللي نزلناه من الموقع (الخطوة الجاية)
if "db" not in st.session_state:
    # ملاحظة: سوي خطوة الـ FirestoreDatabase حتى أعلمج شلون تربطين هذا الجزء
    pass

st.title("🎀 چات مريوم الحِلوه المباشر")

# نظام تسجيل الدخول
my_name = st.sidebar.text_input("سجلي اسمج مريوم (أو أي شخص يدخل):", "مريوم")

# جلب وعرض الرسايل من "المخزن المشترك"
# (هنا الكود راح يتغير شوية حتى يقرأ من الـ Database)
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(f"**{msg['user']}:** {msg['content']}  \n*{msg['time']}*")

# صندوق المراسلة للكل
if prompt := st.chat_input("اكتبي رسالة للطرف الثاني..."):
    # هنا الكود راح يرسل الرسالة للقاعدة
    now = datetime.datetime.now().strftime("%H:%M")
    st.session_state.messages.append({"role": "user", "user": my_name, "content": prompt, "time": now})
    st.rerun()
