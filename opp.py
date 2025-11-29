import streamlit as st
import google.generativeai as genai

# --- 1. إعداد الصفحة (أساس التصميم) ---
st.set_page_config(
    page_title="Ahmad Mnene AI Tool",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. سحر التصميم (CSS) ---
# سنقوم بحقن كود CSS ليغير شكل الموقع بالكامل
st.markdown("""
<style>
    /* استيراد خط تجاري حديث */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');

    /* تطبيق الخط على كامل الموقع */
    * {
        font-family: 'Cairo', sans-serif;
    }

    /* خلفية داكنة مع تدرج لوني خفيف */
    .stApp {
        background: linear-gradient(to bottom right, #0e1117, #1a1c24);
    }

    /* تصميم العنوان الرئيسي */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(120deg, #FF0080, #7928CA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
        padding-top: 20px;
    }
    
    .subtitle {
        text-align: center;
        color: #b0b0b0;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }

    /* تحسين شكل الشريط الجانبي */
    section[data-testid="stSidebar"] {
        background-color: #111;
        border-right: 1px solid #333;
    }

    /* تحسين فقاعات المحادثة */
    .stChatMessage {
        background-color: #262730;
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 10px;
        border: 1px solid #333;
        transition: transform 0.2s;
    }
    
    .stChatMessage:hover {
        transform: scale(1.01);
        border-color: #7928CA;
    }

    /* جعل الكود يظهر بشكل مميز */
    code {
        color: #ff79c6 !important;
        font-weight: bold;
    }
    
    /* زر مخصص */
    .stButton button {
        background: linear-gradient(90deg, #FF0080, #7928CA);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton button:hover {
        opacity: 0.8;
    }

</style>
""", unsafe_allow_html=True)

# --- 3. الشريط الجانبي (بروفايل المطور) ---
with st.sidebar:
    st.markdown("<h3 style='text-align: center;'>🛠️ لوحة التحكم</h3>", unsafe_allow_html=True)
    st.write("---")
    
    # قسم المطور بستايل جميل
    st.markdown("""
    <div style='background-color: #1E1E1E; padding: 15px; border-radius: 10px; text-align: center;'>
        <p style='color: #fff; margin:0;'>تم التطوير بواسطة</p>
        <h2 style='color: #FF0080; margin:0;'>Ahmad Mnene</h2>
        <p style='font-size: 12px; color: #888;'>AI Solutions Architect</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.info("💡 **نصيحة:** كلما كانت إجاباتك دقيقة، كلما كان البرومت أقوى.")

# --- 4. واجهة التطبيق الرئيسية ---
st.markdown('<p class="main-title">AI Prompt Master</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">صمم أوامر احترافية بدقة لا متناهية | Powered by Gemini</p>', unsafe_allow_html=True)

# --- 5. المنطق البرمجي (Gemini) ---
api_key = None
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
except:
    pass

if not api_key:
    # تصميم جميل لمربع إدخال المفتاح إذا لم يوجد
    st.warning("⚠️ لم يتم العثور على مفتاح API، الرجاء إدخاله يدوياً:")
    api_key = st.text_input("🔑 API Key", type="password", help="احصل عليه من Google AI Studio")

SYSTEM_PROMPT = """
أنت خبير ومستشار في هندسة الأوامر (Prompt Engineering).
هويتك: أنت أداة ذكية متطورة من برمجة "Ahmad Mnene".
المهمة:
1. حلل طلب المستخدم واستخرج (Context, Goal, Audience, Tone).
2. إذا نقص شيء، اسأل عنه بأسلوب "مستشار محترف".
3. عند الاكتمال، قدم البرومت النهائي (عربي وإنجليزي) بتنسيق Markdown و Code Blocks.
4. التوقيع: "Designed by Ahmad Mnene".
"""

if api_key:
    genai.configure(api_key=api_key)
    
    if "model" not in st.session_state:
        st.session_state.model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
    
    if "chat" not in st.session_state:
        st.session_state.chat = st.session_state.model.start_chat(history=[])

    # عرض المحادثة
    for message in st.session_state.chat.history:
        role = "user" if message.role == "user" else "assistant"
        # أيقونات مخصصة
        avatar = "🧑‍💻" if role == "user" else "🤖"
        with st.chat_message(role, avatar=avatar):
            st.markdown(message.parts[0].text)

    # الإدخال
    if prompt := st.chat_input("اكتب فكرتك هنا..."):
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)
        
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("جاري تحليل البيانات وبناء الهيكل..."):
                try:
                    response = st.session_state.chat.send_message(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"خطأ في الاتصال: {e}")