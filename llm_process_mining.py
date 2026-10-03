"""
LLM-Powered Process Mining Module
==================================

This module integrates OpenAI LLM capabilities for:
1. Model Evaluation and Report Generation
2. Problem and Anomaly Detection
3. Process Optimization Suggestions
4. Next Event/Activity Prediction
5. Incremental Learning and Process Revision

Author: Process Mining Assignment
Date: January 2026
"""

import os
import json
from datetime import datetime
import pandas as pd
import numpy as np

# Set OpenAI API Key - Load from environment variable
# Set your key: export OPENAI_API_KEY="your-key-here"
# Or create a .env file with OPENAI_API_KEY=your-key-here
if "OPENAI_API_KEY" not in os.environ:
    print("⚠️  Warning: OPENAI_API_KEY not set in environment variables")
    print("   Set it with: export OPENAI_API_KEY='your-key-here'")

from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()


class LLMProcessMiningAnalyst:
    """
    LLM-powered analyst for process mining evaluation and insights.
    """
    
    def __init__(self, model="gpt-4o-mini"):
        """
        Initialize the LLM analyst.
        
        Parameters:
        -----------
        model : str
            OpenAI model to use (default: gpt-4o-mini for cost efficiency)
        """
        self.model = model
        self.conversation_history = []
        self.analysis_context = {}
        
    def _call_llm(self, prompt, system_prompt=None, temperature=0.7):
        """
        Call the OpenAI LLM with a prompt.
        
        Parameters:
        -----------
        prompt : str
            User prompt
        system_prompt : str, optional
            System prompt for context
        temperature : float
            Temperature for response generation
            
        Returns:
        --------
        str
            LLM response
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling LLM: {str(e)}"
    
    def set_analysis_context(self, metrics, event_log_stats, activity_stats, temporal_stats):
        """
        Set the context for analysis with process mining results.
        
        Parameters:
        -----------
        metrics : dict
            Dictionary containing metrics for all models
        event_log_stats : dict
            Statistics about the event log
        activity_stats : dict
            Activity frequency statistics
        temporal_stats : dict
            Temporal pattern statistics
        """
        self.analysis_context = {
            "metrics": metrics,
            "event_log_stats": event_log_stats,
            "activity_stats": activity_stats,
            "temporal_stats": temporal_stats
        }
    
    def _build_context_summary(self):
        """
        Build a formatted summary of the analysis context for the LLM.
        
        Returns:
        --------
        str
            Formatted context summary
        """
        summary_parts = []
        
        # Event Log Statistics
        if self.analysis_context.get('event_log_stats'):
            stats = self.analysis_context['event_log_stats']
            summary_parts.append(f"""
### Event Log Statistics:
- Total Events: {stats.get('total_events', 'N/A'):,}
- Total Cases (Days): {stats.get('total_cases', 'N/A')}
- Unique Activities: {stats.get('unique_activities', 'N/A')}
- Average Case Length: {stats.get('avg_case_length', 'N/A'):.2f} events
- Min Case Length: {stats.get('min_case_length', 'N/A')} events
- Max Case Length: {stats.get('max_case_length', 'N/A')} events
- Average Case Duration: {stats.get('avg_case_duration_hours', 'N/A'):.2f} hours""")
        
        # Model Metrics
        if self.analysis_context.get('metrics'):
            metrics = self.analysis_context['metrics']
            if metrics:
                summary_parts.append("\n### Process Mining Model Metrics:")
                for model_name, model_metrics in metrics.items():
                    summary_parts.append(f"""
**{model_name.title()} Miner:**
- Fitness: {model_metrics.get('fitness', 'N/A')} (how well the model replays traces)
- Precision: {model_metrics.get('precision', 'N/A')} (how precisely the model fits the log)
- Places: {model_metrics.get('places', 'N/A')}
- Transitions: {model_metrics.get('transitions', 'N/A')}""")
        
        # Activity Statistics
        if self.analysis_context.get('activity_stats'):
            stats = self.analysis_context['activity_stats']
            top_5 = dict(list(stats.items())[:5]) if isinstance(stats, dict) else {}
            if top_5:
                summary_parts.append(f"""
