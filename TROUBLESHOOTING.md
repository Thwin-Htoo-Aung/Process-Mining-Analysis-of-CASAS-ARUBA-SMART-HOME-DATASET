# Troubleshooting Guide - CASAS Aruba Process Mining

## Quick Diagnostics

### Check Your Environment
```bash
# Test Python version (need 3.8+)
python --version

# Test if pm4py is installed
python -c "import pm4py; print(f'pm4py version: {pm4py.__version__}')"

# Test if Graphviz is available
python -c "import graphviz; print('Graphviz OK')"

# Check if aruba.csv exists
ls -lh aruba.csv
```

---

## Common Errors and Solutions

### 1. ModuleNotFoundError: No module named 'pm4py'

**Error Message**:
```
ModuleNotFoundError: No module named 'pm4py'
```

**Solution**:
```bash
# Install required packages
pip install pm4py pandas numpy matplotlib seaborn

# Or use requirements.txt
pip install -r requirements.txt
```

**If still failing**:
```bash
# Upgrade pip first
pip install --upgrade pip

# Install with specific version
pip install pm4py==2.7.11
```

---

### 2. Graphviz ExecutableNotFound

**Error Message**:
```
graphviz.backend.execute.ExecutableNotFound: 
failed to execute ['dot', '-Kdot', '-Tpng'], make sure the Graphviz executables are on your systems' PATH
```

**Solution - Windows**:
1. Download Graphviz from: https://graphviz.org/download/
2. Install to default location: `C:\Program Files\Graphviz`
3. Add to PATH:
   - Search "Environment Variables" in Windows
   - Edit System PATH
   - Add: `C:\Program Files\Graphviz\bin`
4. Restart terminal/VS Code
5. Test: `dot -V`

**Solution - Linux**:
```bash
sudo apt-get update
sudo apt-get install graphviz
```

**Solution - macOS**:
```bash
brew install graphviz
```

**Python-only workaround**:
```python
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
```

---

### 3. Memory Error (Large Dataset)

**Error Message**:
```
MemoryError: Unable to allocate array
```

**Cause**: Loading 1.6M rows exceeds available RAM

**Solution 1: Use Sampling**:
```python
# In main() function
SAMPLE_SIZE = 50000  # Start with 50K events
```

**Solution 2: Increase Virtual Memory** (Windows):
1. System Properties → Advanced → Performance Settings
2. Advanced → Virtual Memory → Change
3. Set custom size (Initial: 8GB, Maximum: 16GB)

**Solution 3: Process in Chunks**:
```python
def load_aruba_data_chunked(filepath, chunksize=100000):
    chunks = []
    for chunk in pd.read_csv(filepath, names=column_names, chunksize=chunksize):
        # Process each chunk
        chunks.append(preprocess_chunk(chunk))
    return pd.concat(chunks)
```

---

### 4. Process Discovery Takes Forever

**Symptom**: Script hangs during Alpha/Heuristic/Inductive Miner

**Cause**: Too many unique activities or too many cases

**Solution 1: Reduce Sample Size**:
```python
SAMPLE_SIZE = 10000  # Try with 10K first
```

**Solution 2: Simplify Activities**:
```python
# Group similar activities
df_clean['activity'] = df_clean['sensor_id']  # Remove ON/OFF distinction
```

**Solution 3: Use Only Inductive Miner**:
```python
# Comment out Alpha and Heuristic miners
# alpha_net, alpha_im, alpha_fm = discover_process_alpha_miner(event_log)
tree, ind_net, ind_im, ind_fm = discover_process_inductive_miner(event_log)
```

**Solution 4: Filter Activities**:
```python
# Keep only top 20 most frequent activities
top_activities = event_log_df['activity'].value_counts().head(20).index
event_log_df = event_log_df[event_log_df['activity'].isin(top_activities)]
```

---

### 5. Empty or Trivial Process Models

**Symptom**: Process model has only 1-2 activities or looks too simple

**Cause**: Over-aggressive filtering or too small sample

**Solution 1: Check Event Count**:
```python
print(f"Events in log: {len(event_log_df)}")
print(f"Unique activities: {event_log_df['activity'].nunique()}")
```
- Need at least 1000+ events for meaningful models

**Solution 2: Reduce Noise Threshold**:
```python
TIME_THRESHOLD = 0.5  # Allow closer events (was 1 second)
```

**Solution 3: Disable Duplicate Removal**:
```python
REMOVE_DUPLICATES = False
```

**Solution 4: Increase Sample Size**:
```python
SAMPLE_SIZE = 100000  # Use more data
```

