import FreeCAD
import Part
import os
from src.database_editor import FrescoDatabase

# USER Configuration
DATABASE_FOLDER_PATH = "Database/"
CAD_FOLDER_PATH = "Models/"
DATABASE_NAME = "fresco_v1"
DATABASE_ENTRY_ID = 1
MODEL_NAME = None

class PPEEFrameGenerator:
    """Base class for linear frame generation"""
    
    def __init__(self, database_folder_path, cad_folder_path, database_name, 
                 database_entry_id, model_name=None):
        self.database_folder_path = database_folder_path
        self.cad_folder_path = cad_folder_path
        self.database_name = database_name
        self.database_entry_id = database_entry_id
        self.model_name = model_name or f"LINEAR_MODEL_ID{database_entry_id}"
        
    def generate_frame(self):
        """Generate the linear frame based on database entry"""
        # Create Models folder if it doesn't exist
        if not os.path.exists(self.cad_folder_path):
            os.makedirs(self.cad_folder_path)

        # Access Database
        db = FrescoDatabase(
            self.database_folder_path + self.database_name,
            compress_db=False,
            auto_back_up=False,
            show_invalid_object=False
        )
        doc = FreeCAD.newDocument(self.model_name)
        db_entry = db.data[self.database_entry_id]

        # Extract dimensions
        frm_h = db_entry["frm_h"]
        frm_l = db_entry["frm_l"]
        col_h = db_entry["col_h"]
        bm_h = db_entry["bm_h"]
        bbm_h = db_entry.get("bbm_h", 0)
        col_ext = db_entry.get("col_ext", 0)
        bm_ext = db_entry.get("bm_ext", 0)
        bbm_ext = db_entry.get("bbm_ext", 0)

        # Calculate positions
        frm_in_l = frm_l - 2 * col_h
        frm_in_h = frm_h - bm_h
        col_center_x = col_h / 2.0
        bm_center_y = frm_in_h + bm_h / 2.0

        # Collect all line shapes
        line_shapes = []

        # Base beam
        if bbm_h > 0:
            bbm_center_y = -bbm_h / 2.0
            n1 = FreeCAD.Vector(-col_h - bbm_ext, bbm_center_y, 0)
            n2 = FreeCAD.Vector(-col_center_x, bbm_center_y, 0)
            n3 = FreeCAD.Vector(frm_in_l + col_center_x, bbm_center_y, 0)
            n4 = FreeCAD.Vector(frm_in_l + col_h + bbm_ext, bbm_center_y, 0)
            
            line_shapes.append(Part.makeLine(n1, n2))
            line_shapes.append(Part.makeLine(n2, n3))
            line_shapes.append(Part.makeLine(n3, n4))
            
            col_base_left = n2
            col_base_right = n3
        else:
            col_base_left = FreeCAD.Vector(-col_center_x, 0, 0)
            col_base_right = FreeCAD.Vector(frm_in_l + col_center_x, 0, 0)

        # Beam-column joints
        col_top_left = FreeCAD.Vector(-col_center_x, bm_center_y, 0)
        col_top_right = FreeCAD.Vector(frm_in_l + col_center_x, bm_center_y, 0)

        # Columns
        line_shapes.append(Part.makeLine(col_base_left, col_top_left))
        line_shapes.append(Part.makeLine(col_base_right, col_top_right))

        # Column extensions
        if col_ext > 0:
            col_top_ext_left = FreeCAD.Vector(-col_center_x, frm_in_h + bm_h + col_ext, 0)
            col_top_ext_right = FreeCAD.Vector(frm_in_l + col_center_x, frm_in_h + bm_h + col_ext, 0)
            line_shapes.append(Part.makeLine(col_top_left, col_top_ext_left))
            line_shapes.append(Part.makeLine(col_top_right, col_top_ext_right))

        # Beam
        if bm_ext > 0:
            beam_left = FreeCAD.Vector(-col_h - bm_ext, bm_center_y, 0)
            beam_right = FreeCAD.Vector(frm_in_l + col_h + bm_ext, bm_center_y, 0)
            line_shapes.append(Part.makeLine(beam_left, col_top_left))
            line_shapes.append(Part.makeLine(col_top_left, col_top_right))
            line_shapes.append(Part.makeLine(col_top_right, beam_right))
        else:
            line_shapes.append(Part.makeLine(col_top_left, col_top_right))

        # Create compound and add to document
        compound = Part.makeCompound(line_shapes)
        compound_obj = doc.addObject("Part::Feature", "LinearFrame")
        compound_obj.Shape = compound
        doc.recompute()

        # Export to DXF using importDXF module
        export_filename = f"{self.model_name}.dxf"
        export_path = os.path.join(self.cad_folder_path, export_filename)
        export_path_abs = os.path.abspath(export_path)

        try:
            # Import the DXF export module
            import importDXF
            
            # Export using importDXF
            importDXF.export([compound_obj], export_path)
            
            # Verify file was created
            if os.path.exists(export_path):
                file_size = os.path.getsize(export_path)
                print(f"✓ SUCCESS! DXF file created:")
                print(f"  Path: {export_path_abs}")
                print(f"  Size: {file_size} bytes")
                print(f"  Elements: {len(line_shapes)} lines")
            else:
                print(f"✗ ERROR: File not found after export")
                print(f"  Expected: {export_path_abs}")
                
        except ImportError:
            print(f"✗ ERROR: importDXF module not available")
            print(f"  Install DXF libraries from Edit > Preferences > Import-Export > DXF")
            print(f"  Or enable 'Allow FreeCAD to automatically download DXF libraries'")
        except Exception as e:
            print(f"✗ ERROR during export: {str(e)}")
            print(f"  Path: {export_path_abs}")
            