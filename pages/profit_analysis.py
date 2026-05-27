import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Profit Analysis", layout="wide")


@st.cache_data
def read_csv(file):
    df = pd.read_csv(file)
    return df


df = read_csv("data/sales.csv")
df.columns = df.columns.str.strip()

st.title("Profit Analysis")
st.write("This page analyzes profit trends across time, category, region, and segment.")

if "Order Date" in df.columns:
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month_name()
    df["Month Number"] = df["Order Date"].dt.month
    df["Year Month"] = df["Order Date"].dt.to_period("M").astype(str)


st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Rows", df.shape[0])

with col2:
    st.metric("Total Columns", df.shape[1])

with col3:
    st.metric("Total Profit", f"{df['Profit'].sum():,.2f}")

st.dataframe(df.head(), use_container_width=True)


# Filters

st.subheader("Filters")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    selected_year = st.multiselect(
        "Select Year",
        options=sorted(df["Year"].dropna().unique()),
        default=sorted(df["Year"].dropna().unique())
    )

with filter_col2:
    selected_region = st.multiselect(
        "Select Region",
        options=df["Region"].dropna().unique(),
        default=df["Region"].dropna().unique()
    )

with filter_col3:
    selected_category = st.multiselect(
        "Select Category",
        options=df["Category"].dropna().unique(),
        default=df["Category"].dropna().unique()
    )

filter_col4, filter_col5 = st.columns(2)

with filter_col4:
    selected_segment = st.multiselect(
        "Select Segment",
        options=df["Segment"].dropna().unique(),
        default=df["Segment"].dropna().unique()
    )

with filter_col5:
    selected_ship_mode = st.multiselect(
        "Select Ship Mode",
        options=df["Ship Mode"].dropna().unique(),
        default=df["Ship Mode"].dropna().unique()
    )

filtered_df = df.copy()

filtered_df = filtered_df[
    (filtered_df["Year"].isin(selected_year)) &
    (filtered_df["Region"].isin(selected_region)) &
    (filtered_df["Category"].isin(selected_category)) &
    (filtered_df["Segment"].isin(selected_segment)) &
    (filtered_df["Ship Mode"].isin(selected_ship_mode))
]


# KPIs
st.subheader("Profit KPIs")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("Total Profit", f"{filtered_df['Profit'].sum():,.2f}")

with kpi2:
    st.metric("Average Profit", f"{filtered_df['Profit'].mean():,.2f}")

with kpi3:
    st.metric("Max Profit", f"{filtered_df['Profit'].max():,.2f}")

with kpi4:
    st.metric("Loss Records", (filtered_df["Profit"] < 0).sum())


# Monthly Profit Trend

st.subheader("Monthly Profit Trend")

monthly_profit = filtered_df.groupby("Year Month", as_index=False)["Profit"].sum()

fig1 = px.line(
    monthly_profit,
    x="Year Month",
    y="Profit",
    markers=True,
    title="Monthly Profit Trend"
)

st.plotly_chart(fig1, use_container_width=True)



# Yearly Profit Trend

st.subheader("Yearly Profit Trend")

yearly_profit = filtered_df.groupby("Year", as_index=False)["Profit"].sum()

fig2 = px.bar(
    yearly_profit,
    x="Year",
    y="Profit",
    text_auto=True,
    title="Yearly Profit Trend"
)

st.plotly_chart(fig2, use_container_width=True)


# Category Wise Profit

st.subheader("Category Wise Profit")

category_profit = filtered_df.groupby("Category", as_index=False)["Profit"].sum()

fig3 = px.bar(
    category_profit,
    x="Category",
    y="Profit",
    color="Category",
    text_auto=True,
    title="Category Wise Profit"
)

st.plotly_chart(fig3, use_container_width=True)



# Region Wise Profit

st.subheader("Region Wise Profit")

region_profit = filtered_df.groupby("Region", as_index=False)["Profit"].sum()

fig4 = px.pie(
    region_profit,
    names="Region",
    values="Profit",
    title="Region Wise Profit Distribution"
)

st.plotly_chart(fig4, use_container_width=True)


# Segment Wise Profit Trend

st.subheader("Segment Wise Profit Trend")

segment_profit = filtered_df.groupby(
    ["Year Month", "Segment"],
    as_index=False
)["Profit"].sum()

fig5 = px.area(
    segment_profit,
    x="Year Month",
    y="Profit",
    color="Segment",
    title="Segment Wise Profit Trend"
)

st.plotly_chart(fig5, use_container_width=True)


# Loss Making Sub-Categories


st.subheader("Loss Making Sub-Categories")

loss_df = filtered_df.groupby(
    "Sub-Category",
    as_index=False
)["Profit"].sum()

loss_df = loss_df.sort_values("Profit")

fig6 = px.bar(
    loss_df,
    x="Sub-Category",
    y="Profit",
    color="Profit",
    title="Loss Making Sub-Categories"
)

st.plotly_chart(fig6, use_container_width=True)


# Profit Margin Analysis

st.subheader("Profit Margin Analysis")

margin_df = filtered_df.groupby(
    "Category",
    as_index=False
).agg({
    "Sales": "sum",
    "Profit": "sum"
})

margin_df["Profit Margin %"] = (
    margin_df["Profit"] / margin_df["Sales"]
) * 100

fig7 = px.bar(
    margin_df,
    x="Category",
    y="Profit Margin %",
    text_auto=True,
    title="Profit Margin by Category"
)

st.plotly_chart(fig7, use_container_width=True)

# Summary Table

st.subheader("Profit Summary Table")

summary_table = filtered_df.groupby(
    "Year Month",
    as_index=False
).agg({
    "Profit": "sum",
    "Sales": "sum",
    "Quantity": "sum"
})

st.dataframe(summary_table, use_container_width=True)


# Download

st.subheader("Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Profit Analysis Data",
    data=csv,
    file_name="profit_analysis.csv",
    mime="text/csv"
)