---

### 6. Spaghetti Models (Too Complex)

**Symptom**: Process model is unreadable, too many arrows/nodes

**Cause**: Too much variation in traces (common with smart home data)

**Solution 1: Use Heuristic Miner Only**:
```python
# It automatically filters low-frequency paths
heu_net = discover_process_heuristic_miner(event_log)
```

**Solution 2: Filter Trace Variants**:
```python
# Keep only top 20% most frequent traces
from pm4py.statistics.variants.log import get as variants_module

variants = variants_module.get_variants(event_log)
sorted_variants = sorted(variants.items(), key=lambda x: len(x[1]), reverse=True)

# Calculate 20% threshold
total_cases = len(event_log)
keep_variants = []
cumulative = 0

for variant, cases in sorted_variants:
    keep_variants.append(variant)
    cumulative += len(cases)
    if cumulative >= total_cases * 0.2:
        break

# Filter event log
filtered_log = pm4py.filter_variants(event_log, keep_variants)
```

**Solution 3: Abstract Activities**:
```python
# Merge similar sensors
activity_mapping = {
    'Bedroom_ON': 'Bedroom',
    'Bedroom_OFF': 'Bedroom',
    'Kitchen_ON': 'Kitchen',
    'Kitchen_OFF': 'Kitchen',
}
event_log_df['activity'] = event_log_df['activity'].map(activity_mapping)
```

---

### 7. "File too large" Error

**Error Message**:
```
Files above 50MB cannot be synchronized with extensions
```

**Cause**: VS Code/editor limit for large files

**Solution**: Use command line tools:
```bash
# View first lines
head -n 100 aruba.csv

# Count lines
wc -l aruba.csv

# View specific columns
cut -d',' -f1,3 aruba.csv | head -20

# Sample data
shuf -n 50000 aruba.csv > aruba_sample.csv
```

Then update script:
```python
FILEPATH = 'aruba_sample.csv'
SAMPLE_SIZE = None  # Use entire sample file
```

---

### 8. Timestamp Parsing Errors

**Error Message**:
```
ParserError: Unknown datetime string format
```

**Cause**: Unexpected date/time format in CSV

**Solution 1: Explicit Format**:
```python
df['timestamp'] = pd.to_datetime(
    df['date'] + ' ' + df['time'],
    format='%Y-%m-%d %H:%M:%S.%f'
)
```

**Solution 2: Try Inferring**:
```python
df['timestamp'] = pd.to_datetime(
    df['date'] + ' ' + df['time'],
    infer_datetime_format=True
)
```

**Solution 3: Handle Errors**:
```python
df['timestamp'] = pd.to_datetime(
    df['date'] + ' ' + df['time'],
    errors='coerce'  # NaT for invalid dates
)
df = df.dropna(subset=['timestamp'])
```

---

### 9. No Output Files Generated

**Symptom**: Script runs but no PNG files created

**Cause**: Visualization failed silently

**Solution 1: Check Error Messages**:
- Look for "✗ Visualization failed" in output
- Check if Graphviz is installed

**Solution 2: Test Graphviz Manually**:
```python
import graphviz
dot = graphviz.Digraph()
dot.node('A', 'Test')
dot.node('B', 'Node')
dot.edge('A', 'B')
dot.render('test_graph', format='png', cleanup=True)
```
- Should create `test_graph.png`

**Solution 3: Alternative Visualization**:
```python
# Use matplotlib instead
import matplotlib.pyplot as plt

# Simple activity bar chart
activity_counts.head(10).plot(kind='barh')
plt.savefig('manual_activity_freq.png')
```

---

### 10. Alpha Miner Fails

**Error Message**:
```
Alpha Miner failed: ...
```

**Cause**: Alpha Miner is very sensitive to noise and incompleteness

**Solution**: This is **expected** for smart home data!
- Use Heuristic Miner or Inductive Miner instead
- They are designed for real-world, noisy logs
- Alpha Miner is primarily educational/theoretical

**If you need Alpha Miner**:
1. Use heavily filtered, clean data
2. Reduce activities to 5-10 main ones
3. Accept that it may not work well for this dataset

---

## Performance Optimization

### For Slow Processing

**1. Reduce Data Volume**:
```python
# Option A: Sample rows
SAMPLE_SIZE = 20000

# Option B: Sample time range
df = df[df['timestamp'].dt.date == pd.to_datetime('2010-11-04').date()]

# Option C: Sample sensors
main_sensors = ['Bedroom', 'Kitchen', 'Bathroom', 'LivingRoom']
df = df[df['sensor_id'].isin(main_sensors)]
```

