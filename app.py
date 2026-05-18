import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Kitchen PNL Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# PROFESSIONAL CSS
# =====================================================

st.markdown("""
<style>

/* MAIN BACKGROUND */

.stApp {
    background-color: #F4F7FE;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 2px solid #1F2937;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* KPI CARDS */

div[data-testid="metric-container"] {

    background: linear-gradient(135deg, #111827, #1F2937);

    border: 1px solid #374151;

    padding: 22px;

    border-radius: 16px;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.15);

    text-align: center;
}

/* KPI LABEL */

div[data-testid="metric-container"] label {
    color: #FFFFFF !important;
    font-size: 18px !important;
    font-weight: 700 !important;
}

div[data-testid="metric-container"] label p {
    color: #FFFFFF !important;
    font-size: 18px !important;
    font-weight: 700 !important;
}

/* KPI VALUE */

div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #00E5A8 !important;
    font-size: 34px !important;
    font-weight: bold !important;
}

/* TABS */

button[data-baseweb="tab"] {

    font-size: 17px !important;

    font-weight: 600 !important;

    background-color: white !important;

    color: #111827 !important;

    border-radius: 10px !important;

    padding: 10px 20px !important;

    margin-right: 8px !important;
}

/* ACTIVE TAB */

button[aria-selected="true"] {
    background-color: #2563EB !important;
    color: white !important;
}

/* HEADINGS */

h1, h2, h3 {
    color: #111827 !important;
}

/* DATAFRAME */

[data-testid="stDataFrame"] {

    background-color: white;

    border-radius: 12px;

    border: 1px solid #E5E7EB;

    padding: 5px;
}

/* DOWNLOAD BUTTON */

.stDownloadButton button {

    background-color: #2563EB !important;

    color: white !important;

    border-radius: 10px !important;

    border: none !important;

    padding: 10px 18px !important;

    font-weight: bold !important;
}

/* CHART CONTAINER */

.js-plotly-plot {

    background-color: white;

    border-radius: 14px;

    padding: 10px;

    margin-bottom: 25px;

    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    df = pd.read_excel(
        "Kittchen PNL Data.xlsx",
        header=1
    )

    # RENAME COLUMNS

    df = df.rename(columns={
        'NET REVENUE': 'NET_REVENUE',
        'GROSS MARGIN': 'GM',
        'KITCHEN EBITDA': 'EBITDA'
    })

    # CLEAN TEXT DATA

    df['CITY'] = df['CITY'].astype(str).str.strip()

    df['STORE'] = df['STORE'].astype(str).str.strip()

    df['MONTH'] = df['MONTH'].astype(str).str.strip()

    df['REVENUE COHORT'] = df['REVENUE COHORT'].astype(str).str.strip()

    # REMOVE DUPLICATES

    df = df.drop_duplicates()

    # REMOVE NULLS

    df = df.dropna()

    # RESET INDEX

    df = df.reset_index(drop=True)

    return df


df = load_data()

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.title("📌 Dashboard Filters")

# CITY FILTER

city_filter = st.sidebar.multiselect(
    "Select City",
    sorted(df['CITY'].unique()),
    default=sorted(df['CITY'].unique())
)

# STORE FILTER

store_filter = st.sidebar.multiselect(
    "Select Store",
    sorted(df['STORE'].unique()),
    default=sorted(df['STORE'].unique())
)

# MONTH FILTER

month_filter = st.sidebar.multiselect(
    "Select Month",
    sorted(df['MONTH'].unique()),
    default=sorted(df['MONTH'].unique())
)

# REVENUE FILTER

revenue_filter = st.sidebar.slider(
    "Revenue Range",
    float(df['NET_REVENUE'].min()),
    float(df['NET_REVENUE'].max()),
    (
        float(df['NET_REVENUE'].min()),
        float(df['NET_REVENUE'].max())
    )
)

# EBITDA FILTER

ebitda_filter = st.sidebar.slider(
    "EBITDA Range",
    float(df['EBITDA'].min()),
    float(df['EBITDA'].max()),
    (
        float(df['EBITDA'].min()),
        float(df['EBITDA'].max())
    )
)

# VARIANCE FILTER

variance_filter = st.sidebar.slider(
    "Variance Range",
    float(df['VARIANCE'].min()),
    float(df['VARIANCE'].max()),
    (
        float(df['VARIANCE'].min()),
        float(df['VARIANCE'].max())
    )
)

# =====================================================
# FILTER LOGIC
# =====================================================

filtered_df = df.copy()

if city_filter:
    filtered_df = filtered_df[
        filtered_df['CITY'].isin(city_filter)
    ]

if store_filter:
    filtered_df = filtered_df[
        filtered_df['STORE'].isin(store_filter)
    ]

if month_filter:
    filtered_df = filtered_df[
        filtered_df['MONTH'].isin(month_filter)
    ]

filtered_df = filtered_df[
    (filtered_df['NET_REVENUE'] >= revenue_filter[0]) &
    (filtered_df['NET_REVENUE'] <= revenue_filter[1])
]

filtered_df = filtered_df[
    (filtered_df['EBITDA'] >= ebitda_filter[0]) &
    (filtered_df['EBITDA'] <= ebitda_filter[1])
]

filtered_df = filtered_df[
    (filtered_df['VARIANCE'] >= variance_filter[0]) &
    (filtered_df['VARIANCE'] <= variance_filter[1])
]

# =====================================================
# DOWNLOAD BUTTON
# =====================================================

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.sidebar.download_button(
    "⬇ Download Filtered Data",
    csv,
    "filtered_kitchen_pnl.csv",
    "text/csv"
)

# =====================================================
# TABS
# =====================================================

tab1, tab2 = st.tabs([
    "📊 Kitchen Level PNL",
    "📉 Variance Dashboard"
])

# =====================================================
# TAB 1
# =====================================================

with tab1:

    st.title("📊 Kitchen Level PNL Dashboard")

    st.markdown("---")

    # KPI

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Revenue",
        f"₹ {filtered_df['NET_REVENUE'].sum():,.0f}"
    )

    col2.metric(
        "Total EBITDA",
        f"₹ {filtered_df['EBITDA'].sum():,.0f}"
    )

    col3.metric(
        "Total Gross Margin",
        f"₹ {filtered_df['GM'].sum():,.0f}"
    )

    col4.metric(
        "Total Stores",
        filtered_df['STORE'].nunique()
    )

    st.markdown("---")

    # CHART 1

    fig1 = px.bar(
        filtered_df,
        x='CITY',
        y='NET_REVENUE',
        color='CITY',
        title='City Wise Revenue'
    )

    fig1.update_layout(height=550)

    st.plotly_chart(
        fig1,
        use_container_width=True,
        config={'displayModeBar': False}
    )

    # CHART 2

    fig2 = px.line(
        filtered_df,
        x='MONTH',
        y='NET_REVENUE',
        color='CITY',
        markers=True,
        title='Monthly Revenue Trend'
    )

    fig2.update_layout(height=550)

    st.plotly_chart(
        fig2,
        use_container_width=True,
        config={'displayModeBar': False}
    )

    # CHART 3

    fig3 = px.scatter(
        filtered_df,
        x='NET_REVENUE',
        y='EBITDA',
        color='CITY',
        size='VARIANCE',
        hover_data=['STORE'],
        title='Revenue vs EBITDA'
    )

    fig3.update_layout(height=600)

    st.plotly_chart(
        fig3,
        use_container_width=True,
        config={'displayModeBar': False}
    )

    # CHART 4

    fig4 = px.box(
        filtered_df,
        x='CITY',
        y='VARIANCE',
        color='CITY',
        title='Variance Distribution by City'
    )

    fig4.update_layout(height=550)

    st.plotly_chart(
        fig4,
        use_container_width=True,
        config={'displayModeBar': False}
    )

# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.title("📉 Variance Dashboard")

    st.markdown("---")

    st.subheader("Average Variance % by Revenue Cohort")

    variance_summary = (
        filtered_df
        .groupby('REVENUE COHORT')['VARIANCE']
        .mean()
        .reset_index()
    )

    fig5 = px.bar(
        variance_summary,
        x='REVENUE COHORT',
        y='VARIANCE',
        color='REVENUE COHORT',
        title='Average Variance by Revenue Cohort'
    )

    fig5.update_layout(height=550)

    st.plotly_chart(
        fig5,
        use_container_width=True,
        config={'displayModeBar': False}
    )

    st.subheader("📋 Store Count by Revenue Cohort and Month")

    store_summary = pd.pivot_table(
        filtered_df,
        values='STORE',
        index='REVENUE COHORT',
        columns='MONTH',
        aggfunc='count',
        fill_value=0
    )

    st.dataframe(
        store_summary,
        use_container_width=True
    )

    st.subheader("📄 Filtered Dataset")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown("""

### ✅ Dashboard Features

- Kitchen Level PNL Dashboard
- Variance Dashboard
- Interactive Filters
- Revenue & EBITDA Filters
- Download CSV Button
- KPI Cards
- Plotly Interactive Charts
- Performance Optimized using Cache
- Professional Dashboard Layout

""")