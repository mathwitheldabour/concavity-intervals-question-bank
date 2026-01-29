import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(layout="wide", page_title="Mr. Ibrahim Math Quiz")

# --- CSS: تنسيق الاسم والأزرار والصناديق ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cairo:wght@600&display=swap');

    /* تنسيق اسم المستر */
    .branding-header {
        font-family: 'Great Vibes', cursive;
        font-size: 50px;
        text-align: center;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        padding: 10px;
    }

    /* صناديق الأسئلة - تم تبسيطها لضمان عمل المعادلات */
    .question-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .rtl-text { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; color: #2c3e50; font-size: 18px; }
    .ltr-text { direction: ltr; text-align: left; font-family: sans-serif; color: #2c3e50; font-size: 18px; }

    /* الأزرار */
    .stButton button {
        width: 100%;
        font-weight: bold;
        font-size: 16px;
        padding: 10px;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s;
    }
    .stButton button:hover {
        border-color: #2a5298;
        color: #2a5298;
        background-color: #f0f4f8;
    }
    
    /* بطاقة النتيجة */
    .final-card {
        text-align: center;
        padding: 40px;
        background-color: #d4edda;
        border-radius: 15px;
        color: #155724;
        font-size: 24px;
        font-weight: bold;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- دالة العنوان ---
def show_header():
    st.markdown('<div class="branding-header">Mr. Ibrahim Eldabour</div>', unsafe_allow_html=True)

# --- دالة جوجل شيت ---
def send_to_google_sheet(student_name, section, score, total, details):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("Mr_Ibrahim_Quiz_Results").sheet1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [timestamp, student_name, section, f"{score}/{total}", details]
        sheet.append_row(row)
        return True
    except Exception as e:
        return False

# --- محرك الرسم البياني ---
def plot_textbook_graph(x, y):
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(x, y, color='#007acc', linewidth=2.5)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)
    
    # تحسين حدود الرسم
    y_max = np.max(y)
    y_min = np.min(y)
    ax.set_ylim(max(y_min, -5), min(y_max, 5)) # تقييد المحور الصادي
    ax.set_xlim(-3.5, 3.5)
    
    plt.tight_layout()
    return fig

# --- بنك الأسئلة (المصحح) ---
def get_full_question_bank():
    bank = []

    # === أسئلة المعادلات (Exercises 1-8) ===
    
    # Q1
    bank.append({
        "id": "ex_1", "type": "algebra",
        "en_latex": r"f(x) = x^3 - 3x^2 + 4x - 1",
        "ar_latex": r"f(x) = x^3 - 3x^2 + 4x - 1",
        "question_en": "Determine the inflection point:",
        "question_ar": "حدد نقطة الانقلاب:",
        "options": [r"$(1, 1)$", r"$(1, -1)$", r"$(0, -1)$", r"None"],
        "correct_idx": 0
    })

    # Q2
    bank.append({
        "id": "ex_2", "type": "algebra",
        "en_latex": r"f(x) = x^4 - 6x^2 + 2x + 3",
        "ar_latex": r"f(x) = x^4 - 6x^2 + 2x + 3",
        "question_en": "Identify intervals where the graph is Concave Up:",
        "question_ar": "حدد الفترات التي تكون فيها الدالة مقعرة لأعلى:",
        "options": [
            r"$(-\infty, -1) \cup (1, \infty)$",
            r"$(-1, 1)$",
            r"$(1, \infty)$",
            r"$(-\infty, 1)$"
        ],
        "correct_idx": 0
    })

    # Q3
    bank.append({
        "id": "ex_3", "type": "algebra",
        "en_latex": r"f(x) = x + \frac{1}{x}",
        "ar_latex": r"f(x) = x + \frac{1}{x}",
        "question_en": "Identify inflection points:",
        "question_ar": "حدد نقاط الانقلاب:",
        "options": [r"None (لا توجد)", r"$(0,0)$", r"$(1,2)$", r"$(-1,-2)$"],
        "correct_idx": 0
    })

    # Q4
    bank.append({
        "id": "ex_4", "type": "algebra",
        "en_latex": r"f(x) = x + 3(1-x)^{1/3}",
        "ar_latex": r"f(x) = x + 3(1-x)^{1/3}",
        "question_en": "Identify inflection points:",
        "question_ar": "حدد نقاط الانقلاب:",
        "options": [r"$(1, 1)$", r"$(0, 3)$", r"$(-1, 0)$", r"None"],
        "correct_idx": 0
    })

    # Q5
    bank.append({
        "id": "ex_5", "type": "algebra",
        "en_latex": r"f(x) = \sin x - \cos x",
        "ar_latex": r"f(x) = \sin x - \cos x",
        "question_en": "Inflection points on $[0, 2\pi]$:",
        "question_ar": "نقاط الانقلاب في الفترة $[0, 2\pi]$:",
        "options": [
            r"$\frac{\pi}{4}, \frac{5\pi}{4}$",
            r"$\frac{3\pi}{4}, \frac{7\pi}{4}$",
            r"$\frac{\pi}{2}, \frac{3\pi}{2}$",
            r"$0, \pi$"
        ],
        "correct_idx": 0
    })

    # Q6 (Tan Inverse)
    bank.append({
        "id": "ex_6", "type": "algebra",
        "en_latex": r"f(x) = \tan^{-1}(x^2)",
        "ar_latex": r"f(x) = \tan^{-1}(x^2)",
        "question_en": "Interval where graph is Concave Down:",
        "question_ar": "الفترة التي تكون فيها الدالة مقعرة لأسفل:",
        "options": [
            r"$(-\infty, -\frac{1}{\sqrt{3}}) \cup (\frac{1}{\sqrt{3}}, \infty)$",
            r"$(-\frac{1}{\sqrt{3}}, \frac{1}{\sqrt{3}})$",
            r"$(0, \infty)$",
            r"$(-\infty, 0)$"
        ],
        "correct_idx": 0
    })

    # Q8 (Exponential)
    bank.append({
        "id": "ex_8", "type": "algebra",
        "en_latex": r"f(x) = x e^{-4x}",
        "ar_latex": r"f(x) = x e^{-4x}",
        "question_en": "Interval where graph is Concave Down:",
        "question_ar": "الفترة التي تكون فيها الدالة مقعرة لأسفل:",
        "options": [
            r"$(-\infty, 0.5)$",
            r"$(0.5, \infty)$",
            r"$(-\infty, 0)$",
            r"$(0, \infty)$"
        ],
        "correct_idx": 0
    })
    
    # سؤال إضافي: الثوابت
    bank.append({
        "id": "const_1", "type": "algebra",
        "en_latex": r"f(x) = x^3 + kx^2 + 5, \quad \text{Inflection at } x=2",
        "ar_latex": r"f(x) = x^3 + kx^2 + 5, \quad \text{نقطة انقلاب عند } x=2",
        "question_en": "Find the value of k:",
        "question_ar": "أوجد قيمة الثابت k:",
        "options": [r"$k = -6$", r"$k = -3$", r"$k = 3$", r"$k = 6$"],
        "correct_idx": 0
    })

    # === أسئلة الرسوم البيانية (Exercises 37-40) ===

    # Q37
    bank.append({
        "id": "q37", "type": "graph",
        "conditions_latex": r"""
        f(0)=0 \\
        f'(x) > 0 \quad \text{for } x < 1 \ (x \neq -1) \\
        f'(x) < 0 \quad \text{for } x > 1 \\
        f''(x) > 0 \quad \text{for } |x| > 1 \\
        f''(x) < 0 \quad \text{for } -1 < x < 0
        """,
        "question_en": "Select the graph satisfying these conditions:",
        "question_ar": "اختر الرسم البياني الذي يحقق الشروط:",
        "correct_func": lambda v: -0.5*((v**4)/4 + (v**3)/3 - (v**2)/2 - v), # شكل تقريبي يحقق الشروط
        "distractors": [lambda v: v**3 - 3*v, lambda v: -(v**2) + 2, lambda v: np.sin(v)]
    })

    # Q38
    bank.append({
        "id": "q38", "type": "graph",
        "conditions_latex": r"""
        f(0)=2, \quad f'(0)=1 \\
        f'(x) > 0 \quad \forall x \\
        f''(x) > 0 \quad \text{for } x < 0 \\
        f''(x) < 0 \quad \text{for } x > 0
        """,
        "question_en": "Select the graph satisfying these conditions:",
        "question_ar": "اختر الرسم البياني الذي يحقق الشروط:",
        "correct_func": lambda v: 2 + np.arctan(v), 
        "distractors": [lambda v: 2 + v**3, lambda v: 2 + v**2, lambda v: 2 - np.exp(-v)]
    })

    # Q39 (W-Shape / M-Shape logic based on derivatives)
    bank.append({
        "id": "q39", "type": "graph",
        "conditions_latex": r"""
        f(0)=0, f(-1)=-1, f(1)=1 \\
        f'(x) > 0 \quad \text{for } x < -1, \ 0 < x < 1 \\
        f'(x) < 0 \quad \text{for } -1 < x < 0, \ x > 1
        """,
        "question_en": "Select the graph satisfying these conditions:",
        "question_ar": "اختر الرسم البياني الذي يحقق الشروط:",
        "correct_func": lambda v: 2*v**2 - v**4, # شكل M
        "distractors": [lambda v: v**2, lambda v: v**3, lambda v: -(v**2)]
    })

    # Q40 (The Cusp)
    bank.append({
        "id": "q40", "type": "graph",
        "conditions_latex": r"""
        f(1)=0 \\
        f'(x) < 0 \ (x < 1), \quad f'(x) > 0 \ (x > 1) \\
        f''(x) < 0 \quad \text{everywhere } (x \neq 1)
        """,
        "question_en": "Select the graph satisfying these conditions (Cusp):",
        "question_ar": "اختر الرسم البياني (نقطة زاوية/ناب):",
        "correct_func": lambda v: (np.abs(v-1))**(2/3), # دالة الناب المقعرة لأسفل
        "distractors": [lambda v: (v-1)**2, lambda v: -(v-1)**2, lambda v: np.abs(v-1)]
    })

    return bank

# --- إدارة الحالة (Session State) ---
if 'step' not in st.session_state: st.session_state['step'] = 'login'
if 'student_name' not in st.session_state: st.session_state['student_name'] = ""
if 'section' not in st.session_state: st.session_state['section'] = ""

# ==========================================
# 1. صفحة الدخول (LOGIN PAGE)
# ==========================================
if st.session_state['step'] == 'login':
    show_header()
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h3>🎓 Student Login / تسجيل دخول الطالب</h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        col1, col2 = st.columns(2)
        with col1:
            name_input = st.text_input("Full Name / الاسم الثلاثي")
        with col2:
            sec_input = st.text_input("Section / الشعبة")
        
        submitted = st.form_submit_button("Start Quiz 🚀")
        
        if submitted:
            if name_input.strip():
                st.session_state['student_name'] = name_input
                st.session_state['section'] = sec_input
                
                # إعداد الأسئلة
                all_bank = get_full_question_bank()
                q_count = min(10, len(all_bank))
                st.session_state['quiz_questions'] = random.sample(all_bank, q_count)
                
                st.session_state['current_index'] = 0
                st.session_state['score'] = 0
                st.session_state['history'] = []
                st.session_state['shuffled_options'] = None
                st.session_state['feedback_given'] = False
                
                st.session_state['step'] = 'quiz'
                st.rerun()
            else:
                st.error("⚠️ Please enter your name. الرجاء كتابة الاسم.")

# ==========================================
# 2. صفحة الاختبار (QUIZ PAGE)
# ==========================================
elif st.session_state['step'] == 'quiz':
    show_header()
    
    # معلومات الطالب وشريط التقدم
    questions = st.session_state['quiz_questions']
    idx = st.session_state['current_index']
    curr = questions[idx]
    
    st.markdown(f"**Student:** {st.session_state['student_name']} | **Question:** {idx + 1} / {len(questions)}")
    st.progress((idx + 1) / len(questions))
    st.divider()

    # --- عرض السؤال (فصلنا النصوص عن المعادلات لضمان عدم حدوث أخطاء) ---
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown(f'<div class="question-container ltr-text"><strong>{curr["question_en"]}</strong></div>', unsafe_allow_html=True)
        # عرض المعادلة الإنجليزية باستخدام st.latex مباشرة
        if 'en_latex' in curr:
            st.latex(curr['en_latex'])
        elif 'conditions_latex' in curr:
            st.latex(curr['conditions_latex'])
            
    with c2:
        st.markdown(f'<div class="question-container rtl-text"><strong>{curr["question_ar"]}</strong></div>', unsafe_allow_html=True)
        # عرض المعادلة العربية (نفس المعادلة عادة)
        if 'ar_latex' in curr:
            st.latex(curr['ar_latex'])
        elif 'conditions_latex' in curr:
            st.latex(curr['conditions_latex'])
    
    st.write("---")

    # --- خلط الخيارات ---
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

    # --- عرض الخيارات ---
    cols = st.columns(2) + st.columns(2)
    x_vals = np.linspace(-3.2, 3.2, 300)
    
    for i, opt in enumerate(opts):
        with cols[i]:
            if curr['type'] == 'graph':
                # رسم بياني
                fig = plot_textbook_graph(x_vals, opt['data'](x_vals))
                st.pyplot(fig, use_container_width=True)
                btn_txt = f"Graph {i+1}"
            else:
                # خيار نصي (معادلة)
                st.write("") # مسافة للتنسيق
                btn_txt = opt['data'] # النص هو المعادلة
            
            # الأزرار
            if not st.session_state['feedback_given']:
                if st.button(btn_txt, key=f"btn_{idx}_{i}"):
                    is_corr = opt['correct']
                    if is_corr: st.session_state['score'] += 1
                    
                    # تسجيل السجل
                    ans_label = "Graph" if curr['type']=='graph' else opt['label']
                    status = "✅" if is_corr else "❌"
                    st.session_state['history'].append(f"Q{idx+1}: {status} ({ans_label})")
                    
                    st.session_state['feedback_given'] = True
                    st.rerun()
            else:
                # بعد الإجابة
                if opt['correct']:
                    st.success("✅ Correct")
                else:
                    st.warning("❌") # زر باهت

    # --- زر التالي ---
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

# ==========================================
# 3. صفحة النتيجة (RESULT PAGE)
# ==========================================
elif st.session_state['step'] == 'result':
    show_header()
    
    score = st.session_state['score']
    total = len(st.session_state['quiz_questions'])
    name = st.session_state['student_name']
    
    st.balloons()
    st.markdown(f"""
    <div class="final-card">
        <div>Good Job, {name}!</div>
        <div style="font-size: 50px; margin-top: 10px;">{score} / {total}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # إرسال البيانات
    if 'data_sent' not in st.session_state:
        with st.spinner("Saving results..."):
            history_str = " | ".join(st.session_state['history'])
            success = send_to_google_sheet(name, st.session_state['section'], score, total, history_str)
            if success:
                st.success("✅ Results sent to Mr. Ibrahim successfully!")
                st.session_state['data_sent'] = True
            else:
                st.error("⚠️ Connection Error. Please screenshot this page.")
    
    st.write("---")
    if st.button("🔄 New Student"):
        st.session_state.clear()
        st.rerun()
