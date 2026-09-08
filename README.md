# FormBridge

FormBridge is an AI-powered assistant that helps Arabic-speaking users understand official and administrative documents written mainly in Hebrew.

Upload a PDF, choose your preferred explanation language (Arabic or simple Hebrew), and receive a structured analysis with deadlines, required actions, missing information, and a practical action plan. You can also ask follow-up questions in a document-aware chat.

## Problem Statement

Official documents in Israel are often written in formal Hebrew. For many Arabic-speaking residents, understanding these documents quickly and accurately is difficult. Misreading a deadline, payment, or required document can lead to delays, fines, or missed opportunities.

FormBridge bridges this gap by combining PDF text extraction, OCR for scanned documents, and an AI agent that explains the document in clear language and organizes the information into actionable steps.

## Target Users

- Arabic-speaking residents navigating Israeli government or administrative paperwork
- Social workers, community organizers, and volunteers helping others with official documents
- Students and professionals demonstrating practical AI-assisted document understanding

## Main Features

- PDF upload with drag-and-drop support
- Automatic text extraction with OCR fallback for scanned PDFs
- Structured document analysis displayed in professional cards
- Explanation in **Arabic** or **simple Hebrew**
- Urgency indicators (low / medium / high)
- Numbered action plan and suggested formal Hebrew reply when relevant
- Document-aware follow-up chat
- Download analysis as TXT or Markdown
- Privacy-focused processing (document analyzed per session, not stored on server)
- RTL support for Arabic and Hebrew content

## Technology Stack

| Component | Technology |
|-----------|------------|
| UI | Streamlit |
| AI orchestration | CrewAI |
| Language model | Google Gemini (`gemini/gemini-3.6-flash`) |
| PDF text extraction | pypdf |
| OCR rendering | PyMuPDF (`pymupdf`) |
| OCR engine | Tesseract (Hebrew, Arabic, English) |
| Structured output | Pydantic |
| Configuration | python-dotenv |

## Architecture Overview

```text
User (Streamlit UI)
    │
    ├─ app.py              → session state, user flow, chat
    ├─ ui_components.py    → styling, cards, i18n strings
    │
    ├─ pdf_reader.py       → regular extraction → OCR fallback
    │
    ├─ agent.py            → CrewAI analysis + follow-up Q&A
    └─ models.py           → Pydantic schema + JSON parsing
```

**Flow:**

1. User uploads a PDF and selects a language.
2. `pdf_reader.py` extracts embedded text; if insufficient, it runs OCR.
3. `agent.py` sends the text to Gemini via CrewAI with strict security and accuracy rules.
4. The response is parsed into a `DocumentAnalysis` Pydantic model.
5. `ui_components.py` renders each field in separate cards.
6. Follow-up questions use the document text, structured analysis, and chat history.

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd FormBridge
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Tesseract OCR

FormBridge uses Tesseract for scanned PDFs. Hebrew, Arabic, and English language files are included in the local `tessdata/` folder.

**Windows:**

1. Download the installer from [UB Mannheim Tesseract builds](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install to the default location: `C:\Program Files\Tesseract-OCR\`
3. Optionally set a custom path:

```env
TESSERACT_CMD=C:\Path\To\tesseract.exe
```

**macOS:**

```bash
brew install tesseract
```

**Linux (Debian/Ubuntu):**

```bash
sudo apt update
sudo apt install tesseract-ocr
```

FormBridge detects Tesseract in this order:

1. `TESSERACT_CMD` environment variable
2. System `PATH` (`shutil.which`)
3. Standard Windows installation path

### 5. Configure Gemini API key

Copy the example environment file and add your key:

```bash
copy .env.example .env
```

Edit `.env`:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

Obtain a key from [Google AI Studio](https://aistudio.google.com/).

## How to Run

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`).

## Project Structure

```text
FormBridge/
├── app.py              # Main Streamlit application
├── agent.py            # CrewAI document analysis and chat
├── pdf_reader.py       # PDF extraction and OCR
├── models.py           # Pydantic analysis schema
├── ui_components.py    # UI styling, cards, i18n
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore
├── README.md
└── tessdata/           # OCR language files (heb, ara, eng)
```

## Security and Privacy Notes

- Uploaded documents are treated as **untrusted content**.
- AI prompts explicitly forbid following instructions inside documents.
- The API key is loaded from `.env` and never hardcoded.
- Do not commit `.env` or share your API key.
- FormBridge provides AI-generated explanations, not legal advice.

## Known Limitations

- OCR quality depends on scan resolution and document layout.
- Very long documents are truncated to a safe processing limit.
- Analysis accuracy depends on model availability and document clarity.
- Password-protected PDFs are not supported.
- Requires an active internet connection for Gemini API calls.

## Future Improvements

- Support for additional document formats (DOCX, images)
- User-selectable OCR language priority
- Persistent session export with chat history
- Multi-page document section navigation
- Offline mode with local models
- Accessibility audit and WCAG improvements

## Disclaimer

FormBridge provides an AI-generated explanation and does not replace legal or official professional advice. Always verify important dates, payments, and requirements with the issuing organization.
