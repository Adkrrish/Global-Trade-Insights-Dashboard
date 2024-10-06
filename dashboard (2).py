# -*- coding: utf-8 -*-
"""Dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eNE7L1x4c0Klkvh1kIC9gKY4C2dqohfc
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset with streamlit cache to avoid reloading
@st.cache_data
def load_data(filepath):
    return pd.read_csv(filepath)

# Use relative path or allow user to upload a file
dataset = load_data("D:\\MBA materials\\Trimester 1\\DEVP(AMitra)\\Imports_Exports_Dataset.csv")

# Taking the sample dataset
df = dataset.sample(n=3001, random_state=55022)

# Set the title of the dashboard
st.title('Global Trade Insights Dashboard')

# Sidebar for filters
st.sidebar.header('Filter Options')

# Filter by Country
countries = df['Country'].unique()
selected_countries = st.sidebar.multiselect('Select Countries:', countries, default=countries)

# Filter by Product
products = df['Product'].unique()
selected_products = st.sidebar.multiselect('Select Products:', products, default=products)

# Filter by Date Range
min_date = pd.to_datetime(df['Date']).min()
max_date = pd.to_datetime(df['Date']).max()
start_date, end_date = st.sidebar.date_input(
    "Select Date Range:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply filters to the DataFrame
filtered_df = df[
    (df['Country'].isin(selected_countries)) &
    (df['Product'].isin(selected_products)) &
    (pd.to_datetime(df['Date']) >= start_date) &
    (pd.to_datetime(df['Date']) <= end_date)
]

# Key Metrics
total_value = filtered_df['Value'].sum()
avg_value = filtered_df['Value'].mean()
num_transactions = len(filtered_df)

# Display key metrics
st.header("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Transaction Value", f"${total_value:,.2f}")
col2.metric("Average Transaction Value", f"${avg_value:,.2f}")
col3.metric("Number of Transactions", num_transactions)

# Visualization 1: Transaction Value Distribution by Country
st.header('1. Transaction Value by Country')
top_countries = filtered_df.groupby('Country')['Value'].sum().nlargest(10)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_countries.index, y=top_countries.values, palette='viridis', ax=ax)
ax.set_title('Top 10 Countries by Transaction Value', fontsize=16)
ax.set_xticklabels(top_countries.index, rotation=45, ha='right', fontsize=12)
ax.set_ylabel('Total Transaction Value', fontsize=14)
st.pyplot(fig)

# Visualization 2: Correlation Between Quantity and Value
st.header('2. Correlation Between Quantity and Transaction Value')
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=filtered_df, x='Quantity', y='Value', color='orange', ax=ax)
ax.set_title('Correlation Between Quantity and Transaction Value', fontsize=14)
ax.set_xlabel('Quantity', fontsize=12)
ax.set_ylabel('Transaction Value', fontsize=12)
st.pyplot(fig)

# Visualization 3: Shipping Method Impact on Transaction Value
st.header('3. Shipping Method Impact on Transaction Value')
shipping_agg = filtered_df.groupby('Shipping_Method')['Value'].sum()
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=shipping_agg.index, y=shipping_agg.values, palette='Dark2', ax=ax)
ax.set_title('Shipping Method Impact on Transaction Value', fontsize=14)
ax.set_xlabel('Shipping Method', fontsize=12)
ax.set_ylabel('Total Transaction Value', fontsize=12)
st.pyplot(fig)

# Visualization 4: Top Products by Transaction Value
st.header('4. Top Products by Transaction Value')
top_products = filtered_df.groupby('Product')['Value'].sum().nlargest(5)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_products.values, y=top_products.index, palette='Paired', ax=ax)
ax.set_title('Top 5 Products by Transaction Value', fontsize=16)
ax.set_xlabel('Total Transaction Value', fontsize=12)
ax.set_ylabel('Product', fontsize=12)
st.pyplot(fig)

# Visualization 5: Top Suppliers by Transaction Value
st.header('5. Top Suppliers by Transaction Value')
top_suppliers = filtered_df.groupby('Supplier')['Value'].sum().nlargest(10)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_suppliers.index, y=top_suppliers.values, palette='Set3', ax=ax)
ax.set_title('Top 10 Suppliers by Transaction Value', fontsize=16)
ax.set_xlabel('Supplier', fontsize=12)
ax.set_ylabel('Total Transaction Value', fontsize=12)
ax.set_xticklabels(top_suppliers.index, rotation=45, ha='right', fontsize=10)
st.pyplot(fig)

# Visualization 6: Import vs Export Revenue Share
st.header('6. Import vs Export Revenue Share')
import_export_agg = filtered_df.groupby('Import_Export')['Value'].sum()
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(import_export_agg, labels=import_export_agg.index, autopct='%1.1f%%', startangle=140,
       colors=sns.color_palette('husl'), explode=[0.05, 0.05], shadow=True, textprops={'fontsize': 14})
ax.set_title('Import vs Export Revenue Share', fontsize=16)
st.pyplot(fig)

# Visualization 7: Top 10 Transaction Volume by Port
st.header('7. Top 10 Transaction Volume by Port')
port_agg = filtered_df.groupby('Port')['Transaction_ID'].count().nlargest(10)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=port_agg.index, y=port_agg.values, palette='Set1', ax=ax)
ax.set_title('Top 10 Transaction Volume by Port', fontsize=16)
ax.set_xlabel('Port', fontsize=12)
ax.set_ylabel('Number of Transactions', fontsize=12)
ax.set_xticklabels(port_agg.index, rotation=45, ha='right', fontsize=10)
st.pyplot(fig)

# Visualization 8: Weight vs Transaction Value
st.header('8. Weight vs Transaction Value')
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=filtered_df, x='Weight', y='Value', color='purple', ax=ax)
ax.set_title('Weight vs Transaction Value', fontsize=14)
ax.set_xlabel('Weight', fontsize=12)
ax.set_ylabel('Transaction Value', fontsize=12)
st.pyplot(fig)

# Visualization 9: Payment Terms Distribution by Country
st.header('9. Payment Terms Distribution by Country')
payment_terms_count = filtered_df['Payment_Terms'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=payment_terms_count.index, y=payment_terms_count.values, palette='viridis', ax=ax)
ax.set_title('Count of Countries by Payment Terms', fontsize=16)
ax.set_xlabel('Payment Terms (Days)', fontsize=12)
ax.set_ylabel('Count of Countries', fontsize=12)
ax.set_xticklabels(payment_terms_count.index, rotation=45, ha='right', fontsize=10)
st.pyplot(fig)

# Visualization 10: Top Customers by Transaction Value
st.header('10. Top 5 Customers by Transaction Value')
top_customers = filtered_df.groupby('Customer')['Value'].sum().nlargest(5)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_customers.values, y=top_customers.index, palette='Blues', ax=ax)
ax.set_title('Top 5 Customers by Transaction Value', fontsize=16)
ax.set_xlabel('Total Transaction Value', fontsize=12)
ax.set_ylabel('Customer', fontsize=12)
st.pyplot(fig)