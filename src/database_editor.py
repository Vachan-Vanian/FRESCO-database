from typing import Dict, List, Any, Optional
import json
import os
import shutil
import copy
from datetime import datetime
import gzip
import csv
from .db_fields import RCF_FIELD_CONFIG, RCF_DB_EMPTY_FIELDS


class FrescoUnits:
    """Essential unit converter for structural engineering"""
    
    def __init__(self):
        self.__basic_units = {
            'Length': {
                'm': 1, 'cm': 0.01, 'mm': 0.001, 'in': 0.0254, 'ft': 0.3048
            },
            'Time': {
                's': 1, 'min': 60, 'hr': 3600, 'day': 86400
            },
            'Mass': {
                'kg': 1, 'g': 0.001, 'tonne': 1000, 'lb': 0.45359237
            },
            'Temperature': {'K': 1, 'C': 1, 'F': 1},
            'Pressure': {
                'Pa': 1, 'kPa': 1000, 'MPa': 1000000, 'GPa': 1000000000,
                'N/mm^2': 1000000, 'psi': 6894.757293168360, 'ksi': 6894757.293168360
            },
            'Concentrated_Force': {
                'N': 1, 'kN': 1000, 'MN': 1000000, 'lbf': 4.448221615260500, 'kip': 4448.221615260500
            },
            'Distributed_Force': {
                'N/m': 1, 'kN/m': 1000, 'N/mm': 1000, 'kN/mm': 1000000,
                'lbf/ft': 14.59390293720640, 
                'kip/ft': 14593.90293720640
            },
            'Work': {
                'J': 1, 'kJ': 1000, 'N*m': 1, 'kN*m': 1000, 'N*mm': 0.001, 'kN*mm': 1,
                'lbf*in': 0.1129848290276170, 'lbf*ft': 1.355817948331400, 
                'kip*in': 112.9848290276170, 'kip*ft': 1355.817948331400
            },
            'Density': {
                'kg/m^3': 1, 'g/cm^3': 1000, 'lb/ft^3': 16.0185, 'pcf': 16.0185
            },
            'Strain': {
                'strain': 1, 'percent': 0.01, '%': 0.01, 'ratio': 1
            }
        }
        self.units = copy.deepcopy(self.__basic_units)
    
    def convert_temperature(self, from_value, from_unit, to_unit):
        if from_unit == to_unit:
            return from_value
        
        if from_unit == 'C':
            kelvin = from_value + 273.15
        elif from_unit == 'F':
            kelvin = (from_value - 32) * 5/9 + 273.15
        else:
            kelvin = from_value
        
        if to_unit == 'C':
            return kelvin - 273.15
        elif to_unit == 'F':
            return (kelvin - 273.15) * 9/5 + 32
        else:
            return kelvin
    
    def convert(self, from_value: float, unit_type: str, from_unit: str, to_unit: str, precision: int = 14) -> float:
        if unit_type not in self.units:
            raise KeyError(f"Unit type '{unit_type}' not recognized")
        if from_unit not in self.units[unit_type]:
            raise KeyError(f"From unit '{from_unit}' not recognized for unit type '{unit_type}'")
        if to_unit not in self.units[unit_type]:
            raise KeyError(f"To unit '{to_unit}' not recognized for unit type '{unit_type}'")
        
        if from_unit == to_unit:
            return from_value
        
        if unit_type == 'Temperature':
            result = self.convert_temperature(from_value, from_unit, to_unit)
        else:
            to_base_factor = self.units[unit_type][from_unit]
            base_value = from_value * to_base_factor
            from_base_factor = self.units[unit_type][to_unit]
            result = base_value / from_base_factor
        
        return round(result, precision)
    
    def get_available_units(self, unit_type: str) -> List[str]:
        return list(self.units.get(unit_type, {}).keys())
    
    def get_unit_types(self) -> List[str]:
        return list(self.units.keys())


