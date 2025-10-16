from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
import polars as pl
import streamlit as st

from src.config import RAW_DATA_DIR, RAW_DATA_FILENAME

# Page configuration
st.set_page_config(
    page_title="House Sale Price Analysis", page_icon="🏠", layout="wide"
)

# Constants

DATA_PATH = RAW_DATA_DIR / RAW_DATA_FILENAME


@st.cache_data
def load_data():
    """Load the raw dataset."""
    df = pl.read_csv(
        DATA_PATH, try_parse_dates=True, infer_schema_length=10000, null_values="NA"
    )
    return df


def main():
    st.title("🏠 House Sale Price Analysis")
    st.markdown("Explore how SalePrice relates to various features in the dataset")

    # Load data
    with st.spinner("Loading data..."):
        df = load_data()

    # Sidebar
    st.sidebar.header("Configuration")

    # Get numerical and categorical columns (excluding SalePrice and Id)
    numerical_cols = [
        col
        for col in df.select(pl.col(pl.NUMERIC_DTYPES)).columns
        if col not in ["SalePrice", "Id"]
    ]
    categorical_cols = [
        col
        for col in df.columns
        if df[col].dtype in [pl.Utf8, pl.Categorical] and col != "Id"
    ]

    # Overview Section
    st.header("📊 Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Records", f"{len(df):,}")
    with col2:
        st.metric("Total Features", len(df.columns) - 1)  # Excluding SalePrice
    with col3:
        mean_price = df["SalePrice"].mean()
        st.metric("Mean Sale Price", f"${mean_price:,.0f}")
    with col4:
        median_price = df["SalePrice"].median()
        st.metric("Median Sale Price", f"${median_price:,.0f}")

    # Sale Price Distribution
    st.header("💰 Sale Price Distribution")
    col1, col2 = st.columns(2)

    with col1:
        fig_hist = px.histogram(
            df.to_pandas(),
            x="SalePrice",
            nbins=50,
            title="Sale Price Distribution",
            labels={"SalePrice": "Sale Price ($)"},
        )
        fig_hist.update_layout(showlegend=False)
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        fig_box = px.box(
            df.to_pandas(),
            y="SalePrice",
            title="Sale Price Box Plot",
            labels={"SalePrice": "Sale Price ($)"},
        )
        st.plotly_chart(fig_box, use_container_width=True)

    # Display basic statistics
    with st.expander("📈 Sale Price Statistics"):
        stats = df.select(
            [
                pl.col("SalePrice").min().alias("Min"),
                pl.col("SalePrice").max().alias("Max"),
                pl.col("SalePrice").mean().alias("Mean"),
                pl.col("SalePrice").median().alias("Median"),
                pl.col("SalePrice").std().alias("Std Dev"),
                pl.col("SalePrice").quantile(0.25).alias("Q1"),
                pl.col("SalePrice").quantile(0.75).alias("Q3"),
            ]
        )
        st.dataframe(stats.to_pandas().T, use_container_width=True)

    # Numerical Features Analysis
    st.header("🔢 Sale Price vs Numerical Features")

    # Select top correlated features
    df_pandas = df.to_pandas()
    numeric_df = df_pandas.select_dtypes(include=["int64", "float64"])
    correlations = numeric_df.corr()["SalePrice"].sort_values(ascending=False)
    top_features = correlations[
        1:11
    ].index.tolist()  # Top 10 excluding SalePrice itself

    # Feature selection
    selected_numerical = st.sidebar.multiselect(
        "Select Numerical Features to Compare",
        options=numerical_cols,
        default=top_features[:5] if len(top_features) >= 5 else top_features,
    )

    if selected_numerical:
        # Create scatter plots
        num_cols = 2
        num_rows = (len(selected_numerical) + 1) // 2

        for i in range(0, len(selected_numerical), num_cols):
            cols = st.columns(num_cols)
            for j, col in enumerate(cols):
                if i + j < len(selected_numerical):
                    feature = selected_numerical[i + j]
                    with col:
                        # Calculate correlation
                        corr = df_pandas[[feature, "SalePrice"]].corr().iloc[0, 1]

                        fig = px.scatter(
                            df_pandas,
                            x=feature,
                            y="SalePrice",
                            title=f"SalePrice vs {feature}<br>Correlation: {corr:.3f}",
                            labels={feature: feature, "SalePrice": "Sale Price ($)"},
                            opacity=0.6,
                            trendline="ols",
                        )
                        st.plotly_chart(fig, use_container_width=True)

    # Correlation Heatmap
    st.header("🔥 Correlation Heatmap")

    # Show top N correlations
    max_features = len(numerical_cols)
    n_features = st.sidebar.slider(
        "Number of features in heatmap", 5, max_features, min(10, max_features)
    )
    top_corr_features = correlations[1 : n_features + 1].index.tolist()

    if top_corr_features:
        corr_matrix = df_pandas[top_corr_features + ["SalePrice"]].corr()

        fig_heatmap = px.imshow(
            corr_matrix,
            labels={"color": "Correlation"},
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            title=f"Top {n_features} Features Correlation with SalePrice",
        )
        fig_heatmap.update_layout(height=600)
        st.plotly_chart(fig_heatmap, use_container_width=True)

    # Top Correlations Table
    with st.expander("📊 Top Correlations with SalePrice"):
        top_corr_df = correlations[1:21].reset_index()
        top_corr_df.columns = ["Feature", "Correlation"]
        top_corr_df["Abs Correlation"] = top_corr_df["Correlation"].abs()
        top_corr_df = top_corr_df.sort_values("Abs Correlation", ascending=False)
        st.dataframe(top_corr_df[["Feature", "Correlation"]], use_container_width=True)

    # Categorical Features Analysis
    st.header("📋 Sale Price vs Categorical Features")

    selected_categorical = st.sidebar.multiselect(
        "Select Categorical Features to Compare",
        options=categorical_cols,
        default=categorical_cols[:3]
        if len(categorical_cols) >= 3
        else categorical_cols,
    )

    if selected_categorical:
        for feature in selected_categorical:
            # Calculate average price per category
            avg_price = (
                df.group_by(feature)
                .agg(
                    [
                        pl.col("SalePrice").mean().alias("Avg_Price"),
                        pl.col("SalePrice").count().alias("Count"),
                    ]
                )
                .sort("Avg_Price", descending=True)
            )

            col1, col2 = st.columns([2, 1])

            with col1:
                fig = px.box(
                    df_pandas,
                    x=feature,
                    y="SalePrice",
                    title=f"SalePrice Distribution by {feature}",
                    labels={feature: feature, "SalePrice": "Sale Price ($)"},
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown(f"**Average Price by {feature}**")
                st.dataframe(
                    avg_price.to_pandas().head(10),
                    use_container_width=True,
                    hide_index=True,
                )

    # Raw Data Viewer
    st.header("🔍 Raw Data")
    if st.checkbox("Show raw data"):
        st.dataframe(df.to_pandas(), use_container_width=True)
        st.markdown(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")


if __name__ == "__main__":
    main()
