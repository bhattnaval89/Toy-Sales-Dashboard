import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sales Intelligence",
    layout="wide",
)

st.title(" Sales Intelligence Platform")

# Load datasets
sales = pd.read_csv("data/sales.csv")
products = pd.read_csv("data/products.csv")
stores = pd.read_csv("data/stores.csv")

# Merge datasets
merged = sales.merge(products, on="Product_ID")
merged = merged.merge(stores, on="Store_ID")
# Convert prices from text to numbers
merged["Product_Price"] = (
    merged["Product_Price"]
    .replace("[$,]", "", regex=True)
    .astype(float)
)

merged["Product_Cost"] = (
    merged["Product_Cost"]
    .replace("[$,]", "", regex=True)
    .astype(float)
)
# Revenue
merged["Revenue"] = merged["Units"] * merged["Product_Price"]

#profits

merged["Profit"] = (
    merged["Product_Price"] - merged["Product_Cost"]
) * merged["Units"]


# Sidebar

st.sidebar.header("Filters")

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + list(merged["Product_Category"].unique())
)

# Filter the data based on the selected category


if selected_category != "All":
    filtered_df = merged[
        merged["Product_Category"] == selected_category
    ]
else:
    filtered_df = merged

# KPI Calculations

total_revenue = filtered_df["Revenue"].sum()
total_profit = filtered_df["Profit"].sum()
total_units = filtered_df["Units"].sum()
total_products = merged["Product_ID"].nunique()
total_stores = merged["Store_ID"].nunique()

# KPI Cards
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("💰 Revenue", f"${total_revenue:,.0f}")
c2.metric("💸 Profit", f"${total_profit:,.0f}")
c3.metric("📦 Units Sold", f"{total_units:,}")
c4.metric("🧸 Products", total_products)
c5.metric("🏪 Stores", total_stores)

st.divider()

st.subheader("Dataset Preview")

st.dataframe(filtered_df.head())

st.divider()

st.subheader("🏆 Top 10 Products by Revenue")

product_revenue = (
    filtered_df.groupby("Product_Name")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(product_revenue)