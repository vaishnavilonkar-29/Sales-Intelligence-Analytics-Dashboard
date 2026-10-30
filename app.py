
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Sales Intelligence & Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. PROFESSIONAL DASHBOARD DESIGN
# =========================================================

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(
            ellipse at 5% 5%,
            rgba(89, 91, 219, 0.28),
            transparent 38%
        ),
        radial-gradient(
            ellipse at 95% 20%,
            rgba(0, 190, 180, 0.20),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #10182F 0%,
            #182746 55%,
            #102F42 100%
        ) !important;
    color: #F1F5F9;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: transparent !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1 {
    color: #FFFFFF !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
}

h2 {
    color: #B9C8FF !important;
    font-weight: 700 !important;
}

h3 {
    color: #73E4D2 !important;
    font-weight: 650 !important;
}

.stApp p,
.stApp [data-testid="stCaptionContainer"] {
    color: #DCE6F5;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #182746 0%,
        #20264B 55%,
        #123B49 100%
    ) !important;
    border-right: 1px solid #35466A;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #FFFFFF !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}

/* Sidebar filters */
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="input"],
[data-testid="stSidebar"] [data-baseweb="input"] > div {
    background: #FFFFFF !important;
    border: 1px solid #73E4D2 !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] input,
[data-testid="stSidebar"] [data-baseweb="input"] input {
    color: #172554 !important;
    -webkit-text-fill-color: #172554 !important;
}

[data-testid="stSidebar"] [data-baseweb="input"] svg {
    color: #172554 !important;
    fill: #172554 !important;
}

/* KPI cards */
div[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #FFFFFF 0%,
        #EAF5FF 100%
    ) !important;
    border: 1px solid #B8CBE5;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
}

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] label p,
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] p {
    color: #243B63 !important;
    -webkit-text-fill-color: #243B63 !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"],
div[data-testid="stMetric"] [data-testid="stMetricValue"] * {
    color: #14213D !important;
    -webkit-text-fill-color: #14213D !important;
    font-weight: 800 !important;
    opacity: 1 !important;
}

/* Charts and data tables */
div[data-testid="stPlotlyChart"],
div[data-testid="stDataFrame"] {
    background: #FFFFFF;
    border: 1px solid #D8E4F0;
    border-radius: 14px;
    padding: 6px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

/* Download buttons */
.stDownloadButton button,
.stButton button {
    background: linear-gradient(
        90deg,
        #6558F5,
        #00AFA3
    ) !important;
    color: #FFFFFF !important;
    border: none;
    border-radius: 10px;
    font-weight: 700;
}

hr {
    border-color: #40516F;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. LOAD THE EXISTING CLEANED DATASET
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

# Use the original dataset locally and the sample dataset online.
SAMPLE_DATA_PATH = BASE_DIR / "data" / "sample_sales_data.csv"
LOCAL_DATA_PATH = BASE_DIR / "data" / "cleaned_sales_data.csv"

DATA_PATH = (
    SAMPLE_DATA_PATH
    if SAMPLE_DATA_PATH.exists()
    else LOCAL_DATA_PATH
)


@st.cache_data
def load_data(file_path):

    data = pd.read_csv(file_path)

    required_columns = [
        "Product_Name",
        "Category",
        "Price",
        "Units_Sold",
        "Date",
        "Promotion",
        "Sales"
    ]

    missing = [
        col for col in required_columns
        if col not in data.columns
    ]

    if missing:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing)
        )

    data["Date"] = pd.to_datetime(
        data["Date"], errors="coerce"
    )

    for col in ["Price", "Units_Sold", "Sales"]:
        data[col] = pd.to_numeric(
            data[col], errors="coerce"
        )

    # Standardize Promotion values such as 0, 1, "0", and "1".
    data["Promotion"] = pd.to_numeric(
        data["Promotion"], errors="coerce"
    )

    data = data.dropna(
        subset=[
            "Date",
            "Product_Name",
            "Category",
            "Sales",
            "Units_Sold"
        ]
    )

    data["Month"] = data["Date"].dt.to_period("M")

    return data


try:
    df = load_data(DATA_PATH)

except FileNotFoundError:
    st.error(
        "Dataset not found. Please check that "
        "data/cleaned_sales_data.csv exists."
    )
    st.stop()

except Exception as error:
    st.error(f"Could not load the dataset: {error}")
    st.stop()

if df.empty:
    st.error("The cleaned dataset contains no usable records.")
    st.stop()


# =========================================================
# 4. DASHBOARD HEADER
# =========================================================

st.title("📊 AI-Powered Sales Intelligence Dashboard")

st.markdown(
    "Understand sales performance, discover product trends, "
    "compare promotions, and explore a simple sales forecast."
)

st.caption(
    f"Data period: {df['Date'].min():%d %b %Y} – "
    f"{df['Date'].max():%d %b %Y}"
)

st.markdown("---")


# =========================================================
# 5. SIDEBAR FILTERS
# =========================================================

st.sidebar.title("🎛️ Dashboard Controls")
st.sidebar.markdown("Customize your analysis.")
st.sidebar.markdown("---")

products = sorted(df["Product_Name"].unique().tolist())
categories = sorted(df["Category"].unique().tolist())
promotions = sorted(
    df["Promotion"].dropna().unique().tolist(),
    key=str
)

selected_products = st.sidebar.multiselect(
    "Select Products",
    products,
    default=products
)

selected_categories = st.sidebar.multiselect(
    "Select Categories",
    categories,
    default=categories
)

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

# Use two separate calendar widgets so BOTH dates can be picked
# from a calendar instead of manually typing the end date.
start_date = st.sidebar.date_input(
    "Start Date",
    value=min_date,
    min_value=min_date,
    max_value=max_date,
    key="sales_start_date"
)

end_date = st.sidebar.date_input(
    "End Date",
    value=max_date,
    min_value=min_date,
    max_value=max_date,
    key="sales_end_date"
)

# Friendly labels for the binary promotion column.
promotion_labels = {
    0: "No Promotion",
    1: "Promotion Applied"
}

selected_promotions = st.sidebar.multiselect(
    "Promotion Status",
    options=promotions,
    default=promotions,
    format_func=lambda value: promotion_labels.get(
        int(value), str(value)
    ) if pd.notna(value) else "Unknown"
)

st.sidebar.markdown("---")
st.sidebar.caption(f"Available records: {len(df):,}")


# =========================================================
# 6. FILTER DATA
# =========================================================

if start_date > end_date:
    st.sidebar.error("Start Date must be on or before End Date.")
    st.warning("Please choose a Start Date that is earlier than or equal to the End Date.")
    st.stop()

filtered_df = df[
    df["Product_Name"].isin(selected_products)
    & df["Category"].isin(selected_categories)
    & df["Promotion"].isin(selected_promotions)
    & (df["Date"].dt.date >= start_date)
    & (df["Date"].dt.date <= end_date)
].copy()

# Show how many source records exist in each category to help
# diagnose categories that appear in the dropdown but return no rows.
with st.sidebar.expander("Category data check"):
    category_counts = (
        df.groupby("Category").size().sort_values(ascending=False)
    )
    st.caption("Records available per category in the full dataset:")
    st.dataframe(
        category_counts.rename("Records").rename_axis("Category").reset_index(),
        use_container_width=True,
        hide_index=True
    )

if filtered_df.empty:
    st.warning(
        "No records match these filters. "
        "Please select a different product, category, "
        "promotion status, or date range."
    )
    st.stop()


# =========================================================
# 7. KEY PERFORMANCE INDICATORS
# =========================================================

st.subheader("✨ Sales Performance Overview")

total_sales = filtered_df["Sales"].sum()
total_units = filtered_df["Units_Sold"].sum()
average_sales = filtered_df["Sales"].mean()
record_count = len(filtered_df)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "💰 Total Sales",
        f"₹{total_sales:,.2f}"
    )

