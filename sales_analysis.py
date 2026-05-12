import pandas as pd
import streamlit as st
import plotly.express as px

st.title("📊 Sales & Revenue Analysis Dashboard")

df = pd.read_csv("data/sales_data.csv", encoding="latin1")

# Sidebar filters
st.sidebar.header("Filters")
region = st.sidebar.multiselect("Select Region", df["Region"].unique())
category = st.sidebar.multiselect("Select Category", df["Category"].unique())

# Apply filters
filtered_df = df.copy()

if region:
    filtered_df = filtered_df[filtered_df["Region"].isin(region)]

if category:
    filtered_df = filtered_df[filtered_df["Category"].isin(category)]

# KPI
st.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")

# Top products
top_products = filtered_df.groupby("Product Name")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=False).head(10)

fig1 = px.bar(top_products, x="Product Name", y="Sales", title="Top 10 Products")
st.plotly_chart(fig1)

# Sales by region
region_sales = filtered_df.groupby("Region")["Sales"].sum().reset_index()

fig2 = px.pie(region_sales, names="Region", values="Sales", title="Sales by Region")
st.plotly_chart(fig2)

# Sales trend
filtered_df["Order Date"] = pd.to_datetime(filtered_df["Order Date"])

trend = filtered_df.groupby("Order Date")["Sales"].sum().reset_index()

fig3 = px.line(trend, x="Order Date", y="Sales", title="Sales Trend Over Time")
st.plotly_chart(fig3)