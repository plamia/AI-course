import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("Sales Performance Dashboard")

# Read data (Using absolute paths or assuming running from same dir)
df_sales = pd.read_parquet('gold/daily_sales_by_category.parquet')
df_returns = pd.read_parquet('gold/returns_rate.parquet')

# Metrics
total_rev = df_sales['total_revenue'].sum()
avg_return = df_returns['returns_rate_pct'].mean()
col1, col2 = st.columns(2)
col1.metric("Total Revenue", f"${total_rev:,.2f}")
col2.metric("Average Returns Rate", f"{avg_return:.2f}%")

st.divider()

# Chart 1
st.subheader("Total Revenue by Region")
sales_grouped = df_sales.groupby(['region', 'product_category'])['total_revenue'].sum().reset_index()
fig1 = px.bar(sales_grouped, x='region', y='total_revenue', color='product_category', barmode='group')
st.plotly_chart(fig1, use_container_width=True)

# Chart 2
st.subheader("Returns Rate Over Time")
df_returns = df_returns.sort_values('order_date')
fig2 = px.line(df_returns, x='order_date', y='returns_rate_pct')
st.plotly_chart(fig2, use_container_width=True)

st.caption(f"Data last updated: {df_sales['order_date'].max()}")
