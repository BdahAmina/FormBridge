"""UI strings, styling, and reusable Streamlit components."""

from __future__ import annotations

import html
from typing import Any

import streamlit as st

from models import DocumentAnalysis, NOT_MENTIONED_AR, NOT_MENTIONED_HE


LANGUAGE_AR = "العربية"
LANGUAGE_HE = "עברית פשוטה"

UI_STRINGS: dict[str, dict[str, str]] = {
    "ar": {
        "subtitle": "من المستند الرسمي إلى خطوات واضحة",
        "kicker": "ذكاء اصطناعي لفهم المستندات",
        "privacy_note": "يتم معالجة المستند فقط لأغراض التحليل ولا يُحفظ على الخادم.",
        "workspace_title": "مساحة العمل",
        "step_upload": "١. ارفع المستند",
        "step_language": "٢. اختر لغة الشرح",
        "step_analyze": "٣. حلّل واسأل",
        "status_idle": "بانتظار مستند",
        "status_ready": "جاهز للتحليل",
        "status_done": "تم التحليل",
        "empty_title": "ارفع مستندًا رسميًا للبدء",
        "empty_body": "سيقرأ FormBridge النص، يشرح المطلوب، ويحوّله إلى خطة عمل يمكنك السؤال عنها.",
        "upload_title": "رفع المستند",
        "upload_help": "PDF فقط — حتى 10 ميغابايت",
        "language_title": "لغة الشرح",
        "analyze_button": "تحليل المستند",
        "analyze_again": "إعادة التحليل",
        "replace_document": "استبدال المستند",
        "clear_document": "مسح المستند والبدء من جديد",
        "file_selected": "الملف المحدد",
        "analysis_title": "الملخص الذكي",
        "summary": "ملخص المستند",
        "document_type": "نوع المستند",
        "issuing_org": "الجهة المصدرة",
        "recipient": "المستلم / الشخص المعني",
        "why_sent": "سبب إرسال المستند",
        "urgency": "مستوى الإلحاح",
        "important_dates": "تواريخ مهمة",
        "deadlines": "مواعيد نهائية",
        "payments": "مبالغ ومدفوعات",
        "required_docs": "مستندات مطلوبة",
        "missing_info": "معلومات ناقصة أو غير واضحة",
        "actions_required": "إجراءات مطلوبة",
        "action_plan": "خطة عمل مرقمة",
        "suggested_reply": "رد رسمي مقترح (עברית)",
        "confidence": "درجة الثقة",
        "ocr_warning_title": "تنبيه OCR",
        "original_text": "النص الأصلي المستخرج",
        "chat_title": "أسئلة حول المستند",
        "chat_placeholder": "اكتب سؤالك عن المستند...",
        "chat_hint": "يمكنك السؤال عن المواعيد، المدفوعات، المستندات الناقصة، أو طلب شرح أبسط.",
        "clear_chat": "مسح المحادثة",
        "chat_agent_name": "FormBridge",
        "chat_suggestions_title": "أسئلة مقترحة",
        "chat_empty": "اسألني أي شيء عن المستند — سأجيب بناءً على محتواه فقط.",
        "rag_title": "مقاطع مسترجعة من المستند (RAG)",
        "rag_empty": "لم يُسترجع أي مقطع بعد. اسأل سؤالًا لعرض المقاطع ذات الصلة.",
        "rag_chunks": "مقاطع في قاعدة المعرفة",
        "official_sources": "مصادر رسمية",
        "secondary_source": "مصدر ثانوي",
        "no_official_source": "تعذر التحقق من إجابة رسمية. راجع الموقع الرسمي للجهة.",
        "form_identity": "تعرّف على النموذج",
        "download_txt": "تنزيل تقرير (TXT)",
        "download_md": "تنزيل تقرير (Markdown)",
        "footer_disclaimer": (
            "يوفر FormBridge شرحًا مولّدًا بالذكاء الاصطناعي "
            "ولا يُغني عن استشارة قانونية أو ضريبية أو طبية أو حكومية. "
            "المشروع غير تابع لحكومة إسرائيل. تحقق دائمًا من المصدر الرسمي."
        ),
        "urgency_low": "منخفض",
        "urgency_medium": "متوسط",
        "urgency_high": "مرتفع",
        "language_mismatch": "تم تغيير لغة الشرح. اضغط «إعادة التحليل» لعرض النتائج باللغة الجديدة.",
        "no_analysis_yet": "ارفع مستندًا واضغط «تحليل المستند» لبدء التحليل.",
        "processing": "يقوم FormBridge بقراءة المستند وتحليله...",
        "chat_processing": "جاري إعداد الإجابة...",
        "truncated_note": "تم اختصار المستند لأنه طويل جدًا. قد لا يشمل التحليل كل التفاصيل.",
        "example_questions": [
            "ماذا يجب أن أفعل؟",
            "ما الموعد النهائي؟",
            "اشرح هذا القسم بشكل أبسط",
            "ما المستندات الناقصة؟",
            "كم يجب أن أدفع؟",
            "اكتب ردًا رسميًا بالعبرية",
            "ترجم هذا القسم إلى العربية",
            "ماذا يحدث إذا لم أرد؟",
        ],
    },
    "he": {
        "subtitle": "ממסמך רשמי לצעדים ברורים",
        "kicker": "בינה מלאכותית להבנת מסמכים",
        "privacy_note": "המסמך מעובד לצורך ניתוח בלבד ואינו נשמר בשרת.",
        "workspace_title": "סביבת עבודה",
        "step_upload": "1. העלאת מסמך",
        "step_language": "2. בחירת שפה",
        "step_analyze": "3. ניתוח ושאלות",
        "status_idle": "ממתין למסמך",
        "status_ready": "מוכן לניתוח",
        "status_done": "הניתוח הושלם",
        "empty_title": "העלו מסמך רשמי כדי להתחיל",
        "empty_body": "FormBridge יקרא את הטקסט, יסביר את הנדרש, ויהפוך אותו לתוכנית פעולה שאפשר לשאול עליה.",
        "upload_title": "העלאת מסמך",
        "upload_help": "PDF בלבד — עד 10MB",
        "language_title": "שפת ההסבר",
        "analyze_button": "ניתוח המסמך",
        "analyze_again": "ניתוח מחדש",
        "replace_document": "החלפת מסמך",
        "clear_document": "ניקוי מסמך והתחלה מחדש",
        "file_selected": "קובץ שנבחר",
        "analysis_title": "תקציר חכם",
        "summary": "סיכום המסמך",
        "document_type": "סוג המסמך",
        "issuing_org": "הגורם המוציא",
        "recipient": "נמען / אדם רלוונטי",
        "why_sent": "מדוע נשלח המסמך",
        "urgency": "רמת דחיפות",
        "important_dates": "תאריכים חשובים",
        "deadlines": "מועדים אחרונים",
        "payments": "סכומים ותשלומים",
        "required_docs": "מסמכים נדרשים",
        "missing_info": "מידע חסר או לא ברור",
        "actions_required": "פעולות נדרשות",
        "action_plan": "תוכנית פעולה ממוספרת",
        "suggested_reply": "תגובה רשמית מוצעת (עברית)",
        "confidence": "רמת ביטחון",
        "ocr_warning_title": "אזהרת OCR",
        "original_text": "הטקסט המקורי שחולץ",
        "chat_title": "שאלות על המסמך",
        "chat_placeholder": "כתבו שאלה על המסמך...",
        "chat_hint": "אפשר לשאול על מועדים, תשלומים, מסמכים חסרים, או לבקש הסבר פשוט יותר.",
        "clear_chat": "ניקוי שיחה",
        "chat_agent_name": "FormBridge",
        "chat_suggestions_title": "שאלות מוצעות",
        "chat_empty": "שאלו אותי כל דבר על המסמך — אענה רק על בסיס תוכנו.",
        "rag_title": "קטעים שאוחזרו מהמסמך (RAG)",
        "rag_empty": "עדיין לא אוחזרו קטעים. שאלו שאלה כדי לראות את המקורות.",
        "rag_chunks": "קטעים בבסיס הידע",
        "official_sources": "מקורות רשמיים",
        "secondary_source": "מקור משני",
        "no_official_source": "לא ניתן לאמת תשובה ממקור רשמי. יש לבדוק באתר הרשות.",
        "form_identity": "זיהוי הטופס",
        "download_txt": "הורדת דוח (TXT)",
        "download_md": "הורדת דוח (Markdown)",
        "footer_disclaimer": (
            "FormBridge מספק הסבר שנוצר על ידי בינה מלאכותית "
            "ואינו ייעוץ משפטי, מס, רפואי או ממשלתי. "
            "הפרויקט אינו קשור לממשלת ישראל. יש לאמת מידע באתר הרשמי."
        ),
        "urgency_low": "נמוכה",
        "urgency_medium": "בינונית",
        "urgency_high": "גבוהה",
        "language_mismatch": "שפת ההסבר השתנתה. לחצו «ניתוח מחדש» כדי לראות תוצאות בשפה החדשה.",
        "no_analysis_yet": "העלו מסמך ולחצו «ניתוח המסמך» כדי להתחיל.",
        "processing": "FormBridge קורא ומנתח את המסמך...",
        "chat_processing": "מכין תשובה...",
        "truncated_note": "המסמך קוצר כי הוא ארוך מדי. ייתכן שהניתוח לא כולל את כל הפרטים.",
        "example_questions": [
            "מה אני צריך/ה לעשות?",
            "מה המועד האחרון?",
            "הסבירו את החלק הזה בצורה פשוטה יותר",
            "אילו מסמכים חסרים?",
            "כמה אני צריך/ה לשלם?",
            "כתבו תגובה רשמית בעברית",
            "תרגמו את החלק הזה לערבית",
            "מה קורה אם לא אגיב?",
        ],
    },
}

