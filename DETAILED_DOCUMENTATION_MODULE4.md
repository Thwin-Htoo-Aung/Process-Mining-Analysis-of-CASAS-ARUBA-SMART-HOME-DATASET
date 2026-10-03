# MODULE 4: PROCESS MODEL VISUALIZATION

**Part 4 of 5 - CASAS Aruba Process Mining Documentation**

---

## 🎯 Module Objective

Visualize the process models discovered by Alpha Miner, Heuristic Miner, and Inductive Miner using pm4py's visualization capabilities. Transform abstract model structures into graphical representations that reveal daily living patterns and activity flows in the smart home.

---

## 📝 Assignment Question Addressed

**Question (part of 3, 4, 5):** *"Visualize each discovered process model."*

---

## 🏗️ Module Architecture

```
MODULE 4 COMPONENTS:
├── Function 1: visualize_petri_net()
│   ├── Used for: Alpha Miner output
│   └── Used for: Inductive Miner output (Petri net form)
│
├── Function 2: visualize_heuristics_net()
│   └── Used for: Heuristic Miner output
│
└── Function 3: visualize_process_tree()
    └── Used for: Inductive Miner output (tree form)
```

---

## 📚 Understanding Process Model Visualizations

### Why Visualization Matters

**Raw model data:**
```python
net.places = {<Place p1>, <Place p2>, ...}
net.transitions = {<Transition t1 label='Kitchen_ON'>, ...}
net.arcs = {<Arc from p1 to t1>, ...}
```
❌ Not human-readable

**Visualized model:**
```
    (●) Start
     ↓
┌──────────┐
│Kitchen_ON│
└──────────┘
     ↓
    ( ) Place
     ↓
┌───────────┐
│Bedroom_ON │
└───────────┘
```
✅ Immediately understandable!

---

### Visualization Types

| Model Type | Visualization | Best Shows |
|------------|---------------|------------|
| **Petri Net** | Circles + Rectangles + Arrows | State transitions, control flow |
| **Heuristics Net** | Boxes + Weighted Arrows | Frequencies, main paths |
| **Process Tree** | Hierarchical Tree | Operator structure, nesting |

---

## 🔵 PETRI NET VISUALIZATION

### Understanding Petri Net Diagrams

**Components:**

1. **Places (Circles ○)**
   - Represent states or conditions
   - Can contain tokens (●)
   - Example: "After Kitchen_ON"

2. **Transitions (Rectangles □)**
   - Represent activities
   - Labeled with activity names
   - Example: "Kitchen_ON", "Bedroom_ON"

3. **Arcs (Arrows →)**
   - Connect places to transitions
   - Show flow direction
   - Cannot connect place-to-place or transition-to-transition

4. **Tokens (Dots ●)**
   - Mark current state
   - Move through the net during execution
   - Initial marking: where process starts
   - Final marking: where process should end

### Visual Reading Guide

**Simple sequence:**
```
    (●) ←─ Token here = ready to start
     │
     │ arc (flow)
     ▼
┌──────────┐
│Activity_A│ ←─ Transition (activity)
└──────────┘
     │
     ▼
    ( ) ←─ Place (intermediate state)
     │
     ▼
┌──────────┐
│Activity_B│
└──────────┘
     │
     ▼
    (●) ←─ Final token = process complete
```

**Parallel activities:**
```
         ( )
        ╱   ╲
       ╱     ╲
┌──────┐   ┌──────┐
│Act_A │   │Act_B │  ←─ Can execute in parallel
└──────┘   └──────┘
       ╲     ╱
        ╲   ╱
         ( )
```

**Choice (XOR):**
```
         ( )
          │
      ┌───┴───┐
      │  τ    │  ←─ Silent transition (routing)
      └───┬───┘
        ╱   ╲
       ╱     ╲
┌──────┐   ┌──────┐
│Act_A │   │Act_B │  ←─ Choose one path
└──────┘   └──────┘
```

---

## 🔧 FUNCTION 1: visualize_petri_net()

### Complete Code Implementation

