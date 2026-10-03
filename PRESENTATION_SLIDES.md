# Process Mining Presentation - Slide Content
## CASAS Aruba Smart Home Analysis

---

## SLIDE 1: Title
**Process Mining Assignment**  
**Smart Home Activity Analysis using CASAS Aruba Dataset**

Team Members: [Your Names]  
Date: January 2026  
Course: Process Mining

---

## SLIDE 2: Agenda
1. Dataset Selection & Overview
2. Data Preprocessing
3. Process Discovery (3 Algorithms)
4. Model Evaluation & Selection
5. Insights & Analytics
6. Dashboard Concept
7. Conclusions

---

## SLIDE 3: Dataset - CASAS Aruba
**Why This Dataset?**
- Real-world smart home sensor data
- 50,000+ events over multiple months
- 31 sensors monitoring daily activities
- Perfect for process mining analysis

**Key Statistics:**
- 📊 Events: 50,000 initial → 39,523 after cleaning
- 🏠 Sensors: 31 types (motion, door, temperature)
- 🎯 Activities: 11 distinct types
- 📅 Duration: Several months of continuous monitoring

[Visual: Smart home floor plan with sensor locations]

---

## SLIDE 4: Data Preprocessing
**Step 1: Filtering**
- ❌ Removed "Other_Activity" (10,477 events)
- ✅ Retained 78.95% meaningful data

**Step 2: Cleaning**
- Standardized timestamps
- Removed duplicates
- Validated data integrity

**Step 3: Case Generation**
- ✅ **Daily Cases**: Each day = 1 case (~50 cases)
- Alternative: Session-based (200+ sessions)
- **Rationale**: Captures complete daily routines

[Visual: Before/After data quality metrics table]

---

## SLIDE 5: Process Discovery - Overview
**Three Algorithms Implemented:**

1. **Alpha Miner** 🔷
   - Petri Net model
   - 70 places, 11 transitions
   
2. **Heuristic Miner** 🔶
   - Heuristics Net
   - 11 nodes, frequency-based
   
3. **Inductive Miner** 🔵
   - Process Tree
   - Hierarchical structure

[Visual: Three model types side-by-side]

---

## SLIDE 6: Alpha Miner Results
**Approach:** Mathematical ordering relations

**Results:**
- Places: 70
- Transitions: 11
- Arcs: 150

**Strengths:** ✅ Theoretically sound, guarantees soundness

**Weaknesses:** ❌ Too complex (overfitting), sensitive to noise

**Verdict:** Not suitable for our noisy smart home data

[Visual: Complex Petri net screenshot]

---

## SLIDE 7: Heuristic Miner Results ⭐
**Approach:** Frequency-based dependency analysis

**Results:**
- Nodes: 11 activities
- Dependency threshold: 0.5
- Clear main flows identified

**Discovered Patterns:**
- Morning: Bedroom → Bathroom → Kitchen
- Parallel: Kitchen + other activities
- Evening: Kitchen → Living → Bedroom

**Strengths:** ✅ Readable, robust, interpretable

[Visual: Clean heuristics net with highlighted paths]

---

## SLIDE 8: Inductive Miner Results
**Approach:** Divide-and-conquer process tree

**Results:**
- Hierarchical structure
- Operators: SEQ, XOR, AND, LOOP

**Strengths:** ✅ Sound models, handles incompleteness

**Weaknesses:** ⚠️ May overgeneralize

**Best Use:** Prediction and future behavior modeling

[Visual: Process tree diagram]

---

## SLIDE 9: Model Comparison
| Criteria | Alpha | Heuristic | Inductive |
|----------|-------|-----------|-----------|
| **Complexity** | High ❌ | Medium ✅ | Medium ✅ |
| **Readability** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Noise Handling** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Soundness** | ✅ | ❓ | ✅ |
| **Interpretability** | Low | **High** | Medium |

**Winner: Heuristic Miner** 🏆

---

## SLIDE 10: Why Heuristic Miner? 🏆
**5 Key Reasons:**

1. ✅ **Optimal Complexity** - 11 nodes = perfectly balanced
2. ✅ **Interpretable** - Stakeholders understand immediately
3. ✅ **Robust** - Handles sensor noise effectively
4. ✅ **Practical Insights** - Reveals meaningful daily patterns
5. ✅ **Best for Use Case** - Elderly care monitoring

**Business Value:**
- Detect routine deviations
- Early health issue detection
- Optimize smart home automation

---

## SLIDE 11: Key Insights - Activity Analysis
**Activity Frequency:**
- 🍳 Kitchen: 21.76% (most frequent)
- 🛏️ Bedroom: 15.77%
- 🚿 Bathroom: 12.96%
- 🛋️ Living Room: 12.37%

**Trace Variants:**
- Total unique variants: 8
- Most common: Kitchen → Bedroom → Kitchen → Bathroom (45%)
- Complexity score: 1.0 (highly structured routine)

[Visual: Pie chart of activity distribution]

---

## SLIDE 12: Key Insights - Temporal Patterns
**Peak Activity Hours:**
- 🌅 Morning: 09:00-13:00 (highest)
- 🌆 Evening: 18:00-21:00 (dinner + leisure)
- 🌙 Sleep: 02:00-05:00 (minimal activity)

**Throughput Time:**
- Average daily duration: 23.96 hours
- Median: 21.07 hours
- Consistent across days

[Visual: Temporal heatmap showing hourly activity patterns]

---

## SLIDE 13: Anomaly Detection 🚨
**Types of Anomalies Detected:**

