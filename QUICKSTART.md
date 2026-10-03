# Quick Start Guide - Getting Started in 5 Minutes

## Step 1: Install Python Dependencies (2 minutes)

Open your terminal and navigate to the project folder:

```bash
cd "c:\Users\nfsbu\Desktop\FAST\Developement\ProcessMining1"
```

Install required packages:

```bash
pip install -r requirements.txt
```

**Expected output**:
```
Successfully installed pandas-2.0.0 numpy-1.24.0 pm4py-2.7.11 ...
```

## Step 2: Install Graphviz (2 minutes)

### Windows:
1. Download installer: https://graphviz.org/download/
2. Run installer (keep default location: `C:\Program Files\Graphviz`)
3. **Important**: Add to PATH:
   - Press Windows key, type "environment"
   - Click "Edit system environment variables"
   - Click "Environment Variables"
   - Under "System variables", find "Path", click "Edit"
   - Click "New", add: `C:\Program Files\Graphviz\bin`
   - Click OK on all windows
4. **Restart your terminal/VS Code**

### Test Installation:
```bash
dot -V
```
Should show: `dot - graphviz version 2.xx.x`

## Step 3: Run the Analysis (1 minute)

### Quick Test (10K events):
```bash
python process_mining_aruba.py
```

This will:
- ✅ Load 50,000 sample events (fast!)
- ✅ Preprocess and create event log
- ✅ Run 3 process discovery algorithms
- ✅ Generate 7 visualization files
- ⏱️ Takes ~1-2 minutes

### Expected Output Files:
1. `alpha_miner_model.png`
2. `heuristic_miner_model.png`
3. `inductive_miner_tree.png`
4. `inductive_miner_model.png`
5. `activity_frequency.png`
6. `throughput_time_analysis.png`
7. `temporal_patterns.png`

## Step 4: View Results

Open any generated PNG file to see your process models!

**Best to start with**:
- `activity_frequency.png` - Understand what activities are most common
- `inductive_miner_tree.png` - See the discovered process structure
- `heuristic_miner_model.png` - See main process flow

## Step 5: Customize (Optional)

Edit `process_mining_aruba.py`, line ~785:

```python
# Configuration
FILEPATH = 'aruba.csv'
SAMPLE_SIZE = 50000  # ← Change this!
CASE_STRATEGY = 'daily'  # or 'session'
REMOVE_DUPLICATES = True
TIME_THRESHOLD = 1
```

### Common Configurations:

**Quick test (1 minute)**:
```python
SAMPLE_SIZE = 10000
```

**Detailed analysis (5 minutes)**:
```python
SAMPLE_SIZE = 100000
```

**Full dataset (15-30 minutes)**:
```python
SAMPLE_SIZE = None  # Process all 1.6M events
```

**Session-based cases**:
```python
CASE_STRATEGY = 'session'  # Instead of 'daily'
```

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'pm4py'"
**Solution**:
```bash
pip install pm4py pandas numpy matplotlib seaborn
```

### Problem: "Graphviz not found"
**Solution**:
1. Install Graphviz (see Step 2)
2. Add to PATH
3. **Restart terminal**
4. Test: `dot -V`

### Problem: "MemoryError"
**Solution**: Reduce sample size:
```python
SAMPLE_SIZE = 10000  # Use smaller sample
```

### Problem: Script hangs/takes forever
**Solution**: 
1. Reduce sample size
2. Use only Inductive Miner (comment out Alpha/Heuristic)

### Problem: Process models look messy
**Solution**: This is normal for smart home data!
- Use Heuristic Miner (filters noise)
- Reduce activities by grouping similar sensors
- See TROUBLESHOOTING.md for details

## Next Steps

### Explore Examples:
```bash
python quick_start_examples.py
```

Interactive menu with 7 examples:
1. Quick Analysis (10K events)
2. Session-Based Analysis
3. Inductive Miner Only
4. Specific Sensor Analysis
5. Custom Activity Definition
6. Time-Based Filtering
7. Export Event Log to CSV

### Read Documentation:
- **README.md** - Complete project overview
- **METHODOLOGY.md** - Deep dive into process mining concepts
- **TROUBLESHOOTING.md** - Detailed problem-solving guide

### Modify for Your Assignment:
1. Adjust case definitions (daily vs session)
2. Change activity mappings
3. Add your own analysis functions
4. Export results for your report

## Example Console Output

```
************************************************************
*  CASAS ARUBA SMART HOME - PROCESS MINING ANALYSIS       *
************************************************************

Configuration:
  - File: aruba.csv
  - Sample size: 50000
  - Case strategy: daily
  - Remove duplicates: True
  - Time threshold: 1s

============================================================
STEP 1: Loading Aruba Dataset
============================================================
✓ Loaded 50,000 rows and 4 columns
✓ Memory usage: 2.31 MB
✓ Date range: 2010-11-04 to 2010-11-10

============================================================
STEP 2: Preprocessing Data
============================================================
✓ Creating timestamp column...
✓ Sorting by timestamp...
✓ Validating data...
  - Removed 0 rows with missing values
✓ Removing duplicate sensor events (threshold: 1s)...
  - Removed 15,234 rapid-fire events (30.47%)
✓ Creating activity labels...

✓ Preprocessing complete!
  - Final dataset: 34,766 events
  - Unique sensors: 18
  - Unique activities: 36

============================================================
STEP 3: Creating Event Log for pm4py
============================================================
Case Strategy: daily
✓ Event log created successfully!
  - Total events: 34,766
  - Total cases: 7
  - Unique activities: 36
  - Avg events per case: 4966.57

[... continues with process discovery and analysis ...]

============================================================
ANALYSIS COMPLETE!
============================================================

Generated Files:
  1. alpha_miner_model.png
  2. heuristic_miner_model.png
  3. inductive_miner_tree.png
  4. inductive_miner_model.png
  5. activity_frequency.png
  6. throughput_time_analysis.png
  7. temporal_patterns.png

✓ Process mining analysis completed successfully!
```

## Ready to Go!

You now have a complete process mining solution for smart home data. 

**Start with**:
```bash
python process_mining_aruba.py
```

**Questions?** Check:
- README.md for overview
- METHODOLOGY.md for concepts
- TROUBLESHOOTING.md for problems

Good luck with your assignment! 🚀
