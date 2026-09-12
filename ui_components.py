"""UI strings, styling, and reusable Streamlit components."""

from __future__ import annotations

import html
from typing import Any

import streamlit as st
import streamlit.components.v1 as components

from models import (
    DocumentAnalysis,
    GuidedGuidance,
    NOT_MENTIONED_AR,
    NOT_MENTIONED_EN,
    NOT_MENTIONED_HE,
)


LANGUAGE_AR = "العربية"
LANGUAGE_HE = "עברית פשוטה"
LANGUAGE_EN = "English"

UI_STRINGS: dict[str, dict[str, str]] = {
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
        "guided_placeholder": "مثال: فقدت عملي وأريد معرفة كيف أطلب دمي أبطالة...",
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
        "guided_placeholder": "לדוגמה: פוטרתי מהעבודה ורוצה לדעת איך מגישים תביעה לדמי אבטלה...",
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
        "guided_placeholder": "Example: I lost my job and want to know how to apply for unemployment benefits...",
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
        "generic": "אירעה שגיאה בעיבוד. נסו שוב.",
        "file_too_large": "גודל הקובץ גדול מדי. המקסימום הוא 10MB.",
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
        "generic": "Something went wrong while processing. Please try again.",
        "file_too_large": "The file is too large. Maximum size is 10 MB.",
    },
}


def lang_code(selected_language: str) -> str:
    if selected_language == LANGUAGE_AR:
        return "ar"
    if selected_language == LANGUAGE_EN:
        return "en"
    return "he"


def ui(selected_language: str) -> dict[str, Any]:
    return UI_STRINGS[lang_code(selected_language)]


def errors(selected_language: str) -> dict[str, str]:
    return ERROR_MESSAGES[lang_code(selected_language)]


def rtl_block(content: str, *, extra_class: str = "") -> str:
    safe = html.escape(content).replace("\n", "<br>")
    class_attr = f"rtl-text {extra_class}".strip()
    return f'<div class="{class_attr}">{safe}</div>'


