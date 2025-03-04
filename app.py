import streamlit as st
import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt

# Load Data from JSON
@st.cache_data
def load_data():
    with open("data.json", "r") as file:
        data = json.load(file)
    return pd.DataFrame(data)

df = load_data()

# Streamlit App Layout
st.title("Supermarket Prices Dashboard 🛒💰")

# Display raw data
st.subheader("📋 Raw Data")
st.dataframe(df)

# Average price per category
st.subheader("📊 Average Price by Category")
category_avg = df.groupby("Item Category")["Item Price"].mean().reset_index()

# Bar Chart
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x="Item Category", y="Item Price", data=category_avg, palette="viridis", ax=ax)
plt.xticks(rotation=45)
plt.xlabel("Category")
plt.ylabel("Avg Price (TTD)")
plt.title("Average Price by Category")
st.pyplot(fig)

# Most Expensive & Cheapest Items
st.subheader("🔥 Top 5 Most Expensive Items")
st.table(df.nlargest(5, 'Item Price')[["Item Type", "Item Price"]])

st.subheader("💸 Top 5 Cheapest Items")
st.table(df.nsmallest(5, 'Item Price')[["Item Type", "Item Price"]])

# Filter by category
st.subheader("🔍 Filter by Category")
selected_category = st.selectbox("Choose a Category:", df["Item Category"].unique())
filtered_data = df[df["Item Category"] == selected_category]
st.dataframe(filtered_data)

