"""
Quick Start Examples - CASAS Aruba Process Mining
=================================================

This file demonstrates how to use individual functions from the main script
for specific analysis tasks.
"""

import pandas as pd
from process_mining_aruba import (
    load_aruba_data,
    preprocess_data,
    create_event_log,
    convert_to_pm4py_log,
    discover_process_inductive_miner,
    visualize_petri_net,
    analyze_activity_frequency
)

# ============================================================
# Example 1: Quick Analysis with Small Sample
# ============================================================

def quick_analysis():
    """
    Perform a quick analysis on a small sample for testing.
    """
    print("Example 1: Quick Analysis")
    print("-" * 60)
    
    # Load small sample (10,000 events)
    df = load_aruba_data('aruba.csv', sample_size=10000)
    
    # Preprocess
    df_clean = preprocess_data(df, remove_duplicates=True, time_threshold_seconds=1)
    
    # Create event log with daily cases
    event_log_df = create_event_log(df_clean, case_strategy='daily')
    
    # Quick statistics
    print(f"\nQuick Statistics:")
    print(f"  Total events: {len(event_log_df):,}")
    print(f"  Total cases: {event_log_df['case_id'].nunique()}")
    print(f"  Unique activities: {event_log_df['activity'].nunique()}")
    
    # Show activity frequency
    analyze_activity_frequency(event_log_df, top_n=10)


# ============================================================
# Example 2: Session-Based Analysis
# ============================================================

def session_based_analysis():
    """
    Analyze smart home data using session-based cases instead of daily.
    Sessions are separated by 2-hour gaps (likely sleep periods).
    """
    print("\nExample 2: Session-Based Analysis")
    print("-" * 60)
    
    # Load sample
    df = load_aruba_data('aruba.csv', sample_size=20000)
    
    # Preprocess
    df_clean = preprocess_data(df)
    
    # Create event log with session-based cases
    event_log_df = create_event_log(df_clean, case_strategy='session')
    
    print(f"\nSession Statistics:")
    session_lengths = event_log_df.groupby('case_id').size()
    print(f"  Total sessions: {len(session_lengths)}")
    print(f"  Avg events per session: {session_lengths.mean():.2f}")
    print(f"  Longest session: {session_lengths.max()} events")


# ============================================================
# Example 3: Process Discovery with Single Algorithm
# ============================================================

def discover_with_inductive_miner():
    """
    Focus on just the Inductive Miner for process discovery.
    Best choice for noisy smart home data.
    """
    print("\nExample 3: Inductive Miner Only")
    print("-" * 60)
    
    # Load and prepare data
    df = load_aruba_data('aruba.csv', sample_size=30000)
    df_clean = preprocess_data(df, remove_duplicates=True)
    event_log_df = create_event_log(df_clean, case_strategy='daily')
    event_log = convert_to_pm4py_log(event_log_df)
    
    # Discover process model
    tree, net, im, fm = discover_process_inductive_miner(event_log)
    
    # Visualize
    visualize_petri_net(net, im, fm, 
                       output_file='quick_inductive_model.png',
                       title='Inductive Miner - Quick Analysis')
    
    print("\n✓ Process model saved to: quick_inductive_model.png")


# ============================================================
# Example 4: Analyze Specific Sensors
# ============================================================

def analyze_specific_sensors():
    """
    Analyze activity patterns for specific sensors/rooms only.
    """
    print("\nExample 4: Specific Sensor Analysis")
    print("-" * 60)
    
    # Load data
    df = load_aruba_data('aruba.csv', sample_size=50000)
    
    # Filter for specific sensors (example: bedroom-related sensors)
    print("\nFiltering for bedroom-related sensors...")
    bedroom_sensors = df[df['sensor_id'].str.contains('Bedroom', case=False, na=False)]
    
    print(f"Events with 'Bedroom' sensors: {len(bedroom_sensors):,}")
    
    # Preprocess and create event log
    df_clean = preprocess_data(bedroom_sensors)
    event_log_df = create_event_log(df_clean, case_strategy='daily')
    
    # Analyze
    print("\nActivity Frequency (Bedroom sensors only):")
    analyze_activity_frequency(event_log_df, top_n=5)


# ============================================================
# Example 5: Custom Activity Definition
# ============================================================