def inject_global_css(selected_language: str | None = None) -> None:
    ltr_override = ""
    if selected_language == LANGUAGE_EN:
        ltr_override = """
            .stApp, section.main, .block-container {
                direction: ltr !important;
            }
            .fb-hero, .fb-panel, .fb-section-title, .fb-chat-panel, .fb-empty, .fb-subtitle, .fb-privacy, .fb-mode-label {
                direction: ltr !important;
                text-align: left !important;
            }
            .fb-subtitle, .fb-privacy, .fb-mode-label, .fb-section-title {
                margin-left: 0 !important;
                margin-right: auto !important;
            }
            .fb-bridge-line {
                margin-left: 0 !important;
                margin-right: auto !important;
            }
            .fb-steps .fb-step, .fb-identity-card {
                direction: ltr !important;
                text-align: left !important;
            }
            .fb-steps {
                direction: ltr !important;
            }
            .fb-step-num {
                margin-left: 0 !important;
                margin-right: 0.45rem !important;
            }
            div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
            [data-testid="stChatInput"] textarea {
                direction: ltr !important;
                text-align: left !important;
            }
            .fb-chat-en div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
                direction: ltr !important;
                text-align: left !important;
            }
        """
    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=IBM+Plex+Sans:wght@400;500;600;700&family=Noto+Sans+Arabic:wght@400;500;600;700&family=Noto+Sans+Hebrew:wght@400;500;600;700&display=swap');

            :root {{
                --fb-navy: #071525;
                --fb-blue: #155e75;
                --fb-teal: #0f766e;
                --fb-accent: #14b8a6;
                --fb-ink: #071525;
                --fb-text: #122033;
                --fb-text-secondary: #3f556c;
                --fb-text-muted: #6b8198;
                --fb-bg: #e9eef5;
                --fb-surface: #ffffff;
                --fb-surface-soft: #f3f7fb;
                --fb-border: #cfdceb;
                --fb-border-subtle: #e2eaf3;
                --fb-shadow: 0 24px 60px rgba(7, 21, 37, 0.10);
                --fb-shadow-soft: 0 8px 24px rgba(7, 21, 37, 0.06);
                --fb-warning-bg: #fff7e8;
                --fb-warning-border: #efd7a4;
                --fb-warning-text: #7a5600;
                --fb-chat-bg: #ffffff;
                --fb-code-bg: #eef4f8;
                --fb-blockquote-bg: #ecf9f6;
                --fb-hero-glow: rgba(20, 184, 166, 0.16);
                --fb-radius: 28px;
                --fb-radius-sm: 14px;
            }}
{ltr_override}
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

            .fb-identity-grid {
                direction: rtl;
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 0.8rem;
                margin: 0.95rem 0 1.1rem 0;
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
                background: linear-gradient(135deg, #071525, #0f766e) !important;
                border: none !important;
                border-radius: 14px !important;
                min-height: 52px;
                font-weight: 700;
                font-size: 1rem !important;
                color: #fff !important;
                box-shadow: 0 14px 28px rgba(15, 118, 110, 0.28);
                transition: transform 0.15s ease, box-shadow 0.15s ease;
            }

            .stButton > button[kind="primary"]:hover {
                transform: translateY(-2px);
                box-shadow: 0 18px 34px rgba(15, 118, 110, 0.34);
            }

            .stButton > button[kind="secondary"],
            .stButton > button {
                border-radius: 14px !important;
                min-height: 46px;
                font-weight: 650 !important;
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
                direction: rtl;
                text-align: right;
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


def render_language_switcher(selected_language: str) -> str:
    """Pin a 🌐 language popover beside Streamlit's Deploy button."""
    code_to_lang = {
        "ar": LANGUAGE_AR,
        "he": LANGUAGE_HE,
        "en": LANGUAGE_EN,
    }
    qp = st.query_params.get("lang")
    if isinstance(qp, (list, tuple)):
        qp = qp[0] if qp else None
    if qp in code_to_lang:
        st.session_state.language_selector = code_to_lang[qp]
        selected_language = code_to_lang[qp]
    elif "language_selector" not in st.session_state:
        st.session_state.language_selector = selected_language
    else:
        selected_language = st.session_state.language_selector

    options = [LANGUAGE_AR, LANGUAGE_HE, LANGUAGE_EN]
    if selected_language not in options:
        selected_language = LANGUAGE_AR
        st.session_state.language_selector = selected_language

    st.markdown(
        """
        <style>
        div[data-testid="stLayoutWrapper"]:has(> [data-testid="stPopover"]) {
          position: fixed !important;
          top: 0.45rem !important;
          right: 7.35rem !important;
          left: auto !important;
          width: auto !important;
          height: 2.25rem !important;
          margin: 0 !important;
          padding: 0 !important;
          z-index: 1000000 !important;
          overflow: visible !important;
        }
        div[data-testid="stLayoutWrapper"]:has(> [data-testid="stPopover"]) [data-testid="stPopover"] {
          margin: 0 !important;
        }
        div[data-testid="stLayoutWrapper"]:has(> [data-testid="stPopover"])
          button[data-testid="stPopoverButton"] {
          min-width: 2.25rem !important;
          width: 2.25rem !important;
          height: 2.25rem !important;
          padding: 0 !important;
          border-radius: 999px !important;
          border: 1px solid rgba(49, 51, 63, 0.2) !important;
          background: #ffffff !important;
          box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
          justify-content: center !important;
        }
        div[data-testid="stLayoutWrapper"]:has(> [data-testid="stPopover"])
          button[data-testid="stPopoverButton"]
          span[data-testid="stIconMaterial"] {
          display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.popover("🌐", help="Language / اللغة / שפה"):
        choice = st.radio(
            "Language",
            options=options,
            index=options.index(selected_language),
            label_visibility="collapsed",
            key="fb_toolbar_language_radio",
        )
        if choice != selected_language:
            st.session_state.language_selector = choice
            st.query_params["lang"] = lang_code(choice)
            st.rerun()

    components.html(
        """
        <script>
        (function () {
          const doc = window.parent.document;
          function place() {
            const wrap = doc.querySelector(
              '[data-testid="stLayoutWrapper"]:has(> [data-testid="stPopover"])'
            );
            if (!wrap) return;
            const deploy =
              doc.querySelector('[data-testid="stAppDeployButton"]') ||
              Array.from(doc.querySelectorAll("button")).find(function (b) {
                return ((b.innerText || "") + "").trim() === "Deploy";
              });
            if (!deploy) return;
            const r = deploy.getBoundingClientRect();
            const size = 36;
            wrap.style.setProperty("position", "fixed", "important");
            wrap.style.setProperty("top", Math.max(4, r.top + (r.height - size) / 2) + "px", "important");
            wrap.style.setProperty("left", Math.max(8, r.left - size - 8) + "px", "important");
            wrap.style.setProperty("right", "auto", "important");
            wrap.style.setProperty("z-index", "1000000", "important");
            wrap.style.setProperty("width", "auto", "important");
            wrap.style.setProperty("height", size + "px", "important");
            wrap.style.setProperty("margin", "0", "important");
          }
          let n = 0;
          function tick() {
            place();
            n += 1;
            if (n < 40) setTimeout(tick, 200);
          }
          tick();
          window.parent.addEventListener("resize", place);
        })();
        </script>
        """,
        height=1,
        width=1,
    )
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
        f'<div class="fb-step"><span class="fb-step-num">{index}</span>{html.escape(label)}</div>'
        for index, label in enumerate(steps, start=1)
    )
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
            <p class="fb-subtitle">{html.escape(subtitle)}</p>
            <span class="fb-bridge-line"></span>
            <div class="fb-steps">
                {step_html}
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
            <span class="fb-bridge-line" style="margin: 0.7rem 0 0.85rem auto;"></span>
            <p>{html.escape(strings["empty_body"])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_guided_result(
    guidance: GuidedGuidance,
    selected_language: str,
    citations: list[dict] | None = None,
) -> None:
    """Show clarification questions or the completed guidance cards."""
    strings = ui(selected_language)
    st.info(guidance.assistant_message)

    if guidance.status == "need_clarification":
        questions = guidance.clarifying_questions or []
        if questions:
            st.markdown(f"**{strings['guided_questions']}**")
            for index, question in enumerate(questions):
                if st.button(question, key=f"guided_q_{index}", use_container_width=True):
                    st.session_state.guided_pending = question
                    st.rerun()
        return

    st.markdown(
        f"""
        <div class="fb-identity-grid">
            <div class="fb-identity-card">
                <p class="fb-identity-label">{html.escape(strings['guided_service'])}</p>
                <p class="fb-identity-value">{html.escape(guidance.identified_service or "—")}</p>
            </div>
            <div class="fb-identity-card">
                <p class="fb-identity-label">{html.escape(strings['guided_authority'])}</p>
                <p class="fb-identity-value">{html.escape(guidance.authority or "—")}</p>
            </div>
            <div class="fb-identity-card">
                <p class="fb-identity-label">{html.escape(strings['guided_form_number'])}</p>
                <p class="fb-identity-value">{html.escape(guidance.form_number or "—")}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if guidance.eligibility_summary:
        st.markdown(f"**{strings['guided_eligibility']}**")
        st.write(guidance.eligibility_summary)

    if guidance.required_documents:
        st.markdown(f"**{strings['guided_documents']}**")
        for item in guidance.required_documents:
            st.write(f"- {item}")

    if guidance.steps:
        st.markdown(f"**{strings['guided_steps']}**")
        for index, step in enumerate(guidance.steps, start=1):
            st.write(f"{index}. {step}")

    if guidance.official_links:
        st.markdown(f"**{strings['guided_links']}**")
        for link in guidance.official_links:
            title = link.title or link.url
            st.markdown(f"- [{title}]({link.url})")

    if guidance.confidence_note:
        st.caption(guidance.confidence_note)

    # Always show grounded sources (or the no-source warning) for ready answers.
    render_citations(citations or [], selected_language, warn_if_empty=True)


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
