import streamlit as st

from agent import analyze_document
from pdf_reader import extract_text_from_pdf


st.set_page_config(
    page_title="FormBridge",
    page_icon="📄",
    layout="centered"
)


st.markdown(
    """
    <style>
        .block-container {
            max-width: 1100px;
            padding-top: 2.5rem;
            padding-bottom: 4rem;
        }

        .main-title {
            direction: ltr;
            text-align: left;
            font-family: Arial, sans-serif;
            font-size: 58px;
            font-weight: 700;
            color: #172033;
            margin-bottom: 5px;
        }

        .main-subtitle {
            direction: rtl;
            text-align: right;
            font-family: Arial, sans-serif;
            font-size: 28px;
            font-weight: 600;
            color: #364152;
            margin-bottom: 35px;
        }

        .section-title {
            direction: rtl;
            text-align: right;
            font-family: Arial, sans-serif;
            font-size: 24px;
            font-weight: 700;
            color: #172033;
            margin-top: 25px;
            margin-bottom: 10px;
        }

        .description {
            direction: rtl;
            text-align: right;
            font-family: Arial, sans-serif;
            font-size: 20px;
            line-height: 1.8;
            color: #4b5563;
            margin-bottom: 25px;
        }

        .result-box {
            direction: rtl;
            text-align: right;
            font-family: Arial, sans-serif;
            font-size: 19px;
            line-height: 1.9;
            background-color: #f7f9fc;
            border: 1px solid #d9e1ec;
            border-radius: 15px;
            padding: 25px;
            margin-top: 15px;
        }

        [data-testid="stFileUploader"] {
            direction: ltr;
        }

        [data-baseweb="select"] {
            direction: rtl;
        }

        .stButton button {
            min-height: 52px;
            border-radius: 10px;
            font-weight: 700;
        }

        .stButton button p {
            font-family: Arial, sans-serif;
            font-size: 19px;
        }

        [data-testid="stAlert"] p {
            direction: rtl;
            text-align: right;
            font-family: Arial, sans-serif;
            font-size: 18px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


if "document_text" not in st.session_state:
    st.session_state.document_text = None

if "analysis" not in st.session_state:
    st.session_state.analysis = None


st.markdown(
    '<div class="main-title">📄 FormBridge</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="main-subtitle">
        من المستند الرسمي إلى خطوات واضحة
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="description">
        ارفع مستندًا رسميًا، واختَر لغة الشرح.
        سيقرأ وكيل FormBridge المستند، ويشرح مضمونه،
        ويحدد ما يجب عليك فعله.
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="section-title">1. ارفع المستند</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "PDF document",
    type=["pdf"],
    label_visibility="collapsed"
)


st.markdown(
    '<div class="section-title">2. اختاري لغة الشرح</div>',
    unsafe_allow_html=True
)

selected_language = st.selectbox(
    "Output language",
    ["العربية", "עברית פשוטה"],
    label_visibility="collapsed"
)


if uploaded_file is not None:
    st.success(f"تم رفع الملف بنجاح: {uploaded_file.name}")

    analyze_button = st.button(
        "تحليل المستند",
        type="primary",
        use_container_width=True
    )

    if analyze_button:
        try:
            with st.spinner(
                "يقوم FormBridge بقراءة المستند وتحليله..."
            ):
                document_text = extract_text_from_pdf(
                    uploaded_file
                )

                if not document_text.strip():
                    st.error(
                        "لم نتمكن من قراءة النص من المستند."
                    )
                    st.stop()

                analysis = analyze_document(
                    document_text,
                    selected_language
                )

                st.session_state.document_text = document_text
                st.session_state.analysis = analysis

        except Exception as error:
            st.error(
                f"حدث خطأ أثناء تحليل المستند: {error}"
            )


if st.session_state.analysis:
    st.markdown(
        '<div class="section-title">نتيجة التحليل</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="result-box">
            {st.session_state.analysis}
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("عرض النص الأصلي المستخرج"):
        st.text_area(
            "Extracted document text",
            value=st.session_state.document_text,
            height=250,
            label_visibility="collapsed"
        )