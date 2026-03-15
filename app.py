import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")

# 2. التحديث التلقائي (كل ثانية لضمان دقة الوقت والحالة)
st_autorefresh(interval=1000, key="datarefresh")

# 3. الخلفية الوردية والتنسيقات (محدثة لتناسب الوقت والصحين)
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
    }}
    .stChatMessage {{
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 15px;
        padding: 10px;
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
        margin-top: 2px;
    }}
    .stButton button {{
        border: none !important;
        background: transparent !important;
        color: #888 !important;
        font-size: 20px !important;
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
    st.stop()

# --- القائمة الجانبية ---
st.sidebar.title(f"الملكة {st.session_state.my_name} ✨")
if st.sidebar.button("حذف كل الرسايل للكل 🗑️"):
    all_msgs.clear(); st.rerun()

if st.sidebar.button("تسجيل الخروج ⬅️"):
    del st.session_state.my_name; st.rerun()

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
            
            # عرض الوقت وعلامة الصح (✅✅ للكل، ✅ لرسالتج إذا محد شافها)
            status_icon = "✔️"
            if chat.get('seen', False):
                status_icon = "✔️✔️"
            
            st.markdown(f"""
                <div class="time-style">
                    {chat['time']} <span class="status-style">{status_icon}</span>
                </div>
                """, unsafe_allow_html=True)
            
    if chat['name'] == st.session_state.my_name:
        with col_options:
            if st.button("⋮", key=f"menu_{i}"):
                st.session_state[f"show_options_{i}"] = not st.session_state.get(f"show_options_{i}", False)
            
            if st.session_state.get(f"show_options_{i}", False):
                if st.button("🗑️", key=f"del_{i}"):
                    all_msgs.pop(i); st.rerun()
                if st.button("✏️", key=f"edit_{i}"):
                    st.session_state.edit_index = i
                    st.session_state.edit_text = chat['msg']
                    st.session_state[f"show_options_{i}"] = False; st.rerun()

# منطقة التعديل
if "edit_index" in st.session_state:
    st.divider()
    new_text = st.text_input("تعديل رسالتج:", value=st.session_state.edit_text)
    if st.button("حفظ التعديل ✅"):
        all_msgs[st.session_state.edit_index]['msg'] = new_text
        del st.session_state.edit_index; st.rerun()

# --- خانة إرسال الرسالة الجديدة ---
if prompt := st.chat_input("اكتبي رسالتج هنا..."):
    now = datetime.now().strftime("%I:%M %p") # جلب الوقت الحالي (12:49 AM)
    all_msgs.append({
        "name": st.session_state.my_name, 
        "msg": prompt, 
        "time": now, 
        "seen": False # الحالة الافتراضية: لم تُقرأ بعد
    })
    st.rerun()