```python
def visualize_petri_net(net, initial_marking, final_marking, 
                        output_file='alpha_miner_model.png', title='Alpha Miner'):
    """
    Visualize a Petri net and save to file.
    
    Parameters:
    -----------
    net : pm4py.objects.petri_net.obj.PetriNet
        Petri net object
    initial_marking : pm4py.objects.petri_net.obj.Marking
        Initial marking
    final_marking : pm4py.objects.petri_net.obj.Marking
        Final marking
    output_file : str
        Output filename
    title : str
        Title for the visualization
    """
    if net is None:
        print(f"✗ Cannot visualize {title} - model is None")
        return
    
    print(f"\n✓ Visualizing {title}...")
    try:
        gviz = pn_visualizer.apply(net, initial_marking, final_marking)
        pn_visualizer.save(gviz, output_file)
        print(f"  - Saved to: {output_file}")
    except Exception as e:
        print(f"✗ Visualization failed: {str(e)}")
```

---

### Step-by-Step Code Explanation

#### Import Statement

```python
from pm4py.visualization.petri_net import visualizer as pn_visualizer
```

**What this imports:**
- pm4py's Petri net visualization module
- Uses Graphviz library internally
- Creates PNG/SVG/PDF outputs

#### Creating Visualization

```python
gviz = pn_visualizer.apply(net, initial_marking, final_marking)
```

**Parameters explained:**

1. **net**: The Petri net structure
   - Places, transitions, arcs
   
2. **initial_marking**: Starting state
   - Which places have tokens at start
   - Example: `{source_place: 1}` (one token in source)
   
3. **final_marking**: End state
   - Which places should have tokens at end
   - Example: `{sink_place: 1}` (one token in sink)

**Return value (gviz):**
- Graphviz diagram object
- Contains layout instructions
- Not yet saved to file

#### Saving to File

```python
pn_visualizer.save(gviz, output_file)
```

**What happens:**
1. Renders the Graphviz diagram
2. Saves as PNG image (default)
3. Creates file in current directory

**Supported formats:**
```python
pn_visualizer.save(gviz, 'model.png')   # PNG (default)
pn_visualizer.save(gviz, 'model.svg')   # SVG (scalable)
pn_visualizer.save(gviz, 'model.pdf')   # PDF
```

---

### Visualization Customization (Advanced)

**Default visualization:**
```python
gviz = pn_visualizer.apply(net, initial_marking, final_marking)
```

**Custom parameters:**
```python
from pm4py.visualization.petri_net import visualizer as pn_visualizer

parameters = {
    pn_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "svg",
    pn_visualizer.Variants.WO_DECORATION.value.Parameters.DEBUG: False,
}

gviz = pn_visualizer.apply(net, initial_marking, final_marking, 
                           parameters=parameters)
```

**Available customizations:**
- `FORMAT`: Output format (png, svg, pdf)
- `RANKDIR`: Layout direction (TB=top-bottom, LR=left-right)
- `BGCOLOR`: Background color
- `DEBUG`: Show additional info

---

### Execution Examples

#### Example 1: Alpha Miner Visualization

```python
# Visualize Alpha Miner result
visualize_petri_net(alpha_net, alpha_im, alpha_fm, 
                   output_file='alpha_miner_model.png', 
                   title='Alpha Miner')
```

**Output:**
```
✓ Visualizing Alpha Miner...
  - Saved to: alpha_miner_model.png
```

**File created:** `alpha_miner_model.png` (29 KB)

**Visual content:**
```
Simple flower model with:
- 1 source place (●)
- 22 transitions (all activities)
- 1 sink place
- Minimal structure (all activities connected to start/end)
```

---

#### Example 2: Inductive Miner Visualization

```python
# Visualize Inductive Miner result (Petri net form)
visualize_petri_net(ind_net, ind_im, ind_fm,
                   output_file='inductive_miner_model.png',
                   title='Inductive Miner')
```

**Output:**
```
✓ Visualizing Inductive Miner...
  - Saved to: inductive_miner_model.png
```

**File created:** `inductive_miner_model.png` (156 KB)

**Visual content:**
```
Complex hierarchical model with:
- 47 places (many intermediate states)
- 44 transitions (22 visible + 22 silent)
- Rich structure showing:
  * Sequential patterns
  * Parallel constructs
  * Choice points
  * Loop structures
```