ERROR_MESSAGES: dict[str, dict[str, str]] = {
    "ar": {
        "no_file": "يرجى رفع ملف PDF قبل التحليل.",
        "invalid_type": "نوع الملف غير مدعوم. يرجى رفع ملف PDF.",
        "empty_pdf": "لم نتمكن من قراءة نص من المستند.",
        "password_pdf": "المستند محمي بكلمة مرور. يرجى رفع نسخة غير محمية.",
        "corrupted_pdf": "يبدو أن ملف PDF تالف أو غير صالح.",
        "ocr_missing": "OCR غير متاح. يرجى تثبيت Tesseract OCR.",
        "ocr_lang_missing": "ملفات لغات OCR مفقودة في مجلد tessdata.",
        "api_key_missing": "مفتاح GEMINI_API_KEY غير موجود في ملف .env.",
        "generic": "حدث خطأ أثناء المعالجة. يرجى المحاولة مرة أخرى.",
        "file_too_large": "حجم الملف كبير جدًا. الحد الأقصى 10 ميغابايت.",
    },
    "he": {
        "no_file": "יש להעלות קובץ PDF לפני הניתוח.",
        "invalid_type": "סוג הקובץ אינו נתמך. יש להעלות PDF.",
        "empty_pdf": "לא הצלחנו לקרוא טקסט מהמסמך.",
        "password_pdf": "המסמך מוגן בסיסמה. יש להעלות עותק ללא סיסמה.",
        "corrupted_pdf": "נראה שקובץ ה-PDF פגום או לא תקין.",
        "ocr_missing": "OCR אינו זמין. יש להתקין Tesseract OCR.",
        "ocr_lang_missing": "חסרים קובצי שפות OCR בתיקיית tessdata.",
        "api_key_missing": "מפתח GEMINI_API_KEY לא נמצא בקובץ .env.",
        "generic": "אירעה שגיאה בעיבוד. נסו שוב.",
        "file_too_large": "גודל הקובץ גדול מדי. המקסימום הוא 10MB.",
    },
}


