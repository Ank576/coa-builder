import streamlit as st
import pandas as pd
from io import BytesIO
from openai import OpenAI

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CoA Builder — Ecommerce Marketplace",
    page_icon="📒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
COA_DATA = [
    # ASSETS
    {"Code": 110, "Account Name": "Bank Account - Primary",             "Category": "Assets",             "Type": "Current Asset",           "Statement": "Balance Sheet", "Description": "Main operating cash account",                  "Balance": "Debit"},
    {"Code": 111, "Account Name": "Bank Account - Settlement/Payouts",  "Category": "Assets",             "Type": "Current Asset",           "Statement": "Balance Sheet", "Description": "Dedicated seller payout account",              "Balance": "Debit"},
    {"Code": 120, "Account Name": "Accounts Receivable - Buyers",       "Category": "Assets",             "Type": "Current Asset",           "Statement": "Balance Sheet", "Description": "Money owed by buyers (prepaid orders)",        "Balance": "Debit"},
    {"Code": 121, "Account Name": "Accounts Receivable - Settlement",   "Category": "Assets",             "Type": "Current Asset",           "Statement": "Balance Sheet", "Description": "Settlement pending from payment gateway",      "Balance": "Debit"},
    {"Code": 140, "Account Name": "Held Funds (Escrow)",                "Category": "Assets",             "Type": "Current Asset",           "Statement": "Balance Sheet", "Description": "Disputed/held funds in transit",               "Balance": "Debit"},
    {"Code": 150, "Account Name": "Prepaid Expenses",                   "Category": "Assets",             "Type": "Current Asset",           "Statement": "Balance Sheet", "Description": "Pre-paid gateway fees & expenses",            "Balance": "Debit"},
    # LIABILITIES
    {"Code": 210, "Account Name": "Accounts Payable - Sellers",         "Category": "Liabilities",        "Type": "Current Liability",       "Statement": "Balance Sheet", "Description": "Money owed to sellers for delivered orders",   "Balance": "Credit"},
    {"Code": 211, "Account Name": "Accounts Payable - PG/Agencies",     "Category": "Liabilities",        "Type": "Current Liability",       "Statement": "Balance Sheet", "Description": "Settlement owed by payment gateway",           "Balance": "Credit"},
    {"Code": 215, "Account Name": "GST Payable (Output)",               "Category": "Liabilities",        "Type": "Current Liability",       "Statement": "Balance Sheet", "Description": "Tax liability on sales",                      "Balance": "Credit"},
    {"Code": 216, "Account Name": "TDS Payable",                        "Category": "Liabilities",        "Type": "Current Liability",       "Statement": "Balance Sheet", "Description": "Tax Deducted at Source",                      "Balance": "Credit"},
    {"Code": 220, "Account Name": "Refund Liability",                   "Category": "Liabilities",        "Type": "Current Liability",       "Statement": "Balance Sheet", "Description": "Refunds initiated but not yet processed",     "Balance": "Credit"},
    {"Code": 225, "Account Name": "Dispute Hold Liability",             "Category": "Liabilities",        "Type": "Current Liability",       "Statement": "Balance Sheet", "Description": "Chargebacks & dispute funds held",            "Balance": "Credit"},
    # EQUITY
    {"Code": 310, "Account Name": "Owner's Capital",                    "Category": "Equity",             "Type": "Equity",                  "Statement": "Balance Sheet", "Description": "Initial investment or retained earnings",      "Balance": "Credit"},
    {"Code": 320, "Account Name": "Retained Earnings",                  "Category": "Equity",             "Type": "Equity",                  "Statement": "Balance Sheet", "Description": "Prior year accumulated profits",              "Balance": "Credit"},
    # REVENUE
    {"Code": 410, "Account Name": "Gross Sales (Platform)",             "Category": "Revenue",            "Type": "Operating Revenue",       "Statement": "P&L",           "Description": "Total buyer payments received",               "Balance": "Credit"},
    {"Code": 411, "Account Name": "Gross Sales (Refunded)",             "Category": "Revenue",            "Type": "Contra Revenue",          "Statement": "P&L",           "Description": "Refund reversals (negative revenue)",         "Balance": "Debit"},
    {"Code": 420, "Account Name": "Commission Revenue (from Sellers)",  "Category": "Revenue",            "Type": "Operating Revenue",       "Statement": "P&L",           "Description": "Commission earned on orders",                 "Balance": "Credit"},
    {"Code": 421, "Account Name": "Commission Refunded",                "Category": "Revenue",            "Type": "Contra Revenue",          "Statement": "P&L",           "Description": "Commission reversed on returns",              "Balance": "Debit"},
    # COGS
    {"Code": 510, "Account Name": "MDR (Merchant Discount Rate)",       "Category": "COGS",               "Type": "Direct Cost",             "Statement": "P&L",           "Description": "Payment gateway processing fees",             "Balance": "Debit"},
    {"Code": 511, "Account Name": "PG Charges (Other)",                 "Category": "COGS",               "Type": "Direct Cost",             "Statement": "P&L",           "Description": "Additional gateway charges",                  "Balance": "Debit"},
    {"Code": 520, "Account Name": "TDS (Tax Deducted)",                 "Category": "COGS",               "Type": "Tax Expense",             "Statement": "P&L",           "Description": "Tax paid at source",                          "Balance": "Debit"},
    {"Code": 521, "Account Name": "GST on MDR",                         "Category": "COGS",               "Type": "Tax Expense",             "Statement": "P&L",           "Description": "GST charged on gateway fees",                 "Balance": "Debit"},
    # OPERATING EXPENSES
    {"Code": 610, "Account Name": "Chargeback Losses",                  "Category": "Operating Expenses", "Type": "Operating Expense",       "Statement": "P&L",           "Description": "Disputed/lost transactions",                  "Balance": "Debit"},
    {"Code": 611, "Account Name": "Refund Processing Fees",             "Category": "Operating Expenses", "Type": "Operating Expense",       "Statement": "P&L",           "Description": "Fees for refund reversals",                   "Balance": "Debit"},
    {"Code": 620, "Account Name": "Payment Processing (Manual)",        "Category": "Operating Expenses", "Type": "Operating Expense",       "Statement": "P&L",           "Description": "Staff costs for reconciliation",              "Balance": "Debit"},
    # TAXES
    {"Code": 710, "Account Name": "GST Output (Collected)",             "Category": "Taxes",              "Type": "Tax Liability",           "Statement": "P&L",           "Description": "Sales tax collected from customers",          "Balance": "Credit"},
    {"Code": 711, "Account Name": "GST Input (Paid)",                   "Category": "Taxes",              "Type": "Tax Credit",              "Statement": "P&L",           "Description": "Tax paid on expenses (input credit)",         "Balance": "Debit"},
    {"Code": 720, "Account Name": "TDS Paid",                           "Category": "Taxes",              "Type": "Tax Liability",           "Statement": "P&L",           "Description": "Tax deducted at source paid",                 "Balance": "Debit"},
    # OTHER
    {"Code": 810, "Account Name": "Reconciliation Variance",            "Category": "Other",              "Type": "Reconciliation",          "Statement": "P&L",           "Description": "Timing/rounding differences",                 "Balance": "Debit/Credit"},
    {"Code": 811, "Account Name": "Suspense Account",                   "Category": "Other",              "Type": "Temporary",               "Statement": "Balance Sheet", "Description": "Unmatched transactions (temp hold)",          "Balance": "Debit"},
]