class FrescoReinforcementParser:
    """Smart reinforcement parser with dynamic reinforcement field names"""
    
    def __init__(self, converter: FrescoUnits):
        self.converter = converter
    
    def parse_and_convert_reinforcement(self, rebar_string: str, from_unit: str, to_unit: str) -> str:
        """
        Parse reinforcement string, convert embedded dimensions, and reconstruct
        
        Examples:
        - "3#20+2#14" with mm->cm becomes "3#2.0+2#1.4"
        - "#10@150+#8@100" with mm->cm becomes "#1.0@15.0+#0.8@10.0"
        """
        if not rebar_string or from_unit == to_unit:
            return rebar_string
        
        try:
            # Handle compound reinforcement (split by +)
            if '+' in rebar_string:
                parts = [part.strip() for part in rebar_string.split('+')]
                converted_parts = []
                for part in parts:
                    converted_part = self._convert_single_reinforcement(part, from_unit, to_unit)
                    converted_parts.append(converted_part)
                return '+'.join(converted_parts)
            else:
                return self._convert_single_reinforcement(rebar_string, from_unit, to_unit)
        
        except Exception as e:
            print(f"Warning: Could not convert reinforcement '{rebar_string}': {e}")
            return rebar_string
    
    def _convert_single_reinforcement(self, rebar_string: str, from_unit: str, to_unit: str) -> str:
        """Convert a single reinforcement notation"""
        import re
        
        # Pattern to match reinforcement notation
        # Captures: count, diameter, spacing (optional)
        # Examples: "3#20", "#10@150", "2#16@100"
        pattern = r'(\d*)#(\d+(?:\.\d+)?)(?:@(\d+(?:\.\d+)?))?'
        
        def convert_match(match):
            count_str, diameter_str, spacing_str = match.groups()
            
            # Convert diameter
            diameter = float(diameter_str)
            converted_diameter = self.converter.convert(diameter, 'Length', from_unit, to_unit)
            
            # Build result
            result = f"{'#' if not count_str else count_str + '#'}{converted_diameter:g}"
            
            # Convert spacing if present
            if spacing_str:
                spacing = float(spacing_str)
                converted_spacing = self.converter.convert(spacing, 'Length', from_unit, to_unit)
                result += f"@{converted_spacing:g}"
            
            return result
        
        # Replace all matches in the string
        converted = re.sub(pattern, convert_match, rebar_string)
        return converted
    
    def is_reinforcement_field(self, field_name: str) -> bool:
        """Check if a field contains reinforcement notation with embedded dimensions - DYNAMIC CHECK"""
        return '_reinf' in field_name