def lang_code(selected_language: str) -> str:
    return "ar" if selected_language == LANGUAGE_AR else "he"


def ui(selected_language: str) -> dict[str, Any]:
    return UI_STRINGS[lang_code(selected_language)]


def errors(selected_language: str) -> dict[str, str]:
    return ERROR_MESSAGES[lang_code(selected_language)]


def rtl_block(content: str, *, extra_class: str = "") -> str:
    safe = html.escape(content).replace("\n", "<br>")
    class_attr = f"rtl-text {extra_class}".strip()
    return f'<div class="{class_attr}">{safe}</div>'


def inject_global_css() -> None:
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=Noto+Sans+Arabic:wght@400;500;600;700&family=Noto+Sans+Hebrew:wght@400;500;600;700&display=swap');

            :root {
                --fb-navy: #0a1b2e;
                --fb-blue: #185fa5;
                --fb-teal: #0f9d9a;
                --fb-ink: #0a1b2e;
                --fb-text: #142033;
                --fb-text-secondary: #3b4d63;
                --fb-text-muted: #6b7c90;
                --fb-bg: #e8eef4;
                --fb-surface: #ffffff;
                --fb-surface-soft: #f4f7fa;
                --fb-border: #d3deea;
                --fb-border-subtle: #e4ebf2;
                --fb-shadow: 0 10px 40px rgba(10, 27, 46, 0.07);
                --fb-shadow-soft: 0 2px 8px rgba(10, 27, 46, 0.04);
                --fb-warning-bg: #fff8e8;
                --fb-warning-border: #ecd59a;
                --fb-warning-text: #7a5600;
                --fb-chat-bg: #ffffff;
                --fb-code-bg: #eef4f8;
                --fb-blockquote-bg: #eef8f7;
                --fb-hero-glow: rgba(15, 157, 154, 0.12);
            }

            .stApp[data-theme="dark"],
            [data-theme="dark"] .stApp {
                --fb-navy: #e8f1fb;
                --fb-blue: #7eb6ff;
                --fb-teal: #3ecfcb;
                --fb-ink: #e8f1fb;
                --fb-text: #e8eef6;
                --fb-text-secondary: #c2cedc;
                --fb-text-muted: #8fa0b3;
                --fb-bg: #070b12;
                --fb-surface: #101820;
                --fb-surface-soft: #16202b;
                --fb-border: #253140;
                --fb-border-subtle: #1b2633;
                --fb-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
                --fb-shadow-soft: 0 2px 8px rgba(0, 0, 0, 0.25);
                --fb-warning-bg: #2a210f;
                --fb-warning-border: #5a4a1c;
                --fb-warning-text: #f0c75a;
                --fb-chat-bg: #101820;
                --fb-code-bg: #16202b;
                --fb-blockquote-bg: #102224;
                --fb-hero-glow: rgba(62, 207, 203, 0.08);
            }

            .stApp {
                background:
                    radial-gradient(1200px 420px at 10% -10%, var(--fb-hero-glow), transparent 55%),
                    radial-gradient(900px 360px at 100% 0%, rgba(24, 95, 165, 0.08), transparent 50%),
                    var(--fb-bg) !important;
                color: var(--fb-text);
                font-family: "IBM Plex Sans", "Noto Sans Arabic", "Noto Sans Hebrew", "Segoe UI", sans-serif;
            }

            [data-testid="stDecoration"] { display: none; }
            .block-container {
                max-width: 860px;
                padding-top: 1.35rem;
                padding-bottom: 3.5rem;
            }

            .fb-hero {
                position: relative;
                overflow: hidden;
                background: var(--fb-surface);
                border: 1px solid var(--fb-border);
                border-radius: 22px;
                padding: 1.55rem 1.7rem 1.3rem;
                box-shadow: var(--fb-shadow);
                margin-bottom: 1.15rem;
            }

            .fb-hero::before {
                content: "";
                position: absolute;
                inset: 0 auto auto 0;
                width: 100%;
                height: 3px;
                background: linear-gradient(90deg, #0a1b2e 0%, #185fa5 52%, #0f9d9a 100%);
            }

            .fb-hero-top {
                direction: ltr;
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                gap: 1rem;
            }

            .fb-brand {
                display: flex;
                align-items: center;
                gap: 0.95rem;
            }

            .fb-mark {
                width: 54px;
                height: 54px;
                border-radius: 16px;
                background:
                    linear-gradient(160deg, #0a1b2e 0%, #163a66 70%, #0f9d9a 140%);
                color: #fff;
                display: grid;
                place-items: center;
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                box-shadow: 0 8px 20px rgba(10, 27, 46, 0.28);
            }

            .fb-kicker {
                margin: 0 0 0.2rem 0;
                font-size: 0.68rem;
                font-weight: 600;
                letter-spacing: 0.14em;
                text-transform: uppercase;
                color: var(--fb-teal);
            }

            .fb-title {
                font-size: 1.85rem;
                font-weight: 700;
                color: var(--fb-ink);
                margin: 0;
                letter-spacing: -0.03em;
                line-height: 1;
            }

            .fb-status-pill {
                display: inline-flex;
                align-items: center;
                gap: 0.45rem;
                padding: 0.38rem 0.75rem;
                border-radius: 999px;
                font-size: 0.78rem;
                font-weight: 600;
                background: var(--fb-surface-soft);
                border: 1px solid var(--fb-border);
                color: var(--fb-text-secondary);
                white-space: nowrap;
            }

            .fb-status-dot {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: #94a3b8;
            }

            .fb-status-ready .fb-status-dot { background: #0f9d9a; box-shadow: 0 0 0 4px rgba(15,157,154,0.16); }
            .fb-status-done .fb-status-dot { background: #185fa5; box-shadow: 0 0 0 4px rgba(24,95,165,0.16); }

            .fb-subtitle {
                direction: rtl;
                text-align: right;
                color: var(--fb-text-secondary);
                font-size: 1.02rem;
                margin: 0.85rem 0 0 0;
                font-family: "Noto Sans Arabic", "Noto Sans Hebrew", "IBM Plex Sans", sans-serif;
            }

            .fb-steps {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 0.55rem;
                margin-top: 1.05rem;
            }

            .fb-step {
                direction: rtl;
                text-align: right;
                background: var(--fb-surface-soft);
                border: 1px solid var(--fb-border-subtle);
                border-radius: 12px;
                padding: 0.55rem 0.7rem;
                font-size: 0.8rem;
                color: var(--fb-text-secondary);
                font-weight: 500;
            }

            .fb-privacy {
                direction: rtl;
                text-align: right;
                color: var(--fb-text-muted);
                font-size: 0.82rem;
                margin: 0.9rem 0 0 0;
                padding-top: 0.75rem;
                border-top: 1px solid var(--fb-border-subtle);
                font-family: "Noto Sans Arabic", "Noto Sans Hebrew", "IBM Plex Sans", sans-serif;
            }

            .fb-panel {
                background: var(--fb-surface);
                border: 1px solid var(--fb-border);
                border-radius: 18px;
                padding: 1.15rem 1.3rem 0.35rem;
                margin-bottom: 0.85rem;
                box-shadow: var(--fb-shadow-soft);
            }

            .fb-section-title {
                direction: rtl;
                text-align: right;
                font-size: 1.05rem;
                font-weight: 700;
                color: var(--fb-ink);
                margin: 0 0 0.35rem 0;
                font-family: "Noto Sans Arabic", "Noto Sans Hebrew", "IBM Plex Sans", sans-serif;
            }

            .fb-empty {
                direction: rtl;
                text-align: right;
                background: var(--fb-surface);
                border: 1px dashed var(--fb-border);
                border-radius: 18px;
                padding: 1.35rem 1.4rem;
                margin: 0.4rem 0 1rem 0;
            }

            .fb-empty h3 {
                margin: 0 0 0.4rem 0;
                color: var(--fb-ink);
                font-size: 1.08rem;
            }

            .fb-empty p {
                margin: 0;
                color: var(--fb-text-muted);
                line-height: 1.7;
            }

            /* ── Analysis report (no boxes) ── */
            .fb-brief {
                background: var(--fb-surface);
                border: 1px solid var(--fb-border);
                border-radius: 20px;
                padding: 1.35rem 1.45rem 1.2rem;
                box-shadow: var(--fb-shadow);
                margin: 0.35rem 0 1rem 0;
            }

            .fb-report {
                direction: rtl;
                text-align: right;
                font-family: "Noto Sans Arabic", "Noto Sans Hebrew", "IBM Plex Sans", sans-serif;
                color: var(--fb-text);
                margin-top: 0.15rem;
            }

            .fb-report-he { font-family: "Noto Sans Hebrew", "Heebo", "Segoe UI", sans-serif; }
            .fb-report-ar { font-family: "Noto Sans Arabic", "Segoe UI", Tahoma, sans-serif; }

            .fb-report-meta {
                display: flex;
                flex-wrap: wrap;
                gap: 0.55rem;
                justify-content: flex-start;
                margin: 0.75rem 0 1.25rem 0;
            }

            .fb-meta-chip {
                display: inline-flex;
                align-items: center;
                gap: 0.35rem;
                padding: 0.3rem 0.75rem;
                border-radius: 999px;
                font-size: 0.82rem;
                font-weight: 600;
                background: var(--fb-surface-soft);
                border: 1px solid var(--fb-border);
                color: var(--fb-text-secondary);
            }

            .fb-meta-chip strong {
                color: var(--fb-text-muted);
                font-weight: 500;
            }

            .fb-lead {
                font-size: 1.08rem;
                line-height: 1.9;
                color: var(--fb-text);
                margin: 1rem 0 1.4rem 0;
                padding: 0.15rem 0 1.2rem 0;
                border-bottom: 1px solid var(--fb-border-subtle);
            }

            .fb-report-section {
                margin-bottom: 1.6rem;
                padding-bottom: 1.4rem;
                border-bottom: 1px solid var(--fb-border-subtle);
            }

            .fb-report-section:last-child {
                border-bottom: none;
                margin-bottom: 0;
                padding-bottom: 0;
            }

            .fb-report-heading {
                font-size: 0.74rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                color: var(--fb-teal);
                margin: 0 0 0.7rem 0;
                padding-right: 0.7rem;
                border-right: 2px solid var(--fb-teal);
            }

            .fb-report-text {
                font-size: 0.97rem;
                line-height: 1.8;
                color: var(--fb-text-secondary);
                margin: 0;
            }

            .fb-report-list {
                margin: 0;
                padding: 0 1.1rem 0 0;
                list-style: none;
            }

            .fb-report-list li {
                position: relative;
                font-size: 0.97rem;
                line-height: 1.8;
                color: var(--fb-text-secondary);
                margin-bottom: 0.5rem;
                padding-right: 0.25rem;
            }

            .fb-report-list li::before {
                content: "•";
                color: var(--fb-teal);
                font-weight: 700;
                position: absolute;
                right: -0.9rem;
            }

            .fb-report-steps {
                margin: 0;
                padding: 0;
                list-style: none;
                counter-reset: fbstep;
            }

            .fb-report-steps li {
                counter-increment: fbstep;
                position: relative;
                font-size: 0.97rem;
                line-height: 1.8;
                color: var(--fb-text-secondary);
                margin-bottom: 0.55rem;
                padding: 0.7rem 0.9rem 0.7rem 0;
                padding-right: 2.55rem;
                background: var(--fb-surface-soft);
                border-radius: 12px;
                border: 1px solid var(--fb-border-subtle);
            }

            .fb-report-steps li::before {
                content: counter(fbstep);
                position: absolute;
                right: 0.65rem;
                top: 0.55rem;
                width: 1.45rem;
                height: 1.45rem;
                border-radius: 50%;
                background: var(--fb-teal);
                color: #fff;
                font-size: 0.75rem;
                font-weight: 700;
                display: flex;
                align-items: center;
                justify-content: center;
                line-height: 1.45rem;
                text-align: center;
            }

            .fb-report-kv {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 0.65rem 1.5rem;
            }

            @media (max-width: 640px) {
                .fb-report-kv { grid-template-columns: 1fr; }
            }

            .fb-kv-item {
                display: flex;
                flex-direction: column;
                gap: 0.15rem;
            }

            .fb-kv-label {
                font-size: 0.78rem;
                font-weight: 600;
                color: var(--fb-text-muted);
            }

            .fb-kv-value {
                font-size: 0.95rem;
                color: var(--fb-text);
                line-height: 1.6;
            }

            .fb-hebrew-reply {
                direction: rtl;
                text-align: right;
                font-family: "Noto Sans Hebrew", "Heebo", sans-serif;
                font-size: 0.96rem;
                line-height: 1.85;
                color: var(--fb-text-secondary);
                background: var(--fb-code-bg);
                border-right: 3px solid var(--fb-blue);
                border-radius: 0 8px 8px 0;
                padding: 0.85rem 1rem;
                margin: 0;
                white-space: pre-wrap;
            }

            .fb-badge {
                display: inline-block;
                padding: 0.2rem 0.6rem;
                border-radius: 999px;
                font-size: 0.8rem;
                font-weight: 700;
            }

            .fb-badge-low { background: rgba(22,122,69,0.12); color: #167a45; border: 1px solid rgba(22,122,69,0.25); }
            .fb-badge-medium { background: rgba(168,106,0,0.12); color: #a86a00; border: 1px solid rgba(168,106,0,0.25); }
            .fb-badge-high { background: rgba(180,35,24,0.12); color: #b42318; border: 1px solid rgba(180,35,24,0.25); }

            .stApp[data-theme="dark"] .fb-badge-low { color: #6ee7a0; }
            .stApp[data-theme="dark"] .fb-badge-medium { color: #fbbf24; }
            .stApp[data-theme="dark"] .fb-badge-high { color: #f87171; }

            .fb-confidence-bar {
                direction: ltr;
                height: 6px;
                background: var(--fb-border);
                border-radius: 999px;
                overflow: hidden;
                margin-top: 0.35rem;
            }

            .fb-confidence-fill {
                height: 100%;
                background: linear-gradient(90deg, var(--fb-teal), var(--fb-blue));
                border-radius: 999px;
            }

            .fb-footer {
                direction: rtl;
                text-align: right;
                color: var(--fb-text-muted);
                font-size: 0.86rem;
                margin-top: 1.5rem;
                padding: 0.85rem 0;
                border-top: 1px solid var(--fb-border-subtle);
                font-family: "Noto Sans Arabic", "Noto Sans Hebrew", "Segoe UI", sans-serif;
            }

            .fb-warning {
                direction: rtl;
                text-align: right;
                background: var(--fb-warning-bg);
                border: 1px solid var(--fb-warning-border);
                color: var(--fb-warning-text);
                border-radius: 10px;
                padding: 0.75rem 1rem;
                margin-bottom: 1rem;
                font-size: 0.92rem;
                font-family: "Noto Sans Arabic", "Noto Sans Hebrew", "Segoe UI", sans-serif;
            }

            [data-testid="stFileUploader"] section {
                border: 1.5px dashed #9db4c9;
                border-radius: 16px;
                background: var(--fb-surface-soft);
                padding: 0.6rem;
            }

            [data-testid="stSelectbox"] {
                margin-bottom: 0.4rem;
            }

            .stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #0a1b2e, #185fa5) !important;
                border: none !important;
                border-radius: 12px;
                min-height: 48px;
                font-weight: 700;
                color: #fff !important;
                box-shadow: 0 8px 18px rgba(24, 95, 165, 0.22);
                transition: transform 0.15s ease, box-shadow 0.15s ease;
            }

            .stButton > button[kind="primary"]:hover {
                transform: translateY(-1px);
                box-shadow: 0 10px 22px rgba(24, 95, 165, 0.28);
            }

            .stButton > button[kind="secondary"] {
                border-radius: 12px;
                min-height: 44px;
                border-color: var(--fb-border) !important;
                color: var(--fb-text) !important;
                background: var(--fb-surface) !important;
            }

            div[data-testid="stChatMessage"] {
                border-radius: 14px;
                border: 1px solid var(--fb-border);
                background: var(--fb-chat-bg);
                box-shadow: var(--fb-shadow);
                padding: 0.35rem 0.5rem;
                margin-bottom: 0.85rem;
            }

            div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
                direction: rtl;
                text-align: right;
                unicode-bidi: plaintext;
                font-size: 1.02rem;
                line-height: 1.9;
                color: var(--fb-text);
            }

            div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {
                margin: 0 0 0.85rem 0;
            }

            div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] ul,
            div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] ol {
                direction: rtl;
                text-align: right;
                padding-right: 1.45rem;
                padding-left: 0;
            }

            div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong {
                color: var(--fb-navy);
            }

            div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h3,
            div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h4 {
                direction: rtl;
                text-align: right;
                color: var(--fb-blue);
                font-size: 1rem;
                font-weight: 700;
                border-bottom: 1px solid var(--fb-border-subtle);
                padding-bottom: 0.3rem;
            }

            div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] blockquote {
                direction: rtl;
                text-align: right;
                border-right: 3px solid var(--fb-teal);
                border-left: none;
                background: var(--fb-blockquote-bg);
                border-radius: 8px;
                padding: 0.65rem 0.9rem;
                color: var(--fb-text-secondary);
            }

            div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] pre {
                direction: rtl;
                text-align: right;
                background: var(--fb-code-bg);
                border: 1px solid var(--fb-border);
                border-radius: 10px;
                padding: 0.85rem 1rem;
                white-space: pre-wrap;
                color: var(--fb-text);
            }

            .fb-chat-ar div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
                font-family: "Noto Sans Arabic", "Segoe UI", Tahoma, sans-serif;
            }

            .fb-chat-he div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
                font-family: "Noto Sans Hebrew", "Heebo", "Segoe UI", sans-serif;
            }

            .fb-chat-panel {
                background: var(--fb-surface);
                border: 1px solid var(--fb-border);
                border-radius: 20px;
                box-shadow: var(--fb-shadow);
                padding: 1.3rem 1.35rem 0.55rem;
                margin-top: 0.85rem;
            }

            .fb-chat-agent-tag {
                direction: ltr;
                display: inline-flex;
                align-items: center;
                background: var(--fb-surface-soft);
                border: 1px solid var(--fb-border);
                color: var(--fb-navy);
                border-radius: 999px;
                padding: 0.25rem 0.7rem;
                font-size: 0.8rem;
                font-weight: 600;
                margin-bottom: 0.35rem;
            }

            .fb-chat-suggestions-title {
                direction: rtl;
                text-align: right;
                font-size: 0.86rem;
                font-weight: 600;
                color: var(--fb-text-muted);
                margin-bottom: 0.5rem;
            }

            .fb-cite {
                direction: rtl;
                text-align: right;
                border: 1px solid var(--fb-border);
                background: var(--fb-surface-soft);
                border-radius: 12px;
                padding: 0.7rem 0.85rem;
                margin: 0.45rem 0;
                font-size: 0.88rem;
            }
            .fb-cite a { direction: ltr; unicode-bidi: embed; }
            .fb-cite-badge {
                display: inline-block;
                font-size: 0.72rem;
                font-weight: 700;
                color: var(--fb-teal);
                margin-left: 0.35rem;
            }
            .fb-cite-meta { color: var(--fb-text-muted); font-size: 0.78rem; }

            .fb-chat-empty {
                direction: rtl;
                text-align: right;
                color: var(--fb-text-muted);
                font-size: 0.93rem;
                border: 1px dashed var(--fb-border);
                border-radius: 10px;
                padding: 0.8rem 1rem;
                margin-bottom: 0.85rem;
                background: var(--fb-surface-soft);
            }

            [data-testid="stChatInput"] textarea {
                direction: rtl;
                text-align: right;
                font-family: "Noto Sans Arabic", "Noto Sans Hebrew", "Segoe UI", sans-serif;
                border-radius: 12px;
                background: var(--fb-surface) !important;
                color: var(--fb-text) !important;
                border-color: var(--fb-border) !important;
            }

            [data-testid="stCaptionContainer"] {
                color: var(--fb-text-muted) !important;
            }

            [data-testid="stAlert"] {
                border-radius: 14px;
                border: 1px solid var(--fb-border);
            }

            [data-testid="stExpander"] {
                border: 1px solid var(--fb-border);
                border-radius: 14px;
                background: var(--fb-surface);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(selected_language: str, status: str = "idle") -> None:
    strings = ui(selected_language)
    status_label = {
        "ready": strings["status_ready"],
        "done": strings["status_done"],
    }.get(status, strings["status_idle"])
    status_class = f"fb-status-pill fb-status-{status}"
    st.markdown(
        f"""
        <div class="fb-hero">
            <div class="fb-hero-top">
                <div class="fb-brand">
                    <div class="fb-mark">FB</div>
                    <div>
                        <p class="fb-kicker">FormBridge Intelligence</p>
                        <p class="fb-title">FormBridge</p>
                    </div>
                </div>
                <div class="{status_class}">
                    <span class="fb-status-dot"></span>
                    {html.escape(status_label)}
                </div>
            </div>
            <p class="fb-subtitle">{html.escape(strings["subtitle"])}</p>
            <div class="fb-steps">
                <div class="fb-step">{html.escape(strings["step_upload"])}</div>
                <div class="fb-step">{html.escape(strings["step_language"])}</div>
                <div class="fb-step">{html.escape(strings["step_analyze"])}</div>
            </div>
            <p class="fb-privacy">{html.escape(strings["privacy_note"])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(selected_language: str) -> None:
    strings = ui(selected_language)
    st.markdown(
        f"""
        <div class="fb-empty">
            <h3>{html.escape(strings["empty_title"])}</h3>
            <p>{html.escape(strings["empty_body"])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _urgency_badge(level: str, strings: dict[str, str]) -> str:
    labels = {
        "low": strings["urgency_low"],
        "medium": strings["urgency_medium"],
        "high": strings["urgency_high"],
    }
    css = {"low": "fb-badge-low", "medium": "fb-badge-medium", "high": "fb-badge-high"}
    label = labels.get(level, labels["medium"])
    return f'<span class="fb-badge {css.get(level, css["medium"])}">{html.escape(label)}</span>'


def _is_missing(value: str, not_mentioned: str) -> bool:
    if not value or not value.strip():
        return True
    normalized = value.strip().lower()
    missing_phrases = {
        not_mentioned.lower(),
        "not mentioned in the document",
        "غير مذكور في المستند",
        "לא צוין במסמך",
        "n/a",
        "—",
        "-",
    }
    return normalized in missing_phrases


def _filter_items(items: list[str], not_mentioned: str) -> list[str]:
    return [item for item in items if not _is_missing(item, not_mentioned)]


def _report_section(title: str, inner_html: str) -> str:
    return (
        f'<div class="fb-report-section">'
        f'<p class="fb-report-heading">{html.escape(title)}</p>'
        f"{inner_html}"
        f"</div>"
    )


def _report_list(items: list[str]) -> str:
    items_html = "".join(f"<li>{html.escape(item)}</li>" for item in items)
    return f'<ul class="fb-report-list">{items_html}</ul>'


def _report_steps(items: list[str]) -> str:
    items_html = "".join(f"<li>{html.escape(item)}</li>" for item in items)
    return f'<ol class="fb-report-steps">{items_html}</ol>'


def _report_kv(label: str, value: str) -> str:
    return (
        f'<div class="fb-kv-item">'
        f'<span class="fb-kv-label">{html.escape(label)}</span>'
        f'<span class="fb-kv-value">{html.escape(value)}</span>'
        f"</div>"
    )


def render_analysis_dashboard(analysis: DocumentAnalysis, selected_language: str) -> None:
    strings = ui(selected_language)
    code = lang_code(selected_language)
    not_mentioned = NOT_MENTIONED_AR if code == "ar" else NOT_MENTIONED_HE

    st.markdown(
        f'<div class="fb-section-title">{html.escape(strings["analysis_title"])}</div>',
        unsafe_allow_html=True,
    )

    if analysis.ocr_warning:
        st.markdown(
            f'<div class="fb-warning"><strong>{html.escape(strings["ocr_warning_title"])}:</strong> '
            f'{html.escape(analysis.ocr_warning)}</div>',
            unsafe_allow_html=True,
        )

    meta_parts = [
        f'<span class="fb-meta-chip"><strong>{html.escape(strings["urgency"])}</strong> '
        f'{_urgency_badge(analysis.urgency_level, strings)}</span>',
        f'<span class="fb-meta-chip"><strong>{html.escape(strings["confidence"])}</strong> '
        f'{analysis.confidence_score}/100</span>',
    ]
    if not _is_missing(analysis.document_type, not_mentioned):
        meta_parts.append(
            f'<span class="fb-meta-chip"><strong>{html.escape(strings["document_type"])}</strong> '
            f'{html.escape(analysis.document_type)}</span>'
        )

    report_html = (
        f'<div class="fb-brief"><div class="fb-report fb-report-{code}">'
        f'<div class="fb-report-meta">{"".join(meta_parts)}</div>'
        f'<div class="fb-confidence-bar">'
        f'<div class="fb-confidence-fill" style="width:{analysis.confidence_score}%;"></div>'
        f"</div>"
    )

    if not _is_missing(analysis.summary, not_mentioned):
        report_html += f'<p class="fb-lead">{html.escape(analysis.summary)}</p>'

    kv_items: list[str] = []
    for label_key, value in [
        ("issuing_org", analysis.issuing_organization),
        ("recipient", analysis.recipient),
        ("why_sent", analysis.why_sent),
    ]:
        if not _is_missing(value, not_mentioned):
            kv_items.append(_report_kv(strings[label_key], value))

    if kv_items:
        overview_title = "نظرة عامة" if code == "ar" else "סקירה כללית"
        report_html += _report_section(
            overview_title,
            f'<div class="fb-report-kv">{"".join(kv_items)}</div>',
        )

    list_sections = [
        ("important_dates", analysis.important_dates),
        ("deadlines", analysis.deadlines),
        ("payments", analysis.amounts_and_payments),
        ("required_docs", analysis.required_documents),
        ("actions_required", analysis.actions_required),
        ("missing_info", analysis.missing_or_unclear),
    ]
    for key, items in list_sections:
        filtered = _filter_items(items, not_mentioned)
        if filtered:
            report_html += _report_section(strings[key], _report_list(filtered))

    plan_items = _filter_items(analysis.action_plan, not_mentioned)
    if plan_items:
        report_html += _report_section(strings["action_plan"], _report_steps(plan_items))

    reply = analysis.suggested_formal_reply_hebrew.strip()
    if reply and not _is_missing(reply, not_mentioned):
        report_html += _report_section(
            strings["suggested_reply"],
            f'<p class="fb-hebrew-reply">{html.escape(reply)}</p>',
        )

    report_html += "</div></div>"
    st.markdown(report_html, unsafe_allow_html=True)


def render_download_buttons(analysis: DocumentAnalysis, selected_language: str) -> None:
    strings = ui(selected_language)
    txt_report = build_text_report(analysis, selected_language)
    md_report = build_markdown_report(analysis, selected_language)
    col_a, col_b = st.columns(2)
    with col_a:
        st.download_button(
            strings["download_txt"],
            data=txt_report,
            file_name="formbridge_report.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with col_b:
        st.download_button(
            strings["download_md"],
            data=md_report,
            file_name="formbridge_report.md",
            mime="text/markdown",
            use_container_width=True,
        )


def build_text_report(analysis: DocumentAnalysis, selected_language: str) -> str:
    strings = ui(selected_language)
    lines = [
        "FormBridge Report",
        "=================",
        f"{strings['document_type']}: {analysis.document_type}",
        f"{strings['issuing_org']}: {analysis.issuing_organization}",
        f"{strings['recipient']}: {analysis.recipient}",
        f"{strings['summary']}: {analysis.summary}",
        f"{strings['why_sent']}: {analysis.why_sent}",
        f"{strings['urgency']}: {analysis.urgency_level}",
        "",
        strings["important_dates"],
        *[f"- {item}" for item in analysis.important_dates],
        "",
        strings["deadlines"],
        *[f"- {item}" for item in analysis.deadlines],
        "",
        strings["payments"],
        *[f"- {item}" for item in analysis.amounts_and_payments],
        "",
        strings["required_docs"],
        *[f"- {item}" for item in analysis.required_documents],
        "",
        strings["missing_info"],
        *[f"- {item}" for item in analysis.missing_or_unclear],
        "",
        strings["action_plan"],
        *[f"{index}. {item}" for index, item in enumerate(analysis.action_plan, start=1)],
        "",
        f"{strings['suggested_reply']}: {analysis.suggested_formal_reply_hebrew}",
        f"{strings['confidence']}: {analysis.confidence_score}/100",
    ]
    if analysis.ocr_warning:
        lines.extend(["", f"{strings['ocr_warning_title']}: {analysis.ocr_warning}"])
    return "\n".join(lines)


def build_markdown_report(analysis: DocumentAnalysis, selected_language: str) -> str:
    strings = ui(selected_language)
    def bullet(items: list[str]) -> str:
        if not items:
            return "- —"
        return "\n".join(f"- {item}" for item in items)

    return f"""# FormBridge Report

## {strings["summary"]}
{analysis.summary}

## {strings["document_type"]}
{analysis.document_type}

## {strings["issuing_org"]}
{analysis.issuing_organization}

## {strings["recipient"]}
{analysis.recipient}

## {strings["why_sent"]}
{analysis.why_sent}

## {strings["urgency"]}
{analysis.urgency_level}

## {strings["important_dates"]}
{bullet(analysis.important_dates)}

## {strings["deadlines"]}
{bullet(analysis.deadlines)}

## {strings["payments"]}
{bullet(analysis.amounts_and_payments)}

## {strings["required_docs"]}
{bullet(analysis.required_documents)}

## {strings["missing_info"]}
{bullet(analysis.missing_or_unclear)}

## {strings["action_plan"]}
{chr(10).join(f"{i}. {step}" for i, step in enumerate(analysis.action_plan, start=1)) or "—"}

## {strings["suggested_reply"]}
{analysis.suggested_formal_reply_hebrew or "—"}

## {strings["confidence"]}
{analysis.confidence_score}/100
"""


def render_footer(selected_language: str) -> None:
    strings = ui(selected_language)
    st.markdown(
        f'<div class="fb-footer">{html.escape(strings["footer_disclaimer"])}</div>',
        unsafe_allow_html=True,
    )


def normalize_chat_response(text: str) -> str:
    """Light cleanup so assistant answers render consistently."""
    cleaned = text.strip()
    cleaned = cleaned.replace("\r\n", "\n")
    while "\n\n\n" in cleaned:
        cleaned = cleaned.replace("\n\n\n", "\n\n")
    return cleaned


def render_citations(citations: list[dict], selected_language: str) -> None:
    strings = ui(selected_language)
    if not citations:
        st.caption(strings["no_official_source"])
        return
    st.markdown(
        f'<div class="fb-section-title" style="font-size:0.92rem;">{html.escape(strings["official_sources"])}</div>',
        unsafe_allow_html=True,
    )
    for item in citations:
        badge = (
            strings["official_sources"]
            if item.get("source_type") == "official"
            else strings["secondary_source"]
        )
        title = html.escape(item.get("title") or "")
        authority = html.escape(item.get("authority") or "")
        url = item.get("source_url") or ""
        checked = html.escape(item.get("last_checked_at") or "")
        st.markdown(
            f'<div class="fb-cite">'
            f'<span class="fb-cite-badge">{html.escape(badge)}</span> '
            f'<strong>{authority}</strong> — {title}<br>'
            f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(url)}</a><br>'
            f'<span class="fb-cite-meta">Last checked: {checked}</span>'
            f"</div>",
            unsafe_allow_html=True,
        )


def render_chat_bubble(
    content: str,
    role: str,
    selected_language: str,
    citations: list[dict] | None = None,
) -> None:
    """Render a single chat message with RTL typography and markdown support."""
    strings = ui(selected_language)
    with st.chat_message(role):
        if role == "assistant":
            st.markdown(
                f'<div class="fb-chat-agent-tag">{html.escape(strings["chat_agent_name"])} · AI Assistant</div>',
                unsafe_allow_html=True,
            )
        st.markdown(normalize_chat_response(content))
        if role == "assistant" and citations is not None:
            render_citations(citations, selected_language)
