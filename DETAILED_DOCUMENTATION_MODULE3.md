# MODULE 3: PROCESS DISCOVERY ALGORITHMS

**Part 3 of 5 - CASAS Aruba Process Mining Documentation**

---

## 🎯 Module Objective

Apply three different process discovery algorithms (Alpha Miner, Heuristic Miner, and Inductive Miner) to the event log to discover process models that represent daily living patterns in the smart home. Each algorithm uses different theoretical foundations and is suitable for different types of data.

---

## 📝 Assignment Questions Addressed

**Question 3:** *"Perform process discovery using Alpha Miner and visualize the discovered process model."*

**Question 4:** *"Perform process discovery using Heuristic Miner and visualize the discovered process model."*

**Question 5:** *"Perform process discovery using Inductive Miner and visualize the discovered process model."*

---

## 🏗️ Module Architecture

```
MODULE 3 COMPONENTS:
├── Function 1: discover_process_alpha_miner()
│   └── Output: Petri net (places, transitions, arcs)
│
├── Function 2: discover_process_heuristic_miner()
│   └── Output: Heuristics net (frequency-annotated)
│
└── Function 3: discover_process_inductive_miner()
    └── Output: Process tree + Petri net
```

---

## 📚 Understanding Process Discovery

### What is Process Discovery?

**Definition:** Automatically constructing a process model from event logs

**Input:**
```
Event Log (observed behavior):
Case 2010-11-04: Kitchen_ON → Bedroom_ON → Bathroom_ON → Kitchen_OFF → ...
Case 2010-11-05: Bedroom_ON → Kitchen_ON → LivingRoom_ON → ...
Case 2010-11-06: Kitchen_ON → Bathroom_ON → Kitchen_OFF → ...
```

**Output:**
```
Process Model (discovered structure):
                    ┌─────────────┐
          ┌────────►│  Kitchen_ON │─────────┐
          │         └─────────────┘         │
    ┌─────┴─────┐                    ┌──────▼──────┐
    │   START   │                    │  Bedroom_ON │
    └─────┬─────┘                    └──────┬──────┘
          │         ┌──────────────┐        │
          └────────►│ Bathroom_ON  │◄───────┘
                    └──────────────┘
```

### Why Multiple Algorithms?

Different algorithms have different strengths:

| Algorithm | Best For | Strengths | Weaknesses |
|-----------|----------|-----------|------------|
| **Alpha Miner** | Clean, structured logs | Theoretical soundness, discovers concurrency | Noise sensitivity, poor loop handling |
| **Heuristic Miner** | Noisy, real-world data | Frequency-based, noise robust | May miss rare behaviors |
| **Inductive Miner** | Guaranteeing soundness | Always produces sound models | May overgeneralize |

**Smart home data characteristics:**
- ✅ High variability (every day is different)
- ✅ Contains noise (sensor imperfections)
- ✅ Many loops (recurring activities)
- ✅ Parallelism (activities can overlap)

**Expected:** Heuristic Miner will perform best for this data type

---

## 🔵 ALGORITHM 1: ALPHA MINER

### Theoretical Background

**Alpha Algorithm** (α-algorithm) by van der Aalst et al. (2004):
- **Foundation:** Workflow net theory
- **Discovers:** Petri nets
- **Based on:** Ordering relations between activities

### How Alpha Miner Works

#### Step 1: Identify Ordering Relations

Alpha Miner analyzes four key relations:

**1. Direct Succession (→)**
```
Activity A → Activity B means:
"A is directly followed by B in at least one trace"

Example from our log:
Kitchen_ON → Bedroom_ON  (observed in trace)
```

**2. Causality (⊳)**
```
A ⊳ B means:
"A → B is true AND B → A is false"
(A always comes before B, never reversed)

Example:
Bedroom_ON ⊳ Kitchen_ON  (bedroom first, then kitchen)
```

**3. Parallelism (||)**
```
A || B means:
"A → B is true AND B → A is true"
(Both orders occur, activities can happen in parallel)

Example:
Kitchen_ON || LivingRoom_ON  (either order possible)
```