with k2:
    st.metric(
        "📦 Units Sold",
        f"{total_units:,.0f}"
    )

with k3:
    st.metric(
        "📈 Average Sales / Record",
        f"₹{average_sales:,.2f}"
    )

with k4:
    st.metric(
        "🧾 Records Analyzed",
        f"{record_count:,}"
    )

st.caption(
    f"Showing {record_count:,} records out of "
    f"{len(df):,} records in the full dataset."
)

st.markdown("---")


# =========================================================
# 8. MONTHLY SALES TREND AND GROWTH
# =========================================================

st.subheader("📅 Monthly Sales Analysis")

monthly_sales = (
    filtered_df
    .groupby("Month")["Sales"]
    .sum()
    .sort_index()
)

monthly_chart_data = monthly_sales.reset_index()
monthly_chart_data["Month"] = (
    monthly_chart_data["Month"].astype(str)
)

if len(monthly_chart_data) >= 2:

    monthly_chart_data["Monthly_Growth_Pct"] = (
        monthly_chart_data["Sales"].pct_change() * 100
    )

else:
    monthly_chart_data["Monthly_Growth_Pct"] = np.nan

trend_col, growth_col = st.columns([1.7, 1])

with trend_col:

    fig_monthly = px.line(
        monthly_chart_data,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend",
        labels={
            "Month": "Month",
            "Sales": "Sales (₹)"
        },
        template="plotly_white"
    )

    fig_monthly.update_traces(
        line=dict(color="#6558F5", width=3),
        marker=dict(color="#00AFA3", size=8),
        hovertemplate=(
            "Month: %{x}<br>"
            "Sales: ₹%{y:,.2f}"
            "<extra></extra>"
        )
    )

    fig_monthly.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#172554"),
        title_font=dict(size=18, color="#172554"),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#E2E8F0", tickprefix="₹")
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )

with growth_col:

    fig_growth = px.bar(
        monthly_chart_data,
        x="Month",
        y="Monthly_Growth_Pct",
        title="Month-over-Month Growth",
        labels={
            "Month": "Month",
            "Monthly_Growth_Pct": "Growth (%)"
        },
        template="plotly_white"
    )

    fig_growth.update_traces(
        marker_color="#00AFA3",
        hovertemplate=(
            "Month: %{x}<br>"
            "Growth: %{y:.2f}%"
            "<extra></extra>"
        )
    )

    fig_growth.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#172554"),
        title_font=dict(size=18, color="#172554"),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#E2E8F0")
    )

    st.plotly_chart(
        fig_growth,
        use_container_width=True
    )

st.caption(
    "Monthly growth compares each month's sales with the "
    "previous month's sales. The first month has no prior "
    "month in the selected data for comparison."
)

st.markdown("---")


# =========================================================
# 9. PRODUCT PERFORMANCE
# =========================================================

st.subheader("🏆 Product Performance")

product_sales = (
    filtered_df.groupby("Product_Name", as_index=False)
    .agg(
        Total_Sales=("Sales", "sum"),
        Units_Sold=("Units_Sold", "sum")
    )
    .sort_values("Total_Sales", ascending=False)
)

product_col1, product_col2 = st.columns(2)

with product_col1:

    top_products = product_sales.head(10).sort_values(
        "Total_Sales", ascending=True
    )

    fig_top = px.bar(
        top_products,
        x="Total_Sales",
        y="Product_Name",
        orientation="h",
        title="Top Products by Sales",
        labels={
            "Total_Sales": "Sales (₹)",
            "Product_Name": "Product"
        },
        template="plotly_white"
    )

    fig_top.update_traces(marker_color="#6558F5")

    fig_top.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#172554"),
        title_font=dict(size=18, color="#172554"),
        xaxis=dict(gridcolor="#E2E8F0", tickprefix="₹"),
        yaxis=dict(showgrid=False)
    )

    st.plotly_chart(fig_top, use_container_width=True)

with product_col2:

    bottom_products = product_sales.tail(10).sort_values(
        "Total_Sales", ascending=True
    )

    fig_bottom = px.bar(
        bottom_products,
        x="Total_Sales",
        y="Product_Name",
        orientation="h",
        title="Lowest Products by Sales",
        labels={
            "Total_Sales": "Sales (₹)",
            "Product_Name": "Product"
        },
        template="plotly_white"
    )

    fig_bottom.update_traces(marker_color="#E87979")

    fig_bottom.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#172554"),
        title_font=dict(size=18, color="#172554"),
        xaxis=dict(gridcolor="#E2E8F0", tickprefix="₹"),
        yaxis=dict(showgrid=False)
    )

    st.plotly_chart(fig_bottom, use_container_width=True)

st.caption(
    "The lowest-performing products are ranked by sales value "
    "within the selected data. Low sales alone do not establish "
    "that a product is unprofitable."
)

st.markdown("---")


# =========================================================
# 10. CATEGORY ANALYSIS
# =========================================================

st.subheader("🗂️ Category Contribution")

category_sales = (
    filtered_df.groupby("Category", as_index=False)
    .agg(
        Total_Sales=("Sales", "sum"),
        Units_Sold=("Units_Sold", "sum")
    )
    .sort_values("Total_Sales", ascending=False)
)

category_total = category_sales["Total_Sales"].sum()