def custom_activity_definition():
    """
    Create custom activity labels instead of using sensor_id + value.
    For example, group all ON events as "Activate" and OFF as "Deactivate".
    """
    print("\nExample 5: Custom Activity Definition")
    print("-" * 60)
    
    # Load and preprocess
    df = load_aruba_data('aruba.csv', sample_size=10000)
    df_clean = preprocess_data(df, remove_duplicates=False)  # Keep all events
    
    # Custom activity: Use room name + simplified action
    df_clean['custom_activity'] = df_clean.apply(
        lambda row: f"{row['sensor_id']}_{'Activate' if row['sensor_value'] == 'ON' else 'Deactivate'}",
        axis=1
    )
    
    # Create event log with custom activity
    event_log_df = create_event_log(df_clean, 
                                    case_strategy='daily',
                                    activity_column='custom_activity')
    
    print(f"\nCustom Activities (Top 10):")
    print(event_log_df['activity'].value_counts().head(10))


# ============================================================
# Example 6: Time-Based Filtering
# ============================================================

def analyze_specific_timeframe():
    """
    Analyze only events during specific time periods (e.g., daytime hours).
    """
    print("\nExample 6: Time-Based Filtering")
    print("-" * 60)
    
    # Load data
    df = load_aruba_data('aruba.csv', sample_size=50000)
    df_clean = preprocess_data(df)
    
    # Filter for daytime hours (8 AM to 8 PM)
    df_clean['hour'] = pd.to_datetime(df_clean['timestamp']).dt.hour
    daytime_df = df_clean[(df_clean['hour'] >= 8) & (df_clean['hour'] <= 20)]
    
    print(f"\nDaytime events (8 AM - 8 PM): {len(daytime_df):,}")
    print(f"Percentage of total: {len(daytime_df) / len(df_clean) * 100:.2f}%")
    
    # Create event log
    event_log_df = create_event_log(daytime_df, case_strategy='daily')
    
    print(f"\nDaytime Activity Patterns:")
    analyze_activity_frequency(event_log_df, top_n=10)


# ============================================================
# Example 7: Export Event Log to CSV
# ============================================================

def export_event_log():
    """
    Create and export event log to CSV for use in other tools.
    """
    print("\nExample 7: Export Event Log")
    print("-" * 60)
    
    # Load and prepare
    df = load_aruba_data('aruba.csv', sample_size=20000)
    df_clean = preprocess_data(df)
    event_log_df = create_event_log(df_clean, case_strategy='daily')
    
    # Export to CSV
    output_file = 'aruba_event_log.csv'
    event_log_df[['case_id', 'activity', 'timestamp']].to_csv(output_file, index=False)
    
    print(f"\n✓ Event log exported to: {output_file}")
    print(f"  Columns: case_id, activity, timestamp")
    print(f"  Rows: {len(event_log_df):,}")
    print(f"\nThis CSV can be imported into:")
    print(f"  - ProM (process mining tool)")
    print(f"  - Disco (Fluxicon)")
    print(f"  - Other pm4py scripts")


# ============================================================
# Main Menu
# ============================================================

def main():
    """
    Run example demonstrations.
    """
    print("=" * 60)
    print("CASAS ARUBA - QUICK START EXAMPLES")
    print("=" * 60)
    
    examples = {
        '1': ('Quick Analysis (10K events)', quick_analysis),
        '2': ('Session-Based Analysis', session_based_analysis),
        '3': ('Inductive Miner Only', discover_with_inductive_miner),
        '4': ('Specific Sensor Analysis', analyze_specific_sensors),
        '5': ('Custom Activity Definition', custom_activity_definition),
        '6': ('Time-Based Filtering', analyze_specific_timeframe),
        '7': ('Export Event Log to CSV', export_event_log),
    }
    
    print("\nAvailable Examples:")
    for key, (description, _) in examples.items():
        print(f"  {key}. {description}")
    print(f"  0. Run All Examples")
    print(f"  q. Quit")
    
    choice = input("\nSelect example to run (0-7, q): ").strip()
    
    if choice == 'q':
        print("Exiting...")
        return
    elif choice == '0':
        print("\nRunning all examples...\n")
        for _, func in examples.values():
            try:
                func()
                print("\n" + "=" * 60 + "\n")
            except Exception as e:
                print(f"Error: {e}")
    elif choice in examples:
        description, func = examples[choice]
        print(f"\nRunning: {description}\n")
        try:
            func()
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    # Uncomment to run specific example directly
    # quick_analysis()
    # session_based_analysis()
    # discover_with_inductive_miner()
    # analyze_specific_sensors()
    # custom_activity_definition()
    # analyze_specific_timeframe()
    # export_event_log()
    
    # Or run the interactive menu
    main()