NUMBERING_SYSTEM = [
    {"Range": "100–199", "Category": "Assets",             "Sub-Structure": "100s = Current Assets, 150+ = Fixed Assets",    "Example Accounts": "110 Bank, 120 A/R, 140 Escrow"},
    {"Range": "200–299", "Category": "Liabilities",        "Sub-Structure": "200s = Current Liabilities, 250+ = Long-term",  "Example Accounts": "210 A/P Sellers, 215 GST Payable, 220 Refunds"},
    {"Range": "300–399", "Category": "Equity",             "Sub-Structure": "Capital, retained earnings, distributions",     "Example Accounts": "310 Owner Capital, 320 Retained Earnings"},
    {"Range": "400–499", "Category": "Revenue",            "Sub-Structure": "Platform revenue + seller commissions",         "Example Accounts": "410 Gross Sales, 420 Commission, 411 Refunds"},
    {"Range": "500–599", "Category": "COGS",               "Sub-Structure": "Direct costs that scale with revenue",          "Example Accounts": "510 MDR, 520 TDS, 521 GST on MDR"},
    {"Range": "600–699", "Category": "Operating Expenses", "Sub-Structure": "Indirect costs, fixed or semi-variable",        "Example Accounts": "610 Chargebacks, 620 Processing"},
    {"Range": "700–799", "Category": "Taxes",              "Sub-Structure": "Tax accounts for compliance tracking",          "Example Accounts": "710 GST Output, 720 TDS Paid"},
    {"Range": "800–899", "Category": "Other/Contra",       "Sub-Structure": "Reconciliation, suspense, adjustments",         "Example Accounts": "810 Variance, 811 Suspense"},
]

