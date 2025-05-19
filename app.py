
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("Customer Churn Analysis Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Customer Churn.csv")
    df["TotalCharges"] = df["TotalCharges"].replace(" ", "0")
    df["TotalCharges"] = df["TotalCharges"].astype("float")
    df["SeniorCitizen"] = df["SeniorCitizen"].apply(lambda x: "yes" if x == 1 else "no")
    return df

df = load_data()

st.subheader("Data Preview")
st.dataframe(df.head())

# Churn Count Plot
st.subheader("Churn Count Plot")
fig1, ax1 = plt.subplots()
sns.countplot(x='Churn', data=df, ax=ax1)
ax1.bar_label(ax1.containers[0])
st.pyplot(fig1)

# Churn Pie Chart
st.subheader("Churn Distribution Pie Chart")
gb = df.groupby("Churn").agg({'Churn':"count"})
fig2, ax2 = plt.subplots()
ax2.pie(gb['Churn'], labels=gb.index, autopct="%1.2f%%")
ax2.set_title("Percentage of Churned Customers")
st.pyplot(fig2)

# Churn by Gender
st.subheader("Churn by Gender")
fig3, ax3 = plt.subplots()
sns.countplot(x='gender', data=df, hue='Churn', ax=ax3)
st.pyplot(fig3)

# Senior Citizen Count
st.subheader("Senior Citizen Count")
fig4, ax4 = plt.subplots()
sns.countplot(x='SeniorCitizen', data=df, ax=ax4)
ax4.bar_label(ax4.containers[0])
st.pyplot(fig4)

# Churn by Senior Citizen - Stacked Bar Chart
st.subheader("Churn by Senior Citizen - Percentage")
total_counts = df.groupby('SeniorCitizen')['Churn'].value_counts(normalize=True).unstack() * 100
fig5, ax5 = plt.subplots()
total_counts.plot(kind='bar', stacked=True, ax=ax5, color=['#1f77b4', '#ff7f0e'])
for p in ax5.patches:
    width, height = p.get_width(), p.get_height()
    x, y = p.get_xy()
    ax5.text(x + width / 2, y + height / 2, f'{height:.1f}%', ha='center', va='center')
ax5.set_title('Churn by Senior Citizen (Stacked)')
ax5.set_xlabel('SeniorCitizen')
ax5.set_ylabel('Percentage')
ax5.legend(title='Churn')
st.pyplot(fig5)

# Tenure Distribution
st.subheader("Tenure Distribution")
fig6, ax6 = plt.subplots(figsize=(10, 4))
sns.histplot(x='tenure', data=df, bins=72, hue='Churn', ax=ax6)
st.pyplot(fig6)

# Contract Type
st.subheader("Churn by Contract Type")
fig7, ax7 = plt.subplots()
sns.countplot(x='Contract', data=df, hue='Churn', ax=ax7)
ax7.bar_label(ax7.containers[0])
st.pyplot(fig7)

# Services Analysis
st.subheader("Churn by Various Services")
columns = ['PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
           'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
n_cols = 3
n_rows = (len(columns) + n_cols - 1) // n_cols
fig8, axes = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 4))
axes = axes.flatten()

for i, col in enumerate(columns):
    sns.countplot(x=col, data=df, hue='Churn', ax=axes[i])
    axes[i].set_title(f"{col} vs Churn")

for j in range(i+1, len(axes)):
    fig8.delaxes(axes[j])

st.pyplot(fig8)
