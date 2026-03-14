import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. إعدادات الصفحة (الاسم الملكي الجديد)
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")

# 2. التحديث التلقائي (كل ثانيتين)
st_autorefresh(interval=2000, key="datarefresh")

# 3. الخلفية الوردية الخاصة بمريوم
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
    }}
    /* تنسيق فقاعة الرسالة لتكون أوضح */
    .stChatMessage {{
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 5px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. المخزن المشترك
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
    st.stop()

# --- القائمة الجانبية (Sidebar) ---
st.sidebar.title(f"الملكة {st.session_state.my_name} ✨")
if st.sidebar.button("حذف كل الرسايل للكل 🗑️"):
    all_msgs.clear()
    st.rerun()

if st.sidebar.button("تسجيل الخروج ⬅️"):
    del st.session_state.my_name
    st.rerun()

# --- واجهة الچات ---
st.title("🎀 محادثة مريوم المشتركة")

# عرض الرسائل مع خاصية الحذف والتعديل
for i, chat in enumerate(all_msgs):
    # تقسيم السطر: الرسالة تأخذ مساحة كبيرة، والأزرار مساحة صغيرة
    col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
    
    with col1:
        with st.chat_message("user"):
            st.write(f"**{chat['name']}:** {chat['msg']}")
            
    # أزرار التحكم تظهر فقط لصاحب الرسالة
    if chat['name'] == st.session_state.my_name:
        with col2:
            if st.button("🗑️", key=f"del_{i}", help="حذف الرسالة"):
                all_msgs.pop(i)
                st.rerun()
        with col3:
            if st.button("✏️", key=f"edit_{i}", help="تعديل الرسالة"):
                st.session_state.edit_index = i
                st.session_state.edit_text = chat['msg']

# منطقة التعديل (تظهر فقط عند الضغط على زر القلم)
if "edit_index" in st.session_state:
    st.divider()
    new_text = st.text_input("تعديل رسالتج:", value=st.session_state.edit_text)
    if st.button("حفظ التعديل ✅"):
        all_msgs[st.session_state.edit_index]['msg'] = new_text
        del st.session_state.edit_index # إغلاق وضع التعديل
        st.rerun()
    if st.button("إلغاء ❌"):
        del st.session_state.edit_index
        st.rerun()

# --- خانة إرسال الرسالة الجديدة ---
if prompt := st.chat_input("اكتبي رسالتج هنا..."):
    all_msgs.append({"name": st.session_state.my_name, "msg": prompt})
    st.rerun()
