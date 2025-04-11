# 📊 Stock Analytics Dashboard

An interactive Streamlit dashboard for analyzing stock performance metrics using Python, Pandas, SQL, and TiDB Cloud. This project helps visualize top gainers/losers, volatility, cumulative returns, sector-wise performance, and more for Nifty 50 stocks.

---

## 📁 Project Structure

STOCK/ ├── app.py # Streamlit dashboard ├── model.ipynb # Data cleaning & analysis ├── cleaned_csv/ # Cleaned intermediate datasets ├── data/ # Source files (YAML/CSV) ├── output1_csv/ # Final processed CSVs ├── combined_stocks.csv ├── correlation_matrix.csv ├── cumulative_returns_by_date.csv ├── market_summary.csv ├── monthly_top5_gainers.csv ├── monthly_top5_losers.csv ├── sector_wise_performance.csv ├── stock_price_correlation_pairs.csv ├── top_10_green_stocks.csv ├── top_10_loss_stocks.csv ├── top_10_volatile_stocks.csv ├── yearly_returns.csv


---

## 🚀 Features

- ✅ Visualize most volatile stocks
- ✅ Track cumulative returns by date
- ✅ Compare sector-wise yearly performance
- ✅ Analyze stock price correlation
- ✅ View monthly top gainers and losers

---

## 🧰 Tech Stack

- **Frontend**: Streamlit  
- **Backend**: Python, Pandas  
- **Database**: TiDB Cloud (MySQL-compatible)  
- **Visualization**: Seaborn, Matplotlib  
- **Connector**: `mysql.connector`

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/stock-analysis.git
```

## 📥 Dataset Download & Setup

Go to this Google Drive link and download the dataset:  
👉 [Dataset Drive Link](https://drive.google.com/drive/folders/1dfLGdGNeHmkuf4-7jZT6KYl6aU-t2v6M)

Extract the contents and copy the `data` folder into the root of your project directory:

stock-analysis/ ├── data/ ← place it here


---

## 📘 Run the Notebook for Data Processing

Run the following Jupyter Notebook to process and clean the data:

```bash
run model.ipynb
```

This will generate all required CSV files under cleaned_csv/ and output1_csv/.


🔗 TiDB SQL Configuration
Update your DB config inside app.py like this:
```
mysql.connector.connect(
    host='your_tidb_host',
    user='your_user',
    password='your_password',
    database='stocks_analysis',
    port=4000
)
```

▶️ Launch Streamlit Dashboard
Once data preprocessing is done, launch the dashboard with:

```bash
streamlit run app.py
```

📷 Streamlit Dashboard Preview
Here’s a sneak peek of the interactive dashboard built with Streamlit:

