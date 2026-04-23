# 📒 CoA Builder — Chart of Accounts for Ecommerce Marketplace

**Define, Map & Implement your Chart of Accounts — Built for Indian Ecommerce Marketplaces**

An intelligent LLM-powered Streamlit application that helps ecommerce marketplace businesses set up a complete, India-compliant Chart of Accounts — with workflow mapping, implementation tracking, and an AI assistant for accounting queries.

---

## 🔗 Demo Link

[CLICK HERE — Add Streamlit URL after deployment](#)

---

## ✨ Features

- **📊 Step 1: Account Numbering System** — Full CoA with 30+ accounts across 8 categories (100–899), color-coded by type, filterable, and downloadable as Excel/CSV
- **🔄 Step 2: Workflow Mapping** — Maps all 7 core transaction flows (Payment Capture, Commission, MDR, Payout, Refund, Chargeback, Reconciliation) to account codes with sample journal entries
- **✅ Step 3: Implementation Checklist** — 8-task go-live tracker with status dropdowns, progress bar, and Excel export
- **💡 Step 4: Best Practices** — 7 India-specific accounting best practices + GST/TDS compliance calendar
- **🤖 AI Assistant** — GPT-4o powered chat pre-loaded with full CoA context to answer journal entry, GST, TDS, and reconciliation questions
- **🏠 Business Setup** — Configurable business profile (Commission %, MDR rate, GST/TDS toggles) that personalises all steps and generates a live journal entry preview

---

## 🎯 Use Cases

- **Finance Teams** — Set up accounting structure before onboarding to QuickBooks / Xero / Tally / Zoho Books
- **Startup Founders** — Understand what accounts you need before hiring an accountant
- **Product Managers** — Map payment flows to accounting entries for reconciliation product design
- **Consultants** — Reference tool for CoA setup engagements with marketplace clients

---

## 🗂️ Account Structure (India Ecommerce)

| Range | Category | Key Accounts |
|-------|----------|--------------|
| 100–199 | Assets | 110 Bank, 120 A/R Buyers, 140 Escrow |
| 200–299 | Liabilities | 210 A/P Sellers, 215 GST Payable, 220 Refund Liability |
| 300–399 | Equity | 310 Owner Capital, 320 Retained Earnings |
| 400–499 | Revenue | 410 Gross Sales, 420 Commission Revenue |
| 500–599 | COGS | 510 MDR, 521 GST on MDR, 520 TDS |
| 600–699 | Operating Expenses | 610 Chargeback Losses, 611 Refund Fees |
| 700–799 | Taxes | 710 GST Output, 711 GST Input, 720 TDS Paid |
| 800–899 | Other/Contra | 810 Reconciliation Variance, 811 Suspense |

---

## 🔄 Transaction Workflow Coverage


---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API Key (for AI Assistant tab)

### Installation

```bash
git clone https://github.com/Ank576/coa-builder.git
cd coa-builder
pip install -r requirements.txt
```

### Run Locally

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

---

## 📁 File Structure

---

## 💡 How It Works

1. **Business Setup** — Enter your platform name, commission %, MDR rate, and toggle GST/TDS. See a live journal entry preview instantly.
2. **Account Numbering** — Browse the full 30+ account CoA, filter by category, and download as Excel or CSV.
3. **Workflow Mapping** — View all 7 transaction flows as a table. Select any process to see its sample journal entries with real account codes.
4. **Implementation Checklist** — Track your 8 go-live tasks with status updates and export progress to Excel.
5. **Best Practices** — Expandable cards covering fraud prevention, GST/TDS compliance calendar, reconciliation automation, and seller transparency.
6. **AI Assistant** — Chat with GPT-4o. The system prompt is pre-loaded with your full CoA and business config so it gives context-aware answers.

---

## 💬 Sample AI Assistant Questions

- *"Which accounts are debited and credited when a chargeback is filed?"*
- *"What is the journal entry for a ₹1,000 partial refund?"*
- *"How do I record GST on commission earned from sellers?"*
- *"Which account handles timing differences in daily reconciliation?"*
- *"Should TDS be deducted before or after commission?"*

---

## 🖥️ App Screenshots

> *(Add screenshots after deployment)*

| Page | Description |
|------|-------------|
| 🏠 Business Setup | Configure platform profile + live journal preview |
| 📊 Account Numbering | Color-coded CoA table with Excel download |
| 🔄 Workflow Mapping | Transaction flows + sample journal entries |
| ✅ Checklist | Progress tracker with status dropdowns |
| 🤖 AI Assistant | GPT-4o chat with CoA context |

---

## 🇮🇳 India-Specific Coverage

- **GST (18%)** on commission and MDR — accounts 215, 521, 710, 711
- **TDS (1%)** on seller payouts — accounts 216, 520, 720
- **GSTR-3B** monthly filing calendar (due 20th of next month)
- **TDS deposit** calendar (due 7th of next month)
- **Form 16A** annual TDS certificate for sellers

---

## 🤖 LLM Integration

Powered by **OpenAI GPT-4o** with a domain-specific system prompt that includes:
- Full account code index (100–899)
- India GST/TDS rules pre-loaded as context
- Business config (commission %, MDR rate) injected per session
- Last 10 chat messages maintained for conversation continuity

> Your API key is session-only and never stored or logged.

---

## ⚠️ Disclaimer

**For Reference and Educational Use** — This application provides a standard CoA template for Indian ecommerce marketplaces. It is not a substitute for advice from a qualified Chartered Accountant. Always validate your final account structure with your CA or finance team before going live.

---

## 📚 Resources

- [ICAI Chart of Accounts Guidelines](https://www.icai.org/)
- [GST Portal India](https://www.gst.gov.in/)
- [TDS Compliance — Income Tax India](https://www.incometaxindia.gov.in/)
- [Razorpay Settlement Docs](https://razorpay.com/docs/)
- [Xero India Accounting](https://www.xero.com/in/)

---

## 📝 License

MIT License — Free to use, modify, and distribute with attribution.

---

## 👤 Author

**Ankit Saxena** — Product Leader | LLMs & FinTech | Building intelligent systems at scale

[GitHub](https://github.com/Ank576) | [Portfolio](https://shorturl.at/6wMbi)