if category_total != 0:
    category_sales["Sales_Share_Pct"] = (
        category_sales["Total_Sales"]
        / category_total * 100
    )
else:
    category_sales["Sales_Share_Pct"] = 0.0

cat_col1, cat_col2 = st.columns([1.2, 1])

with cat_col1:

    fig_category = px.bar(
        category_sales.sort_values(
            "Total_Sales", ascending=True
        ),
        x="Total_Sales",
        y="Category",
        orientation="h",
        title="Sales by Category",
        labels={
            "Total_Sales": "Sales (₹)",
            "Category": "Category"
        },
        template="plotly_white"
    )

    fig_category.update_traces(marker_color="#00AFA3")

    fig_category.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#172554"),
        title_font=dict(size=18, color="#172554"),
        xaxis=dict(gridcolor="#E2E8F0", tickprefix="₹"),
        yaxis=dict(showgrid=False)
    )

    st.plotly_chart(fig_category, use_container_width=True)

with cat_col2:

    fig_share = px.pie(
        category_sales,
        names="Category",
        values="Total_Sales",
        hole=0.55,
        title="Share of Sales by Category",
        template="plotly_white"
    )

    fig_share.update_layout(
        paper_bgcolor="white",
        font=dict(color="#172554"),
        title_font=dict(size=18, color="#172554")
    )

    st.plotly_chart(fig_share, use_container_width=True)

st.dataframe(
    category_sales,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")


# =========================================================
# 11. PROMOTION EFFECTIVENESS
# =========================================================

st.subheader("🎯 Promotion Analysis")

promotion_sales = (
    filtered_df.groupby("Promotion", as_index=False)
    .agg(
        Total_Sales=("Sales", "sum"),
        Units_Sold=("Units_Sold", "sum"),
        Average_Sales=("Sales", "mean"),
        Records=("Sales", "count")
    )
)

promotion_sales["Promotion Status"] = promotion_sales["Promotion"].map(
    promotion_labels
).fillna(promotion_sales["Promotion"].astype(str))

promo_col1, promo_col2 = st.columns([1.4, 1])

with promo_col1:

    fig_promo = px.bar(
        promotion_sales,
        x="Promotion Status",
        y="Total_Sales",
        color="Promotion Status",
        title="Sales by Promotion Status",
        labels={
            "Promotion Status": "Promotion Status",
            "Total_Sales": "Sales (₹)"
        },
        template="plotly_white"
    )

    fig_promo.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#172554"),
        title_font=dict(size=18, color="#172554"),
        showlegend=False,
        yaxis=dict(gridcolor="#E2E8F0", tickprefix="₹")
    )

    st.plotly_chart(fig_promo, use_container_width=True)

with promo_col2:

    st.markdown("#### Promotion Summary")

    st.dataframe(
        promotion_sales.drop(columns=["Promotion"]),
        use_container_width=True,
        hide_index=True
    )

st.caption(
    "This section compares observed sales by promotion status. "
    "It does not prove that promotions caused higher sales."
)

st.markdown("---")


# =========================================================
# 12. AUTOMATIC BUSINESS OBSERVATIONS
# =========================================================

st.subheader("💡 Business Insights")

insight1, insight2 = st.columns(2)

if not product_sales.empty:

    best_product = product_sales.iloc[0]

    with insight1:

        st.markdown("#### 🏆 Highest-Selling Product")

        st.success(
            f"{best_product['Product_Name']} has the highest "
            f"sales value in the selected data: "
            f"₹{best_product['Total_Sales']:,.2f}."
        )

if not category_sales.empty:

    best_category = category_sales.sort_values(
        "Total_Sales", ascending=False
    ).iloc[0]

    with insight2:

        st.markdown("#### 🌟 Leading Category")

        st.success(
            f"{best_category['Category']} is the leading category, "
            f"contributing {best_category['Sales_Share_Pct']:.1f}% "
            f"of selected sales."
        )

if len(monthly_sales) >= 2:

    first_month_sales = monthly_sales.iloc[0]
    last_month_sales = monthly_sales.iloc[-1]

    if first_month_sales != 0:

        overall_change = (
            (last_month_sales - first_month_sales)
            / abs(first_month_sales)
        ) * 100

        st.info(
            f"Sales changed by {overall_change:+.2f}% between "
            f"the first and last months available in the selected "
            f"data. This compares the endpoints, not every month."
        )

st.markdown("---")


# =========================================================
# 13. BASIC THREE-MONTH SALES FORECAST
# =========================================================

