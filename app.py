import streamlit as st
import snowflake.connector
import pandas as pd

# ==============================
# CONNECT TO SNOWFLAKE (ENVIRONMENT CONFIGURED)
# ==============================
conn = snowflake.connector.connect()  # Uses environment variables or session context


@st.cache_data(ttl=300)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        df = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])
    return df


# ==============================
# STREAMLIT UI SETUP
# ==============================
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Dashboard")

# Sidebar navigation
pages = ["Sales Summary", "Order Insights", "Top Products", "Monthly Sales Growth"]
page = st.sidebar.radio("Select Dashboard", pages)


# ==============================
# FUNCTIONS FOR DASHBOARDS
# ==============================

def sales_summary():
    st.header("📈 Sales Summary by Region and Product")

    # Fetch regions and products dynamically
    regions_query = "SELECT DISTINCT region FROM sales_db.gold.sales_gold"
    products_query = "SELECT DISTINCT product_id FROM sales_db.gold.sales_gold"

    regions = ["All"] + [row["REGION"] for row in run_query(regions_query).to_dict("records")]
    products = ["All"] + [row["PRODUCT_ID"] for row in run_query(products_query).to_dict("records")]

    # Select filters
    region = st.selectbox("Select Region", regions)
    product = st.selectbox("Select Product", products)

    # Build query based on filter
    query = "SELECT region, product_id, month, total_sales FROM sales_db.gold.sales_gold"
    conditions = []

    if region != "All":
        conditions.append(f"region = '{region}'")

    if product != "All":
        conditions.append(f"product_id = '{product}'")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY month"

    df = run_query(query)

    if df.empty:
        st.warning("No data available.")
    else:
        pivot_df = df.pivot_table(
            values="TOTAL_SALES",
            index="MONTH",
            columns="PRODUCT_ID",
            fill_value=0
        )
        st.line_chart(pivot_df, use_container_width=True)


def order_insights():
    st.header("🔍 Order Insights")

    df = run_query("""
        SELECT order_priority, payment_method, COUNT(*) AS num_orders
        FROM sales_db.silver.sales_silver
        GROUP BY order_priority, payment_method
        ORDER BY order_priority, payment_method
    """)

    if df.empty:
        st.warning("No data available.")
    else:
        st.dataframe(df, use_container_width=True)
        st.bar_chart(df, x="ORDER_PRIORITY", y="NUM_ORDERS", use_container_width=True)


def top_products():
    st.header("🏆 Top Products by Sales")

    df = run_query("""
        SELECT product_id, SUM(total_sales) AS total_sales
        FROM sales_db.gold.sales_gold
        GROUP BY product_id
        ORDER BY total_sales DESC
        LIMIT 10
    """)

    if df.empty:
        st.warning("No data available.")
    else:
        st.dataframe(df, use_container_width=True)
        st.bar_chart(df, x="PRODUCT_ID", y="TOTAL_SALES", use_container_width=True)


def monthly_sales_growth():
    st.header("📊 Monthly Sales Growth")

    df = run_query("""
        SELECT month, SUM(total_sales) AS total_sales
        FROM sales_db.gold.sales_gold
        GROUP BY month
        ORDER BY month
    """)

    if df.empty:
        st.warning("No data available.")
    else:
        st.line_chart(df.set_index("MONTH"), use_container_width=True)


# ==============================
# RENDER SELECTED PAGE
# ==============================

if page == "Sales Summary":
    sales_summary()

elif page == "Order Insights":
    order_insights()

elif page == "Top Products":
    top_products()

elif page == "Monthly Sales Growth":
    monthly_sales_growth()