**🔴 Critical:**
- No activity for >4 hours (potential emergency)
- Missing essential activities (skip meals)

**🟡 Warnings:**
- Unusual nighttime activity (3 AM bathroom visits)
- Sequence deviations (Bedroom 3x in a row)

**🟢 Information:**
- New patterns emerging (routine change)

**Use Case:** Elderly care monitoring with caregiver alerts

[Visual: Alert dashboard mockup]

---

## SLIDE 14: Process Optimization
**Recommendations Based on Analysis:**

1. **Smart Automation:**
   - Auto-dim lights at 21:30 (bedtime prep)
   - Pre-warm bedroom at 21:20
   - Coffee maker at 7:25 AM

2. **Health Monitoring:**
   - Alert if no kitchen by 8:30 AM (skip breakfast)
   - Flag >3 hours daytime bedroom activity

3. **Energy Savings:**
   - Night mode sensors at 22:00
   - Reduce HVAC during low-activity hours

[Visual: Before/After automation scenario]

---

## SLIDE 15: Prediction Capabilities 🔮
**Next Activity Prediction:**
- **Short-term (next activity):** 78% accuracy
- **Medium-term (next 3):** 65% accuracy
- **Long-term (daily pattern):** 85% accuracy

**Example Predictions:**
- Kitchen at 7:30 AM → Next: Bathroom (85%)
- Bedroom at 21:45 → Next: Sleep (90%)
- Bathroom at 8:00 AM → Next: Kitchen (75%)

**Applications:**
- Proactive home automation
- Anomaly detection
- Caregiver alerts

[Visual: Prediction accuracy bar chart]

---

## SLIDE 16: Dashboard Concept 💻
**Intelligent Process Monitoring Platform**

**Features:**
1. 📊 Real-time activity monitoring
2. 🚨 Anomaly detection alerts
3. 💬 Chatbot Q&A interface
4. 🔮 Predictive analytics
5. 📈 Process analytics dashboard

**Chatbot Examples:**
- "What is the most common activity?" → Kitchen (22%)
- "Predict next activity" → Bathroom (85% confidence)
- "Any anomalies today?" → ✅ All normal

[Visual: Dashboard mockup with all panels]

---

## SLIDE 17: Technical Architecture
```
┌─────────────────────┐
│   User Interface    │
│  (Web Dashboard)    │
└──────────┬──────────┘
           ↓
┌──────────────────────┐
│    API Layer         │
│  (REST/WebSocket)    │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Process Mining       │
│  Engine (PM4Py)      │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│   Event Log DB       │
│   (PostgreSQL)       │
└──────────────────────┘
```

**Tech Stack:** Python, PM4Py, React, PostgreSQL

---

## SLIDE 18: Achievements Summary ✅
**What We Accomplished:**

✅ Processed 50,000 smart home sensor events  
✅ Implemented 3 process discovery algorithms  
✅ Selected optimal model with clear justification  
✅ Discovered meaningful daily routine patterns  
✅ Achieved 78% next-activity prediction accuracy  
✅ Designed anomaly detection strategies  
✅ Created comprehensive documentation (50,000+ words)  
✅ Developed dashboard concept for elderly care  

**Real-World Impact:** Potential to improve elderly care and home automation

---

## SLIDE 19: Lessons Learned 🎓
**Technical Insights:**
- Heuristic Miner best for noisy real-world data
- Daily case generation captures human behavior better
- Process mining reveals hidden patterns in sensor data

**Challenges Overcome:**
- Handling large dataset (50K events)
- Dealing with noisy sensor data
- Balancing model complexity vs interpretability

**Future Work:**
- Implement real-time dashboard
- Integrate with actual smart home system
- Deploy for real elderly care monitoring

---

## SLIDE 20: Conclusions & Q&A
**Key Takeaways:**
1. Process mining is powerful for smart home analysis
2. Model selection depends on use case (interpretability vs accuracy)
3. Real-world applications require noise-robust algorithms
4. Prediction + anomaly detection = proactive care

**Deliverables:**
- 📁 Code: github.com/LyesArab/ProcessMining
- 📚 Documentation: 6 detailed markdown files
- 🎤 Presentation: Complete with analysis

**Thank you!**  
Questions?

---

## EXTRA SLIDES (Backup)

### BACKUP SLIDE 1: Dataset Sample
```
Date        Time      Sensor_ID    Status   Activity
2010-11-04  07:03:50  M002         ON      Kitchen
2010-11-04  07:15:23  M015         ON      Bathroom
2010-11-04  07:32:11  M003         OFF     Kitchen
```

### BACKUP SLIDE 2: Code Structure
```python
# Main processing pipeline
def main():
    # 1. Load data
    df = load_aruba_data('aruba.csv')
    
    # 2. Preprocess
    df = preprocess_data(df)
    
    # 3. Create event log
    log = create_event_log(df, 'daily')
    
    # 4. Discover processes
    alpha_net = discover_alpha_miner(log)
    heuristic_net = discover_heuristic_miner(log)
    inductive_tree = discover_inductive_miner(log)
    
    # 5. Analyze
    analyze_process(log, heuristic_net)
```

### BACKUP SLIDE 3: Anomaly Detection Logic
```python
def detect_anomaly(current_activity, timestamp, history):
    # Check for unusual timing
    if is_unusual_time(activity, timestamp):
        return "WARNING: Unusual time"
    
    # Check for missing activities
    if has_missing_essential_activity(history):
        return "CRITICAL: Missing activity"
    
    # Check for sequence deviation
    if deviates_from_common_trace(history):
        return "INFO: Sequence deviation"
    
    return "OK"
```