st.subheader("🔮 Basic Sales Forecast")

st.write(
    "This section estimates the next three months using a simple "
    "linear trend fitted to historical monthly sales. It is a "
    "baseline demonstration, not an advanced AI model."
)

# Aggregate all selected records by month.
forecast_history = (
    filtered_df
    .groupby("Month")["Sales"]
    .sum()
    .sort_index()
)

# Fill missing calendar months with zero sales.
if not forecast_history.empty:

    complete_months = pd.period_range(
        start=forecast_history.index.min(),
        end=forecast_history.index.max(),
        freq="M"
    )

    forecast_history = forecast_history.reindex(
        complete_months,
        fill_value=0
    )

if len(forecast_history) < 3:

    st.warning(
        "At least three months of historical data are required "
        "for this basic forecast. Expand the selected date range "
        "to include more months."
    )

else:

    # Use a straight-line trend over historical monthly sales.
    x_values = np.arange(len(forecast_history))
    y_values = forecast_history.to_numpy(dtype=float)

    slope, intercept = np.polyfit(
        x_values,
        y_values,
        1
    )

    future_x = np.arange(
        len(forecast_history),
        len(forecast_history) + 3
    )

    # Sales cannot be negative, so clamp negative estimates to zero.
    predicted_sales = np.maximum(
        slope * future_x + intercept,
        0
    )

    future_months = pd.period_range(
        start=forecast_history.index[-1] + 1,
        periods=3,
        freq="M"
    )

    history_output = pd.DataFrame({
        "Month": forecast_history.index.astype(str),
        "Sales": y_values,
        "Type": "Historical"
    })

    forecast_output = pd.DataFrame({
        "Month": future_months.astype(str),
        "Sales": predicted_sales,
        "Type": "Trend estimate"
    })

    combined_forecast = pd.concat(
        [history_output, forecast_output],
        ignore_index=True
    )

    fig_forecast = px.line(
        combined_forecast,
        x="Month",
        y="Sales",
        color="Type",
        markers=True,
        title="Historical Sales and Three-Month Trend Estimate",
        labels={
            "Month": "Month",
            "Sales": "Sales (₹)",
            "Type": "Series"
        },
        color_discrete_map={
            "Historical": "#6558F5",
            "Trend estimate": "#00AFA3"
        },
        template="plotly_white"
    )

    fig_forecast.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#172554"),
        title_font=dict(size=18, color="#172554"),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#E2E8F0", tickprefix="₹")
    )

    st.plotly_chart(
        fig_forecast,
        use_container_width=True
    )

    forecast_table = pd.DataFrame({
        "Forecast Month": future_months.astype(str),
        "Estimated Sales (₹)": predicted_sales.round(2)
    })

    st.dataframe(
        forecast_table,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Forecast estimates use a straight-line trend and do not "
        "account for seasonality, holidays, price changes, or "
        "future business events. Accuracy has not been validated."
    )


# =========================================================
# 14. DETAILED DATA AND DOWNLOADS
# =========================================================

st.markdown("---")
st.subheader("📋 Detailed Sales Records")

display_columns = [
    "Date",
    "Product_Name",
    "Category",
    "Price",
    "Units_Sold",
    "Promotion",
    "Sales"
]

display_df = (
    filtered_df[display_columns]
    .sort_values("Date", ascending=False)
    .copy()
)

display_df["Promotion"] = display_df["Promotion"].map(
    promotion_labels
).fillna(display_df["Promotion"].astype(str))

display_df["Date"] = display_df["Date"].dt.strftime(
    "%Y-%m-%d"
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

download_df = filtered_df[display_columns].copy()
download_df["Promotion"] = download_df["Promotion"].map(
    promotion_labels
).fillna(download_df["Promotion"].astype(str))
csv_data = download_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Sales Data (CSV)",
    data=csv_data,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

if len(monthly_chart_data) > 0:

    monthly_csv = monthly_chart_data.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Monthly Sales Analysis (CSV)",
        data=monthly_csv,
        file_name="monthly_sales_analysis.csv",
        mime="text/csv"
    )


# =========================================================
# 15. FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align: center;
        padding: 15px;
        color: #C5D3E8;
    ">
        <p>📊 AI-Powered Sales Intelligence Dashboard</p>
        <p>Built with Python, Streamlit, Pandas, NumPy and Plotly</p>
    </div>
    """,
    unsafe_allow_html=True
)