**2. Optimize DataFrame Operations**:
```python
# Use category dtype for repeated strings
df['sensor_id'] = df['sensor_id'].astype('category')
df['activity'] = df['activity'].astype('category')

# Use more efficient data types
df['sensor_value'] = df['sensor_value'].astype('category')
```

**3. Parallelize When Possible**:
```python
# Use multiple CPU cores for pandas operations
import multiprocessing
cores = multiprocessing.cpu_count()

# Set in pandas
import pandas as pd
pd.set_option('mode.chained_assignment', None)
```

---

## Validation Checks

### Verify Your Event Log is Correct

```python
def validate_event_log(event_log_df):
    """Run validation checks on event log"""
    
    print("Event Log Validation:")
    print("-" * 50)
    
    # Check 1: Required columns
    required = ['case_id', 'activity', 'timestamp']
    missing = [c for c in required if c not in event_log_df.columns]
    if missing:
        print(f"❌ Missing columns: {missing}")
    else:
        print(f"✅ All required columns present")
    
    # Check 2: No null values
    nulls = event_log_df[required].isnull().sum()
    if nulls.any():
        print(f"❌ Null values found:\n{nulls[nulls > 0]}")
    else:
        print(f"✅ No null values")
    
    # Check 3: Timestamps are sorted
    is_sorted = event_log_df.groupby('case_id')['timestamp'].apply(
        lambda x: x.is_monotonic_increasing
    ).all()
    if is_sorted:
        print(f"✅ Timestamps sorted within cases")
    else:
        print(f"❌ Timestamps not sorted - run sort!")
    
    # Check 4: Reasonable number of activities
    n_activities = event_log_df['activity'].nunique()
    if 5 <= n_activities <= 100:
        print(f"✅ Activities: {n_activities} (reasonable)")
    elif n_activities < 5:
        print(f"⚠️ Activities: {n_activities} (too few, may be over-filtered)")
    else:
        print(f"⚠️ Activities: {n_activities} (many, may be complex)")
    
    # Check 5: Reasonable case sizes
    case_sizes = event_log_df.groupby('case_id').size()
    print(f"✅ Case sizes: {case_sizes.min()}-{case_sizes.max()} events")
    print(f"   Mean: {case_sizes.mean():.1f}, Median: {case_sizes.median():.1f}")
    
    return True

# Run validation
validate_event_log(event_log_df)
```

---

## Getting Help

### Information to Provide

When asking for help, include:

1. **Error message** (full traceback)
2. **Environment info**:
   ```bash
   python --version
   pip list | grep -E "(pm4py|pandas|numpy)"
   ```
3. **Sample size** you're using
4. **Basic statistics**:
   ```python
   print(f"Events: {len(event_log_df)}")
   print(f"Cases: {event_log_df['case_id'].nunique()}")
   print(f"Activities: {event_log_df['activity'].nunique()}")
   ```
5. **What you've already tried**

### Useful Resources

- **pm4py Documentation**: https://pm4py.fit.fraunhofer.de/
- **pm4py Forum**: https://groups.google.com/g/pm4py-users
- **CASAS Dataset**: http://casas.wsu.edu/
- **Process Mining Book**: van der Aalst, W. M. P. (2016)

---

## Emergency: Just Get It Working!

If nothing else works, use this minimal script:

```python
"""Minimal working version"""
import pandas as pd
import pm4py

# Load small sample
df = pd.read_csv('aruba.csv', names=['date', 'time', 'sensor', 'value'], nrows=10000)

# Create event log
df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'])
df['case_id'] = df['date']
df['activity'] = df['sensor']

# Convert to pm4py
log_df = df[['case_id', 'activity', 'timestamp']].copy()
log_df['case:concept:name'] = log_df['case_id']
log_df['concept:name'] = log_df['activity']
log_df['time:timestamp'] = log_df['timestamp']

event_log = pm4py.convert_to_event_log(log_df)

# Discover with Inductive Miner (most robust)
tree = pm4py.discover_process_tree_inductive(event_log)

# View in console (if visualization fails)
print("Process tree discovered successfully!")
print(f"Cases: {len(event_log)}")
print(f"Activities: {log_df['activity'].nunique()}")

# Try to visualize
try:
    pm4py.view_process_tree(tree)
    print("✅ Visualization worked!")
except:
    print("⚠️ Visualization failed (likely Graphviz issue)")
    print("But process discovery still worked!")
```

Run with: `python minimal_version.py`

---

**Last Updated**: January 2026  
**For**: CASAS Aruba Process Mining Assignment