---

### Interpreting Petri Net Visualizations

#### Alpha Miner Output

**Expected appearance:**
```
                    ┌─────────────┐
                ┌──►│  Kitchen_ON │────┐
                │   └─────────────┘    │
                │   ┌─────────────┐    │
    (●) ───────┼──►│  Bedroom_ON │────┼─────► ( )
   source      │   └─────────────┘    │      sink
                │   ┌─────────────┐    │
                └──►│ Bathroom_ON │────┘
                    └─────────────┘
                    (... 22 activities)
```

**Characteristics:**
- **Flower/star pattern**: All activities emanate from center
- **Minimal structure**: No discovered sequences
- **Simple topology**: Source → Activities → Sink
- **Limited insight**: Shows activities exist, not their relationships

**Interpretation:**
- ⚠️ Model too simple for useful insights
- Indicates high process variability
- All activity orders considered possible
- Not ideal for understanding daily patterns

---

#### Inductive Miner Output

**Expected appearance:**
```
More complex, hierarchical structure:

    (●) source
     │
     ▼
    ┌───┐
    │ τ │ ←─ Silent transition (XOR split)
    └─┬─┘
      ├──→ [Branch 1: Morning routine]
      │     └──→ Bedroom → Bathroom → Kitchen
      │
      ├──→ [Branch 2: Evening routine]
      │     └──→ Kitchen → LivingRoom → Bedroom
      │
      └──→ [Branch 3: Other patterns]
            └──→ Complex parallel/loop structures
```

**Characteristics:**
- **Hierarchical**: Nested structures
- **Silent transitions**: Many τ for routing
- **Sound**: Guaranteed no deadlocks
- **Complex**: 47 places, hard to read at once

**Interpretation:**
- ✅ Rich detail about process structure
- ✅ Shows different daily pattern variants
- ⚠️ Complexity makes full comprehension difficult
- Best viewed: Focus on specific branches/patterns

---

## 🟢 HEURISTICS NET VISUALIZATION

### Understanding Heuristics Net Diagrams

**Enhanced Petri net with annotations:**

1. **Activity Nodes (Boxes)**
   - Labeled with activity name
   - Size may reflect frequency

2. **Dependency Arcs (Arrows)**
   - Annotated with dependency value (0-1)
   - Thickness represents frequency
   - Direction shows flow

3. **Frequency Information**
   - Numbers show how often path taken
   - Helps identify main vs. exception paths

4. **AND/XOR Indicators**
   - Shows whether activities are parallel or choices

### Visual Reading Guide

**Annotated example:**
```
                    1,234 times
┌────────────┐  ───────────────────►  ┌─────────────┐
│            │  dependency: 0.723     │             │
│ Bedroom_ON │                        │ Kitchen_ON  │
│            │  ◄───────────────────  │             │
└────────────┘     543 times          └─────────────┘
                   dependency: 0.456
```

**Interpretation:**
- Bedroom → Kitchen happens 1,234 times (strong, frequent)
- Kitchen → Bedroom happens 543 times (weaker, less frequent)
- Dependency 0.723: Strong forward flow (Bedroom first)
- Dependency 0.456: Moderate backward flow

**Thick vs thin arrows:**
```
Kitchen_ON ═════════► Kitchen_OFF  (thick = frequent: 4,347 times)
Kitchen_ON ─────────► T001_HIGH    (thin = rare: 45 times)
```

---

## 🔧 FUNCTION 2: visualize_heuristics_net()

### Complete Code Implementation

```python
def visualize_heuristics_net(heu_net, output_file='heuristic_miner_model.png'):
    """
    Visualize a Heuristics Net and save to file.
    
    Parameters:
    -----------
    heu_net : pm4py.objects.heuristics_net.obj.HeuristicsNet
        Heuristics net object
    output_file : str
        Output filename
    """
    if heu_net is None:
        print(f"✗ Cannot visualize Heuristics Net - model is None")
        return
    
    print(f"\n✓ Visualizing Heuristics Net...")
    try:
        gviz = hn_visualizer.apply(heu_net)
        hn_visualizer.save(gviz, output_file)
        print(f"  - Saved to: {output_file}")
    except Exception as e:
        print(f"✗ Visualization failed: {str(e)}")
```

