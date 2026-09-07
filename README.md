# 🛒 Supermarket Sales Analysis Dashboard

A comprehensive, interactive Streamlit analytics platform built using **IBM BOB** to process, validate, and visualize retail sales data. This project delivers an end-to-end data pipeline—ranging from dataset quality checks and re-computed revenue validation to dynamic data visualization and automated executive business recommendations.

---

## 🌟 Key Features

* **Interactive Multi-Filter Sidebar**: Dynamically slice data across multiple dimensions including Branches ($A, B, C, D$), Cities, Categories, Payment Methods, and Customer Types.


* **Automated Data Quality Audits**: Detects missing values, duplicate rows, data type anomalies, and numerical boundary violations in real time.


* **Sales Revenue Validation Engine**: Automatically recalculates revenue ($\text{Calculated Sales} = \text{Quantity} \times \text{Unit Price}$) to guard against manual CSV data entry errors.


* **Interactive Data Visualizations**: Built-in Plotly charts covering monthly trends, revenue distribution, payment method breakdowns, gender vs. category sales heatmaps, and rating analysis.


* **Executive Decision Support**: Auto-generates actionable business recommendations for inventory allocation, category strategy, customer loyalty conversion, and seasonal planning.


* **Data Export Capabilities**: Allows users to filter dataset subsets in real time and export clean CSV reports on demand.



---

## 📊 Dashboard Modules & PDF Reports

The application is structured into 5 dedicated tabs. PDF output reports generated per section are included below:

| Dashboard Section | Primary Functionality | Exported Report PDF |
| --- | --- | --- |
| **1. 📋 Overview** | High-level KPI metrics (Total Sales, Order Value, Ratings) & Raw Data Inspector.

 | `overview.pdf`<br> |
| **2. 🔎 Data Quality** | Null check summary, duplicate scanner, data type table & range validation.

 | `data quality page.pdf`<br> |
| **3. 💰 Sales Analysis** | Granular revenue aggregations by Branch, Category, Payment Method, and Customer Type.

 | `sales analysis.pdf`<br> |
| **4. 📊 Charts** | 10 interactive Plotly charts (Monthly trend line, branch bar chart, heatmaps, scatter plots).

 | `charts dashboard.pdf`<br> |
| **5. 🏆 Business Insights** | Automated strategic recommendations & quick insight summary matrix.

 | `business insights.pdf`<br> |

---

## 🏗️ Project Structure

```text
├── app.py                            # Streamlit application main script
├── supermarket_sales_10500_rows.csv  # Supermarket transaction dataset (10,500 records)
├── overview.pdf                      # Exported PDF report - Overview tab
├── data quality page.pdf             # Exported PDF report - Data Quality tab
├── sales analysis.pdf                # Exported PDF report - Sales Analysis tab
├── charts dashboard.pdf              # Exported PDF report - Charts tab
├── business insights.pdf             # Exported PDF report - Business Insights tab
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation

```

---

## 🛠️ Tech Stack & Development Tooling

* **Built With**: **IBM BOB** (Developer Tooling Environment)
* **Frontend Framework**: [Streamlit](https://streamlit.io/) (Custom CSS styling & responsive tab layout)


* **Data Processing**: `pandas`, `numpy`

* **Visualization Engine**: `plotly.express`, `plotly.graph_objects`


---

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.8+ installed on your system.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/supermarket-sales-analysis.git
cd supermarket-sales-analysis

```

### 2. Install Dependencies

Create a `requirements.txt` file or run:

```bash
pip install streamlit pandas plotly

```

### 3. Run the Dashboard

Launch the Streamlit web application:

```bash
streamlit run app.py

```

Open your browser and navigate to `http://localhost:8501`.

---

## 💡 Key Business Insights Generated

* **Top Performing Branch**: Branch C generated the highest revenue (~₹1.53M), while Branch A required strategic intervention (~₹1.12M).


* **Category Dominance**: Beverages led total product category revenue, whereas Bakery accounted for the lowest revenue share.


* **Payment Preference**: Net Banking and UPI accounted for over 50% of total payment transactions.


* **Customer Retention**: Member and Normal customers contributed almost equally (~50.8% vs 49.2%), presenting an opportunity for targeted loyalty program conversions.
