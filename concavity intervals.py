import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(layout="wide", page_title="Mr. Ibrahim Math Quiz")

# --- دالة عرض الاسم المنمق (Branding) ---
def show_header():
    st.markdown("""
    <div class="branding-header">
        Mr. Ibrahim Eldabour
    </div>
    """, unsafe_allow_html=True)

# --- دالة الربط مع جوجل شيت ---
def send_to_google_sheet(student_name, section, score, total, details):
    try:
        # إعداد الاتصال
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        
        # فتح الشيت
        sheet = client.open("Mr_Ibrahim_Quiz_Results").sheet1
        
        # التوقيت
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # الصف الذي سيتم إضافته
        row = [timestamp, student_name, section, f"{score}/{total}", details]
        
        sheet.append_row(row)
        return True
    except Exception as e:
        st.error(f"خطأ في الاتصال: {e}")
        return False

# --- تنسيق CSS (الاسم المنمق + الصناديق) ---
st.markdown("""
<style>
    /* استيراد خط جميل للاسم */
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Montserrat:wght@600&display=swap');

    /* تنسيق الاسم في الأعلى */
    .branding-header {
        font-family: 'Great Vibes', cursive;
        font-size: 45px;
        text-align: center;
        background: linear-gradient(to right, #141e30, #243b55);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        padding: 10px;
        font-weight: bold;
    }

    /* صناديق الأسئلة */
    .rtl-box { 
        direction: rtl; 
        text-align: right; 
        background-color: #f4f6f9; 
        padding: 20px; 
        border-radius: 12px; 
        border-right: 5px solid #2980b9; 
        margin-bottom: 15px; 
        color: #2c3e50;
        font-size: 18px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .ltr-box { 
        direction: ltr; 
        text-align: left; 
        background-color: #f4f6f9; 
        padding: 20px; 
        border-radius: 12px; 
        border-left: 5px solid #2980b9; 
        margin-bottom: 15px; 
        color: #2c3e50;
        font-size: 18px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* الأزرار */
    .stButton button { 
        width: 100%; 
        font-weight: bold; 
        font-size: 18px; 
        padding: 15px; 
        border-radius: 10px;
        transition: transform 0.1s;
    }
    .stButton button:active {
        transform: scale(0.98);
    }

    /* بطاقة النتيجة */
    .final-card { 
        text-align: center; 
        padding: 40px; 
        background-color: #d4edda; 
        border-radius: 15px; 
        border: 2px solid #c3e6cb; 
        color: #155724; 
        font-size: 26px; 
        font-weight: bold; 
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- محرك الرسم البياني ---
def plot_textbook_graph(x, y):
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(x, y, color='#007acc', linewidth=3)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    plt.tight_layout()
    return fig

# --- بنك الأسئلة (تمت مراجعة النصوص لإصلاح الأخطاء) ---
def get_full_question_bank():
    bank = []

    # 1. سؤال جبري (Inflection Point)
    bank.append({
        "id": "alg_1", "type": "algebra",
        "en_text": r"Determine the inflection point of: $$f(x) = x^3 - 3x^2 + 4x - 1$$",
        "ar_text": r"حدد نقطة الانقلاب للدالة: $$f(x) = x^3 - 3x^2 + 4x - 1$$",
        "options": [r"$(1, 1)$", r"$(1, -1)$", r"$(0, -1)$", r"None"],
        "correct_idx": 0
    })
    
    # 2. سؤال جبري (Concave Up)
    bank.append({
        "id": "alg_2", "type": "algebra",
        "en_text": r"Find the interval where $$f(x) = x^4 - 6x^2 + 2x + 3$$ is **Concave Up**.",
        "ar_text": r"أوجد الفترة التي تكون فيها الدالة $$f(x) = x^4 - 6x^2 + 2x + 3$$ **مقعرة لأعلى**.",
        "options": [r"$(-\infty, -1) \cup (1, \infty)$", r"$(-1, 1)$", r"$(1, \infty)$", r"$(-\infty, 1)$"],
        "correct_idx": 0
    })

    # 3. سؤال رسم (Concave Down Quadratic)
    bank.append({
        "id": "gr_1", "type": "graph",
        "en_text": r"Choose the graph where $$f''(x) < 0$$ for all $$x$$.",
        "ar_text": r"اختر الرسم البياني الذي يحقق $$f''(x) < 0$$ لجميع قيم $$x$$ (مقعر لأسفل دائماً).",
        "correct_func": lambda v: -(v**2),
        "distractors": [lambda v: v**2, lambda v: v**3, lambda v: np.abs(v)]
    })

    # 4. سؤال جبري (Trig)
    bank.append({
        "id": "alg_3", "type": "algebra",
        "en_text": r"Find the x-coordinates of inflection points for $$f(x) = \sin x$$ on $$[0, 2\pi]$$.",
        "ar_text": r"أوجد الإحداثيات السينية لنقاط الانقلاب للدالة $$f(x) = \sin x$$ في الفترة $$[0, 2\pi]$$.",
        "options": [r"$$x = \pi$$", r"$$x = \pi/2$$", r"$$x = 0$$", r"None"],
        "correct_idx": 0
    })

    # 5. سؤال رسم (Cusp / 40)
    bank.append({
        "id": "gr_2", "type": "graph",
        "en_text": r"$$f(1)=0$$, $$f'(x)<0$$ for $$x<1$$, $$f'(x)>0$$ for $$x>1$$, $$f''(x)<0$$ everywhere else.",
        "ar_text": r"$$f(1)=0$$، متناقصة قبل 1 ومتزايدة بعده، ومقعرة لأسفل في كل مكان آخر.",
        "correct_func": lambda v: (np.abs(v-1))**(2/3),
        "distractors": [lambda v: (v-1)**2, lambda v: -(v-1)**2, lambda v: v**3]
    })

    # 6. سؤال جبري (Constants)
    bank.append({
        "id": "alg_4", "type": "algebra",
        "en_text": r"If $$f(x)=x^3+kx^2+5$$ has an inflection point at $$x=2$$, find $$k$$.",
        "ar_text": r"إذا كان للدالة $$f(x)=x^3+kx^2+5$$ نقطة انقلاب عند $$x=2$$، أوجد قيمة الثابت $$k$$.",
        "options": [r"$$k=-3$$", r"$$k=-6$$", r"$$k=3$$", r"$$k=6$$"],
        "correct_idx": 0 # f'' = 6x + 2k -> 12 + 2k = 0 -> k = -6. Correct answer is -6. Let's fix option index.
    })
    # التصحيح: f'(x)=3x^2+2kx -> f''(x)=6x+2k. At x=2, f''(2)=0.
    # 6(2) + 2k = 0 => 12 = -2k => k = -6.
    # سأقوم بتعديل الإجابة الصحيحة في الكود ليكون k=-6 هو الاندكس 1
    bank[-1]["correct_idx"] = 1 

    # 7. سؤال رسم (Linear)
    bank.append({
        "id": "gr_3", "type": "graph",
        "en_text": r"Select the graph of $$f(x)$$ where $$f''(x) = 0$$ for all $$x$$.",
        "ar_text": r"اختر رسم الدالة $$f(x)$$ حيث $$f''(x) = 0$$ لجميع قيم $$x$$ (لا يوجد تقعر).",
        "correct_func": lambda v: v,
        "distractors": [lambda v: v**2, lambda v: v**3, lambda v: np.sin(v)]
    })

    # 8. سؤال جبري (Rational)
    bank.append({
        "id": "alg_5", "type": "algebra",
        "en_text": r"Determine the concavity of $$f(x) = 1/x$$ for $$x>0$$.",
        "ar_text": r"حدد تقعر الدالة $$f(x) = 1/x$$ عندما $$x>0$$.",
        "options": [r"Concave Up (مقعرة لأعلى)", r"Concave Down (مقعرة لأسفل)", r"Inflection (نقطة انقلاب)", r"None"],
        "correct_idx": 0 # f'=-1/x^2, f''=2/x^3. For x>0, f''>0 (Up). Correct.
    })

    # 9. سؤال رسم (S-Shape)
    bank.append({
        "id": "gr_4", "type": "graph",
        "en_text": r"Select graph with inflection point at $$x=0$$ (Concave Down then Up).",
        "ar_text": r"اختر الرسم الذي له نقطة انقلاب عند $$x=0$$ (مقعرة لأسفل ثم لأعلى).",
        "correct_func": lambda v: v**3,
        "distractors": [lambda v: -(v**3), lambda v: v**2, lambda v: -(v**2)]
    })

    # 10. سؤال جبري (Expo)
    bank.append({
        "id": "alg_6", "type": "algebra",
        "en_text": r"Does $$f(x)=e^x$$ have any inflection points?",
        "ar_text": r"هل للدالة $$f(x)=e^x$$ أي نقاط انقلاب؟",
        "options": [r"No (لا)", r"Yes at x=0", r"Yes at x=1", r"Yes at x=-1"],
        "correct_idx": 0
    })

    # 11. سؤال إضافي
    bank.append({
        "id": "alg_7", "type": "algebra",
        "en_text": r"If $$f''(x) = 6x - 12$$, the inflection point is at:",
        "ar_text": r"إذا كانت $$f''(x) = 6x - 12$$، فإن نقطة الانقلاب تقع عند:",
        "options": [r"$$x=2$$", r"$$x=-2$$", r"$$x=0$$", r"$$x=12$$"],
        "correct_idx": 0
    })

    return bank

# --- إدارة الحالة (Session State) ---
# التأكد من تهيئة المتغيرات الأساسية
if 'step' not in st.session_state: st.session_state['step'] = 'login'
if 'student_name' not in st.session_state: st.session_state['student_name'] = ""
if 'section' not in st.session_state: st.session_state['section'] = ""

# --- 1. صفحة الدخول (LOGIN PAGE) ---
if st.session_state['step'] == 'login':
    show_header() # عرض الاسم
    
    st.markdown("### 📝 Student Login / تسجيل دخول الطالب")
    st.info("يرجى إدخال البيانات للبدء في الاختبار")
    
    with st.form("login_form"):
        name_input = st.text_input("Full Name / الاسم الثلاثي")
        sec_input = st.text_input("Section / الشعبة (اختياري)")
        
        submitted = st.form_submit_button("Start Quiz 🚀")
        
        if submitted:
            if name_input.strip():
                # حفظ البيانات
                st.session_state['student_name'] = name_input
                st.session_state['section'] = sec_input
                
                # تجهيز الأسئلة (سحب 10 عشوائي)
                all_bank = get_full_question_bank()
                q_count = min(10, len(all_bank))
                st.session_state['quiz_questions'] = random.sample(all_bank, q_count)
                
                # تهيئة متغيرات الاختبار
                st.session_state['current_index'] = 0
                st.session_state['score'] = 0
                st.session_state['history'] = []
                st.session_state['shuffled_options'] = None
                st.session_state['feedback_given'] = False
                
                # الانتقال للاختبار
                st.session_state['step'] = 'quiz'
                st.rerun()
            else:
                st.error("Please enter your name first. الرجاء كتابة الاسم.")

# --- 2. صفحة الاختبار (QUIZ PAGE) ---
elif st.session_state['step'] == 'quiz':
    show_header()
    
    # بيانات الطالب في الشريط الجانبي أو الأعلى
    st.caption(f"👤 Student: {st.session_state['student_name']} | Section: {st.session_state['section']}")
    
    questions = st.session_state['quiz_questions']
    idx = st.session_state['current_index']
    curr = questions[idx]
    
    # شريط التقدم
    progress_val = (idx + 1) / len(questions)
    st.progress(progress_val)
    st.markdown(f"**Question {idx+1} of {len(questions)}**")
    
    st.divider()
    
    # عرض السؤال (باستخدام Markdown لتجنب الأخطاء)
    c1, c2 = st.columns(2)
    with c1: 
        st.markdown(f'<div class="ltr-box">{curr["en_text"]}</div>', unsafe_allow_html=True)
    with c2: 
        st.markdown(f'<div class="rtl-box">{curr["ar_text"]}</div>', unsafe_allow_html=True)
    
    # خلط الخيارات (مرة واحدة للسؤال)
    if st.session_state['shuffled_options'] is None:
        opts = []
        if curr['type'] == 'graph':
            opts.append({'data': curr['correct_func'], 'correct': True, 'label': 'Correct Graph'})
            for d in curr['distractors']:
                opts.append({'data': d, 'correct': False, 'label': 'Distractor'})
        else:
            for i, txt in enumerate(curr['options']):
                opts.append({'data': txt, 'correct': (i == curr['correct_idx']), 'label': txt})
        
        random.shuffle(opts)
        st.session_state['shuffled_options'] = opts
        
    opts = st.session_state['shuffled_options']
    
    # عرض الخيارات
    cols = st.columns(2) + st.columns(2)
    x_vals = np.linspace(-3.5, 3.5, 300)
    
    for i, opt in enumerate(opts):
        with cols[i]:
            if curr['type'] == 'graph':
                # رسم
                fig = plot_textbook_graph(x_vals, opt['data'](x_vals))
                st.pyplot(fig, use_container_width=True)
                btn_txt = f"Select Graph {i+1}"
            else:
                # نص جبري (استخدام مسافات لتحسين الشكل)
                st.write("") 
                st.write("")
                btn_txt = opt['data']
            
            # الأزرار
            # إذا لم يتم الإجابة بعد
            if not st.session_state['feedback_given']:
                if st.button(btn_txt, key=f"btn_{idx}_{i}"):
                    # تسجيل الإجابة
                    is_corr = opt['correct']
                    if is_corr: st.session_state['score'] += 1
                    
                    # تسجيل التفاصيل للسجل
                    ans_label = "Graph Option" if curr['type']=='graph' else opt['label']
                    status_icon = "✅" if is_corr else "❌"
                    st.session_state['history'].append(f"Q{idx+1}: {status_icon} ({ans_label})")
                    
                    st.session_state['feedback_given'] = True
                    st.rerun()
            else:
                # بعد الإجابة (إظهار النتيجة)
                if opt['correct']:
                    st.success("✅ Correct")
                else:
                    st.warning("❌") # زر رمادي للمحاولات الخاطئة

    # زر الانتقال
    if st.session_state['feedback_given']:
        st.write("---")
        if idx < len(questions) - 1:
            if st.button("Next Question ➡", type="primary"):
                st.session_state['current_index'] += 1
                st.session_state['shuffled_options'] = None
                st.session_state['feedback_given'] = False
                st.rerun()
        else:
            if st.button("Finish & Submit Results 🏁", type="primary"):
                st.session_state['step'] = 'result'
                st.rerun()

# --- 3. صفحة النتيجة (RESULT PAGE) ---
elif st.session_state['step'] == 'result':
    show_header()
    
    score = st.session_state['score']
    total = len(st.session_state['quiz_questions'])
    name = st.session_state['student_name']
    sec = st.session_state['section']
    history_str = " | ".join(st.session_state['history'])
    
    st.balloons()
    
    st.markdown(f"""
    <div class="final-card">
        Excellent work, {name}!<br>
        <span style="font-size: 40px;">{score} / {total}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # إرسال البيانات (مرة واحدة)
    if 'data_sent' not in st.session_state:
        with st.spinner("Saving results to database..."):
            success = send_to_google_sheet(name, sec, score, total, history_str)
            if success:
                st.success("✅ تم إرسال نتيجتك للمعلم بنجاح!")
                st.session_state['data_sent'] = True
            else:
                st.error("⚠️ حدث خطأ في الاتصال، يرجى إبلاغ المعلم بالدرجة.")
    
    # زر إعادة (طالب جديد)
    st.write("---")
    if st.button("🔄 New Student Login / تسجيل طالب جديد"):
        # مسح كل البيانات للبدء من جديد
        st.session_state.clear()
        st.rerun()