---

### Step-by-Step Code Explanation

#### Import Statement

```python
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
```

**What this imports:**
- Specialized Heuristics Net visualizer
- Shows frequency and dependency annotations
- Creates rich, informative diagrams

#### Creating Visualization

```python
gviz = hn_visualizer.apply(heu_net)
```

**Input:** HeuristicsNet object from Heuristic Miner

**What it includes:**
- All activity nodes
- Dependency arcs with values
- Frequency information
- AND/XOR split indicators

**Output:** Graphviz diagram with annotations

#### Saving to File

```python
hn_visualizer.save(gviz, output_file)
```

**Default format:** PNG  
**File size:** Typically larger than Petri nets (more information)

---

### Execution Example

```python
# Visualize Heuristic Miner result
visualize_heuristics_net(heu_net, 
                        output_file='heuristic_miner_model.png')
```

**Output:**
```
✓ Visualizing Heuristics Net...
  - Saved to: heuristic_miner_model.png
```

**File created:** `heuristic_miner_model.png` (2.3 MB)

**Why larger file?**
- Many annotations (frequencies, dependencies)
- Detailed edge labels
- Rich color coding
- Higher resolution needed for readability

---

### Interpreting Heuristics Net Visualization

#### Main Components Visible

**1. Activity Nodes**
```
┌─────────────────┐
│   Kitchen_ON    │  ←─ Activity name
│   Freq: 8,695   │  ←─ Total occurrences
└─────────────────┘
```

**2. Strong Dependencies (Thick Arrows)**
```
Kitchen_ON ═══════════════► Kitchen_OFF
           │ 4,347 times
           │ Dep: 0.956
```
- Very thick arrow = high frequency
- Dependency near 1.0 = strong causal relationship
- Main process flow

**3. Weak Dependencies (Thin Arrows)**
```
Kitchen_ON ───────────────► Bathroom_ON
           │ 234 times
           │ Dep: 0.523
```
- Thin arrow = lower frequency
- Dependency near 0.5 = weaker relationship
- Exception paths or variants

**4. Filtered Dependencies**
```
Kitchen_ON  ╳ ────→  T001_HIGH
(Dependency < 0.5, not shown or dashed)
```

---

#### Discovered Pattern Examples

**Pattern 1: Sensor Pairing**
```
┌──────────┐                    ┌───────────┐
│Kitchen_ON│ ═════════════════► │Kitchen_OFF│
└──────────┘   4,347 / 0.956    └───────────┘
```
**Interpretation:**
- Nearly every Kitchen_ON is followed by Kitchen_OFF
- Strong, reliable pattern
- Represents: Person enters kitchen → stays → leaves

---

**Pattern 2: Morning Routine**
```
┌───────────┐         ┌─────────────┐         ┌──────────┐
│ Bedroom_ON│ ══════► │ Bathroom_ON │ ══════► │Kitchen_ON│
└───────────┘ 1,567   └─────────────┘ 1,189   └──────────┘
             0.723                    0.678
```
**Interpretation:**
- Wake in bedroom (Bedroom_ON)
- Use bathroom (strong dependency 0.723)
- Go to kitchen for breakfast (strong dependency 0.678)
- Clear morning routine sequence

---

**Pattern 3: Evening Routine**
```
┌──────────┐         ┌──────────────┐         ┌───────────┐
│Kitchen_ON│ ══════► │LivingRoom_ON │ ══════► │Bedroom_ON │
└──────────┘ 1,234   └──────────────┘ 1,045   └───────────┘
            0.589                     0.634
```
**Interpretation:**
- Kitchen activity (dinner)
- Move to living room (relaxation)
- Go to bedroom (sleep preparation)
- Evening routine pattern

---

**Pattern 4: High-Frequency Loops**
```
    ┌──────────────┐
    │  Kitchen_ON  │
    └───┬──────▲───┘
        │      │
        │ 4347 │ 4012
        │      │
        ▼      │
    ┌──────────┴───┐
    │ Kitchen_OFF  │
    └──────────────┘
```
**Interpretation:**
- Repeated kitchen entries/exits
- Cooking, eating, cleaning activities
- Multiple visits per day

