"""
Ethiopia Financial Inclusion Dashboard
Streamlit Application

Run with: streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Page configuration
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Dashboard",
    page_icon="🇪🇹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .insight-box {
        background-color: #e8f4f8;
        border-left: 4px solid #2E86AB;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load the enriched dataset."""
    try:
        df = pd.read_csv('data/processed/ethiopia_fi_enriched.csv')
    except:
        df = pd.read_csv('../data/processed/ethiopia_fi_enriched.csv')
    
    df['observation_date'] = pd.to_datetime(df['observation_date'], errors='coerce')
    df['event_date'] = pd.to_datetime(df['event_date'], errors='coerce')
    return df


def create_metric_card(label, value, delta=None, delta_color="normal"):
    """Create a styled metric display."""
    st.metric(label=label, value=value, delta=delta, delta_color=delta_color)


def plot_account_ownership(df):
    """Plot account ownership trajectory."""
    obs = df[(df['record_type'] == 'observation') & (df['indicator_code'] == 'ACC_OWNERSHIP')]
    obs = obs.sort_values('observation_date')
    
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=obs['observation_date'],
        y=obs['value_numeric'],
        mode='lines+markers+text',
        name='Account Ownership',
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=12, color='white', line=dict(color='#2E86AB', width=3)),
        text=[f"{v:.0f}%" for v in obs['value_numeric']],
        textposition='top center',
        textfont=dict(size=12, color='#2E86AB')
    ))
    
    # Add forecast (simple projection)
    last_year = obs['observation_date'].max().year
    last_value = obs['value_numeric'].iloc[-1]
    forecast_years = [datetime(y, 12, 31) for y in [2025, 2026, 2027]]
    forecast_values = [last_value + 2.5 * i for i in [1, 2, 3]]
    
    fig.add_trace(go.Scatter(
        x=forecast_years,
        y=forecast_values,
        mode='lines+markers',
        name='Forecast (Base)',
        line=dict(color='#28A745', width=2, dash='dash'),
        marker=dict(size=10, color='#28A745')
    ))
    
    # Target line
    fig.add_hline(y=60, line_dash="dot", line_color="#DC3545",
                  annotation_text="NFIS-II Target (60%)")
    
    fig.update_layout(
        title="Account Ownership Trajectory (2011-2027)",
        xaxis_title="Year",
        yaxis_title="Account Ownership Rate (%)",
        yaxis_range=[0, 70],
        hovermode='x unified',
        legend=dict(yanchor="bottom", y=0.01, xanchor="right", x=0.99)
    )
    
    return fig


def plot_digital_payments(df):
    """Plot digital payment trends."""
    obs = df[(df['record_type'] == 'observation') & (df['indicator_code'] == 'USG_DIGITAL_PAYMENT')]
    obs = obs.sort_values('observation_date')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=obs['observation_date'],
        y=obs['value_numeric'],
        mode='lines+markers+text',
        name='Digital Payments',
        line=dict(color='#28A745', width=3),
        marker=dict(size=12, color='white', line=dict(color='#28A745', width=3)),
        text=[f"{v:.0f}%" for v in obs['value_numeric']],
        textposition='top center'
    ))
    
    # Target line
    fig.add_hline(y=50, line_dash="dot", line_color="#DC3545",
                  annotation_text="Target (50%)")
    
    fig.update_layout(
        title="Digital Payment Adoption",
        xaxis_title="Year",
        yaxis_title="Digital Payment Rate (%)",
        yaxis_range=[0, 60],
        hovermode='x unified'
    )
    
    return fig


def plot_scenario_forecast(indicator='access'):
    """Plot scenario-based forecasts."""
    years = [2024, 2025, 2026, 2027]
    
    if indicator == 'access':
        base = [49, 51.5, 54, 56.5]
        optimistic = [49, 53, 57, 61]
        pessimistic = [49, 50, 51, 52]
        target = 60
        title = "Account Ownership Scenarios"
        y_label = "Account Ownership (%)"
    else:
        base = [35, 37.5, 40, 42.5]
        optimistic = [35, 39, 43, 47]
        pessimistic = [35, 36, 37, 38]
        target = 50
        title = "Digital Payment Scenarios"
        y_label = "Digital Payment (%)"
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=years, y=optimistic, mode='lines+markers',
                             name='Optimistic', line=dict(color='#28A745', width=2)))
    fig.add_trace(go.Scatter(x=years, y=base, mode='lines+markers',
                             name='Base', line=dict(color='#2E86AB', width=2)))
    fig.add_trace(go.Scatter(x=years, y=pessimistic, mode='lines+markers',
                             name='Pessimistic', line=dict(color='#DC3545', width=2)))
    
    fig.add_hline(y=target, line_dash="dot", line_color="black",
                  annotation_text=f"Target ({target}%)")
    
    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title=y_label,
        hovermode='x unified',
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    return fig