class FrescoDatabase:
    """Unified structural database - reinforcement fields work like any other field"""
    
    def __init__(self, db_name: str, field_config:Dict[str, Dict[str, Any]] = RCF_FIELD_CONFIG, empty_field_config:Dict[str, Dict[str, Any]] = RCF_DB_EMPTY_FIELDS, 
                 auto_save:bool=True, auto_back_up:bool=True, compress_db:bool=True,
                 show_conversion = True, show_invalid_object = True, show_invalid_unit = True):
        self.db_name = db_name
        self.auto_save = auto_save
        self.auto_back_up = auto_back_up
        self.compress_db = compress_db
        self.show_conversion = show_conversion
        self.show_invalid_object = show_invalid_object
        self.show_invalid_unit = show_invalid_unit

        self.data: Dict[int, Dict[str, Any]] = {}
        self.converter = FrescoUnits()
        self.reinforcement_parser = FrescoReinforcementParser(self.converter)
        
        # FLATTENED field mapping - ALL simple data types
        self.field_config = field_config
        self.empty_field_config = empty_field_config
        
        # Extract convenience mappings
        self.field_units = {field: config['unit'] for field, config in self.field_config.items()}
        self.field_unit_types = {field: config['unit_type'] for field, config in self.field_config.items() if config['unit_type']}
        
        self.version = "1.0"
        self.created_date = datetime.now().isoformat()
        self.last_modified = datetime.now().isoformat()
        
        self._load_if_exists()
        print(f"Database '{db_name}' initialized with {len(self.data)} entries")

        if self.data and self.auto_back_up:
            json_file = f"{self.db_name}.json"
            
            json_backup = self._create_backup(json_file)
            
            if json_backup:
                print(f"JSON backup: {json_backup}")
    
    def _create_backup(self, file_path: str) -> str:
        """Create timestamped backup - updated to handle both .json and .json.gz files"""
        if not os.path.exists(file_path):
            return ""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Handle different file extensions properly
        if file_path.endswith('.json.gz'):
            base_name = file_path.replace('.json.gz', '')
            backup_path = f"{base_name}_backup_{timestamp}.json.gz"
        elif file_path.endswith('.json'):
            base_name = file_path.replace('.json', '')
            backup_path = f"{base_name}_backup_{timestamp}.json"
        else:
            raise TypeError(".json or .json.gz are supported only!")
        
        shutil.copy2(file_path, backup_path)
        return backup_path

    def _load_if_exists(self):
        """Load existing database if JSON file exists"""
        # Try both compressed and uncompressed files
        json_file = f"{self.db_name}.json"
        json_file_gz = f"{self.db_name}.json.gz"
        
        db_data = None
        loaded_from = None
        
        # Try compressed first if compression is enabled
        if self.compress_db and os.path.exists(json_file_gz):
            try:
                with gzip.open(json_file_gz, 'rt', encoding='utf-8') as f:
                    db_data = json.load(f)
                loaded_from = json_file_gz
            except Exception as e:
                print(f"Error loading compressed database: {e}")
        
        # Try uncompressed if compressed failed or doesn't exist
        if db_data is None and os.path.exists(json_file):
            try:
                with open(json_file, 'r') as f:
                    db_data = json.load(f)
                loaded_from = json_file
            except Exception as e:
                print(f"Error loading database: {e}")
                return
        
        # Try compressed as fallback even if compression is disabled
        if db_data is None and os.path.exists(json_file_gz):
            try:
                with gzip.open(json_file_gz, 'rt', encoding='utf-8') as f:
                    db_data = json.load(f)
                loaded_from = json_file_gz
            except Exception as e:
                print(f"Error loading compressed database: {e}")
        
        if db_data:
            if "config" in db_data:
                config = db_data["config"]
                self.field_units = config.get("field_units", self.field_units)
                self.version = config.get("version", self.version)
                self.created_date = config.get("created_date", self.created_date)
                self.last_modified = config.get("last_modified", self.last_modified)
            
            if "data" in db_data:
                self.data = {int(k): v for k, v in db_data["data"].items()}
            
            print(f"Loaded existing database from {loaded_from}")

    def set_field_units(self, new_field_units: Dict[str, str]):
        """Set new field units and convert ALL existing data including reinforcement strings"""
        print(f"Updating field units configuration...")
        
        conversions_made = 0
        reinforcement_conversions = 0
        
        for entry_id, entry_data in self.data.items():
            for field_name, value in entry_data.items():
                
                # Handle regular numeric fields with unit conversion
                if (field_name in new_field_units and 
                    field_name in self.field_units and 
                    self.field_units[field_name] != new_field_units[field_name] and
                    isinstance(value, (int, float)) and
                    self.field_units[field_name] is not None and
                    new_field_units[field_name] is not None):
                    
                    old_unit = self.field_units[field_name]
                    new_unit = new_field_units[field_name]
                    unit_type = self.field_unit_types.get(field_name)
                    
                    if unit_type:
                        try:
                            converted_value = self.converter.convert(
                                value, unit_type, old_unit, new_unit
                            )
                            entry_data[field_name] = converted_value
                            conversions_made += 1
                            
                            if self.show_conversion:
                                print(f"  {field_name}: {value} {old_unit} -> {converted_value:.3f} {new_unit}")
                        except Exception as e:
                            print(f"  Warning: Could not convert {field_name}: {e}")
                
                # Handle reinforcement string fields (NOW USING HARDCODED LIST)
                elif (field_name in new_field_units and 
                      field_name in self.field_units and 
                      self.field_units[field_name] != new_field_units[field_name] and
                      isinstance(value, str) and 
                      self.reinforcement_parser.is_reinforcement_field(field_name)):
                    
                    old_unit = self.field_units[field_name]
                    new_unit = new_field_units[field_name]
                    
                    try:
                        converted_reinforcement = self.reinforcement_parser.parse_and_convert_reinforcement(
                            value, old_unit, new_unit
                        )
                        
                        if converted_reinforcement != value:
                            entry_data[field_name] = converted_reinforcement
                            reinforcement_conversions += 1
                            
                            if self.show_conversion:
                                print(f"  {field_name}: '{value}' -> '{converted_reinforcement}'")
                    except Exception as e:
                        print(f"  Warning: Could not convert reinforcement {field_name}: {e}")
        
        # Update field units configuration
        for field_name, new_unit in new_field_units.items():
            if field_name in self.field_units:
                self.field_units[field_name] = new_unit
        
        self.last_modified = datetime.now().isoformat()
                
        self.save()
    
    def _parse_and_convert_input_data(self, input_data: Dict[str, Any], show_error_fileds:bool = False) -> Dict[str, Any]:
        """
        Helper method to parse enhanced input format and convert units
        
        Handles both [value, unit] format and standard value format
        Returns converted data with progress reporting
        """
        # Parse enhanced input format [value, unit] and extract data + units
        converted_data = {}
        input_units = {}
        
        for field_name, field_input in input_data.items():
            if isinstance(field_input, (list, tuple)) and len(field_input) == 2:
                # Enhanced format: [value, unit]
                value, unit = field_input
                converted_data[field_name] = value
                input_units[field_name] = unit
            else:
                # Standard format: just value (use database default unit)
                converted_data[field_name] = field_input
        
        # Validation Rules - Remove invalid fields
        removed_fields = []
        for field_name, value in list(converted_data.items()):
            
            # Rule 1: Value Type Validation - remove type objects
            if isinstance(value, type):
                converted_data.pop(field_name, None)
                input_units.pop(field_name, None)
                if self.show_invalid_object:
                    removed_fields.append(f"{field_name} (type object '{value.__name__}')")
                continue
            
            # Rule 2: Unit Type Validation - remove wrong unit types
            if field_name in input_units and field_name in self.field_unit_types:
                provided_unit = input_units[field_name]
                expected_unit_type = self.field_unit_types[field_name]
                
                if expected_unit_type and provided_unit:
                    available_units = self.converter.get_available_units(expected_unit_type)
                    if provided_unit not in available_units:
                        converted_data.pop(field_name, None)
                        input_units.pop(field_name, None)
                        if self.show_invalid_unit:
                            removed_fields.append(f"{field_name} (invalid unit '{provided_unit}' for {expected_unit_type})")
        
        if removed_fields:
            print(f"  Removed {len(removed_fields)} invalid fields")
            if show_error_fileds:
                for item in removed_fields:
                    print(item)
        
        # End Validation Rules


        conversions_made = 0
        reinforcement_conversions = 0
        
        # Convert input data to database default units
        for field_name, value in converted_data.items():
            
            # Handle regular numeric fields
            if (isinstance(value, (int, float)) and 
                field_name in self.field_units and 
                self.field_units[field_name] is not None):
                
                input_unit = input_units.get(field_name, self.field_units[field_name])
                db_unit = self.field_units[field_name]
                unit_type = self.field_unit_types.get(field_name)
                
                if input_unit != db_unit and unit_type:
                    try:
                        converted_value = self.converter.convert(
                            value, unit_type, input_unit, db_unit
                        )
                        converted_data[field_name] = converted_value
                        conversions_made += 1
                        
                        if self.show_conversion:
                            print(f"  {field_name}: {value} {input_unit} -> {converted_value:.3f} {db_unit}")
                    except Exception as e:
                        print(f"  Warning: Could not convert {field_name}: {e}")
            
            # Handle reinforcement string conversion
            elif (isinstance(value, str) and 
                self.reinforcement_parser.is_reinforcement_field(field_name)):
                
                input_unit = input_units.get(field_name, self.field_units[field_name])
                db_unit = self.field_units[field_name]
                
                if input_unit != db_unit:
                    try:
                        converted_reinforcement = self.reinforcement_parser.parse_and_convert_reinforcement(
                            value, input_unit, db_unit
                        )
                        
                        if converted_reinforcement != value:
                            converted_data[field_name] = converted_reinforcement
                            reinforcement_conversions += 1
                            
                            if self.show_conversion:
                                print(f"  {field_name}: '{value}' -> '{converted_reinforcement}'")
                    except Exception as e:
                        print(f"  Warning: Could not convert reinforcement {field_name}: {e}")
        
        return converted_data

    def _reorder_entry_data(self, entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Reorder entry data to follow RCF_FIELD_CONFIG sequence
        
        Args:
            entry_data: Dictionary with field data in any order
            
        Returns:
            Dictionary with fields ordered according to RCF_FIELD_CONFIG
        """
        ordered_data = {}
        for field_name in self.field_config.keys():
            if field_name in entry_data:
                ordered_data[field_name] = entry_data[field_name]
        return ordered_data

    def add_entry(self, entry_id: int, entry_data: Dict[str, Any], overwrite: bool = False, show_error_fields: bool = False):
        """
        Add new entry with automatic unit conversion including reinforcement parsing
        
        Args:
            entry_id: Unique identifier for the entry
            entry_data: Data to add (supports [value, unit] format)
            overwrite: If True, allows overwriting existing entries
            show_error_fields: If True, shows detailed validation errors
        """
        # Check if entry already exists
        if entry_id in self.data and not overwrite:
            print(f"Error: Entry {entry_id} already exists!")
            print(f"Use overwrite=True to replace, or use update_entry() to modify specific fields")
            return False
        
        action = "Overwriting" if entry_id in self.data else "Adding"
        action_result = "overwritten" if entry_id in self.data else "added"
        print(f"{action} entry {entry_id}...")
        
        # Use existing conversion logic
        converted_data = self._parse_and_convert_input_data(entry_data, show_error_fields)

        # Fill missing fields with defaults from empty_field_config
        missing_fields = {}
        for field_name, default_value in self.empty_field_config.items():
            if field_name not in converted_data:
                missing_fields[field_name] = default_value
        
        if missing_fields:
            # Use the same conversion logic for missing fields
            converted_missing = self._parse_and_convert_input_data(missing_fields)
            converted_data.update(converted_missing)
            print(f"  Filled {len(missing_fields)} missing fields with defaults")

        # Create ordered dictionary following RCF_FIELD_CONFIG order
        converted_data = self._reorder_entry_data(converted_data)
        
        # Store the converted data (complete replacement)
        self.data[entry_id] = converted_data
        self.last_modified = datetime.now().isoformat()
        print(f"Entry {entry_id} {action_result} successfully")
        
        if self.auto_save:
            self.save()
        return True

    def update_entry(self, entry_id: int, updates: Dict[str, Any], show_error_fields: bool = False):
        """
        Update existing entry
        """
        if entry_id not in self.data:
            print(f"Entry {entry_id} not found in database")
            return False
        
        print(f"Updating entry {entry_id}...")
        
        # Use existing conversion logic
        converted_updates = self._parse_and_convert_input_data(updates, show_error_fields)
        
        # Update existing entry fields
        for field_name, field_value in converted_updates.items():
            self.data[entry_id][field_name] = field_value
        
        # Create ordered dictionary following RCF_FIELD_CONFIG order
        self.data[entry_id] = self._reorder_entry_data(self.data[entry_id])
        
        self.last_modified = datetime.now().isoformat()
        print(f"Entry {entry_id} updated successfully")
        
        if self.auto_save:
            self.save()
        return True
    
    def remove_entry(self, entry_id: int):
        """Remove entry with given ID"""
        if entry_id not in self.data:
            print(f"Entry {entry_id} not found in database")
            return False
        
        self.data.pop(entry_id)
        self.last_modified = datetime.now().isoformat()
        
        print(f"Entry {entry_id} removed successfully")
        
        if self.auto_save:
            self.save()
        return True
    
    def save(self):
        """Save database to JSON"""
        # Choose file extension based on compression setting
        if self.compress_db:
            json_file = f"{self.db_name}.json.gz"
        else:
            json_file = f"{self.db_name}.json"
        
        # Prepare database export
        db_export = {
            "config": {
                "field_units": self.field_units,
                "field_config": self.field_config,
                "version": self.version,
                "created_date": self.created_date,
                "last_modified": self.last_modified,
                "compressed": self.compress_db
            },
            "data": self.data,
            "total_entries": len(self.data)
        }
        
        # Save JSON (compressed or uncompressed)
        if self.compress_db:
            with gzip.open(json_file, 'wt', encoding='utf-8', compresslevel=6) as f:
                json.dump(db_export, f, indent=2)
        else:
            with open(json_file, 'w') as f:
                json.dump(db_export, f, indent=2)
              
        compression_info = " (compressed)" if self.compress_db else ""
        print(f"Database saved: {json_file}{compression_info} ({len(self.data)} entries)")
    
    def export_json(self, filename: Optional[str] = None, target_units: Optional[Dict[str, str]] = None):
        """Export database, optionally with different units"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_name = filename or f"{self.db_name}_export_{timestamp}"
        
        if target_units:
            # Convert data for export
            print(f"Exporting with custom units...")
            export_data = {}
            conversions_made = 0
            
            for entry_id, entry_data in self.data.items():
                converted_entry = copy.deepcopy(entry_data)
                
                for field_name, value in converted_entry.items():
                    if (field_name in target_units and 
                        isinstance(value, (int, float)) and
                        field_name in self.field_units and
                        self.field_units[field_name] is not None):
                        
                        db_unit = self.field_units[field_name]
                        target_unit = target_units[field_name]
                        unit_type = self.field_unit_types.get(field_name)
                        
                        if db_unit != target_unit and unit_type:
                            try:
                                converted_value = self.converter.convert(
                                    value, unit_type, db_unit, target_unit
                                )
                                converted_entry[field_name] = converted_value
                                conversions_made += 1
                            except Exception as e:
                                print(f"  Warning: Could not convert {field_name}: {e}")
                
                export_data[entry_id] = converted_entry
            
            # Create temporary database for export with same compression setting
            temp_db = FrescoDatabase(f"temp_{export_name}", 
                                            auto_save=False, 
                                            auto_back_up=False,
                                            compress_db=self.compress_db)
            temp_db.data = export_data
            temp_db.field_units = {**self.field_units, **target_units}
            temp_db.save()
            
            # Rename files with proper extensions
            json_ext = ".json.gz" if self.compress_db else ".json"
            os.rename(f"temp_{export_name}{json_ext}", f"{export_name}{json_ext}")
            
            print(f"Exported with {conversions_made} unit conversions")
        else:
            # Simple export with current units - copy correct file format
            json_ext = ".json.gz" if self.compress_db else ".json"
            source_json = f"{self.db_name}{json_ext}"
            target_json = f"{export_name}{json_ext}"
            
            shutil.copy2(source_json, target_json)
        
        json_ext = ".json.gz" if self.compress_db else ".json"
        compression_info = " (compressed)" if self.compress_db else ""
        print(f"Database exported: {export_name}{json_ext}{compression_info}")
        
    def get_info(self) -> Dict[str, Any]:
        """Get database information"""
        # Count fields by unit type
        unit_summary = {}
        reinforcement_fields = [field for field in self.field_config.keys() if '_reinf' in field]
        
        for field_name, unit in self.field_units.items():
            if unit is not None:
                unit_type = self.field_unit_types.get(field_name, "Other")
                if unit_type not in unit_summary:
                    unit_summary[unit_type] = {}
                if unit not in unit_summary[unit_type]:
                    unit_summary[unit_type][unit] = 0
                unit_summary[unit_type][unit] += 1
        
        return {
            "database_name": self.db_name,
            "total_entries": len(self.data),
            "total_fields": len(self.field_config),
            "fields_with_units": len([u for u in self.field_units.values() if u is not None]),
            "reinforcement_fields": len(reinforcement_fields),
            "version": self.version,
            "created": self.created_date,
            "last_modified": self.last_modified,
            "unit_summary": unit_summary,
            "available_unit_types": list(self.converter.get_unit_types()),
            "dynamic_reinforcement_fields": reinforcement_fields[:10]  # Show first 10
        }

    def export_to_csv(self, filename: Optional[str] = None, target_units: Optional[Dict[str, str]] = None, 
                    include_units_header: bool = True, selected_fields: Optional[List[str]] = None) -> str:
        """
        Export database to CSV format with optional unit conversion
        
        Args:
            filename: Optional custom filename (without extension)
            target_units: Dictionary of field_name -> target_unit for conversion
            include_units_header: If True, adds a second header row with units
            selected_fields: Optional list of fields to export (if None, exports all)
        
        Returns:
            str: The filename of the exported CSV
        """
        if not self.data:
            print("Warning: No data to export")
            return ""
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = filename or f"{self.db_name}_export_{timestamp}"
        if not csv_filename.endswith('.csv'):
            csv_filename += '.csv'
        
        print(f"Exporting to CSV: {csv_filename}")
        
        # Prepare data for export
        export_data = {}
        conversions_made = 0
        reinforcement_conversions = 0
        
        # Convert data if target_units specified
        if target_units:
            print(f"Converting units for CSV export...")
            
            for entry_id, entry_data in self.data.items():
                converted_entry = copy.deepcopy(entry_data)
                
                for field_name, value in converted_entry.items():
                    if field_name in target_units:
                        target_unit = target_units[field_name]
                        
                        # Handle numeric field conversion
                        if (isinstance(value, (int, float)) and 
                            field_name in self.field_units and
                            self.field_units[field_name] is not None):
                            
                            db_unit = self.field_units[field_name]
                            unit_type = self.field_unit_types.get(field_name)
                            
                            if db_unit != target_unit and unit_type:
                                try:
                                    converted_value = self.converter.convert(
                                        value, unit_type, db_unit, target_unit
                                    )
                                    converted_entry[field_name] = converted_value
                                    conversions_made += 1
                                except Exception as e:
                                    print(f"  Warning: Could not convert {field_name}: {e}")
                        
                        # Handle reinforcement string conversion
                        elif (isinstance(value, str) and 
                            self.reinforcement_parser.is_reinforcement_field(field_name)):
                            
                            db_unit = self.field_units[field_name]
                            
                            if db_unit != target_unit:
                                try:
                                    converted_reinforcement = self.reinforcement_parser.parse_and_convert_reinforcement(
                                        value, db_unit, target_unit
                                    )
                                    
                                    if converted_reinforcement != value:
                                        converted_entry[field_name] = converted_reinforcement
                                        reinforcement_conversions += 1
                                except Exception as e:
                                    print(f"  Warning: Could not convert reinforcement {field_name}: {e}")
                
                export_data[entry_id] = converted_entry
            
            if conversions_made > 0:
                print(f"  Converted {conversions_made} numeric values")
            if reinforcement_conversions > 0:
                print(f"  Converted {reinforcement_conversions} reinforcement strings")
        else:
            export_data = self.data
        
        # Determine fields to export - UPDATED: Use RCF_FIELD_CONFIG order
        if selected_fields:
            # Validate selected fields exist and maintain RCF_FIELD_CONFIG order
            all_fields = set()
            for entry_data in export_data.values():
                all_fields.update(entry_data.keys())
            
            invalid_fields = [f for f in selected_fields if f not in all_fields]
            if invalid_fields:
                print(f"Warning: Unknown fields ignored: {invalid_fields}")
            
            # Maintain RCF_FIELD_CONFIG order for selected fields
            fields_to_export = []
            for field_name in self.field_config.keys():
                if field_name in selected_fields and field_name in all_fields:
                    fields_to_export.append(field_name)
        else:
            # Get all fields that exist in data, ordered by RCF_FIELD_CONFIG
            all_fields = set()
            for entry_data in export_data.values():
                all_fields.update(entry_data.keys())
            
            fields_to_export = []
            for field_name in self.field_config.keys():
                if field_name in all_fields:
                    fields_to_export.append(field_name)
        
        if not fields_to_export:
            print("Error: No valid fields to export")
            return ""
        
        # Write CSV file
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header row with field names
            header = ['entry_id'] + fields_to_export
            writer.writerow(header)
            
            # Write units header if requested
            if include_units_header:
                units_row = ['ID']  # First column for entry_id
                for field_name in fields_to_export:
                    if target_units and field_name in target_units:
                        unit = target_units[field_name]
                    elif field_name in self.field_units:
                        unit = self.field_units[field_name]
                    else:
                        unit = ''
                    units_row.append(unit or '')
                writer.writerow(units_row)
            
            # Write data rows
            for entry_id in sorted(export_data.keys()):
                entry_data = export_data[entry_id]
                row = [entry_id]
                
                for field_name in fields_to_export:
                    value = entry_data.get(field_name, '')
                    
                    # Handle different data types for CSV
                    if isinstance(value, (list, dict)):
                        # Convert complex types to string representation
                        row.append(str(value))
                    elif value is None:
                        row.append('')
                    else:
                        row.append(value)
                
                writer.writerow(row)
        
        # Print summary
        total_exported = len(export_data)
        fields_exported = len(fields_to_export)
        
        print(f"CSV export completed:")
        print(f"  File: {csv_filename}")
        print(f"  Entries: {total_exported}")
        print(f"  Fields: {fields_exported}")
        if include_units_header:
            print(f"  Units header: included")
        if selected_fields:
            print(f"  Selected fields: {len(selected_fields)} requested, {fields_exported} valid")
        
        return csv_filename