WORKFLOW_DATA = [
    {"Process Flow": "Payment Capture",      "Accounts Involved": "110, 120, 410",        "Journal Entry Type": "Debit Bank, Credit A/R, Credit Sales", "Frequency": "Per transaction"},
    {"Process Flow": "Commission Accrual",   "Accounts Involved": "120, 420",             "Journal Entry Type": "Debit A/R, Credit Commission Revenue",  "Frequency": "Per transaction"},
    {"Process Flow": "MDR & Taxes",          "Accounts Involved": "510, 521, 215, 720",   "Journal Entry Type": "Debit Expenses, Credit A/R/Payables",   "Frequency": "Per transaction"},
    {"Process Flow": "Seller Payout",        "Accounts Involved": "210, 111",             "Journal Entry Type": "Debit A/P, Credit Bank Payout",         "Frequency": "Daily batch"},
    {"Process Flow": "Refunds",              "Accounts Involved": "220, 411, 421",        "Journal Entry Type": "Debit Liability, Credit Sales & Comm",  "Frequency": "Per refund"},
    {"Process Flow": "Chargebacks",          "Accounts Involved": "225, 610, 111",        "Journal Entry Type": "Debit Dispute Hold, Credit Bank",       "Frequency": "Per dispute"},
    {"Process Flow": "Daily Reconciliation", "Accounts Involved": "810, 811",             "Journal Entry Type": "Post reconciliation variance entries",  "Frequency": "Daily"},
]

CHECKLIST_DATA = [
    {"#": 1, "Task": "Create all 30+ accounts in accounting software",    "Owner": "Finance",  "Timeline": "Day 1",   "Status": "Pending", "Notes": "Map to QuickBooks / Xero / Tally"},
    {"#": 2, "Task": "Configure account hierarchies and parent accounts", "Owner": "Finance",  "Timeline": "Day 1",   "Status": "Pending", "Notes": "Set up consolidation rules"},
    {"#": 3, "Task": "Set up PG API integration for auto-posting",        "Owner": "Tech",     "Timeline": "Day 2–3", "Status": "Pending", "Notes": "Auto-post payment entries"},
    {"#": 4, "Task": "Build daily reconciliation batch process",          "Owner": "Tech",     "Timeline": "Day 3–5", "Status": "Pending", "Notes": "Automate 3-way match"},
    {"#": 5, "Task": "Configure seller payout ledger reporting",          "Owner": "Finance",  "Timeline": "Day 5",   "Status": "Pending", "Notes": "Dashboard for sellers"},
    {"#": 6, "Task": "Train finance team on manual exception handling",   "Owner": "Finance",  "Timeline": "Day 6",   "Status": "Pending", "Notes": "Workshops and SOPs"},
    {"#": 7, "Task": "Soft launch with 10 test transactions",             "Owner": "Tech",     "Timeline": "Day 7",   "Status": "Pending", "Notes": "Verify all entries post correctly"},
    {"#": 8, "Task": "Go live with full reconciliation system",           "Owner": "All",      "Timeline": "Day 8",   "Status": "Pending", "Notes": "Monitor for 48hrs post go-live"},
]

