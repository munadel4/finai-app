import streamlit as st
import tempfile
import os
from fpdf import FPDF
import base64

st.markdown(
    """
    <style>
    body, .stApp {
        direction: rtl;
        text-align: right;
        font-family: 'Arial', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.set_page_config(page_title="FinAI - الذكاء المالي", layout="centered")

# --- العنوان ---
st.title("FinAI - الذكاء الاصطناعي في التمويل")
st.subheader("إعداد: حليمة جيتاوي")

# --- إدخال البيانات ---
st.markdown("### تقييم طلب قرض باستخدام الذكاء الاصطناعي")

income = st.number_input("الدخل الشهري (شيكل)", min_value=0.0, step=10.0)
loan_amount = st.number_input("قيمة القرض المطلوب (شيكل)", min_value=0.0, step=10.0)
commitments = st.number_input("الالتزامات الشهرية (شيكل)", min_value=0.0, step=10.0)
years = st.selectbox("عدد سنوات السداد", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

generate_report = False
analysis_result = ""
tip = ""

# --- تحليل الأهلية ---
if st.button("تحليل الأهلية"):
    if income == 0:
        st.error("يرجى إدخال دخل شهري أكبر من صفر.")
    else:
        monthly_payment = loan_amount / (years * 12)
        dti = (commitments + monthly_payment) / income

        st.markdown("#### نتيجة التحليل:")

        if dti < 0.3:
            analysis_result = (
                f"DTI = {dti:.2f} — ممتاز 👌\n\n"
                "نسبة الدين إلى الدخل منخفضة جداً، مما يشير إلى قدرة مالية جيدة لتغطية القرض. "
                "يُتوقع أن تحصل على موافقة سريعة من الجهة الممولة دون الحاجة لضمانات إضافية."
            )
            st.success(analysis_result)
        elif dti < 0.45:
            analysis_result = (
                f"DTI = {dti:.2f} — جيد ✅\n\n"
                "نسبة الدين إلى الدخل مقبولة. قد تطلب المؤسسة بعض الضمانات الإضافية أو معلومات عن مصدر الدخل."
            )
            st.info(analysis_result)
        elif dti < 0.6:
            analysis_result = (
                f"DTI = {dti:.2f} — متوسط ⚠️\n\n"
                "نسبة الدين مرتفعة نسبيًا. يُنصح بتقليل الالتزامات أو خفض مبلغ القرض لتحسين فرص القبول."
            )
            st.warning(analysis_result)
        else:
            analysis_result = (
                f"DTI = {dti:.2f} — مرتفع ❌\n\n"
                "نسبة الدين مرتفعة جدًا، مما يعرضك لرفض الطلب. حاول سداد بعض الالتزامات أو إعادة جدولة الخطة."
            )
            st.error(analysis_result)

        generate_report = True

# --- النصائح المالية ---
st.markdown("### نصيحة مالية ذكية")
goal = st.selectbox("ما هو هدفك المالي؟", ["ادخار", "استثمار", "سداد ديون"])

if goal == "ادخار":
    tip = (
        "- قم بتخصيص 20% من دخلك الشهري في حساب ادخار مستقل.\n"
        "- استخدم حساب توفير بفائدة تراكُمية.\n"
        "- ضع أهدافًا قصيرة المدى (مثل: 3 أشهر راتب كاحتياطي طوارئ).\n"
        "- تجنب السحب من هذا الحساب إلا في الضرورة القصوى."
    )
elif goal == "استثمار":
    tip = (
        "- ابدأ بمبالغ صغيرة في صناديق استثمار منخفضة المخاطر.\n"
        "- نوع محفظتك: جزء للأسهم، جزء للودائع، وجزء في الذهب.\n"
        "- لا تستثمر المال الذي قد تحتاجه خلال 6 أشهر.\n"
        "- تابع أداء استثماراتك شهريًا وقم بالمراجعة الدورية."
    )
else:
    tip = (
        "- قم بترتيب ديونك حسب الفائدة وابدأ بالأعلى.\n"
        "- استخدم استراتيجية 'كرة الثلج' أو 'الانهيار الجبلي'.\n"
        "- اجعل سداد الديون أولوية قبل التفكير في الاستثمار.\n"
        "- لا تقترض لسداد قرض سابق، فهذا يزيد من الأزمة."
    )

st.info("💡 " + tip.replace("\n", "\n\n"))

# --- توليد تقرير PDF ---
def generate_pdf(income, loan_amount, commitments, years, result, tip_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="تقرير تقييم القرض - FinAI", ln=True, align='C')
    pdf.cell(200, 10, txt="إعداد: حليمة جيتاوي", ln=True, align='R')
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"الدخل الشهري: {income} شيكل", ln=True)
    pdf.cell(200, 10, txt=f"قيمة القرض المطلوب: {loan_amount} شيكل", ln=True)
    pdf.cell(200, 10, txt=f"الالتزامات الشهرية: {commitments} شيكل", ln=True)
    pdf.cell(200, 10, txt=f"سنوات السداد: {years}", ln=True)

    pdf.ln(10)
    pdf.multi_cell(0, 10, f"نتيجة التحليل:\n{result}")
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"نصيحة مالية:\n{tip_text}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        pdf.output(tmpfile.name)
        return tmpfile.name

if generate_report:
    if st.button("تحميل تقرير PDF"):
        file_path = generate_pdf(income, loan_amount, commitments, years, analysis_result, tip)
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
            href = f'<a href="data:application/pdf;base64,{base64_pdf}" download="finai_report.pdf">📄 اضغط هنا لتحميل التقرير</a>'
            st.markdown(href, unsafe_allow_html=True)
        os.remove(file_path)

# --- تذييل ---
st.markdown("---")
st.caption("تطبيق تعليمي يعرض دور الذكاء الاصطناعي في اتخاذ قرارات التمويل الشخصي.")
