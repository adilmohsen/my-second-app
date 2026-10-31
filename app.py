import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta
import requests

# --- إعدادات الباسورد الأساسية ---
PASSWORD = "261239"

# وظيفة إرسال الإشعار لتليجرام
def send_telegram_notification(bot_token, chat_id, message_text):
    if not bot_token or not chat_id:
        return 
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": f"👑 رسالة جديدة في چات Canım:\n\n{message_text}",
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except:
        pass

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

# وظيفة رفع الصور مع إرسال الإشعار
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
            b_token = st.session_state.get("bot_token_input", "")
            t_chat_id = st.session_state.get("target_chat_id", "")
            send_telegram_notification(b_token, t_chat_id, f"{st.session_state.my_name} أرسلت صورة 📷")
        st.session_state.up_files = []

# --- القائمة الجانبية (مع حقول البوت والـ ID) ---
st.sidebar.title(f"الملكة {st.session_state.my_name}")

st.sidebar.markdown("### 🔔 إعدادات إشعار تليجرام")
token_input = st.sidebar.text_input("توكن البوت (Bot Token):", value=st.session_state.get("bot_token_input", ""), type="password")
if token_input:
    st.session_state.bot_token_input = token_input

target_id_input = st.sidebar.text_input("إيدي الشخص المقابل (Chat ID):", value=st.session_state.get("target_chat_id", ""))
if target_id_input:
    st.session_state.target_chat_id = target_id_input

st.sidebar.divider()
st.sidebar.file_uploader("+", key="up_files", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True, on_change=upload_callback)

st.sidebar.divider()
if st.sidebar.button("حذف الكل 🗑️"): all_msgs.clear(); st.rerun()
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

# إرسال نص جديد مع إشعار تليجرام
if prompt := st.chat_input("اكتبي رسالتج هنا..."):
    now = (datetime.now() + timedelta(hours=3)).strftime("%I:%M %p")
    all_msgs.append({"name": st.session_state.my_name, "msg": prompt, "time": now, "seen": False})
    
    # جلب التوكن والإيدي المكتوبين بالقائمة الجانبية وإرسال الإشعار
    b_token = st.session_state.get("bot_token_input", "")
    t_chat_id = st.session_state.get("target_chat_id", "")
    send_telegram_notification(b_token, t_chat_id, f"*{st.session_state.my_name}*: {prompt}")
    
    st.rerun()