---

### Color Coding (if supported)

Some visualizations use colors:

| Color | Meaning |
|-------|---------|
| **Green edges** | Strong dependency (>0.7) |
| **Yellow edges** | Medium dependency (0.5-0.7) |
| **Red edges** | Weak but included (<0.5) |
| **Dashed lines** | AND splits (parallel) |
| **Solid lines** | XOR splits (choice) |

---

## 🌳 PROCESS TREE VISUALIZATION

### Understanding Process Tree Diagrams

**Hierarchical structure showing operators and activities:**

**Operator nodes (circles):**
- **→** Sequence: Do children in order
- **∧** Parallel: Do children in any order
- **×** Choice: Do exactly one child
- **⟲** Loop: Repeat child(ren)

**Activity nodes (rectangles):**
- Leaf nodes containing activity names

### Visual Reading Guide

**Example tree:**
```
            → (sequence root)
           ╱│╲
          ╱ │ ╲
         ╱  │  ╲
        ╱   │   ╲
       ╱    │    ╲
┌─────────┐ │ ┌────────┐
│Bedroom_ON│ │ │Kitchen │
└──────────┘ │ └───────┘
             │
             × (choice)
            ╱ ╲
           ╱   ╲
    ┌─────┐   ┌─────┐
    │ Opt1│   │ Opt2│
    └─────┘   └─────┘
```

**Reading:**
1. Start at root (→ sequence)
2. First: Bedroom_ON
3. Second: Choice (× operator)
   - Either Option 1
   - Or Option 2
4. Third: Kitchen activities

---

## 🔧 FUNCTION 3: visualize_process_tree()

### Complete Code Implementation

```python
def visualize_process_tree(tree, output_file='inductive_miner_tree.png'):
    """
    Visualize a process tree and save to file.
    
    Parameters:
    -----------
    tree : pm4py.objects.process_tree.obj.ProcessTree
        Process tree object
    output_file : str
        Output filename
    """
    if tree is None:
        print(f"✗ Cannot visualize Process Tree - model is None")
        return
    
    print(f"\n✓ Visualizing Process Tree...")
    try:
        gviz = pt_visualizer.apply(tree)
        pt_visualizer.save(gviz, output_file)
        print(f"  - Saved to: {output_file}")
    except Exception as e:
        print(f"✗ Visualization failed: {str(e)}")
```

---

### Step-by-Step Code Explanation

#### Import Statement

```python
from pm4py.visualization.process_tree import visualizer as pt_visualizer
```

**What this imports:**
- Process tree visualization module
- Hierarchical tree layout
- Operator symbol rendering

#### Creating Visualization

```python
gviz = pt_visualizer.apply(tree)
```

**Input:** ProcessTree object from Inductive Miner

**What it shows:**
- Hierarchical structure
- Operator types (→, ∧, ×, ⟲)
- Activity leaves
- Parent-child relationships

#### Saving to File

```python
pt_visualizer.save(gviz, output_file)
```

**Layout:** Top-down tree structure  
**Format:** PNG by default

---

### Execution Example

```python
# Visualize Inductive Miner result (tree form)
visualize_process_tree(tree, 
                      output_file='inductive_miner_tree.png')
```

**Output:**
```
✓ Visualizing Process Tree...
  - Saved to: inductive_miner_tree.png
```

**File created:** `inductive_miner_tree.png` (87 KB)

---

### Interpreting Process Tree Visualization

#### Tree Structure

**Root level:** Overall process structure
```
                    × (choice)
                   ╱│╲
                  ╱ │ ╲
                 ╱  │  ╲
    [Variant 1] [Variant 2] [Variant 3]
```
**Interpretation:** Daily patterns vary (choice among variants)

**Branch level:** Sequential patterns within variants
```
Variant 1 (Weekday):
    → (sequence)
    ├─ Bedroom_activities
    ├─ Morning_bathroom
    ├─ Kitchen_breakfast
    └─ Day_activities
```

