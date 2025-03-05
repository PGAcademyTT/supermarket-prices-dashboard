import streamlit as st
import pandas as pd 
import pymongo
import matplotlib.pyplot as plt
import seaborn as sns

# MongoDB Connection URI (Replace with your actual URI)
MONGO_URI = "mongodb+srv://pipsglobally:ueEbdPP8nWF3oeXC@cluster0.hu59d.mongodb.net/supermarket_db?retryWrites=true&w=majority"


# Connect to MongoDB
@st.cache_data
def get_database():
    client = pymongo.MongoClient(MONGO_URI)
    db = client["supermarket_db"]  # Database Name
    return db

# Fetch Data from MongoDB
@st.cache_data
def load_data():
    db = get_database()
    collection = db["prices"]  # Collection Name
    data = list(collection.find({}, {"_id": 0}))  # Fetch all records, excluding MongoDB's default `_id`
    return pd.DataFrame(data)

df = load_data()

# Streamlit App Layout
st.title("Supermarket Prices Dashboard 🛒💰")

# Display raw data
st.subheader("📋 Raw Data from MongoDB")
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
