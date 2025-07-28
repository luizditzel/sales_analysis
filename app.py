import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings - Streamlit
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/superstore.csv", encoding="latin-1")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Year'] = df['Order Date'].dt.year
    return df

df = load_data()

st.title("Sales dashboard - Superstore")

# Filtering
st.sidebar.header("Filters")
years = st.sidebar.multiselect("Select year:", sorted(df['Year'].unique()), default=df['Year'].unique())
category = st.sidebar.multiselect("Select category:", df['Category'].unique(), default=df['Category'].unique())

df_filtered = df[(df['Year'].isin(years)) & (df['Category'].isin(category))]

# --- KPIs ---
total_sales = df_filtered['Sales'].sum()
total_profit = df_filtered['Profit'].sum()
total_orders = len(df_filtered['Order ID'].unique())

col1, col2, col3 = st.columns(3)
col1.metric("Total sales", f"R${total_sales:,.2f}")
col2.metric("Total profit", f"R${total_profit:,.2f}")
col3.metric("Orders", f"{total_orders:,}")

st.markdown("---")

# Plotting
col4, col5 = st.columns(2)

# Regional sales
sales_region = df_filtered.groupby('Region')['Sales'].sum().reset_index()
fig1 = px.bar(sales_region, x='Region', y='Sales', title="Sales by Region", text_auto=True)
col4.plotly_chart(fig1, use_container_width=True)

# Sales by category
sales_category = df_filtered.groupby('Category')['Sales'].sum().reset_index()
fig2 = px.pie(sales_category, values='Sales', names='Category', title="Sales by category")
col5.plotly_chart(fig2, use_container_width=True)

# Timeline
st.subheader("Sales evolution over time")
sales_time = df_filtered.groupby('Order Date')['Sales'].sum().reset_index()
fig3 = px.line(sales_time, x='Order Date', y='Sales', title="Sales tendency")
st.plotly_chart(fig3, use_container_width=True)

# Tables with details
st.subheader("📋 Dados Filtrados")
st.dataframe(df_filtered)
