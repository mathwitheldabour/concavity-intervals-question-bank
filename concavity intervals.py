import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(layout="wide", page_title="Math Quiz - 10 Questions")

# --- دالة الربط مع جوجل شيت ---
def send_to_google_sheet(student_name, section, score, total, details):
    try:
        # تحديد الصلاحيات والملف
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        
        # فتح الشيت (تأكد أن اسم الشيت في جوجل مطابق لهذا الاسم تماماً)
        sheet = client.open("Mr_Ibrahim_Quiz_Results").sheet1
        
        # التوقيت
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # تجهيز الصف: التاريخ، الاسم، الشعبة، الدرجة، التفاصيل
        row = [timestamp, student_name, section, f"{score}/{total}", details]
        
        # إضافة الصف
        sheet.append_row(row)
        return True
    except Exception as e:
        st.error(f"خطأ في الاتصال بقاعدة البيانات: {e}")
        return False

# --- تنسيق CSS ---
st.markdown("""
<style>
    .rtl-box { direction: rtl; text-align: right; background-color: #f0f8ff; padding: 15px; border-radius: 8px; border-right: 6px solid #2980b9; margin-bottom: 10px; color: black;}
    .ltr-box { direction: ltr; text-align: left; background-color: #f0f8ff; padding: 15px; border-radius: 8px; border-left: 6px solid #2980b9; margin-bottom: 10px; color: black;}
    .stButton button { width: 100%; font-weight: bold; font-size: 18px; padding: 12px; }
    .final-card { text-align: center; padding: 30px; background-color: #d4edda; border-radius: 15px; border: 2px solid #c3e6cb; color: #155724; font-size: 24px; font-weight: bold; }
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

# --- بنك الأسئلة (يجب أن يحتوي على أكثر من 10 أسئلة ليعمل السحب العشوائي) ---
def get_full_question_bank():
    bank = []

    # 1. سؤال جبري (Inflection Point)
    bank.append({
        "id": "alg_1", "type": "algebra",
        "en_text": r"Find the inflection point of: $$f(x) = x^3 - 3x^2 + 4x - 1$$",
        "ar_text": r"أوجد نقطة الانقلاب للدالة: $$f(x) = x^3 - 3x^2 + 4x - 1$$",
        "options": [r"$(1, 1)$", r"$(1, -1)$", r"$(0, -1)$", r"None"],
        "correct_idx": 0
    })
    
    # 2. سؤال جبري (Concave Up)
    bank.append({
        "id": "alg_2", "type": "algebra",
        "en_text": r"Interval where $$f(x) = x^4 - 6x^2$$ is Concave Up:",
        "ar_text": r"الفترة التي تكون فيها الدالة $$f(x) = x^4 - 6x^2$$ مقعرة لأعلى:",
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
        "en_text": r"Inflection points for $$f(x) = \sin x$$ on $$[0, 2\pi]$$:",
        "ar_text": r"نقاط الانقلاب للدالة $$f(x) = \sin x$$ في الفترة $$[0, 2\pi]$$:",
        "options": [r"$$x = \pi$$", r"$$x = \pi/2$$", r"$$x = 0$$", r"None"],
        "correct_idx": 0
    })

    # 5. سؤال رسم (Cusp)
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
        "en_text": r"If $$f(x)=x^3+kx^2$$ has inflection at $$x=1$$, find $$k$$.",
        "ar_text": r"إذا كان للدالة $$f(x)=x^3+kx^2$$ نقطة انقلاب عند $$x=1$$، أوجد $$k$$.",
        "options": [r"$$k=-3/2$$", r"$$k=-3$$", r"$$k=3$$", r"$$k=0$$"],
        "correct_idx": 0
    })

    # 7. سؤال رسم (Linear)
    bank.append({
        "id": "gr_3", "type": "graph",
        "en_text": r"Graph of $$f(x)$$ where $$f''(x) = 0$$ for all $$x$$.",
        "ar_text": r"رسم دالة حيث $$f''(x) = 0$$ لجميع القيم (لا تقعر).",
        "correct_func": lambda v: v,
        "distractors": [lambda v: v**2, lambda v: v**3, lambda v: np.sin(v)]
    })

    # 8. سؤال جبري (Rational)
    bank.append({
        "id": "alg_5", "type": "algebra",
        "en_text": r"Concavity of $$f(x) = 1/x$$ for $$x>0$$:",
        "ar_text": r"تقعر الدالة $$f(x) = 1/x$$ عندما $$x>0$$:",
        "options": [r"Concave Up (لأعلى)", r"Concave Down (لأسفل)", r"Inflection (انقلاب)", r"None"],
        "correct_idx": 0
    })

    # 9. سؤال رسم (S-Shape)
    bank.append({
        "id": "gr_4", "type": "graph",
        "en_text": r"Graph with inflection point at $$x=0$$ (Concave Down then Up).",
        "ar_text": r"رسم دالة لها نقطة انقلاب عند $$0$$ (مقعرة لأسفل ثم لأعلى).",
        "correct_func": lambda v: v**3,
        "distractors": [lambda v: -(v**3), lambda v: v**2, lambda v: -(v**2)]
    })

    # 10. سؤال جبري (Expo)
    bank.append({
        "id": "alg_6", "type": "algebra",
        "en_text": r"$$f(x)=e^x$$. Does it have inflection points?",
        "ar_text": r"الدالة $$f(x)=e^x$$، هل لها نقاط انقلاب؟",
        "options": [r"No (لا)", r"Yes at x=0", r"Yes at x=1", r"Yes at x=-1"],
        "correct_idx": 0
    })

    # 11. سؤال إضافي (لضمان وجود أكثر من 10)
    bank.append({
        "id": "alg_7", "type": "algebra",
        "en_text": r"$$f''(x) = 6x - 12$$. Inflection point is at:",
        "ar_text": r"إذا كانت $$f''(x) = 6x - 12$$، فإن نقطة الانقلاب تقع عند:",
        "options": [r"$$x=2$$", r"$$x=-2$$", r"$$x=0$$", r"$$x=12$$"],
        "correct_idx": 0
    })

    return bank

# --- إدارة الحالة ---
if 'step' not in st.session_state: st.session_state['step'] = 'login'
if 'student_name' not in st.session_state: st.session_state['student_name'] = ""
if 'section' not in st.session_state: st.session_state['section'] = ""

# --- 1. صفحة الدخول ---
if st.session_state['step'] == 'login':
    st.title("📝 Math Quiz (10 Questions)")
    st.markdown("### أدخل بياناتك لبدء الاختبار")
    with st.form("login"):
        name = st.text_input("Full Name / الاسم الثلاثي")
        sec = st.text_input("Section / الشعبة")
        if st.form_submit_button("Start Quiz / ابدأ"):
            if name:
                st.session_state['student_name'] = name
                st.session_state['section'] = sec
                
                # سحب 10 أسئلة عشوائية
                all_q = get_full_question_bank()
                # هنا الرقم 10 هو عدد الأسئلة المطلوبة
                q_count = min(10, len(all_q))
                st.session_state['quiz_questions'] = random.sample(all_q, q_count)
                
                st.session_state['current_index'] = 0
                st.session_state['score'] = 0
                st.session_state['history'] = []
                st.session_state['step'] = 'quiz'
                st.session_state['shuffled_options'] = None
                st.session_state['feedback_given'] = False
                st.rerun()
            else:
                st.warning("الرجاء كتابة الاسم")

# --- 2. صفحة الاختبار ---
elif st.session_state['step'] == 'quiz':
    qs = st.session_state['quiz_questions']
    idx = st.session_state['current_index']
    curr = qs[idx]
    
    # شريط التقدم
    st.progress((idx + 1) / len(qs))
    st.write(f"Question {idx+1} of {len(qs)}")
    st.divider()
    
    # عرض السؤال
    c1, c2 = st.columns(2)
    with c1: 
        st.markdown('<div class="ltr-box">', unsafe_allow_html=True)
        st.markdown(curr['en_text'])
        st.markdown('</div>', unsafe_allow_html=True)
    with c2: 
        st.markdown('<div class="rtl-box">', unsafe_allow_html=True)
        st.markdown(curr['ar_text'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    # خلط الخيارات (مرة واحدة)
    if st.session_state['shuffled_options'] is None:
        if curr['type'] == 'graph':
            opts = [{'data': curr['correct_func'], 'correct': True, 'label': 'Correct'}]
            for d in curr['distractors']:
                opts.append({'data': d, 'correct': False, 'label': 'Wrong'})
        else:
            opts = []
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
                btn_label = f"Select Graph {i+1}"
            else:
                # نص جبري
                st.write("") # مسافة
                btn_label = opt['data']
            
            # الأزرار
            if not st.session_state['feedback_given']:
                if st.button(btn_label, key=f"btn_{idx}_{i}"):
                    # تسجيل الإجابة
                    is_correct = opt['correct']
                    if is_correct: st.session_state['score'] += 1
                    
                    # حفظ في السجل
                    ans_text = "Graph" if curr['type']=='graph' else opt['label']
                    status = "✅" if is_correct else "❌"
                    st.session_state['history'].append(f"Q{idx+1}: {status} ({ans_text})")
                    
                    st.session_state['feedback_given'] = True
                    st.rerun()
            else:
                # بعد الإجابة (تعطيل الأزرار)
                if opt['correct']:
                    st.success("Correct Answer")
                else:
                    st.warning("Wrong Answer") # زر رمادي

    # زر الانتقال
    if st.session_state['feedback_given']:
        st.write("---")
        if idx < len(qs) - 1:
            if st.button("Next Question ➡"):
                st.session_state['current_index'] += 1
                st.session_state['shuffled_options'] = None
                st.session_state['feedback_given'] = False
                st.rerun()
        else:
            if st.button("Submit Results 🏁"):
                st.session_state['step'] = 'result'
                st.rerun()

# --- 3. صفحة النتيجة والإرسال ---
elif st.session_state['step'] == 'result':
    score = st.session_state['score']
    total = len(st.session_state['quiz_questions'])
    name = st.session_state['student_name']
    sec = st.session_state['section']
    history_str = " | ".join(st.session_state['history'])
    
    st.balloons()
    st.markdown(f"""
    <div class="final-card">
    Good Job, {name}!<br>
    Your Score: {score} / {total}
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # إرسال للبيانات (مرة واحدة)
    if 'sent' not in st.session_state:
        with st.spinner("Sending results to teacher..."):
            success = send_to_google_sheet(name, sec, score, total, history_str)
            if success:
                st.success("✅ تم إرسال النتيجة بنجاح!")
                st.session_state['sent'] = True
            else:
                st.error("فشل الإرسال. تأكد من الاتصال بالإنترنت.")
    
    if st.button("Start New Quiz (طالب جديد)"):
        st.session_state.clear()
        st.rerun()