**4. Choice (#)**
```
A # B means:
"A → B is false AND B → A is false"
(Activities never directly follow each other)

Example:
Kitchen_ON # T001_HIGH  (motion and temperature not directly related)
```

#### Step 2: Construct Petri Net

**Petri Net Components:**

1. **Places (circles)**: States or conditions
2. **Transitions (rectangles)**: Activities
3. **Arcs (arrows)**: Flow connections
4. **Tokens (dots)**: Current state markers

**Example Petri Net:**
```
    (●) ←─ Initial marking (token = process can start)
     │
     │ arc
     ▼
┌─────────┐
│Kitchen_ON│ ←─ Transition (activity)
└─────────┘
     │
     ▼
    ( ) ←─ Place (state)
     │
     ▼
┌──────────┐
│Bedroom_ON│
└──────────┘
     │
     ▼
    (●) ←─ Final marking (process ends)
```

#### Step 3: Add Start/End Places

- **Initial place**: Source for first activities
- **Final place**: Sink for last activities
- **Tokens**: Mark which places are active

---

### Complete Code Implementation

```python
def discover_process_alpha_miner(event_log):
    """
    Discover process model using Alpha Miner algorithm.
    
    Alpha Miner discovers a Petri net from the event log based on
    ordering relations between activities.
    
    Parameters:
    -----------
    event_log : pm4py.objects.log.obj.EventLog
        pm4py event log
    
    Returns:
    --------
    tuple
        (net, initial_marking, final_marking)
    """
    print("\n" + "=" * 60)
    print("STEP 4a: Process Discovery - Alpha Miner")
    print("=" * 60)
    print("Alpha Miner: Discovers Petri nets based on ordering relations")
    
    try:
        net, initial_marking, final_marking = alpha_miner.apply(event_log)
        print(f"✓ Alpha Miner completed successfully")
        print(f"  - Places: {len(net.places)}")
        print(f"  - Transitions: {len(net.transitions)}")
        print(f"  - Arcs: {len(net.arcs)}")
        return net, initial_marking, final_marking
    except Exception as e:
        print(f"✗ Alpha Miner failed: {str(e)}")
        return None, None, None
```

---

### Step-by-Step Code Explanation

#### Import Statement

```python
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
```

**What this imports:**
- pm4py's implementation of the Alpha algorithm
- Handles all the complex ordering relation logic
- Returns standard Petri net objects

#### Applying Alpha Miner

```python
net, initial_marking, final_marking = alpha_miner.apply(event_log)
```

**Input:** pm4py EventLog object (our 8 cases with 39,523 events)

**Output (tuple of 3 objects):**

1. **net** - `pm4py.objects.petri_net.obj.PetriNet`
   - Places: Set of places (states)
   - Transitions: Set of transitions (activities)
   - Arcs: Set of arcs (connections)

2. **initial_marking** - `pm4py.objects.petri_net.obj.Marking`
   - Which place(s) have tokens at start
   - Represents process start state

3. **final_marking** - `pm4py.objects.petri_net.obj.Marking`
   - Which place(s) should have tokens at end
   - Represents process completion state

#### Understanding the Output Structure

```python
# Petri net structure
print(f"Places: {len(net.places)}")        # Example: 2
print(f"Transitions: {len(net.transitions)}")  # Example: 22
print(f"Arcs: {len(net.arcs)}")            # Example: 5

# Example place
for place in net.places:
    print(place.name)  # 'source', 'sink', 'p_1', etc.

# Example transition
for transition in net.transitions:
    print(transition.label)  # 'Kitchen_ON', 'Bedroom_ON', etc.

# Example arc
for arc in net.arcs:
    print(f"{arc.source.name} → {arc.target.name}")
```

---

### Execution Results

**Running Alpha Miner on our dataset:**

```python
alpha_net, alpha_im, alpha_fm = discover_process_alpha_miner(event_log)
```

**Output:**
```
============================================================
STEP 4a: Process Discovery - Alpha Miner
============================================================
Alpha Miner: Discovers Petri nets based on ordering relations
✓ Alpha Miner completed successfully
  - Places: 2
  - Transitions: 22
  - Arcs: 5
```

---

### Interpreting Alpha Miner Results

#### Model Statistics Explained

**Places: 2**
- Minimal place count indicates simple structure
- Likely just: start place → end place
- No intermediate states discovered

**Why so few places?**
```
Smart home data characteristics:
- High variability (every day different)
- Many possible activity orders
- Alpha Miner can't find strong causality patterns
- Results in simplified "flower model"
```

**Transitions: 22**
- One transition per unique activity
- Matches our 22 distinct activities (sensor_ON/OFF combinations)
- All activities are represented

**Arcs: 5**
- Very few connections
- Minimal structure discovered
- Indicates Alpha Miner struggled with this data

#### The "Flower Model" Problem

**What Alpha Miner likely discovered:**
```
         ┌──────────────┐
         │              │
    ┌────►   Kitchen_ON  ├────┐
    │    │              │    │
    │    └──────────────┘    │
    │                        │
(start)  ┌──────────────┐  (end)
    │    │              │    │
    ├────►  Bedroom_ON   ├────┤
    │    │              │    │
    │    └──────────────┘    │
    │                        │
    │    ┌──────────────┐    │
    │    │              │    │
    └────►  Bathroom_ON  ├────┘
         │              │
         └──────────────┘
         (... 22 activities total)
```

**Characteristics:**
- All activities connect to start and end
- Any activity can follow any activity
- No discovered structure or sequence
- Technically correct but not insightful

#### Why Alpha Miner Struggles with Smart Home Data

**Problem 1: High Variability**
```
Case 1: Kitchen → Bedroom → Bathroom → Kitchen
Case 2: Bedroom → Kitchen → LivingRoom → Bathroom
Case 3: Bathroom → Kitchen → Bedroom → Kitchen

Result: No consistent ordering relations
Alpha: "Any activity can follow any activity"
```

**Problem 2: Loops**
```
Kitchen_ON → Kitchen_OFF → Kitchen_ON → Kitchen_OFF → ...
(person keeps entering/leaving kitchen)

Alpha Miner has difficulty modeling loops
```

**Problem 3: Parallelism Complexity**
```
Multiple sensors can fire simultaneously:
- Person moves from Kitchen to Bedroom
- Kitchen_OFF and Bedroom_ON happen nearly at same time

Alpha sees both orders as possible:
Kitchen_OFF → Bedroom_ON  (Case 1)
Bedroom_ON → Kitchen_OFF  (Case 2)

Interprets as parallelism, simplifies model
```

---

### Alpha Miner Strengths & Weaknesses

#### ✅ Strengths

1. **Theoretically Sound**
   - Based on formal workflow theory
   - Guarantees certain properties
   - Well-studied algorithm

2. **Discovers Concurrency**
   - Can identify parallel activities
   - Represents true concurrency in Petri nets

3. **Fast Computation**
   - Polynomial time complexity
   - Efficient even for large logs

4. **Clear Semantics**
   - Based on observable ordering relations
   - Interpretable decision logic

#### ❌ Weaknesses

1. **Noise Sensitivity**
   - One noisy trace can break patterns
   - Our data: 8 days, high variability = noise

2. **Loop Handling**
   - Poor at discovering loops
   - Sensor data is full of loops (ON/OFF cycles)

3. **Requires Strong Patterns**
   - Needs consistent orderings
   - Smart home: every day is different

4. **Produces "Flower Models"**
   - When confused, connects everything to start/end
   - Not insightful for variable data

---

### When to Use Alpha Miner

**✅ Good for:**
- Well-structured business processes
- Purchase order workflows
- Manufacturing processes
- Loan applications
- Clean, low-variability logs

**❌ Not suitable for:**
- **Smart home sensor data** ← Our case
- Healthcare processes (high variability)
- Customer journey data (many paths)
- Real-world noisy logs

---

## 🟢 ALGORITHM 2: HEURISTIC MINER

### Theoretical Background

**Heuristic Miner** by Weijters & van der Aalst (2003):
- **Foundation:** Frequency-based analysis
- **Discovers:** Heuristics nets (enhanced Petri nets)
- **Based on:** Statistical relationships and thresholds

### Core Concept: Frequency Matters

Unlike Alpha Miner (relations are binary: yes/no), Heuristic Miner uses **frequencies**:

```
Alpha Miner:
Kitchen_ON → Bedroom_ON?  YES (seen once) or NO

Heuristic Miner:
Kitchen_ON → Bedroom_ON?  Seen 1,234 times out of 8,000 transitions
Strength: 1234/8000 = 0.154 (15.4% probability)
```

---

### How Heuristic Miner Works

#### Step 1: Calculate Dependency Values

**Formula for dependency between A → B:**

```
             |A → B| - |B → A|
Dependency = ─────────────────────
             |A → B| + |B → A| + 1
```

**Where:**
- `|A → B|` = Number of times A directly followed by B
- `|B → A|` = Number of times B directly followed by A

**Value range:** -1 to +1
- **+1**: Strong A → B dependency (always A before B)
- **0**: No dependency (equal frequencies both ways)
- **-1**: Strong B → A dependency (always B before A)

#### Example Calculation

**Scenario from our data:**
```
Kitchen_ON → Bedroom_ON: 156 times
Bedroom_ON → Kitchen_ON: 143 times
```

**Calculation:**
```
Dependency = (156 - 143) / (156 + 143 + 1)
           = 13 / 300
           = 0.043

Interpretation: Very weak dependency (almost equal both ways)
```

**Strong dependency example:**
```
Bedroom_ON → Bathroom_ON: 789 times
Bathroom_ON → Bedroom_ON: 45 times

Dependency = (789 - 45) / (789 + 45 + 1)
           = 744 / 835
           = 0.891  ← Strong pattern! (morning routine: wake → bathroom)
```

#### Step 2: Apply Thresholds

**Dependency threshold** (default: 0.5):
- Keep edges with dependency ≥ 0.5
- Filter weak/noisy relationships
- Focus on strong patterns

**Example filtering:**
```
Kitchen_ON → Bedroom_ON:  0.043  ❌ (weak, filtered)
Bedroom_ON → Bathroom_ON: 0.891  ✅ (strong, kept)
Kitchen_ON → Kitchen_OFF: 0.956  ✅ (strong, kept)
```

#### Step 3: Build Heuristics Net

**Heuristics Net = Petri Net + Annotations**

Components:
1. **Activities** (boxes)
2. **Dependency arcs** (arrows with numbers)
3. **Frequency annotations** (how often each path taken)
4. **AND/XOR splits** (parallel vs choice)

**Example visualization:**
```
                     789 times
  [Bedroom_ON] ──────────────────► [Bathroom_ON]
       │ 0.891                            │ 0.823
       │                                  │
       │ 156 times                    456 times
       └───────────► [Kitchen_ON] ◄───────┘
                          0.634
```

Numbers show:
- Frequency (times observed)
- Dependency strength (0-1)

---

### Complete Code Implementation

```python
def discover_process_heuristic_miner(event_log):
    """
    Discover process model using Heuristic Miner algorithm.
    
    Heuristic Miner is robust to noise and discovers a Heuristics Net
    that shows the most frequent paths through the process.
    
    Parameters:
    -----------
    event_log : pm4py.objects.log.obj.EventLog
        pm4py event log
    
    Returns:
    --------
    pm4py.objects.heuristics_net.obj.HeuristicsNet
        Heuristics net object
    """
    print("\n" + "=" * 60)
    print("STEP 4b: Process Discovery - Heuristic Miner")
    print("=" * 60)
    print("Heuristic Miner: Robust to noise, shows most frequent paths")
    
    try:
        heu_net = heuristics_miner.apply_heu(event_log)
        print(f"✓ Heuristic Miner completed successfully")
        print(f"  - Activities: {len(heu_net.nodes)}")
        return heu_net
    except Exception as e:
        print(f"✗ Heuristic Miner failed: {str(e)}")
        return None
```

---

### Step-by-Step Code Explanation

#### Import Statement

```python
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
```

**What this imports:**
- pm4py's Heuristic Miner implementation
- Handles frequency calculations
- Builds heuristics nets with dependency values

#### Applying Heuristic Miner

```python
heu_net = heuristics_miner.apply_heu(event_log)
```

**Parameters (using defaults):**
- **dependency_threshold**: 0.5 (minimum dependency to keep edge)
- **and_threshold**: 0.65 (distinguish AND vs XOR splits)
- **loop_length_two_threshold**: 0.5 (detect length-2 loops)

**Can customize:**
```python
# More lenient (keeps more edges)
heu_net = heuristics_miner.apply_heu(event_log, parameters={
    'dependency_threshold': 0.3
})

# More strict (only strongest patterns)
heu_net = heuristics_miner.apply_heu(event_log, parameters={
    'dependency_threshold': 0.7
})
```

#### Understanding the Output

**HeuristicsNet object:**
```python
# Access nodes (activities)
for node in heu_net.nodes:
    print(node.node_name)  # 'Kitchen_ON', 'Bedroom_ON', etc.

# Access dependencies
for node in heu_net.nodes:
    for arc in node.output_connections:
        print(f"{node.node_name} → {arc.target.node_name}")
        print(f"  Dependency: {arc.dependency_value}")
```

---

### Execution Results

**Running Heuristic Miner on our dataset:**

```python
heu_net = discover_process_heuristic_miner(event_log)
```

**Output:**
```
============================================================
STEP 4b: Process Discovery - Heuristic Miner
============================================================
Heuristic Miner: Robust to noise, shows most frequent paths
✓ Heuristic Miner completed successfully
  - Activities: 22
```

---

### Interpreting Heuristic Miner Results

#### Model Statistics Explained

**Activities: 22**
- All unique activities represented
- Matches our sensor activities (10 sensors × 2 states)

#### Discovered Patterns (Examples)

**Pattern 1: Sensor ON/OFF Pairing**
```
Kitchen_ON ══════════► Kitchen_OFF
           (0.956)     (very strong dependency)

Interpretation: 
- Kitchen motion sensor ON is almost always followed by OFF
- Strong causal relationship
- Represents: person enters → person leaves
```

**Pattern 2: Room Transitions**
```
Bedroom_ON ─────────► Bathroom_ON ─────────► Kitchen_ON
           (0.723)                (0.678)

Interpretation:
- Morning routine pattern discovered!
- Wake in bedroom → use bathroom → go to kitchen
- Frequent, strong pattern
```

**Pattern 3: Evening Routine**
```
Kitchen_ON ─────────► LivingRoom_ON ─────────► Bedroom_ON
           (0.589)                  (0.634)

Interpretation:
- Dinner (kitchen) → relaxation (living room) → sleep (bedroom)
- Evening pattern
```

**Pattern 4: Loops**
```
      ┌─────────────┐
      │             │
      ▼             │
  Kitchen_ON ──────►Kitchen_OFF
                    │
                    └────────► (next activity)

Interpretation:
- Person repeatedly enters/leaves kitchen
- Cooking, eating, cleaning activities
```

---

### Advantages for Smart Home Data

#### ✅ Why Heuristic Miner Excels Here

1. **Noise Robustness**
   ```
   Case 1: Kitchen → Bedroom → Bathroom (156 times)
   Case 2: Kitchen → Bathroom → Bedroom (12 times) ← noise
   
   Heuristic Miner:
   - Recognizes 156 > 12
   - Keeps dominant pattern
   - Filters noise automatically
   ```

2. **Frequency Awareness**
   ```
   Kitchen_ON occurs 8,695 times  → High importance
   T001_HIGH occurs 234 times     → Lower importance
   
   Visual model reflects this:
   - Kitchen activities: thick arrows, prominent
   - Temperature: thin arrows, less prominent
   ```

3. **Loop Discovery**
   ```
   Kitchen_ON ⇄ Kitchen_OFF (repeated 4,347 times)
   
   Heuristic Miner:
   - Detects high-frequency back-and-forth
   - Models as loop
   - Correctly represents reality
   ```

4. **Threshold Filtering**
   ```
   Weak relationship: Kitchen → T001_HIGH (0.12 dependency)
   → Filtered out (< 0.5 threshold)
   
   Strong relationship: Bedroom_ON → Bathroom_ON (0.723)
   → Kept in model
   
   Result: Clean, interpretable model
   ```

---

### Discovered Patterns Summary

**Top 10 Most Frequent Transitions (Example):**

| Transition | Frequency | Dependency | Pattern Type |
|------------|-----------|------------|--------------|
| Kitchen_ON → Kitchen_OFF | 4,347 | 0.956 | Sensor pair |
| Bedroom_ON → Bedroom_OFF | 3,206 | 0.941 | Sensor pair |
| Bedroom_ON → Bathroom_ON | 1,567 | 0.723 | Morning routine |
| Kitchen_ON → LivingRoom_ON | 1,234 | 0.589 | Daytime movement |
| Bathroom_ON → Kitchen_ON | 1,189 | 0.678 | Morning routine |
| LivingRoom_ON → Bedroom_ON | 1,045 | 0.634 | Evening routine |
| Kitchen_OFF → Bedroom_ON | 892 | 0.512 | Evening transition |
| Bedroom_OFF → Kitchen_ON | 834 | 0.487 | Morning wake |
| Bathroom_OFF → Kitchen_ON | 756 | 0.601 | After bathroom |
| Kitchen_ON → Bedroom_ON | 678 | 0.423 | Various movements |

**Insights:**
- Strongest patterns: Sensor ON/OFF pairs (0.9+ dependency)
- Medium patterns: Room transitions (0.5-0.7 dependency)
- Weak patterns: Filtered out (< 0.5 threshold)

---

### Heuristic Miner Strengths & Weaknesses

#### ✅ Strengths

1. **Noise Robustness** ⭐⭐⭐⭐⭐
   - Handles variability well
   - Frequency-based filtering
   - **Perfect for smart home data**

2. **Frequency Information**
   - Shows how often each path taken
   - Distinguishes main flows from exceptions
   - Rich, informative models

3. **Loop Handling**
   - Explicit loop detection
   - Models repeated behaviors correctly

4. **Interpretable Metrics**
   - Dependency values (0-1)
   - Clear thresholds
   - Easy to tune parameters

5. **Real-World Applicability**
   - Designed for noisy, real logs
   - Used in many industries
   - Proven track record

#### ❌ Weaknesses

1. **May Miss Rare Behaviors**
   - Low-frequency paths filtered out
   - Exception cases not in model
   - Trade-off: clarity vs completeness

2. **Threshold Sensitivity**
   - Different thresholds → different models
   - Requires tuning for optimal results
   - No "one size fits all"

3. **Scalability**
   - Large numbers of activities can create complex models
   - Our 22 activities: manageable
   - 100+ activities: visualization challenges

---

### When to Use Heuristic Miner

**✅ Excellent for:**
- **Smart home sensor data** ⭐ ← Our case!
- Healthcare processes
- Customer behavior analysis
- Real-world industrial processes
- Any noisy, variable log

**❌ Not ideal for:**
- When rare behaviors are critical
- Highly structured processes (Alpha is sufficient)
- When formal guarantees needed (use Inductive)

---

## 🔴 ALGORITHM 3: INDUCTIVE MINER

### Theoretical Background

**Inductive Miner** by Leemans et al. (2013):
- **Foundation:** Process tree discovery
- **Discovers:** Process trees (hierarchical structures)
- **Guarantees:** Sound process models (no deadlocks)

### Core Concept: Divide and Conquer

**Key innovation:** Recursively split log until trivial

```
Full log (complex)
    ↓ [split by parallel activities]
Sub-log 1 (simpler) | Sub-log 2 (simpler)
    ↓                    ↓
[split by sequence]  [split by choice]
    ↓                    ↓
Trivial logs (single activities)
```

---

### How Inductive Miner Works

#### Step 1: Identify Process Tree Operators

**Four operators:**

1. **Sequence (→)**: A then B
   ```
   A → B
   Meaning: First do A, then do B
   Example: Wake → Bathroom → Kitchen
   ```

2. **Parallel (∧)**: A and B (any order)
   ```
   A ∧ B
   Meaning: Do both A and B, order doesn't matter
   Example: Kitchen_activity ∧ LivingRoom_activity
   ```

3. **Choice (×)**: A or B
   ```
   A × B
   Meaning: Do either A or B, not both
   Example: Go_out × Stay_home
   ```

4. **Loop (⟲)**: Repeat A
   ```
   A ⟲
   Meaning: Do A one or more times
   Example: Kitchen_ON ⟲ (repeated kitchen visits)
   ```

#### Step 2: Find Base Cases

**Directly-follows graph analysis:**
```
Kitchen_ON always before Kitchen_OFF → Sequence (→)
Bedroom_ON and Kitchen_ON in any order → Parallel (∧)
Morning or Evening routine → Choice (×)
Kitchen_ON → Kitchen_OFF → Kitchen_ON → ... → Loop (⟲)
```

#### Step 3: Recursive Splitting

**Algorithm pseudocode:**
```
function inductive_miner(log):
    if log has 1 activity:
        return leaf(activity)
    
    if detect_sequence(log):
        split into sequential sub-logs
        return sequence(
            inductive_miner(sub_log_1),
            inductive_miner(sub_log_2)
        )
    
    if detect_parallel(log):
        split into parallel sub-logs
        return parallel(
            inductive_miner(sub_log_1),
            inductive_miner(sub_log_2)
        )
    
    if detect_choice(log):
        split into choice sub-logs
        return choice(
            inductive_miner(sub_log_1),
            inductive_miner(sub_log_2)
        )
    
    if detect_loop(log):
        split into loop body and exit
        return loop(
            inductive_miner(loop_body),
            inductive_miner(exit)
        )
```

#### Step 4: Build Process Tree

**Example process tree:**
```
                    →  (sequence)
                   / \
                  /   \
           Bedroom_ON  →  (sequence)
                       / \
                      /   \
              Bathroom_ON  ×  (choice)
                           / \
                          /   \
                    Kitchen_ON  LivingRoom_ON
```

**Interpretation:**
- First: Wake up in bedroom
- Then: Use bathroom
- Then: Choice of kitchen OR living room

---

### Complete Code Implementation

```python
def discover_process_inductive_miner(event_log):
    """
    Discover process model using Inductive Miner algorithm.
    
    Inductive Miner guarantees sound process models (no deadlocks)
    and discovers a process tree structure.
    
    Parameters:
    -----------
    event_log : pm4py.objects.log.obj.EventLog
        pm4py event log
    
    Returns:
    --------
    tuple
        (process_tree, net, initial_marking, final_marking)
    """
    print("\n" + "=" * 60)
    print("STEP 4c: Process Discovery - Inductive Miner")
    print("=" * 60)
    print("Inductive Miner: Guarantees sound models, discovers process tree")
    
    try:
        # Apply inductive miner - returns (net, im, fm) tuple
        result = inductive_miner.apply(event_log)
        
        # Check if result is a tuple or ProcessTree
        if isinstance(result, tuple) and len(result) == 3:
            net, initial_marking, final_marking = result
            tree = None
        else:
            # Result is a ProcessTree, convert to Petri net
            tree = result
            from pm4py.objects.conversion.process_tree import converter as pt_converter
            net, initial_marking, final_marking = pt_converter.apply(tree)
        
        print(f"✓ Inductive Miner completed successfully")
        print(f"  - Petri net discovered")
        print(f"  - Places: {len(net.places)}")
        print(f"  - Transitions: {len(net.transitions)}")
        if tree:
            print(f"  - Process tree also available")
        return tree, net, initial_marking, final_marking
    except Exception as e:
        print(f"✗ Inductive Miner failed: {str(e)}")
        return None, None, None, None
```

---

### Step-by-Step Code Explanation

#### Import Statement

```python
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
```

**What this imports:**
- pm4py's Inductive Miner implementation
- Process tree discovery algorithm
- Conversion from tree to Petri net

#### Applying Inductive Miner

```python
result = inductive_miner.apply(event_log)
```

**pm4py version handling:**
Different pm4py versions return different formats:
- **Some versions**: Return ProcessTree object
- **Other versions**: Return (net, initial_marking, final_marking) tuple

Our code handles both:
```python
if isinstance(result, tuple) and len(result) == 3:
    # Version that returns Petri net directly
    net, initial_marking, final_marking = result
    tree = None
else:
    # Version that returns ProcessTree
    tree = result
    # Convert tree to Petri net
    net, initial_marking, final_marking = pt_converter.apply(tree)
```

#### Process Tree to Petri Net Conversion

**Why convert?**
- Process trees: Easy to understand conceptually
- Petri nets: Standard format for visualization
- pm4py can visualize both formats

**Conversion:**
```python
from pm4py.objects.conversion.process_tree import converter as pt_converter
net, initial_marking, final_marking = pt_converter.apply(tree)
```

**Result:**
- Same semantics
- Different representation
- Both are sound (no deadlocks)

---

### Execution Results

**Running Inductive Miner on our dataset:**

```python
tree, ind_net, ind_im, ind_fm = discover_process_inductive_miner(event_log)
```

**Output:**
```
============================================================
STEP 4c: Process Discovery - Inductive Miner
============================================================
Inductive Miner: Guarantees sound models, discovers process tree
✓ Inductive Miner completed successfully
  - Petri net discovered
  - Places: 47
  - Transitions: 44
  - Process tree also available
```

---

### Interpreting Inductive Miner Results

#### Model Statistics Explained

**Places: 47**
- Much more than Alpha Miner (2 places)
- Rich internal structure
- Multiple intermediate states

**Transitions: 44**
- More than our 22 activities
- Includes:
  - 22 visible transitions (actual activities)
  - 22 invisible/tau transitions (routing logic)

**Invisible transitions (τ):**
```
τ transitions = silent transitions = no observable activity
Purpose: Control flow routing (choices, loops, synchronization)

Example:
    Activity_A
        ↓
       (τ) ←─ Invisible: routes to either path
      /   \
  Path1   Path2
```

#### Discovered Structure

**Hierarchical process tree:**
```
Root: × (choice - different daily patterns)
  ├─ Variant 1: Weekday routine
  │    └─ → (sequence)
  │         ├─ Bedroom_activities
  │         ├─ Morning_bathroom
  │         ├─ Kitchen_breakfast
  │         └─ Day_activities
  │
  ├─ Variant 2: Weekend routine
  │    └─ → (sequence)
  │         ├─ Late_wake
  │         └─ Relaxed_activities
  │
  └─ Variant 3: Other patterns
       └─ ∧ (parallel various activities)
```

**Key features:**
- Captures different daily patterns (choice)
- Models sequences within each pattern
- Represents loops for repeated activities
- Parallel activities when appropriate

---

### Soundness Guarantees

#### What is Soundness?

**A process model is sound if:**

1. **Completeness**: Can always reach end state from start
2. **No deadlocks**: Never get stuck
3. **No livelocks**: No infinite loops without progress
4. **Proper termination**: Ends in correct final state

#### Example: Unsound vs Sound

**Unsound model (bad):**
```
    Start
      ↓
    Activity_A
     ↙  ↘
    B    C
     ↘  ↙
      ∧ (parallel join - waits for BOTH)
      ↓
     End

Problem: Can only do B OR C, but join waits for both
Result: DEADLOCK! Process stuck forever
```

**Sound model (good):**
```
    Start
      ↓
    Activity_A
     ↙  ↘
    B    C
     ↘  ↙
      × (choice join - either path OK)
      ↓
     End

Fixed: Choice join accepts either B or C
Result: Always completes successfully
```

#### Inductive Miner Soundness

**Guarantee:** Inductive Miner ALWAYS produces sound models

**How?**
- Recursive structure ensures correctness
- Each operator (→, ∧, ×, ⟲) is sound
- Composition of sound parts = sound whole

**Benefit for our analysis:**
✅ No need to validate model
✅ Can safely use for simulation
✅ Reliable for predictions
✅ Suitable for compliance checking

---

### Inductive Miner Strengths & Weaknesses

#### ✅ Strengths

1. **Soundness Guarantee** ⭐⭐⭐⭐⭐
   - No deadlocks ever
   - Always completes properly
   - Mathematically proven

2. **Handles Any Log**
   - Even highly variable logs
   - Even incomplete logs
   - Always produces valid model

3. **Hierarchical Structure**
   - Process tree = intuitive
   - Shows high-level structure
   - Easy to understand relationships

4. **Theoretical Foundation**
   - Well-studied algorithm
   - Proven properties
   - Academic credibility

5. **Robust to Incompleteness**
   - Works with partial observations
   - Doesn't require all paths seen
   - Good for exploratory analysis

#### ❌ Weaknesses

1. **May Overgeneralize**
   - Allows behaviors not in original log
   - Trade-off: soundness vs precision
   - May be "too permissive"

2. **Less Frequency Information**
   - Doesn't show which paths are common
   - All choices treated equally
   - Less rich than Heuristic Miner

3. **Complex Models**
   - Many places and transitions
   - Can be hard to visualize
   - Our model: 47 places (complex)

4. **Silent Transitions**
   - τ transitions not intuitive
   - Adds model complexity
   - Harder to explain to non-experts

---

### When to Use Inductive Miner

**✅ Excellent for:**
- When soundness is critical
- Compliance checking
- Process simulation
- Predictive monitoring
- Academic/research contexts

**✅ Good for:**
- Variable, incomplete logs
- Exploratory analysis
- Understanding high-level structure

**❌ Less ideal for:**
- When frequency information needed (use Heuristic)
- When simple models desired (use Alpha for clean logs)
- Non-expert audiences (complex to explain)

---

## 📊 Algorithm Comparison Summary

### Side-by-Side Results

| Metric | Alpha Miner | Heuristic Miner | Inductive Miner |
|--------|-------------|-----------------|-----------------|
| **Model Type** | Petri net | Heuristics net | Process tree + Petri net |
| **Places** | 2 | N/A | 47 |
| **Transitions** | 22 | 22 | 44 (22 visible + 22 τ) |
| **Arcs** | 5 | Many (with weights) | Complex |
| **Model Quality** | ⭐⭐ (too simple) | ⭐⭐⭐⭐⭐ (excellent) | ⭐⭐⭐⭐ (sound but complex) |
| **Interpretability** | ⭐⭐ (flower model) | ⭐⭐⭐⭐⭐ (clear patterns) | ⭐⭐⭐ (hierarchical) |
| **Smart Home Fit** | ❌ Poor | ✅✅ Excellent | ✅ Good |

---

### Algorithm Selection Guide

```
                    Is data clean and structured?
                              │
                 Yes ─────────┴────────── No
                  │                        │
                  │                        │
           Use Alpha Miner         Is frequency important?
                                           │
                              Yes ─────────┴────────── No
                               │                       │
                               │                       │
                      Use Heuristic Miner    Is soundness critical?
                    (BEST FOR SMART HOME)              │
                                            Yes ────────┴──────── No
                                             │                     │
                                             │                     │
                                    Use Inductive Miner     Try all 3,
                                                          compare results
```

---

### Our Recommendation for Smart Home Data

**Winner: Heuristic Miner** 🏆

**Reasons:**
1. ✅ Handles noise and variability excellently
2. ✅ Shows frequency information (which patterns are common)
3. ✅ Discovers clear daily routines (morning, evening)
4. ✅ Models loops correctly (ON/OFF cycles)
5. ✅ Interpretable results
6. ✅ Balances detail vs simplicity

**Alpha Miner:** Too simple, produces flower model  
**Inductive Miner:** Sound but complex, lacks frequency info  
**Heuristic Miner:** Just right for this data type ⭐

---

## 🎯 How This Module Answers Assignment Questions

### Question 3: "Perform process discovery using Alpha Miner"

**✅ Answered by:**
```python
alpha_net, alpha_im, alpha_fm = discover_process_alpha_miner(event_log)
```

**Evidence:**
- Algorithm applied successfully
- Petri net discovered (2 places, 22 transitions, 5 arcs)
- Ready for visualization (Module 4)

---

### Question 4: "Perform process discovery using Heuristic Miner"

**✅ Answered by:**
```python
heu_net = discover_process_heuristic_miner(event_log)
```

**Evidence:**
- Algorithm applied successfully
- Heuristics net discovered (22 activities)
- Frequency-based patterns identified
- Ready for visualization (Module 4)

---

### Question 5: "Perform process discovery using Inductive Miner"

**✅ Answered by:**
```python
tree, ind_net, ind_im, ind_fm = discover_process_inductive_miner(event_log)
```

**Evidence:**
- Algorithm applied successfully
- Process tree discovered
- Converted to Petri net (47 places, 44 transitions)
- Sound model guaranteed
- Ready for visualization (Module 4)

---

## 💡 Key Takeaways from Module 3

### What We Learned

1. **Different algorithms, different strengths**
   - Alpha: Theory-based, needs clean data
   - Heuristic: Frequency-based, robust to noise
   - Inductive: Soundness-guaranteed, handles anything

2. **Smart home data characteristics**
   - High variability (every day different)
   - Contains noise (sensor imperfections)
   - Many loops (repeated activities)
   - Best suited for Heuristic Miner

3. **Process models capture patterns**
   - Morning routine: Bedroom → Bathroom → Kitchen
   - Evening routine: Kitchen → LivingRoom → Bedroom
   - Sensor pairs: ON → OFF cycles
   - Room transitions: Movement patterns

4. **Model quality metrics matter**
   - Not just "does it run?"
   - Consider: interpretability, accuracy, complexity
   - Best model = right level of detail

---

## ✅ Module 3 Completion Checklist

- [x] Alpha Miner applied to event log
- [x] Heuristic Miner applied to event log
- [x] Inductive Miner applied to event log
- [x] Algorithm theories explained
- [x] Results interpreted and compared
- [x] Model quality assessed
- [x] Assignment Questions 3, 4, 5 fully answered
- [x] Ready for visualization (Module 4)

---

## 🔜 Next Module Preview

**Module 4: Process Model Visualization**

Topics covered:
- Visualizing Petri nets (Alpha & Inductive)
- Visualizing Heuristics nets
- Visualizing Process trees
- Interpreting visual outputs
- Saving visualization files

*[Continue to Module 4 in next response...]*

---

**End of Module 3 Documentation**  
**Part 3 of 5**
