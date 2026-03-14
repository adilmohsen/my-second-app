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

# المخزن المشترك بالسيرفر
@st.cache_resource
def get_global_messages():
    return []

all_msgs = get_global_messages()

# --- شاشة تسجيل الدخول ---
if "my_name" not in st.session_state:
    st.title("🎀 أهلاً بيج بالچات الوردي")
    name_input = st.text_input("قبل ما نبدأ، اكتبي اسمج هنا:")
    if st.button("دخول للچات"):
        if name_input:
            st.session_state.my_name = name_input
            st.rerun()
        else:
            st.warning("لازم تكتبين اسم حتى تدخلين!")
    st.stop() # يوقف الكود هنا وما يخلي الباقي يظهر إلا بعد الدخول

# --- إذا تم إدخال الاسم، تظهر الواجهة الجوة ---

# القائمة الجانبية (Sidebar)
st.sidebar.title(f"أهلاً {st.session_state.my_name} ✨")
if st.sidebar.button("حذف كل الرسايل 🗑️"):
    all_msgs.clear()
    st.rerun()

if st.sidebar.button("تسجيل الخروج ⬅️"):
    del st.session_state.my_name
    st.rerun()

# واجهة الچات
st.title("🎀 محادثة مريوم المشتركة")

for chat in all_msgs:
    # تنسيق بسيط: إذا الرسالة مني تطلع بلون مختلف (اختياري)
    with st.chat_message("user"):
        st.write(f"**{chat['name']}:** {chat['msg']}")

if prompt := st.chat_input("اكتبي رسالتج هنا..."):
    all_msgs.append({"name": st.session_state.my_name, "msg": prompt})
    st.rerun()
