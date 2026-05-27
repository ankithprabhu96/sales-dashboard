import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Region Analysis", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/sales.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.title("Region Wise Analysis")
st.write("This page analyzes sales, profit, and performance across regions.")


if "Order Date" in df.columns:
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month_name()
    df["Year Month"] = df["Order Date"].dt.to_period("M").astype(str)


st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Rows", df.shape[0])

with col2:
    st.metric("Total Regions", df["Region"].nunique())

with col3:
    st.metric("Total Sales", f"{df['Sales'].sum():,.2f}")

st.dataframe(df.head(), use_container_width=True)



# Filters
st.subheader("Filters")

filter_col1, filter_col2 = st.columns(2)

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

filtered_df = df.copy()

filtered_df = filtered_df[
    (filtered_df["Year"].isin(selected_year)) &
    (filtered_df["Region"].isin(selected_region))
]



# KPIs

st.subheader("Region KPIs")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("Total Sales", f"{filtered_df['Sales'].sum():,.2f}")

with kpi2:
    st.metric("Total Profit", f"{filtered_df['Profit'].sum():,.2f}")

with kpi3:
    st.metric("Total Orders", filtered_df["Order ID"].nunique())

with kpi4:
    st.metric("Average Profit per Order", f"{filtered_df['Profit'].mean():,.2f}")



# Region Wise Sales
st.subheader("Region Wise Sales")

region_sales = filtered_df.groupby("Region", as_index=False)["Sales"].sum()

fig1 = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    color="Region",
    text_auto=True,
    title="Region Wise Sales"
)

st.plotly_chart(fig1, use_container_width=True)


# Region Wise Profit

st.subheader("Region Wise Profit")

region_profit = filtered_df.groupby("Region", as_index=False)["Profit"].sum()

fig2 = px.bar(
    region_profit,
    x="Region",
    y="Profit",
    color="Region",
    text_auto=True,
    title="Region Wise Profit"
)

st.plotly_chart(fig2, use_container_width=True)



# Sales vs Profit by Region

st.subheader("Sales vs Profit by Region")

region_summary = filtered_df.groupby("Region", as_index=False).agg({
    "Sales": "sum",
    "Profit": "sum"
})

fig3 = px.scatter(
    region_summary,
    x="Sales",
    y="Profit",
    size="Sales",
    color="Region",
    title="Sales vs Profit by Region"
)

st.plotly_chart(fig3, use_container_width=True)



# Monthly Trend by Region

st.subheader("Monthly Trend by Region")

monthly_region = filtered_df.groupby(
    ["Year Month", "Region"],
    as_index=False
)[["Sales", "Profit"]].sum()

fig4 = px.line(
    monthly_region,
    x="Year Month",
    y="Sales",
    color="Region",
    markers=True,
    title="Monthly Sales Trend by Region"
)

st.plotly_chart(fig4, use_container_width=True)



# Region Contribution Pie

st.subheader("Region Contribution to Sales")

fig5 = px.pie(
    region_sales,
    names="Region",
    values="Sales",
    title="Sales Contribution by Region"
)

st.plotly_chart(fig5, use_container_width=True)



# Summary Table
st.subheader("Region Summary Table")

summary = filtered_df.groupby("Region", as_index=False).agg({
    "Sales": "sum",
    "Profit": "sum",
    "Quantity": "sum",
    "Order ID": "nunique"
})

summary = summary.rename(columns={"Order ID": "Total Orders"})

st.dataframe(summary, use_container_width=True)


# Download

st.subheader("Download Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Region Analysis Data",
    data=csv,
    file_name="region_analysis.csv",
    mime="text/csv"
)
