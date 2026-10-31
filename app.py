import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# --- إعداد الباسورد ---
PASSWORD = "261239"

# 1. إعدادات الصفحة
st.set_page_config(page_title="The Queen Meryoum 👑", page_icon="🎀")
st_autorefresh(interval=1000, key="datarefresh")

# 2. التنسيقات
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("https://raw.githubusercontent.com/adilmohsen/my-second-app/main/55fcafb76ebdf0b2fff590b1c0b6886c.jpg");
        background-size: cover;
    }}
    .stChatMessage {{ background-color: rgba(255, 255, 255, 0.8) !important; border-radius: 15px; }}
    
    .chat-info {{ color: #888888 !important; font-size: 8px !important; float: right; margin-top: 5px; font-family: sans-serif; }}
    .status-icon {{ color: #888888 !important; margin-left: 2px; font-size: 9px !important; }}
    
    .stButton button {{ border: none !important; background: transparent !important; color: #888 !important; font-size: 20px !important; }}

    /* ستايل علامة الـ + السحرية */
    section[data-testid="stSidebar"] .stFileUploader label {{
        font-size: 40px !important; color: #888 !important; display: block !important; text-align: center; cursor: pointer;
    }}
    section[data-testid="stSidebar"] .stFileUploader section {{ padding: 0 !important; border: none !important; background: transparent !important; }}
    section[data-testid="stSidebar"] .stFileUploader section > div {{ display: none !important; }}
    section[data-testid="stSidebar"] .stFileUploader [data-testid="stMarkdownContainer"] {{ display: none !important; }}
    </style>
    """, unsafe_allow_html=True)

# 3. المخزن المشترك
@st.cache_resource
def get_global_messages(): return []
all_msgs = get_global_messages()

# وظيفة الإرسال التلقائي للصور
def upload_callback():
    if st.session_state.up_files:
        now = (datetime.now() + timedelta(hours=3)).strftime("%I:%M %p")
        for f in st.session_state.up_files:
            all_msgs.append({
                "name": st.session_state.my_name, 
                "msg": "", 
                "file": f.getvalue(), 
                "is_image": True, 
                "time": now, 
                "seen": False
            })
        st.session_state.up_files = []

# --- نظام الحماية ---
if "authenticated" not in st.session_state:
    st.title("🎀 منطقة خاصة للملكات")
    pass_input = st.text_input("أدخلي كلمة المرور للوصول:", type="password")
    if st.button("دخول"):
        if pass_input == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("كلمة المرور غلط! ❌")
    st.stop()

# --- تسجيل الدخول (الاسم) ---
if "my_name" not in st.session_state:
    st.title("🎀 أهلاً بيج بالچات الوردي")
    name_input = st.text_input("اسمج هنا:")
    if st.button("تأكيد الاسم"):
        if name_input: st.session_state.my_name = name_input; st.rerun()
    st.stop()

# --- 🔔 نظام الإشعارات والتحقق من الرسائل الجديدة ---
if "last_msg_count" not in st.session_state:
    st.session_state.last_msg_count = len(all_msgs)

# التحقق هل وصل عدد الرسائل لأكثر مما نعرف وهل الرسالة من شخص آخر؟
if len(all_msgs) > st.session_state.last_msg_count:
    last_msg = all_msgs[-1]
    if last_msg["name"] != st.session_state.my_name:
        # 1. إشعار داخل التطبيق (Toast)
        sender = last_msg['name']
        msg_content = "📷 صورة جديدة" if last_msg.get("is_image") else last_msg['msg']
        st.toast(f"💬 رسالة جديدة من {sender}: {msg_content}", icon="🎀")
        
        # 2. إشعار صوتي + إشعار المتصفح (Browser Notification) عبر JS
        js_notification = f"""
        <script>
        if (Notification.permission === "granted") {{
            new Notification("رسالة جديدة من {sender} 👑", {{
                body: "{msg_content}",
                icon: "https://em-content.zobj.net/source/apple/354/ribbon_1f380.png"
            }});
        }} else if (Notification.permission !== "denied") {{
            Notification.requestPermission();
        }}
        </script>
        """
        components.html(js_notification, height=0)

    st.session_state.last_msg_count = len(all_msgs)

# --- القائمة الجانبية ---
st.sidebar.title(f"الملكة {st.session_state.my_name}")

# زر لتفعيل إشعارات المتصفح
if st.sidebar.button("تفعيل إشعارات الشاشة 🔔"):
    components.html("""
        <script>
        Notification.requestPermission().then(function(permission) {
            if (permission === 'granted') {
                alert('تم تفعيل الإشعارات بنجاح! 👑');
            }
        });
        </script>
    """, height=0)

st.sidebar.file_uploader("+", key="up_files", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True, on_change=upload_callback)

st.sidebar.divider()
if st.sidebar.button("حذف الكل 🗑️"): 
    all_msgs.clear()
    st.session_state.last_msg_count = 0
    st.rerun()

if st.sidebar.button("خروج ⬅️"): 
    del st.session_state.my_name
    del st.session_state.authenticated
    st.rerun()

st.title("Canım 🎀")

# --- عرض المحادثة ---
for i, chat in enumerate(all_msgs):
    if chat['name'] != st.session_state.my_name: chat['seen'] = True
    col_msg, col_options = st.columns([0.85, 0.15])
    
    with col_msg:
        with st.chat_message("user"):
            if chat.get("msg"):
                st.write(f"**{chat['name']}:** {chat['msg']}")
            else:
                st.write(f"**{chat['name']}:**")
            
            if "file" in chat and chat.get("is_image"):
                st.image(chat["file"], use_container_width=True)
                st.download_button("حفظ 📥", chat["file"], file_name=f"Canim_{i}.png", key=f"dl_{i}")
            
            t, s = chat.get('time', ''), ("v v" if chat.get('seen', False) else "v")
            st.markdown(f'<div class="chat-info">{t} <span class="status-icon">{s}</span></div>', unsafe_allow_html=True)
            
    if chat['name'] == st.session_state.my_name:
        with col_options:
            if st.button("⋮", key=f"menu_{i}"):
                st.session_state[f"opt_{i}"] = not st.session_state.get(f"opt_{i}", False)
            if st.session_state.get(f"opt_{i}", False):
                if st.button("🗑️", key=f"del_{i}"): all_msgs.pop(i); st.rerun()
                if chat.get("msg") and st.button("✏️", key=f"ed_{i}"):
                    st.session_state.edit_idx = i
                    st.session_state.edit_val = chat['msg']
                    st.session_state[f"opt_{i}"] = False; st.rerun()

# --- واجهة التعديل ---
if "edit_idx" in st.session_state:
    st.divider()
    new_txt = st.text_input("تعديل الرسالة:", value=st.session_state.edit_val)
    if st.button("حفظ ✅"):
        all_msgs[st.session_state.edit_idx]['msg'] = new_txt
        del st.session_state.edit_idx; st.rerun()

# إرسال نص جديد
if prompt := st.chat_input("اكتبي رسالتج هنا..."):
    now = (datetime.now() + timedelta(hours=3)).strftime("%I:%M %p")
    all_msgs.append({"name": st.session_state.my_name, "msg": prompt, "time": now, "seen": False})
    st.rerun()
