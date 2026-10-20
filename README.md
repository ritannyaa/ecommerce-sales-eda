# 📊 E-Commerce Sales & Customer Performance: Exploratory Data Analysis (EDA)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-1.24%2B-013243?logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange)
![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Plots-blueviolet)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter)

## 📌 Executive Summary
This project presents an **Exploratory Data Analysis (EDA) and Data Visualization** study on a multi-category retail e-commerce business dataset (**Global Superstore**). The project investigates the interplay between sales volume, customer segments, regional distribution, promotional discounts, product profitability, and shipping logistics.

The objective is to provide actionable business intelligence that can help managers improve profit margins, avoid revenue leaks caused by excessive discounts, and optimize inventory and shipping operations.

---

## 🗂️ Project Repository Structure

```text
ecommerce-sales-eda/
│
├── data/
│   └── superstore_sales.csv            # Cleaned transactional dataset (9,994 records)
│
├── notebooks/
│   └── ecommerce_sales_analysis.ipynb  # Interactive Jupyter Notebook with executed outputs
│
├── src/
│   └── run_eda.py                      # Standalone Python script for end-to-end analysis
│
├── visualizations/                     # High-resolution (300 DPI) exported charts
│   ├── 01_monthly_sales_trend.png
│   ├── 02_sales_and_profit_by_category.png
│   ├── 03_sub_category_profitability.png
│   ├── 04_customer_segment_distribution.png
│   ├── 05_regional_performance.png
│   ├── 06_discount_vs_profit_margin.png
│   ├── 07_shipping_mode_analysis.png
│   └── 08_correlation_matrix.png
│
├── requirements.txt                    # Python library dependencies
├── .gitignore                          # Standard git ignore rules
└── README.md                           # Comprehensive project documentation
```

---

## 📊 Dataset Overview

- **Source:** Superstore Retail Sales Dataset
- **Records:** 9,994 completed orders (2015 – 2018)
- **Features (21 columns):**
  - **Order Details:** `Order ID`, `Order Date`, `Ship Date`, `Ship Mode`
  - **Customer Details:** `Customer ID`, `Customer Name`, `Segment`, `Country`, `City`, `State`, `Postal Code`, `Region`
  - **Product Details:** `Product ID`, `Category`, `Sub-Category`, `Product Name`
  - **Financial Metrics:** `Sales`, `Quantity`, `Discount`, `Profit`
- **Engineered Metrics:** `Shipping Days`, `Profit Margin (%)`, `Order Year`, `Order Month`, `Discount Tier`

---

## 🔍 Key Findings & Visual Insights

### 1. Sales & Profit Seasonality
- **Finding:** Clear annual cyclicality with notable sales and profit peaks in Q4 (September – December).
- **Reason:** Year-end holiday purchasing and annual corporate budget utilization.
- 📈 *Visualization:* `visualizations/01_monthly_sales_trend.png`

### 2. Category Performance vs. Margin Paradox
- **Technology** generates the highest total profit ($145.5k) and healthy margins.
- **Furniture** produces substantial revenue ($742k) but delivers low profits ($18.5k) due to low margin sub-categories.
- 📈 *Visualization:* `visualizations/02_sales_and_profit_by_category.png`

### 3. The Loss Leaders (Sub-Category Analysis)
- **High-Profit Drivers:** `Copiers` (+$55.6k), `Phones` (+$44.5k), `Accessories` (+$41.9k).
- **Loss Leaders:** `Tables` (-$17.7k), `Bookcases` (-$3.5k), and `Supplies` (-$1.2k).
- 📈 *Visualization:* `visualizations/03_sub_category_profitability.png`

### 4. Customer Segmentation
- **Consumer Segment:** Contributes 50.6% of overall sales and largest volume of transactions.
- **Corporate & Home Office:** Make up the remaining 49.4% with consistent order values.
- 📈 *Visualization:* `visualizations/04_customer_segment_distribution.png`

### 5. Regional Disparities
- **West:** Top-performing region with $725k in revenue and $108k in profit.
- **Central:** Generates comparable revenue to the East (~$501k) but lags heavily in profit ($39.7k) due to excessive discount depth.
- 📈 *Visualization:* `visualizations/05_regional_performance.png`

### 6. Destructive Impact of High Discounts (>20%)
- Orders with discounts between **1% and 20%** maintain positive margins (~14.8%).
- Orders with discounts **greater than 20%** suffer an average margin of **-36.7%**, causing a cumulative financial drain of **-$135,376**.
- 📈 *Visualization:* `visualizations/06_discount_vs_profit_margin.png`

### 7. Shipping Logistics
- **Standard Class** handles ~60% of all shipments with an average transit time of **5.0 days**.
- **Same Day** delivery averages **0.0 days**, serving emergency customer needs.
- 📈 *Visualization:* `visualizations/07_shipping_mode_analysis.png`

### 8. Correlation Analysis
- Strong negative correlation (**-0.53**) between `Discount` and `Profit Margin (%)`.
- `Sales` and `Profit` share a positive correlation (**+0.48**), indicating volume drives revenue but margin controls actual profitability.
- 📈 *Visualization:* `visualizations/08_correlation_matrix.png`

---

## 💡 Strategic Business Recommendations

1. **Cap Promotional Discounts:** Eliminate discounts above 20% unless used for dead-stock clearance. This single adjustment can save over $130k in profit.
2. **Restructure Furniture & Tables:** Renegotiate supplier pricing on `Tables` and `Bookcases` or bundle them with high-margin accessories to protect profitability.
3. **Scale Technology Offerings:** Expand marketing and inventory for `Technology` sub-categories (`Copiers`, `Phones`, `Accessories`) to maximize margin dollars.
4. **Targeted Regional Interventions:** Audit discount approvals in the `Central` region to bring profit margins in line with the `West` and `East`.
5. **Customer Loyalty Incentives:** Introduce tiered B2B corporate rewards to increase frequency in the Corporate and Home Office customer groups.

---

## 🚀 How to Run the Project Locally

### 1. Clone the Repository
```bash
git clone <YOUR_REPOSITORY_URL>
cd ecommerce-sales-eda
```

### 2. Set Up Virtual Environment (Recommended)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Analysis via Script
To regenerate all 8 charts and view terminal summary:
```bash
python src/run_eda.py
```

### 5. Run via Jupyter Notebook
To explore interactively:
```bash
jupyter notebook notebooks/ecommerce_sales_analysis.ipynb
```

---

## 🛠️ Technologies Used
- **Language:** Python 3.10+
- **Data Manipulation:** Pandas, NumPy
- **Data Visualization:** Matplotlib, Seaborn
- **Development Environment:** Jupyter Notebook / Visual Studio Code

---

## 📄 License & Attribution
This project was developed for educational and academic submission purposes. Dataset courtesy of the classic Global Superstore / Tableau public sample.
