import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Stock Analytics Dashboard", layout="wide")

@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host='gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
        user='2Djg5GyoVwWC4gN.root',
        password='JWYIDlQjiVFU2pUD',
        database='stocks_analysis',
        port=4000
    )

conn = get_connection()
cursor = conn.cursor()

option = st.sidebar.selectbox(
    "Select Analysis",
    [
        "1. Volatility Analysis",
        "2. Cumulative Return Over Time",
        "3. Sector-wise Performance",
        "4. Stock Price Correlation",
        "5. Monthly Top Gainers & Losers"
    ]
)

# === 1. Volatility Analysis ===
if option == "1. Volatility Analysis":
    st.header("Top 10 Most Volatile Stocks")

    df = pd.read_sql("SELECT * FROM top_10_volatile_stocks", conn)
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(x='symbol', y='volatility', data=df.sort_values('volatility', ascending=False), palette='magma', ax=ax)
    for container in ax.containers:
        ax.bar_label(container, fmt='%.4f', label_type='edge', padding=3)
    
    plt.xticks(rotation=45)
    ax.set_title("Top 10 Volatile Stocks")
    st.pyplot(fig)

# === 2. Cumulative Return Over Time ===
elif option == "2. Cumulative Return Over Time":
    st.header("Cumulative Return Over Time (Top 5 Performing Stocks)")

    df = pd.read_sql("SELECT date, symbol, cumulative_return FROM cumulative_returns_by_date", conn)
    df['date'] = pd.to_datetime(df['date'])

    top_5_symbols = df.groupby('symbol')['cumulative_return'].last().sort_values(ascending=False).head(5).index.tolist()
    df = df[df['symbol'].isin(top_5_symbols)]
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=df, x='date', y='cumulative_return', hue='symbol', ax=ax)
    ax.set_title("Cumulative Returns Over Time for Top 5 Stocks")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Return")
    ax.legend(title="Stock Symbol")
    st.pyplot(fig)

# === 3. Sector-wise Performance ===
elif option == "3. Sector-wise Performance":
    st.header("Average Yearly Return by Sector")

    df = pd.read_sql("SELECT * FROM sector_wise_performance", conn)  

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='sector', y='average_return', data=df.sort_values('average_return', ascending=False), palette='coolwarm', ax=ax)

    for container in ax.containers:
        labels = [f"{v.get_height():.2f}" for v in container]
        ax.bar_label(container, labels=labels, label_type="edge", fontsize=9, padding=3)

    ax.set_title("Average Yearly Return by Sector", fontsize=16)
    ax.set_xlabel("Sector", fontsize=12)
    ax.set_ylabel("Average Return", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)


elif option == "4. Stock Price Correlation":
    st.title("Stock Price Correlation Analysis")

    query = "SELECT * FROM correlation_matrix"  # table name as per your structure
    df_corr = pd.read_sql(query, conn, index_col='symbol')
    conn.close()

    # Plot the heatmap
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(df_corr, annot=False, cmap='coolwarm', center=0, linewidths=0.5)
    ax.set_title("Stock Price Correlation Heatmap")
    st.pyplot(fig)


# === 5. Monthly Top Gainers & Losers ===
elif option == "5. Monthly Top Gainers & Losers":
    st.header("Monthly Top 5 Gainers and Losers")

    # === Load data from TiDB === 
    gainers_df = pd.read_sql("SELECT * FROM monthly_top5_gainers", conn)
    losers_df = pd.read_sql("SELECT * FROM monthly_top5_losers", conn)

    # Ensure consistent types
    gainers_df['month'] = gainers_df['month'].astype(str)
    losers_df['month'] = losers_df['month'].astype(str)

    # Custom month ordering: "2023-01" to "2023-12"
    months_order = [
        "2023-10", "2023-11", "2023-12", "2024-01", "2024-02", "2024-03",
        "2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09","2024-10","2024-10","2024-11"
    ]

    # === Generate charts month by month ===
    for month in months_order:
        gainers = gainers_df[gainers_df['month'] == month]
        losers = losers_df[losers_df['month'] == month]

        if not gainers.empty and not losers.empty:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader(f"Top 5 Gainers - {month}")
                fig1, ax1 = plt.subplots()
                sns.barplot(x='symbol', y='monthly_return', data=gainers, palette='Greens_d', ax=ax1)
                ax1.set_ylabel("Return (%)")
                ax1.set_xlabel("Stock")
                ax1.set_title(f"Top 5 Gainers - {month}")
                st.pyplot(fig1)

            with col2:
                st.subheader(f"Top 5 Losers - {month}")
                fig2, ax2 = plt.subplots()
                sns.barplot(x='symbol', y='monthly_return', data=losers, palette='Reds_d', ax=ax2)
                ax2.set_ylabel("Return (%)")
                ax2.set_xlabel("Stock")
                ax2.set_title(f"Top 5 Losers - {month}")
                st.pyplot(fig2) 