"""
Supermarket Sales Analysis Dashboard
=====================================
A Streamlit-based data analytics app covering:
  1. Data loading & inspection
  2. Data quality checks (missing / incorrect values)
  3. Sales validation  (Quantity × Unit Price)
  4. Grouped summaries (totals, counts, averages)
  5. Interactive charts
  6. Business insights & recommendations
"""

import io
import warnings

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# Page configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Supermarket Sales Analysis",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS — clean, readable, professional
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
        /* Main background */
        .main { background-color: #f7f8fa; }

        /* Metric card style */
        div[data-testid="metric-container"] {
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            padding: 16px 20px;
        }

        /* Section headers */
        h2 { color: #1f2328; border-bottom: 2px solid #3b82d4; padding-bottom: 4px; }
        h3 { color: #3b82d4; }

        /* Sidebar */
        section[data-testid="stSidebar"] { background-color: #1f2328; color: #ffffff; }
        section[data-testid="stSidebar"] .css-1d391kg { color: #ffffff; }

        /* Table */
        .stDataFrame { border: 1px solid #e5e7eb; border-radius: 8px; }

        /* Alert boxes */
        .insight-box {
            background-color: #eff6ff;
            border-left: 5px solid #3b82d4;
            padding: 14px 18px;
            border-radius: 6px;
            margin: 8px 0;
        }
        .warning-box {
            background-color: #fffbeb;
            border-left: 5px solid #f59e0b;
            padding: 14px 18px;
            border-radius: 6px;
            margin: 8px 0;
        }
        .success-box {
            background-color: #f0fdf4;
            border-left: 5px solid #22c55e;
            padding: 14px 18px;
            border-radius: 6px;
            margin: 8px 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# Helper utilities
# ─────────────────────────────────────────────
PALETTE = px.colors.qualitative.Set2

def fmt_inr(val: float) -> str:
    """Format a number as Indian Rupees with commas."""
    return f"₹{val:,.2f}"

def section(title: str, icon: str = "") -> None:
    st.markdown(f"## {icon} {title}")

def insight(text: str) -> None:
    st.markdown(f'<div class="insight-box">💡 {text}</div>', unsafe_allow_html=True)

def warn_box(text: str) -> None:
    st.markdown(f'<div class="warning-box">⚠️ {text}</div>', unsafe_allow_html=True)

def ok_box(text: str) -> None:
    st.markdown(f'<div class="success-box">✅ {text}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 1. Data Loading
# ─────────────────────────────────────────────
@st.cache_data(show_spinner="Loading dataset…")
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["DayOfWeek"] = df["Date"].dt.day_name()
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Unit Price"] = pd.to_numeric(df["Unit Price"], errors="coerce")
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    # Recalculate Sales to guarantee accuracy
    df["Calculated Sales"] = df["Quantity"] * df["Unit Price"]
    return df


df_raw = load_data("supermarket_sales_10500_rows.csv")


# ─────────────────────────────────────────────
# Sidebar — global filters
# ─────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://img.icons8.com/color/96/000000/shopping-cart--v2.png",
        width=72,
    )
    st.title("🛒 SuperMart Analytics")
    st.markdown("---")

    st.subheader("🔍 Filters")

    all_branches = sorted(df_raw["Branch"].dropna().unique())
    sel_branches = st.multiselect("Branch", all_branches, default=all_branches)

    all_cities = sorted(df_raw["City"].dropna().unique())
    sel_cities = st.multiselect("City", all_cities, default=all_cities)

    all_cats = sorted(df_raw["Category"].dropna().unique())
    sel_cats = st.multiselect("Category", all_cats, default=all_cats)

    all_pay = sorted(df_raw["Payment"].dropna().unique())
    sel_pay = st.multiselect("Payment Method", all_pay, default=all_pay)

    cust_types = sorted(df_raw["Customer Type"].dropna().unique())
    sel_cust = st.multiselect("Customer Type", cust_types, default=cust_types)

    st.markdown("---")
    st.caption("Data: supermarket_sales_500_rows.csv")

# Apply filters
df = df_raw[
    df_raw["Branch"].isin(sel_branches)
    & df_raw["City"].isin(sel_cities)
    & df_raw["Category"].isin(sel_cats)
    & df_raw["Payment"].isin(sel_pay)
    & df_raw["Customer Type"].isin(sel_cust)
].copy()


# ─────────────────────────────────────────────
# Tab layout
# ─────────────────────────────────────────────
tabs = st.tabs([
    "📋 Overview",
    "🔎 Data Quality",
    "💰 Sales Analysis",
    "📊 Charts",
    "🏆 Business Insights",
])


# ══════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════
with tabs[0]:
    st.markdown("# 🛒 Supermarket Sales Analysis Dashboard")
    st.markdown(
        "An end-to-end analytics view of supermarket transactions — "
        "from raw data inspection to actionable business recommendations."
    )
    st.markdown("---")

    # KPI row
    total_sales = df["Calculated Sales"].sum()
    total_txns = len(df)
    avg_order = df["Calculated Sales"].mean()
    avg_rating = df["Rating"].mean()
    total_qty = df["Quantity"].sum()
    top_cat = df.groupby("Category")["Calculated Sales"].sum().idxmax() if not df.empty else "N/A"

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("💵 Total Sales", fmt_inr(total_sales))
    k2.metric("🧾 Transactions", f"{total_txns:,}")
    k3.metric("🛍️ Avg Order Value", fmt_inr(avg_order))
    k4.metric("⭐ Avg Rating", f"{avg_rating:.2f} / 5")
    k5.metric("📦 Units Sold", f"{int(total_qty):,}")
    k6.metric("🥇 Top Category", top_cat)

    st.markdown("---")

    # Raw data preview
    section("Dataset Preview", "📄")
    st.markdown(
        f"Showing **{len(df):,} rows** × **{len(df.columns)} columns** "
        f"(after filters). Scroll right to see all columns."
    )
    st.dataframe(df.drop(columns=["Month", "DayOfWeek"]).head(20), use_container_width=True)

    # Column descriptions
    with st.expander("📖 Column Descriptions"):
        col_desc = pd.DataFrame(
            {
                "Column": [
                    "Invoice ID", "Date", "Branch", "City", "Customer Type",
                    "Gender", "Product", "Category", "Quantity", "Unit Price",
                    "Payment", "Rating", "Sales", "Calculated Sales",
                ],
                "Description": [
                    "Unique transaction identifier",
                    "Date of purchase",
                    "Store branch (A / B / C)",
                    "City where branch is located",
                    "Member or Normal customer",
                    "Customer gender",
                    "Name of the product purchased",
                    "Product category",
                    "Number of units bought",
                    "Price per unit (₹)",
                    "Payment method used",
                    "Customer satisfaction score (1–5)",
                    "Sales value in the original CSV",
                    "Re-computed as Quantity × Unit Price",
                ],
                "Data Type": [
                    "String", "Date", "String", "String", "String",
                    "String", "String", "String", "Integer", "Float",
                    "String", "Float", "Float", "Float",
                ],
            }
        )
        st.dataframe(col_desc, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════
# TAB 2 — DATA QUALITY
# ══════════════════════════════════════════════
with tabs[1]:
    section("Data Quality Report", "🔎")

    # ── Missing values ──────────────────────────
    st.subheader("Missing Values")
    missing = df_raw.isnull().sum().reset_index()
    missing.columns = ["Column", "Missing Count"]
    missing["Missing %"] = (missing["Missing Count"] / len(df_raw) * 100).round(2)
    missing["Status"] = missing["Missing Count"].apply(
        lambda x: "✅ Clean" if x == 0 else "⚠️ Has nulls"
    )
    st.dataframe(missing, use_container_width=True, hide_index=True)

    total_missing = missing["Missing Count"].sum()
    if total_missing == 0:
        ok_box("No missing values found in the entire dataset.")
    else:
        warn_box(f"{total_missing} missing value(s) detected. See table above.")

    st.markdown("---")

    # ── Duplicate rows ──────────────────────────
    st.subheader("Duplicate Rows")
    dupes = df_raw.duplicated().sum()
    if dupes == 0:
        ok_box(f"No duplicate rows found. Dataset has {len(df_raw):,} unique records.")
    else:
        warn_box(f"{dupes} duplicate row(s) found.")

    st.markdown("---")

    # ── Data type summary ───────────────────────
    st.subheader("Column Data Types & Sample Values")
    dtype_df = pd.DataFrame(
        {
            "Column": df_raw.columns,
            "Dtype": df_raw.dtypes.astype(str).values,
            "Non-Null Count": df_raw.count().values,
            "Unique Values": [df_raw[c].nunique() for c in df_raw.columns],
            "Sample": [str(df_raw[c].dropna().iloc[0]) if not df_raw[c].dropna().empty else "—" for c in df_raw.columns],
        }
    )
    st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Numeric range validation ────────────────
    st.subheader("Numeric Range Checks")
    checks = []

    neg_qty = (df_raw["Quantity"] <= 0).sum()
    checks.append({
        "Check": "Quantity > 0",
        "Issue Count": int(neg_qty),
        "Status": "✅ Pass" if neg_qty == 0 else "❌ Fail",
    })

    neg_price = (df_raw["Unit Price"] <= 0).sum()
    checks.append({
        "Check": "Unit Price > 0",
        "Issue Count": int(neg_price),
        "Status": "✅ Pass" if neg_price == 0 else "❌ Fail",
    })

    bad_rating = ((df_raw["Rating"] < 1) | (df_raw["Rating"] > 5)).sum()
    checks.append({
        "Check": "Rating between 1 and 5",
        "Issue Count": int(bad_rating),
        "Status": "✅ Pass" if bad_rating == 0 else "❌ Fail",
    })

    # Sales vs Calculated mismatch
    df_raw["_diff"] = (df_raw["Sales"] - df_raw["Calculated Sales"]).abs()
    mismatch = (df_raw["_diff"] > 0.01).sum()
    checks.append({
        "Check": "Sales ≈ Quantity × Unit Price",
        "Issue Count": int(mismatch),
        "Status": "✅ Pass" if mismatch == 0 else "⚠️ Mismatch",
    })

    st.dataframe(pd.DataFrame(checks), use_container_width=True, hide_index=True)

    if mismatch > 0:
        warn_box(
            f"{mismatch} row(s) have a discrepancy between the original 'Sales' column "
            "and the re-computed Quantity × Unit Price. The dashboard uses the "
            "**Calculated Sales** column for all analysis."
        )
    else:
        ok_box("Sales column is perfectly consistent with Quantity × Unit Price.")

    st.markdown("---")

    # ── Statistical summary ─────────────────────
    st.subheader("Descriptive Statistics (Numeric Columns)")
    numeric_cols = ["Quantity", "Unit Price", "Rating", "Sales", "Calculated Sales"]
    st.dataframe(
        df_raw[numeric_cols].describe().T.rename(columns={"50%": "median"}).round(2),
        use_container_width=True,
    )


# ══════════════════════════════════════════════
# TAB 3 — SALES ANALYSIS
# ══════════════════════════════════════════════
with tabs[2]:
    section("Sales Analysis", "💰")

    # ── Sales Calculation Explained ─────────────
    with st.expander("📐 How Sales is Calculated", expanded=True):
        st.markdown(
            """
            **Sales Formula:**

            ```
            Sales = Quantity × Unit Price
            ```

            Every transaction's revenue is re-validated by multiplying the number of units
            purchased by the price per unit. This ensures accuracy regardless of any
            data-entry errors in the original CSV's `Sales` column.
            """
        )
        sample = df[["Invoice ID", "Quantity", "Unit Price", "Sales", "Calculated Sales"]].head(8)
        st.dataframe(sample, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── By Branch ──────────────────────────────
    st.subheader("Sales by Branch")
    branch_df = (
        df.groupby("Branch")
        .agg(
            Total_Sales=("Calculated Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Order=("Calculated Sales", "mean"),
            Total_Qty=("Quantity", "sum"),
            Avg_Rating=("Rating", "mean"),
        )
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )
    branch_df.columns = ["Branch", "Total Sales (₹)", "Transactions", "Avg Order (₹)", "Units Sold", "Avg Rating"]
    branch_df["Total Sales (₹)"] = branch_df["Total Sales (₹)"].round(2)
    branch_df["Avg Order (₹)"] = branch_df["Avg Order (₹)"].round(2)
    branch_df["Avg Rating"] = branch_df["Avg Rating"].round(2)
    st.dataframe(branch_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── By Category ────────────────────────────
    st.subheader("Sales by Category")
    cat_df = (
        df.groupby("Category")
        .agg(
            Total_Sales=("Calculated Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Order=("Calculated Sales", "mean"),
            Total_Qty=("Quantity", "sum"),
        )
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )
    cat_df.columns = ["Category", "Total Sales (₹)", "Transactions", "Avg Order (₹)", "Units Sold"]
    cat_df["Total Sales (₹)"] = cat_df["Total Sales (₹)"].round(2)
    cat_df["Avg Order (₹)"] = cat_df["Avg Order (₹)"].round(2)
    st.dataframe(cat_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── By Payment Method ──────────────────────
    st.subheader("Sales by Payment Method")
    pay_df = (
        df.groupby("Payment")
        .agg(
            Total_Sales=("Calculated Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Order=("Calculated Sales", "mean"),
        )
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )
    pay_df.columns = ["Payment Method", "Total Sales (₹)", "Transactions", "Avg Order (₹)"]
    pay_df["Total Sales (₹)"] = pay_df["Total Sales (₹)"].round(2)
    pay_df["Avg Order (₹)"] = pay_df["Avg Order (₹)"].round(2)
    st.dataframe(pay_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── By Customer Type ───────────────────────
    st.subheader("Sales by Customer Type")
    cust_df = (
        df.groupby("Customer Type")
        .agg(
            Total_Sales=("Calculated Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Order=("Calculated Sales", "mean"),
            Avg_Rating=("Rating", "mean"),
        )
        .reset_index()
    )
    cust_df.columns = ["Customer Type", "Total Sales (₹)", "Transactions", "Avg Order (₹)", "Avg Rating"]
    cust_df["Total Sales (₹)"] = cust_df["Total Sales (₹)"].round(2)
    cust_df["Avg Order (₹)"] = cust_df["Avg Order (₹)"].round(2)
    cust_df["Avg Rating"] = cust_df["Avg Rating"].round(2)
    st.dataframe(cust_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Monthly Trend ──────────────────────────
    st.subheader("Monthly Sales Trend")
    month_df = (
        df.groupby("Month")
        .agg(
            Total_Sales=("Calculated Sales", "sum"),
            Transactions=("Invoice ID", "count"),
        )
        .reset_index()
        .sort_values("Month")
    )
    month_df.columns = ["Month", "Total Sales (₹)", "Transactions"]
    month_df["Total Sales (₹)"] = month_df["Total Sales (₹)"].round(2)
    st.dataframe(month_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Top Products ───────────────────────────
    st.subheader("Top 10 Products by Revenue")
    top_prod = (
        df.groupby("Product")["Calculated Sales"]
        .sum()
        .reset_index()
        .sort_values("Calculated Sales", ascending=False)
        .head(10)
        .rename(columns={"Calculated Sales": "Total Sales (₹)"})
    )
    top_prod["Total Sales (₹)"] = top_prod["Total Sales (₹)"].round(2)
    st.dataframe(top_prod, use_container_width=True, hide_index=True)

    # ── Download filtered data ─────────────────
    st.markdown("---")
    st.subheader("📥 Download Filtered Dataset")
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download as CSV",
        data=csv_bytes,
        file_name="filtered_sales.csv",
        mime="text/csv",
    )


# ══════════════════════════════════════════════
# TAB 4 — CHARTS
# ══════════════════════════════════════════════
with tabs[3]:
    section("Interactive Charts", "📊")

    if df.empty:
        st.warning("No data matches the current filters. Adjust the sidebar filters.")
    else:
        # ── 1. Monthly Sales Trend ─────────────
        st.subheader("1. Monthly Sales Trend")
        monthly = (
            df.groupby("Month")["Calculated Sales"]
            .sum()
            .reset_index()
            .sort_values("Month")
        )
        fig1 = px.line(
            monthly,
            x="Month",
            y="Calculated Sales",
            markers=True,
            title="Total Revenue by Month",
            labels={"Calculated Sales": "Revenue (₹)", "Month": "Month"},
            color_discrete_sequence=["#3b82d4"],
        )
        fig1.update_layout(xaxis_tickangle=-30, hovermode="x unified")
        fig1.update_traces(line_width=2.5, marker_size=8)
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("---")

        # ── 2. Sales by Branch (Bar) ───────────
        st.subheader("2. Sales by Branch")
        br = (
            df.groupby("Branch")["Calculated Sales"]
            .sum()
            .reset_index()
            .sort_values("Calculated Sales", ascending=False)
        )
        fig2 = px.bar(
            br,
            x="Branch",
            y="Calculated Sales",
            color="Branch",
            title="Total Revenue per Branch",
            labels={"Calculated Sales": "Revenue (₹)"},
            color_discrete_sequence=PALETTE,
            text_auto=".2s",
        )
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")

        # ── 3. Category Revenue (Pie) ──────────
        st.subheader("3. Revenue Share by Category")
        cat_rev = df.groupby("Category")["Calculated Sales"].sum().reset_index()
        fig3 = px.pie(
            cat_rev,
            names="Category",
            values="Calculated Sales",
            title="Revenue Distribution Across Categories",
            color_discrete_sequence=PALETTE,
            hole=0.35,
        )
        fig3.update_traces(textposition="outside", textinfo="percent+label")
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown("---")

        # ── 4. Payment Method Distribution ─────
        st.subheader("4. Payment Method Distribution")
        c41, c42 = st.columns(2)
        pay_cnt = df["Payment"].value_counts().reset_index()
        pay_cnt.columns = ["Payment Method", "Transactions"]
        with c41:
            fig4a = px.bar(
                pay_cnt,
                x="Payment Method",
                y="Transactions",
                color="Payment Method",
                title="Transactions per Payment Method",
                color_discrete_sequence=PALETTE,
                text_auto=True,
            )
            fig4a.update_layout(showlegend=False)
            st.plotly_chart(fig4a, use_container_width=True)

        pay_rev = df.groupby("Payment")["Calculated Sales"].sum().reset_index()
        with c42:
            fig4b = px.pie(
                pay_rev,
                names="Payment",
                values="Calculated Sales",
                title="Revenue Share by Payment Method",
                color_discrete_sequence=PALETTE,
                hole=0.35,
            )
            st.plotly_chart(fig4b, use_container_width=True)

        st.markdown("---")

        # ── 5. Gender × Category Heatmap ───────
        st.subheader("5. Sales Heatmap — Gender vs Category")
        pivot = df.pivot_table(
            index="Category",
            columns="Gender",
            values="Calculated Sales",
            aggfunc="sum",
            fill_value=0,
        )
        fig5 = px.imshow(
            pivot,
            text_auto=".2s",
            aspect="auto",
            title="Revenue Heatmap: Category × Gender",
            color_continuous_scale="Blues",
        )
        st.plotly_chart(fig5, use_container_width=True)

        st.markdown("---")

        # ── 6. Avg Rating by Category ──────────
        st.subheader("6. Average Customer Rating by Category")
        rating_cat = (
            df.groupby("Category")["Rating"]
            .mean()
            .reset_index()
            .sort_values("Rating", ascending=True)
        )
        fig6 = px.bar(
            rating_cat,
            x="Rating",
            y="Category",
            orientation="h",
            title="Average Customer Rating per Category",
            labels={"Rating": "Avg Rating (out of 5)"},
            color="Rating",
            color_continuous_scale="Blues",
            text_auto=".2f",
        )
        fig6.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig6, use_container_width=True)

        st.markdown("---")

        # ── 7. Scatter — Unit Price vs Sales ───
        st.subheader("7. Unit Price vs Sales (Scatter)")
        fig7 = px.scatter(
            df,
            x="Unit Price",
            y="Calculated Sales",
            color="Category",
            size="Quantity",
            hover_data=["Product", "Branch", "City"],
            title="Unit Price vs Total Sales (bubble size = Quantity)",
            color_discrete_sequence=PALETTE,
            opacity=0.75,
        )
        st.plotly_chart(fig7, use_container_width=True)

        st.markdown("---")

        # ── 8. Branch × Category Grouped Bar ───
        st.subheader("8. Revenue by Branch & Category")
        br_cat = (
            df.groupby(["Branch", "Category"])["Calculated Sales"]
            .sum()
            .reset_index()
        )
        fig8 = px.bar(
            br_cat,
            x="Category",
            y="Calculated Sales",
            color="Branch",
            barmode="group",
            title="Revenue Split by Branch and Category",
            labels={"Calculated Sales": "Revenue (₹)"},
            color_discrete_sequence=PALETTE,
            text_auto=".2s",
        )
        fig8.update_layout(xaxis_tickangle=-20)
        st.plotly_chart(fig8, use_container_width=True)

        st.markdown("---")

        # ── 9. Member vs Normal Revenue ────────
        st.subheader("9. Member vs Normal Customer — Revenue & Ratings")
        c91, c92 = st.columns(2)
        cust_rev = df.groupby("Customer Type")["Calculated Sales"].sum().reset_index()
        with c91:
            fig9a = px.bar(
                cust_rev,
                x="Customer Type",
                y="Calculated Sales",
                color="Customer Type",
                title="Total Revenue: Member vs Normal",
                labels={"Calculated Sales": "Revenue (₹)"},
                color_discrete_sequence=PALETTE,
                text_auto=".2s",
            )
            fig9a.update_layout(showlegend=False)
            st.plotly_chart(fig9a, use_container_width=True)

        cust_rate = df.groupby("Customer Type")["Rating"].mean().reset_index()
        with c92:
            fig9b = px.bar(
                cust_rate,
                x="Customer Type",
                y="Rating",
                color="Customer Type",
                title="Avg Rating: Member vs Normal",
                labels={"Rating": "Avg Rating"},
                color_discrete_sequence=PALETTE,
                text_auto=".2f",
            )
            fig9b.update_layout(showlegend=False, yaxis_range=[0, 5])
            st.plotly_chart(fig9b, use_container_width=True)

        st.markdown("---")

        # ── 10. Top 10 Products ─────────────────
        st.subheader("10. Top 10 Products by Revenue")
        top10 = (
            df.groupby("Product")["Calculated Sales"]
            .sum()
            .nlargest(10)
            .reset_index()
            .sort_values("Calculated Sales")
        )
        fig10 = px.bar(
            top10,
            x="Calculated Sales",
            y="Product",
            orientation="h",
            title="Top 10 Products by Total Revenue",
            labels={"Calculated Sales": "Revenue (₹)"},
            color="Calculated Sales",
            color_continuous_scale="Blues",
            text_auto=".2s",
        )
        fig10.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig10, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 5 — BUSINESS INSIGHTS
# ══════════════════════════════════════════════
with tabs[4]:
    section("Business Insights & Recommendations", "🏆")

    if df.empty:
        st.warning("No data matches the current filters. Adjust the sidebar filters.")
    else:
        # Compute key figures
        top_branch     = df.groupby("Branch")["Calculated Sales"].sum().idxmax()
        top_branch_val = df.groupby("Branch")["Calculated Sales"].sum().max()

        bottom_branch     = df.groupby("Branch")["Calculated Sales"].sum().idxmin()
        bottom_branch_val = df.groupby("Branch")["Calculated Sales"].sum().min()

        top_cat_val = df.groupby("Category")["Calculated Sales"].sum()
        best_cat    = top_cat_val.idxmax()
        worst_cat   = top_cat_val.idxmin()

        best_pay   = df.groupby("Payment")["Calculated Sales"].sum().idxmax()
        best_pay_pct = (
            df.groupby("Payment")["Calculated Sales"].sum().max()
            / df["Calculated Sales"].sum()
            * 100
        )

        best_rating_cat = df.groupby("Category")["Rating"].mean().idxmax()
        worst_rating_cat = df.groupby("Category")["Rating"].mean().idxmin()
        overall_rating  = df["Rating"].mean()

        member_rev  = df[df["Customer Type"] == "Member"]["Calculated Sales"].sum()
        normal_rev  = df[df["Customer Type"] == "Normal"]["Calculated Sales"].sum()
        member_pct  = member_rev / (member_rev + normal_rev) * 100

        peak_month = df.groupby("Month")["Calculated Sales"].sum().idxmax()

        # ── Branch Performance ─────────────────
        st.subheader("🏪 Branch Performance")
        col1, col2 = st.columns(2)
        with col1:
            insight(
                f"**Branch {top_branch}** is the highest-earning branch with "
                f"**{fmt_inr(top_branch_val)}** in revenue. Allocate more inventory "
                f"and staff to sustain its momentum."
            )
        with col2:
            warn_box(
                f"**Branch {bottom_branch}** generates only {fmt_inr(bottom_branch_val)}. "
                f"Investigate local demand, pricing strategy, and promotions to close the gap."
            )

        st.markdown("---")

        # ── Category Strategy ─────────────────
        st.subheader("📦 Category Strategy")
        insight(
            f"**{best_cat}** is the top-performing category by revenue. "
            f"Consider expanding its product range, offering bundle deals, "
            f"and featuring it prominently in store displays."
        )
        warn_box(
            f"**{worst_cat}** records the lowest revenue. "
            f"Re-evaluate pricing, placement, or whether the category suits the customer base."
        )

        st.markdown("---")

        # ── Payment Preferences ───────────────
        st.subheader("💳 Payment Preferences")
        insight(
            f"**{best_pay}** is the most-used payment method, accounting for "
            f"**{best_pay_pct:.1f}%** of total revenue. "
            f"Ensure smooth, uninterrupted support for this method across all branches. "
            f"Offer cashback or loyalty points to further incentivise its use."
        )

        st.markdown("---")

        # ── Customer Satisfaction ─────────────
        st.subheader("⭐ Customer Satisfaction")
        insight(
            f"Overall average rating is **{overall_rating:.2f} / 5**. "
            f"**{best_rating_cat}** earns the highest satisfaction scores — "
            f"use it as a benchmark for product quality and service."
        )
        warn_box(
            f"**{worst_rating_cat}** has the lowest rating. "
            f"Conduct customer surveys, improve product quality, and train "
            f"staff specifically for this category."
        )

        st.markdown("---")

        # ── Loyalty Program ───────────────────
        st.subheader("🎁 Loyalty & Customer Type")
        if member_rev > normal_rev:
            insight(
                f"**Member customers** contribute **{member_pct:.1f}%** of total revenue. "
                f"Strengthen the loyalty programme with exclusive discounts and early-access "
                f"sales to convert more Normal customers into Members."
            )
        else:
            insight(
                f"**Normal customers** contribute more than Members ({100 - member_pct:.1f}%). "
                f"This is a strong sign-up opportunity — promote membership benefits "
                f"at checkout to grow the loyalty base."
            )

        st.markdown("---")

        # ── Seasonal / Monthly Trend ──────────
        st.subheader("📅 Seasonal Planning")
        insight(
            f"**{peak_month}** is the peak sales month. "
            f"Plan inventory builds, promotional campaigns, and extra staffing "
            f"well in advance to maximise revenue during peak periods."
        )

        st.markdown("---")

        # ── Summary Table ─────────────────────
        st.subheader("📋 Quick Insight Summary")
        summary = pd.DataFrame(
            {
                "Insight": [
                    "Top Branch",
                    "Needs Improvement (Branch)",
                    "Best Revenue Category",
                    "Lowest Revenue Category",
                    "Preferred Payment Method",
                    "Highest Rated Category",
                    "Lowest Rated Category",
                    "Peak Sales Month",
                    "Overall Avg Rating",
                ],
                "Finding": [
                    f"Branch {top_branch} — {fmt_inr(top_branch_val)}",
                    f"Branch {bottom_branch} — {fmt_inr(bottom_branch_val)}",
                    best_cat,
                    worst_cat,
                    f"{best_pay} ({best_pay_pct:.1f}% of revenue)",
                    best_rating_cat,
                    worst_rating_cat,
                    peak_month,
                    f"{overall_rating:.2f} / 5",
                ],
                "Action": [
                    "Scale up inventory & staffing",
                    "Review pricing, promotions & local demand",
                    "Expand range, bundle offers, prime placement",
                    "Reassess pricing, placement, or viability",
                    "Ensure reliability; add cashback incentives",
                    "Use as benchmark across all categories",
                    "Improve quality; gather customer feedback",
                    "Pre-stock inventory & run targeted campaigns",
                    "Target ≥ 4.0; address low-rated categories",
                ],
            }
        )
        st.dataframe(summary, use_container_width=True, hide_index=True)

    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align:center;color:#57606a;font-size:12px;'>"
        "Supermarket Sales Analytics Dashboard &nbsp;|&nbsp; Built with Streamlit &amp; Plotly"
        "</p>",
        unsafe_allow_html=True,
    )
