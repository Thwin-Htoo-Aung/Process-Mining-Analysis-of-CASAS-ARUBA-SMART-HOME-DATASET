"""
Regenerate charts from CSV data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def generate_grouped_bar_chart(metrics_df, output_path):
    """Generate grouped bar chart comparing all metrics."""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    models = metrics_df['Model'].tolist()
    metrics = ['Fitness', 'Precision', 'Generalization', 'Simplicity']
    x = np.arange(len(metrics))
    width = 0.25
    
    colors = ['#2ecc71', '#3498db', '#e74c3c']  # Green, Blue, Red
    
    for i, model in enumerate(models):
        values = [metrics_df[metrics_df['Model'] == model][m].values[0] for m in metrics]
        offset = (i - len(models)/2 + 0.5) * width
        bars = ax.bar(x + offset, values, width, label=model, color=colors[i % len(colors)], 
                      edgecolor='black', linewidth=0.5)
        
        for bar, val in zip(bars, values):
            ax.annotate(f'{val:.3f}',
                       xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax.set_xlabel('Metric', fontsize=12, fontweight='bold')
    ax.set_ylabel('Score (0-1)', fontsize=12, fontweight='bold')
    ax.set_title('Process Mining Model Quality Metrics Comparison', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=11)
    ax.set_ylim(0, 1.15)
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    ax.set_facecolor('#f8f9fa')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: {output_path}")


def generate_individual_metric_charts(metrics_df, output_dir):
    """Generate individual bar charts for each metric."""
    metrics = ['Fitness', 'Precision', 'Generalization', 'Simplicity']
    colors = ['#2ecc71', '#3498db', '#e74c3c']
    icons = ['🎯', '🎯', '🔄', '📐']
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, metric in enumerate(metrics):
        ax = axes[idx]
        models = metrics_df['Model'].tolist()
        values = metrics_df[metric].tolist()
        
        bars = ax.bar(models, values, color=colors[:len(models)], edgecolor='black', linewidth=0.5)
        
        for bar, val in zip(bars, values):
            ax.annotate(f'{val:.4f}',
                       xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_title(f'{icons[idx]} {metric} Comparison', fontsize=12, fontweight='bold')
        ax.set_ylabel('Score', fontsize=10)
        ax.set_ylim(0, 1.15)
        ax.grid(axis='y', alpha=0.3)
        ax.set_facecolor('#f8f9fa')
    
    plt.suptitle('Individual Metric Analysis', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, 'individual_metrics.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: {output_path}")


def generate_radar_chart(metrics_df, output_path):
    """Generate radar chart for overall model comparison."""
    metrics = ['Fitness', 'Precision', 'Generalization', 'Simplicity']
    num_metrics = len(metrics)
    
    angles = np.linspace(0, 2 * np.pi, num_metrics, endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    colors = ['#2ecc71', '#3498db', '#e74c3c']
    
    for idx, (_, row) in enumerate(metrics_df.iterrows()):
        values = [row[m] for m in metrics]
        values += values[:1]
        
        ax.plot(angles, values, 'o-', linewidth=2, label=row['Model'], 
                color=colors[idx % len(colors)])
        ax.fill(angles, values, alpha=0.25, color=colors[idx % len(colors)])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics, fontsize=12, fontweight='bold')
    ax.set_ylim(0, 1)
    ax.set_title('Model Quality Radar Chart', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=10)
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: {output_path}")


def generate_heatmap(metrics_df, output_path):
    """Generate heatmap of metrics."""
    metrics = ['Fitness', 'Precision', 'Generalization', 'Simplicity']
    models = metrics_df['Model'].tolist()
    
    data = metrics_df[metrics].values
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    im = ax.imshow(data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    
    cbar = ax.figure.colorbar(im, ax=ax, shrink=0.8)
    cbar.ax.set_ylabel('Score', rotation=-90, va="bottom", fontsize=10)
    
    ax.set_xticks(np.arange(len(metrics)))
    ax.set_yticks(np.arange(len(models)))
    ax.set_xticklabels(metrics, fontsize=11, fontweight='bold')
    ax.set_yticklabels(models, fontsize=11, fontweight='bold')
    
    for i in range(len(models)):
        for j in range(len(metrics)):
            text = ax.text(j, i, f'{data[i, j]:.3f}',
                          ha="center", va="center", color="black", fontsize=12, fontweight='bold')
    
    ax.set_title('Model Metrics Heatmap', fontsize=14, fontweight='bold', pad=15)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: {output_path}")


def generate_summary_table_image(metrics_df, output_path):
    """Generate a table image of all metrics."""
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis('off')
    
    columns = ['Model', 'Fitness', 'Precision', 'Generalization', 'Simplicity']
    cell_text = []
    for _, row in metrics_df.iterrows():
        cell_text.append([
            row['Model'],
            f"{row['Fitness']:.4f}",
            f"{row['Precision']:.4f}",
            f"{row['Generalization']:.4f}",
            f"{row['Simplicity']:.4f}"
        ])
    
    table = ax.table(cellText=cell_text, colLabels=columns, cellLoc='center', loc='center',
                     colColours=['#3498db']*5)
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 2)
    
    for i in range(len(columns)):
        table[(0, i)].set_text_props(fontweight='bold', color='white')
        table[(0, i)].set_facecolor('#2c3e50')
    
    for i in range(1, len(cell_text) + 1):
        for j in range(1, len(columns)):
            val = float(cell_text[i-1][j])
            if val >= 0.8:
                table[(i, j)].set_facecolor('#d5f4e6')
            elif val >= 0.5:
                table[(i, j)].set_facecolor('#fef9e7')
            else:
                table[(i, j)].set_facecolor('#fadbd8')
    
    ax.set_title('Process Mining Model Metrics Summary', fontsize=14, fontweight='bold', pad=20, y=0.95)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: {output_path}")


def main():
    print("Regenerating charts from CSV...")
    
    output_dir = "metrics_images"
    metrics_df = pd.read_csv(os.path.join(output_dir, 'metrics_data.csv'))
    
    print("\nMetrics data:")
    print(metrics_df.to_string(index=False))
    print()
    
    generate_grouped_bar_chart(metrics_df, os.path.join(output_dir, 'grouped_bar_chart.png'))
    generate_individual_metric_charts(metrics_df, output_dir)
    generate_radar_chart(metrics_df, os.path.join(output_dir, 'radar_chart.png'))
    generate_heatmap(metrics_df, os.path.join(output_dir, 'heatmap.png'))
    generate_summary_table_image(metrics_df, os.path.join(output_dir, 'summary_table.png'))
    
    print("\nDone! All charts regenerated.")


if __name__ == "__main__":
    main()
