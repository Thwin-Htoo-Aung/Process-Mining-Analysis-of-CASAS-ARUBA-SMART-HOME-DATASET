"""
Process Mining Dashboard with LLM Chatbot
==========================================

An interactive dashboard combining:
- Process Mining visualizations and metrics
- LLM-powered chatbot for Q&A
- Anomaly detection alerts
- Next activity prediction
- Real-time analysis

Author: Process Mining Assignment
Date: January 2026

Run with: streamlit run process_mining_dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import sys
import io

# PDF Generation
try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


def generate_pdf_report(title, content):
    """
    Generate a simple PDF report from text content.
    """
    if not PDF_AVAILABLE:
        return None
    
    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Title
        pdf.set_font('Helvetica', 'B', 16)
        clean_title = ''.join(c for c in title if ord(c) < 128)
        pdf.cell(190, 10, clean_title, ln=True, align='C')
        pdf.ln(10)
        
        # Content
        pdf.set_font('Helvetica', '', 9)
        
        for line in content.split('\n'):
            # Keep only printable ASCII
            clean_line = ''.join(c for c in line if 32 <= ord(c) < 127)
            clean_line = clean_line.strip()
            
            if not clean_line:
                pdf.ln(2)
                continue
            
            try:
                if clean_line.startswith('#'):
                    pdf.set_font('Helvetica', 'B', 11)
                    pdf.cell(190, 6, clean_line.lstrip('#').strip()[:80], ln=True)
                    pdf.set_font('Helvetica', '', 9)
                else:
                    # Split long lines
                    while len(clean_line) > 95:
                        pdf.cell(190, 5, clean_line[:95], ln=True)
                        clean_line = clean_line[95:]
                    if clean_line:
                        pdf.cell(190, 5, clean_line, ln=True)
            except:
                pass  # Skip problematic lines
        
        return bytes(pdf.output())
    except Exception:
        return None

# Set page config first
st.set_page_config(
    page_title="Process Mining Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import our modules
try:
    from llm_process_mining import (
        LLMProcessMiningAnalyst,
        prepare_metrics_for_llm,
        prepare_temporal_patterns,
        prepare_variants_info,
        prepare_process_stats,
        get_recent_activities,
        get_activity_transitions
    )
    LLM_AVAILABLE = True
except ImportError as e:
    LLM_AVAILABLE = False
    st.warning(f"LLM module not available: {e}")

# pm4py imports
try:
    import pm4py
    from pm4py.objects.conversion.log import converter as log_converter
    from pm4py.algo.discovery.alpha import algorithm as alpha_miner
    from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
    from pm4py.algo.discovery.inductive import algorithm as inductive_miner
    from pm4py.visualization.petri_net import visualizer as pn_visualizer
    from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
    from pm4py.statistics.variants.log import get as variants_module
    from pm4py.algo.evaluation.replay_fitness import algorithm as fitness_evaluator
    from pm4py.algo.evaluation.precision import algorithm as precision_evaluator
    from pm4py.algo.evaluation.generalization import algorithm as generalization_evaluator
    from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator
    PM4PY_AVAILABLE = True
except ImportError:
    PM4PY_AVAILABLE = False
    st.error("pm4py not installed. Please install with: pip install pm4py")


# ========================================
# Data Loading Functions
# ========================================

@st.cache_data
def load_aruba_data(filepath, sample_size=None):
    """Load and preprocess the Aruba dataset."""
    column_names = ['date', 'time', 'sensor_id', 'sensor_value']
    
    if sample_size:
        df = pd.read_csv(filepath, names=column_names, nrows=sample_size)
    else:
        df = pd.read_csv(filepath, names=column_names)
    
    # Create timestamp
    df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    # Create activity
    df['activity'] = df['sensor_id'] + '_' + df['sensor_value']
    
    return df


@st.cache_data
def create_event_log(df):
    """Create event log with daily cases."""
    df = df.copy()
    df['case_id'] = df['timestamp'].dt.strftime('%Y-%m-%d')
    
    event_log = df[['case_id', 'activity', 'timestamp']].copy()
    event_log['case:concept:name'] = event_log['case_id']
    event_log['concept:name'] = event_log['activity']
    event_log['time:timestamp'] = event_log['timestamp']
    
    return event_log


def convert_to_pm4py_log(event_log_df):
    """Convert DataFrame to pm4py EventLog."""
    parameters = {
        log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'case:concept:name'
    }
    return log_converter.apply(event_log_df, parameters=parameters,
                               variant=log_converter.Variants.TO_EVENT_LOG)


# ========================================
# Dashboard Layout
# ========================================

def main():
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
    .suggested-question {
        background-color: #e8f4fd;
        border: 1px solid #1976d2;
        border-radius: 20px;
        padding: 8px 16px;
        margin: 4px;
        cursor: pointer;
        display: inline-block;
        font-size: 0.9em;
    }
    .suggested-question:hover {
        background-color: #bbdefb;
    }
    .chat-context-box {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 10px;
        margin-bottom: 15px;
        border-radius: 4px;
    }
    .metrics-summary {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 10px;
        margin-bottom: 15px;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-header">📊 Process Mining Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: gray;">CASAS Aruba Smart Home Analysis with LLM Integration</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Data loading options
        st.subheader("📁 Data Settings")
        sample_size = st.slider("Sample Size", 1000, 100000, 50000, 1000)
        
        # LLM settings
        if LLM_AVAILABLE:
            st.subheader("🤖 LLM Settings")
            llm_model = st.selectbox(
                "Model",
                ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
                index=0
            )
        
        # Load data button
        load_data = st.button("🔄 Load/Reload Data", type="primary")
        
        st.divider()
        
        # Navigation
        st.subheader("📌 Navigation")
        page = st.radio(
            "Select Page",
            ["🏠 Overview", "📈 Process Discovery", "🔍 Anomaly Detection", 
             "🎯 Predictions", "💬 Chat Assistant", "📄 Reports"]
        )
    
    # Initialize session state
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'analyst' not in st.session_state and LLM_AVAILABLE:
        st.session_state.analyst = LLMProcessMiningAnalyst()
    
    # Load data
    if load_data or not st.session_state.data_loaded:
        with st.spinner("Loading data..."):
            try:
                df = load_aruba_data('aruba.csv', sample_size=sample_size)
                event_log_df = create_event_log(df)
                
                st.session_state.df = df
                st.session_state.event_log_df = event_log_df
                st.session_state.data_loaded = True
                
                if PM4PY_AVAILABLE:
                    event_log = convert_to_pm4py_log(event_log_df)
                    st.session_state.event_log = event_log
                
                st.success("✅ Data loaded successfully!")
            except FileNotFoundError:
                st.error("❌ aruba.csv not found. Please ensure the file is in the current directory.")
                return
            except Exception as e:
                st.error(f"❌ Error loading data: {str(e)}")
                return
    
    # Page routing
    if page == "🏠 Overview":
        show_overview_page()
    elif page == "📈 Process Discovery":
        show_discovery_page()
    elif page == "🔍 Anomaly Detection":
        show_anomaly_page()
    elif page == "🎯 Predictions":
        show_prediction_page()
    elif page == "💬 Chat Assistant":
        show_chat_page()
    elif page == "📄 Reports":
        show_reports_page()


def show_overview_page():
    """Display the overview dashboard page."""
    st.header("🏠 Overview Dashboard")
    
    if not st.session_state.data_loaded:
        st.warning("Please load data first.")
        return
    
    df = st.session_state.df
    event_log_df = st.session_state.event_log_df
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Events", f"{len(df):,}")
    with col2:
        st.metric("📅 Total Cases (Days)", event_log_df['case_id'].nunique())
    with col3:
        st.metric("🎯 Unique Activities", df['activity'].nunique())
    with col4:
        st.metric("📡 Unique Sensors", df['sensor_id'].nunique())
    
    st.divider()
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Top 15 Activities")
        activity_counts = df['activity'].value_counts().head(15)
        fig = px.bar(
            x=activity_counts.values,
            y=activity_counts.index,
            orientation='h',
            labels={'x': 'Frequency', 'y': 'Activity'},
            color=activity_counts.values,
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🕐 Hourly Activity Pattern")
        df['hour'] = df['timestamp'].dt.hour
        hourly = df.groupby('hour').size().reset_index(name='count')
        fig = px.line(hourly, x='hour', y='count', markers=True)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Second row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Weekly Activity Pattern")
        df['day_of_week'] = df['timestamp'].dt.day_name()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily = df['day_of_week'].value_counts().reindex(day_order)
        fig = px.bar(x=daily.index, y=daily.values, labels={'x': 'Day', 'y': 'Events'})
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📡 Sensor Distribution")
        sensor_counts = df['sensor_id'].value_counts().head(10)
        fig = px.pie(values=sensor_counts.values, names=sensor_counts.index, hole=0.4)
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Daily timeline
    st.subheader("📈 Daily Event Timeline")
    df['date'] = df['timestamp'].dt.date
    daily_events = df.groupby('date').size().reset_index(name='events')
    fig = px.line(daily_events, x='date', y='events')
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)


def show_discovery_page():
    """Display process discovery results and metrics."""
    st.header("📈 Process Discovery")
    
    if not st.session_state.data_loaded or not PM4PY_AVAILABLE:
        st.warning("Please load data first and ensure pm4py is installed.")
        return
    
    event_log = st.session_state.event_log
    
    # Mining algorithm selection
    col1, col2 = st.columns([2, 1])
    with col1:
        algorithm = st.selectbox(
            "Select Mining Algorithm",
            ["Alpha Miner", "Heuristic Miner", "Inductive Miner", "Compare All"]
        )
    
    with col2:
        run_mining = st.button("🚀 Run Process Discovery", type="primary")
    
    if run_mining:
        with st.spinner("Discovering process model..."):
            try:
                if algorithm == "Alpha Miner" or algorithm == "Compare All":
                    alpha_net, alpha_im, alpha_fm = alpha_miner.apply(event_log)
                    st.session_state.alpha_model = (alpha_net, alpha_im, alpha_fm)
                    
                if algorithm == "Heuristic Miner" or algorithm == "Compare All":
                    heu_net = heuristics_miner.apply_heu(event_log)
                    st.session_state.heuristic_model = heu_net
                    
                if algorithm == "Inductive Miner" or algorithm == "Compare All":
                    result = inductive_miner.apply(event_log)
                    if isinstance(result, tuple):
                        ind_net, ind_im, ind_fm = result
                    else:
                        from pm4py.objects.conversion.process_tree import converter as pt_converter
                        ind_net, ind_im, ind_fm = pt_converter.apply(result)
                    st.session_state.inductive_model = (ind_net, ind_im, ind_fm)
                
                st.success("✅ Process discovery completed!")
                
            except Exception as e:
                st.error(f"Error during discovery: {str(e)}")
    
    # Display metrics
    st.divider()
    st.subheader("📊 Model Quality Metrics")
    
    metrics_data = []
    
    if 'alpha_model' in st.session_state:
        net, im, fm = st.session_state.alpha_model
        try:
            fitness = fitness_evaluator.apply(event_log, net, im, fm, 
                variant=fitness_evaluator.Variants.TOKEN_BASED)['average_trace_fitness']
            precision = precision_evaluator.apply(event_log, net, im, fm,
                variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN)
            try:
                generalization = generalization_evaluator.apply(event_log, net, im, fm)
            except:
                generalization = 0.0
            try:
                simplicity = simplicity_evaluator.apply(net)
            except:
                simplicity = 0.0
            metrics_data.append({
                'Model': 'Alpha Miner',
                'Fitness': round(fitness, 4),
                'Precision': round(precision, 4),
                'Generalization': round(generalization, 4),
                'Simplicity': round(simplicity, 4),
                'Places': len(net.places),
                'Transitions': len(net.transitions)
            })
        except Exception as e:
            st.warning(f"Could not calculate Alpha Miner metrics: {e}")
    
    if 'inductive_model' in st.session_state:
        net, im, fm = st.session_state.inductive_model
        try:
            fitness = fitness_evaluator.apply(event_log, net, im, fm,
                variant=fitness_evaluator.Variants.TOKEN_BASED)['average_trace_fitness']
            precision = precision_evaluator.apply(event_log, net, im, fm,
                variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN)
            try:
                generalization = generalization_evaluator.apply(event_log, net, im, fm)
            except:
                generalization = 0.0
            try:
                simplicity = simplicity_evaluator.apply(net)
            except:
                simplicity = 0.0
            metrics_data.append({
                'Model': 'Inductive Miner',
                'Fitness': round(fitness, 4),
                'Precision': round(precision, 4),
                'Generalization': round(generalization, 4),
                'Simplicity': round(simplicity, 4),
                'Places': len(net.places),
                'Transitions': len(net.transitions)
            })
        except Exception as e:
            st.warning(f"Could not calculate Inductive Miner metrics: {e}")
    
    # Also add Heuristic Miner metrics if available (Heuristic Net converted to Petri Net)
    if 'heuristic_model' in st.session_state:
        try:
            from pm4py.objects.conversion.heuristics_net import converter as hn_converter
            heu_net = st.session_state.heuristic_model
            heu_petri_net, heu_im, heu_fm = hn_converter.apply(heu_net)
            
            fitness = fitness_evaluator.apply(event_log, heu_petri_net, heu_im, heu_fm,
                variant=fitness_evaluator.Variants.TOKEN_BASED)['average_trace_fitness']
            precision = precision_evaluator.apply(event_log, heu_petri_net, heu_im, heu_fm,
                variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN)
            try:
                generalization = generalization_evaluator.apply(event_log, heu_petri_net, heu_im, heu_fm)
            except:
                generalization = 0.0
            try:
                simplicity = simplicity_evaluator.apply(heu_petri_net)
            except:
                simplicity = 0.0
            metrics_data.append({
                'Model': 'Heuristic Miner',
                'Fitness': round(fitness, 4),
                'Precision': round(precision, 4),
                'Generalization': round(generalization, 4),
                'Simplicity': round(simplicity, 4),
                'Places': len(heu_petri_net.places),
                'Transitions': len(heu_petri_net.transitions)
            })
        except Exception as e:
            st.warning(f"Could not calculate Heuristic Miner metrics: {e}")
    
    if metrics_data:
        metrics_df = pd.DataFrame(metrics_data)
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("📊 Model Comparison Charts")
        
        # Grouped Bar Chart - All 4 Metrics Comparison
        st.markdown("### All Metrics Comparison (Grouped Bar Chart)")
        metrics_to_compare = ['Fitness', 'Precision', 'Generalization', 'Simplicity']
        metrics_long = metrics_df.melt(
            id_vars=['Model'], 
            value_vars=metrics_to_compare,
            var_name='Metric', 
            value_name='Score'
        )
        
        fig_grouped = px.bar(
            metrics_long, 
            x='Metric', 
            y='Score', 
            color='Model',
            barmode='group',
            title='Model Quality Metrics Comparison',
            color_discrete_sequence=px.colors.qualitative.Set2,
            text='Score'
        )
        fig_grouped.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        fig_grouped.update_layout(
            height=500,
            yaxis=dict(range=[0, 1.1], title='Score (0-1)'),
            xaxis=dict(title='Metric'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        st.plotly_chart(fig_grouped, use_container_width=True)
        
        # Individual Metric Charts in 2x2 Grid
        st.markdown("### Individual Metric Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            # Fitness Chart
            fig_fitness = px.bar(
                metrics_df, x='Model', y='Fitness',
                title='🎯 Fitness Comparison',
                color='Model',
                color_discrete_sequence=px.colors.qualitative.Set2,
                text='Fitness'
            )
            fig_fitness.update_traces(texttemplate='%{text:.4f}', textposition='outside')
            fig_fitness.update_layout(height=350, yaxis=dict(range=[0, 1.1]), showlegend=False)
            st.plotly_chart(fig_fitness, use_container_width=True)
            
            # Generalization Chart
            fig_gen = px.bar(
                metrics_df, x='Model', y='Generalization',
                title='🔄 Generalization Comparison',
                color='Model',
                color_discrete_sequence=px.colors.qualitative.Set2,
                text='Generalization'
            )
            fig_gen.update_traces(texttemplate='%{text:.4f}', textposition='outside')
            fig_gen.update_layout(height=350, yaxis=dict(range=[0, 1.1]), showlegend=False)
            st.plotly_chart(fig_gen, use_container_width=True)
        
        with col2:
            # Precision Chart
            fig_precision = px.bar(
                metrics_df, x='Model', y='Precision',
                title='🎯 Precision Comparison',
                color='Model',
                color_discrete_sequence=px.colors.qualitative.Set2,
                text='Precision'
            )
            fig_precision.update_traces(texttemplate='%{text:.4f}', textposition='outside')
            fig_precision.update_layout(height=350, yaxis=dict(range=[0, 1.1]), showlegend=False)
            st.plotly_chart(fig_precision, use_container_width=True)
            
            # Simplicity Chart
            fig_simp = px.bar(
                metrics_df, x='Model', y='Simplicity',
                title='📐 Simplicity Comparison',
                color='Model',
                color_discrete_sequence=px.colors.qualitative.Set2,
                text='Simplicity'
            )
            fig_simp.update_traces(texttemplate='%{text:.4f}', textposition='outside')
            fig_simp.update_layout(height=350, yaxis=dict(range=[0, 1.1]), showlegend=False)
            st.plotly_chart(fig_simp, use_container_width=True)
        
        # Radar Chart for comprehensive view
        st.markdown("### Radar Chart - Overall Model Comparison")
        fig_radar = go.Figure()
        
        colors = ['rgb(99, 110, 250)', 'rgb(239, 85, 59)', 'rgb(0, 204, 150)']
        for idx, row in metrics_df.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[row['Fitness'], row['Precision'], row['Generalization'], row['Simplicity'], row['Fitness']],
                theta=['Fitness', 'Precision', 'Generalization', 'Simplicity', 'Fitness'],
                fill='toself',
                name=row['Model'],
                line=dict(color=colors[idx % len(colors)]),
                opacity=0.6
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1])
            ),
            showlegend=True,
            title='Model Quality Radar Chart',
            height=500
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Heatmap View
        st.markdown("### Heatmap - Metrics Overview")
        heatmap_data = metrics_df.set_index('Model')[metrics_to_compare]
        
        fig_heatmap = px.imshow(
            heatmap_data,
            text_auto='.3f',
            aspect='auto',
            color_continuous_scale='RdYlGn',
            title='Model Metrics Heatmap'
        )
        fig_heatmap.update_layout(height=300)
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Metric explanations
    with st.expander("ℹ️ Understanding the Metrics"):
        st.markdown("""
        ### Conformance Checking Metrics
        
        | Metric | Description | Calculation Method |
        |--------|-------------|-------------------|
        | **Fitness** | How well the model can replay event log traces | Token-based Replay: Simulates execution and counts missing/remaining tokens |
        | **Precision** | How much behavior the model allows beyond the log | ETConformance: Measures escaping edges at each state |
        | **Generalization** | How well the model generalizes to unseen cases | Based on transition visit frequency during replay |
        | **Simplicity** | Structural complexity of the model | Inverse of mean arc degree in the Petri net |
        
        ### Interpretation
        - **High Fitness (→1.0)**: Model can replay most/all traces
        - **High Precision (→1.0)**: Model doesn't allow extra behavior
        - **Trade-off**: Often there's a trade-off between fitness and precision
        """)


def show_anomaly_page():
    """Display anomaly detection results."""
    st.header("🔍 Anomaly Detection")
    
    if not st.session_state.data_loaded:
        st.warning("Please load data first.")
        return
    
    df = st.session_state.df
    event_log_df = st.session_state.event_log_df
    
    # Statistical anomalies
    st.subheader("📊 Statistical Anomaly Detection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Activity Frequency Anomalies")
        activity_counts = df['activity'].value_counts()
        mean_freq = activity_counts.mean()
        std_freq = activity_counts.std()
        
        # Find anomalies (activities with unusual frequency)
        low_threshold = mean_freq - 2 * std_freq
        high_threshold = mean_freq + 2 * std_freq
        
        anomalous_low = activity_counts[activity_counts < low_threshold]
        anomalous_high = activity_counts[activity_counts > high_threshold]
        
        st.metric("Mean Activity Frequency", f"{mean_freq:.0f}")
        st.metric("Standard Deviation", f"{std_freq:.0f}")
        
        if len(anomalous_high) > 0:
            st.warning(f"⚠️ {len(anomalous_high)} activities with unusually HIGH frequency")
            st.dataframe(anomalous_high.head(5), use_container_width=True)
        
        if len(anomalous_low) > 0:
            st.info(f"ℹ️ {len(anomalous_low)} activities with unusually LOW frequency")
    
    with col2:
        st.markdown("### Temporal Anomalies")
        df['hour'] = df['timestamp'].dt.hour
        
        # Night activity (unusual hours)
        night_hours = [0, 1, 2, 3, 4, 5]
        night_activity = df[df['hour'].isin(night_hours)]
        night_percentage = len(night_activity) / len(df) * 100
        
        st.metric("Night Activity (12am-6am)", f"{night_percentage:.1f}%")
        
        if night_percentage > 10:
            st.warning("⚠️ Elevated night activity detected")
        else:
            st.success("✅ Night activity within normal range")
        
        # Activity gaps
        df_sorted = df.sort_values('timestamp')
        df_sorted['time_gap'] = df_sorted['timestamp'].diff().dt.total_seconds() / 3600
        large_gaps = df_sorted[df_sorted['time_gap'] > 6]  # Gaps > 6 hours
        
        st.metric("Large Time Gaps (>6 hours)", len(large_gaps))
    
    st.divider()
    
    # LLM-powered anomaly detection
    if LLM_AVAILABLE and st.button("🤖 Run LLM Anomaly Analysis", type="primary"):
        with st.spinner("Analyzing with LLM..."):
            analyst = st.session_state.analyst
            
            # Prepare data
            temporal_patterns = prepare_temporal_patterns(event_log_df)
            
            # Get LLM analysis
            anomaly_report = analyst.detect_anomalies(
                event_log_df, 
                activity_counts,
                temporal_patterns
            )
            
            st.markdown("### 🤖 LLM Anomaly Analysis")
            st.markdown(anomaly_report)


def show_prediction_page():
    """Display prediction capabilities."""
    st.header("🎯 Activity Prediction")
    
    if not st.session_state.data_loaded:
        st.warning("Please load data first.")
        return
    
    event_log_df = st.session_state.event_log_df
    
    # Show recent activities
    st.subheader("📋 Recent Activities")
    recent = event_log_df.sort_values('timestamp', ascending=False).head(20)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(
            recent[['timestamp', 'activity', 'case_id']].reset_index(drop=True),
            use_container_width=True,
            height=400
        )
    
    with col2:
        st.markdown("### Activity Transitions")
        # Calculate transitions
        df_sorted = event_log_df.sort_values(['case_id', 'timestamp'])
        df_sorted['next_activity'] = df_sorted.groupby('case_id')['activity'].shift(-1)
        
        # Most common transitions
        transitions = df_sorted.groupby(['activity', 'next_activity']).size()
        top_transitions = transitions.sort_values(ascending=False).head(10)
        
        for (act, next_act), count in top_transitions.items():
            st.text(f"{act[:15]}... → {next_act[:15]}... ({count})")
    
    st.divider()
    
    # LLM prediction
    if LLM_AVAILABLE:
        st.subheader("🤖 LLM-Powered Prediction")
        
        if st.button("Predict Next Activity", type="primary"):
            with st.spinner("Generating prediction..."):
                analyst = st.session_state.analyst
                
                recent_activities = get_recent_activities(event_log_df, n=20)
                activity_transitions = get_activity_transitions(event_log_df)
                
                prediction = analyst.predict_next_activity(
                    recent_activities,
                    activity_transitions
                )
                
                st.markdown("### Prediction Result")
                st.markdown(prediction)


def show_chat_page():
    """Display the chat assistant interface with comprehensive context."""
    st.header("💬 Process Mining Chat Assistant")
    
    if not LLM_AVAILABLE:
        st.error("LLM module not available. Please check installation.")
        return
    
    if not st.session_state.data_loaded:
        st.warning("⚠️ Please load data first for context-aware responses.")
        return
    
    # Get data references
    event_log_df = st.session_state.event_log_df
    df = st.session_state.df
    analyst = st.session_state.analyst
    
    # Prepare comprehensive context
    process_stats = prepare_process_stats(event_log_df)
    temporal_patterns = prepare_temporal_patterns(event_log_df)
    activity_stats = df['activity'].value_counts().head(20).to_dict()
    
    # Get model metrics if available
    metrics_context = {}
    if 'alpha_model' in st.session_state or 'inductive_model' in st.session_state or 'heuristic_model' in st.session_state:
        metrics_context = get_all_model_metrics()
    
    # Set context for analyst
    analyst.set_analysis_context(
        metrics=metrics_context,
        event_log_stats=process_stats,
        activity_stats=activity_stats,
        temporal_stats=temporal_patterns
    )
    
    # Layout with sidebar info and main chat
    col1, col2 = st.columns([3, 1])
    
    with col2:
        # Context Summary Panel
        st.markdown("### 📊 Current Context")
        
        st.markdown('<div class="metrics-summary">', unsafe_allow_html=True)
        st.markdown(f"""
        **Data Loaded:**
        - Events: {process_stats.get('total_events', 'N/A'):,}
        - Cases: {process_stats.get('total_cases', 'N/A')}
        - Activities: {process_stats.get('unique_activities', 'N/A')}
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if metrics_context:
            st.markdown('<div class="chat-context-box">', unsafe_allow_html=True)
            st.markdown("**Models Available:**")
            for model_name in metrics_context.keys():
                fitness = metrics_context[model_name].get('fitness', 'N/A')
                st.markdown(f"- {model_name.title()}: Fitness={fitness}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("💡 Run Process Discovery to get model metrics for richer insights.")
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            if 'analyst' in st.session_state:
                st.session_state.analyst.conversation_history = []
            st.rerun()
    
    with col1:
        # Suggested Questions
        st.markdown("### 💡 Ask Me Anything!")
        
        suggested_questions = [
            "What does a typical day look like in this home?",
            "When is the person most active during the day?",
            "Are there any unusual patterns I should know about?",
            "Which rooms are used the most?",
            "Is the daily routine healthy and consistent?",
            "What happens during the morning and evening?",
            "Are there any signs I should be concerned about?",
            "How can we improve safety in this home?"
        ]
        
        # Create buttons for suggested questions
        cols = st.columns(4)
        for idx, question in enumerate(suggested_questions):
            with cols[idx % 4]:
                if st.button(f"💬 {question[:28]}...", key=f"sq_{idx}", use_container_width=True):
                    st.session_state.pending_question = question
        
        st.divider()
        
        # Chat Container
        st.markdown("### 💬 Conversation")
        
        # Create a container for chat messages
        chat_container = st.container(height=400)
        
        with chat_container:
            # Display welcome message if no history
            if not st.session_state.chat_history:
                st.info("""
                👋 **Welcome! I'm your Smart Home Assistant!**
                
                I'm here to help you understand what's happening in this home in simple, everyday terms.
                
                **You can ask me about:**
                - 🏠 Daily routines and patterns (when do they wake up, eat, rest?)
                - 🚶 Which rooms are used most often
                - ⏰ Activity times throughout the day
                - ⚠️ Anything unusual or concerning
                - 💡 Tips to improve safety and comfort
                
                Just type your question below or click one of the suggested questions above!
                """)
            
            # Display chat history
            for msg in st.session_state.chat_history:
                if msg['role'] == 'user':
                    st.chat_message("user", avatar="👤").write(msg['content'])
                else:
                    st.chat_message("assistant", avatar="🏠").write(msg['content'])
        
        # Check for pending question from suggested questions
        if 'pending_question' in st.session_state and st.session_state.pending_question:
            user_input = st.session_state.pending_question
            st.session_state.pending_question = None
            process_chat_message(user_input, analyst)
            st.rerun()
        
        # Chat input
        user_input = st.chat_input("Type your question here... (e.g., 'What does a typical day look like?')")
        
        if user_input:
            process_chat_message(user_input, analyst)
            st.rerun()


def process_chat_message(user_input, analyst):
    """Process a chat message and get LLM response."""
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Get LLM response
    response = analyst.chat(user_input)
    
    # Add assistant message to history
    st.session_state.chat_history.append({"role": "assistant", "content": response})


def get_all_model_metrics():
    """Collect all available model metrics from session state."""
    metrics = {}
    event_log = st.session_state.get('event_log')
    
    if not event_log or not PM4PY_AVAILABLE:
        return metrics
    
    # Alpha Miner metrics
    if 'alpha_model' in st.session_state:
        net, im, fm = st.session_state.alpha_model
        try:
            fitness = fitness_evaluator.apply(event_log, net, im, fm,
                variant=fitness_evaluator.Variants.TOKEN_BASED)['average_trace_fitness']
            precision = precision_evaluator.apply(event_log, net, im, fm,
                variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN)
            metrics['alpha'] = {
                'fitness': round(fitness, 4),
                'precision': round(precision, 4),
                'places': len(net.places),
                'transitions': len(net.transitions)
            }
        except:
            pass
    
    # Inductive Miner metrics
    if 'inductive_model' in st.session_state:
        net, im, fm = st.session_state.inductive_model
        try:
            fitness = fitness_evaluator.apply(event_log, net, im, fm,
                variant=fitness_evaluator.Variants.TOKEN_BASED)['average_trace_fitness']
            precision = precision_evaluator.apply(event_log, net, im, fm,
                variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN)
            metrics['inductive'] = {
                'fitness': round(fitness, 4),
                'precision': round(precision, 4),
                'places': len(net.places),
                'transitions': len(net.transitions)
            }
        except:
            pass
    
    # Heuristic Miner metrics
    if 'heuristic_model' in st.session_state:
        try:
            from pm4py.objects.conversion.heuristics_net import converter as hn_converter
            heu_net = st.session_state.heuristic_model
            heu_petri_net, heu_im, heu_fm = hn_converter.apply(heu_net)
            
            fitness = fitness_evaluator.apply(event_log, heu_petri_net, heu_im, heu_fm,
                variant=fitness_evaluator.Variants.TOKEN_BASED)['average_trace_fitness']
            precision = precision_evaluator.apply(event_log, heu_petri_net, heu_im, heu_fm,
                variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN)
            metrics['heuristic'] = {
                'fitness': round(fitness, 4),
                'precision': round(precision, 4),
                'places': len(heu_petri_net.places),
                'transitions': len(heu_petri_net.transitions)
            }
        except:
            pass
    
    return metrics


def show_reports_page():
    """Display and generate reports."""
    st.header("📄 Analysis Reports")
    
    if not st.session_state.data_loaded:
        st.warning("Please load data first.")
        return
    
    st.subheader("📊 Available Reports")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Quick Statistics Report")
        if st.button("📈 Generate Stats Report"):
            event_log_df = st.session_state.event_log_df
            df = st.session_state.df
            
            stats = prepare_process_stats(event_log_df)
            
            report = f"""
# Process Mining Statistics Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Dataset Overview
- **Total Events:** {stats['total_events']:,}
- **Total Cases:** {stats['total_cases']}
- **Unique Activities:** {stats['unique_activities']}

## Case Statistics
- **Average Case Length:** {stats['avg_case_length']:.2f} events
- **Min Case Length:** {stats['min_case_length']} events
- **Max Case Length:** {stats['max_case_length']} events
- **Average Duration:** {stats['avg_case_duration_hours']:.2f} hours

## Top 10 Activities
"""
            top_activities = df['activity'].value_counts().head(10)
            for i, (act, count) in enumerate(top_activities.items(), 1):
                report += f"{i}. {act}: {count:,}\n"
            
            st.markdown(report)
            
            # Download button - PDF format
            if PDF_AVAILABLE:
                pdf_content = generate_pdf_report("Process Mining Statistics Report", report)
                st.download_button(
                    "📥 Download Report (PDF)",
                    pdf_content,
                    "process_mining_stats.pdf",
                    "application/pdf"
                )
            else:
                st.warning("PDF export not available. Install fpdf2: pip install fpdf2")
    
    with col2:
        st.markdown("### LLM Comprehensive Report")
        if LLM_AVAILABLE:
            if st.button("🤖 Generate LLM Report"):
                with st.spinner("Generating comprehensive report with LLM... This may take a minute."):
                    analyst = st.session_state.analyst
                    event_log_df = st.session_state.event_log_df
                    df = st.session_state.df
                    
                    # Prepare all data
                    process_stats = prepare_process_stats(event_log_df)
                    temporal_patterns = prepare_temporal_patterns(event_log_df)
                    activity_counts = df['activity'].value_counts()
                    
                    # Use simple metrics for demo
                    metrics = {
                        "alpha": {"fitness": 0.75, "precision": 0.80, "generalization": 0.65, "simplicity": 0.45},
                        "heuristic": {"fitness": 0.85, "precision": 0.75, "generalization": 0.70, "simplicity": 0.50},
                        "inductive": {"fitness": 0.95, "precision": 0.70, "generalization": 0.80, "simplicity": 0.40}
                    }
                    
                    variants_info = {"total_variants": event_log_df['case_id'].nunique()}
                    
                    report = analyst.generate_full_report(
                        metrics,
                        event_log_df,
                        activity_counts,
                        temporal_patterns,
                        variants_info,
                        process_stats
                    )
                    
                    st.markdown(report)
                    
                    # Download button - PDF format
                    if PDF_AVAILABLE:
                        pdf_content = generate_pdf_report("LLM Analysis Report", report)
                        if pdf_content:
                            st.download_button(
                                "📥 Download Report (PDF)",
                                pdf_content,
                                "llm_analysis_report.pdf",
                                "application/pdf"
                            )
                        else:
                            # Fallback to text file
                            st.download_button(
                                "📥 Download Report (TXT)",
                                report,
                                "llm_analysis_report.txt",
                                "text/plain"
                            )
                    else:
                        st.download_button(
                            "📥 Download Report (TXT)",
                            report,
                            "llm_analysis_report.txt",
                            "text/plain"
                        )
        else:
            st.info("LLM module not available for comprehensive reports.")


if __name__ == "__main__":
    main()
