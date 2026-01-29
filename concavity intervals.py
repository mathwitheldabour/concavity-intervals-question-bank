import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# إعدادات الصفحة
st.set_page_config(layout="wide", page_title="Calculus Advanced Quiz")

# --- CSS للتنسيق (نفس التنسيق السابق مع تحسينات للأزرار النصية) ---
st.markdown("""
<style>
    .rtl-box {
        direction: rtl;
        text-align: right;
        font-family: 'Arial', sans-serif;
        font-size: 18px;
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-right: 6px solid #2980b9;
        margin-bottom: 10px;
    }
    .ltr-box {
        direction: ltr;
        text-align: left;
        font-family: 'Arial', sans-serif;
        font-size: 18px;
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 6px solid #2980b9;
        margin-bottom: 10px;
    }
    .header-text-ar { text-align: right; font-weight: bold; font-size: 20px; margin-bottom: 5px; color: #2c3e50; }
    .header-text-en { text-align: left; font-weight: bold; font-size: 20px; margin-bottom: 5px; color: #2c3e50; }
    
    /* تنسيق أزرار الاختيار النصية */
    .stButton button {
        width: 100%;
        font-weight: bold;
        font-size: 18px;
        padding: 15px;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s;
    }
    .stButton button:hover {
        border-color: #2980b9;
        color: #2980b9;
    }
    
    /* النتيجة النهائية */
    .final-score {
        text-align: center;
        padding: 40px;
        background-color: #d4edda;
        border-radius: 15px;
        border: 2px solid #c3e6cb;
        color: #155724;
        font-size: 28px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- محرك الرسم (للأسئلة البيانية) ---
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

# --- بنك الأسئلة الشامل (Algebraic & Graphical) ---
def get_full_question_bank():
    bank = []

    # ==========================================
    # القسم الأول: أسئلة المعادلات (Algebraic)
    # تمارين 1-8 وأسئلة الثوابت
    # ==========================================

    # س1: كثيرة حدود (Exercise 1)
    bank.append({
        "id": "alg_1",
        "type": "algebra", # نوع السؤال: جبري (اختيارات نصية)
        "en_latex": r"Determine the inflection point of: \quad f(x) = x^3 - 3x^2 + 4x - 1",
        "ar_latex": r"حدد نقطة الانقلاب للدالة: \quad f(x) = x^3 - 3x^2 + 4x - 1",
        "options": [
            r"$(1, 1)$",          # Correct: f''(x)=6x-6=0 -> x=1, f(1)=1
            r"$(1, -1)$",
            r"$(0, -1)$",
            r"No inflection point"
        ],
        "correct_idx": 0
    })

    # س2: فترات التقعر (Exercise 2 Modified)
    bank.append({
        "id": "alg_2",
        "type": "algebra",
        "en_latex": r"Find the interval where $f(x) = x^4 - 6x^2 + 2x + 3$ is **Concave Up**.",
        "ar_latex": r"أوجد الفترة التي تكون فيها الدالة $f(x) = x^4 - 6x^2 + 2x + 3$ **مقعرة لأعلى**.",
        "options": [
            r"$(-\infty, -1) \cup (1, \infty)$", # Correct: f''=12x^2-12 > 0 -> x^2>1
            r"$(-1, 1)$",
            r"$(-\infty, 1)$",
            r"$(1, \infty)$"
        ],
        "correct_idx": 0
    })

    # س3: دالة نسبية (Exercise 3)
    bank.append({
        "id": "alg_3",
        "type": "algebra",
        "en_latex": r"Determine the inflection points of: \quad f(x) = x + \frac{1}{x}",
        "ar_latex": r"حدد نقاط الانقلاب للدالة: \quad f(x) = x + \frac{1}{x}",
        "options": [
            r"No inflection points", # Correct: f'' = 2/x^3 (changes sign at 0 but undefined)
            r"$(0, 0)$",
            r"$(1, 2)$",
            r"$(-1, -2)$"
        ],
        "correct_idx": 0
    })

    # س4: دالة مثلثية (Exercise 5)
    bank.append({
        "id": "alg_4",
        "type": "algebra",
        "en_latex": r"Find the x-coordinates of inflection points for $f(x) = \sin x - \cos x$ on $[0, 2\pi]$.",
        "ar_latex": r"أوجد الإحداثيات السينية لنقاط الانقلاب للدالة $f(x) = \sin x - \cos x$ في الفترة $[0, 2\pi]$.",
        "options": [
            r"$x = \frac{\pi}{4}, \frac{5\pi}{4}$", # Correct: f'' = -sin + cos = 0 -> tan=1
            r"$x = \frac{3\pi}{4}, \frac{7\pi}{4}$",
            r"$x = \frac{\pi}{2}, \frac{3\pi}{2}$",
            r"$x = 0, \pi, 2\pi$"
        ],
        "correct_idx": 0
    })

    # س5: دالة أسية (Exercise 8)
    bank.append({
        "id": "alg_5",
        "type": "algebra",
        "en_latex": r"Determine the interval where $f(x) = xe^{-4x}$ is **Concave Down**.",
        "ar_latex": r"حدد الفترة التي تكون فيها الدالة $f(x) = xe^{-4x}$ **مقعرة لأسفل**.",
        "options": [
            r"$(-\infty, 0.5)$", # Correct: f'' = 8e^-4x (2x - 1). Concave Down when f'' < 0 -> 2x < 1
            r"$(0.5, \infty)$",
            r"$(-\infty, 0)$",
            r"$(0, \infty)$"
        ],
        "correct_idx": 0
    })

    # س6: إيجاد الثوابت - مجهول واحد (Finding Constants)
    bank.append({
        "id": "const_1",
        "type": "algebra",
        "en_latex": r"If $f(x) = x^3 + kx^2 + 5$ has an inflection point at $x=2$, find the value of $k$.",
        "ar_latex": r"إذا كان للدالة $f(x) = x^3 + kx^2 + 5$ نقطة انقلاب عند $x=2$، فأوجد قيمة الثابت $k$.",
        "options": [
            r"$k = -3$", # Correct: f'=3x^2+2kx, f''=6x+2k. f''(2)=12+2k=0 -> k=-6. Wait. 6(2)+2k=0 -> 12=-2k -> k=-6.
            r"$k = -6$", 
            r"$k = 3$",
            r"$k = 6$"
        ],
        "correct_idx": 1 # k = -6 is correct logic: 12 + 2k = 0
    })

    # س7: إيجاد الثوابت - مجهولين (Finding a, b)
    bank.append({
        "id": "const_2",
        "type": "algebra",
        "en_latex": r"Let $f(x) = ax^3 + bx^2$. The graph has an inflection point at $(1, 2)$. Find $a$ and $b$.",
        "ar_latex": r"لتكن $f(x) = ax^3 + bx^2$. إذا كان للمنحنى نقطة انقلاب عند $(1, 2)$، فأوجد قيمتي $a$ و $b$.",
        "options": [
            r"$a = -1, \quad b = 3$", # Correct logic below:
            # f(1)=2 => a+b=2
            # f''(1)=0 => f'=3ax^2+2bx => f''=6ax+2b => 6a+2b=0 => b=-3a
            # Sub b: a - 3a = 2 => -2a=2 => a=-1. b=3.
            r"$a = 1, \quad b = 1$",
            r"$a = 2, \quad b = 0$",
            r"$a = -2, \quad b = 4$"
        ],
        "correct_idx": 0
    })

    # ==========================================
    # القسم الثاني: أسئلة الرسوم البيانية (Graphical)
    # (الأسئلة السابقة 37-40)
    # ==========================================

    # س8: الرسم البياني (سؤال 37)
    bank.append({
        "id": "graph_37",
        "type": "graph", # نوع السؤال: رسم بياني
        "en_latex": r'''
        \begin{aligned}
        &f(0)=0 \\
        &f'(x) > 0 \quad \text{for} \quad x < 1 \quad (x \neq -1) \\
        &f'(x) < 0 \quad \text{for} \quad x > 1 \\
        &f''(x) > 0 \quad \text{for} \quad |x| > 1, \quad f''(x) < 0 \quad \text{for} \quad -1 < x < 0
        \end{aligned}
        ''',
        "ar_latex": r'''
        \begin{aligned}
        &f(0)=0 \\
        &f'(x) > 0 \quad \text{عندما} \quad x < 1 \quad (x \neq -1) \\
        &f'(x) < 0 \quad \text{عندما} \quad x > 1 \\
        &f''(x) > 0 \quad \text{عندما} \quad |x| > 1, \quad f''(x) < 0 \quad \text{عندما} \quad -1 < x < 0
        \end{aligned}
        ''',
        "correct_func": lambda v: -0.5*((v**4)/4 + (v**3)/3 - (v**2)/2 - v),
        "distractors": [lambda v: v**3 - 3*v, lambda v: -(v**2) + 1, lambda v: np.sin(v)]
    })

    # س9: الرسم البياني (سؤال 38)
    bank.append({
        "id": "graph_38",
        "type": "graph",
        "en_latex": r'''
        \begin{aligned}
        &f(0)=2, \quad f'(0)=1 \\
        &f'(x) > 0 \quad \text{for all } x \\
        &f''(x) > 0 \quad \text{for} \quad x < 0, \quad f''(x) < 0 \quad \text{for} \quad x > 0
        \end{aligned}
        ''',
        "ar_latex": r'''
        \begin{aligned}
        &f(0)=2, \quad f'(0)=1 \\
        &f'(x) > 0 \quad \text{لجميع قيم } x \\
        &f''(x) > 0 \quad \text{عندما} \quad x < 0, \quad f''(x) < 0 \quad \text{عندما} \quad x > 0
        \end{aligned}
        ''',
        "correct_func": lambda v: 2 + np.arctan(v),
        "distractors": [lambda v: 2 + v**3, lambda v: 2 + v**2, lambda v: 2 - np.arctan(v)]
    })
    
    # س10: سؤال إضافي بياني (Concave Up Parabola)
    bank.append({
        "id": "graph_extra",
        "type": "graph",
        "en_latex": r"Select the graph of a function where $f''(x) > 0$ for all real numbers.",
        "ar_latex": r"اختر الرسم البياني لدالة تحقق $f''(x) > 0$ لجميع الأعداد الحقيقية (مقعرة لأعلى دائماً).",
        "correct_func": lambda v: v**2 - 2,
        "distractors": [lambda v: -(v**2) + 2, lambda v: v**3, lambda v: np.sin(v)]
    })

    return bank

# --- إدارة حالة الاختبار ---

def start_new_quiz():
    full_bank = get_full_question_bank()
    # سحب أسئلة عشوائية (مثلاً 5 أسئلة لكل اختبار)
    # يمكنك زيادة الرقم هنا
    num_questions = min(5, len(full_bank))
    selected_questions = random.sample(full_bank, num_questions)
    
    st.session_state['quiz_questions'] = selected_questions
    st.session_state['current_index'] = 0
    st.session_state['score'] = 0
    st.session_state['quiz_finished'] = False
    st.session_state['shuffled_options'] = None
    st.session_state['feedback_given'] = False

if 'quiz_questions' not in st.session_state:
    start_new_quiz()

# المتغيرات الحالية
questions = st.session_state['quiz_questions']
idx = st.session_state['current_index']
score = st.session_state['score']
is_finished = st.session_state['quiz_finished']

# --- الواجهة الرئيسية ---

if not is_finished:
    # شريط التقدم
    st.progress((idx) / len(questions))
    st.caption(f"Question {idx + 1} of {len(questions)} | Score: {score}")
else:
    st.progress(1.0)

st.divider()

# --- منطق العرض (انتهى الاختبار / جاري الاختبار) ---

if is_finished:
    final_score_pct = (score / len(questions)) * 100
    if final_score_pct == 100:
        msg = "Excellent! درجة كاملة 🎉"
        st.balloons()
    elif final_score_pct >= 80:
        msg = "Great Job! أداء ممتاز 👏"
    else:
        msg = "Good effort! حاول مرة أخرى 💪"
        
    st.markdown(f"""
    <div class="final-score">
    {msg}<br><br>
    Final Score: {score} / {len(questions)}
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Start New Quiz / اختبار جديد", type="primary"):
        start_new_quiz()
        st.rerun()

else:
    curr_q = questions[idx]
    
    # خلط الخيارات (مرة واحدة لكل سؤال)
    if st.session_state['shuffled_options'] is None:
        if curr_q['type'] == 'graph':
            # خلط للرسوم
            opts = [{'func': curr_q['correct_func'], 'is_correct': True}]
            for d in curr_q['distractors']:
                opts.append({'func': d, 'is_correct': False})
            random.shuffle(opts)
            st.session_state['shuffled_options'] = opts
        else:
            # خلط للنصوص (مع حفظ المؤشر الصحيح)
            # الطريقة: ننشئ قائمة كائنات تحتوي النص وهل هو صحيح أم لا
            txt_opts = []
            for i, txt in enumerate(curr_q['options']):
                txt_opts.append({'text': txt, 'is_correct': (i == curr_q['correct_idx'])})
            random.shuffle(txt_opts)
            st.session_state['shuffled_options'] = txt_opts
    
    opts = st.session_state['shuffled_options']

    # --- عرض السؤال ---
    h_en, h_ar = st.columns(2)
    
    # عنوان ديناميكي حسب نوع السؤال
    if curr_q['type'] == 'graph':
        title_en = "Select the graph that satisfies:"
        title_ar = "اختر الرسم البياني الذي يحقق:"
    else:
        title_en = "Solve and select the correct answer:"
        title_ar = "حل المسألة واختر الإجابة الصحيحة:"

    with h_en: st.markdown(f'<div class="header-text-en">{title_en}</div>', unsafe_allow_html=True)
    with h_ar: st.markdown(f'<div class="header-text-ar">{title_ar}</div>', unsafe_allow_html=True)

    # عرض نص السؤال (Latex)
    col_en, col_ar = st.columns(2)
    with col_en:
        st.markdown('<div class="ltr-box">', unsafe_allow_html=True)
        st.latex(curr_q['en_latex'])
        st.markdown('</div>', unsafe_allow_html=True)
    with col_ar:
        st.markdown('<div class="rtl-box">', unsafe_allow_html=True)
        st.latex(curr_q['ar_latex'])
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")

    # --- عرض الخيارات ---
    
    # الحالة 1: أسئلة الرسم البياني
    if curr_q['type'] == 'graph':
        x_vals = np.linspace(-3.5, 3.5, 400)
        row1 = st.columns(2)
        row2 = st.columns(2)
        
        for i, col in enumerate(row1 + row2):
            with col:
                # رسم
                y_vals = opts[i]['func'](x_vals)
                fig = plot_textbook_graph(x_vals, y_vals)
                st.pyplot(fig, use_container_width=True)
                
                # زر
                btn_key = f"g_btn_{curr_q['id']}_{i}"
                if not st.session_state['feedback_given']:
                    if st.button(f"Graph {i+1}", key=btn_key):
                        if opts[i]['is_correct']:
                            st.session_state['score'] += 1
                            st.toast("✅ Correct Answer!")
                        else:
                            st.toast("❌ Wrong Answer")
                        st.session_state['feedback_given'] = True
                        st.rerun()
                else:
                    # إظهار الحل
                    if opts[i]['is_correct']:
                        st.success("✅ Correct Graph")
                    else:
                        st.button(f"Graph {i+1}", key=btn_key+"_dis", disabled=True)

    # الحالة 2: أسئلة الجبر (نصوص)
    else:
        # عرض الأزرار في شبكة 2x2
        row1 = st.columns(2)
        row2 = st.columns(2)
        cols = row1 + row2
        
        for i, option_item in enumerate(opts):
            with cols[i]:
                # الحاوية للصندوق
                if not st.session_state['feedback_given']:
                    # عرض الزر مع النص الرياضي
                    if st.button(option_item['text'], key=f"t_btn_{curr_q['id']}_{i}"):
                        if option_item['is_correct']:
                            st.session_state['score'] += 1
                            st.toast("✅ Correct Answer!")
                        else:
                            st.toast("❌ Wrong Answer")
                        st.session_state['feedback_given'] = True
                        st.rerun()
                else:
                    # مرحلة ما بعد الإجابة
                    if option_item['is_correct']:
                        st.success(f"✅ {option_item['text']}")
                    else:
                        # زر معطل للإجابات الخاطئة
                        st.warning(f"❌ {option_item['text']}")

    # --- زر التالي ---
    if st.session_state['feedback_given']:
        st.write("---")
        btn_txt = "Next Question ➡" if idx < len(questions) - 1 else "Show Results 🏁"
        if st.button(btn_txt, type="primary"):
            if idx < len(questions) - 1:
                st.session_state['current_index'] += 1
                st.session_state['shuffled_options'] = None
                st.session_state['feedback_given'] = False
            else:
                st.session_state['quiz_finished'] = True
            st.rerun()