BEST_PRACTICES = [
    {
        "title": "🔢 Unique Account Numbers",
        "why": "Prevents errors, confusion, and duplicate entries in the ledger.",
        "how": "Never reuse retired account numbers. Keep a retired accounts log with reason and date."
    },
    {
        "title": "📝 Clear Narratives on Every Entry",
        "why": "Enables audit trail and speeds up dispute resolution.",
        "how": "Always reference Order ID, Refund ID, or Chargeback ID in the entry description."
    },
    {
        "title": "🔒 Segregation of Duties",
        "why": "Fraud prevention — no single person controls full payment cycle.",
        "how": "Finance posts entries → Tech extracts data → Auditor reviews → Management approves."
    },
    {
        "title": "🤖 Automated Reconciliation",
        "why": "Reduces manual errors, catches timing differences early.",
        "how": "API integration between Payment Gateway, Bank, and Internal DB for 3-way match."
    },
    {
        "title": "📂 Dispute Evidence Retention",
        "why": "Legal compliance — chargebacks require documented evidence.",
        "how": "Store all chargeback docs (screenshots, delivery proof, comms) for minimum 3 years."
    },
    {
        "title": "📅 Tax Compliance Calendar",
        "why": "Avoid penalties for late GST/TDS filings (India).",
        "how": "GSTR-3B due 20th of each month. TDS deposit by 7th. Set automated reminders 2 weeks early."
    },
    {
        "title": "📊 Seller Transparency Dashboard",
        "why": "Builds trust, reduces disputes and seller churn.",
        "how": "Weekly email/dashboard showing gross order value, commission deducted, TDS, and net payout."
    },
]

CATEGORY_COLORS = {
    "Assets":             "#1f77b4",
    "Liabilities":        "#d62728",
    "Equity":             "#9467bd",
    "Revenue":            "#2ca02c",
    "COGS":               "#ff7f0e",
    "Operating Expenses": "#8c564b",
    "Taxes":              "#e377c2",
    "Other":              "#7f7f7f",
}

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def to_excel(df: pd.DataFrame) -> bytes:
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
        ws = writer.sheets["Sheet1"]
        for i, col in enumerate(df.columns):
            ws.set_column(i, i, max(len(col) + 4, df[col].astype(str).map(len).max() + 2))
    return buf.getvalue()


def color_row(row):
    color = CATEGORY_COLORS.get(row["Category"], "#ffffff")
    return [f"background-color: {color}18; color: {color}" if col == "Category"
            else "" for col in row.index]


def get_llm_response(messages: list, api_key: str) -> str:
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.4,
            max_tokens=800,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"


SYSTEM_PROMPT = """You are a senior chartered accountant and fintech product expert specializing in 
Indian ecommerce marketplace accounting. You have deep expertise in:
- Chart of Accounts (CoA) design for online marketplaces
- India-specific taxes: GST (18%), TDS (1% on seller payouts), MDR on payment gateways
- Journal entry patterns for: payment capture, commission accrual, seller payouts, refunds, chargebacks
- Reconciliation best practices and automation
- Accounting software setup (QuickBooks, Xero, Tally, Zoho Books)

The app uses these account codes:
ASSETS (100-199): 110 Bank-Primary, 111 Bank-Payout, 120 A/R Buyers, 121 A/R Settlement, 140 Held Funds, 150 Prepaid
LIABILITIES (200-299): 210 A/P Sellers, 211 A/P PG, 215 GST Payable, 216 TDS Payable, 220 Refund Liability, 225 Dispute Hold
EQUITY (300-399): 310 Owner Capital, 320 Retained Earnings
REVENUE (400-499): 410 Gross Sales, 411 Sales Refunded, 420 Commission, 421 Commission Refunded
COGS (500-599): 510 MDR, 511 PG Charges, 520 TDS Deducted, 521 GST on MDR
OPERATING EXPENSES (600-699): 610 Chargeback Losses, 611 Refund Processing Fees, 620 Manual Processing
TAXES (700-799): 710 GST Output, 711 GST Input, 720 TDS Paid
OTHER (800-899): 810 Reconciliation Variance, 811 Suspense

Answer concisely and always reference account codes (e.g., Dr 110, Cr 420) when explaining journal entries.
Keep answers practical and India-specific."""

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "checklist" not in st.session_state:
    st.session_state.checklist = [dict(row) for row in CHECKLIST_DATA]
