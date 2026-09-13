"""UI strings, styling, and reusable Streamlit components."""

from __future__ import annotations

import html
from typing import Any

import streamlit as st

from models import (
    DocumentAnalysis,
    GuidedGuidance,
    NOT_MENTIONED_AR,
    NOT_MENTIONED_EN,
    NOT_MENTIONED_HE,
    humanize_guided_text,
)


LANGUAGE_AR = "العربية"
LANGUAGE_HE = "עברית פשוטה"
LANGUAGE_EN = "English"

UI_STRINGS: dict[str, dict[str, str | list[str]]] = {
    "ar": {
        "subtitle": "نفهم المستند الرسمي معك — ونحوّله إلى خطوات واضحة يمكنك الوثوق بها",
        "kicker": "ذكاء اصطناعي لفهم المستندات",
        "privacy_note": "يتم معالجة المستند فقط لأغراض التحليل ولا يُحفظ على الخادم.",
        "workspace_title": "مساحة العمل",
        "mode_upload": "رفع مستند",
        "mode_guided": "اسأل عن استمارة / وضعك",
        "mode_picker": "اختر طريقة المساعدة",
        "guided_title": "مساعدة في اختيار الاستمارة أو الخدمة",
        "guided_help": "صف وضعك أو اسأل سؤالًا. قد يطلب الوكيل تفاصيل إضافية، ثم يحدد الاستمارة ويشرح الخطوات مع رابط رسمي.",
        "guided_placeholder": "اكتب سؤالك هنا...",
        "guided_send": "إرسال",
        "guided_clear": "بدء محادثة جديدة",
        "guided_service": "الاستمارة / الخدمة",
        "guided_authority": "الجهة",
        "guided_form_number": "رقم الاستمارة",
        "guided_eligibility": "من قد يستحق",
        "guided_documents": "مستندات مطلوبة",
        "guided_steps": "خطوات واضحة",
        "guided_links": "روابط رسمية",
        "guided_questions": "أسئلة توضيحية",
        "guided_tools_used": "استخدم الوكيل أداة البحث في المصادر الرسمية",
        "guided_empty": "ابدأ بوصف وضعك. مثال: أحتاج تعبئة טופס 101 عند مشغّل جديد.",
        "guided_fields": "حقول مهمة",
        "guided_missing": "معلومات ناقصة",
        "guided_preview": "ملخص قبل التقديم (بدون إرسال تلقائي)",
        "guided_no_autosubmit": "FormBridge لا يقدّم الاستمارات تلقائيًا. راجع الملخص ثم قدّم بنفسك عبر الموقع الرسمي.",
        "guided_suggestions_title": "أسئلة مقترحة",
        "guided_example_questions": [
            "فقدت عملي — كيف أطلب دمي أبطالة؟",
            "ماذا أحتاج لتعبئة טופס 101؟",
            "كيف أغيّر عنواني في بطاقة الهوية؟",
        ],
        "consent_required": "وافق على إشعار الخصوصية قبل المتابعة.",
        "privacy_notice_title": "الخصوصية",
        "step_upload": "ارفع المستند",
        "step_language": "اختر لغة الشرح",
        "step_analyze": "حلّل واسأل",
        "guided_subtitle": "من وصف وضعك إلى استمارة واضحة، خطوات عملية، وروابط رسمية موثوقة",
        "step_describe": "صف وضعك",
        "step_clarify": "أجب عن أسئلة التوضيح",
        "step_guidance": "احصل على الاستمارة والخطوات",
        "status_idle": "بانتظار مستند",
        "status_ready": "جاهز للتحليل",
        "status_done": "تم التحليل",
        "status_guided_idle": "جاهز لمساعدتك",
        "status_guided_ready": "جارٍ التوجيه",
        "status_guided_done": "تم تحديد الخدمة",
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
        "chat_tools_used": "استخدم الوكيل أداة البحث في المصادر الرسمية",
        "chat_empty": "اسألني أي شيء عن المستند — سأجيب بناءً على محتواه فقط.",
        "rag_title": "مقاطع مسترجعة من المستند (RAG)",
        "rag_empty": "لم يُسترجع أي مقطع بعد. اسأل سؤالًا لعرض المقاطع ذات الصلة.",
        "rag_chunks": "مقاطع في قاعدة المعرفة",
        "official_sources": "مصادر رسمية",
        "secondary_source": "مصدر ثانوي",
        "no_official_source": "تعذر التحقق من إجابة رسمية موثوقة. لا تعتمد على معلومات غير مؤكدة — راجع الموقع الرسمي للجهة.",
        "last_checked": "آخر تحقق",
        "last_updated": "آخر تحديث",
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
            "ماذا أحتاج لطلب البطالة (نموذج 1500)؟",
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
        "subtitle": "אנחנו מבינים איתכם את המסמך הרשמי — והופכים אותו לצעדים ברורים שאפשר לסמוך עליהם",
        "kicker": "בינה מלאכותית להבנת מסמכים",
        "privacy_note": "המסמך מעובד לצורך ניתוח בלבד ואינו נשמר בשרת.",
        "workspace_title": "סביבת עבודה",
        "mode_upload": "העלאת מסמך",
        "mode_guided": "שאלה על טופס / מצב",
        "mode_picker": "בחרו אופן סיוע",
        "guided_title": "עזרה בבחירת טופס או שירות",
        "guided_help": "תארו את המצב או שאלו שאלה. הסוכן ישאל שאלות הבהרה במידת הצורך, יזהה טופס/שירות, וייתן שלבים עם קישור רשמי.",
        "guided_placeholder": "כתבו את השאלה כאן...",
        "guided_send": "שליחה",
        "guided_clear": "שיחה חדשה",
        "guided_service": "הטופס / השירות",
        "guided_authority": "הגורם",
        "guided_form_number": "מספר טופס",
        "guided_eligibility": "מי עשוי להיות זכאי",
        "guided_documents": "מסמכים נדרשים",
        "guided_steps": "הוראות שלב אחר שלב",
        "guided_links": "קישורים רשמיים",
        "guided_questions": "שאלות הבהרה",
        "guided_tools_used": "הסוכן השתמש בכלי חיפוש במקורות רשמיים",
        "guided_empty": "התחילו בתיאור המצב. לדוגמה: אני צריך/ה למלא טופס 101 אצל מעסיק חדש.",
        "guided_fields": "שדות חשובים",
        "guided_missing": "מידע חסר",
        "guided_preview": "תקציר לפני הגשה (ללא שליחה אוטומטית)",
        "guided_no_autosubmit": "FormBridge אינו מגיש טפסים אוטומטית. בדקו את התקציר והגישו בעצמכם באתר הרשמי.",
        "guided_suggestions_title": "שאלות מוצעות",
        "guided_example_questions": [
            "פוטרתי — איך מגישים תביעה לדמי אבטלה?",
            "מה צריך כדי למלא טופס 101?",
            "איך משנים כתובת במרשם האוכלוסין?",
        ],
        "consent_required": "יש לאשר את הודעת הפרטיות לפני המשך.",
        "privacy_notice_title": "פרטיות",
        "step_upload": "העלאת מסמך",
        "step_language": "בחירת שפה",
        "step_analyze": "ניתוח ושאלות",
        "guided_subtitle": "מתיאור המצב לטופס ברור, צעדים מעשיים וקישורים רשמיים אמינים",
        "step_describe": "תיאור המצב",
        "step_clarify": "שאלות הבהרה",
        "step_guidance": "טופס וצעדים ברורים",
        "status_idle": "ממתין למסמך",
        "status_ready": "מוכן לניתוח",
        "status_done": "הניתוח הושלם",
        "status_guided_idle": "מוכן לעזור",
        "status_guided_ready": "בתהליך הכוונה",
        "status_guided_done": "השירות זוהה",
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
        "chat_tools_used": "הסוכן השתמש בכלי חיפוש במקורות רשמיים",
        "chat_empty": "שאלו אותי כל דבר על המסמך — אענה רק על בסיס תוכנו.",
        "rag_title": "קטעים שאוחזרו מהמסמך (RAG)",
        "rag_empty": "עדיין לא אוחזרו קטעים. שאלו שאלה כדי לראות את המקורות.",
        "rag_chunks": "קטעים בבסיס הידע",
        "official_sources": "מקורות רשמיים",
        "secondary_source": "מקור משני",
        "no_official_source": "לא ניתן לאמת תשובה ממקור רשמי אמין. אין להסתמך על מידע לא מאומת — בדקו באתר הרשות.",
        "last_checked": "נבדק לאחרונה",
        "last_updated": "עודכן לאחרונה",
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
            "מה צריך לטופס 1500 דמי אבטלה?",
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
    "en": {
        "subtitle": "We read the official document with you — and turn it into clear steps you can trust",
        "kicker": "AI for understanding documents",
        "privacy_note": "The document is processed for analysis only and is not stored on the server.",
        "workspace_title": "Workspace",
        "mode_upload": "Upload document",
        "mode_guided": "Ask about a form / situation",
        "mode_picker": "Choose how to get help",
        "guided_title": "Help choosing a form or service",
        "guided_help": "Describe your situation or ask a question. The agent may ask follow-ups, identify the form/service, and give steps with an official link.",
        "guided_placeholder": "Write your question here...",
        "guided_send": "Send",
        "guided_clear": "Start new chat",
        "guided_service": "Form / service",
        "guided_authority": "Authority",
        "guided_form_number": "Form number",
        "guided_eligibility": "Who may be eligible",
        "guided_documents": "Required documents",
        "guided_steps": "Step-by-step instructions",
        "guided_links": "Official links",
        "guided_questions": "Clarifying questions",
        "guided_tools_used": "The agent used the official-sources search tool",
        "guided_empty": "Start by describing your situation. Example: I need to fill form 101 for a new employer.",
        "guided_fields": "Important fields",
        "guided_missing": "Missing information",
        "guided_preview": "Pre-submission preview (never auto-submit)",
        "guided_no_autosubmit": "FormBridge never submits forms automatically. Review the preview, then file yourself on the official site.",
        "guided_suggestions_title": "Suggested questions",
        "guided_example_questions": [
            "I lost my job — how do I apply for unemployment?",
            "What do I need to fill Form 101?",
            "How do I change my address on my ID?",
        ],
        "consent_required": "Please accept the privacy notice before continuing.",
        "privacy_notice_title": "Privacy",
        "step_upload": "Upload document",
        "step_language": "Choose language",
        "step_analyze": "Analyze and ask",
        "guided_subtitle": "From your situation to a clear form, practical steps, and trusted official links",
        "step_describe": "Describe your situation",
        "step_clarify": "Answer clarifying questions",
        "step_guidance": "Get the form and steps",
        "status_idle": "Waiting for a document",
        "status_ready": "Ready to analyze",
        "status_done": "Analysis complete",
        "status_guided_idle": "Ready to help",
        "status_guided_ready": "Guiding you",
        "status_guided_done": "Service identified",
        "empty_title": "Upload an official document to start",
        "empty_body": "FormBridge will read the text, explain what is required, and turn it into an action plan you can ask about.",
        "upload_title": "Upload document",
        "upload_help": "PDF only — up to 10 MB",
        "language_title": "Explanation language",
        "page_language_title": "Interface language",
        "analyze_button": "Analyze document",
        "analyze_again": "Re-analyze",
        "replace_document": "Replace document",
        "clear_document": "Clear document and start over",
        "file_selected": "Selected file",
        "analysis_title": "Smart summary",
        "summary": "Document summary",
        "document_type": "Document type",
        "issuing_org": "Issuing organization",
        "recipient": "Recipient / person concerned",
        "why_sent": "Why this document was sent",
        "urgency": "Urgency level",
        "important_dates": "Important dates",
        "deadlines": "Deadlines",
        "payments": "Amounts and payments",
        "required_docs": "Required documents",
        "missing_info": "Missing or unclear information",
        "actions_required": "Required actions",
        "action_plan": "Numbered action plan",
        "suggested_reply": "Suggested formal reply (Hebrew)",
        "confidence": "Confidence",
        "ocr_warning_title": "OCR warning",
        "original_text": "Extracted original text",
        "chat_title": "Questions about the document",
        "chat_placeholder": "Ask a question about the document...",
        "chat_hint": "Ask about deadlines, payments, missing documents, or request a simpler explanation.",
        "clear_chat": "Clear chat",
        "chat_agent_name": "FormBridge",
        "chat_suggestions_title": "Suggested questions",
        "chat_tools_used": "The agent used the official-sources search tool",
        "chat_empty": "Ask me anything about the document — I will answer based on its content only.",
        "rag_title": "Retrieved document passages (RAG)",
        "rag_empty": "No passages retrieved yet. Ask a question to see related sources.",
        "rag_chunks": "Chunks in the knowledge base",
        "official_sources": "Official sources",
        "secondary_source": "Secondary source",
        "no_official_source": "Could not verify a reliable official answer. Do not rely on unverified details — check the authority website.",
        "last_checked": "Last checked",
        "last_updated": "Last updated",
        "form_identity": "Form identification",
        "download_txt": "Download report (TXT)",
        "download_md": "Download report (Markdown)",
        "footer_disclaimer": (
            "FormBridge provides AI-generated explanations and is not a substitute "
            "for legal, tax, medical, or government advice. "
            "This project is not affiliated with the Israeli government. Always verify on the official source."
        ),
        "urgency_low": "Low",
        "urgency_medium": "Medium",
        "urgency_high": "High",
        "language_mismatch": "Explanation language changed. Click “Re-analyze” to see results in the new language.",
        "no_analysis_yet": "Upload a document and click “Analyze document” to start.",
        "processing": "FormBridge is reading and analyzing the document...",
        "chat_processing": "Preparing an answer...",
        "truncated_note": "The document was shortened because it is very long. The analysis may not include every detail.",
        "example_questions": [
            "What do I need for unemployment form 1500?",
            "What should I do?",
            "What is the deadline?",
            "Explain this section more simply",
            "What documents are missing?",
            "How much do I need to pay?",
            "Write a formal reply in Hebrew",
            "Translate this section into Arabic",
            "What happens if I do not respond?",
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
        "api_denied": (
            "تم رفض الوصول إلى Gemini (403). أنشئ مفتاح API جديدًا من Google AI Studio "
            "وتأكد أن Generative Language API مفعّل، ثم ضعه في ملف .env."
        ),
        "api_quota": (
            "تم تجاوز حصة Gemini المجانية حالياً (429). انتظر حتى تتجدد الحصة اليومية، "
            "أو أنشئ مشروعًا/مفتاح API جديدًا في Google AI Studio، أو فعّل الفوترة."
        ),
        "api_model_missing": (
            "نموذج Gemini غير متاح لهذا المفتاح (404). ضع في .env: "
            "GEMINI_MODEL=gemini/gemini-3.6-flash ثم أعد تشغيل التطبيق."
        ),
        "api_groq_model_missing": (
            "نموذج Groq غير متاح لهذا المفتاح. ضع في .env مثلًا: "
            "GROQ_MODEL=groq/openai/gpt-oss-20b ثم أعد تشغيل التطبيق."
        ),
        "api_groq_quota": (
            "تم تجاوز حد طلبات Groq (TPM). انتظر حوالي 20 ثانية ثم أعد المحاولة."
        ),
        "api_groq_denied": (
            "تم رفض الوصول إلى Groq. تحقق من GROQ_API_KEY في ملف .env."
        ),
        "api_groq_key_missing": "مفتاح GROQ_API_KEY غير موجود في ملف .env.",
        "api_groq_tools": "فشل Groq في استدعاء أداة البحث. أعد المحاولة، أو اختصر السؤال.",
        "generic": "حدث خطأ أثناء المعالجة. يرجى المحاولة مرة أخرى.",
        "file_too_large": "حجم الملف كبير جدًا. الحد الأقصى 10 ميغابايت.",
        "source_unreachable": "تعذر الوصول إلى مصدر حكومي أو واجهة النموذج. حاول لاحقًا أو راجع الموقع الرسمي مباشرة.",
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
        "api_denied": (
            "הגישה ל-Gemini נדחתה (403). צרו מפתח API חדש ב-Google AI Studio, "
            "ודאו ש-Generative Language API מופעל, והדביקו אותו בקובץ .env."
        ),
        "api_quota": (
            "חריגה ממכסת Gemini החינמית (429). המתינו לחידוש המכסה היומית, "
            "או צרו פרויקט/מפתח API חדש ב-Google AI Studio, או הפעילו חיוב."
        ),
        "api_model_missing": (
            "מודל Gemini אינו זמין למפתח זה (404). הגדירו ב-.env: "
            "GEMINI_MODEL=gemini/gemini-3.6-flash והפעילו מחדש את האפליקציה."
        ),
        "api_groq_model_missing": (
            "מודל Groq אינו זמין למפתח זה. הגדירו ב-.env לדוגמה: "
            "GROQ_MODEL=groq/openai/gpt-oss-20b והפעילו מחדש את האפליקציה."
        ),
        "api_groq_quota": "חריגה ממכסת Groq (TPM). המתינו כ-20 שניות ונסו שוב.",
        "api_groq_denied": "הגישה ל-Groq נדחתה. בדקו את GROQ_API_KEY בקובץ .env.",
        "api_groq_key_missing": "מפתח GROQ_API_KEY לא נמצא בקובץ .env.",
        "api_groq_tools": "Groq נכשל בקריאת כלי החיפוש. נסו שוב, או קצרו את השאלה.",
        "generic": "אירעה שגיאה בעיבוד. נסו שוב.",
        "file_too_large": "גודל הקובץ גדול מדי. המקסימום הוא 10MB.",
        "source_unreachable": "לא ניתן להגיע למקור ממשלתי או לממשק המודל. נסו שוב מאוחר יותר או בדקו באתר הרשמי.",
    },
    "en": {
        "no_file": "Please upload a PDF before analysis.",
        "invalid_type": "Unsupported file type. Please upload a PDF.",
        "empty_pdf": "We could not read text from the document.",
        "password_pdf": "The document is password-protected. Upload an unprotected copy.",
        "corrupted_pdf": "The PDF looks corrupted or invalid.",
        "ocr_missing": "OCR is unavailable. Please install Tesseract OCR.",
        "ocr_lang_missing": "OCR language files are missing from the tessdata folder.",
        "api_key_missing": "GEMINI_API_KEY was not found in the .env file.",
        "api_denied": (
            "Gemini access was denied (403). Create a new API key in Google AI Studio, "
            "enable the Generative Language API, and put the key in your .env file."
        ),
        "api_quota": (
            "Gemini free-tier quota exceeded (429). Wait for the daily quota to reset, "
            "create a new API key/project in Google AI Studio, or enable billing."
        ),
        "api_model_missing": (
            "This Gemini model is not available for your key (404). Set in .env: "
            "GEMINI_MODEL=gemini/gemini-3.6-flash and restart the app."
        ),
        "api_groq_model_missing": (
            "This Groq model is not available for your key. Set in .env e.g. "
            "GROQ_MODEL=groq/openai/gpt-oss-20b and restart the app."
        ),
        "api_groq_quota": "Groq rate limit (TPM) reached. Wait about 20 seconds and try again.",
        "api_groq_denied": "Groq access was denied. Check GROQ_API_KEY in your .env file.",
        "api_groq_key_missing": "GROQ_API_KEY was not found in the .env file.",
        "api_groq_tools": "Groq failed to call a search tool. Try again, or shorten the question.",
        "generic": "Something went wrong while processing. Please try again.",
        "file_too_large": "The file is too large. Maximum size is 10 MB.",
        "source_unreachable": "A government source or model API could not be reached. Try again later or check the official website.",
    },
}


def lang_code(selected_language: str) -> str:
    if selected_language == LANGUAGE_AR:
        return "ar"
    if selected_language == LANGUAGE_EN:
        return "en"
    return "he"


PRODUCT_COPY: dict[str, dict[str, str]] = {
    "ar": {
        "landing_kicker": "مساعد حكومي موثوق",
        "landing_title": "افهم الاستمارة الرسمية — ثم تصرّف بثقة",
        "landing_lead": "FormBridge يوجّهك من وصف وضعك إلى الاستمارة الصحيحة، المستندات، والخطوات، مع مصادر إسرائيلية رسمية فقط.",
        "landing_how": "كيف يعمل",
        "feat_flow": "حوار موجّه: أسئلة توضيح، تحديد الاستمارة، أهلية، وخطوات.",
        "feat_kb": "معرفة رسمية من gov.il، التأمين الوطني، الضرائب، السكان، العمل والصحة.",
        "feat_rag": "استرجاع مُستند إلى الأدلة مع اقتباسات قابلة للنقر.",
        "feat_safe": "لا إرسال تلقائي. تنبيه واضح إن لم يُعثر على مصدر موثوق.",
        "auth_title": "حسابك",
        "auth_login": "تسجيل الدخول",
        "auth_register": "إنشاء حساب",
        "auth_guest": "متابعة كضيف",
        "auth_email": "البريد الإلكتروني",
        "auth_password": "كلمة المرور",
        "auth_password_hint": "8 أحرف على الأقل",
        "auth_name": "الاسم",
        "auth_logout": "تسجيل الخروج",
        "auth_error_exists": "هذا البريد مسجّل مسبقاً. سجّل الدخول أو أعد تعيين كلمة المرور.",
        "auth_error_invalid": "البريد أو كلمة المرور غير صحيحة.",
        "auth_error_email": "صيغة البريد الإلكتروني غير صحيحة.",
        "auth_error_weak": "كلمة المرور قصيرة جداً. استخدم 8 أحرف على الأقل.",
        "auth_error_mismatch": "كلمتا المرور غير متطابقتين.",
        "auth_confirm": "تأكيد كلمة المرور",
        "auth_welcome_sent": "تم إنشاء الحساب. يمكنك البدء الآن.",
        "auth_have_account": "لديك حساب؟ سجّل الدخول",
        "auth_need_account": "حساب جديد",
        "auth_login_lead": "أدخل بريدك وكلمة المرور للمتابعة.",
        "auth_signup_lead": "أنشئ حساباً لحفظ محادثاتك واستعادة الوصول لاحقاً.",
        "auth_change_password": "تغيير كلمة المرور",
        "auth_current_password": "كلمة المرور الحالية",
        "auth_change_save": "حفظ كلمة المرور الجديدة",
        "auth_change_done": "تم تحديث كلمة المرور.",
        "auth_change_bad": "كلمة المرور الحالية غير صحيحة.",
        "new_chat": "محادثة جديدة",
        "recent_chats": "محادثاتك",
        "delete_chat": "حذف",
        "validator_title": "التحقق من الحقول",
        "validator_help": "تحقق من رقم هوية، بريد، هاتف أو تاريخ قبل التعبئة الرسمية.",
        "validator_run": "تحقق",
        "account_guest": "ضيف",
    },
    "he": {
        "landing_kicker": "סיוע ממשלתי אמין",
        "landing_title": "להבין את הטופס — ולפעול בביטחון",
        "landing_lead": "FormBridge מוביל מתיאור המצב לטופס הנכון, למסמכים ולשלבים — רק ממקורות רשמיים בישראל.",
        "landing_how": "איך זה עובד",
        "feat_flow": "שיחה מודרכת: שאלות הבהרה, זיהוי טופס, זכאות ושלבים.",
        "feat_kb": "ידע רשמי מ-gov.il, ביטוח לאומי, מסים, אוכלוסין, עבודה ובריאות.",
        "feat_rag": "שליפה מבוססת ראיות עם ציטוטים ללחיצה.",
        "feat_safe": "בלי הגשה אוטומטית. אזהרה ברורה כשאין מקור אמין.",
        "auth_title": "החשבון שלך",
        "auth_login": "כניסה",
        "auth_register": "הרשמה",
        "auth_guest": "המשך כאורח/ת",
        "auth_email": "אימייל",
        "auth_password": "סיסמה",
        "auth_password_hint": "לפחות 8 תווים",
        "auth_name": "שם",
        "auth_logout": "התנתקות",
        "auth_error_exists": "האימייל כבר רשום. התחברו או אפסו סיסמה.",
        "auth_error_invalid": "אימייל או סיסמה שגויים.",
        "auth_error_email": "כתובת האימייל אינה תקינה.",
        "auth_error_weak": "הסיסמה קצרה מדי. צריך לפחות 8 תווים.",
        "auth_error_mismatch": "הסיסמאות אינן תואמות.",
        "auth_confirm": "אימות סיסמה",
        "auth_welcome_sent": "החשבון נוצר. אפשר להתחיל.",
        "auth_have_account": "יש לכם חשבון? התחברו",
        "auth_need_account": "חשבון חדש",
        "auth_login_lead": "הזינו אימייל וסיסמה כדי להמשיך.",
        "auth_signup_lead": "צרו חשבון כדי לשמור שיחות ולחזור אליהן אחר כך.",
        "auth_change_password": "שינוי סיסמה",
        "auth_current_password": "סיסמה נוכחית",
        "auth_change_save": "שמירת הסיסמה החדשה",
        "auth_change_done": "הסיסמה עודכנה.",
        "auth_change_bad": "הסיסמה הנוכחית שגויה.",
        "new_chat": "שיחה חדשה",
        "recent_chats": "השיחות שלך",
        "delete_chat": "מחיקה",
        "validator_title": "בדיקת שדות",
        "validator_help": "בדקו ת.ז., אימייל, טלפון או תאריך לפני מילוי באתר הרשמי.",
        "validator_run": "בדיקה",
        "account_guest": "אורח/ת",
    },
    "en": {
        "landing_kicker": "Trusted government guidance",
        "landing_title": "Understand the official form — then act with confidence",
        "landing_lead": "FormBridge takes you from a situation to the right Israeli form, documents, and steps — grounded only in official sources.",
        "landing_how": "How it works",
        "feat_flow": "Guided dialogue: clarifying questions, form ID, eligibility, and steps.",
        "feat_kb": "Official knowledge from gov.il, Bituach Leumi, Tax, PIBA, Labor, and Health.",
        "feat_rag": "Evidence-first retrieval with clickable citations.",
        "feat_safe": "No auto-submit. A clear warning when no reliable source is found.",
        "auth_title": "Your account",
        "auth_login": "Sign in",
        "auth_register": "Create account",
        "auth_guest": "Continue as guest",
        "auth_email": "Email",
        "auth_password": "Password",
        "auth_password_hint": "At least 8 characters",
        "auth_name": "Name",
        "auth_logout": "Sign out",
        "auth_error_exists": "This email is already registered. Sign in or reset your password.",
        "auth_error_invalid": "Email or password is incorrect.",
        "auth_error_email": "That email address is not valid.",
        "auth_error_weak": "Password is too short. Use at least 8 characters.",
        "auth_error_mismatch": "The passwords do not match.",
        "auth_confirm": "Confirm password",
        "auth_welcome_sent": "Account created. You can start now.",
        "auth_have_account": "Already have an account? Sign in",
        "auth_need_account": "Create an account",
        "auth_login_lead": "Enter your email and password to continue.",
        "auth_signup_lead": "Create an account to keep your conversations and come back later.",
        "auth_change_password": "Change password",
        "auth_current_password": "Current password",
        "auth_change_save": "Save new password",
        "auth_change_done": "Password updated.",
        "auth_change_bad": "Current password is incorrect.",
        "new_chat": "New conversation",
        "recent_chats": "Your conversations",
        "delete_chat": "Delete",
        "validator_title": "Field checks",
        "validator_help": "Validate an Israeli ID, email, phone, or date before filing on the official site.",
        "validator_run": "Validate",
        "account_guest": "Guest",
    },
}


def ui(selected_language: str) -> dict[str, Any]:
    code = lang_code(selected_language)
    return {**UI_STRINGS[code], **PRODUCT_COPY.get(code, {})}


def errors(selected_language: str) -> dict[str, str]:
    return ERROR_MESSAGES[lang_code(selected_language)]


def rtl_block(content: str, *, extra_class: str = "") -> str:
    safe = html.escape(content).replace("\n", "<br>")
    class_attr = f"rtl-text {extra_class}".strip()
    return f'<div class="{class_attr}">{safe}</div>'


def inject_global_css(selected_language: str | None = None) -> None:
    page_dir = "ltr" if selected_language == LANGUAGE_EN else "rtl"
    page_align = "left" if page_dir == "ltr" else "right"
    language_dir = f"""
            /* Never apply RTL to Streamlit's outer flex layout or sidebar shell.
               Doing so breaks the collapsed-sidebar width calculation. */
            .stApp,
            [data-testid="stAppViewContainer"],
            [data-testid="stSidebar"] {{
                direction: ltr !important;
            }}
            [data-testid="stAppViewContainer"] > .main,
            .block-container,
            [data-testid="stSidebarContent"] {{
                direction: {page_dir} !important;
            }}
            .fb-topbar, .fb-deck, .fb-panel, .fb-section-title, .fb-chat-panel,
            .fb-empty, .fb-subtitle, .fb-privacy, .fb-mode-label, .fb-masthead,
            .fb-identity-card, footer.fb-footer {{
                direction: {page_dir} !important;
                text-align: {page_align} !important;
            }}
            .fb-topbar-aside {{
                text-align: {page_align} !important;
            }}
            [data-testid="stChatInput"] textarea {{
                direction: auto !important;
                text-align: start !important;
                unicode-bidi: plaintext !important;
            }}
    """
    st.markdown(
        f"""
        <style>
            /* Hide Streamlit auto page list — FormBridge uses custom page_link nav. */
            [data-testid="stSidebarNav"],
            section[data-testid="stSidebarNav"],
            div[data-testid="stSidebarNavItems"],
            ul[data-testid="stSidebarNavItems"] {{
                display: none !important;
            }}

            @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Noto+Sans+Arabic:wght@400;500;600;700;800&family=Noto+Sans+Hebrew:wght@400;500;600;700;800&display=swap');

            :root {{
                --fb-navy: #141414;
                --fb-blue: #1F4E46;
                --fb-teal: #1F4E46;
                --fb-accent: #9A3412;
                --fb-ink: #141414;
                --fb-text: #141414;
                --fb-text-secondary: #4A453C;
                --fb-text-muted: #7A7468;
                --fb-bg: #F4F1EA;
                --fb-surface: #ffffff;
                --fb-surface-soft: #F8F6F1;
                --fb-border: #D9D4C8;
                --fb-border-subtle: #E8E4D9;
                --fb-shadow: none;
                --fb-shadow-soft: none;
                --fb-warning-bg: #F8EFE2;
                --fb-warning-border: #E4D2B8;
                --fb-warning-text: #6B3F12;
                --fb-chat-bg: #ffffff;
                --fb-code-bg: #F1EDE3;
                --fb-blockquote-bg: #F3EEE4;
                --fb-hero-glow: transparent;
                --fb-radius: 6px;
                --fb-radius-sm: 4px;
            }}
{language_dir}
        </style>
        """,
        unsafe_allow_html=True,
    )
    # Keep the large existing stylesheet too (theme + components).
    st.markdown(
        """
        <style>
            .stApp[data-theme="dark"],
            [data-theme="dark"] .stApp {
                --fb-navy: #e8f1fb;
                --fb-blue: #7dd3fc;
                --fb-teal: #5eead4;
                --fb-accent: #2dd4bf;
                --fb-ink: #e8f1fb;
                --fb-text: #e8eef6;
                --fb-text-secondary: #c2cedc;
                --fb-text-muted: #8fa0b3;
                --fb-bg: #050a12;
                --fb-surface: #0d1520;
                --fb-surface-soft: #14202e;
                --fb-border: #243447;
                --fb-border-subtle: #1a2736;
                --fb-shadow: 0 16px 48px rgba(0, 0, 0, 0.45);
                --fb-shadow-soft: 0 4px 16px rgba(0, 0, 0, 0.3);
                --fb-warning-bg: #2a210f;
                --fb-warning-border: #5a4a1c;
                --fb-warning-text: #f0c75a;
                --fb-chat-bg: #0d1520;
                --fb-code-bg: #14202e;
                --fb-blockquote-bg: #102422;
                --fb-hero-glow: rgba(45, 212, 191, 0.1);
            }

            .stApp {
                background:
                    radial-gradient(980px 460px at 0% -5%, rgba(15, 118, 110, 0.18), transparent 55%),
                    radial-gradient(820px 420px at 100% 0%, rgba(21, 94, 117, 0.16), transparent 50%),
                    linear-gradient(165deg, #f5f8fc 0%, #e9eef5 42%, #e3eaf3 100%) !important;
                color: var(--fb-text);
                font-family: "IBM Plex Sans", "Noto Sans Arabic", "Noto Sans Hebrew", sans-serif;
            }

            .stApp::before {
                content: "";
                position: fixed;
                inset: 0;
                pointer-events: none;
                opacity: 0.035;
                background-image:
                    linear-gradient(rgba(7,21,37,0.55) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(7,21,37,0.55) 1px, transparent 1px);
                background-size: 48px 48px;
                z-index: 0;
            }

            [data-testid="stDecoration"] { display: none; }
            header[data-testid="stHeader"] {
                background: transparent !important;
            }
            [data-testid="stToolbar"] {
                right: 1rem !important;
            }
            .block-container {
                max-width: 980px;
                padding-top: 0.85rem;
                padding-bottom: 4.5rem;
                position: relative;
                z-index: 1;
            }

            .fb-hero {
                position: relative;
                overflow: hidden;
                background:
                    linear-gradient(135deg, #071525 0%, #0c2740 48%, #0f4c5c 100%);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 32px;
                padding: 2rem 2rem 1.55rem;
                box-shadow: 0 30px 70px rgba(7, 21, 37, 0.28);
                margin-bottom: 1.15rem;
                color: #f4faf9;
                animation: fb-rise 0.55s cubic-bezier(0.22, 1, 0.36, 1);
            }

            @keyframes fb-rise {
                from { opacity: 0; transform: translateY(14px) scale(0.985); }
                to { opacity: 1; transform: translateY(0) scale(1); }
            }

            .fb-hero::before {
                content: "";
                position: absolute;
                inset: 0;
                background:
                    radial-gradient(520px 240px at 88% 18%, rgba(20,184,166,0.28), transparent 60%),
                    radial-gradient(420px 200px at 12% 90%, rgba(56,189,248,0.12), transparent 65%);
                pointer-events: none;
            }

            .fb-hero::after {
                content: "";
                position: absolute;
                width: 280px;
                height: 280px;
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 50%;
                right: -90px;
                top: -110px;
                pointer-events: none;
            }

            .fb-hero-top {
                direction: ltr;
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                gap: 1rem;
                position: relative;
                z-index: 1;
            }

            .fb-brand {
                display: flex;
                align-items: center;
                gap: 1.05rem;
            }

            .fb-mark {
                width: 64px;
                height: 64px;
                border-radius: 20px;
                background:
                    linear-gradient(145deg, rgba(255,255,255,0.18), rgba(255,255,255,0.04));
                border: 1px solid rgba(255,255,255,0.22);
                color: #fff;
                display: grid;
                place-items: center;
                font-family: "Outfit", "IBM Plex Sans", sans-serif;
                font-size: 0.92rem;
                font-weight: 800;
                letter-spacing: 0.08em;
                box-shadow: 0 12px 28px rgba(0,0,0,0.25);
                backdrop-filter: blur(8px);
            }

            .fb-kicker {
                margin: 0 0 0.28rem 0;
                font-family: "Outfit", "IBM Plex Sans", sans-serif;
                font-size: 0.72rem;
                font-weight: 600;
                letter-spacing: 0.2em;
                text-transform: uppercase;
                color: #5eead4;
            }

            .fb-title {
                font-family: "Outfit", "IBM Plex Sans", sans-serif;
                font-size: 2.35rem;
                font-weight: 800;
                color: #ffffff;
                margin: 0;
                letter-spacing: -0.04em;
                line-height: 0.95;
            }

            .fb-status-pill {
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.5rem 0.95rem;
                border-radius: 999px;
                font-size: 0.8rem;
                font-weight: 600;
                background: rgba(255,255,255,0.1);
                border: 1px solid rgba(255,255,255,0.18);
                color: rgba(255,255,255,0.92);
                white-space: nowrap;
                backdrop-filter: blur(10px);
            }

            .fb-status-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #94a3b8;
            }

            .fb-status-ready .fb-status-dot { background: #5eead4; box-shadow: 0 0 0 4px rgba(94,234,212,0.22); }
            .fb-status-done .fb-status-dot { background: #7dd3fc; box-shadow: 0 0 0 4px rgba(125,211,252,0.22); }
            .fb-status-idle .fb-status-dot { background: #cbd5e1; }

            .fb-subtitle {
                direction: rtl;
                text-align: right;
                color: rgba(236, 253, 245, 0.9);
                font-size: 1.12rem;
                margin: 1.15rem 0 0 0;
                line-height: 1.55;
                font-family: "Noto Sans Arabic", "Noto Sans Hebrew", "IBM Plex Sans", sans-serif;
                position: relative;
                z-index: 1;
                max-width: 36rem;
                margin-right: 0;
                margin-left: auto;
            }

            .fb-steps {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 0.75rem;
                margin-top: 1.35rem;
                position: relative;
                z-index: 1;
                direction: rtl;
            }

            .fb-step {
                direction: rtl;
                text-align: right;
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 18px;
                padding: 0.9rem 0.95rem;
                font-size: 0.88rem;
                color: rgba(255,255,255,0.9);
                font-weight: 500;
                line-height: 1.45;
                backdrop-filter: blur(8px);
                transition: transform 0.2s ease, background 0.2s ease;
            }

            .fb-step:hover {
                background: rgba(255,255,255,0.14);
                transform: translateY(-2px);
            }

            .fb-step-num {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 1.45rem;
                height: 1.45rem;
                border-radius: 50%;
                background: #14b8a6;
                color: #042f2e;
                font-family: "Outfit", sans-serif;
                font-size: 0.72rem;
                font-weight: 800;
                margin-left: 0.45rem;
                vertical-align: middle;
            }

            .fb-privacy {
                direction: rtl;
                text-align: right;
                color: rgba(226, 232, 240, 0.72);
                font-size: 0.8rem;
                margin: 1.15rem 0 0 0;
                padding-top: 0.95rem;
                border-top: 1px solid rgba(255,255,255,0.12);
                font-family: "Noto Sans Arabic", "Noto Sans Hebrew", "IBM Plex Sans", sans-serif;
                position: relative;
                z-index: 1;
            }

            .fb-panel {
                background: rgba(255,255,255,0.92);
                border: 1px solid var(--fb-border);
                border-radius: var(--fb-radius);
                padding: 1.4rem 1.5rem 0.7rem;
                margin-bottom: 1rem;
                box-shadow: var(--fb-shadow-soft);
                backdrop-filter: blur(10px);
                animation: fb-rise 0.45s ease-out;
            }

            .fb-section-title {
                direction: rtl;
                text-align: right;
                font-family: "Outfit", "Noto Sans Arabic", "Noto Sans Hebrew", sans-serif;
                font-size: 1.2rem;
                font-weight: 700;
                color: var(--fb-ink);
                margin: 0 0 0.45rem 0;
                letter-spacing: -0.02em;
            }

            .fb-mode-label {
                direction: rtl;
                text-align: right;
                font-size: 0.8rem;
                font-weight: 700;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                color: var(--fb-text-muted);
                margin: 0.2rem 0 0.45rem 0;
            }

            .fb-guided-details {
                margin-top: 0.55rem;
            }
            .fb-identity-grid {
                direction: rtl;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
                gap: 0.8rem;
                margin: 0.55rem 0 0.85rem 0;
            }

            .fb-identity-card {
                background: linear-gradient(180deg, #ffffff 0%, #f3f8f7 100%);
                border: 1px solid var(--fb-border-subtle);
                border-radius: 18px;
                padding: 1rem 1.05rem;
                box-shadow: var(--fb-shadow-soft);
            }

            .fb-identity-label {
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.05em;
                color: var(--fb-teal);
                margin: 0 0 0.4rem 0;
                text-transform: uppercase;
            }

            .fb-identity-value {
                font-size: 1rem;
                font-weight: 700;
                color: var(--fb-ink);
                line-height: 1.45;
                margin: 0;
            }

            @media (max-width: 700px) {
                .fb-steps { grid-template-columns: 1fr; }
                .fb-identity-grid { grid-template-columns: 1fr; }
                .fb-title { font-size: 1.85rem; }
                .fb-hero { padding: 1.5rem 1.25rem 1.25rem; border-radius: 24px; }
            }

            .fb-empty {
                direction: rtl;
                text-align: right;
                background:
                    linear-gradient(160deg, rgba(255,255,255,0.95), rgba(243,247,251,0.92));
                border: 1px solid var(--fb-border);
                border-radius: var(--fb-radius);
                padding: 1.8rem 1.7rem;
                margin: 0.5rem 0 1.1rem 0;
                box-shadow: var(--fb-shadow-soft);
                position: relative;
                overflow: hidden;
            }

            .fb-empty::before {
                content: "";
                position: absolute;
                width: 140px;
                height: 140px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(15,118,110,0.12), transparent 70%);
                left: -30px;
                bottom: -40px;
            }

            .fb-empty h3 {
                margin: 0 0 0.5rem 0;
                color: var(--fb-ink);
                font-family: "Outfit", "Noto Sans Arabic", sans-serif;
                font-size: 1.25rem;
                position: relative;
            }

            .fb-empty p {
                margin: 0;
                color: var(--fb-text-muted);
                line-height: 1.8;
                position: relative;
                font-size: 0.98rem;
            }

            .fb-bridge-line {
                display: block;
                width: 72px;
                height: 4px;
                border-radius: 999px;
                background: linear-gradient(90deg, #14b8a6, #38bdf8);
                margin: 0.85rem 0 0 auto;
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
                padding: 0.75rem;
                transition: border-color 0.2s ease, background 0.2s ease;
            }

            [data-testid="stFileUploader"] section:hover {
                border-color: var(--fb-teal);
                background: #f0faf9;
            }

            [data-testid="stSelectbox"] {
                margin-bottom: 0.4rem;
            }

            /* Mode segmented control */
            div[data-testid="stRadio"] > div {
                gap: 0.4rem !important;
                background: rgba(255,255,255,0.9) !important;
                border: 1px solid var(--fb-border) !important;
                border-radius: 18px !important;
                padding: 0.4rem !important;
                box-shadow: var(--fb-shadow) !important;
                margin-bottom: 1rem !important;
            }

            div[data-testid="stRadio"] label {
                border-radius: 14px !important;
                padding: 0.75rem 1.05rem !important;
                font-weight: 700 !important;
                font-size: 0.95rem !important;
                transition: all 0.18s ease !important;
                border: 1px solid transparent !important;
            }

            div[data-testid="stRadio"] label:hover {
                background: rgba(15, 118, 110, 0.08) !important;
            }

            div[data-testid="stRadio"] label[data-checked="true"],
            div[data-testid="stRadio"] label:has(input:checked) {
                background: linear-gradient(135deg, #071525, #0f766e) !important;
                color: #fff !important;
                box-shadow: 0 10px 22px rgba(15, 118, 110, 0.25) !important;
            }

            .stButton > button[kind="primary"] {
                background: #0f766e !important;
                border: 1px solid #0d5f59 !important;
                border-radius: 10px !important;
                min-height: 42px;
                font-weight: 650;
                font-size: 0.95rem !important;
                color: #fff !important;
                box-shadow: none;
                letter-spacing: 0.01em;
            }

            .stButton > button[kind="primary"]:hover {
                background: #0d5f59 !important;
            }

            .stButton > button[kind="secondary"],
            .stButton > button {
                border-radius: 10px !important;
                min-height: 40px;
                font-weight: 600 !important;
            }

            div[data-testid="stChatMessage"] {
                border-radius: 18px;
                border: 1px solid var(--fb-border);
                background: rgba(255,255,255,0.94);
                box-shadow: var(--fb-shadow-soft);
                padding: 0.45rem 0.65rem;
                margin-bottom: 0.95rem;
            }

            [data-testid="stChatInput"] {
                background: transparent !important;
            }

            [data-testid="stChatInput"] textarea {
                direction: auto;
                text-align: start;
                unicode-bidi: plaintext;
                font-family: "Noto Sans Arabic", "Noto Sans Hebrew", "IBM Plex Sans", sans-serif;
                border-radius: 18px !important;
                background: rgba(255,255,255,0.96) !important;
                color: var(--fb-text) !important;
                border: 1px solid var(--fb-border) !important;
                box-shadow: var(--fb-shadow-soft) !important;
                min-height: 56px !important;
            }

            [data-testid="stAlert"] {
                border-radius: 18px !important;
                border: 1px solid var(--fb-border) !important;
                box-shadow: var(--fb-shadow-soft);
            }

            [data-testid="stFileUploader"] section {
                border: 2px dashed #9db8c9 !important;
                border-radius: 20px !important;
                background: linear-gradient(180deg, #ffffff, #f3f8fb) !important;
                padding: 1.1rem !important;
                transition: border-color 0.2s ease, box-shadow 0.2s ease;
            }

            [data-testid="stFileUploader"] section:hover {
                border-color: #0f766e !important;
                box-shadow: 0 12px 28px rgba(15, 118, 110, 0.12);
            }

            .fb-footer {
                direction: rtl;
                text-align: right;
                color: var(--fb-text-muted);
                font-size: 0.86rem;
                margin-top: 1.8rem;
                padding: 1.1rem 0 0.4rem;
                border-top: 1px solid var(--fb-border-subtle);
                font-family: "Noto Sans Arabic", "Noto Sans Hebrew", "IBM Plex Sans", sans-serif;
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
                background: linear-gradient(180deg, #fff 0%, var(--fb-surface-soft) 100%);
                border-radius: 14px;
                padding: 0.85rem 1rem;
                margin: 0.5rem 0;
                font-size: 0.88rem;
                box-shadow: var(--fb-shadow-soft);
            }
            .fb-cite a {
                direction: ltr;
                unicode-bidi: embed;
                color: var(--fb-blue);
                text-decoration: none;
                font-weight: 500;
                word-break: break-all;
            }
            .fb-cite a:hover { text-decoration: underline; }
            .fb-cite-badge {
                display: inline-block;
                font-size: 0.7rem;
                font-weight: 700;
                color: #fff;
                background: var(--fb-teal);
                border-radius: 999px;
                padding: 0.12rem 0.5rem;
                margin-left: 0.4rem;
            }
            .fb-cite-meta { color: var(--fb-text-muted); font-size: 0.78rem; }

            .fb-chat-empty {
                direction: auto;
                text-align: start;
                unicode-bidi: plaintext;
                color: var(--fb-text-muted);
                font-size: 0.93rem;
                border: 1px dashed var(--fb-border);
                border-radius: 10px;
                padding: 0.8rem 1rem;
                margin-bottom: 0.85rem;
                background: var(--fb-surface-soft);
            }

            [data-testid="stChatInput"] textarea {
                direction: auto;
                text-align: start;
                unicode-bidi: plaintext;
                font-family: "Noto Sans Arabic", "Noto Sans Hebrew", "Segoe UI", sans-serif;
                border-radius: 12px;
                background: var(--fb-surface) !important;
                color: var(--fb-text) !important;
                border-color: var(--fb-border) !important;
            }

            div[data-testid="stMarkdownContainer"]:has(.fb-chat-thread) {
                max-width: 100%;
                overflow-x: hidden;
            }
            div[data-testid="stMarkdownContainer"]:has(.fb-chat-thread) > p {
                margin: 0;
            }
            .fb-chat-thread {
                display: flex;
                flex-direction: column;
                gap: 12px;
                width: 100%;
                max-width: 100%;
                margin: 0.35rem 0 0.75rem;
                direction: ltr;
                unicode-bidi: isolate;
                overflow-x: hidden;
                overflow-y: visible;
                scroll-behavior: smooth;
            }
            .fb-chat-panel,
            .fb-panel {
                overflow-x: hidden;
            }
            .fb-chat-message {
                display: flex;
                align-items: flex-start;
                gap: 0.55rem;
                width: 100%;
                max-width: 100%;
            }
            .fb-chat-message--user {
                justify-content: flex-end;
            }
            .fb-chat-message--assistant {
                justify-content: flex-start;
            }
            .fb-chat-avatar {
                flex: 0 0 32px;
                width: 32px;
                height: 32px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, #0f766e, #155e75);
                color: #fff;
                margin-top: 0.15rem;
            }
            .fb-chat-bubble {
                max-width: min(850px, 85%);
                border-radius: 16px;
                padding: 0.7rem 0.95rem;
                box-shadow: var(--fb-shadow-soft);
            }
            .fb-chat-bubble--assistant {
                background: var(--fb-surface);
                border: 1px solid var(--fb-border);
            }
            .fb-chat-bubble--user {
                background: #e6f4f2;
                border: 1px solid #b7ddd7;
            }
            .fb-chat-name {
                direction: ltr;
                text-align: left;
                font-size: 0.75rem;
                font-weight: 700;
                color: var(--fb-teal);
                margin: 0 0 0.35rem;
            }
            .fb-chat-name-sub {
                margin-inline-start: 0.35rem;
                color: var(--fb-text-muted);
                font-weight: 600;
            }
            .message-content {
                max-width: 100%;
                white-space: normal;
                overflow-wrap: anywhere;
                word-break: break-word;
                line-height: 1.7;
                font-size: 1.02rem;
                color: var(--fb-text);
                unicode-bidi: isolate;
            }
            .message-content--rtl {
                direction: rtl;
                text-align: right;
                font-family: "Noto Sans Arabic", "Noto Sans Hebrew", "IBM Plex Sans", sans-serif;
            }
            .message-content--ltr,
            .message-content--auto {
                direction: ltr;
                text-align: left;
                font-family: "IBM Plex Sans", "Noto Sans Arabic", "Noto Sans Hebrew", sans-serif;
            }
            .message-content p {
                margin: 0 0 0.65rem;
            }
            .message-content p:last-child {
                margin-bottom: 0;
            }
            .message-content ul,
            .message-content ol {
                margin: 0.2rem 0 0.65rem;
                padding-inline-start: 1.25rem;
            }
            .message-content pre,
            .message-content code {
                direction: ltr;
                text-align: left;
                unicode-bidi: isolate;
                font-family: ui-monospace, Consolas, monospace;
            }
            .message-content pre {
                background: var(--fb-code-bg);
                border: 1px solid var(--fb-border);
                border-radius: 10px;
                padding: 0.75rem 0.85rem;
                overflow-x: auto;
                white-space: pre-wrap;
            }
            .message-content code {
                background: var(--fb-code-bg);
                border-radius: 6px;
                padding: 0.05rem 0.3rem;
            }
            .message-content a {
                color: var(--fb-blue);
                overflow-wrap: anywhere;
            }
            .message-content bdi,
            .message-content [dir="ltr"] {
                unicode-bidi: isolate;
            }
            .fb-chat-cites {
                margin-top: 0.65rem;
                padding-top: 0.5rem;
                border-top: 1px solid var(--fb-border-subtle);
                font-size: 0.82rem;
            }
            .fb-chat-cites-title {
                margin: 0 0 0.3rem;
                font-weight: 700;
                color: var(--fb-text-muted);
            }
            .fb-chat-cites ul {
                margin: 0;
                padding-inline-start: 1.1rem;
            }
            .fb-chat-cite-item a {
                direction: ltr;
                unicode-bidi: isolate;
            }
            [data-testid="stChatInput"] {
                position: sticky;
                bottom: 0;
                z-index: 20;
                background: var(--fb-bg) !important;
                padding-top: 0.35rem;
            }
            @media (max-width: 720px) {
                .fb-chat-bubble {
                    max-width: 94%;
                    padding: 0.6rem 0.75rem;
                }
                .fb-chat-thread {
                    gap: 10px;
                }
                .fb-chat-avatar {
                    width: 28px;
                    height: 28px;
                    flex-basis: 28px;
                }
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
                border-radius: 12px;
                background: var(--fb-surface);
            }

            .fb-landing {
                max-width: 920px;
                margin: 0 auto 1.5rem;
            }
            .fb-landing-kicker {
                font-size: 0.72rem;
                letter-spacing: 0.14em;
                text-transform: uppercase;
                color: var(--fb-teal);
                font-weight: 700;
                margin: 0 0 0.45rem;
            }
            .fb-landing-title {
                font-family: Outfit, "IBM Plex Sans", sans-serif;
                font-size: clamp(1.7rem, 3vw, 2.35rem);
                line-height: 1.25;
                color: var(--fb-navy);
                margin: 0 0 0.7rem;
                font-weight: 750;
            }
            .fb-landing-lead {
                font-size: 1.05rem;
                line-height: 1.7;
                color: var(--fb-text-secondary);
                margin: 0 0 1.25rem;
                max-width: 40rem;
            }
            .fb-feature-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 0.75rem;
            }
            .fb-feature {
                background: #fff;
                border: 1px solid var(--fb-border);
                border-radius: 12px;
                padding: 0.95rem 1rem;
                min-height: 7.5rem;
            }
            .fb-feature strong {
                display: block;
                color: var(--fb-navy);
                margin-bottom: 0.35rem;
                font-size: 0.92rem;
            }
            .fb-feature p {
                margin: 0;
                color: var(--fb-text-secondary);
                line-height: 1.55;
                font-size: 0.9rem;
            }
            .fb-auth-card {
                background: #fff;
                border: 1px solid var(--fb-border);
                border-radius: 14px;
                padding: 1.1rem 1.15rem 0.4rem;
                box-shadow: 0 10px 30px rgba(7, 21, 37, 0.05);
                max-width: 460px;
            }
            .fb-user-chip {
                font-size: 0.82rem;
                color: var(--fb-text-muted);
                margin: 0 0 0.45rem;
            }
            .fb-hero {
                border-radius: 18px !important;
                padding: 1.35rem 1.4rem 1.15rem !important;
            }
            .fb-title {
                letter-spacing: -0.03em;
            }
            .fb-footer {
                max-width: 920px;
            }
            section[data-testid="stSidebar"] .stButton > button {
                min-height: 36px !important;
                font-size: 0.86rem !important;
            }

            .stApp {
                background: #F6F8FA !important;
                font-family: "Source Sans 3", "Noto Sans Arabic", "Noto Sans Hebrew", sans-serif !important;
            }
            .stApp::before { display: none !important; }
            .block-container {
                max-width: 880px !important;
                padding-top: 1.1rem !important;
            }
            [data-testid="stSidebar"] {
                background: #F6F8FA !important;
                border-inline-end: 1px solid #D7DEE6 !important;
            }
            [data-testid="stSidebar"] * {
                color: #1E293B !important;
            }
            [data-testid="stSidebar"] .stButton > button {
                background: #fff !important;
                color: #0F766E !important;
                border: 1px solid #C5D5D2 !important;
                border-radius: 12px !important;
            }

            .fb-topbar {
                display: flex;
                justify-content: space-between;
                align-items: flex-end;
                gap: 1.5rem;
                padding: 0 0 1rem;
                margin: 0 0 0.85rem;
                border-bottom: 1px solid #D7DEE6;
                background: transparent !important;
                box-shadow: none !important;
                border-radius: 0 !important;
                animation: none !important;
            }
            .fb-topbar::before,
            .fb-topbar::after { display: none !important; }
            .fb-topbar-brand {
                display: flex;
                align-items: center;
                gap: 0.75rem;
            }
            .fb-logomark {
                width: 32px;
                height: 32px;
                display: grid;
                place-items: center;
                background: #0F766E;
                color: #fff;
                border-radius: 10px;
                font-family: "Source Serif 4", serif;
                font-size: 1rem;
                font-weight: 700;
            }
            .fb-wordmark {
                margin: 0;
                font-family: "Source Serif 4", "Noto Sans Hebrew", "Noto Sans Arabic", serif;
                font-size: 1.35rem;
                font-weight: 600;
                letter-spacing: -0.02em;
                color: #0F3D3A;
                line-height: 1.1;
            }
            .fb-wordmark-sub {
                margin: 0.15rem 0 0;
                font-size: 0.72rem;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #64748B;
            }
            .fb-topline {
                display: flex;
                gap: 1rem;
                list-style: none;
                margin: 0 0 0.4rem;
                padding: 0;
                color: #475569;
                font-size: 0.78rem;
            }
            .fb-topline li span {
                display: inline-block;
                min-width: 0.9rem;
                margin-inline-end: 0.25rem;
                color: #0F766E;
                font-weight: 700;
            }
            .fb-deck {
                margin: 0 0 1.35rem;
                max-width: 38rem;
                font-size: 1.02rem;
                line-height: 1.6;
                color: #475569;
            }
            .fb-status-pill {
                display: inline-block !important;
                margin: 0 !important;
                padding: 0 !important;
                background: none !important;
                border: none !important;
                color: #0F766E !important;
                font-size: 0.72rem !important;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }
            .fb-status-dot { display: none !important; }

            .fb-masthead { max-width: 40rem; margin: 1rem 0 1.75rem; }
            .fb-eyebrow {
                margin: 0 0 0.55rem;
                font-size: 0.72rem;
                letter-spacing: 0.16em;
                text-transform: uppercase;
                color: #0F766E;
                font-weight: 650;
            }
            .fb-display {
                margin: 0 0 0.85rem;
                font-family: "Source Serif 4", "Noto Sans Arabic", "Noto Sans Hebrew", serif;
                font-size: clamp(2rem, 4.4vw, 3.1rem);
                line-height: 1.15;
                font-weight: 600;
                letter-spacing: -0.03em;
                color: #0F3D3A;
            }
            .fb-standfirst {
                margin: 0 0 1.6rem;
                font-size: 1.12rem;
                line-height: 1.7;
                color: #475569;
            }
            .fb-points {
                display: grid;
                gap: 0;
                border-top: 1px solid #D7DEE6;
            }
            .fb-point {
                display: grid;
                grid-template-columns: 2.4rem 1fr;
                gap: 0.85rem;
                padding: 0.85rem 0;
                border-bottom: 1px solid #E6EBF0;
                background: none;
                min-height: 0;
            }
            .fb-point span {
                font-family: "Source Serif 4", serif;
                color: #0F766E;
                font-weight: 600;
            }
            .fb-point p {
                margin: 0;
                color: #1E293B;
                line-height: 1.55;
                font-size: 0.98rem;
            }

            .fb-panel,
            .fb-chat-panel,
            .fb-empty,
            .fb-identity-card {
                background: #fff !important;
                border: 1px solid #E2E8F0 !important;
                border-radius: 16px !important;
                box-shadow: 0 8px 24px rgba(15, 61, 58, 0.04) !important;
            }
            .fb-auth-card { display: none !important; }
            .fb-auth-shell h2 {
                margin: 0 0 0.85rem;
                font-family: "Source Serif 4", "Noto Sans Arabic", "Noto Sans Hebrew", serif;
                font-size: 1.7rem;
                font-weight: 600;
                color: #0F3D3A;
            }
            [data-testid="stForm"] {
                background: #fff;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
                padding: 1rem 1.1rem 0.35rem;
                box-shadow: 0 8px 24px rgba(15, 61, 58, 0.04);
            }
            .fb-section-title {
                font-family: "Source Serif 4", "Noto Sans Arabic", "Noto Sans Hebrew", serif !important;
                font-size: 1.2rem !important;
                font-weight: 600 !important;
                color: #0F3D3A !important;
            }
            .fb-bridge-line { display: none !important; }

            .fb-chat-bubble { box-shadow: none !important; border-radius: 16px !important; }
            .fb-chat-bubble--assistant {
                background: transparent !important;
                border: none !important;
            }
            .fb-chat-bubble--user {
                background: #E7F3F1 !important;
                border: 1px solid #C5D5D2 !important;
            }
            .fb-chat-avatar {
                background: #0F766E !important;
                border-radius: 10px !important;
            }
            .fb-chat-name { color: #0F766E !important; }

            .stButton > button {
                border-radius: 12px !important;
                min-height: 44px !important;
                padding: 0.45rem 1.15rem !important;
                font-weight: 650 !important;
                box-shadow: none !important;
            }
            .stButton > button[kind="primary"] {
                background: #0F766E !important;
                border: 1px solid #0F766E !important;
                color: #fff !important;
            }
            .stButton > button[kind="primary"]:hover {
                background: #0C5F59 !important;
            }
            .stButton > button[kind="secondary"],
            .stButton > button[kind="tertiary"] {
                background: #fff !important;
                color: #0F766E !important;
                border: 1px solid #C5D5D2 !important;
            }
            div[data-testid="stRadio"] label {
                border-radius: 12px !important;
                border: 1px solid #D7DEE6 !important;
                background: #fff !important;
                box-shadow: none !important;
                min-height: 44px !important;
            }
            div[data-testid="stRadio"] label[data-checked="true"],
            div[data-testid="stRadio"] label:has(input:checked) {
                background: #E7F3F1 !important;
                color: #0F3D3A !important;
                border-color: #0F766E !important;
                box-shadow: none !important;
            }
            [data-testid="stTextInput"] input,
            [data-testid="stChatInput"] textarea {
                border-radius: 12px !important;
                background: #fff !important;
                min-height: 44px !important;
                box-shadow: none !important;
                border-color: #D7DEE6 !important;
            }
            .fb-footer {
                border-top: 1px solid #D7DEE6;
                color: #64748B;
                font-size: 0.8rem;
                margin-top: 2.5rem;
                padding-top: 0.9rem;
                background: none;
            }

            /* ============================================================
               FormBridge 2026 — final visual system
               Kept last intentionally so one coherent system wins over
               older component rules above.
               ============================================================ */
            :root {
                --fb-primary: #0B6B63;
                --fb-primary-hover: #07564F;
                --fb-primary-soft: #E8F5F2;
                --fb-accent: #D5A84B;
                --fb-navy: #102A43;
                --fb-ink: #172B3A;
                --fb-muted: #617182;
                --fb-canvas: #F4F7F9;
                --fb-surface: #FFFFFF;
                --fb-line: #DCE5EA;
                --fb-line-strong: #C7D5DC;
                --fb-radius: 20px;
                --fb-shadow: 0 18px 50px rgba(16, 42, 67, .09);
                --fb-shadow-hover: 0 22px 55px rgba(16, 42, 67, .14);
            }

            html, body, .stApp,
            [data-testid="stMarkdownContainer"],
            button, input, textarea, select {
                font-family: "Manrope", "Noto Sans Arabic", "Noto Sans Hebrew", sans-serif !important;
            }
            .stApp {
                color: var(--fb-ink) !important;
                background:
                    radial-gradient(circle at 7% 2%, rgba(11,107,99,.10), transparent 24rem),
                    radial-gradient(circle at 95% 12%, rgba(213,168,75,.10), transparent 22rem),
                    var(--fb-canvas) !important;
            }
            .block-container {
                max-width: 1080px !important;
                padding: 1.75rem 2rem 5rem !important;
            }

            /* Premium header */
            .fb-topbar {
                align-items: center !important;
                padding: .9rem 1.1rem !important;
                margin-bottom: 1.4rem !important;
                border: 1px solid rgba(199,213,220,.9) !important;
                border-radius: 18px !important;
                background: rgba(255,255,255,.82) !important;
                box-shadow: 0 10px 35px rgba(16,42,67,.06) !important;
                backdrop-filter: blur(16px);
            }
            .fb-logomark {
                width: 42px !important;
                height: 42px !important;
                border-radius: 13px !important;
                background: linear-gradient(145deg, #0B6B63, #084C47) !important;
                box-shadow: 0 8px 18px rgba(11,107,99,.25);
                font-family: "Manrope", sans-serif !important;
            }
            .fb-wordmark {
                font-family: "Manrope", sans-serif !important;
                font-size: 1.25rem !important;
                font-weight: 800 !important;
                color: var(--fb-navy) !important;
                letter-spacing: -.035em !important;
            }
            .fb-wordmark-sub { font-weight: 700; color: var(--fb-muted); }
            .fb-status-pill {
                display: inline-flex !important;
                align-items: center;
                padding: .45rem .75rem !important;
                border: 1px solid #B9DDD7 !important;
                border-radius: 999px !important;
                background: var(--fb-primary-soft) !important;
                color: var(--fb-primary) !important;
                font-weight: 800 !important;
                letter-spacing: .04em !important;
            }

            /* Strong type hierarchy */
            .fb-display {
                font-family: "Manrope", "Noto Sans Arabic", "Noto Sans Hebrew", sans-serif !important;
                max-width: 800px;
                font-size: clamp(2.25rem, 5vw, 4rem) !important;
                line-height: 1.08 !important;
                font-weight: 800 !important;
                letter-spacing: -.055em !important;
                color: var(--fb-navy) !important;
            }
            .fb-eyebrow, .fb-kicker {
                color: var(--fb-primary) !important;
                font-weight: 800 !important;
                letter-spacing: .12em !important;
            }
            .fb-standfirst, .fb-deck {
                max-width: 720px !important;
                color: var(--fb-muted) !important;
                font-size: 1.08rem !important;
                line-height: 1.8 !important;
            }
            .fb-section-title {
                font-family: "Manrope", "Noto Sans Arabic", "Noto Sans Hebrew", sans-serif !important;
                color: var(--fb-navy) !important;
                font-size: 1.25rem !important;
                font-weight: 800 !important;
                letter-spacing: -.025em !important;
            }

            /* Cards with depth and clear grouping */
            .fb-panel, .fb-chat-panel, .fb-empty, .fb-brief, .fb-identity-card,
            .fb-feature, .fb-auth-card {
                background: rgba(255,255,255,.96) !important;
                border: 1px solid var(--fb-line) !important;
                border-radius: var(--fb-radius) !important;
                box-shadow: var(--fb-shadow) !important;
            }
            .fb-panel, .fb-chat-panel { padding: 1.55rem 1.65rem 1rem !important; }
            .fb-panel:hover, .fb-feature:hover, .fb-identity-card:hover {
                border-color: var(--fb-line-strong) !important;
                box-shadow: var(--fb-shadow-hover) !important;
                transform: translateY(-2px);
                transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
            }
            /* Centered landing composition */
            .fb-masthead {
                position: relative;
                max-width: 980px !important;
                margin: 3.2rem auto 2.5rem !important;
                padding: 2.2rem 1.4rem 1rem;
                text-align: center !important;
            }
            .fb-masthead::before {
                content: "";
                position: absolute;
                width: 380px;
                height: 380px;
                top: -150px;
                left: 50%;
                transform: translateX(-50%);
                border-radius: 50%;
                background: radial-gradient(circle, rgba(11,107,99,.12), transparent 68%);
                pointer-events: none;
                z-index: -1;
            }
            .fb-masthead .fb-eyebrow,
            .fb-masthead .fb-display,
            .fb-masthead .fb-standfirst {
                margin-inline: auto !important;
                text-align: center !important;
            }
            .fb-masthead > .fb-eyebrow:first-child {
                display: inline-flex;
                align-items: center;
                gap: .5rem;
                padding: .45rem .85rem;
                margin-bottom: 1.25rem !important;
                border: 1px solid #B9DDD7;
                border-radius: 999px;
                background: rgba(232,245,242,.88);
                box-shadow: 0 8px 22px rgba(11,107,99,.08);
            }
            .fb-masthead > .fb-eyebrow:first-child::before {
                content: "";
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: #19A58F;
                box-shadow: 0 0 0 4px rgba(25,165,143,.13);
            }
            .fb-display {
                max-width: 900px !important;
                text-wrap: balance;
            }
            .fb-standfirst {
                max-width: 790px !important;
                margin-bottom: 2.7rem !important;
                text-wrap: balance;
            }
            .fb-masthead > .fb-eyebrow:nth-of-type(3) {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: .9rem;
                margin-bottom: 1.15rem !important;
                font-size: .82rem;
            }
            .fb-masthead > .fb-eyebrow:nth-of-type(3)::before,
            .fb-masthead > .fb-eyebrow:nth-of-type(3)::after {
                content: "";
                width: 54px;
                height: 1px;
                background: linear-gradient(90deg, transparent, #A9C4C0);
            }
            .fb-masthead > .fb-eyebrow:nth-of-type(3)::after {
                transform: scaleX(-1);
            }
            .fb-points {
                display: grid !important;
                grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
                gap: 1rem !important;
                max-width: 900px;
                margin: 0 auto;
                border: 0 !important;
                text-align: start !important;
            }
            .fb-point {
                position: relative;
                display: grid !important;
                grid-template-columns: 3rem minmax(0, 1fr) !important;
                align-items: start;
                gap: 1rem !important;
                min-height: 148px !important;
                padding: 1.3rem 1.25rem !important;
                overflow: hidden;
                border: 1px solid var(--fb-line) !important;
                border-radius: 20px;
                background: rgba(255,255,255,.88) !important;
                box-shadow: 0 14px 38px rgba(16,42,67,.07);
                backdrop-filter: blur(12px);
                transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease;
            }
            .fb-point::after {
                content: "";
                position: absolute;
                inset-inline-end: -38px;
                bottom: -48px;
                width: 120px;
                height: 120px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(213,168,75,.11), transparent 68%);
            }
            .fb-point:hover {
                transform: translateY(-4px);
                border-color: #B9D8D3 !important;
                box-shadow: 0 20px 45px rgba(16,42,67,.12);
            }
            .fb-point span {
                display: grid;
                place-items: center;
                width: 3rem;
                height: 3rem;
                border-radius: 15px;
                color: #8A671F !important;
                background: #FBF4E4;
                border: 1px solid #EBD9AE;
                font-family: "Manrope", sans-serif !important;
                font-size: .9rem;
                font-weight: 800 !important;
                line-height: 1;
            }
            .fb-point p {
                margin: .1rem 0 0 !important;
                color: var(--fb-ink) !important;
                font-size: 1rem !important;
                line-height: 1.75 !important;
                font-weight: 600;
            }

            /* Controls */
            .stButton > button {
                min-height: 48px !important;
                padding: .65rem 1.2rem !important;
                border-radius: 14px !important;
                font-weight: 800 !important;
                transition: transform .16s ease, box-shadow .16s ease, background .16s ease !important;
            }
            .stButton > button[kind="primary"] {
                color: #fff !important;
                background: linear-gradient(135deg, #0B766D, #07564F) !important;
                border: 1px solid #07564F !important;
                box-shadow: 0 9px 22px rgba(11,107,99,.22) !important;
            }
            .stButton > button:hover { transform: translateY(-1px); }
            .stButton > button[kind="primary"]:hover {
                background: linear-gradient(135deg, #08645C, #064741) !important;
                box-shadow: 0 12px 26px rgba(11,107,99,.28) !important;
            }
            [data-testid="stTextInput"] input,
            [data-testid="stTextArea"] textarea,
            [data-testid="stChatInput"] textarea,
            [data-baseweb="select"] > div,
            [data-testid="stFileUploaderDropzone"] {
                border: 1px solid var(--fb-line-strong) !important;
                border-radius: 14px !important;
                background: #fff !important;
                box-shadow: 0 1px 2px rgba(16,42,67,.03) !important;
            }
            [data-testid="stTextInput"] input:focus,
            [data-testid="stTextArea"] textarea:focus,
            [data-testid="stChatInput"] textarea:focus {
                border-color: var(--fb-primary) !important;
                box-shadow: 0 0 0 4px rgba(11,107,99,.12) !important;
            }
            div[data-testid="stRadio"] label {
                padding: .65rem .9rem !important;
                border-radius: 14px !important;
                font-weight: 700 !important;
            }
            div[data-testid="stRadio"] label:has(input:checked) {
                background: var(--fb-primary-soft) !important;
                border-color: var(--fb-primary) !important;
                box-shadow: 0 0 0 3px rgba(11,107,99,.08) !important;
            }

            /* Chat resembles a polished product, with readable separation */
            .fb-chat-thread { gap: 16px !important; padding: .4rem 0; }
            .fb-chat-bubble {
                max-width: min(760px, 82%) !important;
                padding: .9rem 1.05rem !important;
                border-radius: 18px !important;
                line-height: 1.75 !important;
            }
            .fb-chat-bubble--assistant {
                background: #fff !important;
                border: 1px solid var(--fb-line) !important;
                box-shadow: 0 7px 22px rgba(16,42,67,.06) !important;
            }
            .fb-chat-bubble--user {
                color: #123C38 !important;
                background: linear-gradient(145deg, #E9F7F4, #DDF0EC) !important;
                border: 1px solid #B9DDD7 !important;
            }
            .fb-chat-avatar {
                width: 36px !important;
                height: 36px !important;
                flex-basis: 36px !important;
                border-radius: 12px !important;
                box-shadow: 0 6px 14px rgba(11,107,99,.20);
            }
            [data-testid="stChatInput"] {
                padding: .7rem 0 .3rem !important;
                background: rgba(244,247,249,.92) !important;
                backdrop-filter: blur(12px);
            }

            /* Sidebar */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #F8FAFB 0%, #EEF4F4 100%) !important;
                border-inline-end: 1px solid var(--fb-line) !important;
            }
            /* Keep the main page full-width after the sidebar is collapsed. */
            [data-testid="stAppViewContainer"] > .main {
                width: 100% !important;
                min-width: 0 !important;
            }
            [data-testid="stSidebar"][aria-expanded="false"] {
                min-width: 0 !important;
                max-width: 0 !important;
                border: 0 !important;
            }
            [data-testid="collapsedControl"] {
                direction: ltr !important;
                z-index: 1000000 !important;
            }
            [data-testid="stSidebar"] .stButton > button {
                background: rgba(255,255,255,.9) !important;
                border-color: var(--fb-line) !important;
            }

            @media (max-width: 780px) {
                .block-container { padding: 1rem 1rem 4rem !important; }
                .fb-topbar { align-items: flex-start !important; gap: .75rem !important; }
                .fb-topline { display: none !important; }
                .fb-display { font-size: clamp(2rem, 11vw, 3rem) !important; }
                .fb-masthead { margin-top: 1.4rem !important; padding-inline: 0; }
                .fb-points { grid-template-columns: 1fr !important; }
                .fb-point { min-height: 0 !important; }
                .fb-panel, .fb-chat-panel { padding: 1.15rem 1rem .75rem !important; }
                .fb-chat-bubble { max-width: 92% !important; }
            }

            .fb-auth-shell {
                margin: 0 0 1rem;
                text-align: center;
            }
            .fb-auth-shell h2 {
                margin: 0 0 .45rem !important;
                font-family: "Manrope", "Noto Sans Arabic", "Noto Sans Hebrew", sans-serif !important;
                font-size: 1.7rem !important;
                font-weight: 800 !important;
                letter-spacing: -.03em;
                color: var(--fb-navy) !important;
            }
            .fb-auth-shell p {
                margin: 0 auto;
                max-width: 26rem;
                color: var(--fb-muted);
                line-height: 1.65;
                font-size: .95rem;
            }
            [data-testid="stVerticalBlock"]:has(.fb-auth-shell) [data-testid="stForm"] {
                background: rgba(255,255,255,.97) !important;
                border: 1px solid var(--fb-line) !important;
                border-radius: 22px !important;
                padding: 1.2rem 1.2rem .4rem !important;
                box-shadow: var(--fb-shadow) !important;
            }
            [data-testid="stVerticalBlock"]:has(.fb-auth-shell) [data-testid="stForm"] .stButton > button,
            [data-testid="stVerticalBlock"]:has(.fb-auth-shell) [data-testid="stFormSubmitButton"] button {
                width: 100% !important;
            }
            [data-testid="stVerticalBlock"]:has(.fb-auth-shell) button[kind="tertiary"] {
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
                color: var(--fb-primary) !important;
                min-height: 38px !important;
            }
            [data-testid="stSegmentedControl"] {
                justify-content: center !important;
                margin-bottom: .35rem;
            }
            [data-testid="stVerticalBlock"]:has(.fb-auth-shell) [data-testid="stTextInput"] input {
                min-height: 48px !important;
                border-radius: 14px !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def is_admin_unlocked() -> bool:
    return bool(st.session_state.get("fb_admin_unlocked"))


def unlock_admin(password: str) -> bool:
    """Validate KB_ADMIN_PASSWORD and mark this browser session as admin."""
    import hmac
    import os

    expected = (os.getenv("KB_ADMIN_PASSWORD") or "").strip()
    if not expected or not password:
        return False
    if hmac.compare_digest(password, expected):
        st.session_state.fb_admin_unlocked = True
        return True
    return False


def lock_admin() -> None:
    st.session_state.fb_admin_unlocked = False


def render_sidebar_nav() -> None:
    """Home always visible; admin links only after password unlock for this session."""
    import os

    st.markdown("### FormBridge")
    st.page_link("app.py", label="Home", icon="🏠")

    if is_admin_unlocked():
        st.divider()
        st.caption("Admin")
        st.page_link("pages/1_Official_Sources.py", label="Official Sources", icon="📚")
        st.page_link("pages/2_Evals.py", label="Evals", icon="🧪")
        st.page_link("pages/3_Monitor.py", label="Monitor", icon="📊")
        if st.button("Lock admin", key="fb_admin_lock_btn", use_container_width=True):
            lock_admin()
            st.rerun()
        return

    with st.expander("Admin"):
        expected = (os.getenv("KB_ADMIN_PASSWORD") or "").strip()
        if not expected:
            st.caption("Admin access is not configured.")
            return
        password = st.text_input(
            "Password",
            type="password",
            key="fb_sidebar_admin_password",
            label_visibility="collapsed",
            placeholder="Password",
        )
        if st.button("Unlock", key="fb_admin_unlock_btn", use_container_width=True):
            if unlock_admin(password):
                st.rerun()
            else:
                st.error("Wrong password.")


def render_language_switcher(selected_language: str) -> str:
    """Compact 🌐 language icon at the top of the page."""
    code_to_lang = {
        "ar": LANGUAGE_AR,
        "he": LANGUAGE_HE,
        "en": LANGUAGE_EN,
    }
    labels = {
        "ar": "العربية",
        "he": "עברית",
        "en": "English",
    }

    if "language_selector" not in st.session_state:
        st.session_state.language_selector = selected_language
    if st.session_state.language_selector not in code_to_lang.values():
        st.session_state.language_selector = LANGUAGE_AR

    qp = st.query_params.get("lang")
    if isinstance(qp, (list, tuple)):
        qp = qp[0] if qp else None
    if qp in code_to_lang and qp != st.session_state.get("fb_language_query"):
        st.session_state.language_selector = code_to_lang[qp]
        st.session_state.fb_language_query = qp

    current_code = lang_code(st.session_state.language_selector)

    # Compact top-right control inside the page content.
    st.markdown(
        """
        <style>
        div[data-testid="stPopover"] button[data-testid="stPopoverButton"] {
            width: 2.75rem !important;
            min-width: 2.75rem !important;
            max-width: 2.75rem !important;
            height: 2.75rem !important;
            min-height: 2.75rem !important;
            padding: 0 !important;
            border-radius: 13px !important;
            border: 1px solid #C7D9D6 !important;
            background: rgba(255,255,255,.94) !important;
            box-shadow: 0 7px 20px rgba(16,42,67,.08) !important;
            justify-content: center !important;
            font-size: 1rem !important;
            line-height: 1 !important;
            transform: none !important;
        }
        div[data-testid="stPopover"] button[data-testid="stPopoverButton"]:hover {
            border-color: #0B6B63 !important;
            background: #EAF6F3 !important;
            box-shadow: 0 9px 24px rgba(11,107,99,.14) !important;
        }
        div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPopover"]) {
            direction: ltr !important;
            align-items: center !important;
            margin: 0 0 .35rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    _spacer, icon_col = st.columns([14, 1])
    with icon_col:
        with st.popover("🌐"):
            for code in ("ar", "he", "en"):
                is_current = code == current_code
                if st.button(
                    labels[code],
                    key=f"fb_lang_pop_{code}",
                    type="primary" if is_current else "secondary",
                    use_container_width=True,
                    disabled=is_current,
                ):
                    st.session_state.language_selector = code_to_lang[code]
                    st.session_state.fb_language_query = code
                    st.query_params["lang"] = code
                    st.rerun()

    if st.query_params.get("lang") != current_code:
        st.session_state.fb_language_query = current_code
        st.query_params["lang"] = current_code

    return st.session_state.language_selector


def render_header(
    selected_language: str,
    status: str = "idle",
    mode: str = "upload",
) -> None:
    strings = ui(selected_language)
    guided = mode == "guided"
    if guided:
        status_label = {
            "ready": strings["status_guided_ready"],
            "done": strings["status_guided_done"],
        }.get(status, strings["status_guided_idle"])
        subtitle = strings["guided_subtitle"]
        steps = (
            strings["step_describe"],
            strings["step_clarify"],
            strings["step_guidance"],
        )
    else:
        status_label = {
            "ready": strings["status_ready"],
            "done": strings["status_done"],
        }.get(status, strings["status_idle"])
        subtitle = strings["subtitle"]
        steps = (
            strings["step_upload"],
            strings["step_language"],
            strings["step_analyze"],
        )
    status_class = f"fb-status-pill fb-status-{status}"
    step_html = "".join(
        f'<li><span>{index}</span>{html.escape(label)}</li>'
        for index, label in enumerate(steps, start=1)
    )
    st.markdown(
        f"""
        <header class="fb-topbar">
            <div class="fb-topbar-brand">
                <span class="fb-logomark" aria-hidden="true">F</span>
                <div>
                    <p class="fb-wordmark">FormBridge</p>
                    <p class="fb-wordmark-sub">Official Israeli form guidance</p>
                </div>
            </div>
            <div class="fb-topbar-aside">
                <ol class="fb-topline">{step_html}</ol>
                <p class="{status_class}">{html.escape(status_label)}</p>
            </div>
        </header>
        <p class="fb-deck">{html.escape(subtitle)}</p>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(selected_language: str) -> None:
    strings = ui(selected_language)
    st.markdown(
        f"""
        <div class="fb-empty">
            <h3>{html.escape(strings["empty_title"])}</h3>
            <span class="fb-bridge-line" style="margin: 0.7rem 0 0.85rem auto;"></span>
            <p>{html.escape(strings["empty_body"])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _visible_guided_value(value: str | None) -> str:
    text = html.unescape((value or "").strip())
    if not text or text in {"—", "-", "n/a", "N/A"}:
        return ""
    return text


def _guidance_has_sidebar_details(guidance: GuidedGuidance) -> bool:
    return bool(
        _visible_guided_value(guidance.identified_service)
        or _visible_guided_value(guidance.authority)
        or _visible_guided_value(guidance.form_number)
        or _visible_guided_value(guidance.eligibility_summary)
        or guidance.important_fields
        or guidance.required_documents
        or guidance.missing_fields
        or guidance.steps
        or guidance.official_links
        or (
            guidance.status == "need_clarification"
            and guidance.clarifying_questions
        )
    )


def render_guided_result(
    guidance: GuidedGuidance,
    selected_language: str,
    citations: list[dict] | None = None,
) -> None:
    """Show follow-up chips or structured details — never a second copy of the chat reply."""
    strings = ui(selected_language)
    if not _guidance_has_sidebar_details(guidance):
        return

    if guidance.status == "need_clarification":
        questions = guidance.clarifying_questions or []
        if questions:
            st.markdown(f"**{strings['guided_questions']}**")
            for index, question in enumerate(questions):
                if st.button(question, key=f"guided_q_{index}", use_container_width=True):
                    st.session_state.guided_pending = question
                    st.rerun()
        return

    identity_cards: list[tuple[str, str]] = [
        (strings["guided_service"], _visible_guided_value(guidance.identified_service)),
        (strings["guided_authority"], _visible_guided_value(guidance.authority)),
        (strings["guided_form_number"], _visible_guided_value(guidance.form_number)),
    ]
    identity_cards = [(label, value) for label, value in identity_cards if value]
    if identity_cards:
        cards_html = "".join(
            f'<div class="fb-identity-card">'
            f'<p class="fb-identity-label">{html.escape(label)}</p>'
            f'<p class="fb-identity-value">{html.escape(value)}</p>'
            f"</div>"
            for label, value in identity_cards
        )
        st.markdown(
            f'<div class="fb-guided-details"><div class="fb-identity-grid">{cards_html}</div></div>',
            unsafe_allow_html=True,
        )

    if _visible_guided_value(guidance.eligibility_summary):
        st.markdown(f"**{strings['guided_eligibility']}**")
        st.write(guidance.eligibility_summary)

    if guidance.important_fields:
        st.markdown(f"**{strings.get('guided_fields', 'Important fields')}**")
        for item in guidance.important_fields:
            st.write(f"- {item}")

    if guidance.required_documents:
        st.markdown(f"**{strings['guided_documents']}**")
        for item in guidance.required_documents:
            st.write(f"- {item}")

    if guidance.missing_fields:
        st.markdown(f"**{strings.get('guided_missing', 'Missing information')}**")
        for item in guidance.missing_fields:
            st.write(f"- {item}")

    if guidance.steps:
        st.markdown(f"**{strings['guided_steps']}**")
        for index, step in enumerate(guidance.steps, start=1):
            st.write(f"{index}. {step}")

    chat_reply = html.unescape(
        humanize_guided_text(guidance.assistant_message, lang_code(selected_language))
    ).strip()
    preview = _visible_guided_value(guidance.preview_summary)
    if preview and preview != chat_reply:
        st.markdown(f"**{strings.get('guided_preview', 'Preview')}**")
        st.write(preview)

    if guidance.steps or guidance.official_links:
        st.caption(strings.get("guided_no_autosubmit", "FormBridge never submits forms automatically."))

    if guidance.official_links:
        st.markdown(f"**{strings['guided_links']}**")
        for link in guidance.official_links:
            title = link.title or link.url
            st.markdown(f"- [{title}]({link.url})")

    if guidance.confidence_note:
        st.caption(guidance.confidence_note)

    claim_like = bool(guidance.steps or guidance.required_documents)
    render_citations(
        citations or [],
        selected_language,
        warn_if_empty=claim_like and not citations and not guidance.official_links,
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
        f'<footer class="fb-footer" role="contentinfo">{html.escape(strings["footer_disclaimer"])}</footer>',
        unsafe_allow_html=True,
    )


def render_landing(selected_language: str) -> None:
    strings = ui(selected_language)
    features = (
        ("01", strings["feat_flow"]),
        ("02", strings["feat_kb"]),
        ("03", strings["feat_rag"]),
        ("04", strings["feat_safe"]),
    )
    cards = "".join(
        f'<article class="fb-point"><span>{index}</span><p>{html.escape(text)}</p></article>'
        for index, text in features
    )
    st.markdown(
        f"""
        <section class="fb-masthead" dir="auto">
            <p class="fb-eyebrow">{html.escape(strings["landing_kicker"])}</p>
            <h1 class="fb-display">{html.escape(strings["landing_title"])}</h1>
            <p class="fb-standfirst">{html.escape(strings["landing_lead"])}</p>
            <p class="fb-eyebrow">{html.escape(strings["landing_how"])}</p>
            <div class="fb-points">{cards}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_auth_panel(selected_language: str) -> None:
    from auth import authenticate, register_user, validate_credentials

    strings = ui(selected_language)
    view = st.session_state.get("fb_auth_view") or "login"
    if view not in ("login", "signup"):
        view = "login"
        st.session_state.fb_auth_view = "login"
    _left, card, _right = st.columns([0.7, 1.4, 0.7], gap="medium")
    with card:
        notice = st.session_state.pop("fb_auth_flash", None)
        if notice:
            st.success(notice)

        if st.session_state.get("fb_auth_segment") not in ("login", "signup"):
            st.session_state.fb_auth_segment = view
        picked = st.segmented_control(
            "auth-mode",
            options=["login", "signup"],
            format_func=lambda item: strings["auth_login"]
            if item == "login"
            else strings["auth_register"],
            key="fb_auth_segment",
            label_visibility="collapsed",
            width="stretch",
        )
        if picked in ("login", "signup"):
            view = picked
            st.session_state.fb_auth_view = view
        titles = {
            "login": strings["auth_login"],
            "signup": strings["auth_register"],
        }
        leads = {
            "login": strings["auth_login_lead"],
            "signup": strings["auth_signup_lead"],
        }
        st.markdown(
            f'<section class="fb-auth-shell"><h2>{html.escape(titles.get(view, strings["auth_login"]))}</h2>'
            f"<p>{html.escape(leads.get(view, ''))}</p></section>",
            unsafe_allow_html=True,
        )

        if view == "login":
            with st.form("fb_login_form", clear_on_submit=False, border=False):
                email = st.text_input(
                    strings["auth_email"],
                    key="fb_login_email",
                    autocomplete="username",
                    placeholder="name@email.com",
                )
                password = st.text_input(
                    strings["auth_password"],
                    type="password",
                    key="fb_login_password",
                    autocomplete="current-password",
                )
                submitted = st.form_submit_button(
                    strings["auth_login"],
                    type="primary",
                    use_container_width=True,
                )
            if submitted:
                user = authenticate(email, password)
                if user:
                    st.session_state.fb_user = user
                    st.session_state.fb_guest = False
                    st.rerun()
                st.error(strings["auth_error_invalid"])

        else:
            with st.form("fb_signup_form", clear_on_submit=False, border=False):
                name = st.text_input(strings["auth_name"], key="fb_signup_name")
                email = st.text_input(
                    strings["auth_email"],
                    key="fb_signup_email",
                    autocomplete="email",
                    placeholder="name@email.com",
                )
                password = st.text_input(
                    strings["auth_password"],
                    type="password",
                    key="fb_signup_password",
                    help=strings["auth_password_hint"],
                    autocomplete="new-password",
                )
                confirm = st.text_input(
                    strings["auth_confirm"],
                    type="password",
                    key="fb_signup_confirm",
                    autocomplete="new-password",
                )
                submitted = st.form_submit_button(
                    strings["auth_register"],
                    type="primary",
                    use_container_width=True,
                )
            if submitted:
                problem = validate_credentials(email, password)
                if problem == "invalid_email":
                    st.error(strings["auth_error_email"])
                elif problem == "weak_password":
                    st.error(strings["auth_error_weak"])
                elif password != confirm:
                    st.error(strings["auth_error_mismatch"])
                else:
                    try:
                        user = register_user(email, password, name)
                        st.session_state.fb_user = user
                        st.session_state.fb_guest = False
                        st.session_state.fb_flash = strings["auth_welcome_sent"]
                        st.rerun()
                    except ValueError as error:
                        if str(error) == "exists":
                            st.error(strings["auth_error_exists"])
                        elif str(error) == "weak_password":
                            st.error(strings["auth_error_weak"])
                        else:
                            st.error(strings["auth_error_email"])

        if st.button(strings["auth_guest"], key="fb_guest_btn", type="secondary", use_container_width=True):
            st.session_state.fb_guest = True
            st.session_state.fb_user = None
            st.rerun()


def render_account_sidebar(selected_language: str) -> None:
    from auth import delete_conversation, list_conversations

    strings = ui(selected_language)
    user = st.session_state.get("fb_user")
    if user:
        st.caption(user.get("display_name") or user["email"])
        if st.button(strings["auth_logout"], key="fb_logout_btn", type="secondary"):
            st.session_state.fb_user = None
            st.session_state.fb_guest = False
            st.session_state.fb_auth_view = "login"
            st.session_state.fb_auth_segment = "login"
            st.rerun()
        with st.expander(strings["auth_change_password"]):
            from auth import change_password

            with st.form("fb_change_password_form", border=False):
                current = st.text_input(
                    strings["auth_current_password"],
                    type="password",
                    key="fb_pw_current",
                )
                new_password = st.text_input(
                    strings["auth_password"],
                    type="password",
                    key="fb_pw_new",
                    help=strings["auth_password_hint"],
                )
                confirm = st.text_input(
                    strings["auth_confirm"],
                    type="password",
                    key="fb_pw_confirm",
                )
                submitted = st.form_submit_button(
                    strings["auth_change_save"],
                    type="primary",
                    use_container_width=True,
                )
            if submitted:
                if new_password != confirm:
                    st.error(strings["auth_error_mismatch"])
                else:
                    problem = change_password(user["email"], current, new_password)
                    if not problem:
                        st.success(strings["auth_change_done"])
                    elif problem == "weak_password":
                        st.error(strings["auth_error_weak"])
                    else:
                        st.error(strings["auth_change_bad"])
        if st.button(strings["new_chat"], key="fb_new_chat_btn", type="secondary"):
            st.session_state["_fb_new_chat"] = True
            st.rerun()
        rows = list_conversations(user["user_id"])[:12]
        with st.popover("☰  " + strings["recent_chats"]):
            if not rows:
                st.caption(strings["chat_empty"])
            for row in rows:
                title = str(row.get("title") or row.get("id") or "")
                left, right = st.columns([5, 1])
                if left.button(title, key=f"fb_load_{row['id']}", use_container_width=True):
                    st.session_state["_fb_load_chat"] = row["id"]
                    st.rerun()
                if right.button("✕", key=f"fb_del_{row['id']}", help=strings["delete_chat"]):
                    delete_conversation(user["user_id"], row["id"])
                    st.rerun()
    elif st.session_state.get("fb_guest"):
        st.caption(strings["account_guest"])
        if st.button(strings["new_chat"], key="fb_new_chat_guest", type="secondary"):
            st.session_state["_fb_new_chat"] = True
            st.rerun()


def render_field_validator(selected_language: str) -> None:
    from validation import validate_user_input

    strings = ui(selected_language)
    with st.expander(strings["validator_title"]):
        st.caption(strings["validator_help"])
        field_type = st.selectbox(
            strings["validator_title"],
            options=["israeli_id", "email", "phone", "date", "required"],
            label_visibility="collapsed",
            key="fb_validator_type",
        )
        value = st.text_input(strings["validator_help"], key="fb_validator_value")
        if st.button(strings["validator_run"], key="fb_validator_run"):
            result = validate_user_input(field_type, value)
            if result.ok:
                st.success(result.message)
            else:
                st.error(result.message)


def normalize_chat_response(text: str, language: str = "ar") -> str:
    """Light cleanup so assistant answers render consistently."""
    from chat_ui import normalize_chat_response as render_normalized_chat

    return render_normalized_chat(text, language)


def render_citations(
    citations: list[dict],
    selected_language: str,
    *,
    warn_if_empty: bool = True,
) -> None:
    strings = ui(selected_language)
    if not citations:
        if warn_if_empty:
            st.warning(strings["no_official_source"])
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
        updated = html.escape(item.get("last_updated_at") or "")
        date_bits = []
        if updated:
            date_bits.append(f'{strings["last_updated"]}: {updated}')
        if checked:
            date_bits.append(f'{strings["last_checked"]}: {checked}')
        meta = " · ".join(date_bits)
        st.markdown(
            f'<div class="fb-cite">'
            f'<span class="fb-cite-badge">{html.escape(badge)}</span> '
            f'<strong>{authority}</strong> — {title}<br>'
            f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(url)}</a><br>'
            f'<span class="fb-cite-meta">{meta}</span>'
            f"</div>",
            unsafe_allow_html=True,
        )


def render_chat_bubble(
    content: str,
    role: str,
    selected_language: str,
    citations: list[dict] | None = None,
) -> None:
    """Render a single chat message with per-message RTL/LTR detection."""
    from chat_ui import render_conversation

    render_conversation(
        [{"role": role, "content": content, "citations": citations}],
        selected_language,
        strings=ui(selected_language),
    )
