# 📊 Snowflake Sales Data Pipeline & Streamlit Dashboard

This project demonstrates an end-to-end **Data Engineering pipeline
using Snowflake** with the **Medallion Architecture (Bronze, Silver,
Gold)** and a **Streamlit dashboard** for visualization.

The pipeline automatically ingests raw sales data, processes it through
multiple layers, and presents insights through an interactive dashboard.

------------------------------------------------------------------------

# 🚀 Project Architecture

This project follows the **Medallion Architecture**:

Raw Data → Bronze Layer → Silver Layer → Gold Layer → Streamlit
Dashboard

### 1️⃣ Bronze Layer

Stores raw ingested sales data from CSV files.

### 2️⃣ Silver Layer

Cleans and transforms the raw data into structured format.

### 3️⃣ Gold Layer

Creates aggregated data for analytics and reporting.

------------------------------------------------------------------------

# 🧱 Snowflake Components Used

This project uses several Snowflake features:

-   Snowflake Database & Schemas
-   Internal Stage
-   COPY INTO command
-   Streams (for Change Data Capture)
-   Tasks (for automated scheduling)
-   MERGE statements for incremental updates

------------------------------------------------------------------------

# 🗂 Database Structure

Database: `SALES_DB`

Schemas:

-   `BRONZE` → Raw Data
-   `SILVER` → Cleaned Data
-   `GOLD` → Aggregated Data

Tables:

SALES_DB

BRONZE\
• SALES_BRONZE\
• SALES_BRONZE_STREAM

SILVER\
• SALES_SILVER\
• SALES_SILVER_STREAM

GOLD\
• SALES_GOLD

------------------------------------------------------------------------

# ⚙️ Data Pipeline Flow

## Step 1: Data Ingestion (Bronze Layer)

Raw CSV files are loaded into Snowflake using:

COPY INTO SALES_DB.BRONZE.SALES_BRONZE FROM @SALES_DB.BRONZE.SALES_STAGE

A **Snowflake Task** runs every **1 minute** to ingest data.

------------------------------------------------------------------------

## Step 2: Data Transformation (Silver Layer)

The Silver layer:

-   Converts data types
-   Cleans invalid records
-   Calculates additional fields

Examples:

-   TOTAL_AMOUNT
-   ORDER_PRIORITY

Example transformation:

QUANTITY \* PRICE AS TOTAL_AMOUNT

------------------------------------------------------------------------

## Step 3: Aggregation (Gold Layer)

The Gold layer generates analytical tables such as:

-   Monthly Sales
-   Total Quantity
-   Sales by Region & Product

It uses a **MERGE statement** for incremental updates.

------------------------------------------------------------------------

# 🔄 Real-Time Processing

The pipeline uses:

## Streams

Capture changes in tables.

## Tasks

Automate processing every minute.

Example condition:

WHEN SYSTEM\$STREAM_HAS_DATA('SALES_DB.BRONZE.SALES_BRONZE_STREAM')

This ensures only **new data** is processed.

------------------------------------------------------------------------

# 📊 Streamlit Dashboard

The project includes a **Streamlit dashboard** connected to Snowflake.

## Dashboard Features

### 1️⃣ Sales Summary

Sales trends by region and product.

### 2️⃣ Order Insights

Order priority distribution and payment method analysis.

### 3️⃣ Top Products

Top 10 products by revenue.

### 4️⃣ Monthly Sales Growth

Monthly sales trend visualization.

------------------------------------------------------------------------

# 🛠 Tech Stack

### Data Warehouse

Snowflake

### Data Processing

Snowflake SQL\
Streams\
Tasks

### Programming

Python

### Visualization

Streamlit\
Pandas

------------------------------------------------------------------------

# 📦 Python Libraries

Install dependencies:

pip install streamlit\
pip install snowflake-connector-python\
pip install pandas

------------------------------------------------------------------------

# ▶️ Running the Streamlit App

Run the dashboard locally:

streamlit run app.py

------------------------------------------------------------------------

# 📁 Project Structure

project-folder

├── snowflake_pipeline.sql\
├── app.py\
├── README.md\
└── data/\
    └── sales_data.csv

------------------------------------------------------------------------

# 📈 Example Insights

The dashboard provides insights such as:

-   Regional sales performance
-   Best selling products
-   Monthly sales trends
-   Order priority distribution

------------------------------------------------------------------------

# 🎯 Learning Outcomes

This project demonstrates:

-   Modern Data Engineering architecture
-   Real-time data pipelines
-   Snowflake Streams & Tasks
-   Data transformation pipelines
-   Interactive dashboards with Streamlit

------------------------------------------------------------------------

# 👨‍💻 Author

Muhammad Yaseen
