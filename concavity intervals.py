import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(layout="wide", page_title="Mr. Ibrahim Math Quiz")

# --- CSS: تنسيق الاسم، الاتجاهات، ورابط الواتس أب ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cairo:wght@600&display=swap');

    /* رابط الواتس أب (تنسيق الاسم كزر) */
    .whatsapp-link {
        text-decoration: none !important;
        display: block;
        text-align: center;
        transition: transform 0.2s;
    }
    .whatsapp-link:hover {
        transform: scale(1.05);
        cursor: pointer;
    }

    /* تنسيق اسم المستر */
    .branding-header {
        font-family: 'Great Vibes', cursive;
        font-size: 55px;
        text-align: center;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        padding: 10px;
        width: 100%;
    }
    
    .contact-subtext {
        text-align: center;
        color: #2a5298;
        font-family: 'Cairo', sans-serif;
        font-size: 14px;
        margin-bottom: 30px;
    }

    /* صناديق الأسئلة */
    .question-box {
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        font-size: 20px;
        line-height: 1.8;
    }
    
    /* الصندوق العربي: اتجاه يمين، لكن المعادلات يسار */
    .rtl-box {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background-color: #fcfcfc;
        border-right: 6px solid #2980b9;
        color: #2c3e50;
    }
    
    /* الصندوق الإنجليزي */
    .ltr-box {
        direction: ltr;
        text-align: left;
        font-family: sans-serif;
        background-color: #fcfcfc;
        border-left: 6px solid #2980b9;
        color: #2c3e50;
    }

    /* إجبار المعادلات داخل النص العربي على الاتجاه الصحيح */
    .rtl-box .katex {
        direction: ltr;
        unicode-bidi: embed;
        font-family: 'Times New Roman', serif; 
    }

    /* الأزرار */
    .stButton button {
        width: 100%;
        font-weight: bold;
        font-size: 18px;
        padding: 12px;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        background-color: white;
        transition: all 0.3s;
    }
    .stButton button:hover {
        border-color: #2a5298;
        color: white;
        background-color: #2a5298;
    }
    
    /* بطاقة النتيجة */
    .final-card {
        text-align: center;
        padding: 50px;
        background-color: #d4edda;
        border-radius: 20px;
        border: 2px solid #c3e6cb;
        color: #155724;
        font-family: 'Cairo', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# --- دالة العنوان (مع رابط واتس أب) ---
def show_header():
    # الرابط يوجه لرقمك مباشرة
    whatsapp_url = "https://wa.me/971502188644"
    st.markdown(f"""
    <a href="{whatsapp_url}" target="_blank" class="whatsapp-link" title="تواصل عبر واتس أب">
        <div class="branding-header">Mr. Ibrahim Eldabour</div>
        <div class="contact-subtext">Click to Chat on WhatsApp | اضغط للتواصل واتس أب</div>
    </a>
    """, unsafe_allow_html=True)

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
    
    y_max = np.max(y)
    y_min = np.min(y)
    # ضبط حدود الرسم ليكون واضحاً
    ax.set_ylim(max(y_min - 1, -5), min(y_max + 1, 5))
    ax.set_xlim(-3.5, 3.5)
    
    plt.tight_layout()
    return fig

# --- بنك الأسئلة (تم ضبط الرموز لتكون MathJax) ---
def get_full_question_bank():
    bank = []

    # Q1
    bank.append({
        "id": "ex_1", "type": "algebra",
        # السؤال العربي: النصوص عربية لكن الرموز داخل $$ لضمان التنسيق
        "ar_text": r"حدد **نقطة الانقلاب** للدالة: $$f(x) = x^3 - 3x^2 + 4x - 1$$",
        "en_text": r"Determine the **inflection point** of: $$f(x) = x^3 - 3x^2 + 4x - 1$$",
        "options": [r"$(1, 1)$", r"$(1, -1)$", r"$(0, -1)$", r"None"],
        "correct_idx": 0
    })

    # Q2
    bank.append({
        "id": "ex_2", "type": "algebra",
        "ar_text": r"أوجد الفترة التي تكون فيها الدالة $$f(x) = x^4 - 6x^2 + 2x + 3$$ **مقعرة لأعلى**:",
        "en_text": r"Find the interval where $$f(x) = x^4 - 6x^2 + 2x + 3$$ is **Concave Up**:",
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
        "ar_text": r"حدد **نقاط الانقلاب** للدالة: $$f(x) = x + \frac{1}{x}$$",
        "en_text": r"Determine the **inflection points** of: $$f(x) = x + \frac{1}{x}$$",
        "options": [r"None (لا توجد)", r"$(0,0)$", r"$(1,2)$", r"$(-1,-2)$"],
        "correct_idx": 0
    })

    # Q4
    bank.append({
        "id": "ex_4", "type": "algebra",
        "ar_text": r"حدد نقاط الانقلاب للدالة: $$f(x) = x + 3(1-x)^{1/3}$$",
        "en_text": r"Identify inflection points for: $$f(x) = x + 3(1-x)^{1/3}$$",
        "options": [r"$(1, 1)$", r"$(0, 3)$", r"$(-1, 0)$", r"None"],
        "correct_idx": 0
    })

    # Q5
    bank.append({
        "id": "ex_5", "type": "algebra",
        "ar_text": r"أوجد الإحداثيات السينية لنقاط الانقلاب للدالة $$f(x) = \sin x - \cos x$$ في الفترة $$[0, 2\pi]$$:",
        "en_text": r"Find x-coordinates of inflection points for $$f(x) = \sin x - \cos x$$ on $$[0, 2\pi]$$:",
        "options": [
            r"$$\frac{\pi}{4}, \frac{5\pi}{4}$$",
            r"$$\frac{3\pi}{4}, \frac{7\pi}{4}$$",
            r"$$\frac{\pi}{2}, \frac{3\pi}{2}$$",
            r"$$0, \pi$$"
        ],
        "correct_idx": 0
    })

    # Q6
    bank.append({
        "id": "ex_6", "type": "algebra",
        "ar_text": r"حدد الفترة التي تكون فيها الدالة $$f(x) = \tan^{-1}(x^2)$$ **مقعرة لأسفل**:",
        "en_text": r"Interval where $$f(x) = \tan^{-1}(x^2)$$ is **Concave Down**:",
        "options": [
            r"$$(-\infty, -\frac{1}{\sqrt{3}}) \cup (\frac{1}{\sqrt{3}}, \infty)$$",
            r"$$(-\frac{1}{\sqrt{3}}, \frac{1}{\sqrt{3}})$$",
            r"$$(0, \infty)$$",
            r"$$(-\infty, 0)$$"
        ],
        "correct_idx": 0
    })

    # Q8
    bank.append({
        "id": "ex_8", "type": "algebra",
        "ar_text": r"حدد الفترة التي تكون فيها الدالة $$f(x) = xe^{-4x}$$ **مقعرة لأسفل**:",
        "en_text": r"Interval where $$f(x) = xe^{-4x}$$ is **Concave Down**:",
        "options": [
            r"$$(-\infty, 0.5)$$",
            r"$$(0.5, \infty)$$",
            r"$$(-\infty, 0)$$",
            r"$$(0, \infty)$$"
        ],
        "correct_idx": 0
    })
    
    # Constants Question
    bank.append({
        "id": "const_1", "type": "algebra",
        "ar_text": r"إذا كان للدالة $$f(x) = x^3 + kx^2 + 5$$ نقطة انقلاب عند $$x=2$$، فإن قيمة الثابت $$k$$ تساوي:",
        "en_text": r"If $$f(x) = x^3 + kx^2 + 5$$ has an inflection point at $$x=2$$, then $$k$$ equals:",
        "options": [r"$$k = -6$$", r"$$k = -3$$", r"$$k = 3$$", r"$$k = 6$$"],
        "correct_idx": 0
    })

    # === Graph Questions (37-40) ===

    # Q37
    bank.append({
        "id": "q37", "type": "graph",
        # تم وضع الشروط داخل aligned لترتيبها
        "ar_text": r"""
        **اختر الرسم الذي يحقق الشروط التالية:**
        $$
        \begin{aligned}
        &f(0)=0 \\
        &f'(x) > 0 \quad \text{for } x < 1 \ (x \neq -1) \\
        &f'(x) < 0 \quad \text{for } x > 1 \\
        &f''(x) > 0 \quad \text{for } |x| > 1 \\
        &f''(x) < 0 \quad \text{for } -1 < x < 0
        \end{aligned}
        $$
        """,
        "en_text": r"""
        **Select the graph satisfying these conditions:**
        $$
        \begin{aligned}
        &f(0)=0 \\
        &f'(x) > 0 \quad \text{for } x < 1 \ (x \neq -1) \\
        &f'(x) < 0 \quad \text{for } x > 1 \\
        &f''(x) > 0 \quad \text{for } |x| > 1 \\
        &f''(x) < 0 \quad \text{for } -1 < x < 0
        \end{aligned}
        $$
        """,
        "correct_func": lambda v: -0.5*((v**4)/4 + (v**3)/3 - (v**2)/2 - v), 
        "distractors": [lambda v: v**3 - 3*v, lambda v: -(v**2) + 2, lambda v: np.sin(v)]
    })

    # Q38
    bank.append({
        "id": "q38", "type": "graph",
        "ar_text": r"""
        **اختر الرسم الذي يحقق الشروط التالية:**
        $$
        \begin{aligned}
        &f(0)=2, \quad f'(0)=1 \\
        &f'(x) > 0 \quad \forall x \\
        &f''(x) > 0 \quad \text{for } x < 0 \\
        &f''(x) < 0 \quad \text{for } x > 0
        \end{aligned}
        $$
        """,
        "en_text": r"""
        **Select the graph satisfying these conditions:**
        $$
        \begin{aligned}
        &f(0)=2, \quad f'(0)=1 \\
        &f'(x) > 0 \quad \forall x \\
        &f''(x) > 0 \quad \text{for } x < 0 \\
        &f''(x) < 0 \quad \text{for } x > 0
        \end{aligned}
        $$
        """,
        "correct_func": lambda v: 2 + np.arctan(v), 
        "distractors": [lambda v: 2 + v**3, lambda v: 2 + v**2, lambda v: 2 - np.exp(-v)]
    })

    # Q39
    bank.append({
        "id": "q39", "type": "graph",
        "ar_text": r"""
        **اختر الرسم الذي يحقق الشروط التالية:**
        $$
        \begin{aligned}
        &f(0)=0, f(-1)=-1, f(1)=1 \\
        &f'(x) > 0 \quad \text{for } x < -1, \ 0 < x < 1 \\
        &f'(x) < 0 \quad \text{for } -1 < x < 0, \ x > 1
        \end{aligned}
        $$
        """,
        "en_text": r"""
        **Select the graph satisfying these conditions:**
        $$
        \begin{aligned}
        &f(0)=0, f(-1)=-1, f(1)=1 \\
        &f'(x) > 0 \quad \text{for } x < -1, \ 0 < x < 1 \\
        &f'(x) < 0 \quad \text{for } -1 < x < 0, \ x > 1
        \end{aligned}
        $$
        """,
        "correct_func": lambda v: 2*v**2 - v**4, 
        "distractors": [lambda v: v**2, lambda v: v**3, lambda v: -(v**2)]
    })

    # Q40
    bank.append({
        "id": "q40", "type": "graph",
        "ar_text": r"""
        **اختر الرسم الذي يحقق الشروط التالية:**
        $$
        \begin{aligned}
        &f(1)=0 \\
        &f'(x) < 0 \ (x < 1), \quad f'(x) > 0 \ (x > 1) \\
        &f''(x) < 0 \quad \text{everywhere } (x \neq 1)
        \end{aligned}
        $$
        """,
        "en_text": r"""
        **Select the graph satisfying these conditions:**
        $$
        \begin{aligned}
        &f(1)=0 \\
        &f'(x) < 0 \ (x < 1), \quad f'(x) > 0 \ (x > 1) \\
        &f''(x) < 0 \quad \text{everywhere } (x \neq 1)
        \end{aligned}
        $$
        """,
        "correct_func": lambda v: (np.abs(v-1))**(2/3), 
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
    <div style="text-align: center; margin-bottom: 20px; font-family: 'Cairo', sans-serif;">
        <h3>🎓 تسجيل دخول الطالب / Student Login</h3>
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
    
    questions = st.session_state['quiz_questions']
    idx = st.session_state['current_index']
    curr = questions[idx]
    
    # معلومات الطالب
    st.markdown(f"""
    <div style='text-align: center; color: #666; font-size: 14px; margin-bottom: 10px;'>
    Student: <b>{st.session_state['student_name']}</b> | Question {idx + 1} of {len(questions)}
    </div>
    """, unsafe_allow_html=True)
    
    st.progress((idx + 1) / len(questions))
    
    # --- عرض السؤال ---
    # نستخدم st.markdown مع الصناديق التي صممناها في CSS
    # لاحظ أننا نمرر النص العربي للمعادلة (التي تحتوي على رموز MathJax)
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown(f'<div class="question-box ltr-box">{curr["en_text"]}</div>', unsafe_allow_html=True)
            
    with c2:
        st.markdown(f'<div class="question-box rtl-box">{curr["ar_text"]}</div>', unsafe_allow_html=True)
    
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
                st.write("") 
                st.write("") 
                btn_txt = opt['data'] # النص هو المعادلة
            
            # الأزرار
            if not st.session_state['feedback_given']:
                if st.button(btn_txt, key=f"btn_{idx}_{i}"):
                    is_corr = opt['correct']
                    if is_corr: st.session_state['score'] += 1
                    
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
                    st.warning("❌") 

    # --- زر الانتقال ---
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
        <div style="font-size: 16px; margin-top: 20px; color: #155724;">Results are being sent to your teacher...</div>
    </div>
    """, unsafe_allow_html=True)
    
    # إرسال البيانات
    if 'data_sent' not in st.session_state:
        with st.spinner("Saving results..."):
            history_str = " | ".join(st.session_state['history'])
            success = send_to_google_sheet(name, st.session_state['section'], score, total, history_str)
            if success:
                st.success("✅ Results sent successfully!")
                st.session_state['data_sent'] = True
            else:
                st.error("⚠️ Connection Error. Please inform your teacher.")
    
    st.write("---")
    if st.button("🔄 New Student Login"):
        st.session_state.clear()
        st.rerun()
