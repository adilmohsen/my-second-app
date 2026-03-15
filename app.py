import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta

# 1. إعدادات الصفحة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")

# 2. التحديث التلقائي (كل ثانية واحدة لضمان السرعة)
st_autorefresh(interval=1000, key="datarefresh")

# 3. الخلفية الوردية والتنسيقات
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-color: #FFDEE9;
        background-image: linear-gradient(0deg, #FFDEE9 0%, #B5FFFC 100%);
        background-size: cover;
        background-attachment: fixed;
    }}
    .stChatMessage {{
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 15px;
        padding: 10px;
        border: 1px solid #FFB6C1;
    }}
    .time-style {{
        font-size: 10px;
        color: #888;
        float: right;
        margin-top: 5px;
    }}
    .status-style {{
        font-size: 12px;
        color: #34B7F1; /* لون أزرق مثل الواتساب */
        float: right;
        margin-left: 5px;
    }}
    /* تنسيق زر النقاط (⋮) */
    .stButton button {{
        border: none !important;
        background: transparent !important;
        color: #FF69B4 !important;
        font-size: 22px !important;
        font-weight: bold !important;
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
    name_input = st.text_input("قبل ما نبدأ، اكتبي اسمج هنا يا حلوه:")
    if st.button("دخول ✨"):
        if name_input:
            st.session_state.my_name = name_input
            st.rerun()
    st.stop()

# --- القائمة الجانبية (Sidebar) ---
st.sidebar.title(f"👑 الملكة {st.session_state.my_name}")
if st.sidebar.button("حذف كل الرسايل للكل 🗑️"):
    all_msgs.clear()
    st.rerun()

if st.sidebar.button("تسجيل الخروج ⬅️"):
    del st.session_state.my_name
    st.rerun()

# --- واجهة الچات ---
st.title("🎀 محادثة مريوم المشتركة")

# عرض الرسائل
for i, chat in enumerate(all_msgs):
    # تحديث حالة "تمت الرؤية" إذا شخص آخر فتح الچات
    if chat['name'] != st.session_state.my_name:
        chat['seen'] = True

    col_msg, col_options = st.columns([0.9, 0.1])
    
    with col_msg:
        with st.chat_message("user"):
            st.write(f"**{chat['name']}:** {chat['msg']}")
            
            # جلب الوقت وحالة الصحين مع حماية من الأخطاء
            msg_time = chat.get('time', '')
            status_icon = "✔️✔️" if chat.get('seen', False) else "✔️"
            
            st.markdown(f"""
                <div class="time-style">
                    {msg_time} <span class="status-style">{status_icon}</span>
                </div>
                """, unsafe_allow_html=True)
            
    if chat['name'] == st.session_state.my_name:
        with col_options:
            if st.button("⋮", key=f"menu_{i}"):
                st.session_state[f"show_opt_{i}"] = not st.session_state.get(f"show_opt_{i}", False)
            
            if st.session_state.get(f"show_opt_{i}", False):
                if st.button("🗑️", key=f"del_{i}"):
                    all_msgs.pop(i)
                    st.session_state[f"show_opt_{i}"] = False
                    st.rerun()
                if st.button("✏️", key=f"edit_{i}"):
                    st.session_state.edit_idx = i
                    st.session_state.edit_txt = chat['msg']
                    st.session_state[f"show_opt_{i}"] = False
                    st.rerun()

# منطقة التعديل
if "edit_idx" in st.session_state:
    with st.container(border=True):
        new_text = st.text_input("عدلي رسالتج:", value=st.session_state.edit_txt)
        if st.button("حفظ التعديل ✅"):
            all_msgs[st.session_state.edit_idx]['msg'] = new_text
            del st.session_state.edit_idx
            st.rerun()

# --- خانة إرسال الرسالة الجديدة ---
if prompt := st.chat_input("اكتبي رسالتج هنا..."):
    # ضبط الوقت بتوقيت العراق (إضافة 3 ساعات لتوقيت السيرفر العالمي)
    iraq_time = datetime.now() + timedelta(hours=3)
    now = iraq_time.strftime("%I:%M %p")
    
    all_msgs.append({
        "name": st.session_state.my_name, 
        "msg": prompt, 
        "time": now, 
        "seen": False
    })
    st.rerun()