### Top 5 Activities by Frequency:
{json.dumps(top_5, indent=2)}""")
        
        # Temporal Patterns
        if self.analysis_context.get('temporal_stats'):
            temporal = self.analysis_context['temporal_stats']
            summary_parts.append(f"""
### Temporal Patterns:
{json.dumps(temporal, indent=2, default=str)}""")
        
        if not summary_parts:
            return "No analysis context available yet. Please load data and run process discovery."
        
        return "\n".join(summary_parts)
    
    def generate_model_evaluation_report(self, metrics):
        """
        Generate a comprehensive evaluation report for all discovered models.
        
        Parameters:
        -----------
        metrics : dict
            Dictionary with metrics for Alpha, Heuristic, and Inductive miners
            
        Returns:
        --------
        str
            Detailed evaluation report
        """
        system_prompt = """You are an expert process mining analyst. Your task is to evaluate 
        process discovery models based on their conformance metrics and provide actionable insights.
        Be specific, technical, and provide clear recommendations."""
        
        prompt = f"""
        Please evaluate the following process mining models discovered from a Smart Home (CASAS Aruba) dataset.
        The dataset contains sensor activations from motion sensors, door sensors, and temperature sensors
        tracking daily activities of an elderly person living alone.

        ## Model Metrics

        ### Alpha Miner
        - Fitness: {metrics.get('alpha', {}).get('fitness', 'N/A')}
        - Precision: {metrics.get('alpha', {}).get('precision', 'N/A')}
        - Generalization: {metrics.get('alpha', {}).get('generalization', 'N/A')}
        - Simplicity: {metrics.get('alpha', {}).get('simplicity', 'N/A')}

        ### Heuristic Miner
        - Fitness: {metrics.get('heuristic', {}).get('fitness', 'N/A')}
        - Precision: {metrics.get('heuristic', {}).get('precision', 'N/A')}
        - Generalization: {metrics.get('heuristic', {}).get('generalization', 'N/A')}
        - Simplicity: {metrics.get('heuristic', {}).get('simplicity', 'N/A')}

        ### Inductive Miner
        - Fitness: {metrics.get('inductive', {}).get('fitness', 'N/A')}
        - Precision: {metrics.get('inductive', {}).get('precision', 'N/A')}
        - Generalization: {metrics.get('inductive', {}).get('generalization', 'N/A')}
        - Simplicity: {metrics.get('inductive', {}).get('simplicity', 'N/A')}

        Please provide:
        1. **Individual Model Analysis**: Evaluate each model's strengths and weaknesses
        2. **Comparative Analysis**: Compare the three models
        3. **Best Model Recommendation**: Which model is best for this smart home use case and why
        4. **Metric Interpretation**: Explain what each metric means in practical terms
        5. **Improvement Suggestions**: How could the models or analysis be improved
        """
        
        return self._call_llm(prompt, system_prompt)
    
    def detect_anomalies(self, event_log_df, activity_counts, temporal_patterns):
        """
        Detect anomalies and problems in the process.
        
        Parameters:
        -----------
        event_log_df : pd.DataFrame
            Event log dataframe
        activity_counts : pd.Series
            Activity frequency counts
        temporal_patterns : dict
            Temporal pattern statistics
            
        Returns:
        --------
        str
            Anomaly detection report
        """
        system_prompt = """You are an expert in anomaly detection for smart home and IoT systems.
        Analyze the provided data to identify unusual patterns, potential issues, and anomalies
        that could indicate problems or interesting behaviors."""
        
        # Prepare statistics for LLM
        top_activities = activity_counts.head(10).to_dict() if hasattr(activity_counts, 'head') else activity_counts
        
        prompt = f"""
        Analyze the following smart home sensor data for anomalies and problems:

        ## Activity Statistics
        - Total events: {len(event_log_df) if hasattr(event_log_df, '__len__') else 'N/A'}
        - Unique activities: {event_log_df['activity'].nunique() if 'activity' in event_log_df.columns else 'N/A'}
        - Top 10 activities (frequency): {json.dumps(top_activities, indent=2)}

        ## Temporal Patterns
        {json.dumps(temporal_patterns, indent=2, default=str)}

        Please identify:
        1. **Unusual Activity Patterns**: Any activities with abnormal frequencies
        2. **Temporal Anomalies**: Strange timing patterns (night activity, irregular schedules)
        3. **Sensor Issues**: Potential sensor malfunctions or data quality problems
        4. **Behavioral Concerns**: Patterns that might indicate health or safety issues
        5. **Missing Activities**: Expected activities that seem to be missing
        6. **Recommendations**: Actions to investigate or address these anomalies
        """
        
        return self._call_llm(prompt, system_prompt)
    
    def optimize_process(self, process_stats, variants_info):
        """
        Suggest process optimizations based on discovered patterns.
        
        Parameters:
        -----------
        process_stats : dict
            Process statistics
        variants_info : dict
            Information about trace variants
            
        Returns:
        --------
        str
            Process optimization suggestions
        """
        system_prompt = """You are a process optimization expert specializing in smart home 
        and IoT systems. Provide practical suggestions to improve daily routines and 
        system efficiency based on process mining insights."""
        
        prompt = f"""
        Based on the following process mining analysis of a smart home system, suggest optimizations:

        ## Process Statistics
        {json.dumps(process_stats, indent=2, default=str)}

        ## Trace Variants (Process Paths)
        {json.dumps(variants_info, indent=2, default=str)}

        Please provide:
        1. **Routine Optimizations**: How can daily routines be improved
        2. **Energy Efficiency**: Suggestions for reducing energy consumption
        3. **Safety Improvements**: Recommendations for enhancing safety
        4. **Automation Opportunities**: Activities that could be automated
        5. **Sensor Placement**: Suggestions for better sensor coverage
        6. **Process Simplification**: Ways to streamline activities
        """
        
        return self._call_llm(prompt, system_prompt)
    
    def predict_next_activity(self, recent_activities, activity_patterns):
        """
        Predict the next likely activity based on patterns.
        
        Parameters:
        -----------
        recent_activities : list
            List of recent activities
        activity_patterns : dict
            Historical activity transition patterns
            
        Returns:
        --------
        str
            Prediction with explanation
        """
        system_prompt = """You are a predictive analytics expert for smart home systems.
        Based on historical patterns and recent activities, predict what activity is most
        likely to occur next and explain your reasoning."""
        
        prompt = f"""
        Based on the smart home activity patterns, predict the next activity:

        ## Recent Activity Sequence (last 10 events)
        {json.dumps(recent_activities[-10:] if len(recent_activities) > 10 else recent_activities, indent=2)}

        ## Historical Activity Transition Patterns
        {json.dumps(activity_patterns, indent=2, default=str)}

        Please provide:
        1. **Most Likely Next Activity**: What activity will probably happen next
        2. **Confidence Level**: How confident are you (low/medium/high)
        3. **Alternative Predictions**: Other possible activities
        4. **Reasoning**: Explain the pattern that led to this prediction
        5. **Time Estimate**: When is this activity likely to occur
        """
        
        return self._call_llm(prompt, system_prompt)
    
    def incremental_learning_suggestions(self, current_model_info, new_data_stats):
        """
        Provide suggestions for incremental learning and model revision.
        
        Parameters:
        -----------
        current_model_info : dict
            Information about current process model
        new_data_stats : dict
            Statistics about new incoming data
            
        Returns:
        --------
        str
            Incremental learning recommendations
        """
        system_prompt = """You are an expert in online/incremental machine learning and process mining.
        Provide guidance on how to update process models with new data while maintaining accuracy."""
        
        prompt = f"""
        Provide recommendations for incrementally updating the process model:

        ## Current Model Information
        {json.dumps(current_model_info, indent=2, default=str)}

        ## New Data Statistics
        {json.dumps(new_data_stats, indent=2, default=str)}

        Please provide:
        1. **Model Update Strategy**: How to incorporate new data
        2. **Drift Detection**: Signs that the process has changed
        3. **Retraining Triggers**: When to retrain the full model
        4. **Data Retention Policy**: How much historical data to keep
        5. **Validation Approach**: How to validate updated models
        6. **Concept Drift Handling**: Strategies for handling changing patterns
        """
        
        return self._call_llm(prompt, system_prompt)
    
    def chat(self, user_message):
        """
        Interactive chat for asking questions about the process mining results.
        
        Parameters:
        -----------
        user_message : str
            User's question or message
            
        Returns:
        --------
        str
            LLM response
        """
        # Build comprehensive context
        context_summary = self._build_context_summary()
        
        system_prompt = f"""You are a friendly and helpful Smart Home Activity Assistant. 
        You help people understand what's happening in their smart home by analyzing sensor data.
        
        IMPORTANT: The user is NOT a technical person. You must:
        - Use simple, everyday language (like explaining to a friend or family member)
        - AVOID technical jargon like "Petri nets", "conformance checking", "token replay"
        - Use analogies and real-world examples to explain concepts
        - Focus on practical insights about daily life and routines
        - Be warm, conversational, and encouraging
        
        ## WHAT YOU'RE ANALYZING:
        This smart home belongs to an elderly person living alone. Sensors track their 
        movements throughout the day - when they wake up, use the kitchen, bathroom, etc.
        
        ## YOUR DATA:
        {context_summary}

        ## HOW TO EXPLAIN THINGS SIMPLY:
        
        Instead of "Fitness metric of 1.0":
        ✅ Say: "The system can perfectly follow and understand all the daily routines"
        
        Instead of "Precision of 0.44":
        ✅ Say: "The model is moderately focused - it captures the main patterns but also allows for some flexibility in daily routines"
        
        Instead of "Inductive Miner algorithm":
        ✅ Say: "The pattern-finding method that works best for this home"
        
        Instead of "Process discovery":
        ✅ Say: "Finding patterns in daily activities"
        
        Instead of "Anomaly detection":
        ✅ Say: "Spotting unusual or concerning changes in routine"
        
        ## YOUR RESPONSE STYLE:
        - Start with a friendly greeting or acknowledgment
        - Use bullet points and short paragraphs (easy to read)
        - Include emojis sparingly to make it friendly 🏠
        - Give practical, actionable advice when relevant
        - If asked about technical details, explain in simple terms first, then offer more detail if they want
        - Relate everything back to real-life activities (sleeping, eating, moving around the house)
        
        ## EXAMPLE RESPONSES:
        
        User: "What patterns do you see?"
        Good response: "Looking at the activity in this home, I can see some clear daily patterns! 🏠
        
        **Morning routine**: Most activity starts around 7-8 AM, likely when they wake up
        **Busiest areas**: The kitchen and living room see the most movement
        **Evening wind-down**: Activity decreases after 9 PM
        
        This looks like a pretty healthy, consistent routine!"

        Remember: You're helping someone understand their loved one's daily life, not giving a technical report."""
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Build messages with history
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.conversation_history[-10:])  # Keep last 10 messages
        
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1500
            )
            assistant_message = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            return assistant_message
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_full_report(self, metrics, event_log_df, activity_counts, 
                            temporal_patterns, variants_info, process_stats):
        """
        Generate a comprehensive analysis report.
        
        Parameters:
        -----------
        metrics : dict
            Model metrics
        event_log_df : pd.DataFrame
            Event log
        activity_counts : pd.Series
            Activity frequencies
        temporal_patterns : dict
            Temporal statistics
        variants_info : dict
            Variant information
        process_stats : dict
            Process statistics
            
        Returns:
        --------
        str
            Full markdown report
        """
        print("\n🤖 Generating LLM-Powered Analysis Report...")
        print("   This may take a moment...\n")
        
        # Generate individual sections
        print("   📊 Evaluating models...")
        model_eval = self.generate_model_evaluation_report(metrics)
        
        print("   🔍 Detecting anomalies...")
        anomalies = self.detect_anomalies(event_log_df, activity_counts, temporal_patterns)
        
        print("   ⚡ Generating optimization suggestions...")
        optimizations = self.optimize_process(process_stats, variants_info)
        
        # Compile full report
        report = f"""