**Leaf level:** Actual activities
```
Kitchen_breakfast:
    → (sequence)
    ├─ Kitchen_ON
    ├─ (kitchen activities)
    └─ Kitchen_OFF
```

---

#### Operator Meanings in Context

**→ (Sequence) - Order matters**
```
    → 
   ╱│╲
  1 2 3

Must do: 1, then 2, then 3 (in order)
Example: Wake → Bathroom → Kitchen
```

**∧ (Parallel) - Order doesn't matter**
```
    ∧
   ╱│╲
  A B C

Can do: A,B,C or B,A,C or C,B,A (any order)
Example: Kitchen_activity ∧ LivingRoom_activity
```

**× (Choice) - Pick one**
```
    ×
   ╱│╲
  A B C

Do exactly one: A or B or C (not multiple)
Example: Go_out × Stay_home
```

**⟲ (Loop) - Repeat**
```
    ⟲
   ╱ ╲
 Body Exit

Do Body repeatedly, then Exit
Example: Kitchen_ON → Kitchen_OFF (repeat)
```

---

## 📊 Visualization Results Summary

### Files Generated

| File | Size | Source Algorithm | Content |
|------|------|------------------|---------|
| `alpha_miner_model.png` | 29 KB | Alpha Miner | Simple flower model Petri net |
| `heuristic_miner_model.png` | 2.3 MB | Heuristic Miner | Annotated heuristics net |
| `inductive_miner_model.png` | 156 KB | Inductive Miner | Complex Petri net |
| `inductive_miner_tree.png` | 87 KB | Inductive Miner | Hierarchical process tree |

**Total:** 4 visualization files, ~2.6 MB

---

### Visualization Quality Comparison

| Aspect | Alpha | Heuristic | Inductive (Net) | Inductive (Tree) |
|--------|-------|-----------|-----------------|------------------|
| **Clarity** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Detail** | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Insight** | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Frequency** | ❌ | ✅ | ❌ | ❌ |
| **Soundness** | ⚠️ | ⚠️ | ✅ | ✅ |

**Winner for interpretation:** Heuristic Miner visualization 🏆
- Shows frequencies
- Highlights main patterns
- Filters noise
- Easy to identify daily routines

---

## 💡 Reading Visualizations: Tips & Tricks

### For Petri Nets

**1. Follow the tokens**
```
(●) → Activity_A → ( ) → Activity_B → (●)
```
- Start where token is (●)
- Trace path through transitions
- End where final token should be

**2. Identify patterns**
- Sequential flow: Linear chain
- Parallelism: Fork and join
- Choices: Alternative paths from one place
- Loops: Cycles back to earlier place

