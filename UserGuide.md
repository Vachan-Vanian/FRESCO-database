# FRESCO Database User Guide

## Table of Contents
1. [Introduction](#1-introduction)
2. [Installation and Setup](#2-installation-and-setup)
3. [Quick Start Guide](#3-quick-start-guide)
4. [Understanding the Database Structure](#4-understanding-the-database-structure)
5. [Working with the Database](#5-working-with-the-database)
6. [Unit System and Conversions](#6-unit-system-and-conversions)
7. [Reinforcement Notation](#7-reinforcement-notation)
8. [Data Entry Best Practices](#8-data-entry-best-practices)
9. [Exporting Data](#9-exporting-data)
10. [3D Model Generation](#10-3d-model-generation)
11. [Common Issues and Troubleshooting](#11-common-issues-and-troubleshooting)
12. [Advanced Usage](#12-advanced-usage)
13. [Complete Examples](#13-complete-examples)

---

## 1. Introduction

### 1.1 What is FRESCO?

FRESCO (Fiber REinforced Strengthening COmposite Database) is a comprehensive open-source database designed to systematically organize experimental data on infilled RC frame systems, with integrated modeling capabilities for simulating advanced composite strengthening interventions such as Fiber Reinforced Polymers (FRP), Textile Reinforced Mortars (TRM), and other fiber-based solutions. The database employs open-source practices while providing high-quality output that is fully compatible with leading commercial software packages such as ANSYS.

### 1.2 Key Features

- **Automatic Unit Conversion**: Enter data in any unit system, automatically converts to database defaults
- **Reinforcement Parsing**: Smart parsing of reinforcement notation (e.g., "4#20+2#16", "#10@150")
- **Data Validation**: Automatic validation of data types and unit compatibility
- **3D Model Generation**: Automated generation of FreeCAD models from database entries
- **Multiple Export Formats**: Export to CSV, JSON, or compressed JSON
- **Version Control Ready**: All data stored in human-readable JSON format

### 1.3 System Requirements

- Python 3.8 or higher
- FreeCAD v1.0 (for 3D model generation)
- Required Python packages: `json`, `gzip`, `csv`, `copy`, `datetime`, `re`

---

## 2. Installation and Setup

### 2.1 Repository main Structure

```
FRESCO-database/
├── src/                            # Source code
├── Database/                       # Database storage location
├── Models/                         # Generated 3D models
├── Examples/                       # Example and template entries
├── UserGuide.md                    # This file
├── README.md
├── LICENSE
├── CONTRIBUTING.md
...
```

### 2.2 Initial Setup

**1. Install Visual Studio Code**
- Download from: https://code.visualstudio.com/
- Install VS Code on your system

**2. Install FreeCAD**
- Download FreeCAD v1.0 or higher from: https://www.freecad.org/
- Install FreeCAD on your system

**3. Clone the FRESCO Repository**
```bash
git clone https://github.com/Vachan-Vanian/FRESCO-database.git
cd FRESCO-database
```

### 2.2 Verify Installation

1. **Check Python installation:**
```bash
python --version  # Should be 3.8+
```

3. **Test the installation:**
```python
from src.database_editor import FrescoDatabase

# Create a test database
db = FrescoDatabase("test_db", compress_db=False)
print(f"Database initialized successfully!")
```

---

## 3. Quick Start Guide

### 3.1 Creating Your First Database

```python
from src.database_editor import FrescoDatabase

# Initialize database
db = FrescoDatabase(
    db_name="my_first_database",
    compress_db=False,  # Use True for compressed storage
    auto_save=True,     # Auto-save after operations
    auto_back_up=True   # Auto-backup on load
)
```

### 3.2 Adding Your First Entry

**Step 1: Use the Template**

Start with the template from `Examples/Templates/TEMPLATE_RCF.py`:

```python
from Examples.Templates.TEMPLATE_RCF import TEMPLATE_RCF
import copy

# Create your entry by copying the template
my_entry = copy.deepcopy(TEMPLATE_RCF)
```

**Step 2: Fill in the Required Fields**

```python
my_entry.update({
    # Reference information
    "specimen_id": "TEST-01",
    "year": 2025,
    "source": "https://doi.org/example",
    "title": "My Test Specimen",
    "authors": "Smith, J., Doe, A.",
    
    # Frame geometry (you can specify units!)
    "frm_h": [1500, "mm"],     # Frame height
    "frm_l": [2100, "mm"],     # Frame length
    "col_h": [200, "mm"],      # Column height
    "col_d": [140, "mm"],      # Column depth
    "bm_h": [250, "mm"],       # Beam height
    "bm_t": [140, "mm"],       # Beam thickness
    
    # Or use simple values (uses database default units)
    "bbm_h": 250,              # Base beam height (mm)
    "bbm_t": 540,              # Base beam thickness (mm)
})
```

**Step 3: Add to Database**

```python
db.add_entry(
    entry_id=1,
    entry_data=my_entry,
    overwrite=False,           # Set True to replace existing
    show_error_fields=True     # Show validation errors
)
```

### 3.3 Your First Complete Example

```python
from src.database_editor import FrescoDatabase

# Initialize database
db = FrescoDatabase("my_project", compress_db=False)

# Simple entry with mixed units
entry = {
    "specimen_id": "SPEC-001",
    "year": 2025,
    "source": "Lab Test",
    "title": "Preliminary Test",
    "authors": "Research Team",
    
    # Frame dimensions in different units
    "frm_h": [1.5, "m"],       # 1.5 meters
    "frm_l": [2100, "mm"],     # 2100 millimeters
    "col_h": [20, "cm"],       # 20 centimeters
    "col_d": [140, "mm"],
    
    # Reinforcement with automatic dimension parsing
    "col_long_reinf_corner": ["4#10", "mm"],  # 4 bars of 10mm diameter
    "col_trans_mid_reinf": ["#6@150", "mm"],  # 6mm bars at 150mm spacing
    
    # Material properties
    "fc": [25, "MPa"],         # Concrete strength
    "fy": [400, "MPa"],        # Steel yield strength
}

# Add to database
db.add_entry(entry_id=1, entry_data=entry)
print("Entry added successfully!")

# View database info
info = db.get_info()
print(f"Total entries: {info['total_entries']}")
```

---

## 4. Understanding the Database Structure

### 4.1 The 13 Sections

The FRESCO database organizes data into 13 logical sections:

| Section | Purpose | Key Fields |
|---------|---------|------------|
| 1. Reference | Basic identification | specimen_id, year, authors, source |
| 2. Frame Geometry | RC frame dimensions | frm_h, frm_l, col_h, bm_h, etc. |
| 3. Infill Geometry | Masonry infill details | inf_type, inf_ul, inf_uh, openings |
| 4. Reinforcement Details | Steel reinforcement | Longitudinal & transverse rebars |
| 5. Concrete Properties | Concrete materials | fc, Ec, density |
| 6. Steel Properties | Steel materials | fy, fu, Ey |
| 7. Infill Mechanical Properties | Masonry materials | Brick and mortar properties |
| 8. Loading (In-Plane) | In-plane loading | Protocol, loads |
| 9. Loading (Out-of-Plane) | Out-of-plane loading | Protocol, loads |
| 10. Response (Global) | System-level response | Stiffness, peak load, failure mode |
| 11. Response (Local) | Component response | Crack patterns, damage |
| 12. Retrofit Techniques | Strengthening methods | Intervention description |
| 13. General Comments | Additional notes | User comments |

### 4.2 Field Types and Units

Each field has a specific type and unit category:

```python
# Example field configurations
{
    "frm_h": {
        "group": "frame_geometry",
        "unit": "mm",                    # Default unit
        "unit_type": "Length",           # Unit category
        "data_type": "float",            # Data type
        "explanation": "Frame height..."
    }
}
```

**Available Unit Types:**
- `Length`: m, cm, mm, in, ft
- `Pressure`: Pa, kPa, MPa, GPa, psi, ksi
- `Concentrated_Force`: N, kN, MN, lbf, kip
- `Distributed_Force`: N/m, kN/m, lbf/ft, kip/ft
- `Time`: s, min, hr, day
- `Mass`: kg, g, tonne, lb
- `Temperature`: K, C, F
- `Work`: J, kJ, N*m, kN*m, lbf*ft, kip*ft
- `Density`: kg/m^3, g/cm^3, lb/ft^3, pcf
- `Strain`: strain, percent, %, ratio

---

## 5. Working with the Database

### 5.1 Creating a Database Instance

```python
from src.database_editor import FrescoDatabase

db = FrescoDatabase(
    db_name="project_name",           # Database name (without extension)
    compress_db=True,                  # Use gzip compression
    auto_save=True,                    # Auto-save after operations
    auto_back_up=True,                 # Create backups
    show_conversion=True,              # Show unit conversions
    show_invalid_object=True,          # Show invalid objects
    show_invalid_unit=True             # Show invalid units
)
```

**When to use compression:**
- ✅ Large databases (saves disk space)
- ✅ Production databases
- ❌ During active development (slower read/write)
- ❌ When frequently editing in text editor

### 5.2 Adding Entries

**Basic Addition:**

```python
# Prepare entry data
entry_data = {
    "specimen_id": "TEST-01",
    "frm_h": [1500, "mm"],
    # ... other fields
}

# Add to database
success = db.add_entry(
    entry_id=1,
    entry_data=entry_data,
    overwrite=False,              # Don't replace existing
    show_error_fields=True        # Show validation errors
)

if success:
    print("Entry added!")
```

**Adding with Overwrite:**

```python
# Replace existing entry
db.add_entry(
    entry_id=1,
    entry_data=new_data,
    overwrite=True  # ⚠️ This will replace the entire entry
)
```

**Important Notes:**
- Entry IDs must be unique (unless `overwrite=True`)
- Missing fields are filled with defaults from `RCF_DB_EMPTY_FIELDS`
- Fields are automatically reordered to match `RCF_FIELD_CONFIG`

### 5.3 Updating Entries

**Update Specific Fields:**

```python
# Update only specific fields
updates = {
    "fc": [30, "MPa"],        # Update concrete strength
    "fy": [500, "MPa"],       # Update steel strength
}

db.update_entry(
    entry_id=1,
    updates=updates,
    show_error_fields=True
)
```

**Difference between `add_entry` with `overwrite=True` and `update_entry`:**

```python
# add_entry with overwrite=True: Replaces ENTIRE entry
db.add_entry(entry_id=1, entry_data=new_data, overwrite=True)
# Result: Only fields in new_data exist, others are defaults

# update_entry: Updates ONLY specified fields
db.update_entry(entry_id=1, updates=updates)
# Result: Only updated fields change, others remain unchanged
```

### 5.4 Removing Entries

```python
# Remove an entry
success = db.remove_entry(entry_id=1)

if success:
    print("Entry removed!")
else:
    print("Entry not found!")
```

### 5.5 Retrieving Data

```python
# Get specific entry
entry = db.data[1]
print(f"Specimen: {entry['specimen_id']}")
print(f"Frame height: {entry['frm_h']} mm")

# Get all entries
for entry_id, entry_data in db.data.items():
    print(f"Entry {entry_id}: {entry_data['specimen_id']}")

# Get database information
info = db.get_info()
print(f"Database: {info['database_name']}")
print(f"Total entries: {info['total_entries']}")
print(f"Total fields: {info['total_fields']}")
print(f"Reinforcement fields: {info['reinforcement_fields']}")
```

### 5.6 Saving the Database

```python
# Manual save (if auto_save=False)
db.save()

# Automatic saving occurs when:
# - Adding entries (with auto_save=True)
# - Updating entries (with auto_save=True)
# - Removing entries (with auto_save=True)
# - Changing unit systems (always saves)
```

---

## 6. Unit System and Conversions

### 6.1 How Unit Conversion Works

The database uses a **default internal unit system** (defined in `RCF_FIELD_CONFIG`):

```python
# Default units
{
    "frm_h": "mm",      # Length in millimeters
    "fc": "MPa",        # Pressure in megapascals
    "fy": "MPa",        # Pressure in megapascals
    # ... etc
}
```

When you enter data, you can specify any compatible unit:

```python
entry = {
    "frm_h": [1.5, "m"],      # Entered as meters
    # Internally stored as 1500 mm
    
    "fc": [3625, "psi"],      # Entered as psi
    # Internally stored as 25 MPa
}
```

### 6.2 Specifying Units When Adding Data

**Method 1: List Format [value, unit]**

```python
entry = {
    "frm_h": [5, "ft"],              # 5 feet → converted to mm
    "col_h": [8, "in"],              # 8 inches → converted to mm
    "fc": [3600, "psi"],             # 3600 psi → converted to MPa
    "fy": [60, "ksi"],               # 60 ksi → converted to MPa
}
```

**Method 2: Simple Value (uses default units)**

```python
entry = {
    "frm_h": 1500,    # Already in mm (default)
    "fc": 25,         # Already in MPa (default)
}
```

**Method 3: Mixed Approach**

```python
entry = {
    "frm_h": [1.5, "m"],       # Specify unit
    "frm_l": 2100,             # Use default (mm)
    "col_h": [20, "cm"],       # Specify unit
    "col_d": 140,              # Use default (mm)
}
```

### 6.3 Changing Database Unit System

You can change the entire database unit system:

```python
# Define new unit system
new_units = {
    "frm_h": "m",         # Change from mm to m
    "frm_l": "m",         # Change from mm to m
    "col_h": "cm",        # Change from mm to cm
    "fc": "ksi",          # Change from MPa to ksi
    "fy": "ksi",          # Change from MPa to ksi
}

# Apply changes (automatically converts ALL existing data!)
db.set_field_units(new_units)
```

**⚠️ Important:**
- This converts **ALL** existing entries
- Reinforcement strings are also converted (e.g., "4#20" → "4#2" if mm→cm)
- Creates automatic backup before conversion
- Cannot be undone easily (restore from backup if needed)

### 6.4 Reinforcement Field Unit Conversion

Reinforcement notation includes embedded dimensions:

```python
# Original (mm):
"col_long_reinf_corner": ["4#20", "mm"]   # 4 bars, 20mm diameter

# After converting to cm:
"col_long_reinf_corner": "4#2"             # 4 bars, 2cm diameter

# Transverse reinforcement with spacing:
# Original (mm):
"col_trans_mid_reinf": ["#10@150", "mm"]   # 10mm bars at 150mm spacing

# After converting to cm:
"col_trans_mid_reinf": "#1@15"             # 1cm bars at 15cm spacing
```

### 6.5 Available Units Quick Reference

See `Examples/Templates/AVAILABLE_UNITS_FOR_TEMPLATE_RCF.py` for complete list:

```python
AVAILABLE_UNITS = {
    'Length': ['m', 'cm', 'mm', 'in', 'ft'],
    'Pressure': ['Pa', 'kPa', 'MPa', 'GPa', 'psi', 'ksi'],
    'Concentrated_Force': ['N', 'kN', 'MN', 'lbf', 'kip'],
    'Distributed_Force': ['N/m', 'kN/m', 'lbf/ft', 'kip/ft'],
    'Time': ['s', 'min', 'hr', 'day'],
    'Density': ['kg/m^3', 'g/cm^3', 'lb/ft^3'],
    'Work': ['J', 'kJ', 'N*m', 'kN*m', 'lbf*ft', 'kip*ft'],
    'Strain': ['strain', 'percent', '%', 'ratio'],
}
```

---

## 7. Reinforcement Notation

### 7.1 Understanding Reinforcement Strings

FRESCO uses a **smart notation** for reinforcement that includes:
- Number of bars
- Bar diameter
- Spacing (for transverse reinforcement)

**Format:**
```
[count]#[diameter][@spacing]

Where:
- count: Number of bars (optional for transverse)
- diameter: Bar diameter
- spacing: Center-to-center spacing (optional)
```

### 7.2 Longitudinal Reinforcement Examples

```python
# Corner reinforcement
"col_long_reinf_corner": ["4#20", "mm"]
# → 4 bars of 20mm diameter at corners

# Top reinforcement
"col_long_reinf_top": ["2#16", "mm"]
# → 2 bars of 16mm diameter

# Multiple bar groups
"bm_long_reinf_top": ["3#20+2#16", "mm"]
# → 3 bars of 20mm + 2 bars of 16mm diameter
```

### 7.3 Transverse Reinforcement (Stirrups) Examples

```python
# With count and spacing
"col_trans_mid_reinf": ["1#8@150", "mm"]
# → Single 8mm stirrup at 150mm spacing

# Without count (assumes 1)
"col_trans_mid_reinf": ["#8@150", "mm"]
# → Same as above

# Multiple types
"col_trans_crit_bot_reinf": ["2#8@100", "mm"]
# → Double 8mm stirrups at 100mm spacing
```

### 7.4 Fields with Reinforcement Notation

**All fields containing `_reinf` are parsed:**

**Columns:**
- `col_long_reinf_corner`
- `col_long_reinf_top`
- `col_long_reinf_mid`
- `col_long_reinf_bot`
- `col_trans_crit_top_reinf`
- `col_trans_crit_bot_reinf`
- `col_trans_mid_reinf`

**Beams:**
- `bm_long_reinf_corner`
- `bm_long_reinf_top`
- `bm_long_reinf_mid`
- `bm_long_reinf_bot`
- `bm_trans_crit_left_reinf`
- `bm_trans_crit_right_reinf`
- `bm_trans_mid_reinf`

**Base Beams:** (same pattern as beams)

**Slabs:**
- `slb_top_l_reinf`
- `slb_top_d_reinf`
- `slb_bot_l_reinf`
- `slb_bot_d_reinf`

### 7.5 Common Mistakes to Avoid

❌ **Wrong:**
```python
# Missing # symbol
"col_long_reinf_corner": ["420", "mm"]  # Will not parse!

# Wrong separator
"col_long_reinf_corner": ["4-20", "mm"]  # Use # not -

# Missing unit
"col_long_reinf_corner": "4#20"  # Ambiguous, specify unit!
```

✅ **Correct:**
```python
"col_long_reinf_corner": ["4#20", "mm"]
"col_trans_mid_reinf": ["#8@150", "mm"]
"bm_long_reinf_top": ["3#20+2#16", "mm"]
```

---

## 8. Data Entry Best Practices

### 8.1 Starting with the Template

**Always start with the template:**

```python
from Examples.Templates.TEMPLATE_RCF import TEMPLATE_RCF
import copy

# Create a copy (don't modify original)
my_entry = copy.deepcopy(TEMPLATE_RCF)

# Update only what you need
my_entry.update({
    "specimen_id": "MY-SPEC-01",
    # ... other fields
})
```

### 8.2 Required vs Optional Fields

**Absolutely Required:**
```python
{
    "specimen_id": "...",    # Must be unique and descriptive
    "year": 2025,            # Publication year
    "source": "...",         # DOI or URL
    "title": "...",          # Reference title
    "authors": "...",        # Author names
}
```

**Critical for 3D Modeling:**
```python
{
    # Frame dimensions
    "frm_h": ...,  "frm_l": ...,
    "col_h": ...,  "col_d": ...,
    "bm_h": ...,   "bm_t": ...,
    
    # Reinforcement (at minimum)
    "col_long_reinf_corner": ["4#..", "mm"],
    "col_trans_mid_reinf": ["#..@..", "mm"],
    "bm_long_reinf_corner": ["4#..", "mm"],
    "bm_trans_mid_reinf": ["#..@..", "mm"],
}
```

### 8.3 Data Entry Workflow

**Step 1: Gather Information**
```
Read the experimental paper and extract:
- Specimen ID and reference details
- All geometric dimensions
- Reinforcement details
- Material properties
- Loading protocol
- Test results
```

**Step 2: Prepare Entry Dictionary**
```python
# Start with template
entry = copy.deepcopy(TEMPLATE_RCF)

# Fill in sections systematically
# Section 1: Reference
entry["specimen_id"] = "..."
entry["year"] = ...

# Section 2: Frame Geometry
entry["frm_h"] = [..., "..."]
# ... continue
```

**Step 3: Validate Before Adding**
```python
# Check for required fields
required = ["specimen_id", "year", "source", "title", "authors"]
for field in required:
    assert field in entry and entry[field], f"Missing {field}"

# Check for placeholder types
for key, value in entry.items():
    assert not isinstance(value, type), f"{key} has type object!"
```

**Step 4: Add to Database**
```python
db.add_entry(
    entry_id=1,
    entry_data=entry,
    show_error_fields=True  # Shows validation issues
)
```

### 8.4 Handling Missing Data

**For Unknown Numeric Values:**
```python
# Option 1: Use 0 (default from RCF_DB_EMPTY_FIELDS)
"fc": 0,

# Option 2: Omit the field (will use default)
# Don't include "fc" in your entry

# Option 3: Use reasonable assumptions
"Ec": [4700 * (fc**0.5), "MPa"]  # ACI formula
```

**For Unknown String Values:**
```python
# Use descriptive placeholders
"inf_mortar_type": "Type M (assumed)",
"glb_failure_mode": "Not reported in source",
"comments": "Material properties estimated from similar specimens"
```

**❌ Never use type objects for missing data:**
```python
# WRONG:
"fc": float,
"fy": int,
"inf_mortar_type": str

# These will be rejected during validation!
```

### 8.5 Unit Consistency

**Be consistent within an entry:**

```python
# Good: Consistent use of metric
entry = {
    "frm_h": [1500, "mm"],
    "frm_l": [2100, "mm"],
    "col_h": [200, "mm"],
    "fc": [25, "MPa"],
    "fy": [400, "MPa"],
}

# Also good: Consistent use of imperial
entry = {
    "frm_h": [5, "ft"],
    "frm_l": [7, "ft"],
    "col_h": [8, "in"],
    "fc": [3625, "psi"],
    "fy": [58, "ksi"],
}

# Avoid mixing without good reason:
entry = {
    "frm_h": [1500, "mm"],
    "frm_l": [7, "ft"],        # Different unit
    "col_h": [200, "mm"],
}
```

### 8.6 Documentation in Comments

**Use the comments field:**

```python
entry["comments"] = """
1. Material properties from companion paper (DOI: ...)
2. Base beam reinforcement estimated (not reported)
3. Slab dimensions include topping
4. Test conducted at 0.5 scale per Cauchy similarity
"""
```

### 8.7 Validation Checklist

Before finalizing an entry:

- [ ] All required fields filled
- [ ] No `type` objects (float, int, str) in data
- [ ] Units specified for all dimensional data
- [ ] Reinforcement notation correct (use `#` and `@`)
- [ ] Consistent unit system
- [ ] Comments added for assumptions/missing data
- [ ] Cross-checked with source document
- [ ] No obvious typos in numeric values

---

## 9. Exporting Data

### 9.1 Export to JSON

```python
# Export with same units as database
db.export_json(filename="my_export")
# Creates: my_export.json (or .json.gz if compress_db=True)

# Export with custom units
target_units = {
    "frm_h": "m",
    "frm_l": "m",
    "col_h": "cm",
    "fc": "psi",
    "fy": "ksi",
}

db.export_json(
    filename="my_export_imperial",
    target_units=target_units
)
```

**Output Structure:**
```json
{
  "config": {
    "field_units": {...},
    "field_config": {...},
    "version": "1.0",
    "created_date": "2025-01-15T10:30:00",
    "last_modified": "2025-01-20T14:45:00"
  },
  "data": {
    "1": {
      "specimen_id": "TEST-01",
      "frm_h": 1500,
      ...
    }
  },
  "total_entries": 1
}
```

### 9.2 Export to CSV

```python
# Basic CSV export
db.export_to_csv(
    filename="my_export",
    include_units_header=True,    # Include units in second row
    selected_fields=None           # Export all fields
)

# Export specific fields only
selected = [
    "specimen_id", "year", "authors",
    "frm_h", "frm_l", "col_h", "bm_h",
    "fc", "fy", "glb_peak_lateral_load"
]

db.export_to_csv(
    filename="summary_export",
    selected_fields=selected,
    include_units_header=True
)

# Export with unit conversion
target_units = {
    "frm_h": "ft",
    "frm_l": "ft",
    "fc": "ksi",
}

db.export_to_csv(
    filename="imperial_export",
    target_units=target_units,
    include_units_header=True
)
```

**CSV Format:**

Without units header:
```csv
entry_id,specimen_id,year,frm_h,frm_l,fc
1,TEST-01,2025,1500,2100,25
2,TEST-02,2025,1800,2400,30
```

With units header:
```csv
entry_id,specimen_id,year,frm_h,frm_l,fc
ID,,,,mm,mm,MPa
1,TEST-01,2025,1500,2100,25
2,TEST-02,2025,1800,2400,30
```

### 9.3 Programmatic Access

```python
# Access database data directly
import json

# Read JSON database
with open("my_database.json", 'r') as f:
    data = json.load(f)

# Access entries
for entry_id, entry_data in data['data'].items():
    print(f"{entry_id}: {entry_data['specimen_id']}")

# Get field units
units = data['config']['field_units']
print(f"Frame height unit: {units['frm_h']}")
```

---

## 10. 3D Model Generation

### 10.1 Prerequisites

```bash
# Install FreeCAD v1.0
# Download from: https://www.freecad.org/

# Check Python path
python -c "import FreeCAD; print(FreeCAD.Version())"
```

### 10.2 Basic Model Generation

```python
# In rcf_model_creator.py

from src.rcf_model import RCFrameGenerator

generator = RCFrameGenerator(
    database_folder_path = "Database/",
    cad_folder_path = "Models/",
    database_name = "fresco_v1",
    compress_db = False)

generator.generate_db_model(database_entry_id=1)

## Optional
# generator.generate_frp_beam_column()
# generator.generate_frp_infill()
# generator.generate_trm_infill()

generator.export_model()

```

### 10.3 Model Generation Stages

The script creates models in 5 stages:

**Stage 1: RC Frame Geometry**
- Columns (left & right)
- Beams (top)
- Base beam (bottom)
- Slab (if specified)

**Stage 2: Transverse Reinforcement (Stirrups)**
- Column stirrups (top/mid/bottom regions)
- Beam stirrups (left/mid/right regions)
- Base beam stirrups
- Slab mesh (if specified)

**Stage 3: Longitudinal Reinforcement**
- Corner bars
- Top/mid/bottom bars

**Stage 4: Infill Brick Pattern**
- Running bond or stack bond
- First row (full bricks)
- Second row (offset or aligned)
- Vertical repetition
- Final row (adjusted height)

**Stage 5: Mortar and Interfaces**
- Mortar joints (bed & head)
- Frame-infill interfaces
- Openings (windows/doors)

### 10.4 Advanced Model Features

The generator supports additional strengthening features:

**TRM Reinforcement**
```python
# Generate Textile Reinforced Mortar (TRM) layer for infill
generator.generate_trm_infill(
    trm_thickness=[10, 'mm'],      # Thickness of TRM layer
    grid_spacing_h=[25, 'mm'],     # Horizontal grid spacing
    grid_spacing_v=[25, 'mm'],     # Vertical grid spacing
    z_offset=[100, 'mm']           # Z-axis offset
)
```

**FRP Strengthening**
```python
# Generate Fiber-Reinforced Polymer (FRP) infill strengthening
generator.generate_frp_infill(
    anchor_extension_z=[50, 'mm'],   # Anchor extension depth
    z_offset=[100, 'mm']             # Z-axis offset
)

# Generate FRP column/beam wrapping
generator.generate_frp_beam_column(
    wrap_columns=True,                  # Wrap columns (bool)
    column_bottom_length=[300, 'mm'],   # Bottom column wrapping length
    column_top_length=[300, 'mm'],      # Top column wrapping length
    beam_flexural=False,                # Create flexural strengthening (bool)
    beam_flexural_length=None,          # Length of flexural strengthening (None = full)
    beam_flexural_center=False,         # Center the flexural strengthening (bool)
    beam_shear_left=True,               # Create left shear strengthening (bool)
    beam_shear_left_length=[300, 'mm'], # Length of left shear region
    beam_shear_right=True,              # Create right shear strengthening (bool)
    beam_shear_right_length=[300, 'mm'] # Length of right shear region
)
```
### 10.5 STEP File Export

Models are exported in ISO 10303-21 (STEP AP214) format:

**Advantages:**
- ✅ Industry standard
- ✅ Compatible with ANSYS, Abaqus, etc.
- ✅ Preserves geometry precisely
- ✅ Readable by most CAD systems

**Importing into ANSYS:**
```python
# ANSYS SpaceClaim
File → Open → Select .step file

# ANSYS Workbench
Geometry → Import → External Geometry File
```

### 10.6 Troubleshooting Model Generation

**Issue: Model not generated**
```python
# Check database entry exists
print(db.data[DATABASE_ENTRY_ID])

# Check required fields
required_geom = ["frm_h", "frm_l", "col_h", "col_d", "bm_h", "bm_t"]
for field in required_geom:
    assert field in db.data[DATABASE_ENTRY_ID], f"Missing {field}"
```

**Issue: Reinforcement not visible**
```python
# Check reinforcement fields are strings, not types
entry = db.data[1]
print(type(entry["col_long_reinf_corner"]))  # Should be <class 'str'>

# Not: <class 'type'>
```

**Issue: Infill not created**
```python
# Check infill type
print(db.data[1]["inf_type"])  # Should be "one_wythe", "two_wythe", or "none"

# Check infill dimensions
assert db.data[1]["inf_ul"] > 0, "Invalid infill unit length"
assert db.data[1]["inf_uh"] > 0, "Invalid infill unit height"
```

---

## 11. Common Issues and Troubleshooting

### 11.1 Entry Not Saving

**Symptom:** Entry added but database file not updated

**Causes & Solutions:**

```python
# Cause 1: auto_save=False
db = FrescoDatabase("test", auto_save=False)
db.add_entry(1, data)
# Solution: Manual save
db.save()

# Cause 2: Permission issues
# Check write permissions on Database/ folder

# Cause 3: File locked by another process
# Close any programs accessing the .json file
```

### 11.2 Unit Conversion Errors

**Symptom:** ValueError about unit types

```python
# Error: "Invalid unit 'meters' for unit type 'Length'"

# Cause: Wrong unit name
entry = {"frm_h": [1.5, "meters"]}  # ❌ Wrong

# Solution: Use correct unit name
entry = {"frm_h": [1.5, "m"]}       # ✅ Correct

# Check available units:
from Examples.Templates.AVAILABLE_UNITS_FOR_TEMPLATE_RCF import AVAILABLE_UNITS
print(AVAILABLE_UNITS['Length'])
# ['m', 'cm', 'mm', 'in', 'ft']
```

### 11.3 Reinforcement Parsing Errors

**Symptom:** Reinforcement string not converted during unit change

```python
# Check if field is recognized as reinforcement
parser = db.reinforcement_parser
print(parser.is_reinforcement_field("col_long_reinf_corner"))  # True
print(parser.is_reinforcement_field("col_h"))                  # False

# Common issues:
# 1. Missing # symbol
"4-20"      # ❌ Wrong separator
"4#20"      # ✅ Correct

# 2. Extra spaces
"4 # 20"    # ❌ Has spaces
"4#20"      # ✅ No spaces

# 3. Decimal handling
"4#20.5"    # ✅ Supported
"4#20,5"    # ❌ Use . not ,
```

### 11.4 Invalid Objects in Entry

**Symptom:** "Removed invalid fields" message

```python
# Cause: Type objects used for missing data
entry = {
    "fc": float,         # ❌ Type object
    "fy": int,           # ❌ Type object
    "specimen_id": str,  # ❌ Type object
}

# Solution: Use actual values or omit fields
entry = {
    "fc": 0,                    # ✅ Or omit for default
    "fy": 0,                    # ✅ Or omit for default
    "specimen_id": "TEST-01",   # ✅ Actual value
}
```

### 11.5 Missing Fields After Add/Update

**Symptom:** Fields not appearing in entry

```python
# Cause: Fields outside RCF_FIELD_CONFIG
entry = {"my_custom_field": 123}  # Not in config!

# Solution: Only use defined fields
from src.db_fields import RCF_FIELD_CONFIG
print(list(RCF_FIELD_CONFIG.keys()))  # See all valid fields

# Or: Extend RCF_FIELD_CONFIG if needed
```

### 11.6 Database Won't Load

**Symptom:** Error when creating FrescoDatabase instance

```python
# Cause 1: Corrupted JSON file
# Solution: Restore from backup
# Look for: Database/my_database_backup_YYYYMMDD_HHMMSS.json

# Cause 2: Compression mismatch
# File is .json but trying to load as compressed
db = FrescoDatabase("test", compress_db=True)
# Solution: Match compression setting to file type
db = FrescoDatabase("test", compress_db=False)  # For .json
db = FrescoDatabase("test", compress_db=True)   # For .json.gz

# Cause 3: Invalid JSON syntax
# Solution: Validate JSON
import json
with open("Database/test.json") as f:
    json.load(f)  # Will show syntax error
```

### 11.7 Model Generation Issues

**Symptom:** 3D model incomplete or incorrect

```python
# Issue 1: Missing geometry
# Check for negative or zero dimensions
entry = db.data[1]
assert entry["frm_h"] > 0, "Invalid frame height"
assert entry["col_h"] > 0, "Invalid column dimension"

# Issue 2: Reinforcement not visible
# Check field contains string, not type
assert isinstance(entry["col_long_reinf_corner"], str)

# Issue 3: Infill not generated
# Check infill type and dimensions
assert entry["inf_type"] in ["one_wythe", "two_wythe"]
assert entry["inf_ul"] > 0 and entry["inf_uh"] > 0

# Issue 4: FreeCAD import error
# Update FreeCAD to v1.0 or later
```

### 11.8 Performance Issues

**Symptom:** Slow database operations

```python
# For large databases (>100 entries):

# 1. Use compression
db = FrescoDatabase("large_db", compress_db=True)

# 2. Disable auto-save during bulk operations
db.auto_save = False
for i, entry in enumerate(entries):
    db.add_entry(i, entry)
db.save()  # Single save at end

# 3. Disable conversion messages
db.show_conversion = False

# 4. Use batch operations
# Instead of multiple updates:
updates = {}
for field, value in changes.items():
    updates[field] = value
db.update_entry(id, updates)  # Single update
```

---

## 12. Advanced Usage

### 12.1 Custom Field Configurations

To add custom fields (requires modifying source):

```python
# In src/db_fields.py, add to RCF_FIELD_CONFIG:

RCF_FIELD_CONFIG = {
    # ... existing fields ...
    
    # Custom field
    "custom_measurement": {
        "group": "custom_group",
        "sub_group": "",
        "unit": "mm",
        "unit_type": "Length",
        "data_type": "float",
        "explanation": "Custom measurement description"
    },
}

# Also add default value in RCF_DB_EMPTY_FIELDS:
RCF_DB_EMPTY_FIELDS = {
    # ... existing fields ...
    "custom_measurement": 0.0,
}
```

### 12.2 Batch Processing

```python
from src.database_editor import FrescoDatabase
import json

# Load entries from external source
with open("entries_to_import.json") as f:
    entries = json.load(f)

# Create database
db = FrescoDatabase("batch_import", auto_save=False)

# Batch add entries
for idx, entry_data in entries.items():
    print(f"Processing entry {idx}...")
    db.add_entry(
        entry_id=int(idx),
        entry_data=entry_data,
        show_error_fields=False  # Suppress messages
    )

# Single save after all additions
db.save()
print(f"Imported {len(entries)} entries")
```

### 12.3 Database Merging

```python
def merge_databases(db1_name, db2_name, output_name):
    """Merge two databases into one"""
    
    # Load both databases
    db1 = FrescoDatabase(db1_name, auto_save=False)
    db2 = FrescoDatabase(db2_name, auto_save=False)
    
    # Create output database
    db_merged = FrescoDatabase(output_name, auto_save=False)
    
    # Copy from db1
    for entry_id, entry_data in db1.data.items():
        db_merged.data[entry_id] = entry_data
    
    # Copy from db2 with offset IDs
    max_id = max(db1.data.keys()) if db1.data else 0
    for entry_id, entry_data in db2.data.items():
        new_id = max_id + entry_id
        db_merged.data[new_id] = entry_data
    
    # Save merged database
    db_merged.save()
    print(f"Merged {len(db1.data)} + {len(db2.data)} entries")
    return db_merged

# Usage
merged = merge_databases("project_A", "project_B", "combined_project")
```

### 12.4 Data Validation Scripts

```python
def validate_database(db_name):
    """Comprehensive database validation"""
    
    db = FrescoDatabase(db_name)
    issues = []
    
    for entry_id, entry in db.data.items():
        # Check required fields
        required = ["specimen_id", "year", "source"]
        for field in required:
            if not entry.get(field):
                issues.append(f"Entry {entry_id}: Missing {field}")
        
        # Check for type objects
        for field, value in entry.items():
            if isinstance(value, type):
                issues.append(f"Entry {entry_id}: {field} is type object")
        
        # Check geometry consistency
        if entry.get("frm_h", 0) <= 0:
            issues.append(f"Entry {entry_id}: Invalid frm_h")
        
        if entry.get("col_h", 0) > entry.get("frm_h", float('inf')):
            issues.append(f"Entry {entry_id}: col_h > frm_h")
        
        # Check material properties
        if entry.get("fc", 0) < 0 or entry.get("fc", 0) > 200:
            issues.append(f"Entry {entry_id}: Suspicious fc value")
    
    if issues:
        print("Validation Issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✓ All entries valid!")
    
    return issues

# Usage
validate_database("my_project")
```

### 12.5 Automated Unit System Detection

```python
def detect_unit_system(entry_data):
    """Detect if entry uses metric or imperial"""
    
    metric_indicators = ['mm', 'cm', 'm', 'MPa', 'kN', 'kg']
    imperial_indicators = ['in', 'ft', 'psi', 'ksi', 'kip', 'lb']
    
    metric_count = 0
    imperial_count = 0
    
    for field, value in entry_data.items():
        if isinstance(value, (list, tuple)) and len(value) == 2:
            unit = value[1]
            if unit in metric_indicators:
                metric_count += 1
            elif unit in imperial_indicators:
                imperial_count += 1
    
    if metric_count > imperial_count:
        return "metric"
    elif imperial_count > metric_count:
        return "imperial"
    else:
        return "mixed"

# Usage
system = detect_unit_system(my_entry)
print(f"Entry uses {system} units")
```

### 12.6 Query and Filtering

```python
def query_database(db, conditions):
    """Query database with conditions"""
    
    results = []
    
    for entry_id, entry in db.data.items():
        match = True
        for field, condition in conditions.items():
            if callable(condition):
                if not condition(entry.get(field)):
                    match = False
                    break
            else:
                if entry.get(field) != condition:
                    match = False
                    break
        
        if match:
            results.append((entry_id, entry))
    
    return results

# Usage examples:

# Find all entries from a specific author
results = query_database(db, {
    "authors": lambda x: "Smith" in x if x else False
})

# Find entries with high concrete strength
results = query_database(db, {
    "fc": lambda x: x > 30 if x else False
})

# Find entries from specific year
results = query_database(db, {
    "year": 2019
})

# Multiple conditions
results = query_database(db, {
    "year": lambda x: x >= 2015,
    "inf_type": "one_wythe",
    "fc": lambda x: x > 20 if x else False
})

print(f"Found {len(results)} matching entries")
for entry_id, entry in results:
    print(f"  {entry_id}: {entry['specimen_id']}")
```

---

## 13. Complete Examples

### 13.1 Example 1: Simple Single-Bay Frame

```python
from src.database_editor import FrescoDatabase

# Create database
db = FrescoDatabase("simple_frame", compress_db=False)

# Define entry
entry = {
    # Reference
    "specimen_id": "SIMPLE-01",
    "year": 2025,
    "source": "Laboratory Test",
    "title": "Simple Frame Test",
    "authors": "Test Team",
    
    # Frame geometry (metric units)
    "frm_h": [1500, "mm"],
    "frm_l": [2000, "mm"],
    "col_h": [200, "mm"],
    "col_d": [200, "mm"],
    "bm_h": [300, "mm"],
    "bm_t": [200, "mm"],
    "bbm_h": [400, "mm"],
    "bbm_t": [200, "mm"],
    
    # No infill
    "inf_type": "none",
    
    # Basic reinforcement
    "col_cover": [30, "mm"],
    "col_long_reinf_corner": ["4#16", "mm"],
    "col_trans_mid_reinf": ["#8@200", "mm"],
    
    "bm_cover": [30, "mm"],
    "bm_long_reinf_corner": ["4#16", "mm"],
    "bm_trans_mid_reinf": ["#8@200", "mm"],
    
    "bbm_cover": [40, "mm"],
    "bbm_long_reinf_corner": ["4#20", "mm"],
    "bbm_trans_mid_reinf": ["#10@150", "mm"],
    
    # Material properties
    "fc": [25, "MPa"],
    "Ec": [25000, "MPa"],
    "conc_density": [2400, "kg/m^3"],
    "fy": [420, "MPa"],
    "fu": [550, "MPa"],
    
    # Loading
    "inp_loading_protocol": "cyclic",
    "inp_cyclic_protocol": "ACI374",
    "inp_column_vertical_load": [100, "kN"],
}

# Add to database
db.add_entry(entry_id=1, entry_data=entry)

# Get info
info = db.get_info()
print(f"Database: {info['database_name']}")
print(f"Entries: {info['total_entries']}")

# Export
db.export_to_csv("simple_frame_export")
```

### 13.2 Example 2: Infilled Frame with Opening

```python
from src.database_editor import FrescoDatabase
import copy
from Examples.Templates.TEMPLATE_RCF import TEMPLATE_RCF

# Create database
db = FrescoDatabase("infilled_frame", compress_db=True)

# Start with template
entry = copy.deepcopy(TEMPLATE_RCF)

# Update with actual data
entry.update({
    # Reference
    "specimen_id": "INF-WIN-01",
    "year": 2025,
    "source": "https://doi.org/example",
    "title": "Infilled Frame with Window Opening",
    "authors": "Researcher, A., Colleague, B.",
    
    # Frame geometry
    "frm_h": [1800, "mm"],
    "frm_l": [2400, "mm"],
    "col_h": [250, "mm"],
    "col_d": [250, "mm"],
    "bm_h": [350, "mm"],
    "bm_t": [250, "mm"],
    
    # Infill with window
    "inf_type": "one_wythe",
    "inf_opn_type": "window",
    "inf_bnd_pat": "running",
    "inf_inff_intfc": "mortar_bond",
    
    # Infill dimensions
    "inf_ul": [200, "mm"],
    "inf_uh": [100, "mm"],
    "inf_ut": [100, "mm"],
    "inf_uhead_t": [10, "mm"],
    "inf_ubed_t": [10, "mm"],
    
    # Window opening
    "inf_win_h": [800, "mm"],
    "inf_win_v": [600, "mm"],
    "inf_win_ph": [800, "mm"],
    "inf_win_pv": [600, "mm"],
    
    # Frame-infill interface
    "inf_interface_bottom": [10, "mm"],
    "inf_interface_left": [10, "mm"],
    "inf_interface_top": [10, "mm"],
    "inf_interface_right": [10, "mm"],
    
    # Reinforcement
    "col_cover": [25, "mm"],
    "col_long_reinf_corner": ["4#16", "mm"],
    "col_long_reinf_top": ["2#12", "mm"],
    "col_long_reinf_bot": ["2#12", "mm"],
    "col_trans_crit_top_distance": [400, "mm"],
    "col_trans_crit_top_reinf": ["#8@100", "mm"],
    "col_trans_crit_bot_distance": [400, "mm"],
    "col_trans_crit_bot_reinf": ["#8@100", "mm"],
    "col_trans_mid_reinf": ["#8@200", "mm"],
    
    # Material properties
    "fc": [30, "MPa"],
    "fy": [500, "MPa"],
    "inf_unit_density": [1800, "kg/m^3"],
    "inf_mortar_density": [2000, "kg/m^3"],
    "inf_unit_compressive_strength_width": [15, "MPa"],
    "inf_mortar_compressive_strength": [10, "MPa"],
    
    # Test results
    "glb_initial_stiffness": [25, "kN/mm"],
    "glb_peak_lateral_load": [180, "kN"],
    "glb_drift_at_peak_lateral_load": [1.2, "%"],
    "glb_failure_mode": "Diagonal cracking of infill with corner crushing",
    
    # Comments
    "comments": "Window opening significantly reduced lateral capacity"
})

# Add to database
db.add_entry(entry_id=1, entry_data=entry)

# Generate 3D model (in separate script)
# Set DATABASE_NAME="infilled_frame" and DATABASE_ENTRY_ID=1 in rcf_model_creator.py
```

### 13.3 Example 3: Multi-Entry Database with Variations

```python
from src.database_editor import FrescoDatabase

# Create database
db = FrescoDatabase("parametric_study", compress_db=True, auto_save=False)

# Base specimen configuration
base_config = {
    "specimen_scale": 0.5,
    "source": "Parametric Study 2025",
    "title": "Effect of Infill Properties on Frame Response",
    "authors": "Research Team",
    "year": 2025,
    
    # Frame geometry (constant)
    "frm_h": [1500, "mm"],
    "frm_l": [2000, "mm"],
    "col_h": [200, "mm"],
    "col_d": [200, "mm"],
    "bm_h": [300, "mm"],
    "bm_t": [200, "mm"],
    
    # Infill geometry (constant)
    "inf_type": "one_wythe",
    "inf_ul": [200, "mm"],
    "inf_uh": [100, "mm"],
    "inf_ut": [100, "mm"],
    "inf_uhead_t": [10, "mm"],
    "inf_ubed_t": [10, "mm"],
    
    # Reinforcement (constant)
    "col_cover": [25, "mm"],
    "col_long_reinf_corner": ["4#16", "mm"],
    "col_trans_mid_reinf": ["#8@150", "mm"],
    "bm_cover": [25, "mm"],
    "bm_long_reinf_corner": ["4#16", "mm"],
    "bm_trans_mid_reinf": ["#8@150", "mm"],
    
    # Concrete (constant)
    "fc": [25, "MPa"],
    "fy": [420, "MPa"],
}

# Variable: Infill strength
infill_strengths = [5, 10, 15, 20, 25]  # MPa

for idx, strength in enumerate(infill_strengths, start=1):
    entry = base_config.copy()
    entry.update({
        "specimen_id": f"PARAM-{idx:02d}",
        "inf_unit_compressive_strength_width": [strength, "MPa"],
        "inf_mortar_compressive_strength": [strength * 0.7, "MPa"],
    })
    
    db.add_entry(entry_id=idx, entry_data=entry)
    print(f"Added specimen {idx} with fc_infill={strength} MPa")

# Save all at once
db.save()

# Export summary
db.export_to_csv(
    filename="parametric_summary",
    selected_fields=[
        "specimen_id",
        "inf_unit_compressive_strength_width",
        "inf_mortar_compressive_strength"
    ]
)

print(f"Created database with {len(db.data)} specimens")
```

### 13.4 Example 4: Imperial Units Entry

```python
from src.database_editor import FrescoDatabase

# Create database
db = FrescoDatabase("imperial_study", compress_db=False)

# Entry in US customary units
entry = {
    # Reference
    "specimen_id": "US-FRAME-01",
    "year": 2025,
    "source": "US Laboratory",
    "title": "Frame Test (Imperial Units)",
    "authors": "American Researchers",
    
    # Frame geometry in imperial
    "frm_h": [5, "ft"],          # 5 feet
    "frm_l": [7, "ft"],          # 7 feet
    "col_h": [8, "in"],          # 8 inches
    "col_d": [8, "in"],
    "bm_h": [12, "in"],
    "bm_t": [8, "in"],
    
    # Reinforcement (still in inches for diameter)
    "col_cover": [1, "in"],
    "col_long_reinf_corner": ["4#0.625", "in"],  # #5 bars (5/8")
    "col_trans_mid_reinf": ["#0.375@6", "in"],   # #3 stirrups @ 6"
    
    # Material properties in imperial
    "fc": [4, "ksi"],            # 4000 psi
    "fy": [60, "ksi"],           # 60000 psi
    "conc_density": [150, "pcf"], # pounds per cubic foot
    
    # Loading in imperial
    "inp_column_vertical_load": [22.5, "kip"],  # 22.5 kips
    "glb_peak_lateral_load": [40, "kip"],
}

# Add to database (will be converted to metric internally)
db.add_entry(entry_id=1, entry_data=entry)

# Export in original imperial units
imperial_units = {
    "frm_h": "ft",
    "frm_l": "ft",
    "col_h": "in",
    "col_d": "in",
    "fc": "ksi",
    "fy": "ksi",
}

db.export_json(
    filename="imperial_export",
    target_units=imperial_units
)

# Also export in metric for international use
db.export_json(filename="metric_export")  # Uses database defaults
```

### 13.5 Example 5: Updating Existing Database

```python
from src.database_editor import FrescoDatabase

# Load existing database
db = FrescoDatabase("existing_project")

# Update material properties for entry 5
material_updates = {
    "fc": [30, "MPa"],    # Updated concrete strength
    "fy": [500, "MPa"],   # Updated steel strength
    "Ec": [31000, "MPa"], # Computed from updated fc
}

db.update_entry(entry_id=5, updates=material_updates)

# Add test results for entry 3
results = {
    "glb_initial_stiffness": [32, "kN/mm"],
    "glb_peak_lateral_load": [145, "kN"],
    "glb_drift_at_peak_lateral_load": [1.8, "%"],
    "glb_failure_mode": "Shear failure in columns with infill crushing",
    "lcl_crack_pattern": "Diagonal cracks in infill, flexural cracks in columns",
}

db.update_entry(entry_id=3, updates=results)

# Change unit system for entire database
new_units = {
    "frm_h": "m",
    "frm_l": "m",
    "col_h": "cm",
    "fc": "ksi",
}

# ⚠️ This converts ALL entries!
db.set_field_units(new_units)

# Export updated database
db.export_to_csv("updated_database")
```

---

## Quick Reference Card

### Common Operations

```python
# Initialize
from src.database_editor import FrescoDatabase
db = FrescoDatabase("my_db", compress_db=False, auto_save=True)

# Add entry
db.add_entry(entry_id=1, entry_data=my_entry)

# Update entry
db.update_entry(entry_id=1, updates={"fc": [30, "MPa"]})

# Remove entry
db.remove_entry(entry_id=1)

# Save manually
db.save()

# Export
db.export_to_csv("export")
db.export_json("export")

# Change units
db.set_field_units({"frm_h": "m", "fc": "ksi"})

# Get info
info = db.get_info()
```

### Unit Specification Format

```python
# List format [value, unit]
"frm_h": [1500, "mm"]
"fc": [3625, "psi"]

# Simple value (uses defaults)
"frm_h": 1500  # mm
"fc": 25       # MPa
```

### Reinforcement Notation

```python
# Longitudinal: [count]#[diameter]
"4#20"         # 4 bars of 20mm
"3#16+2#12"    # 3 of 16mm + 2 of 12mm

# Transverse: [count]#[diameter]@[spacing]
"#8@150"       # 8mm bars @ 150mm
"2#8@100"      # Double 8mm @ 100mm
```

### Required Fields

```python
{
    "specimen_id": "...",
    "year": 2025,
    "source": "...",
    "title": "...",
    "authors": "...",
}
```

---

## Getting Help

- **GitHub Issues**: https://github.com/Vachan-Vanian/FRESCO-database/issues
- **Documentation**: See repository README.md and Contribution.md
- **Examples**: Check `Examples/ManuscriptsExamples/` folder

---

**Document Version**: 1.0  
**Last Updated**: October 2025  
**Compatible with**: FRESCO Database v1.0