def main():
    """Main dashboard application."""
    
    # Load data
    df = load_data()
    observations = df[df['record_type'] == 'observation']
    events = df[df['record_type'] == 'event']
    targets = df[df['record_type'] == 'target']
    
    # Sidebar
    st.sidebar.title("🇪🇹 Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["📊 Overview", "📈 Trends", "🔮 Forecasts", "📋 Data Explorer"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "This dashboard tracks Ethiopia's financial inclusion progress "
        "using Global Findex data and operator reports."
    )
    
    # Main content based on page selection
    if page == "📊 Overview":
        st.markdown('<h1 class="main-header">Ethiopia Financial Inclusion Dashboard</h1>', 
                    unsafe_allow_html=True)
        st.markdown("### Key Metrics (2024)")
        
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📈 Account Ownership",
                value="49%",
                delta="+3pp from 2021",
                delta_color="normal"
            )
        
        with col2:
            st.metric(
                label="💳 Digital Payments",
                value="35%",
                delta="+8pp from 2021",
                delta_color="normal"
            )
        
        with col3:
            st.metric(
                label="📱 Mobile Money Users",
                value="64M",
                delta="Telebirr 54M + M-Pesa 10M"
            )
        
        with col4:
            st.metric(
                label="🎯 Gap to Target",
                value="11pp",
                delta="to reach 60%",
                delta_color="inverse"
            )
        
        st.markdown("---")
        
        # Charts row
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(plot_account_ownership(df), use_container_width=True)
        
        with col2:
            st.plotly_chart(plot_digital_payments(df), use_container_width=True)
        
        # Key insights
        st.markdown("### 🔍 Key Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="insight-box">
            <strong>The Stagnation Puzzle</strong><br>
            Account ownership grew only +3pp (2021-2024) despite 64M+ mobile money registrations.
            This suggests high overlap with existing accounts or inactive registrations.
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="insight-box">
            <strong>Gender Gap Closing</strong><br>
            The gender gap reduced from 8pp (2021) to 4pp (2024). Female growth (+5pp) 
            outpaced male growth (+1pp).
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "📈 Trends":
        st.markdown("## 📈 Financial Inclusion Trends")
        
        tab1, tab2 = st.tabs(["Account Ownership", "Events Timeline"])
        
        with tab1:
            st.plotly_chart(plot_account_ownership(df), use_container_width=True)
            
            st.markdown("### Growth Rate Analysis")
            growth_data = pd.DataFrame({
                'Period': ['2011-2014', '2014-2017', '2017-2021', '2021-2024'],
                'Growth (pp)': [8, 13, 11, 3],
                'Annual Rate': [2.7, 4.3, 2.75, 1.0]
            })
            st.dataframe(growth_data, use_container_width=True)
        
        with tab2:
            st.markdown("### Event List")
            event_display = events[['event_date', 'category', 'indicator', 'value_text']].copy()
            event_display['event_date'] = event_display['event_date'].dt.strftime('%Y-%m-%d')
            st.dataframe(event_display, use_container_width=True)
    
    elif page == "🔮 Forecasts":
        st.markdown("## 🔮 Financial Inclusion Projections")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(plot_scenario_forecast('access'), use_container_width=True)
        
        with col2:
            st.plotly_chart(plot_scenario_forecast('usage'), use_container_width=True)
        
        st.markdown("### Forecast Summary")
        
        forecast_df = pd.DataFrame({
            'Year': [2025, 2026, 2027],
            'Account Ownership (Base)': ['51.5%', '54.0%', '56.5%'],
            'Account Ownership (Range)': ['50-53%', '51-57%', '52-61%'],
            'Digital Payment (Base)': ['37.5%', '40.0%', '42.5%'],
            'Digital Payment (Range)': ['36-39%', '37-43%', '38-47%']
        })
        st.dataframe(forecast_df, use_container_width=True)
        
        st.markdown("### Scenario Assumptions")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.success("**Optimistic (+4pp/year)**\n\nAccelerated adoption, new products, strong interoperability")
        with col2:
            st.info("**Base (+2.5pp/year)**\n\nCurrent trend continuation")
        with col3:
            st.error("**Pessimistic (+1pp/year)**\n\nMarket saturation, infrastructure constraints")
    
    elif page == "📋 Data Explorer":
        st.markdown("## 📋 Data Explorer")
        
        tab1, tab2, tab3 = st.tabs(["Observations", "Events", "Targets"])
        
        with tab1:
            st.markdown("### Observations Data")
            obs_display = observations[['observation_date', 'pillar', 'indicator_code', 
                                        'value_numeric', 'source_name', 'confidence']].copy()
            obs_display['observation_date'] = obs_display['observation_date'].dt.strftime('%Y-%m-%d')
            
            # Filters
            col1, col2 = st.columns(2)
            with col1:
                pillar_filter = st.multiselect("Filter by Pillar", 
                                               options=obs_display['pillar'].unique())
            with col2:
                indicator_filter = st.multiselect("Filter by Indicator",
                                                  options=obs_display['indicator_code'].unique())
            
            if pillar_filter:
                obs_display = obs_display[obs_display['pillar'].isin(pillar_filter)]
            if indicator_filter:
                obs_display = obs_display[obs_display['indicator_code'].isin(indicator_filter)]
            
            st.dataframe(obs_display, use_container_width=True)
            
            # Download button
            csv = obs_display.to_csv(index=False)
            st.download_button(
                label="📥 Download Observations CSV",
                data=csv,
                file_name="ethiopia_fi_observations.csv",
                mime="text/csv"
            )
        
        with tab2:
            st.markdown("### Events Data")
            events_display = events[['event_date', 'category', 'indicator', 'value_text']].copy()
            events_display['event_date'] = events_display['event_date'].dt.strftime('%Y-%m-%d')
            st.dataframe(events_display, use_container_width=True)
        
        with tab3:
            st.markdown("### NFIS-II Targets")
            targets_display = targets[['indicator', 'value_numeric', 'observation_date']].copy()
            targets_display.columns = ['Target', 'Value (%)', 'Target Year']
            st.dataframe(targets_display, use_container_width=True)


if __name__ == "__main__":
    main()