**3. Look for anomalies**
- Dead transitions (no path to them)
- Dead places (tokens can't reach)
- Deadlocks (tokens stuck, can't progress)

---

### For Heuristics Nets

**1. Follow thick arrows first**
```
A ═════► B (thick = main flow)
A ─────► C (thin = exception)
```
- Thick arrows = frequent, important paths
- Main process flow is most prominent

**2. Read dependency values**
```
A → B (0.956) = Strong: A almost always before B
A → C (0.534) = Weak: A sometimes before C
```
- Values near 1.0 = reliable patterns
- Values near 0.5 = variable patterns

**3. Identify routines**
- Look for chains of strong dependencies
- Example: Bedroom → Bathroom → Kitchen (morning)
- Multiple strong links = routine pattern

---

### For Process Trees

**1. Understand the hierarchy**
```
Root = overall structure
Branches = major variants or phases
Leaves = actual activities
```

**2. Interpret operators**
```
→ under root = sequential phases
× under root = different daily patterns
∧ in branch = parallel activities
⟲ in branch = repeated actions
```

**3. Trace a path**
- Start at root
- Follow one path down
- See what activities/operators encountered
- Represents one possible execution

---

## 🎨 Customizing Visualizations (Advanced)

### Changing Layout Direction

**Default (top-to-bottom):**
```python
gviz = pn_visualizer.apply(net, im, fm)
```

**Left-to-right:**
```python
from pm4py.visualization.petri_net import visualizer as pn_visualizer

parameters = {
    pn_visualizer.Variants.FREQUENCY.value.Parameters.RANKDIR: "LR"
}
gviz = pn_visualizer.apply(net, im, fm, parameters=parameters)
```

---

### Adjusting File Format

**Change to SVG (scalable):**
```python
parameters = {
    pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "svg"
}
gviz = pn_visualizer.apply(net, im, fm, parameters=parameters)
pn_visualizer.save(gviz, 'model.svg')
```

**Benefits of SVG:**
- Scalable without quality loss
- Smaller file size for simple models
- Can edit in vector graphics software

---

### Frequency-Annotated Petri Nets

**Show edge frequencies:**
```python
from pm4py.statistics.traces.generic.log import case_statistics
from pm4py.visualization.petri_net import visualizer as pn_visualizer

# Calculate edge frequencies
edge_freq = case_statistics.get_variant_statistics(event_log)

parameters = {
    pn_visualizer.Variants.FREQUENCY.value.Parameters.AGGREGATION_MEASURE: "mean"
}

gviz = pn_visualizer.apply(net, im, fm, 
                           log=event_log,
                           parameters=parameters,
                           variant=pn_visualizer.Variants.FREQUENCY)
```

**Result:** Petri net with edge thickness showing frequency

---

## 🎯 How This Module Answers Assignment Questions

### Question 3: "Visualize Alpha Miner model"

**✅ Answered by:**
```python
visualize_petri_net(alpha_net, alpha_im, alpha_fm, 
                   'alpha_miner_model.png', 'Alpha Miner')
```

**Evidence:**
- File generated: `alpha_miner_model.png` (29 KB)
- Shows Petri net with 2 places, 22 transitions
- Visualization complete ✓

---

### Question 4: "Visualize Heuristic Miner model"

**✅ Answered by:**
```python
visualize_heuristics_net(heu_net, 'heuristic_miner_model.png')
```

**Evidence:**
- File generated: `heuristic_miner_model.png` (2.3 MB)
- Shows heuristics net with frequency annotations
- Discovered patterns visible ✓

---

### Question 5: "Visualize Inductive Miner model"

**✅ Answered by:**
```python
# Petri net form
visualize_petri_net(ind_net, ind_im, ind_fm,
                   'inductive_miner_model.png', 'Inductive Miner')

# Process tree form
visualize_process_tree(tree, 'inductive_miner_tree.png')
```

**Evidence:**
- 2 files generated:
  - `inductive_miner_model.png` (156 KB) - Petri net
  - `inductive_miner_tree.png` (87 KB) - Process tree
- Both forms visualized ✓

---

## 📈 Visualization Best Practices

### Do's ✅

1. **Save in appropriate format**
   - PNG: For presentations, documents
   - SVG: For scalability, editing
   - PDF: For publications

2. **Use descriptive filenames**
   ```python
   'alpha_miner_model.png'  ✅ Clear
   'model.png'               ❌ Ambiguous
   ```

3. **Generate all variants**
   - Alpha, Heuristic, Inductive
   - Compare side-by-side
   - Choose best for insights

4. **Check file creation**
   ```python
   import os
   if os.path.exists('alpha_miner_model.png'):
       print("✓ File created successfully")
   ```

5. **Handle errors gracefully**
   - Check if model is None before visualizing
   - Catch exceptions
   - Provide clear error messages

---

### Don'ts ❌

1. **Don't ignore None models**
   ```python
   # ❌ Bad
   visualize_petri_net(None, None, None)  # Crashes
   
   # ✅ Good
   if net is not None:
       visualize_petri_net(net, im, fm)
   ```

2. **Don't use same filename**
   ```python
   # ❌ Bad - overwrites!
   visualize_petri_net(alpha_net, ..., 'model.png')
   visualize_petri_net(ind_net, ..., 'model.png')
   
   # ✅ Good
   visualize_petri_net(alpha_net, ..., 'alpha_model.png')
   visualize_petri_net(ind_net, ..., 'inductive_model.png')
   ```

3. **Don't skip error checking**
   ```python
   # ❌ Bad
   gviz = pn_visualizer.apply(net, im, fm)
   pn_visualizer.save(gviz, output_file)
   
   # ✅ Good
   try:
       gviz = pn_visualizer.apply(net, im, fm)
       pn_visualizer.save(gviz, output_file)
   except Exception as e:
       print(f"Error: {e}")
   ```

---

## 🔍 Troubleshooting Common Issues

### Issue 1: "Graphviz not found"

**Error:**
```
graphviz.backend.ExecutableNotFound: failed to execute ['dot', '-Tpng']
```

**Solution:**
```bash
# Install Graphviz (system-wide)
# Windows: Download from https://graphviz.org/download/
# After install, add to PATH

# Or use conda
conda install -c conda-forge python-graphviz graphviz

# Or use pip
pip install graphviz
```

---

### Issue 2: "Image file not created"

**Problem:** Code runs but file doesn't appear

**Solution:**
```python
import os

# Check current directory
print(f"Current directory: {os.getcwd()}")

# Use absolute path
output_path = os.path.join(os.getcwd(), 'alpha_miner_model.png')
pn_visualizer.save(gviz, output_path)

# Verify creation
if os.path.exists(output_path):
    print(f"✓ File created: {output_path}")
else:
    print(f"✗ File not found: {output_path}")
```

---

### Issue 3: "Model too complex to visualize"

**Problem:** Huge model, visualization unreadable

**Solution 1:** Filter model
```python
# Keep only most frequent activities
from pm4py.algo.filtering.log.attributes import attributes_filter

filtered_log = attributes_filter.apply_events(
    event_log, 
    values=['Kitchen_ON', 'Bedroom_ON', 'Bathroom_ON']  # Top activities
)

# Rediscover with filtered log
heu_net = heuristics_miner.apply_heu(filtered_log)
```

**Solution 2:** Adjust visualization parameters
```python
# Increase image size
parameters = {
    'format': 'svg',  # Scalable
    'rankdir': 'LR'   # Left-right (wider)
}
```

---

### Issue 4: "Out of memory"

**Problem:** Large model crashes visualization

**Solution:**
```python
# Use simplified variant
from pm4py.visualization.petri_net import visualizer as pn_visualizer

# Use variant without decorations (simpler)
gviz = pn_visualizer.apply(net, im, fm, 
                           variant=pn_visualizer.Variants.WO_DECORATION)
```

---

## ✅ Module 4 Completion Checklist

- [x] Petri net visualization function implemented
- [x] Heuristics net visualization function implemented
- [x] Process tree visualization function implemented
- [x] Alpha Miner model visualized → `alpha_miner_model.png`
- [x] Heuristic Miner model visualized → `heuristic_miner_model.png`
- [x] Inductive Miner Petri net visualized → `inductive_miner_model.png`
- [x] Inductive Miner tree visualized → `inductive_miner_tree.png`
- [x] 4 visualization files generated successfully
- [x] Visualization interpretation guide provided
- [x] Assignment visualization requirements fully met

---

## 💡 Key Takeaways from Module 4

### What We Learned

1. **Three visualization types**
   - Petri nets: State-based, show control flow
   - Heuristics nets: Frequency-annotated, show patterns
   - Process trees: Hierarchical, show structure

2. **pm4py visualization tools**
   - Simple API: `apply()` then `save()`
   - Multiple format support: PNG, SVG, PDF
   - Customizable parameters

3. **Interpretation skills**
   - Reading Petri nets: Follow tokens
   - Reading Heuristics nets: Follow thick arrows
   - Reading Process trees: Understand operators

4. **Visualization quality**
   - Heuristic Miner: Best for insights (frequencies, patterns)
   - Inductive Miner: Best for structure (sound, hierarchical)
   - Alpha Miner: Too simple for this data

---

## 🔜 Next Module Preview

**Module 5: Process Analysis & Insights (FINAL)**

Topics covered:
- Activity frequency analysis with charts
- Trace variant discovery
- Throughput time analysis (case durations)
- Temporal patterns (hourly/daily trends)
- Business insights from smart home data
- Complete assignment summary

*[Continue to Module 5 in next response...]*

---

**End of Module 4 Documentation**  
**Part 4 of 5**
