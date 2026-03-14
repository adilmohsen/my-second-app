import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="محادثة مريوم الحِلوه", page_icon="🎀")

# الخلفية الوردية مالتج
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- السحر هنا: مخزن مشترك للكل بدون قاعدة بيانات ---
@st.cache_resource
def get_global_messages():
    return [] # هاي القائمة راح يشوفها الكل ويعدلون عليها

all_msgs = get_global_messages()

st.title("🎀 چات مريوم المشترك")

# اسم المستخدم
user_name = st.sidebar.text_input("اسمج مريوم:", "مريوم")

# عرض الرسايل (هنا الكل راح يشوف نفس الرسايل)
for chat in all_msgs:
    with st.chat_message("user"):
        st.write(f"**{chat['name']}:** {chat['msg']}")

# صندوق الكتابة
if prompt := st.chat_input("اكتبي رسالتج هنا للكل..."):
    all_msgs.append({"name": user_name, "msg": prompt})
    st.rerun()