if "business_name" not in st.session_state:
    st.session_state.business_name = ""
if "commission_pct" not in st.session_state:
    st.session_state.commission_pct = 10
if "gst_registered" not in st.session_state:
    st.session_state.gst_registered = True
if "tds_applicable" not in st.session_state:
    st.session_state.tds_applicable = True

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📒 CoA Builder")
    st.markdown("*Ecommerce Marketplace · India*")
    st.divider()

    page = st.radio(
        "Navigate",
        ["🏠 Business Setup",
         "📊 Step 1: Account Numbering",
         "🔄 Step 2: Workflow Mapping",
         "✅ Step 3: Implementation Checklist",
         "💡 Step 4: Best Practices",
         "🤖 AI Assistant"],
        label_visibility="collapsed"
    )

    st.divider()
    st.caption("Business Config")
    if st.session_state.business_name:
        st.success(f"**{st.session_state.business_name}**")
        st.caption(f"Commission: {st.session_state.commission_pct}%  |  "
                   f"GST: {'✅' if st.session_state.gst_registered else '❌'}  |  "
                   f"TDS: {'✅' if st.session_state.tds_applicable else '❌'}")
    else:
        st.warning("⚠️ Complete Business Setup first")

# ─────────────────────────────────────────────
# PAGE: BUSINESS SETUP
# ─────────────────────────────────────────────
if page == "🏠 Business Setup":
    st.title("🏠 Business Setup")
    st.markdown("Configure your marketplace profile. This personalizes your CoA and workflow.")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        biz_name = st.text_input("Business / Platform Name", value=st.session_state.business_name,
                                  placeholder="e.g., ShopEasy Marketplace")
        platform_type = st.selectbox("Platform Type",
                                      ["B2C Marketplace", "B2B Marketplace", "D2C + Marketplace", "Hyperlocal"])
        commission_pct = st.slider("Commission % on Orders", min_value=1, max_value=30,
                                    value=st.session_state.commission_pct, step=1)
    with col2:
        pg_used = st.multiselect("Payment Gateways Used",
                                  ["Razorpay", "PayU", "Cashfree", "PayTM", "CCAvenue", "Stripe"],
                                  default=["Razorpay"])
        gst_registered = st.toggle("GST Registered", value=st.session_state.gst_registered)
        tds_applicable = st.toggle("TDS Applicable (seller payouts)", value=st.session_state.tds_applicable)
        mdr_rate = st.number_input("MDR Rate (%)", min_value=0.5, max_value=5.0, value=2.0, step=0.1)

    st.divider()
    if st.button("💾 Save Configuration", type="primary", use_container_width=True):
        if not biz_name.strip():
            st.error("Please enter a business name.")
        else:
            st.session_state.business_name = biz_name
            st.session_state.commission_pct = commission_pct
            st.session_state.gst_registered = gst_registered
            st.session_state.tds_applicable = tds_applicable
            st.session_state.mdr_rate = mdr_rate
            st.session_state.pg_used = pg_used
            st.success(f"✅ Configuration saved for **{biz_name}**! Navigate using the sidebar.")

    # Quick example
    st.divider()
    st.markdown("### 💡 Sample Journal Entry Preview")
    st.markdown(f"*Based on a ₹1,000 order with {commission_pct}% commission:*")
    comm = 1000 * commission_pct / 100
    mdr_amt = round(1000 * mdr_rate / 100, 2)
    gst_on_mdr = round(mdr_amt * 0.18, 2) if gst_registered else 0
    tds_amt = round((1000 - comm) * 0.01, 2) if tds_applicable else 0
    net_payout = round(1000 - comm - tds_amt, 2)

    preview = pd.DataFrame([
        {"Step": "Payment Captured",   "Debit": f"110 Bank  ₹1,000",     "Credit": f"120 A/R  ₹1,000"},
        {"Step": "Commission Accrued", "Debit": f"120 A/R  ₹{comm}",     "Credit": f"420 Commission  ₹{comm}"},
        {"Step": "MDR Posted",         "Debit": f"510 MDR  ₹{mdr_amt}",  "Credit": f"120 A/R  ₹{mdr_amt}"},
        {"Step": "GST on MDR",         "Debit": f"521 GST-MDR  ₹{gst_on_mdr}", "Credit": f"120 A/R  ₹{gst_on_mdr}"},
        {"Step": "TDS Deducted",       "Debit": f"720 TDS  ₹{tds_amt}",  "Credit": f"120 A/R  ₹{tds_amt}"},
        {"Step": "Seller Payout",      "Debit": f"210 A/P  ₹{net_payout}", "Credit": f"111 Bank-Payout  ₹{net_payout}"},
    ])
    st.dataframe(preview, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# PAGE: STEP 1 — ACCOUNT NUMBERING
# ─────────────────────────────────────────────
elif page == "📊 Step 1: Account Numbering":
    st.title("📊 Step 1: Account Numbering System")
    st.markdown("Standard CoA structure for an **Indian Ecommerce Marketplace** — 100-series to 800-series.")
    st.divider()

    # Numbering overview
    st.subheader("🗂️ Number Range Guide")
    num_df = pd.DataFrame(NUMBERING_SYSTEM)
    st.dataframe(num_df, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("📋 Full Chart of Accounts")

    # Filter
    coa_df = pd.DataFrame(COA_DATA)
    categories = ["All"] + sorted(coa_df["Category"].unique().tolist())
    selected_cat = st.selectbox("Filter by Category", categories)

    if selected_cat != "All":
        filtered_df = coa_df[coa_df["Category"] == selected_cat].reset_index(drop=True)
    else:
        filtered_df = coa_df.copy()

    st.dataframe(
        filtered_df.style.apply(color_row, axis=1),
        use_container_width=True,
        hide_index=True,
        height=500
    )

    st.caption(f"Showing {len(filtered_df)} of {len(coa_df)} accounts")

    # Download
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        excel_bytes = to_excel(coa_df)
        st.download_button(
            label="⬇️ Download Full CoA (Excel)",
            data=excel_bytes,
            file_name=f"chart_of_accounts_{st.session_state.business_name or 'ecommerce'}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            type="primary"
        )
    with col2:
        csv_bytes = coa_df.to_csv(index=False).encode()
        st.download_button(
            label="⬇️ Download Full CoA (CSV)",
            data=csv_bytes,
            file_name="chart_of_accounts.csv",
            mime="text/csv",
            use_container_width=True
        )

# ─────────────────────────────────────────────
# PAGE: STEP 2 — WORKFLOW MAPPING
# ─────────────────────────────────────────────
elif page == "🔄 Step 2: Workflow Mapping":
    st.title("🔄 Step 2: Workflow Mapping")
    st.markdown("Maps each business process to the accounts it touches and the journal entry type.")
    st.divider()

    # Config context
    if st.session_state.business_name:
        st.info(f"📌 Configured for **{st.session_state.business_name}** · "
                f"Commission: **{st.session_state.commission_pct}%** · "
                f"GST: **{'On' if st.session_state.gst_registered else 'Off'}** · "
                f"TDS: **{'On' if st.session_state.tds_applicable else 'Off'}**")

    wf_df = pd.DataFrame(WORKFLOW_DATA)

    # Grey out TDS row if not applicable
    if not st.session_state.tds_applicable:
        st.warning("⚠️ TDS is disabled in your config — TDS rows are informational only.")

    st.subheader("📋 Workflow Table")
    st.dataframe(wf_df, use_container_width=True, hide_index=True, height=320)

    st.divider()
    st.subheader("🔍 Process Deep-Dive")

    process = st.selectbox("Select a process to explore", [r["Process Flow"] for r in WORKFLOW_DATA])
    selected = next(r for r in WORKFLOW_DATA if r["Process Flow"] == process)

    col1, col2, col3 = st.columns(3)
    col1.metric("Accounts Involved", selected["Accounts Involved"])
    col2.metric("Entry Type", selected["Journal Entry Type"].split(",")[0] + "...")
    col3.metric("Frequency", selected["Frequency"])

    # Sample entry detail
    sample_entries = {
        "Payment Capture":      [("Dr 120 A/R Settlement", "₹1,000"), ("Cr 410 Gross Sales", "₹1,000"),
                                  ("Dr 110 Bank Account", "₹1,000"), ("Cr 120 A/R Settlement", "₹1,000")],
        "Commission Accrual":   [("Dr 120 A/R Settlement", f"₹{st.session_state.commission_pct*10}"),
                                  ("Cr 420 Commission Revenue", f"₹{st.session_state.commission_pct*10}")],
        "MDR & Taxes":          [("Dr 510 MDR Expense", "₹20"), ("Cr 120 A/R", "₹20"),
                                  ("Dr 521 GST on MDR", "₹3.60"), ("Cr 120 A/R", "₹3.60")],
        "Seller Payout":        [("Dr 210 A/P Sellers", "₹891"), ("Cr 111 Bank-Payout", "₹891")],
        "Refunds":              [("Dr 220 Refund Liability", "₹1,000"), ("Cr 411 Sales Refunded", "₹1,000"),
                                  ("Dr 421 Commission Refunded", "₹100"), ("Cr 420 Commission", "₹100")],
        "Chargebacks":          [("Dr 225 Dispute Hold", "₹1,000"), ("Cr 110 Bank", "₹1,000"),
                                  ("Dr 610 Chargeback Loss", "₹15"), ("Cr 110 Bank", "₹15")],
        "Daily Reconciliation": [("Dr/Cr 810 Variance", "± difference"), ("Dr/Cr 811 Suspense", "timing diff")],
    }

    if process in sample_entries:
        st.markdown("**Sample Journal Entries:**")
        entries = sample_entries[process]
        entry_df = pd.DataFrame(entries, columns=["Account", "Amount"])
        st.dataframe(entry_df, use_container_width=True, hide_index=True)

    st.divider()
    excel_bytes = to_excel(wf_df)
    st.download_button(
        label="⬇️ Download Workflow Mapping (Excel)",
        data=excel_bytes,
        file_name="workflow_mapping.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary"
    )

# ─────────────────────────────────────────────
# PAGE: STEP 3 — IMPLEMENTATION CHECKLIST
# ─────────────────────────────────────────────
elif page == "✅ Step 3: Implementation Checklist":
    st.title("✅ Step 3: Implementation Checklist")
    st.markdown("Track your CoA go-live tasks. Mark items complete as you progress.")
    st.divider()

    # Progress
    completed = sum(1 for row in st.session_state.checklist if row["Status"] == "Done ✅")
    total = len(st.session_state.checklist)
    st.progress(completed / total, text=f"**{completed} of {total} tasks complete**")
    st.divider()

    status_options = ["Pending", "In Progress 🔄", "Done ✅", "Blocked ❌"]

    for i, task in enumerate(st.session_state.checklist):
        with st.container():
            col1, col2, col3, col4 = st.columns([0.5, 4, 2, 2])
            col1.markdown(f"**#{task['#']}**")
            col2.markdown(f"**{task['Task']}**  \n`{task['Owner']}` · {task['Timeline']}")
            new_status = col3.selectbox(
                "Status", status_options,
                index=status_options.index(task["Status"]) if task["Status"] in status_options else 0,
                key=f"status_{i}",
                label_visibility="collapsed"
            )
            col4.caption(task["Notes"])
            st.session_state.checklist[i]["Status"] = new_status
        st.divider()

    # Download
    checklist_df = pd.DataFrame(st.session_state.checklist)
    excel_bytes = to_excel(checklist_df)
    st.download_button(
        label="⬇️ Download Checklist (Excel)",
        data=excel_bytes,
        file_name=f"implementation_checklist_{st.session_state.business_name or 'ecommerce'}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
        use_container_width=True
    )

# ─────────────────────────────────────────────
# PAGE: STEP 4 — BEST PRACTICES
# ─────────────────────────────────────────────
elif page == "💡 Step 4: Best Practices":
    st.title("💡 Step 4: Best Practices")
    st.markdown("India-specific accounting best practices for ecommerce marketplace operators.")
    st.divider()

    for bp in BEST_PRACTICES:
        with st.expander(bp["title"], expanded=False):
            col1, col2 = st.columns(2)
            col1.markdown(f"**Why it matters**  \n{bp['why']}")
            col2.markdown(f"**How to implement**  \n{bp['how']}")

    st.divider()
    st.subheader("📅 India Tax Compliance Calendar")
    tax_cal = pd.DataFrame([
        {"Filing": "GSTR-3B (GST Return)",        "Frequency": "Monthly",   "Due Date": "20th of next month",     "Account": "710 GST Output"},
        {"Filing": "TDS Deposit to Government",    "Frequency": "Monthly",   "Due Date": "7th of next month",      "Account": "720 TDS Paid"},
        {"Filing": "GST Input Credit Recon",       "Frequency": "Monthly",   "Due Date": "Ongoing",                "Account": "711 GST Input"},
        {"Filing": "Seller TDS Certificates 16A",  "Frequency": "Annual",    "Due Date": "30th June",              "Account": "216 TDS Payable"},
        {"Filing": "Annual Tax Audit",             "Frequency": "Annual",    "Due Date": "31st May",               "Account": "All"},
        {"Filing": "GSTR-9 Annual Return",         "Frequency": "Annual",    "Due Date": "31st December",          "Account": "710, 711"},
    ])
    st.dataframe(tax_cal, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# PAGE: AI ASSISTANT
# ─────────────────────────────────────────────
elif page == "🤖 AI Assistant":
    st.title("🤖 AI Assistant")
    st.markdown("Ask anything about Chart of Accounts, journal entries, GST/TDS, or reconciliation.")
    st.divider()

    # API Key input
    api_key = st.text_input(
        "🔑 OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="Your key is never stored. It stays in this session only."
    )

    if not api_key:
        st.info("👆 Enter your OpenAI API key above to enable the AI assistant.")
        st.markdown("**Example questions you can ask:**")
        examples = [
            "Which accounts are debited and credited when a chargeback is filed?",
            "How do I record GST on commission earned from sellers?",
            "What is the journal entry for a partial refund of ₹500?",
            "Which account should I use for timing differences in reconciliation?",
            "How should I handle TDS if I have both Indian and foreign sellers?",
        ]
        for ex in examples:
            st.markdown(f"- *{ex}*")
    else:
        # Chat display
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Input
        if prompt := st.chat_input("Ask about CoA, journal entries, GST, TDS, reconciliation..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Build messages
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]

            # Add business context if configured
            if st.session_state.business_name:
                context = (f"\n\nUser's business: {st.session_state.business_name} | "
                           f"Commission: {st.session_state.commission_pct}% | "
                           f"GST Registered: {st.session_state.gst_registered} | "
                           f"TDS Applicable: {st.session_state.tds_applicable}")
                messages[0]["content"] += context

            messages += [{"role": m["role"], "content": m["content"]}
                         for m in st.session_state.chat_history[-10:]]

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    reply = get_llm_response(messages, api_key)
                st.markdown(reply)

            st.session_state.chat_history.append({"role": "assistant", "content": reply})

        # Clear chat
        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat History"):
                st.session_state.chat_history = []
                st.rerun()
