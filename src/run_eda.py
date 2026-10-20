"""
E-Commerce Sales & Customer Insights: Exploratory Data Analysis (EDA)
---------------------------------------------------------------------
Author: EDA & Visualization Student Project
Topic: Global E-Commerce Sales & Customer Behavior Analysis
Description:
    This script performs comprehensive end-to-end Exploratory Data Analysis
    on the Superstore E-Commerce dataset. It covers data cleaning,
    feature engineering, descriptive statistics, and generates 8 high-quality
    visualizations for academic presentation and business decision making.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set aesthetics
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['figure.dpi'] = 300

def load_and_clean_data(file_path):
    print("=" * 60)
    print("STEP 1: LOADING & CLEANING DATA")
    print("=" * 60)
    
    df = pd.read_csv(file_path)
    print(f"Raw dataset shape: {df.shape}")
    
    # 1. Drop rows where critical transaction fields are null (blank trailing rows)
    initial_count = len(df)
    df = df.dropna(subset=['Order ID', 'Order Date', 'Sales', 'Profit'])
    print(f"Dropped {initial_count - len(df)} empty/corrupted records. Clean shape: {df.shape}")
    
    # 2. Convert Dates
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='mixed')
    
    # 3. Clean numeric columns
    df['Sales'] = df['Sales'].astype(float)
    df['Profit'] = df['Profit'].astype(float)
    df['Discount'] = df['Discount'].astype(float)
    df['Quantity'] = df['Quantity'].astype(int)
    
    # 4. Feature Engineering
    df['Order Year'] = df['Order Date'].dt.year
    df['Order Month'] = df['Order Date'].dt.month
    df['Order YearMonth'] = df['Order Date'].dt.to_period('M')
    df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
    df['Profit Margin (%)'] = np.where(df['Sales'] > 0, (df['Profit'] / df['Sales']) * 100, 0)
    
    # Categorize discount levels
    def discount_tier(d):
        if d == 0:
            return 'No Discount (0%)'
        elif d <= 0.20:
            return 'Moderate (1-20%)'
        else:
            return 'High (>20%)'
            
    df['Discount Tier'] = df['Discount'].apply(discount_tier)
    
    print("\nSummary of Engineered Features:")
    print(f"- Time span: {df['Order Date'].min().date()} to {df['Order Date'].max().date()}")
    print(f"- Total Orders: {df['Order ID'].nunique():,}")
    print(f"- Unique Customers: {df['Customer ID'].nunique():,}")
    print(f"- Total Revenue: ${df['Sales'].sum():,.2f}")
    print(f"- Total Profit: ${df['Profit'].sum():,.2f}")
    print(f"- Overall Profit Margin: {(df['Profit'].sum() / df['Sales'].sum()) * 100:.2f}%")
    print("-" * 60)
    
    return df

def generate_visualizations(df, output_dir):
    print("\n" + "=" * 60)
    print("STEP 2: GENERATING VISUALIZATIONS")
    print("=" * 60)
    os.makedirs(output_dir, exist_ok=True)
    
    # -------------------------------------------------------------
    # Plot 1: Monthly Sales & Profit Trend Over Time
    # -------------------------------------------------------------
    print("[1/8] Generating Monthly Sales & Profit Trend...")
    monthly_data = df.groupby('Order YearMonth').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    monthly_data['YearMonth_Str'] = monthly_data['Order YearMonth'].astype(str)
    
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_data['YearMonth_Str'], monthly_data['Sales'], marker='o', color='#1f77b4', linewidth=2.5, label='Monthly Sales ($)')
    plt.plot(monthly_data['YearMonth_Str'], monthly_data['Profit'], marker='s', color='#2ca02c', linewidth=2, linestyle='--', label='Monthly Profit ($)')
    plt.title('Monthly Sales and Profit Performance Over Time', pad=15)
    plt.xlabel('Year - Month')
    plt.ylabel('Amount (USD)')
    plt.xticks(rotation=65, ha='right', fontsize=9)
    plt.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '01_monthly_sales_trend.png'), dpi=300)
    plt.close()
    
    # -------------------------------------------------------------
    # Plot 2: Total Sales vs Profit by Product Category
    # -------------------------------------------------------------
    print("[2/8] Generating Category Sales & Profit Breakdown...")
    cat_summary = df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(cat_summary['Category']))
    width = 0.35
    
    rects1 = ax.bar(x - width/2, cat_summary['Sales'], width, label='Sales', color='#2b5c8f')
    rects2 = ax.bar(x + width/2, cat_summary['Profit'], width, label='Profit', color='#38b000')
    
    ax.set_ylabel('Total Amount (USD)')
    ax.set_title('Total Sales vs. Profit Across Product Categories', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(cat_summary['Category'], fontweight='bold')
    ax.legend()
    
    # Value annotations on bars
    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f'${height/1e3:.1f}k',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
    for rect in rects2:
        height = rect.get_height()
        ax.annotate(f'${height/1e3:.1f}k',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
                    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '02_sales_and_profit_by_category.png'), dpi=300)
    plt.close()
    
    # -------------------------------------------------------------
    # Plot 3: Sub-Category Profitability Analysis (Highlighting Loss Makers)
    # -------------------------------------------------------------
    print("[3/8] Generating Sub-Category Profitability...")
    subcat_profit = df.groupby('Sub-Category')['Profit'].sum().sort_values()
    
    plt.figure(figsize=(10, 7))
    colors = ['#d90429' if val < 0 else '#2a9d8f' for val in subcat_profit.values]
    bars = plt.barh(subcat_profit.index, subcat_profit.values, color=colors, edgecolor='black', alpha=0.85)
    plt.axvline(0, color='black', linestyle='--', linewidth=1)
    plt.title('Profitability by Product Sub-Category (Loss vs. Profit Makers)', pad=15)
    plt.xlabel('Total Profit (USD)')
    plt.ylabel('Sub-Category')
    
    # Annotate numbers
    for bar in bars:
        width = bar.get_width()
        offset = 500 if width >= 0 else -3000
        ha = 'left' if width >= 0 else 'right'
        plt.text(width + offset, bar.get_y() + bar.get_height()/2, f'${width:,.0f}',
                 va='center', ha=ha, fontsize=8.5, fontweight='bold', color='black')
                 
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '03_sub_category_profitability.png'), dpi=300)
    plt.close()
    
    # -------------------------------------------------------------
    # Plot 4: Customer Segment Share (Sales & Orders)
    # -------------------------------------------------------------
    print("[4/8] Generating Customer Segment Breakdown...")
    seg_summary = df.groupby('Segment').agg({'Sales': 'sum', 'Order ID': 'nunique'}).reset_index()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    colors_donut = ['#457b9d', '#e76f51', '#2a9d8f']
    
    # Sales share donut
    ax1.pie(seg_summary['Sales'], labels=seg_summary['Segment'], autopct='%1.1f%%',
            startangle=140, colors=colors_donut, wedgeprops=dict(width=0.4, edgecolor='w'))
    ax1.set_title('Revenue Share by Customer Segment', pad=10)
    
    # Order volume bar chart
    sns.barplot(data=seg_summary, x='Segment', y='Order ID', hue='Segment', palette=['#457b9d', '#e76f51', '#2a9d8f'], legend=False, ax=ax2)
    ax2.set_title('Order Volume by Customer Segment', pad=10)
    ax2.set_ylabel('Number of Unique Orders')
    for p in ax2.patches:
        ax2.annotate(f'{int(p.get_height()):,}', (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontweight='bold')
                     
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '04_customer_segment_distribution.png'), dpi=300)
    plt.close()
    
    # -------------------------------------------------------------
    # Plot 5: Regional Sales & Profit Performance
    # -------------------------------------------------------------
    print("[5/8] Generating Regional Performance Analysis...")
    region_summary = df.groupby('Region').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    region_melt = pd.melt(region_summary, id_vars=['Region'], value_vars=['Sales', 'Profit'],
                          var_name='Metric', value_name='Total (USD)')
                          
    plt.figure(figsize=(9, 5))
    ax = sns.barplot(data=region_melt, x='Region', y='Total (USD)', hue='Metric', palette=['#1d3557', '#06d6a0'])
    plt.title('Regional Sales and Profit Comparison', pad=15)
    plt.ylabel('Amount (USD)')
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f'${height/1e3:.0f}k',
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=8.5, fontweight='bold',
                        xytext=(0, 3), textcoords='offset points')
    plt.legend(title='')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '05_regional_performance.png'), dpi=300)
    plt.close()
    
    # -------------------------------------------------------------
    # Plot 6: Impact of Discounts on Profit Margin
    # -------------------------------------------------------------
    print("[6/8] Generating Discount vs. Profit Margin Impact...")
    disc_summary = df.groupby('Discount Tier').agg(
        Avg_Profit_Margin=('Profit Margin (%)', 'mean'),
        Avg_Sales=('Sales', 'mean'),
        Order_Count=('Order ID', 'count')
    ).reindex(['No Discount (0%)', 'Moderate (1-20%)', 'High (>20%)']).reset_index()
    
    plt.figure(figsize=(9, 5))
    bar_colors = ['#2a9d8f', '#e9c46a', '#e76f51']
    bars = plt.bar(disc_summary['Discount Tier'], disc_summary['Avg_Profit_Margin'], color=bar_colors, edgecolor='gray', width=0.5)
    plt.axhline(0, color='black', linestyle='--', linewidth=1)
    plt.title('Impact of Discount Tier on Average Profit Margin (%)', pad=15)
    plt.xlabel('Discount Tier')
    plt.ylabel('Average Profit Margin (%)')
    
    for bar in bars:
        h = bar.get_height()
        va = 'bottom' if h >= 0 else 'top'
        y_pos = h + (1.5 if h >= 0 else -3.5)
        plt.text(bar.get_x() + bar.get_width()/2., y_pos, f'{h:.1f}%',
                 ha='center', va=va, fontweight='bold', fontsize=11)
                 
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '06_discount_vs_profit_margin.png'), dpi=300)
    plt.close()
    
    # -------------------------------------------------------------
    # Plot 7: Shipping Modes & Average Shipping Days
    # -------------------------------------------------------------
    print("[7/8] Generating Shipping Modes Analysis...")
    ship_summary = df.groupby('Ship Mode').agg(
        Order_Count=('Order ID', 'count'),
        Avg_Ship_Days=('Shipping Days', 'mean')
    ).sort_values('Order_Count', ascending=False).reset_index()
    
    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax2 = ax1.twinx()
    
    sns.barplot(data=ship_summary, x='Ship Mode', y='Order_Count', ax=ax1, color='#457b9d', alpha=0.85)
    sns.lineplot(data=ship_summary, x='Ship Mode', y='Avg_Ship_Days', ax=ax2, color='#e63946', marker='o', linewidth=3)
    
    ax1.set_ylabel('Number of Orders', color='#457b9d')
    ax2.set_ylabel('Average Shipping Days', color='#e63946')
    ax1.set_title('Shipping Mode Frequency vs. Average Delivery Duration', pad=15)
    ax2.grid(False)
    
    for i, row in ship_summary.iterrows():
        ax2.annotate(f"{row['Avg_Ship_Days']:.1f} days",
                     (i, row['Avg_Ship_Days']),
                     textcoords="offset points", xytext=(0, 8), ha='center',
                     fontweight='bold', color='#e63946')
                     
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '07_shipping_mode_analysis.png'), dpi=300)
    plt.close()
    
    # -------------------------------------------------------------
    # Plot 8: Numerical Features Correlation Heatmap
    # -------------------------------------------------------------
    print("[8/8] Generating Correlation Matrix Heatmap...")
    numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit', 'Shipping Days', 'Profit Margin (%)']
    corr_matrix = df[numeric_cols].corr()
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, vmin=-1, vmax=1)
    plt.title('Correlation Matrix of Quantitative Variables', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '08_correlation_matrix.png'), dpi=300)
    plt.close()
    
    print("\nAll 8 visualizations generated and saved in:", output_dir)
    print("=" * 60)

def print_key_insights(df):
    print("\n" + "=" * 60)
    print("KEY BUSINESS & ANALYTICAL FINDINGS")
    print("=" * 60)
    
    # Top sub-categories
    subcat = df.groupby('Sub-Category').agg({'Sales': 'sum', 'Profit': 'sum'}).sort_values('Profit', ascending=False)
    print(f"Top 3 Most Profitable Sub-Categories: {list(subcat.head(3).index)}")
    print(f"Top 3 Loss-Making Sub-Categories: {list(subcat.tail(3).index)}")
    
    # Region summary
    region = df.groupby('Region').agg({'Sales': 'sum', 'Profit': 'sum'})
    print(f"Highest Revenue Region: {region['Sales'].idxmax()} (${region['Sales'].max():,.2f})")
    print(f"Highest Profit Region: {region['Profit'].idxmax()} (${region['Profit'].max():,.2f})")
    
    # Discount findings
    high_disc_loss = df[df['Discount'] > 0.20]['Profit'].sum()
    print(f"Net Profit/Loss on High Discount (>20%) Transactions: ${high_disc_loss:,.2f}")
    print("=" * 60)

if __name__ == '__main__':
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'superstore_sales.csv')
    viz_dir = os.path.join(os.path.dirname(__file__), '..', 'visualizations')
    
    df_clean = load_and_clean_data(data_path)
    generate_visualizations(df_clean, viz_dir)
    print_key_insights(df_clean)
