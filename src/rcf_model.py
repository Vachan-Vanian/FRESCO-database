import re
import math
import FreeCAD
import Part
import Import
from typing import Union, Tuple, List, Any, Optional
from src.database_editor import FrescoDatabase


class RCFrameGenerator:
    def __init__(self, database_folder_path="Database/", cad_folder_path="Models/", database_name="fresco_v1", compress_db=False):
        self.DATABASE_FOLDER_PATH = database_folder_path
        self.CAD_FOLDER_PATH = cad_folder_path
        self.DATABASE_NAME = database_name
        self.DATABASE_ENTRY_ID = None
        
        # Initialize database and document
        self.db = FrescoDatabase(self.DATABASE_FOLDER_PATH + self.DATABASE_NAME, 
                                 auto_save = False, auto_back_up = False, compress_db = compress_db, 
                                 show_conversion = False, show_invalid_object = False, show_invalid_unit = False)

        self.converter = self.db.converter
        self.db_length_unit = self._get_db_length_unit()


    def _get_db_length_unit(self) -> str:
        """Get primary length unit from database"""
        length_fields = ['frm_h', 'frm_l', 'col_h', 'col_d']
        for field in length_fields:
            if field in self.db.field_units:
                return self.db.field_units[field]
        return 'mm'  # fallback
    
    def _parse_dimension(self, value: Union[float, Tuple[float, str], List], 
                       default_unit: str = None) -> float:
        """
        Parse dimension with optional unit specification
        
        Args:
            value: Can be:
                - float/int: 300 (uses database default unit)
                - tuple/list: [300, 'mm'] (converts from mm to database unit)
            default_unit: Unit to assume if none specified (default: database unit)
        
        Returns:
            float: Value in database units
        """
        if default_unit is None:
            default_unit = self.db_length_unit
            
        # Handle [value, unit] format
        if isinstance(value, (list, tuple)) and len(value) == 2:
            val, unit = value
            if unit != self.db_length_unit:
                return self.converter.convert(val, 'Length', unit, self.db_length_unit)
            return float(val)
        
        # Handle plain number (assume default_unit)
        elif isinstance(value, (int, float)):
            if default_unit != self.db_length_unit:
                return self.converter.convert(value, 'Length', default_unit, self.db_length_unit)
            return float(value)
        
        else:
            raise ValueError(f"Invalid dimension format: {value}")

    def _cad_create_part(self, label):
        """Create a new part object"""
        tmp_comp_obj = self.doc.addObject("App::Part")
        tmp_comp_obj.Label = label
        return tmp_comp_obj

    def _cad_add_shape_to_feature_to_part(self, label, part_shape_obj, comp_obj):
        """Add a shape to a part assembly"""
        tmp_part_obj = self.doc.addObject("Part::Feature")
        tmp_part_obj.Shape = part_shape_obj
        tmp_part_obj.Label = label
        comp_obj.addObject(tmp_part_obj)
        return tmp_part_obj

    def _parse_reinforcement_string(self, rebar_string):
        """
        Parse reinforcement notation like '4#20+2#16' or '2#8@150'
        Returns list of (count, diameter, spacing) tuples
        """
        if not rebar_string or rebar_string == "":
            return []
        
        # Split by '+' for compound reinforcement
        parts = rebar_string.split('+')
        reinforcement = []
        
        for part in parts:
            part = part.strip()
            
            # Pattern for reinforcement: optional count + # + diameter + optional @spacing
            pattern = r'(\d*)#(\d+(?:\.\d+)?)(?:@(\d+(?:\.\d+)?))?'
            match = re.match(pattern, part)
            
            if match:
                count_str, diameter_str, spacing_str = match.groups()
                count = int(count_str) if count_str else 1
                diameter = float(diameter_str)
                spacing = float(spacing_str) if spacing_str else None
                reinforcement.append((count, diameter, spacing))
        
        return reinforcement

    def _transverse_reinforcement(self, type, cs_dimx, cs_dimz, cover, reinf_d, translate=(0,0,0), rot_x=0, rot_y=0, rot_z=0):
        """
        Create transverse reinforcement shape
        """
        w = cs_dimz - 2*cover - reinf_d
        d = cs_dimx - 2*cover - reinf_d

        if type == "rect":
            points = [
                FreeCAD.Vector(0, 0, 0),
                FreeCAD.Vector(d, 0, 0),
                FreeCAD.Vector(d, 0, w),
                FreeCAD.Vector(0, 0, w),
                FreeCAD.Vector(0, 0, 0)
            ]
        elif type =="diamond":
            points = [
                FreeCAD.Vector(d/2, 0, 0),
                FreeCAD.Vector(d, 0, w/2),
                FreeCAD.Vector(d/2, 0, w),
                FreeCAD.Vector(0, 0, w/2),
                FreeCAD.Vector(d/2, 0, 0),
            ]
        else:
            raise ValueError("Stirrup type must be 'rect' or 'diamond'")

        trans_reinf_shape = Part.makePolygon(points)

        if rot_x!= 0:
            trans_reinf_shape.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), rot_x)
        if rot_y!= 0:
            trans_reinf_shape.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), rot_y)
        if rot_z!= 0:
            trans_reinf_shape.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), rot_z)
        
        tx,ty,tz = translate
        trans_reinf_shape.translate(FreeCAD.Vector(tx,ty,tz))

        return trans_reinf_shape

    def _longitudinal_reinforcement(self, elem_l, elm1_cover, elm1_transv_reinf, elm2_cover, elm2_transv_reinf, translate=(0,0,0), rot_x=0, rot_y=0, rot_z=0):
        """
        Create longitudinal reinforcement shape
        """
        points = [
            FreeCAD.Vector(0, 0, 0),
            FreeCAD.Vector(0, elem_l -elm1_cover -elm1_transv_reinf/2 -elm2_cover -elm2_transv_reinf/2, 0),
        ]
        long_reinf_shape = Part.makePolygon(points)
        if rot_x!= 0:
            long_reinf_shape.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), rot_x)
        if rot_y!= 0:
            long_reinf_shape.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), rot_y)
        if rot_z!= 0:
            long_reinf_shape.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), rot_z)
        
        tx,ty,tz = translate
        long_reinf_shape.translate(FreeCAD.Vector(tx,ty,tz))

        return long_reinf_shape

    def _create_copied_shapes(self, base_shape, axis, spacing, length, assembly_obj, start_label, start_number, add_base_shape=True, add_last_element=True, use_rounding=False):
        """
        Creates repeated copies of a base shape along a specified axis with auto-labeling.
        
        Parameters:
            base_shape: Part.Shape - the original shape to copy
            axis: tuple 
            spacing: float - distance between each copy
            length: float - total length to replicate over
            assembly_obj - Assembly Object to serve as container cad_create_part() function
            start_label: str - base label name
            start_number: int - starting number for labeling
            
        Returns:
            tuple: (assembly_object, next label number)
        """
        
        # Normalize axis vector
        axis_vec = FreeCAD.Vector(axis)
        
        # Calculate number of copies needed
        if spacing <= 0:
            raise ValueError("Spacing must be positive")
        
        if use_rounding:
            num_reps = int((length / spacing) + 0.5) + 1  # Round for uniform spacing
        else:
            num_reps = int(length // spacing) + 1  # Floor to stay within bounds
        
        # Check if assembly object is ok
        if not hasattr(assembly_obj, 'TypeId') or assembly_obj.TypeId != 'App::Part':
            raise ValueError("Provided assembly_obj must be an App::Part object")
        
        # List to store feature objects
        feature_objects = []
        
        # Create each copy with auto-labeling
        if add_base_shape==True:
            start = 0
        else:
            start = 1

        if add_last_element == True:
            end = num_reps
        else:
            end = num_reps - 1
        
        for i in range(start, end, 1):
            offset_vec = axis_vec * (i * spacing)
            new_shape = base_shape.copy()
            new_shape.translate(offset_vec)
            
            # Auto-generate label
            if add_base_shape==True:
                label = f"{start_label}_{start_number + i}"
            else:
                label = f"{start_label}_{start_number + i-1}"
            
            # Add to assembly
            
            feature_obj = self._cad_add_shape_to_feature_to_part(label=label, part_shape_obj=new_shape, comp_obj=assembly_obj)
            feature_objects.append(feature_obj)
        
        return feature_objects, start_number+len(feature_objects)

    def _create_infill_first_row(self, inf_ul, inf_uh, inf_ut, row_height):
        inf_bnd_pat = self.inf_bnd_pat
        inf_interface_left = self.inf_interface_left
        inf_dp = self.inf_dp
        inf_uhead_t = self.inf_uhead_t
        inf_l = self.inf_l

        list_bricks = []
        if inf_bnd_pat == "running" or inf_bnd_pat == "stack":
            brickr1_shape = Part.makeBox(inf_ul, inf_uh, inf_ut)
            brickr1_shape.translate(FreeCAD.Vector(inf_interface_left, row_height, -inf_ut))
            brickr1_shape.translate(FreeCAD.Vector(0,0, inf_dp))

            temp_obj, self.brick_num = self._create_copied_shapes(brickr1_shape, (1,0,0), inf_ul+inf_uhead_t, inf_l-(inf_ul+inf_uhead_t), 
                                self.infill_assembly, "Brick", self.brick_num, add_base_shape=True, add_last_element=True)
            list_bricks.extend(temp_obj)

            num_brick_gen = len(temp_obj)
            brk1_last_l = inf_l - (num_brick_gen*inf_ul) - (num_brick_gen*inf_uhead_t)
            brickr1_last_locationx = inf_interface_left + (num_brick_gen*inf_ul) + (num_brick_gen*inf_uhead_t) 
            if brk1_last_l>0:
                brickr1_last = Part.makeBox(brk1_last_l, inf_uh, inf_ut)
                brickr1_last.translate(FreeCAD.Vector(brickr1_last_locationx, row_height, -inf_ut))
                brickr1_last.translate(FreeCAD.Vector(0,0, inf_dp))

                temp_obj=self._cad_add_shape_to_feature_to_part(f"Brick_{self.brick_num}", brickr1_last, self.infill_assembly)
                list_bricks.extend([temp_obj])
                self.brick_num = self.brick_num+1
        return list_bricks

    def _create_infill_second_row(self, inf_ul, inf_uh, inf_ut, row_height):

        inf_bnd_pat = self.inf_bnd_pat
        inf_uhead_t = self.inf_uhead_t
        inf_interface_left = self.inf_interface_left
        inf_dp = self.inf_dp
        inf_l = self.inf_l


        list_bricks = []
        if inf_bnd_pat == "running":
            brickr21_shape = Part.makeBox(inf_ul/2-inf_uhead_t/2, inf_uh, inf_ut)
            brickr21_shape.translate(FreeCAD.Vector(inf_interface_left, row_height, -inf_ut))
            brickr21_shape.translate(FreeCAD.Vector(0,0, inf_dp))
            temp_obj=self._cad_add_shape_to_feature_to_part(f"Brick_{self.brick_num}", brickr21_shape, self.infill_assembly)
            list_bricks.extend([temp_obj])
            self.brick_num = self.brick_num+1

            brickr22_shape = Part.makeBox(inf_ul, inf_uh, inf_ut)
            brickr22_location = inf_interface_left+(inf_ul/2-inf_uhead_t/2)+inf_uhead_t
            brickr22_shape.translate(FreeCAD.Vector(brickr22_location, row_height, -inf_ut))
            brickr22_shape.translate(FreeCAD.Vector(0,0, inf_dp))
            temp_obj=self._cad_add_shape_to_feature_to_part(f"Brick_{self.brick_num}", brickr22_shape, self.infill_assembly)
            list_bricks.extend([temp_obj])
            self.brick_num = self.brick_num+1
            
            
            temp_obj, self.brick_num = self._create_copied_shapes(brickr22_shape, (1,0,0), inf_ul+inf_uhead_t, inf_l-(inf_ul+inf_uhead_t+brickr22_location), 
                                self.infill_assembly, "Brick", self.brick_num, add_base_shape=False, add_last_element=True)
            list_bricks.extend(temp_obj)
            
            num_brick_gen = len(temp_obj)
            brickr23_location = brickr22_location + inf_ul + inf_uhead_t
            brickr2_last_locationx = brickr23_location + (num_brick_gen*inf_ul) + (num_brick_gen*inf_uhead_t) 
            brk2_last_l = inf_l + inf_interface_left - brickr2_last_locationx
            if brk2_last_l>0:
                brickr2_last = Part.makeBox(brk2_last_l, inf_uh, inf_ut)
                brickr2_last.translate(FreeCAD.Vector(brickr2_last_locationx, row_height, -inf_ut))
                brickr2_last.translate(FreeCAD.Vector(0,0, inf_dp))

                temp_obj=self._cad_add_shape_to_feature_to_part(f"Brick_{self.brick_num}", brickr2_last, self.infill_assembly)
                list_bricks.extend([temp_obj])
                self.brick_num = self.brick_num+1
        elif inf_bnd_pat == "stack":
            # Stack bond - identical to first row, so just call the first row function
            list_bricks = self._create_infill_first_row(inf_ul, inf_uh, inf_ut, row_height)

        return list_bricks

    def _create_frame_geometry(self):
        """
        Generate frame geometry based on database entries
        """
        # Extract dimensions
        frm_h = self.frm_h = self.db_entry["frm_h"]
        frm_l = self.frm_l = self.db_entry["frm_l"]
        col_h = self.col_h = self.db_entry["col_h"]
        col_d = self.col_d = self.db_entry["col_d"]
        bm_h = self.bm_h = self.db_entry["bm_h"]
        bm_t = self.bm_t = self.db_entry["bm_t"]
        bbm_h = self.bbm_h = self.db_entry["bbm_h"]
        bbm_t = self.bbm_t = self.db_entry["bbm_t"]
        slb_d = self.slb_d = self.db_entry["slb_d"]
        slb_h = self.slb_h = self.db_entry["slb_h"]
        col_ext = self.col_ext = self.db_entry["col_ext"]
        bm_ext = self.bm_ext = self.db_entry["bm_ext"]
        bbm_ext = self.bbm_ext = self.db_entry["bbm_ext"]


        # Validate that critical dimensions are positive (> 0)
        if not(frm_h>0 and frm_l>0 and col_h>0 and col_d>0 and bm_h>0 and bm_t>0):
            raise ValueError("Critical frame dimensions (frm_h, frm_l, col_h, col_d, bm_h, bm_t) must be positive")

        # Validate that other dimensions are non-negative (>= 0)
        if not(bbm_h>=0 and bbm_t>=0 and slb_d>=0 and slb_h>=0 and col_ext>=0 and bm_ext>=0 and bbm_ext>=0):
            raise ValueError("Other dimensions (bbm_h, bbm_t, slb_d, slb_h, col_ext, bm_ext, bbm_ext) must not be negative")

        # Calculate dimensions
        col_tot_h = self.col_tot_h = col_ext + frm_h + bbm_h
        frm_in_l = self.frm_in_l = frm_l - 2*col_h
        frm_in_h = self.frm_in_h = frm_h - bm_h
        bm_tot_l = self.bm_tot_l = 2*bm_ext + frm_l
        bbm_tot_l = self.bbm_tot_l = 2*bbm_ext + frm_l

        # Validate that calculated dimensions are positive
        if not(col_tot_h>0 and frm_in_l>0 and frm_in_h>0 and bm_tot_l>0 and bbm_tot_l>0):
            raise ValueError("Calculated dimensions (col_tot_h, frm_in_l, frm_in_h, bm_tot_l, bbm_tot_l) must be positive")

        # Create individual shapes (not features yet)
        rc_frame_shapes = []

        # left column
        left_column_shape = Part.makeBox(col_h, col_tot_h, col_d)
        left_column_shape.translate(FreeCAD.Vector(-col_h, -bbm_h, -col_d/2))
        rc_frame_shapes.append(left_column_shape)

        # right column
        right_column_shape = Part.makeBox(col_h, col_tot_h, col_d)
        right_column_shape.translate(FreeCAD.Vector(frm_in_l, -bbm_h, -col_d/2))
        rc_frame_shapes.append(right_column_shape)

        # beam
        beam_shape = Part.makeBox(bm_tot_l, bm_h, bm_t)
        beam_shape.translate(FreeCAD.Vector(-bm_ext-col_h, frm_in_h, -bm_t/2))
        rc_frame_shapes.append(beam_shape)

        # base_beam
        if bbm_h>0 and bbm_t>0:
            base_beam_shape = Part.makeBox(bbm_tot_l, bbm_h, bbm_t)
            base_beam_shape.translate(FreeCAD.Vector(-bbm_ext-col_h, -bbm_h, -bbm_t/2))
            rc_frame_shapes.append(base_beam_shape)

        # slab
        if slb_h>0 and slb_d>0:
            slab_shape = Part.makeBox(bm_tot_l, slb_h, slb_d)
            slab_shape.translate(FreeCAD.Vector(-bm_ext-col_h, frm_in_h+(bm_h-slb_h), -slb_d/2))
            rc_frame_shapes.append(slab_shape)

        # Fuse all shapes together
        fused_rc_frame_shape = left_column_shape.fuse(rc_frame_shapes)

        # Create assembly and add single fused part
        self.rc_frame_assembly = self._cad_create_part(label="RC_Frame_Assembly")
        fused_rc_frame = self._cad_add_shape_to_feature_to_part(label="Fused_RC_Frame", part_shape_obj=fused_rc_frame_shape, comp_obj=self.rc_frame_assembly)

    def _create_reinforcement(self):

        #### RETRIEVE DATA ####
        frm_h = self.frm_h
        frm_l = self.frm_l
        col_h = self.col_h
        col_d = self.col_d
        bm_h = self.bm_h
        bm_t = self.bm_t
        bbm_h = self.bbm_h
        bbm_t = self.bbm_t
        slb_d = self.slb_d
        slb_h = self.slb_h
        col_ext = self.col_ext
        bm_ext = self.bm_ext
        bbm_ext = self.bbm_ext

        col_tot_h = self.col_tot_h
        frm_in_l = self.frm_in_l
        frm_in_h = self.frm_in_h
        bm_tot_l = self.bm_tot_l
        bbm_tot_l = self.bbm_tot_l 
        #### RETRIEVE DATA ####


        ##################################################################
        # ========= TRANSVERSE REINFORCEMENT COLUMNS ===========
        ##################################################################
        self.reinf_left_column_assembly = self._cad_create_part(label="Left_Column_Reinforcement_Assembly")

        col_trans_crit_top_distance = self.db_entry["col_trans_crit_top_distance"]
        col_trans_crit_top_reinf = self.db_entry["col_trans_crit_top_reinf"]
        col_trans_crit_bot_distance = self.db_entry["col_trans_crit_bot_distance"]
        col_trans_crit_bot_reinf = self.db_entry["col_trans_crit_bot_reinf"]
        col_trans_mid_reinf = self.db_entry["col_trans_mid_reinf"]
        col_cover = self.db_entry["col_cover"]

        # Check if col_cover is positive
        if col_cover <= 0:
            raise ValueError("col_cover must be a positive value")

        col_crit_top_reinf_data = self._parse_reinforcement_string(col_trans_crit_top_reinf)
        col_crit_bot_reinf_data = self._parse_reinforcement_string(col_trans_crit_bot_reinf)
        col_mid_reinf_data = self._parse_reinforcement_string(col_trans_mid_reinf)

        # Check if any variable is empty
        if not col_crit_top_reinf_data or not col_crit_bot_reinf_data or not col_mid_reinf_data:
            raise ValueError("Some column transverse reinforcement are incorrect!")
        else:
            col_crit_bot_reinf_n, col_crit_bot_creinf_d, col_crit_bot_creinf_s = col_crit_bot_reinf_data[0]
            col_crit_top_reinf_n, col_crit_top_creinf_d, col_crit_top_creinf_s  = col_crit_top_reinf_data[0]
            col_mid_reinf_n, col_mid_creinf_d, col_mid_creinf_s  = col_mid_reinf_data[0]

            col_crit_bot_creinf_d = col_crit_top_creinf_d = col_mid_creinf_d = max(col_crit_bot_creinf_d, col_crit_top_creinf_d, col_mid_creinf_d )

            if col_crit_bot_reinf_n==0:
                col_crit_bot_creinf_s =  col_mid_creinf_s

            if col_crit_top_reinf_n==0:
                col_crit_top_creinf_s =  col_mid_creinf_s
            
            if col_mid_reinf_n == col_crit_bot_reinf_n == col_crit_top_reinf_n ==0:
                print("Warning: No transverse reinforcement exist in columns!")

            lcol_num=1
            list_left_column_tranv_reinf = []


            if col_crit_bot_reinf_n>0:
                col_reinf_w = col_h - 2*col_cover - col_crit_bot_creinf_d
                col_reinf_d= col_d - 2*col_cover - col_crit_bot_creinf_d
                left_column_reinf_shape_bot = self._transverse_reinforcement("rect", col_h, col_d, col_cover, col_crit_bot_creinf_d, (-col_reinf_w-col_cover-col_crit_bot_creinf_d/2, 0, -col_reinf_d/2))
                left_column_BOT, lcol_num = self._create_copied_shapes(left_column_reinf_shape_bot, (0,1,0), col_crit_bot_creinf_s, col_trans_crit_bot_distance, self.reinf_left_column_assembly, "Left_Column_Reinf", lcol_num)
                list_left_column_tranv_reinf.extend(left_column_BOT)

            if col_crit_top_reinf_n>0:
                col_reinf_w = col_h - 2*col_cover - col_crit_top_creinf_d
                col_reinf_d= col_d - 2*col_cover - col_crit_top_creinf_d
                left_column_reinf_shape_top = self._transverse_reinforcement("rect", col_h, col_d, col_cover, col_crit_top_creinf_d, (-col_reinf_w-col_cover-col_crit_top_creinf_d/2, frm_in_h, -col_reinf_d/2))
                left_column_TOP, lcol_num = self._create_copied_shapes(left_column_reinf_shape_top, (0,-1,0), col_crit_top_creinf_s, col_trans_crit_top_distance, self.reinf_left_column_assembly, "Left_Column_Reinf", lcol_num)
                list_left_column_tranv_reinf.extend(left_column_TOP)

            if col_mid_reinf_n>0:
                col_mid_reinf_distance_half= (frm_in_h - col_trans_crit_bot_distance - col_trans_crit_top_distance)/2
                col_mid_reinf_location = col_trans_crit_bot_distance+col_mid_reinf_distance_half
                col_reinf_w = col_h - 2*col_cover - col_mid_creinf_d
                col_reinf_d= col_d - 2*col_cover - col_mid_creinf_d
                left_column_reinf_shape_mid = self._transverse_reinforcement("rect", col_h, col_d, col_cover, col_mid_creinf_d, (-col_reinf_w-col_cover-col_mid_creinf_d/2, col_mid_reinf_location, -col_reinf_d/2))
                left_column_MID_1, lcol_num = self._create_copied_shapes(left_column_reinf_shape_mid, (0,1,0), col_mid_creinf_s, col_mid_reinf_distance_half, self.reinf_left_column_assembly, "Left_Column_Reinf", lcol_num)
                left_column_MID_2, lcol_num = self._create_copied_shapes(left_column_reinf_shape_mid, (0,-1,0), col_mid_creinf_s, col_mid_reinf_distance_half, self.reinf_left_column_assembly, "Left_Column_Reinf", lcol_num, False)
                list_left_column_tranv_reinf.extend(left_column_MID_1)
                list_left_column_tranv_reinf.extend(left_column_MID_2)

            if col_ext>0:
                if col_crit_bot_creinf_s>0:
                    col_ext_reinf_location = frm_in_h + bm_h + col_ext - col_cover - col_crit_bot_creinf_d/2
                    col_ext_reinf_distance = col_ext - col_cover
                    col_reinf_w = col_h - 2*col_cover - col_crit_bot_creinf_d
                    col_reinf_d= col_d - 2*col_cover - col_crit_bot_creinf_d
                    left_column_reinf_shape_ext = self._transverse_reinforcement("rect", col_h, col_d, col_cover, col_crit_bot_creinf_d, (-col_reinf_w-col_cover-col_crit_bot_creinf_d/2, col_ext_reinf_location, -col_reinf_d/2))
                    left_column_EXT, lcol_num = self._create_copied_shapes(left_column_reinf_shape_ext, (0,-1,0), col_crit_bot_creinf_s, col_ext_reinf_distance, self.reinf_left_column_assembly, "Left_Column_Reinf", lcol_num)
                    list_left_column_tranv_reinf.extend(left_column_EXT)


            self.reinf_right_column_assembly = self._cad_create_part(label="Right_Column_Reinforcement_Assembly")
            rcol_num=1
            for partFeature in list_left_column_tranv_reinf:
                self._create_copied_shapes(partFeature.Shape, (1,0,0), frm_in_l+col_h, frm_in_l+col_h, self.reinf_right_column_assembly, "Right_Column_Reinf", rcol_num, False)
                rcol_num = rcol_num + 1


        ##################################################################
        # ========= TRANSVERSE REINFORCEMENT BEAM ===========
        ##################################################################
        self.reinf_beam_assembly = self._cad_create_part(label="Beam_Reinforcement_Assembly")

        # Get base beam reinforcement data from database
        bm_trans_crit_left_distance = self.db_entry["bm_trans_crit_left_distance"]
        bm_trans_crit_left_reinf = self.db_entry["bm_trans_crit_left_reinf"]
        bm_trans_crit_right_distance = self.db_entry["bm_trans_crit_right_distance"]
        bm_trans_crit_right_reinf = self.db_entry["bm_trans_crit_right_reinf"]
        bm_trans_mid_reinf = self.db_entry["bm_trans_mid_reinf"]
        bm_cover = self.db_entry["bm_cover"]

        # Check if col_cover is positive
        if bm_cover <= 0:
            raise ValueError("bm_cover must be a positive value")

        # Parse reinforcement strings
        bm_crit_left_reinf_data = self._parse_reinforcement_string(bm_trans_crit_left_reinf)
        bm_crit_right_reinf_data = self._parse_reinforcement_string(bm_trans_crit_right_reinf)
        bm_mid_reinf_data = self._parse_reinforcement_string(bm_trans_mid_reinf)

        # Check if any variable is empty
        if not bm_crit_left_reinf_data or not bm_crit_right_reinf_data or not bm_mid_reinf_data:
            raise ValueError("Some beam transverse reinforcement are incorrect!")
        else:
            bm_crit_left_reinf_n, bm_crit_left_reinf_d, bm_crit_left_reinf_s = bm_crit_left_reinf_data[0]
            bm_crit_right_reinf_n, bm_crit_right_reinf_d, bm_crit_right_reinf_s = bm_crit_right_reinf_data[0]
            bm_mid_reinf_n, bm_mid_creinf_d, bm_mid_creinf_s  = bm_mid_reinf_data[0]

            bm_crit_left_reinf_d = bm_crit_right_reinf_d = bm_mid_creinf_d = max(bm_crit_left_reinf_d, bm_crit_right_reinf_d, bm_mid_creinf_d)

            if bm_crit_left_reinf_n==0:
                bm_crit_left_reinf_s =  bm_mid_creinf_s

            if bm_crit_right_reinf_n==0:
                bm_crit_right_reinf_s =  bm_mid_creinf_s

            if bm_mid_reinf_n == bm_crit_left_reinf_n == bm_crit_right_reinf_n ==0:
                print("Warning: No transverse reinforcement exist in beam!")


            bm_num = 1

            # LEFT Critical Region
            if bm_crit_left_reinf_n>0:
                bm_reinf_w = bm_t - 2*bm_cover - bm_crit_left_reinf_d
                bm_reinf_h = bm_h - 2*bm_cover - bm_crit_left_reinf_d
                beam_reinf_shape_left = self._transverse_reinforcement("rect", bm_h, bm_t, bm_cover, bm_crit_left_reinf_d, (0,frm_in_h+bm_cover+bm_crit_left_reinf_d/2, -bm_reinf_w/2), rot_z=90)
                beam_LEFT, bm_num = self._create_copied_shapes(beam_reinf_shape_left, (1,0,0), bm_crit_left_reinf_s, bm_trans_crit_left_distance, self.reinf_beam_assembly, "Beam_Reinf", bm_num)

            # RIGHT Critical Region
            if bm_crit_right_reinf_n>0:
                bm_reinf_w = bm_t - 2*bm_cover - bm_crit_right_reinf_d
                bm_reinf_h = bm_h - 2*bm_cover - bm_crit_right_reinf_d
                beam_reinf_shape_right = self._transverse_reinforcement("rect", bm_h, bm_t, bm_cover, bm_crit_right_reinf_d, (frm_in_l,frm_in_h+bm_cover+bm_crit_right_reinf_d/2, -bm_reinf_w/2), rot_z=90)
                beam_RIGHT, bm_num = self._create_copied_shapes(beam_reinf_shape_right, (-1,0,0), bm_crit_right_reinf_s, bm_trans_crit_right_distance, self.reinf_beam_assembly, "Beam_Reinf", bm_num)

            if bm_mid_reinf_n>0:
                # MID Region 
                bm_mid_reinf_distance_half= (frm_in_l - bm_trans_crit_right_distance - bm_trans_crit_left_distance)/2
                bm_mid_reinf_location = bm_trans_crit_left_distance + bm_mid_reinf_distance_half

                bm_reinf_w = bm_t - 2*bm_cover - bm_mid_creinf_d
                bm_reinf_h = bm_h - 2*bm_cover - bm_mid_creinf_d
                beam_reinf_shape_mid = self._transverse_reinforcement("rect", bm_h, bm_t, bm_cover, bm_mid_creinf_d, (bm_mid_reinf_location, frm_in_h+bm_cover+bm_mid_creinf_d/2, -bm_reinf_w/2), rot_z=90)
                beam_MID_1, bm_num = self._create_copied_shapes(beam_reinf_shape_mid, (1,0,0), bm_mid_creinf_s, bm_mid_reinf_distance_half, self.reinf_beam_assembly, "Beam_Reinf", bm_num)
                beam_MID_2, bm_num = self._create_copied_shapes(beam_reinf_shape_mid, (-1,0,0), bm_mid_creinf_s, bm_mid_reinf_distance_half, self.reinf_beam_assembly, "Beam_Reinf", bm_num, False)

            if bm_ext>0:
                if bm_crit_left_reinf_s>0:
                    bm_left_ext_reinf_location = -bm_ext - col_h + bm_cover + bm_crit_left_reinf_d/2
                    bm_left_ext_reinf_distance = bm_ext - bm_cover
                    bm_reinf_w = bm_t - 2*bm_cover - bm_crit_left_reinf_d
                    bm_reinf_h = bm_h - 2*bm_cover - bm_crit_left_reinf_d
                    beam_reinf_shape_ext = self._transverse_reinforcement("rect", bm_h, bm_t, bm_cover, bm_crit_left_reinf_d, (bm_left_ext_reinf_location,frm_in_h+bm_cover+bm_crit_left_reinf_d/2, -bm_reinf_w/2), rot_z=90)
                    beam_EXT, bm_num = self._create_copied_shapes(beam_reinf_shape_ext, (1,0,0), bm_crit_left_reinf_s, bm_left_ext_reinf_distance, self.reinf_beam_assembly, "Beam_Reinf", bm_num)
                if bm_crit_right_reinf_s>0:
                    bm_right_ext_reinf_location = frm_in_l + col_h + bm_ext - bm_cover - bm_crit_left_reinf_d/2
                    bm_right_ext_reinf_distance = bm_ext - bm_cover
                    bm_reinf_w = bm_t - 2*bm_cover - bm_crit_right_reinf_d
                    bm_reinf_h = bm_h - 2*bm_cover - bm_crit_right_reinf_d
                    beam_reinf_shape_ext = self._transverse_reinforcement("rect", bm_h, bm_t, bm_cover, bm_crit_right_reinf_d, (bm_right_ext_reinf_location,frm_in_h+bm_cover+bm_crit_right_reinf_d/2, -bm_reinf_w/2), rot_z=90)
                    beam_EXT_2, bm_num = self._create_copied_shapes(beam_reinf_shape_ext, (-1,0,0), bm_crit_right_reinf_s, bm_right_ext_reinf_distance, self.reinf_beam_assembly, "Beam_Reinf", bm_num)


        ##################################################################
        # ========= TRANSVERSE REINFORCEMENT BASE BEAM ===========
        ##################################################################
        self.reinf_base_beam_assembly = self._cad_create_part(label="Base_Beam_Reinforcement_Assembly")

        # Get base beam reinforcement data from database
        bbm_trans_crit_left_distance = self.db_entry["bbm_trans_crit_left_distance"]
        bbm_trans_crit_left_reinf = self.db_entry["bbm_trans_crit_left_reinf"]
        bbm_trans_crit_right_distance = self.db_entry["bbm_trans_crit_right_distance"]
        bbm_trans_crit_right_reinf = self.db_entry["bbm_trans_crit_right_reinf"]
        bbm_trans_mid_reinf = self.db_entry["bbm_trans_mid_reinf"]
        bbm_cover = self.db_entry["bbm_cover"]

        # Check if col_cover is positive
        if bbm_cover <= 0:
            raise ValueError("bbm_cover must be a positive value")

        # Parse reinforcement strings
        bbm_crit_left_reinf_data = self._parse_reinforcement_string(bbm_trans_crit_left_reinf)
        bbm_crit_right_reinf_data = self._parse_reinforcement_string(bbm_trans_crit_right_reinf)
        bbm_mid_reinf_data = self._parse_reinforcement_string(bbm_trans_mid_reinf)

        # Check if any variable is empty
        if not bbm_crit_left_reinf_data or not bbm_crit_right_reinf_data or not bbm_mid_reinf_data:
            raise ValueError("Some base_beam transverse reinforcement are incorrect!")
        else:

            bbm_crit_left_reinf_n, bbm_crit_left_reinf_d, bbm_crit_left_reinf_s = bbm_crit_left_reinf_data[0]
            bbm_crit_right_reinf_n, bbm_crit_right_reinf_d, bbm_crit_right_reinf_s = bbm_crit_right_reinf_data[0]
            bbm_mid_reinf_n, bbm_mid_creinf_d, bbm_mid_creinf_s  = bbm_mid_reinf_data[0]

            bbm_crit_left_reinf_d = bbm_crit_right_reinf_d = bbm_mid_creinf_d = max(bbm_crit_left_reinf_d, bbm_crit_right_reinf_d, bbm_mid_creinf_d)

            if bbm_crit_left_reinf_n==0:
                bbm_crit_left_reinf_s =  bbm_mid_creinf_s

            if bbm_crit_right_reinf_n==0:
                bbm_crit_right_reinf_s =  bbm_mid_creinf_s

            if bbm_mid_reinf_n == bbm_crit_left_reinf_n == bbm_crit_right_reinf_n ==0:
                print("Warning: No transverse reinforcement exist in base_beam!")


            bbm_num = 1

            # LEFT Critical Region
            if bbm_crit_left_reinf_n>0:
                bbm_reinf_w = bbm_t - 2*bbm_cover - bbm_crit_left_reinf_d
                bbm_reinf_h = bbm_h - 2*bbm_cover - bbm_crit_left_reinf_d
                base_beam_reinf_shape_left = self._transverse_reinforcement("rect", bbm_h, bbm_t, bbm_cover, bbm_crit_left_reinf_d, (0,-bbm_h+bbm_cover+bbm_crit_left_reinf_d/2, -bbm_reinf_w/2), rot_z=90)
                base_beam_LEFT, bbm_num = self._create_copied_shapes(base_beam_reinf_shape_left, (1,0,0), bbm_crit_left_reinf_s, bbm_trans_crit_left_distance, self.reinf_base_beam_assembly, "Base_Beam_Reinf", bbm_num)

            # RIGHT Critical Region
            if bbm_crit_right_reinf_n>0:
                bbm_reinf_w = bbm_t - 2*bbm_cover - bbm_crit_right_reinf_d
                bbm_reinf_h = bbm_h - 2*bbm_cover - bbm_crit_right_reinf_d
                base_beam_reinf_shape_right = self._transverse_reinforcement("rect", bbm_h, bbm_t, bbm_cover, bbm_crit_right_reinf_d, (frm_in_l,-bbm_h+bbm_cover+bbm_crit_right_reinf_d/2, -bbm_reinf_w/2), rot_z=90)
                base_beam_RIGHT, bbm_num = self._create_copied_shapes(base_beam_reinf_shape_right, (-1,0,0), bbm_crit_right_reinf_s, bbm_trans_crit_right_distance, self.reinf_base_beam_assembly, "Base_Beam_Reinf", bbm_num)

            if bbm_mid_reinf_n>0:
                # MID Region 
                bbm_mid_reinf_distance_half= (frm_in_l - bbm_trans_crit_right_distance - bbm_trans_crit_left_distance)/2
                bbm_mid_reinf_location = bbm_trans_crit_left_distance + bbm_mid_reinf_distance_half

                bbm_reinf_w = bbm_t - 2*bbm_cover - bbm_mid_creinf_d
                bbm_reinf_h = bbm_h - 2*bbm_cover - bbm_mid_creinf_d
                left_base_beam_reinf_shape_mid = self._transverse_reinforcement("rect", bbm_h, bbm_t, bbm_cover, bbm_mid_creinf_d, (bbm_mid_reinf_location, -bbm_h+bbm_cover+bbm_crit_right_reinf_d/2, -bbm_reinf_w/2), rot_z=90)
                left_base_beam_MID_1, bbm_num = self._create_copied_shapes(left_base_beam_reinf_shape_mid, (1,0,0), bbm_mid_creinf_s, bbm_mid_reinf_distance_half, self.reinf_base_beam_assembly, "Base_Beam_Reinf", bbm_num)
                left_base_beam_MID_2, bbm_num = self._create_copied_shapes(left_base_beam_reinf_shape_mid, (-1,0,0), bbm_mid_creinf_s, bbm_mid_reinf_distance_half, self.reinf_base_beam_assembly, "Base_Beam_Reinf", bbm_num, False)

            if bbm_ext>0:
                if bbm_crit_left_reinf_s>0:
                    bbm_left_ext_reinf_location = -bbm_ext - col_h + bbm_cover + bbm_crit_left_reinf_d/2
                    bbm_left_ext_reinf_distance = bbm_ext - bbm_cover
                    bbm_reinf_w = bbm_t - 2*bbm_cover - bbm_crit_left_reinf_d
                    bbm_reinf_h = bbm_h - 2*bbm_cover - bbm_crit_left_reinf_d
                    left_base_beam_reinf_shape_ext = self._transverse_reinforcement("rect", bbm_h, bbm_t, bbm_cover, bbm_crit_left_reinf_d, (bbm_left_ext_reinf_location,-bbm_h+bbm_cover+bbm_crit_left_reinf_d/2, -bbm_reinf_w/2), rot_z=90)
                    left_base_beam_EXT, bbm_num = self._create_copied_shapes(left_base_beam_reinf_shape_ext, (1,0,0), bbm_crit_left_reinf_s, bbm_left_ext_reinf_distance, self.reinf_base_beam_assembly, "Base_Beam_Reinf", bbm_num)
                if bbm_crit_right_reinf_s>0:
                    bbm_right_ext_reinf_location = frm_in_l + col_h + bbm_ext - bbm_cover - bbm_crit_right_reinf_d/2
                    bbm_right_ext_reinf_distance = bbm_ext - bbm_cover
                    bbm_reinf_w = bbm_t - 2*bbm_cover - bbm_crit_right_reinf_d
                    bbm_reinf_h = bbm_h - 2*bbm_cover - bbm_crit_right_reinf_d
                    right_base_beam_reinf_shape_ext = self._transverse_reinforcement("rect", bbm_h, bbm_t, bbm_cover, bbm_crit_right_reinf_d, (bbm_right_ext_reinf_location,-bbm_h+bbm_cover+bbm_crit_right_reinf_d/2, -bbm_reinf_w/2), rot_z=90)
                    right_base_beam_EXT, bbm_num = self._create_copied_shapes(right_base_beam_reinf_shape_ext, (-1,0,0), bbm_crit_right_reinf_s, bbm_right_ext_reinf_distance, self.reinf_base_beam_assembly, "Base_Beam_Reinf", bbm_num)


        ##################################################################
        # ========= COLUMN LONGITUDINAL REINFORCEMENT ===========
        ##################################################################
        self.reinf_left_column_long_assembly = self._cad_create_part(label="Left_Column_Longitudinal_Reinforcement_Assembly")

        # Get column longitudinal reinforcement data from database
        col_long_reinf_corner = self.db_entry["col_long_reinf_corner"]
        col_long_reinf_top = self.db_entry["col_long_reinf_top"]
        col_long_reinf_mid = self.db_entry["col_long_reinf_mid"]
        col_long_reinf_bot = self.db_entry["col_long_reinf_bot"]

        # Parse reinforcement strings
        col_corner_reinf_data = self._parse_reinforcement_string(col_long_reinf_corner)
        col_top_reinf_data = self._parse_reinforcement_string(col_long_reinf_top)
        col_mid_reinf_data = self._parse_reinforcement_string(col_long_reinf_mid)
        col_bot_reinf_data = self._parse_reinforcement_string(col_long_reinf_bot)


        col_corner_count, col_corner_d, _ = col_corner_reinf_data[0]
        if col_corner_count !=4:
            raise ValueError("Define exactly four (4) longitudinal reinforcement for forners!")

        col_long_num = 1
        list_left_col_long_reinf = []
        col_reinf_w = col_h - 2*col_cover - col_crit_bot_creinf_d
        col_reinf_d = col_d - 2*col_cover - col_crit_bot_creinf_d
        tmp_shape = self._longitudinal_reinforcement(col_tot_h, col_cover, col_crit_top_creinf_d, bbm_cover, bbm_crit_left_reinf_d, (-col_cover-col_crit_bot_creinf_d/2, -bbm_h+bbm_crit_left_reinf_d/2+bbm_cover, col_reinf_d/2))
        tmp_shape, col_long_num = self._create_copied_shapes(tmp_shape, (-1,0,0), col_reinf_w, col_reinf_w, self.reinf_left_column_long_assembly, "Left_Column_Long_Reinf", col_long_num, add_base_shape=True)
        list_left_col_long_reinf.extend(tmp_shape)
        tmp_shape, col_long_num = self._create_copied_shapes(tmp_shape[1].Shape, (0,0,-1), col_reinf_d, col_reinf_d, self.reinf_left_column_long_assembly, "Left_Column_Long_Reinf", col_long_num, add_base_shape=False)
        list_left_col_long_reinf.extend(tmp_shape)
        tmp_shape, col_long_num = self._create_copied_shapes(tmp_shape[0].Shape, (1,0,0), col_reinf_w, col_reinf_w, self.reinf_left_column_long_assembly, "Left_Column_Long_Reinf", col_long_num, add_base_shape=False)
        list_left_col_long_reinf.extend(tmp_shape)


        n_left_col_long_top_reinf = 0
        for item in col_top_reinf_data:
            n_left_col_long_top_reinf = n_left_col_long_top_reinf + item[0]
        tmp_shape, col_long_num = self._create_copied_shapes(list_left_col_long_reinf[2].Shape, (1,0,0), col_reinf_w/(n_left_col_long_top_reinf+1), col_reinf_w, self.reinf_left_column_long_assembly, "Left_Column_Long_Reinf", col_long_num, add_base_shape=False, add_last_element=False, use_rounding=True)
        list_left_col_long_reinf.extend(tmp_shape)


        n_left_col_long_bot_reinf = 0
        for item in col_bot_reinf_data:
            n_left_col_long_bot_reinf = n_left_col_long_bot_reinf + item[0]
        tmp_shape, col_long_num = self._create_copied_shapes(list_left_col_long_reinf[1].Shape, (1,0,0), col_reinf_w/(n_left_col_long_bot_reinf+1), col_reinf_w, self.reinf_left_column_long_assembly, "Left_Column_Long_Reinf", col_long_num, add_base_shape=False, add_last_element=False, use_rounding=True)
        list_left_col_long_reinf.extend(tmp_shape)

        n_left_col_long_mid_reinf = 0
        for item in col_mid_reinf_data:
            n_left_col_long_mid_reinf = n_left_col_long_mid_reinf + item[0]
        if n_left_col_long_mid_reinf % 2 != 0:
            raise ValueError(f"Middle Reinforcement of Columns must be EVEN number!")

        n_left_col_long_mid_reinf=n_left_col_long_mid_reinf/2
        tmp_shape, col_long_num = self._create_copied_shapes(list_left_col_long_reinf[1].Shape, (0,0,-1), col_reinf_d/(n_left_col_long_mid_reinf+1), col_reinf_d, self.reinf_left_column_long_assembly, "Left_Column_Long_Reinf", col_long_num, add_base_shape=False, add_last_element=False, use_rounding=True)
        list_left_col_long_reinf.extend(tmp_shape)
        tmp_shape, col_long_num = self._create_copied_shapes(list_left_col_long_reinf[0].Shape, (0,0,-1), col_reinf_d/(n_left_col_long_mid_reinf+1), col_reinf_d, self.reinf_left_column_long_assembly, "Left_Column_Long_Reinf", col_long_num, add_base_shape=False, add_last_element=False, use_rounding=True)
        list_left_col_long_reinf.extend(tmp_shape)


        self.reinf_right_column_long_assembly = self._cad_create_part(label="Right_Column_Longitudinal_Reinforcement_Assembly")
        rcol_num=1
        for partFeature in list_left_col_long_reinf:
            self._create_copied_shapes(partFeature.Shape, (1,0,0), frm_in_l+col_h, frm_in_l+col_h, self.reinf_right_column_long_assembly, "Right_Column_Long_Reinf", rcol_num, False)
            rcol_num = rcol_num + 1


        ##################################################################
        # ========= BEAM LONGITUDINAL REINFORCEMENT ===========
        ##################################################################
        self.reinf_beam_long_assembly = self._cad_create_part(label="Beam_Longitudinal_Reinforcement_Assembly")

        # Get beam longitudinal reinforcement data from database
        bm_long_reinf_corner = self.db_entry["bm_long_reinf_corner"]
        bm_long_reinf_top = self.db_entry["bm_long_reinf_top"]
        bm_long_reinf_mid = self.db_entry["bm_long_reinf_mid"]
        bm_long_reinf_bot = self.db_entry["bm_long_reinf_bot"]

        # Parse reinforcement strings
        bm_corner_reinf_data = self._parse_reinforcement_string(bm_long_reinf_corner)
        bm_top_reinf_data = self._parse_reinforcement_string(bm_long_reinf_top)
        bm_mid_reinf_data = self._parse_reinforcement_string(bm_long_reinf_mid)
        bm_bot_reinf_data = self._parse_reinforcement_string(bm_long_reinf_bot)

        # Validate corner reinforcement
        bm_corner_count, bm_corner_d, _ = bm_corner_reinf_data[0]
        if bm_corner_count !=4:
            raise ValueError("Define exactly four (4) longitudinal reinforcement for forners!")

        bm_long_num = 1
        list_beam_long_reinf = []

        bm_reinf_w = bm_t - 2*bm_cover - bm_crit_left_reinf_d
        bm_reinf_h = bm_h - 2*bm_cover - bm_crit_left_reinf_d

        tmp_shape = self._longitudinal_reinforcement(bm_tot_l, bm_cover, bm_crit_left_reinf_d, bm_cover, bm_crit_left_reinf_d, (bm_tot_l-col_h-bm_ext-bm_cover-bm_crit_left_reinf_d/2,frm_in_h+bm_cover+bm_crit_left_reinf_d/2, -bm_reinf_w/2), rot_z=90)
        tmp_shape, bm_long_num = self._create_copied_shapes(tmp_shape, (0,0,1), bm_reinf_w, bm_reinf_w, self.reinf_beam_long_assembly, "Beam_Long_Reinf", bm_long_num, add_base_shape=True)
        list_beam_long_reinf.extend(tmp_shape)
        tmp_shape, bm_long_num = self._create_copied_shapes(tmp_shape[1].Shape, (0,1,0), bm_reinf_h, bm_reinf_h, self.reinf_beam_long_assembly, "Beam_Long_Reinf", bm_long_num, add_base_shape=False)
        list_beam_long_reinf.extend(tmp_shape)
        tmp_shape, bm_long_num = self._create_copied_shapes(tmp_shape[0].Shape, (0,0,-1), bm_reinf_w, bm_reinf_w, self.reinf_beam_long_assembly, "Beam_Long_Reinf", bm_long_num, add_base_shape=False)
        list_beam_long_reinf.extend(tmp_shape)



        n_bm_long_top_reinf = 0
        for item in bm_top_reinf_data:
            n_bm_long_top_reinf = n_bm_long_top_reinf + item[0]
        tmp_shape, bm_long_num = self._create_copied_shapes(list_beam_long_reinf[2].Shape, (0,0,-1), bm_reinf_w/(n_bm_long_top_reinf+1), bm_reinf_w, self.reinf_beam_long_assembly, "Beam_Long_Reinf", bm_long_num, add_base_shape=False, add_last_element=False, use_rounding=True)
        list_beam_long_reinf.extend(tmp_shape)

        n_bm_long_bot_reinf = 0
        for item in bm_bot_reinf_data:
            n_bm_long_bot_reinf = n_bm_long_bot_reinf + item[0]
        tmp_shape, bm_long_num = self._create_copied_shapes(list_beam_long_reinf[1].Shape, (0,0,-1), bm_reinf_w/(n_bm_long_bot_reinf+1), bm_reinf_w, self.reinf_beam_long_assembly, "Beam_Long_Reinf", bm_long_num, add_base_shape=False, add_last_element=False, use_rounding=True)
        list_beam_long_reinf.extend(tmp_shape)

        n_bm_long_mid_reinf = 0
        for item in bm_mid_reinf_data:
            n_bm_long_mid_reinf = n_bm_long_mid_reinf + item[0]
        if n_bm_long_mid_reinf % 2 != 0:
            raise ValueError(f"Middle Reinforcement of Beam must be EVEN number!")

        n_bm_long_mid_reinf=n_bm_long_mid_reinf/2
        tmp_shape, bm_long_num = self._create_copied_shapes(list_beam_long_reinf[1].Shape, (0,1,0), bm_reinf_h/(n_bm_long_mid_reinf+1), bm_reinf_h, self.reinf_beam_long_assembly, "Beam_Long_Reinf", bm_long_num, add_base_shape=False, add_last_element=False, use_rounding=True)
        list_beam_long_reinf.extend(tmp_shape)
        tmp_shape, bm_long_num = self._create_copied_shapes(list_beam_long_reinf[0].Shape, (0,1,0), bm_reinf_h/(n_bm_long_mid_reinf+1), bm_reinf_h, self.reinf_beam_long_assembly, "Beam_Long_Reinf", bm_long_num, add_base_shape=False, add_last_element=False, use_rounding=True)
        list_beam_long_reinf.extend(tmp_shape)


        ##################################################################
        # ========= BASE BEAM LONGITUDINAL REINFORCEMENT ===========
        ##################################################################
        self.reinf_base_beam_long_assembly = self._cad_create_part(label="Base_Beam_Longitudinal_Reinforcement_Assembly")

        # Get base beam longitudinal reinforcement data from database
        bbm_long_reinf_corner = self.db_entry["bbm_long_reinf_corner"]
        bbm_long_reinf_top = self.db_entry["bbm_long_reinf_top"]
        bbm_long_reinf_mid = self.db_entry["bbm_long_reinf_mid"]
        bbm_long_reinf_bot = self.db_entry["bbm_long_reinf_bot"]

        # Parse reinforcement strings
        bbm_corner_reinf_data = self._parse_reinforcement_string(bbm_long_reinf_corner)
        bbm_top_reinf_data = self._parse_reinforcement_string(bbm_long_reinf_top)
        bbm_mid_reinf_data = self._parse_reinforcement_string(bbm_long_reinf_mid)
        bbm_bot_reinf_data = self._parse_reinforcement_string(bbm_long_reinf_bot)

        # Validate corner reinforcement
        bbm_corner_count, bbm_corner_d, _ = bbm_corner_reinf_data[0]
        if bbm_corner_count != 4:
            raise ValueError("Define exactly four (4) longitudinal reinforcement for base beam corners!")

        bbm_long_num = 1
        list_base_beam_long_reinf = []

        bbm_reinf_w = bbm_t - 2*bbm_cover - bbm_crit_left_reinf_d
        bbm_reinf_h = bbm_h - 2*bbm_cover - bbm_crit_left_reinf_d
        # Check if values are positive
        if bbm_reinf_w <= 0:
            raise ValueError(f"Invalid bbm_reinf_w: {bbm_reinf_w}. Check base_beam t, cover and rebar diameter values.")
        if bbm_reinf_h <= 0:
            raise ValueError(f"Invalid bbm_reinf_h: {bbm_reinf_h}. Check base_beam h, cover and rebar diameter values.")


        tmp_shape = self._longitudinal_reinforcement(bbm_tot_l, bbm_cover, bbm_crit_left_reinf_d, bbm_cover, bbm_crit_left_reinf_d, (bbm_tot_l-col_h-bbm_ext-bbm_cover-bbm_crit_left_reinf_d/2, -bbm_h+bbm_cover+bbm_crit_left_reinf_d/2, -bbm_reinf_w/2), rot_z=90)
        tmp_shape, bbm_long_num = self._create_copied_shapes(tmp_shape, (0,0,1), bbm_reinf_w, bbm_reinf_w, self.reinf_base_beam_long_assembly, "Base_Beam_Long_Reinf", bbm_long_num, add_base_shape=True)
        list_base_beam_long_reinf.extend(tmp_shape)

        tmp_shape, bbm_long_num = self._create_copied_shapes(tmp_shape[1].Shape, (0,1,0), bbm_reinf_h, bbm_reinf_h, self.reinf_base_beam_long_assembly, "Base_Beam_Long_Reinf", bbm_long_num, add_base_shape=False)
        list_base_beam_long_reinf.extend(tmp_shape)

        tmp_shape, bbm_long_num = self._create_copied_shapes(tmp_shape[0].Shape, (0,0,-1), bbm_reinf_w, bbm_reinf_w, self.reinf_base_beam_long_assembly, "Base_Beam_Long_Reinf", bbm_long_num, add_base_shape=False)
        list_base_beam_long_reinf.extend(tmp_shape)

        n_bbm_long_top_reinf = 0
        for item in bbm_top_reinf_data:
            n_bbm_long_top_reinf = n_bbm_long_top_reinf + item[0]

        tmp_shape, bbm_long_num = self._create_copied_shapes(list_base_beam_long_reinf[2].Shape, (0,0,-1), bbm_reinf_w/(n_bbm_long_top_reinf+1), bbm_reinf_w, self.reinf_base_beam_long_assembly, "Base_Beam_Long_Reinf", bbm_long_num, add_base_shape=False, add_last_element=False, use_rounding=True)
        list_base_beam_long_reinf.extend(tmp_shape)

        n_bbm_long_bot_reinf = 0
        for item in bbm_bot_reinf_data:
            n_bbm_long_bot_reinf = n_bbm_long_bot_reinf + item[0]

        tmp_shape, bbm_long_num = self._create_copied_shapes(list_base_beam_long_reinf[1].Shape, (0,0,-1), bbm_reinf_w/(n_bbm_long_bot_reinf+1), bbm_reinf_w, self.reinf_base_beam_long_assembly, "Base_Beam_Long_Reinf", bbm_long_num, add_base_shape=False, add_last_element=False, use_rounding=True)
        list_base_beam_long_reinf.extend(tmp_shape)

        n_bbm_long_mid_reinf = 0
        for item in bbm_mid_reinf_data:
            n_bbm_long_mid_reinf = n_bbm_long_mid_reinf + item[0]

        if n_bbm_long_mid_reinf % 2 != 0:
            raise ValueError(f"Middle Reinforcement of Base Beam must be EVEN number!")

        n_bbm_long_mid_reinf = n_bbm_long_mid_reinf/2

        tmp_shape, bbm_long_num = self._create_copied_shapes(list_base_beam_long_reinf[1].Shape, (0,1,0), bbm_reinf_h/(n_bbm_long_mid_reinf+1), bbm_reinf_h, self.reinf_base_beam_long_assembly, "Base_Beam_Long_Reinf", bbm_long_num, add_base_shape=False, add_last_element=False, use_rounding=True)
        list_base_beam_long_reinf.extend(tmp_shape)

        tmp_shape, bbm_long_num = self._create_copied_shapes(list_base_beam_long_reinf[0].Shape, (0,1,0), bbm_reinf_h/(n_bbm_long_mid_reinf+1), bbm_reinf_h, self.reinf_base_beam_long_assembly, "Base_Beam_Long_Reinf", bbm_long_num, add_base_shape=False, add_last_element=False, use_rounding=True)
        list_base_beam_long_reinf.extend(tmp_shape)


        ##################################################################
        # ========= SLAB REINFORCEMENT ===========
        ##################################################################
        self.reinf_slab_assembly = self._cad_create_part(label="Slab_Reinforcement_Assembly")
        # Get slab reinforcement data from database
        slb_cover = self.db_entry["slb_cover"]
        slb_top_l_reinf = self.db_entry["slb_top_l_reinf"]
        slb_top_d_reinf = self.db_entry["slb_top_d_reinf"]
        slb_bot_l_reinf = self.db_entry["slb_bot_l_reinf"]
        slb_bot_d_reinf = self.db_entry["slb_bot_d_reinf"]

        # Parse reinforcement strings
        slb_top_l_data = self._parse_reinforcement_string(slb_top_l_reinf)
        slb_top_d_data = self._parse_reinforcement_string(slb_top_d_reinf)
        slb_bot_l_data = self._parse_reinforcement_string(slb_bot_l_reinf)
        slb_bot_d_data = self._parse_reinforcement_string(slb_bot_d_reinf)

        slb_num = 1
        list_slab_reinf = []

        # =============================================================================
        # SECTION 1: TOP L REINFORCEMENT (LEFT & RIGHT)
        # =============================================================================
        slb_eq_tr_d = slb_top_l_data[0][1]
        slb_eq_space = slb_top_l_data[0][2]

        if slb_eq_tr_d>0 and slb_eq_space>0:
            slab_distance = (slb_d - bm_t - 2*slb_cover - slb_eq_space)/2
            slb_reinf_w = slb_d - 2*slb_cover - slb_eq_tr_d
            slb_reinf_h = slb_h - 2*slb_cover - slb_eq_tr_d

            tmp_shape = self._longitudinal_reinforcement(bm_tot_l, slb_cover, slb_eq_tr_d, slb_cover, slb_eq_tr_d, (bm_tot_l-col_h-bm_ext-slb_cover-slb_eq_tr_d/2, frm_in_h+bm_h-slb_cover-slb_eq_tr_d/2, -slb_reinf_w/2), rot_z=90)
            tmp_shape, slb_num = self._create_copied_shapes(tmp_shape, (0,0,1), slb_eq_space, slab_distance, self.reinf_slab_assembly, "Slab_Reinf", slb_num, add_base_shape=True)
            list_slab_reinf.extend(tmp_shape)

            tmp_shape = self._longitudinal_reinforcement(bm_tot_l, slb_cover, slb_eq_tr_d, slb_cover, slb_eq_tr_d, (bm_tot_l-col_h-bm_ext-slb_cover-slb_eq_tr_d/2, frm_in_h+bm_h-slb_cover-slb_eq_tr_d/2, slb_reinf_w/2), rot_z=90)
            tmp_shape, slb_num = self._create_copied_shapes(tmp_shape, (0,0,-1), slb_eq_space, slab_distance, self.reinf_slab_assembly, "Slab_Reinf", slb_num, add_base_shape=True)
            list_slab_reinf.extend(tmp_shape)

        # =============================================================================
        # SECTION 2: BOTTOM L REINFORCEMENT (LEFT & RIGHT)
        # =============================================================================
        slb_eq_tr_d = slb_bot_l_data[0][1]
        slb_eq_space = slb_bot_l_data[0][2]

        if slb_eq_tr_d>0 and slb_eq_space>0:
            slab_distance = (slb_d - bm_t - 2*slb_cover - slb_eq_space)/2
            slb_reinf_w = slb_d - 2*slb_cover - slb_eq_tr_d
            slb_reinf_h = slb_h - 2*slb_cover - slb_eq_tr_d

            tmp_shape = self._longitudinal_reinforcement(bm_tot_l, slb_cover, slb_eq_tr_d, slb_cover, slb_eq_tr_d, (bm_tot_l-col_h-bm_ext-slb_cover-slb_eq_tr_d/2, frm_in_h+(bm_h-slb_h)+slb_cover+slb_eq_tr_d/2, -slb_reinf_w/2), rot_z=90)
            tmp_shape, slb_num = self._create_copied_shapes(tmp_shape, (0,0,1), slb_eq_space, slab_distance, self.reinf_slab_assembly, "Slab_Reinf", slb_num, add_base_shape=True)
            list_slab_reinf.extend(tmp_shape)

            tmp_shape = self._longitudinal_reinforcement(bm_tot_l, slb_cover, slb_eq_tr_d, slb_cover, slb_eq_tr_d, (bm_tot_l-col_h-bm_ext-slb_cover-slb_eq_tr_d/2, frm_in_h+(bm_h-slb_h)+slb_cover+slb_eq_tr_d/2, slb_reinf_w/2), rot_z=90)
            tmp_shape, slb_num = self._create_copied_shapes(tmp_shape, (0,0,-1), slb_eq_space, slab_distance, self.reinf_slab_assembly, "Slab_Reinf", slb_num, add_base_shape=True)
            list_slab_reinf.extend(tmp_shape)

        # =============================================================================
        # SECTION 3: TOP D REINFORCEMENT (MID Z-AXIS)
        # =============================================================================
        slb_eq_tr_d = slb_top_d_data[0][1]
        slb_eq_space = slb_top_d_data[0][2]

        if slb_eq_tr_d>0 and slb_eq_space>0:
            slb_reinf_w = slb_d - 2*slb_cover - slb_eq_tr_d
            slb_reinf_h = slb_h - 2*slb_cover - slb_eq_tr_d

            tmp_shape0 = self._longitudinal_reinforcement(slb_d, slb_cover, slb_eq_tr_d, slb_cover, slb_eq_tr_d, (frm_in_l/2, frm_in_h+bm_h-slb_cover-slb_eq_tr_d/2, -slb_reinf_w/2), rot_x=90)
            tmp_shape, slb_num = self._create_copied_shapes(tmp_shape0, (1,0,0), slb_eq_space, frm_in_l/2, self.reinf_slab_assembly, "Slab_Reinf", slb_num, add_base_shape=True)
            list_slab_reinf.extend(tmp_shape)
            tmp_shape, slb_num = self._create_copied_shapes(tmp_shape0, (-1,0,0), slb_eq_space, frm_in_l/2, self.reinf_slab_assembly, "Slab_Reinf", slb_num, add_base_shape=False)
            list_slab_reinf.extend(tmp_shape)

        # =============================================================================
        # SECTION 4: BOTTOM D REINFORCEMENT (MID Z-AXIS)
        # =============================================================================
        slb_eq_tr_d = slb_bot_d_data[0][1]
        slb_eq_space = slb_bot_d_data[0][2]

        if slb_eq_tr_d>0 and slb_eq_space>0:

            slb_reinf_w = slb_d - 2*slb_cover - slb_eq_tr_d
            slb_reinf_h = slb_h - 2*slb_cover - slb_eq_tr_d

            tmp_shape0 = self._longitudinal_reinforcement(slb_d, slb_cover, slb_eq_tr_d, slb_cover, slb_eq_tr_d, (frm_in_l/2, frm_in_h+(bm_h-slb_h)+slb_cover+slb_eq_tr_d/2, -slb_reinf_w/2), rot_x=90)
            tmp_shape, slb_num = self._create_copied_shapes(tmp_shape0, (1,0,0), slb_eq_space, frm_in_l/2, self.reinf_slab_assembly, "Slab_Reinf", slb_num, add_base_shape=True)
            list_slab_reinf.extend(tmp_shape)
            tmp_shape, slb_num = self._create_copied_shapes(tmp_shape0, (-1,0,0), slb_eq_space, frm_in_l/2, self.reinf_slab_assembly, "Slab_Reinf", slb_num, add_base_shape=False)
            list_slab_reinf.extend(tmp_shape)

        # =============================================================================
        # SECTION 5: TOP D REINFORCEMENT (LEFF & RIGHT Z-AXIS)
        # =============================================================================
        slb_eq_tr_d = slb_top_d_data[0][1]
        slb_eq_space = slb_top_d_data[0][2]

        if slb_eq_tr_d>0 and slb_eq_space>0:

            slb_reinf_w = slb_d - 2*slb_cover - slb_eq_tr_d
            slb_reinf_h = slb_h - 2*slb_cover - slb_eq_tr_d

            tmp_shape0 = self._longitudinal_reinforcement(slb_d, slb_cover, slb_eq_tr_d, slb_cover, slb_eq_tr_d, (frm_in_l+col_h+bm_ext-slb_cover-slb_eq_tr_d/2, frm_in_h+bm_h-slb_cover-slb_eq_tr_d/2, -slb_reinf_w/2), rot_x=90)
            tmp_shape, slb_num = self._create_copied_shapes(tmp_shape0, (-1,0,0), slb_eq_space, bm_ext-slb_cover-slb_eq_tr_d/2, self.reinf_slab_assembly, "Slab_Reinf", slb_num, add_base_shape=True)
            list_slab_reinf.extend(tmp_shape)

            tmp_shape0 = self._longitudinal_reinforcement(slb_d, slb_cover, slb_eq_tr_d, slb_cover, slb_eq_tr_d, (-col_h-bm_ext+slb_cover+slb_eq_tr_d/2, frm_in_h+bm_h-slb_cover-slb_eq_tr_d/2, -slb_reinf_w/2), rot_x=90)
            tmp_shape, slb_num = self._create_copied_shapes(tmp_shape0, (1,0,0), slb_eq_space, bm_ext-slb_cover-slb_eq_tr_d/2, self.reinf_slab_assembly, "Slab_Reinf", slb_num, add_base_shape=True)
            list_slab_reinf.extend(tmp_shape)

        # =============================================================================
        # SECTION 6: BOTTOM D REINFORCEMENT (LEFF & RIGHT Z-AXIS)
        # =============================================================================
        slb_eq_tr_d = slb_bot_d_data[0][1]
        slb_eq_space = slb_bot_d_data[0][2]

        if slb_eq_tr_d>0 and slb_eq_space>0:

            slb_reinf_w = slb_d - 2*slb_cover - slb_eq_tr_d
            slb_reinf_h = slb_h - 2*slb_cover - slb_eq_tr_d

            tmp_shape0 = self._longitudinal_reinforcement(slb_d, slb_cover, slb_eq_tr_d, slb_cover, slb_eq_tr_d, (frm_in_l+col_h+bm_ext-slb_cover-slb_eq_tr_d/2, frm_in_h+(bm_h-slb_h)+slb_cover+slb_eq_tr_d/2, -slb_reinf_w/2), rot_x=90)
            tmp_shape, slb_num = self._create_copied_shapes(tmp_shape0, (-1,0,0), slb_eq_space, bm_ext-slb_cover-slb_eq_tr_d/2, self.reinf_slab_assembly, "Slab_Reinf", slb_num, add_base_shape=True)
            list_slab_reinf.extend(tmp_shape)

            tmp_shape0 = self._longitudinal_reinforcement(slb_d, slb_cover, slb_eq_tr_d, slb_cover, slb_eq_tr_d, (-col_h-bm_ext+slb_cover+slb_eq_tr_d/2, frm_in_h+(bm_h-slb_h)+slb_cover+slb_eq_tr_d/2, -slb_reinf_w/2), rot_x=90)
            tmp_shape, slb_num = self._create_copied_shapes(tmp_shape0, (1,0,0), slb_eq_space, bm_ext-slb_cover-slb_eq_tr_d/2, self.reinf_slab_assembly, "Slab_Reinf", slb_num, add_base_shape=True)
            list_slab_reinf.extend(tmp_shape)

    def _create_infill(self):
        """
        Generate infill configuration
        """
        # Initialize assemblies
        self.infill_assembly = self._cad_create_part(label="infill_assembly")
        self.interface_assembly = self._cad_create_part(label="Interface_Assembly")

        # INFILL INFORMATION
        inf_type = self.db_entry["inf_type"]
        if not(inf_type=="none"):
            
            # infill opening type
            inf_opn_type = self.inf_opn_type = self.db_entry["inf_opn_type"]

            # Window dimensions (for window openings)
            inf_win_h = self.inf_win_h = self.db_entry["inf_win_h"]
            inf_win_v = self.inf_win_v = self.db_entry["inf_win_v"]
            inf_win_ph = self.inf_win_ph = self.db_entry["inf_win_ph"]
            inf_win_pv = self.inf_win_pv = self.db_entry["inf_win_pv"]

            # Door dimensions (for door openings)
            inf_door_h = self.inf_door_h = self.db_entry["inf_door_h"]
            inf_door_v = self.inf_door_v = self.db_entry["inf_door_v"]
            inf_door_ph = self.inf_door_ph = self.db_entry["inf_door_ph"]
            inf_door_pv = self.inf_door_pv = self.db_entry["inf_door_pv"]

            # First wythe properties
            inf_dp = self.inf_dp = self.db_entry["inf_dp"]
            inf_bnd_pat = self.inf_bnd_pat = self.db_entry["inf_bnd_pat"]
            inf_inff_intfc = self.inf_inff_intfc = self.db_entry["inf_inff_intfc"]

            # First wythe interface dimensions
            inf_interface_bottom = self.inf_interface_bottom = self.db_entry["inf_interface_bottom"]
            inf_interface_left = self.inf_interface_left = self.db_entry["inf_interface_left"]
            inf_interface_top = self.inf_interface_top = self.db_entry["inf_interface_top"]
            inf_interface_right = self.inf_interface_right = self.db_entry["inf_interface_right"]

            # First wythe unit and joint info
            inf_ul = self.inf_ul = self.db_entry["inf_ul"]
            inf_uh = self.inf_uh = self.db_entry["inf_uh"]
            inf_ut = self.inf_ut = self.db_entry["inf_ut"]
            inf_uhead_t = self.inf_uhead_t = self.db_entry["inf_uhead_t"]
            inf_ubed_t = self.inf_ubed_t = self.db_entry["inf_ubed_t"]


            # RETRIEVE DATA
            frm_in_h = self.frm_in_h
            frm_in_l = self.frm_in_l



            ### CALCULATIONS
            self.inf_h = frm_in_h - inf_interface_bottom - inf_interface_top
            self.inf_l = frm_in_l - inf_interface_left - inf_interface_right

            if not(inf_bnd_pat == "running" or inf_bnd_pat == "stack"):
                print(f"Unsupported infill bond '{inf_bnd_pat}'. Infill will not be created!")
            else:
                
                inf_thickness = inf_ut

                dict_all_bricks_rows = {}
                self.brick_num = 1

                dict_all_bricks_rows[1] = self._create_infill_first_row(inf_ul, inf_uh, inf_ut, inf_interface_bottom)

                dict_all_bricks_rows[2] = self._create_infill_second_row(inf_ul, inf_uh, inf_ut, inf_interface_bottom+inf_uh+inf_ubed_t)


                steph = 2*inf_uh + 2*inf_ubed_t
                max_inf_h = frm_in_h - inf_interface_top
                row1_height = inf_interface_bottom + inf_uh
                row2_height = row1_height + inf_ubed_t + inf_uh
                repeat_steps = math.floor(self.inf_h / steph)
                current_brick_row = 2

                # Track the actual top of the last created row
                last_row_top = row2_height

                for i in range(1, repeat_steps + 1):
                    for j in range(1, 3):
                        # Calculate theoretical position
                        if j == 1:
                            new_row_top = row1_height + steph * i
                        else:
                            new_row_top = row2_height + steph * i
                            
                        # Check if it fits
                        if new_row_top > max_inf_h:
                            continue
                            
                        # Create the row
                        new_list_bricks = []
                        for bricki in dict_all_bricks_rows[j]:
                            copy_bricki = bricki.Shape.copy()
                            translation_vector = FreeCAD.Vector(0, steph*i, 0)
                            copy_bricki.translate(translation_vector)
                            temp_obj = self._cad_add_shape_to_feature_to_part(f"Brick_{self.brick_num}", copy_bricki, self.infill_assembly)
                            new_list_bricks.extend([temp_obj])
                            self.brick_num = self.brick_num + 1
                            
                        current_brick_row += 1
                        dict_all_bricks_rows[current_brick_row] = new_list_bricks
                        
                        # Update the actual last row position
                        last_row_top = new_row_top

                # Calculate remaining height from ACTUAL last row position
                remaining_height = max_inf_h - last_row_top

                # Account for the bed joint that needs to be added
                remaining_height_for_brick = remaining_height - inf_ubed_t

                if remaining_height_for_brick > 0:
                    current_brick_row += 1
                    final_row_bottom = last_row_top + inf_ubed_t
                    
                    # Determine which pattern to use for the final row
                    if current_brick_row % 2 == 1:
                        dict_all_bricks_rows[current_brick_row] = self._create_infill_first_row(inf_ul, remaining_height_for_brick, inf_ut, final_row_bottom)
                    else:
                        dict_all_bricks_rows[current_brick_row] = self._create_infill_second_row(inf_ul, remaining_height_for_brick, inf_ut, final_row_bottom)

                #### ================== MORTAR ===========================
                mortar_shape = Part.makeBox(self.inf_l, self.inf_h, inf_ut)
                mortar_shape.translate(FreeCAD.Vector(inf_interface_left, inf_interface_bottom, -inf_ut))
                mortar_shape.translate(FreeCAD.Vector(0,0, inf_dp))

                all_bricks_fused = None
                for row_num in dict_all_bricks_rows:
                    for brick in dict_all_bricks_rows[row_num]:
                        if all_bricks_fused is None:
                            all_bricks_fused = brick.Shape
                        else:
                            all_bricks_fused = all_bricks_fused.fuse(brick.Shape)

                mortar_with_holes = mortar_shape.cut(all_bricks_fused)


                #### ================== OPENING ===========================
                if inf_opn_type != "none":
                    if inf_win_h>0 and inf_win_v>0 and inf_win_ph>=0 and inf_win_pv>=0 :
                        window_shape = Part.makeBox(inf_win_h, inf_win_v, inf_ut)
                        window_shape.translate(FreeCAD.Vector(inf_win_ph, inf_win_pv, -inf_ut))
                        window_shape.translate(FreeCAD.Vector(0,0, inf_dp))

                        all_bricks_fused = all_bricks_fused.cut(window_shape)
                        mortar_with_holes = mortar_with_holes.cut(window_shape)
                        print("Windows Created!")

                    if inf_door_h>0 and inf_door_v>0 and inf_door_ph>=0 and inf_door_pv>=0 :
                        door_shape = Part.makeBox(inf_door_h, inf_door_v, inf_ut)
                        door_shape.translate(FreeCAD.Vector(inf_door_ph, inf_door_pv, -inf_ut))
                        door_shape.translate(FreeCAD.Vector(0,0, inf_dp))

                        all_bricks_fused = all_bricks_fused.cut(door_shape)
                        mortar_with_holes = mortar_with_holes.cut(door_shape)
                        print("Door Created!")

                    # Add to assemblies
                    self.infill_assembly = self._cad_create_part(label="Infill_Assembly")
                    self._cad_add_shape_to_feature_to_part("Mortar", mortar_with_holes, self.infill_assembly)
                    self._cad_add_shape_to_feature_to_part("Bricks", all_bricks_fused, self.infill_assembly)
                else:
                    self._cad_add_shape_to_feature_to_part("Mortar", mortar_with_holes, self.infill_assembly)

                #### ================== INTERFACES ===========================
                interface_shape1 = Part.makeBox(frm_in_l, frm_in_h, inf_ut)
                interface_shape2 = Part.makeBox(frm_in_l-(inf_interface_left+inf_interface_right), frm_in_h-(inf_interface_top+inf_interface_bottom), inf_ut)
                interface_shape2.translate(FreeCAD.Vector(inf_interface_left, inf_interface_bottom, 0))
                interface_shape0 = interface_shape1.cut(interface_shape2)
                interface_shape0.translate(FreeCAD.Vector(0, 0, -inf_ut))
                interface_shape0.translate(FreeCAD.Vector(0, 0, inf_dp))
                self._cad_add_shape_to_feature_to_part("Interfaces", interface_shape0, self.infill_assembly)

    def generate_db_model(self, database_entry_id:int):
        
        self.DATABASE_ENTRY_ID = database_entry_id
        self.doc = FreeCAD.newDocument(f"MODEL_ID{self.DATABASE_ENTRY_ID}")
        
        self.db_entry = self.db.data[self.DATABASE_ENTRY_ID]
        
        # Assembly objects
        self.rc_frame_assembly = None
        self.reinf_left_column_assembly = None
        self.reinf_right_column_assembly = None
        self.reinf_beam_assembly = None
        self.reinf_base_beam_assembly = None
        self.reinf_left_column_long_assembly = None
        self.reinf_right_column_long_assembly = None
        self.reinf_beam_long_assembly = None
        self.reinf_base_beam_long_assembly = None
        self.reinf_slab_assembly = None
        self.infill_assembly = None
        self.interface_assembly = None
        self.trm_assembly = None
        self.frp_assembly = None
        self.frp_wrapping = None
        
        # Brick tracking
        self.brick_num = 1

        self._create_frame_geometry()
        self._create_reinforcement()
        self._create_infill()

    def generate_trm_infill(self,
               trm_thickness: Union[float, List] = [10, 'mm'],
               grid_spacing_h: Union[float, List] = [25, 'mm'],
               grid_spacing_v: Union[float, List] = [25, 'mm'],
               z_offset: Union[float, List]=None):
        """
        Creates TRM reinforcement on the external surface of the infill
        
        Args:
            trm_thickness: thickness of the TRM mortar layer [value, 'unit'] or value
            grid_spacing_h: horizontal spacing of textile grid [value, 'unit'] or value
            grid_spacing_v: vertical spacing of textile grid [value, 'unit'] or value
            z_offset: offset in Z direction to move the entire assembly [value, 'unit'] or value
        """
        if not z_offset:
            if self.infill_assembly:
                z_offset = self.inf_ut/2
            else:
                z_offset = 0.0

        # Parse dimensions with unit conversion
        trm_thickness = self._parse_dimension(trm_thickness)
        grid_spacing_h = self._parse_dimension(grid_spacing_h)
        grid_spacing_v = self._parse_dimension(grid_spacing_v)
        z_offset = self._parse_dimension(z_offset)
        
        self.trm_assembly = self._cad_create_part(label="TRM_Reinforcement_Assembly")


        # RETRIEVE DATA
        frm_in_h = self.frm_in_h 
        bm_h = self.bm_h
        frm_l = self.frm_l
        inf_dp = self.inf_dp
        inf_ut = self.inf_ut
        col_h = self.col_h
        frm_in_l = self.frm_in_l

        
        # Calculate TRM coverage area - from base beam top to TOP of beam
        trm_height = frm_in_h + bm_h  # Full height including beam
        trm_width = frm_l  # Full width including columns
        
        # Z position with offset
        z_pos = inf_dp - inf_ut - trm_thickness + z_offset
        z_grid_pos = inf_dp - inf_ut - trm_thickness/2 + z_offset
        
        # Create solid mortar layer
        mortar_layer = Part.makeBox(trm_width, trm_height, trm_thickness)
        mortar_layer.translate(FreeCAD.Vector(-col_h, 0, z_pos))
        self._cad_add_shape_to_feature_to_part("TRM_Mortar", mortar_layer, self.trm_assembly)
        
        # Create horizontal grid lines (as lines, not solid)
        h_grid_num = 1
        num_h_lines = int(trm_height / grid_spacing_v) + 1
        for i in range(num_h_lines):
            y_pos = i * grid_spacing_v
            if y_pos <= trm_height:
                # Create line from start to end
                start_point = FreeCAD.Vector(-col_h, y_pos, z_grid_pos)
                end_point = FreeCAD.Vector(-col_h + trm_width, y_pos, z_grid_pos)
                h_line = Part.LineSegment(start_point, end_point).toShape()
                self._cad_add_shape_to_feature_to_part(f"TRM_H_Grid_{h_grid_num}", h_line, self.trm_assembly)
                h_grid_num += 1
        
        # Create vertical grid lines (as lines, not solid) with 270° rotation
        v_grid_num = 1
        num_v_lines = int(trm_width / grid_spacing_h) + 1
        for i in range(num_v_lines):
            x_pos = -col_h + i * grid_spacing_h
            if x_pos <= frm_in_l + col_h:
                # Create line from bottom to top
                start_point = FreeCAD.Vector(x_pos, 0, z_grid_pos)
                end_point = FreeCAD.Vector(x_pos, trm_height, z_grid_pos)
                v_line = Part.LineSegment(start_point, end_point).toShape()
                self._cad_add_shape_to_feature_to_part(f"TRM_V_Grid_{v_grid_num}", v_line, self.trm_assembly)
                v_grid_num += 1
        
    def generate_frp_infill(self,
               anchor_extension_z: Union[float, List] = [50, 'mm'],
               z_offset: Union[float, List] = None):
        """ 
        Creates FRP shell strengthening on the external face of the infill
        Edge strips extend in Z direction (into wall) for anchoring into frame
        
        Parameters:
            anchor_extension_z: how much edge strips extend in Z direction for anchoring
            z_offset: offset in Z direction to position the shell
        """
        if not z_offset:
            if self.infill_assembly:
                z_offset = self.inf_ut/2
            else:
                z_offset = 0.0

        anchor_extension_z = self._parse_dimension(anchor_extension_z)
        z_offset = self._parse_dimension(z_offset)

        self.frp_assembly = self._cad_create_part(label="FRP_Infill_Strengthening_Assembly")
        
        # Shell covers clean infill region
        shell_width = self.inf_l
        shell_height = self.inf_h
        
        # Starting position
        x_start = self.inf_interface_left
        y_start = self.inf_interface_bottom
        
        # Z position with offset (on external face of infill)
        z_pos = self.inf_dp - self.inf_ut + z_offset
        z_anchor_end = z_pos + anchor_extension_z  # Extension goes deeper into wall
        
        # Create main FRP shell (2D surface)
        main_shell_points = [
            FreeCAD.Vector(x_start, y_start, z_pos),
            FreeCAD.Vector(x_start + shell_width, y_start, z_pos),
            FreeCAD.Vector(x_start + shell_width, y_start + shell_height, z_pos),
            FreeCAD.Vector(x_start, y_start + shell_height, z_pos),
            FreeCAD.Vector(x_start, y_start, z_pos)
        ]
        main_wire = Part.makePolygon(main_shell_points)
        frp_main = Part.Face(main_wire)
        
        # Create bottom anchor strip (extends in Z direction)
        bottom_anchor_points = [
            FreeCAD.Vector(x_start, y_start, z_pos),
            FreeCAD.Vector(x_start + shell_width, y_start, z_pos),
            FreeCAD.Vector(x_start + shell_width, y_start, z_anchor_end),
            FreeCAD.Vector(x_start, y_start, z_anchor_end),
            FreeCAD.Vector(x_start, y_start, z_pos)
        ]
        bottom_wire = Part.makePolygon(bottom_anchor_points)
        frp_bottom = Part.Face(bottom_wire)
        
        # Create top anchor strip (extends in Z direction)
        top_anchor_points = [
            FreeCAD.Vector(x_start, y_start + shell_height, z_pos),
            FreeCAD.Vector(x_start + shell_width, y_start + shell_height, z_pos),
            FreeCAD.Vector(x_start + shell_width, y_start + shell_height, z_anchor_end),
            FreeCAD.Vector(x_start, y_start + shell_height, z_anchor_end),
            FreeCAD.Vector(x_start, y_start + shell_height, z_pos)
        ]
        top_wire = Part.makePolygon(top_anchor_points)
        frp_top = Part.Face(top_wire)
        
        # Create left anchor strip (extends in Z direction)
        left_anchor_points = [
            FreeCAD.Vector(x_start, y_start, z_pos),
            FreeCAD.Vector(x_start, y_start + shell_height, z_pos),
            FreeCAD.Vector(x_start, y_start + shell_height, z_anchor_end),
            FreeCAD.Vector(x_start, y_start, z_anchor_end),
            FreeCAD.Vector(x_start, y_start, z_pos)
        ]
        left_wire = Part.makePolygon(left_anchor_points)
        frp_left = Part.Face(left_wire)
        
        # Create right anchor strip (extends in Z direction)
        right_anchor_points = [
            FreeCAD.Vector(x_start + shell_width, y_start, z_pos),
            FreeCAD.Vector(x_start + shell_width, y_start + shell_height, z_pos),
            FreeCAD.Vector(x_start + shell_width, y_start + shell_height, z_anchor_end),
            FreeCAD.Vector(x_start + shell_width, y_start, z_anchor_end),
            FreeCAD.Vector(x_start + shell_width, y_start, z_pos)
        ]
        right_wire = Part.makePolygon(right_anchor_points)
        frp_right = Part.Face(right_wire)
        
        # Add all components
        self._cad_add_shape_to_feature_to_part("FRP_Main_Shell", frp_main, self.frp_assembly)
        self._cad_add_shape_to_feature_to_part("FRP_Bottom_Anchor", frp_bottom, self.frp_assembly)
        self._cad_add_shape_to_feature_to_part("FRP_Top_Anchor", frp_top, self.frp_assembly)
        self._cad_add_shape_to_feature_to_part("FRP_Left_Anchor", frp_left, self.frp_assembly)
        self._cad_add_shape_to_feature_to_part("FRP_Right_Anchor", frp_right, self.frp_assembly)
        
    def generate_frp_beam_column(self,
               wrap_columns: bool = True,
               column_bottom_length: Union[float, List] = [300, 'mm'],
               column_top_length: Union[float, List] = [300, 'mm'],
               beam_flexural: bool = False,
               beam_flexural_length: Optional[Union[float, List]] = None,
               beam_flexural_center: bool = False,
               beam_shear_left: bool = True,
               beam_shear_left_length: Union[float, List] = [300, 'mm'],
               beam_shear_right: bool = True,
               beam_shear_right_length: Union[float, List] = [300, 'mm']):
        """
        Creates FRP shell strengthening for columns and beams
        
        Parameters:
            wrap_columns: wrap columns (bool)
            column_bottom_length: length of bottom column wrapping from base
            column_top_length: length of top column wrapping from beam
            beam_flexural: create flexural strengthening (bottom only)
            beam_flexural_length: length of flexural strengthening (None = full)
            beam_flexural_center: center the flexural strengthening
            beam_shear_left: create left shear strengthening (U-shape)
            beam_shear_left_length: length of left shear region
            beam_shear_right: create right shear strengthening (U-shape)
            beam_shear_right_length: length of right shear region
        """

        column_bottom_length = self._parse_dimension(column_bottom_length)
        column_top_length = self._parse_dimension(column_top_length)
        beam_shear_left_length = self._parse_dimension(beam_shear_left_length)
        beam_shear_right_length = self._parse_dimension(beam_shear_right_length)
        
        if beam_flexural_length is not None:
            beam_flexural_length = self._parse_dimension(beam_flexural_length)
        else:
            beam_flexural_length = None

        self.frp_wrapping = self._cad_create_part(label="FRP_Column_Beam_Strengthening_Assembly")

        #### RETRIEVE DATA ####
        col_h = self.col_h
        col_d = self.col_d
        bm_h = self.bm_h
        bm_t = self.bm_t

        frm_in_l = self.frm_in_l
        frm_in_h = self.frm_in_h
        #### RETRIEVE DATA ####


        # ==== COLUMN BOTTOM REGION (all 4 faces) ====
        if wrap_columns and column_bottom_length > 0:
            # Bottom wrapping for LEFT column
            # Left face
            pts = [
                FreeCAD.Vector(-col_h, 0, -col_d/2),
                FreeCAD.Vector(-col_h, column_bottom_length, -col_d/2),
                FreeCAD.Vector(-col_h, column_bottom_length, col_d/2),
                FreeCAD.Vector(-col_h, 0, col_d/2),
                FreeCAD.Vector(-col_h, 0, -col_d/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Left_Col_Bottom_Left", shell, self.frp_wrapping)
            
            # Right face (inside)
            pts = [
                FreeCAD.Vector(0, 0, -col_d/2),
                FreeCAD.Vector(0, column_bottom_length, -col_d/2),
                FreeCAD.Vector(0, column_bottom_length, col_d/2),
                FreeCAD.Vector(0, 0, col_d/2),
                FreeCAD.Vector(0, 0, -col_d/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Left_Col_Bottom_Right", shell, self.frp_wrapping)
            
            # Front face
            pts = [
                FreeCAD.Vector(-col_h, 0, -col_d/2),
                FreeCAD.Vector(-col_h, column_bottom_length, -col_d/2),
                FreeCAD.Vector(0, column_bottom_length, -col_d/2),
                FreeCAD.Vector(0, 0, -col_d/2),
                FreeCAD.Vector(-col_h, 0, -col_d/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Left_Col_Bottom_Front", shell, self.frp_wrapping)
            
            # Back face
            pts = [
                FreeCAD.Vector(-col_h, 0, col_d/2),
                FreeCAD.Vector(-col_h, column_bottom_length, col_d/2),
                FreeCAD.Vector(0, column_bottom_length, col_d/2),
                FreeCAD.Vector(0, 0, col_d/2),
                FreeCAD.Vector(-col_h, 0, col_d/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Left_Col_Bottom_Back", shell, self.frp_wrapping)
            
            # Bottom wrapping for RIGHT column
            # Left face (inside)
            pts = [
                FreeCAD.Vector(frm_in_l, 0, -col_d/2),
                FreeCAD.Vector(frm_in_l, column_bottom_length, -col_d/2),
                FreeCAD.Vector(frm_in_l, column_bottom_length, col_d/2),
                FreeCAD.Vector(frm_in_l, 0, col_d/2),
                FreeCAD.Vector(frm_in_l, 0, -col_d/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Right_Col_Bottom_Left", shell, self.frp_wrapping)
            
            # Right face
            pts = [
                FreeCAD.Vector(frm_in_l + col_h, 0, -col_d/2),
                FreeCAD.Vector(frm_in_l + col_h, column_bottom_length, -col_d/2),
                FreeCAD.Vector(frm_in_l + col_h, column_bottom_length, col_d/2),
                FreeCAD.Vector(frm_in_l + col_h, 0, col_d/2),
                FreeCAD.Vector(frm_in_l + col_h, 0, -col_d/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Right_Col_Bottom_Right", shell, self.frp_wrapping)
            
            # Front face
            pts = [
                FreeCAD.Vector(frm_in_l, 0, -col_d/2),
                FreeCAD.Vector(frm_in_l, column_bottom_length, -col_d/2),
                FreeCAD.Vector(frm_in_l + col_h, column_bottom_length, -col_d/2),
                FreeCAD.Vector(frm_in_l + col_h, 0, -col_d/2),
                FreeCAD.Vector(frm_in_l, 0, -col_d/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Right_Col_Bottom_Front", shell, self.frp_wrapping)
            
            # Back face
            pts = [
                FreeCAD.Vector(frm_in_l, 0, col_d/2),
                FreeCAD.Vector(frm_in_l, column_bottom_length, col_d/2),
                FreeCAD.Vector(frm_in_l + col_h, column_bottom_length, col_d/2),
                FreeCAD.Vector(frm_in_l + col_h, 0, col_d/2),
                FreeCAD.Vector(frm_in_l, 0, col_d/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Right_Col_Bottom_Back", shell, self.frp_wrapping)
        
        # ==== COLUMN TOP REGION (all 4 faces) ====
        if wrap_columns and column_top_length > 0:
            top_start_y = frm_in_h - column_top_length
            
            # Top wrapping for LEFT column
            # Left face
            pts = [
                FreeCAD.Vector(-col_h, top_start_y, -col_d/2),
                FreeCAD.Vector(-col_h, frm_in_h, -col_d/2),
                FreeCAD.Vector(-col_h, frm_in_h, col_d/2),
                FreeCAD.Vector(-col_h, top_start_y, col_d/2),
                FreeCAD.Vector(-col_h, top_start_y, -col_d/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Left_Col_Top_Left", shell, self.frp_wrapping)
            
            # Right face
            pts = [
                FreeCAD.Vector(0, top_start_y, -col_d/2),
                FreeCAD.Vector(0, frm_in_h, -col_d/2),
                FreeCAD.Vector(0, frm_in_h, col_d/2),
                FreeCAD.Vector(0, top_start_y, col_d/2),
                FreeCAD.Vector(0, top_start_y, -col_d/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Left_Col_Top_Right", shell, self.frp_wrapping)
            
            # Front face
            pts = [
                FreeCAD.Vector(-col_h, top_start_y, -col_d/2),
                FreeCAD.Vector(-col_h, frm_in_h, -col_d/2),
                FreeCAD.Vector(0, frm_in_h, -col_d/2),
                FreeCAD.Vector(0, top_start_y, -col_d/2),
                FreeCAD.Vector(-col_h, top_start_y, -col_d/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Left_Col_Top_Front", shell, self.frp_wrapping)
            
            # Back face
            pts = [
                FreeCAD.Vector(-col_h, top_start_y, col_d/2),
                FreeCAD.Vector(-col_h, frm_in_h, col_d/2),
                FreeCAD.Vector(0, frm_in_h, col_d/2),
                FreeCAD.Vector(0, top_start_y, col_d/2),
                FreeCAD.Vector(-col_h, top_start_y, col_d/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Left_Col_Top_Back", shell, self.frp_wrapping)
            
            # Top wrapping for RIGHT column
            # Left face
            pts = [
                FreeCAD.Vector(frm_in_l, top_start_y, -col_d/2),
                FreeCAD.Vector(frm_in_l, frm_in_h, -col_d/2),
                FreeCAD.Vector(frm_in_l, frm_in_h, col_d/2),
                FreeCAD.Vector(frm_in_l, top_start_y, col_d/2),
                FreeCAD.Vector(frm_in_l, top_start_y, -col_d/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Right_Col_Top_Left", shell, self.frp_wrapping)
            
            # Right face
            pts = [
                FreeCAD.Vector(frm_in_l + col_h, top_start_y, -col_d/2),
                FreeCAD.Vector(frm_in_l + col_h, frm_in_h, -col_d/2),
                FreeCAD.Vector(frm_in_l + col_h, frm_in_h, col_d/2),
                FreeCAD.Vector(frm_in_l + col_h, top_start_y, col_d/2),
                FreeCAD.Vector(frm_in_l + col_h, top_start_y, -col_d/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Right_Col_Top_Right", shell, self.frp_wrapping)
            
            # Front face
            pts = [
                FreeCAD.Vector(frm_in_l, top_start_y, -col_d/2),
                FreeCAD.Vector(frm_in_l, frm_in_h, -col_d/2),
                FreeCAD.Vector(frm_in_l + col_h, frm_in_h, -col_d/2),
                FreeCAD.Vector(frm_in_l + col_h, top_start_y, -col_d/2),
                FreeCAD.Vector(frm_in_l, top_start_y, -col_d/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Right_Col_Top_Front", shell, self.frp_wrapping)
            
            # Back face
            pts = [
                FreeCAD.Vector(frm_in_l, top_start_y, col_d/2),
                FreeCAD.Vector(frm_in_l, frm_in_h, col_d/2),
                FreeCAD.Vector(frm_in_l + col_h, frm_in_h, col_d/2),
                FreeCAD.Vector(frm_in_l + col_h, top_start_y, col_d/2),
                FreeCAD.Vector(frm_in_l, top_start_y, col_d/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Right_Col_Top_Back", shell, self.frp_wrapping)
        
        # ==== BEAM FLEXURAL (bottom surface only) ====
        if beam_flexural:
            if beam_flexural_length is None:
                flex_len = frm_in_l
                flex_start_x = 0
            else:
                flex_len = beam_flexural_length
                if beam_flexural_center:
                    flex_start_x = (frm_in_l - beam_flexural_length) / 2
                else:
                    flex_start_x = 0
            
            pts = [
                FreeCAD.Vector(flex_start_x, frm_in_h, -bm_t/2),
                FreeCAD.Vector(flex_start_x + flex_len, frm_in_h, -bm_t/2),
                FreeCAD.Vector(flex_start_x + flex_len, frm_in_h, bm_t/2),
                FreeCAD.Vector(flex_start_x, frm_in_h, bm_t/2),
                FreeCAD.Vector(flex_start_x, frm_in_h, -bm_t/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Beam_Flexural", shell, self.frp_wrapping)
        
        # ==== BEAM SHEAR LEFT (U-shape) ====
        if beam_shear_left and beam_shear_left_length > 0:
            # Bottom
            pts = [
                FreeCAD.Vector(0, frm_in_h, -bm_t/2),
                FreeCAD.Vector(beam_shear_left_length, frm_in_h, -bm_t/2),
                FreeCAD.Vector(beam_shear_left_length, frm_in_h, bm_t/2),
                FreeCAD.Vector(0, frm_in_h, bm_t/2),
                FreeCAD.Vector(0, frm_in_h, -bm_t/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Beam_Shear_Left_Bottom", shell, self.frp_wrapping)
            
            # Left side
            pts = [
                FreeCAD.Vector(0, frm_in_h, -bm_t/2),
                FreeCAD.Vector(beam_shear_left_length, frm_in_h, -bm_t/2),
                FreeCAD.Vector(beam_shear_left_length, frm_in_h + bm_h, -bm_t/2),
                FreeCAD.Vector(0, frm_in_h + bm_h, -bm_t/2),
                FreeCAD.Vector(0, frm_in_h, -bm_t/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Beam_Shear_Left_Side1", shell, self.frp_wrapping)
            
            # Right side
            pts = [
                FreeCAD.Vector(0, frm_in_h, bm_t/2),
                FreeCAD.Vector(beam_shear_left_length, frm_in_h, bm_t/2),
                FreeCAD.Vector(beam_shear_left_length, frm_in_h + bm_h, bm_t/2),
                FreeCAD.Vector(0, frm_in_h + bm_h, bm_t/2),
                FreeCAD.Vector(0, frm_in_h, bm_t/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Beam_Shear_Left_Side2", shell, self.frp_wrapping)
        
        # ==== BEAM SHEAR RIGHT (U-shape) ====
        if beam_shear_right and beam_shear_right_length > 0:
            right_start = frm_in_l - beam_shear_right_length
            
            # Bottom
            pts = [
                FreeCAD.Vector(right_start, frm_in_h, -bm_t/2),
                FreeCAD.Vector(frm_in_l, frm_in_h, -bm_t/2),
                FreeCAD.Vector(frm_in_l, frm_in_h, bm_t/2),
                FreeCAD.Vector(right_start, frm_in_h, bm_t/2),
                FreeCAD.Vector(right_start, frm_in_h, -bm_t/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Beam_Shear_Right_Bottom", shell, self.frp_wrapping)
            
            # Left side
            pts = [
                FreeCAD.Vector(right_start, frm_in_h, -bm_t/2),
                FreeCAD.Vector(frm_in_l, frm_in_h, -bm_t/2),
                FreeCAD.Vector(frm_in_l, frm_in_h + bm_h, -bm_t/2),
                FreeCAD.Vector(right_start, frm_in_h + bm_h, -bm_t/2),
                FreeCAD.Vector(right_start, frm_in_h, -bm_t/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Beam_Shear_Right_Side1", shell, self.frp_wrapping)
            
            # Right side
            pts = [
                FreeCAD.Vector(right_start, frm_in_h, bm_t/2),
                FreeCAD.Vector(frm_in_l, frm_in_h, bm_t/2),
                FreeCAD.Vector(frm_in_l, frm_in_h + bm_h, bm_t/2),
                FreeCAD.Vector(right_start, frm_in_h + bm_h, bm_t/2),
                FreeCAD.Vector(right_start, frm_in_h, bm_t/2)
            ]
            shell = Part.Face(Part.makePolygon(pts))
            self._cad_add_shape_to_feature_to_part("FRP_Beam_Shear_Right_Side2", shell, self.frp_wrapping)
        
    def export_model(self, file_name=None):
        """
        Export the model to STEP format
        """

        if not file_name:
            file_name = f"{self.DATABASE_NAME}_model_id_{self.DATABASE_ENTRY_ID}"

        export_path = self.CAD_FOLDER_PATH + file_name + ".step"
        exported_objects = [
            self.rc_frame_assembly, 
            self.reinf_left_column_assembly, 
            self.reinf_right_column_assembly, 
            self.reinf_beam_assembly, 
            self.reinf_base_beam_assembly,
            self.reinf_left_column_long_assembly,  
            self.reinf_right_column_long_assembly,
            self.reinf_beam_long_assembly, 
            self.reinf_base_beam_long_assembly,
            self.reinf_slab_assembly,
            self.infill_assembly,
            self.interface_assembly,
            self.trm_assembly,
            self.frp_assembly,
            self.frp_wrapping
        ]
        
        # Filter out None values
        exported_objects = [obj for obj in exported_objects if obj is not None]
        
        Import.export(exported_objects, export_path)
        print(f"Model Created: {export_path}")
        return export_path

