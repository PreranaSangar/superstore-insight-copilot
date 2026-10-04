import pandas as pd
import matplotlib.pyplot as plt


# =========================================================
# Load Dataset
# =========================================================

df = pd.read_csv("data/train.csv")


# =========================================================
# Convert Order Date to datetime
# =========================================================

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    dayfirst=True
)


# =========================================================
# DATA QUERY TOOL
# =========================================================

def data_query_tool(query_type: str):
    """
    Query the Superstore dataset.
    """

    # -----------------------------------------------------
    # Total Sales
    # -----------------------------------------------------

    if query_type == "total_sales":

        return df["Sales"].sum()


    # -----------------------------------------------------
    # Sales by Category
    # -----------------------------------------------------

    elif query_type == "sales_by_category":

        return (
            df.groupby("Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .to_dict()
        )


    # -----------------------------------------------------
    # Sales by Region
    # -----------------------------------------------------

    elif query_type == "sales_by_region":

        return (
            df.groupby("Region")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .to_dict()
        )


    # -----------------------------------------------------
    # Monthly Sales
    # -----------------------------------------------------

    elif query_type == "monthly_sales":

        return (
            df.groupby(
                df["Order Date"].dt.to_period("M")
            )["Sales"]
            .sum()
            .sort_index()
            .to_dict()
        )


    # -----------------------------------------------------
    # Invalid Query
    # -----------------------------------------------------

    else:

        return "I don't have a query for that."


# =========================================================
# CALCULATION TOOL
# =========================================================

def calculation_tool(calculation_type: str):

    # -----------------------------------------------------
    # Sales Growth
    # -----------------------------------------------------

    if calculation_type == "sales_growth":

        monthly_sales = (
            df.groupby(
                df["Order Date"].dt.to_period("M")
            )["Sales"]
            .sum()
            .sort_index()
        )

        first_month = monthly_sales.iloc[0]

        last_month = monthly_sales.iloc[-1]

        growth = (
            (last_month - first_month)
            / first_month
        ) * 100

        return f"Sales growth: {round(growth, 2)}%"


    # -----------------------------------------------------
    # Average Sales per Order
    # -----------------------------------------------------

    elif calculation_type == "average_sales":

        order_sales = (
            df.groupby("Order ID")["Sales"]
            .sum()
        )

        average_sales_per_order = order_sales.mean()

        return round(
            average_sales_per_order,
            2
        )


    # -----------------------------------------------------
    # Top 3 Products
    # -----------------------------------------------------

    elif calculation_type == "top_products":

        return (
            df.groupby("Product Name")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(3)
        )


    # -----------------------------------------------------
    # Invalid Calculation
    # -----------------------------------------------------

    else:

        return "Calculation not available."


# =========================================================
# CHART TOOL
# =========================================================

def chart_tool(chart_type: str):

    # Clean chart type
    chart_type = chart_type.strip().lower()


    # =====================================================
    # Monthly Sales Chart
    # =====================================================

    if chart_type == "monthly_sales":

        monthly_sales = (
            df.groupby(
                df["Order Date"].dt.to_period("M")
            )["Sales"]
            .sum()
            .sort_index()
        )

        plt.figure(figsize=(10, 5))

        monthly_sales.plot(
            kind="line",
            marker="o"
        )

        plt.title("Monthly Sales Trend")

        plt.xlabel("Month")

        plt.ylabel("Sales")

        plt.xticks(rotation=45)

        plt.tight_layout()

        chart_path = "monthly_sales.png"

        plt.savefig(chart_path)

        plt.close()

        return chart_path


    # =====================================================
    # Top 3 Products Chart
    # =====================================================

    elif chart_type == "top_3_products":

        top_products = (
            df.groupby("Product Name")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(3)
            .sort_values(ascending=True)
        )

        plt.figure(figsize=(12, 6))

        top_products.plot(
            kind="barh"
        )

        plt.title("Top 3 Products by Sales")

        plt.xlabel("Sales")

        plt.ylabel("Product")

        plt.tight_layout()

        chart_path = "top_3_products.png"

        plt.savefig(chart_path)

        plt.close()

        return chart_path


    # =====================================================
    # Category Sales Chart
    # =====================================================

    elif chart_type == "category_sales":

        category_sales = (
            df.groupby("Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        plt.figure(figsize=(8, 5))

        category_sales.plot(
            kind="bar"
        )

        plt.title("Sales by Category")

        plt.xlabel("Category")

        plt.ylabel("Sales")

        plt.tight_layout()

        chart_path = "category_sales.png"

        plt.savefig(chart_path)

        plt.close()

        return chart_path


    # =====================================================
    # Region Sales Chart
    # =====================================================

    elif chart_type == "region_sales":

        region_sales = (
            df.groupby("Region")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        plt.figure(figsize=(8, 5))

        region_sales.plot(
            kind="bar"
        )

        plt.title("Sales by Region")

        plt.xlabel("Region")

        plt.ylabel("Sales")

        plt.tight_layout()

        chart_path = "region_sales.png"

        plt.savefig(chart_path)

        plt.close()

        return chart_path


    # =====================================================
    # Invalid Chart Type
    # =====================================================

    else:

        return (
            f"Chart type '{chart_type}' not available."
        )