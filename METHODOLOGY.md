# Process Mining Methodology for Smart Home Data

## Table of Contents
1. [Introduction](#introduction)
2. [From Sensor Data to Process Mining](#from-sensor-data-to-process-mining)
3. [Event Log Structure](#event-log-structure)
4. [Design Decisions Explained](#design-decisions-explained)
5. [Process Discovery Algorithms](#process-discovery-algorithms)
6. [Interpretation Guide](#interpretation-guide)
7. [Common Challenges](#common-challenges)

---

## Introduction

### What is Process Mining?

Process mining is a data science technique that:
- **Discovers** actual processes from event logs
- **Monitors** process performance and compliance
- **Improves** processes based on data-driven insights

### Why Apply Process Mining to Smart Homes?

Smart homes generate massive amounts of sensor data. Process mining helps us:
- **Understand behavior patterns**: How do inhabitants move through their home?
- **Detect anomalies**: Are there unusual activity patterns?
- **Optimize comfort**: When and where do activities typically occur?
- **Support healthcare**: Monitor elderly or patients for care support

---

## From Sensor Data to Process Mining

### The Transformation Pipeline

```
RAW SENSOR DATA → PREPROCESSED DATA → EVENT LOG → PROCESS MODEL
```

#### Stage 1: Raw Sensor Data
```
2010-11-04, 02:32:33.351906, Bedroom, ON
2010-11-04, 02:32:38.895958, Bedroom, OFF
2010-11-04, 03:42:21.823650, Kitchen, ON
```

**Characteristics**:
- High-frequency events (millions)
- Simple structure: timestamp + sensor + value
- No explicit case or activity labels
- Contains noise (sensor bounces, false triggers)

#### Stage 2: Preprocessed Data
```python
timestamp               sensor_id    sensor_value    activity
2010-11-04 02:32:33    Bedroom      ON              Bedroom_ON
2010-11-04 02:32:38    Bedroom      OFF             Bedroom_OFF
2010-11-04 03:42:21    Kitchen      ON              Kitchen_ON
```

**Transformations**:
- Combined date + time → single timestamp
- Created activity label (sensor_id + value)
- Removed rapid duplicates (< 1 second apart)
- Sorted chronologically

#### Stage 3: Event Log
```python
case_id       activity        timestamp
2010-11-04    Bedroom_ON      2010-11-04 02:32:33
2010-11-04    Bedroom_OFF     2010-11-04 02:32:38
2010-11-04    Kitchen_ON      2010-11-04 03:42:21
```

**Key Additions**:
- **case_id**: Groups events into process instances (daily cases)
- **activity**: Standardized activity labels
- **timestamp**: Precise event ordering

#### Stage 4: Process Model

Visualized as:
- **Petri nets**: Places (states) and transitions (activities)
- **Heuristics nets**: Activities with frequency/dependency info
- **Process trees**: Hierarchical control-flow structures

---

## Event Log Structure

### The Three Essential Columns

#### 1. Case ID (`case_id`)

**Definition**: Unique identifier for a process instance.

**For Smart Homes**:
- **Daily cases** (our choice): `YYYY-MM-DD`
  - Rationale: Human activities follow daily cycles
  - Example: All events on "2010-11-04" belong to one case
  
- **Session cases** (alternative): `YYYY-MM-DD_S1`, `YYYY-MM-DD_S2`
  - Rationale: Separate active periods (split by 2+ hour gaps)
  - Example: Morning activities vs. evening activities

**Why it matters**:
- Defines process boundaries
- Enables trace comparison
- Affects model complexity

#### 2. Activity (`activity`)

**Definition**: What happened in the process.

**For Smart Homes**:
- **Our choice**: `Sensor_ID + Sensor_Value`
  - Examples: `Bedroom_ON`, `Kitchen_OFF`, `Bathroom_ON`
  - Rationale: Captures both location and state change
  
- **Alternatives**:
  - Just location: `Bedroom`, `Kitchen`
  - Abstract activities: `EnterRoom`, `LeaveRoom`
  - Inferred activities: `CookingStart`, `SleepingStart`

**Why it matters**:
- Defines process vocabulary
- Determines model interpretability
- Affects process complexity

#### 3. Timestamp (`timestamp`)

**Definition**: When the event occurred.

**For Smart Homes**:
- Format: `YYYY-MM-DD HH:MM:SS.ffffff`
- Precision: Microseconds (sensor data is precise)
- Type: Python datetime object

**Why it matters**:
- Establishes event ordering
- Enables temporal analysis
- Critical for process discovery algorithms

---

## Design Decisions Explained

### Decision 1: Daily Cases vs. Session Cases

#### Daily Cases (Chosen Approach)
```
Case: 2010-11-04
Events: [Bedroom_ON, Kitchen_ON, Bathroom_ON, ..., Bedroom_OFF]
Duration: 00:00:00 to 23:59:59
```

**Advantages**:
✅ Natural human activity boundaries  
✅ Consistent case sizes  
✅ Easy to interpret (one day = one case)  
✅ Aligns with daily routines  

**Disadvantages**:
❌ May combine multiple activity episodes  
❌ Midnight transitions split artificially  

#### Session Cases (Alternative)
```
Case: 2010-11-04_S1 (Morning session)
Events: [Bedroom_ON, Kitchen_ON, Bathroom_ON, Kitchen_OFF]
Duration: 07:00 to 10:30

Case: 2010-11-04_S2 (Evening session)
Events: [Kitchen_ON, LivingRoom_ON, Bedroom_ON]
Duration: 18:00 to 23:00
```

**Advantages**:
✅ Natural activity boundaries (separated by sleep/absence)  
✅ More focused process instances  
✅ Better for within-day patterns  

**Disadvantages**:
❌ Inconsistent case sizes  
❌ Requires threshold tuning (gap duration)  
❌ May fragment related activities  

### Decision 2: Activity Definition

#### Our Choice: `Sensor_ID + Sensor_Value`

**Example**: `Bedroom_ON`, `Kitchen_OFF`

**Rationale**:
1. **Interpretability**: Clear what sensor fired and its state
2. **Traceability**: Direct mapping to raw sensor data
3. **Completeness**: Captures both activation and deactivation
4. **No assumptions**: Doesn't require inferring intent

**Trade-offs**:
- 📈 Increases number of activities (2x)
- 📊 Creates more complex models
- 🎯 Very precise but verbose

#### Alternative: Location Only

**Example**: `Bedroom`, `Kitchen`

**When to use**:
- Focus on movement patterns
- Simplify models
- State (ON/OFF) is less important

#### Alternative: Inferred Activities

**Example**: `Cooking`, `Sleeping`, `Hygiene`

**When to use**:
- Ground truth activity labels available
- High-level behavior analysis
- Comparing with expected routines

**Challenge**: Requires activity recognition (ML/rules)

### Decision 3: Noise Reduction

#### Our Approach: 1-Second Threshold

```python
# Before noise reduction
Bedroom_ON  at 10:00:00.100
Bedroom_ON  at 10:00:00.250  ← Duplicate (0.15s later)
Bedroom_ON  at 10:00:00.500  ← Duplicate (0.25s later)
Bedroom_OFF at 10:00:05.000  ← Keep (4.5s later)

# After noise reduction
Bedroom_ON  at 10:00:00.100  ← Keep (first event)
Bedroom_OFF at 10:00:05.000  ← Keep (>1s apart)
```

**Why 1 second?**
- Physical sensor limitation: Motion sensors can't reliably distinguish sub-second movements
- Noise reduction: Filters sensor "bouncing" and false triggers
- Information preservation: Real state changes take > 1 second

**Alternatives**:
- **No filtering** (0s): Keep all data, very noisy models
- **2-5 seconds**: More aggressive, risk losing quick transitions
- **Smart filtering**: Remove only same-sensor, same-value duplicates

---

## Process Discovery Algorithms

### Algorithm Comparison Table

| Algorithm | Output | Strengths | Weaknesses | Best For |
|-----------|--------|-----------|------------|----------|
| **Alpha Miner** | Petri Net | Theoretically sound, detects concurrency | Noise-sensitive, poor loop handling | Clean, structured logs |
| **Heuristic Miner** | Heuristics Net | Noise-robust, frequency information | May miss rare paths | Real-world, noisy logs |
| **Inductive Miner** | Process Tree + Petri Net | Guarantees soundness, handles incompleteness | Less precise | Guaranteed correctness needed |

### When to Use Each Algorithm

#### Alpha Miner
**Use when**:
- Log is clean and complete
- Need formal guarantees
- Teaching/learning process mining concepts

**For Smart Homes**:
- ⚠️ **Challenging**: Too sensitive to sensor noise
- Best with heavily filtered data

#### Heuristic Miner
**Use when**:
- Log is noisy (common in reality)
- Want to see main process flow
- Frequency matters (common vs. rare paths)

**For Smart Homes**:
- ✅ **Recommended**: Best balance for sensor data
- Handles noise well
- Shows typical daily patterns

#### Inductive Miner
**Use when**:
- Need guaranteed sound model (no deadlocks)
- Log may be incomplete
- Want hierarchical structure

**For Smart Homes**:
- ✅ **Recommended**: Reliable for any smart home data
- Always produces valid model
- Good starting point

---

## Interpretation Guide

### Reading Process Models

#### Petri Net Elements

```
[Place] → (Transition) → [Place]
  ○    →    Bedroom_ON  →    ○
```

- **Places (circles)**: States/conditions
- **Transitions (rectangles)**: Activities/events
- **Arcs (arrows)**: Flow direction
- **Tokens (dots in places)**: Current state

**Example Smart Home Pattern**:
```
[Start] → (Bedroom_ON) → [In Bedroom] → (Kitchen_ON) → [In Kitchen]
```
Interpretation: Person enters bedroom, then moves to kitchen

#### Heuristics Net Elements

```
Activity1 ──0.95──> Activity2
          ──0.05──> Activity3
```

- **Numbers on arcs**: Frequency/dependency strength
- **0.95 (95%)**: Strong relationship, happens often
- **0.05 (5%)**: Weak relationship, happens rarely

**Example**:
```
Bedroom_ON ──0.80──> Bathroom_ON
           ──0.20──> Kitchen_ON
```
Interpretation: 80% of the time after bedroom activation, bathroom is next

### Common Patterns in Smart Home Data

#### Pattern 1: Morning Routine
```
Bedroom_OFF → Bathroom_ON → Kitchen_ON → [Exit]
```
**Interpretation**: Wake up, hygiene, breakfast, leave

#### Pattern 2: Evening Routine
```
[Entry] → Kitchen_ON → LivingRoom_ON → Bedroom_ON → Bedroom_OFF
```
**Interpretation**: Come home, cook, relax, sleep

#### Pattern 3: Looping Behavior
```
Kitchen_ON ⟲ LivingRoom_ON ⟲ Kitchen_ON
```
**Interpretation**: Moving between rooms during meal preparation

#### Pattern 4: Parallel Activities
```
        ┌→ TV_ON ─┐
Entry ──┤         ├→ Exit
        └→ Light_ON ┘
```
**Interpretation**: Multiple sensors activated simultaneously

---

## Common Challenges

### Challenge 1: Process Complexity

**Problem**: Smart homes generate highly variable traces
- Example: Day 1 = 500 events, Day 2 = 50 events
- Hundreds of unique activity sequences

**Solutions**:
1. **Abstraction**: Group similar activities
   ```python
   'Bedroom_ON' + 'Bedroom_OFF' → 'BedroomActivity'
   ```

2. **Filtering**: Focus on important sensors
   ```python
   # Keep only room motion sensors, ignore cabinet sensors
   df = df[df['sensor_id'].isin(main_sensors)]
   ```

3. **Aggregation**: Use session-based cases to create shorter traces

### Challenge 2: Spaghetti Models

**Problem**: Too many unique paths create unreadable visualizations

**Solutions**:
1. **Use Heuristic Miner**: Automatically filters infrequent paths
2. **Increase noise threshold**: Remove more sensor duplicates
3. **Simplify activities**: Merge similar sensor events
4. **Filter variants**: Keep only top 80% most frequent traces

### Challenge 3: No Ground Truth

**Problem**: We don't know what activities actually occurred

**Partial Solutions**:
1. **Process mining**: Discover patterns empirically
2. **Domain knowledge**: Interpret sensor patterns
3. **Validation**: Compare with expected daily routines
4. **Activity recognition**: Apply ML if labeled data available (beyond scope)

### Challenge 4: Temporal Gaps

**Problem**: Large gaps between events (sleep, absence)

**Solutions**:
1. **Session cases**: Split at gaps > 2 hours
2. **Ignore gaps**: Keep daily cases, accept long durations
3. **Mark explicitly**: Add "Gap_Start" and "Gap_End" activities

### Challenge 5: Sensor Noise

**Problem**: False triggers, sensor malfunction, repeated firings

**Solutions**:
1. **Temporal filtering**: Remove events < 1s apart (implemented)
2. **Statistical outliers**: Remove sensors with abnormal frequency
3. **Domain rules**: E.g., "Person can't be in two rooms simultaneously"

---

## Best Practices Summary

### ✅ DO:
- Start with small samples (10K-50K events) for testing
- Document your case_id rationale clearly
- Experiment with different activity definitions
- Use Inductive Miner as baseline (always works)
- Visualize temporal patterns before process discovery
- Export event logs for reproducibility

### ❌ DON'T:
- Process full dataset (1.6M events) without testing first
- Use Alpha Miner on noisy data
- Ignore domain knowledge when interpreting models
- Expect perfect process models from sensor data
- Remove too much data during preprocessing

### 🎯 Success Criteria:
1. **Interpretable models**: Can you explain the discovered process?
2. **Reasonable complexity**: Not spaghetti, not trivial
3. **Valid patterns**: Match domain expectations (morning routines, sleep cycles)
4. **Reproducible**: Documented decisions and parameters

---

## Further Reading

### Process Mining Theory
- van der Aalst, W. M. P. (2016). *Process Mining: Data Science in Action*. Springer.
- [Process Mining: Overview and Opportunities](https://doi.org/10.1145/2436417.2436418)

### Smart Home Activity Recognition
- Cook, D. J., & Das, S. K. (2007). *How smart are our environments?*
- [CASAS Dataset Documentation](http://casas.wsu.edu/)

### pm4py Documentation
- [Official pm4py Docs](https://pm4py.fit.fraunhofer.de/)
- [pm4py Algorithm Reference](https://pm4py.fit.fraunhofer.de/documentation#discovery)

---

**Document Version**: 1.0  
**Last Updated**: January 2026  
**For**: CASAS Aruba Process Mining Assignment