# 📊 LLM-Powered Process Mining Analysis Report
## CASAS Aruba Smart Home Dataset
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 1. Executive Summary

This report provides a comprehensive analysis of the smart home process mining results,
leveraging Large Language Model (LLM) capabilities for deeper insights and actionable
recommendations.

---

## 2. Model Evaluation

{model_eval}

---

## 3. Anomaly Detection

{anomalies}

---

## 4. Process Optimization Recommendations

{optimizations}

---

## 5. Technical Appendix

### Metrics Calculation Methods

| Metric | Method | Description |
|--------|--------|-------------|
| Fitness | Token-based Replay | Measures how well traces can be replayed on the model |
| Precision | ETConformance | Measures how much extra behavior the model allows |
| Generalization | Transition Coverage | Measures model's ability to generalize to unseen traces |
| Simplicity | Inverse Arc Degree | Measures structural complexity of the model |

### Dataset Information
- **Source:** CASAS Aruba Smart Home Dataset
- **Total Events:** {len(event_log_df) if hasattr(event_log_df, '__len__') else 'N/A'}
- **Unique Activities:** {event_log_df['activity'].nunique() if 'activity' in event_log_df.columns else 'N/A'}

---

*Report generated using OpenAI GPT-4o-mini*
"""
        return report


def prepare_metrics_for_llm(alpha_metrics, heuristic_metrics, inductive_metrics):
    """
    Prepare metrics dictionary for LLM analysis.
    
    Parameters:
    -----------
    alpha_metrics : dict
        Alpha miner metrics
    heuristic_metrics : dict
        Heuristic miner metrics
    inductive_metrics : dict
        Inductive miner metrics
        
    Returns:
    --------
    dict
        Combined metrics dictionary
    """
    return {
        "alpha": alpha_metrics if alpha_metrics else {},
        "heuristic": heuristic_metrics if heuristic_metrics else {},
        "inductive": inductive_metrics if inductive_metrics else {}
    }


def prepare_temporal_patterns(event_log_df):
    """
    Prepare temporal pattern statistics for LLM analysis.
    
    Parameters:
    -----------
    event_log_df : pd.DataFrame
        Event log dataframe
        
    Returns:
    --------
    dict
        Temporal pattern statistics
    """
    df = event_log_df.copy()
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.day_name()
    
    events_per_hour = df.groupby('hour').size().to_dict()
    events_per_day = df['day_of_week'].value_counts().to_dict()
    
    # Find peak hours
    peak_hour = max(events_per_hour, key=events_per_hour.get)
    quiet_hour = min(events_per_hour, key=events_per_hour.get)
    
    return {
        "events_per_hour": events_per_hour,
        "events_per_day": events_per_day,
        "peak_activity_hour": peak_hour,
        "quiet_hour": quiet_hour,
        "avg_events_per_hour": sum(events_per_hour.values()) / len(events_per_hour)
    }


def prepare_variants_info(variants, top_n=5):
    """
    Prepare variant information for LLM analysis.
    
    Parameters:
    -----------
    variants : dict
        Variants dictionary from pm4py
    top_n : int
        Number of top variants to include
        
    Returns:
    --------
    dict
        Variant information
    """
    sorted_variants = sorted(variants.items(), key=lambda x: len(x[1]), reverse=True)
    
    top_variants = []
    total_cases = sum(len(cases) for _, cases in sorted_variants)
    
    for i, (variant, cases) in enumerate(sorted_variants[:top_n], 1):
        activities = list(variant)[:5]  # First 5 activities
        top_variants.append({
            "rank": i,
            "count": len(cases),
            "percentage": f"{(len(cases) / total_cases * 100):.2f}%",
            "first_activities": activities,
            "total_activities": len(variant)
        })
    
    return {
        "total_variants": len(variants),
        "total_cases": total_cases,
        "top_variants": top_variants
    }


def prepare_process_stats(event_log_df):
    """
    Prepare process statistics for LLM analysis.
    
    Parameters:
    -----------
    event_log_df : pd.DataFrame
        Event log dataframe
        
    Returns:
    --------
    dict
        Process statistics
    """
    case_lengths = event_log_df.groupby('case_id').size()
    case_times = event_log_df.groupby('case_id')['timestamp'].agg(['min', 'max'])
    case_times['duration_hours'] = (case_times['max'] - case_times['min']).dt.total_seconds() / 3600
    
    return {
        "total_events": len(event_log_df),
        "total_cases": event_log_df['case_id'].nunique(),
        "unique_activities": event_log_df['activity'].nunique(),
        "avg_case_length": float(case_lengths.mean()),
        "min_case_length": int(case_lengths.min()),
        "max_case_length": int(case_lengths.max()),
        "avg_case_duration_hours": float(case_times['duration_hours'].mean()),
        "events_per_case": float(len(event_log_df) / event_log_df['case_id'].nunique())
    }


def get_recent_activities(event_log_df, n=20):
    """
    Get the most recent activities for prediction.
    
    Parameters:
    -----------
    event_log_df : pd.DataFrame
        Event log dataframe
    n : int
        Number of recent activities
        
    Returns:
    --------
    list
        List of recent activities
    """
    sorted_df = event_log_df.sort_values('timestamp', ascending=False)
    return sorted_df['activity'].head(n).tolist()


def get_activity_transitions(event_log_df):
    """
    Calculate activity transition probabilities.
    
    Parameters:
    -----------
    event_log_df : pd.DataFrame
        Event log dataframe
        
    Returns:
    --------
    dict
        Transition patterns
    """
    df = event_log_df.sort_values(['case_id', 'timestamp']).copy()
    df['next_activity'] = df.groupby('case_id')['activity'].shift(-1)
    
    # Get top transitions
    transitions = df.groupby(['activity', 'next_activity']).size().reset_index(name='count')
    transitions = transitions.sort_values('count', ascending=False).head(20)
    
    result = {}
    for _, row in transitions.iterrows():
        key = row['activity']
        if key not in result:
            result[key] = []
        result[key].append({
            "next": row['next_activity'],
            "count": int(row['count'])
        })
    
    return result


if __name__ == "__main__":
    # Test the LLM analyst
    print("Testing LLM Process Mining Analyst...")
    
    analyst = LLMProcessMiningAnalyst()
    
    # Test with sample metrics
    sample_metrics = {
        "alpha": {"fitness": 0.75, "precision": 0.82, "generalization": 0.68, "simplicity": 0.45},
        "heuristic": {"fitness": 0.88, "precision": 0.79, "generalization": 0.72, "simplicity": 0.52},
        "inductive": {"fitness": 0.95, "precision": 0.71, "generalization": 0.85, "simplicity": 0.38}
    }
    
    print("\n" + "="*60)
    print("MODEL EVALUATION REPORT")
    print("="*60)
    report = analyst.generate_model_evaluation_report(sample_metrics)
    print(report)
