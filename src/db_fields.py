RCF_FIELD_CONFIG = {
            # ============================================================================
            # REFERENCE GROUP - Basic identification
            # ============================================================================
            "specimen_id": {
                "group": "reference", "sub_group": "", "unit": None, "unit_type": None, "data_type": "str", 
                "explanation": "The name of the specimen defined in the manuscript"
            },
            "specimen_scale": {
                "group": "reference", "sub_group": "", "unit": None, "unit_type": None, "data_type": "float", 
                "explanation": "The scale of the specimen defined in the manuscript (1, 0.5, 0.1, ... etc)"
            },
            "source": {
                "group": "reference", "sub_group": "", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "Site for reference source (webpage or doi)"
            },
            "title": {
                "group": "reference", "sub_group": "", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "Title of the reference source"
            },
            "authors": {
                "group": "reference", "sub_group": "", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "List of authors for the reference source (comma-separated string)"
            },
            "year": {
                "group": "reference", "sub_group": "", "unit": None, "unit_type": None, "data_type": "int",
                "explanation": "Publication year of the reference source"
            },
            
            # ============================================================================
            # FRAME GEOMETRY GROUP
            # ============================================================================
            
            # Basic frame dimensions
            "frm_h": {
                "group": "frame_geometry", "sub_group": "", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Height of the frame calculated from the top surface of the base_beam to the top surface of the top_beam. (also known as floor to floor height)"
            },
            "frm_l": {
                "group": "frame_geometry", "sub_group": "", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Length of the frame calculated from the external surfaces of the columns."
            },
            
            # Column rectangle cross section
            "col_h": {
                "group": "frame_geometry", "sub_group": "column_rectangle_cross_section", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Column dimension parallel to frame plane"
            },
            "col_d": {
                "group": "frame_geometry", "sub_group": "column_rectangle_cross_section", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Column dimension perpendicular to frame plane"
            },
            
            # Beam rectangle cross section
            "bm_h": {
                "group": "frame_geometry", "sub_group": "beam_rectangle_cross_section", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Beam height"
            },
            "bm_t": {
                "group": "frame_geometry", "sub_group": "beam_rectangle_cross_section", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Beam thickness"
            },

            # Base_Beam rectangle cross section
            "bbm_h": {
                "group": "frame_geometry", "sub_group": "base_beam_rectangle_cross_section", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Base_Beam height"
            },
            "bbm_t": {
                "group": "frame_geometry", "sub_group": "base_beam_rectangle_cross_section", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Base_Beam thickness"
            },
            
            # Slab section
            "slb_d": {
                "group": "frame_geometry", "sub_group": "slab_section", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Slab Depth (dimension perpendicular to frame plane)"
            },
            "slb_h": {
                "group": "frame_geometry", "sub_group": "slab_section", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Slab height (dimension parallel to frame plane)"
            },
            
            # Extensions
            "col_ext": {
                "group": "frame_geometry", "sub_group": "extensions", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Column extension above Beam top surface"
            },
            "bm_ext": {
                "group": "frame_geometry", "sub_group": "extensions", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Beam extension outside the external surfaces of the columns"
            },
            "bbm_ext": {
                "group": "frame_geometry", "sub_group": "extensions", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Base Beam extension outside the external surfaces of the columns"
            },
            
            # ============================================================================
            # INFILL GEOMETRY GROUP
            # ============================================================================
            
            # Basic infill properties
            "inf_type": {
                "group": "infill_geometry", "sub_group": "", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "1. one_wythe 2. two_wythe 3. none"
            },
            "inf_opn_type": {
                "group": "infill_geometry", "sub_group": "Openings", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "1. window 2. door 3. mix 4. none"
            },
            
            # Opening dimensions
            "inf_win_h": {
                "group": "infill_geometry", "sub_group": "Openings", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Window horizontal dimension (length)"
            },
            "inf_win_v": {
                "group": "infill_geometry", "sub_group": "Openings", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Window vertical dimension (height)"
            },
            "inf_win_ph": {
                "group": "infill_geometry", "sub_group": "Openings", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Window horizontal position from main reference point"
            },
            "inf_win_pv": {
                "group": "infill_geometry", "sub_group": "Openings", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Window vertical position from main reference point"
            },

            "inf_door_h": {
                "group": "infill_geometry", "sub_group": "Openings", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Door horizontal dimension (length)"
            },
            "inf_door_v": {
                "group": "infill_geometry", "sub_group": "Openings", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Door vertical dimension (height)"
            },
            "inf_door_ph": {
                "group": "infill_geometry", "sub_group": "Openings", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Door horizontal position from main reference point"
            },
            "inf_door_pv": {
                "group": "infill_geometry", "sub_group": "Openings", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Door vertical position from main reference point"
            },
            
            
            # Infill properties
            "inf_dp": {
                "group": "infill_geometry", "sub_group": "first_wythe", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Infill depth from the main reference point"
            },
            "inf_bnd_pat": {
                "group": "infill_geometry", "sub_group": "first_wythe", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "Infill bond pattern  1. running 2. stack"
            },
            "inf_inff_intfc": {
                "group": "infill_geometry", "sub_group": "interface_information", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "Infill infill frame interface condition info  1. mortar_bond  2. seismic_joint 3. dowels 4. gap"
            },
            
            # Infill interface information
            "inf_interface_bottom": {
                "group": "infill_geometry", "sub_group": "interface_information", "unit": "mm", "unit_type": "Length", 
                "explanation": "Infill interface fill/gap dimension at bottom"
            },
            "inf_interface_left": {
                "group": "infill_geometry", "sub_group": "interface_information", "unit": "mm", "unit_type": "Length", 
                "explanation": "Infill interface fill/gap dimension at left"
            },
            "inf_interface_top": {
                "group": "infill_geometry", "sub_group": "interface_information", "unit": "mm", "unit_type": "Length", 
                "explanation": "Infill interface fill/gap dimension at top"
            },
            "inf_interface_right": {
                "group": "infill_geometry", "sub_group": "interface_information", "unit": "mm", "unit_type": "Length", 
                "explanation": "Infill interface fill/gap dimension at right"
            },
                     
            # Infill unit and joint info
            "inf_ul": {
                "group": "infill_geometry", "sub_group": "Infill unit and joint info", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Infill unit length (horizontal)"
            },
            "inf_uh": {
                "group": "infill_geometry", "sub_group": "Infill unit and joint info", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Infill unit height (vertical)"
            },
            "inf_ut": {
                "group": "infill_geometry", "sub_group": "Infill unit and joint info", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Infill unit thickness (depth)"
            },
            "inf_uhead_t": {
                "group": "infill_geometry", "sub_group": "Infill unit and joint info", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Infill head joint thickness (vertical)"
            },
            "inf_ubed_t": {
                "group": "infill_geometry", "sub_group": "Infill unit and joint info", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Infill bed joint thickness (horizontal)"
            },           
            
            # ============================================================================
            # REINFORCEMENT DETAILS GROUP
            # ============================================================================
            
            # Column rectangle reinforcement
            "col_cover": {
                "group": "reinforcement_details", "sub_group": "column_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Cover till the external surface of the transverse reinforcement"
            },
            "col_long_reinf_corner": {
                "group": "reinforcement_details", "sub_group": "column_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Column longitudinal reinforcement at corners (e.g., '4#20') - dimensions auto-convert"
            },
            "col_long_reinf_top": {
                "group": "reinforcement_details", "sub_group": "column_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Column longitudinal reinforcement at top (e.g., '2#16') - dimensions auto-convert"
            },
            "col_long_reinf_mid": {
                "group": "reinforcement_details", "sub_group": "column_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Column longitudinal reinforcement at mid-height (e.g., '2#16') - dimensions auto-convert"
            },
            "col_long_reinf_bot": {
                "group": "reinforcement_details", "sub_group": "column_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Column longitudinal reinforcement at bottom (e.g., '2#16') - dimensions auto-convert"
            },
            
            # Column transverse reinforcement
            "col_trans_crit_top_distance": {
                "group": "reinforcement_details", "sub_group": "column_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Column transverse reinforcement critical top region distance"
            },
            "col_trans_crit_top_reinf": {
                "group": "reinforcement_details", "sub_group": "column_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Column transverse reinforcement at critical top region (e.g., '2#8@150') - dimensions auto-convert"
            },
            "col_trans_crit_bot_distance": {
                "group": "reinforcement_details", "sub_group": "column_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Column transverse reinforcement critical bottom region distance"
            },
            "col_trans_crit_bot_reinf": {
                "group": "reinforcement_details", "sub_group": "column_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Column transverse reinforcement at critical bottom region (e.g., '2#8@150') - dimensions auto-convert"
            },
            "col_trans_mid_reinf": {
                "group": "reinforcement_details", "sub_group": "column_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Column transverse reinforcement at mid-height (e.g., '1#8@250') - dimensions auto-convert"
            },
            
            # Beam rectangle reinforcement
            "bm_cover": {
                "group": "reinforcement_details", "sub_group": "beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Cover till the external surface of the transverse reinforcement"
            },
            "bm_long_reinf_corner": {
                "group": "reinforcement_details", "sub_group": "beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Beam longitudinal reinforcement at corners (e.g., '2#20') - dimensions auto-convert"
            },
            "bm_long_reinf_top": {
                "group": "reinforcement_details", "sub_group": "beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Beam longitudinal reinforcement at top (e.g., '3#16') - dimensions auto-convert"
            },
            "bm_long_reinf_mid": {
                "group": "reinforcement_details", "sub_group": "beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Beam longitudinal reinforcement at mid-span (e.g., '2#16') - dimensions auto-convert"
            },
            "bm_long_reinf_bot": {
                "group": "reinforcement_details", "sub_group": "beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Beam longitudinal reinforcement at bottom (e.g., '3#20') - dimensions auto-convert"
            },
            "bm_trans_crit_left_distance": {
                "group": "reinforcement_details", "sub_group": "beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Beam transverse reinforcement critical ;rft region distance"
            },
            "bm_trans_crit_left_reinf": {
                "group": "reinforcement_details", "sub_group": "beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Beam transverse reinforcement at critical right region (e.g., '2#8@100') - dimensions auto-convert"
            },
            "bm_trans_crit_right_distance": {
                "group": "reinforcement_details", "sub_group": "beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Beam transverse reinforcement critical right region distance"
            },
            "bm_trans_crit_right_reinf": {
                "group": "reinforcement_details", "sub_group": "beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Beam transverse reinforcement at critical right region (e.g., '2#8@100') - dimensions auto-convert"
            },
            "bm_trans_mid_reinf": {
                "group": "reinforcement_details", "sub_group": "beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Beam transverse reinforcement at mid-span (e.g., '1#8@200') - dimensions auto-convert"
            },

            # Base_Beam rectangle reinforcement
            "bbm_cover": {
                "group": "reinforcement_details", "sub_group": "base_beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Cover till the external surface of the transverse reinforcement"
            },
            "bbm_long_reinf_corner": {
                "group": "reinforcement_details", "sub_group": "base_beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Base_Beam longitudinal reinforcement at corners (e.g., '2#20') - dimensions auto-convert"
            },
            "bbm_long_reinf_top": {
                "group": "reinforcement_details", "sub_group": "base_beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Base_Beam longitudinal reinforcement at top (e.g., '3#16') - dimensions auto-convert"
            },
            "bbm_long_reinf_mid": {
                "group": "reinforcement_details", "sub_group": "base_beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Base_Beam longitudinal reinforcement at mid-span (e.g., '2#16') - dimensions auto-convert"
            },
            "bbm_long_reinf_bot": {
                "group": "reinforcement_details", "sub_group": "base_beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Base_Beam longitudinal reinforcement at bottom (e.g., '3#20') - dimensions auto-convert"
            },
            "bbm_trans_crit_left_distance": {
                "group": "reinforcement_details", "sub_group": "base_beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Base_Beam transverse reinforcement critical left region distance"
            },
            "bbm_trans_crit_left_reinf": {
                "group": "reinforcement_details", "sub_group": "base_beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Base_Beam transverse reinforcement at critical left region (e.g., '2#8@100') - dimensions auto-convert"
            },
            "bbm_trans_crit_right_distance": {
                "group": "reinforcement_details", "sub_group": "base_beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Base_Beam transverse reinforcement critical right region distance"
            },
            "bbm_trans_crit_right_reinf": {
                "group": "reinforcement_details", "sub_group": "base_beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Base_Beam transverse reinforcement at critical right region (e.g., '2#8@100') - dimensions auto-convert"
            },
            "bbm_trans_mid_reinf": {
                "group": "reinforcement_details", "sub_group": "base_beam_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Base_Beam transverse reinforcement at mid-span (e.g., '1#8@200') - dimensions auto-convert"
            },
            
            # Slab rectangle reinforcement
            "slb_cover": {
                "group": "reinforcement_details", "sub_group": "slab_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "float",
                "explanation": "Slab cover"
            },
            "slb_top_l_reinf": {
                "group": "reinforcement_details", "sub_group": "slab_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Slab Top reinforcement parallel to frame plane (e.g., '#12@200') - dimensions auto-convert"
            },
            "slb_top_d_reinf": {
                "group": "reinforcement_details", "sub_group": "slab_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Slab Top reinforcement perpendicular to frame plane (e.g., '#12@250') - dimensions auto-convert"
            },
            "slb_bot_l_reinf": {
                "group": "reinforcement_details", "sub_group": "slab_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Slab Bottom reinforcement parallel to frame plane (e.g., '#12@200') - dimensions auto-convert"
            },
            "slb_bot_d_reinf": {
                "group": "reinforcement_details", "sub_group": "slab_rectangle_reinforcement", "unit": "mm", "unit_type": "Length", "data_type": "str",
                "explanation": "Slab Bottom reinforcement perpendicular to frame plane (e.g., '#12@250') - dimensions auto-convert"
            },
            
            # ============================================================================
            # CONCRETE PROPERTIES GROUP
            # ============================================================================
            "fc": {
                "group": "concrete_properties", "sub_group": "", "unit": "MPa", "unit_type": "Pressure", "data_type": "float",
                "explanation": "Concrete compressive strength"
            },
            "Ec": {
                "group": "concrete_properties", "sub_group": "", "unit": "GPa", "unit_type": "Pressure", "data_type": "float",
                "explanation": "Concrete modulus of elasticity"
            },
            "conc_prop_day": {
                "group": "concrete_properties", "sub_group": "", "unit": "day", "unit_type": "Time", "data_type": "float",
                "explanation": "Concrete properties test age"
            },
            "conc_density": {
                "group": "concrete_properties", "sub_group": "", "unit": "kg/m^3", "unit_type": "Density", "data_type": "float",
                "explanation": "Concrete density"
            },
            
            # ============================================================================
            # STEEL PROPERTIES GROUP
            # ============================================================================
            "fy": {
                "group": "steel_properties", "sub_group": "", "unit": "MPa", "unit_type": "Pressure", "data_type": "float",
                "explanation": "Steel yield strength"
            },
            "fu": {
                "group": "steel_properties", "sub_group": "", "unit": "MPa", "unit_type": "Pressure", "data_type": "float",
                "explanation": "Steel ultimate strength"
            },
            "Ey": {
                "group": "steel_properties", "sub_group": "", "unit": "GPa", "unit_type": "Pressure", "data_type": "float",
                "explanation": "Steel modulus of elasticity"
            },
            "stl_density": {
                "group": "steel_properties", "sub_group": "", "unit": "kg/m^3", "unit_type": "Density", "data_type": "float",
                "explanation": "Steel density"
            },
            
            # ============================================================================
            # INFILL MECHANICAL PROPERTIES
            # ============================================================================
            "inf_unit_density": {
                "group": "infill_mechanical_properties", "sub_group": "infill_mechanical_properties", "unit": "kg/m^3", "unit_type": "Density", "data_type": "float",
                "explanation": "Infill unit density"
            },
            "inf_mortar_density": {
                "group": "infill_mechanical_properties", "sub_group": "infill_mechanical_properties", "unit": "kg/m^3", "unit_type": "Density", "data_type": "float",
                "explanation": "Infill mortar density"
            },
            "inf_unit_compressive_strength_length": {
                "group": "infill_mechanical_properties", "sub_group": "infill_mechanical_properties", "unit": "MPa", "unit_type": "Pressure", "data_type": "float",
                "explanation": "Infill unit compressive strength parallel to length"
            },
            "inf_unit_compressive_strength_height": {
                "group": "infill_mechanical_properties", "sub_group": "infill_mechanical_properties", "unit": "MPa", "unit_type": "Pressure", "data_type": "float",
                "explanation": "Infill unit compressive strength parallel to height"
            },
            "inf_unit_compressive_strength_width": {
                "group": "infill_mechanical_properties", "sub_group": "infill_mechanical_properties", "unit": "MPa", "unit_type": "Pressure", "data_type": "float",
                "explanation": "Infill unit compressive strength parallel to width"
            },
            "inf_mortar_type": {
                "group": "infill_mechanical_properties", "sub_group": "infill_mechanical_properties", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "Infill mortar type classification"
            },
            "inf_mortar_compressive_strength": {
                "group": "infill_mechanical_properties", "sub_group": "infill_mechanical_properties", "unit": "MPa", "unit_type": "Pressure", "data_type": "float",
                "explanation": "Infill mortar compressive strength"
            },
            "inf_assembly_compressive_strength_height": {
                "group": "infill_mechanical_properties", "sub_group": "infill_mechanical_properties", "unit": "MPa", "unit_type": "Pressure", "data_type": "float",
                "explanation": "Infill assembly compressive strength in height direction"
            },
            "inf_assembly_compressive_strength_diagonal": {
                "group": "infill_mechanical_properties", "sub_group": "infill_1_mechanical_properties", "unit": "MPa", "unit_type": "Pressure", "data_type": "float",
                "explanation": "Infill assembly diagonal compressive strength"
            },
            
            
            # ============================================================================
            # LOADING GROUP - IN-PLANE
            # ============================================================================
            "inp_loading_protocol": {
                "group": "loading", "sub_group": "loading_in_plane", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "In-plane loading protocol. Options. 1. monotonic 2. cyclic 3. none (not_applicable)"
            },
            "inp_cyclic_number_of_cycles": {
                "group": "loading", "sub_group": "loading_in_plane", "unit": None, "unit_type": None, "data_type": "int",
                "explanation": "In-plane number of cycles per amplitude level"
            },
            "inp_cyclic_repetition": {
                "group": "loading", "sub_group": "loading_in_plane", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "In-plane cyclic repetition pattern. Options: 1. constant  2. increasing"
            },
            "inp_cyclic_protocol": {
                "group": "loading", "sub_group": "loading_in_plane", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "In-plane cyclic protocol standard: FEMA461, ACI374, etc OR none (not_applicable)"
            },
            "inp_column_vertical_load": {
                "group": "loading", "sub_group": "loading_in_plane", "unit": "kN", "unit_type": "Concentrated_Force", "data_type": "float",
                "explanation": "In-plane column vertical load"
            },
            "inp_beam_vertical_load": {
                "group": "loading", "sub_group": "loading_in_plane", "unit": "kN/m", "unit_type": "Distributed_Force", "data_type": "float",
                "explanation": "In-plane beam distributed vertical load"
            },
            
            # ============================================================================
            # LOADING GROUP - OUT-OF-PLANE
            # ============================================================================
            "oop_loading_protocol": {
                "group": "loading", "sub_group": "loading_out_of_plane", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "Out-of-plane loading protocol. Options: 1. monotonic 2. cyclic 3. none (not_applicable)"
            },
            "oop_cyclic_number_of_cycles": {
                "group": "loading", "sub_group": "loading_out_of_plane", "unit": None, "unit_type": None, "data_type": "int",
                "explanation": "Out-of-plane number of cycles per amplitude level"
            },
            "oop_cyclic_repetition": {
                "group": "loading", "sub_group": "loading_out_of_plane", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "Out-of-plane cyclic repetition pattern. Options:  1. constant  2. increasing"
            },
            "oop_cyclic_protocol": {
                "group": "loading", "sub_group": "loading_out_of_plane", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "Out-of-plane cyclic protocol standard: FEMA461, ACI374, etc OR none (not_applicable)"
            },
            "oop_column_vertical_load": {
                "group": "loading", "sub_group": "loading_out_of_plane", "unit": "kN", "unit_type": "Concentrated_Force", "data_type": "float",
                "explanation": "Out-of-plane column vertical load"
            },
            "oop_beam_vertical_load": {
                "group": "loading", "sub_group": "loading_out_of_plane", "unit": "kN/m", "unit_type": "Distributed_Force", "data_type": "float",
                "explanation": "Out-of-plane beam distributed vertical load"
            },
            
            # ============================================================================
            # RESPONSE GROUP - GLOBAL
            # ============================================================================
            "glb_initial_stiffness": {
                "group": "response", "sub_group": "global_response", "unit": "kN/m", "unit_type": "Distributed_Force", "data_type": "float",
                "explanation": "Global initial stiffness"
            },
            "glb_peak_lateral_load": {
                "group": "response", "sub_group": "global_response", "unit": "kN", "unit_type": "Concentrated_Force", "data_type": "float",
                "explanation": "Global peak lateral load"
            },
            "glb_drift_at_peak_lateral_load": {
                "group": "response", "sub_group": "global_response", "unit": "ratio", "unit_type": "Strain", "data_type": "float",
                "explanation": "Global drift ratio at peak lateral load"
            },
            "glb_peak_lateral_drift": {
                "group": "response", "sub_group": "global_response", "unit": "ratio", "unit_type": "Strain", "data_type": "float",
                "explanation": "Global peak lateral drift ratio"
            },
            "glb_load_at_peak_lateral_drift": {
                "group": "response", "sub_group": "global_response", "unit": "kN", "unit_type": "Concentrated_Force", "data_type": "float",
                "explanation": "Global load at peak lateral drift"
            },
            "glb_energy_dissipation": {
                "group": "response", "sub_group": "global_response", "unit": "kJ", "unit_type": "Work", "data_type": "float",
                "explanation": "Global energy dissipation"
            },
            "glb_failure_mode": {
                "group": "response", "sub_group": "global_response", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "Global failure mode description"
            },
            
            # ============================================================================
            # RESPONSE GROUP - LOCAL
            # ============================================================================
            "lcl_crack_pattern": {
                "group": "response", "sub_group": "local_response", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "Local crack pattern description"
            },
            "lcl_failure_mechanism": {
                "group": "response", "sub_group": "local_response", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "Local failure mechanism description"
            },
            "lcl_damage_progression": {
                "group": "response", "sub_group": "local_response", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "Local damage progression description"
            },
            "lcl_strain_distribution": {
                "group": "response", "sub_group": "local_response", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "Local strain distribution description"
            },
            
            # ============================================================================
            # RETROFIT TECHNIQUES
            # ============================================================================
            "retrofit_techniques": {
                "group": "retrifit", "sub_group": "", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "A maximum of four (4) sentences describing retrofitting techniques applied to the specimen."
            },

            # ============================================================================
            # GENERAL COMMENTS
            # ============================================================================
            "comments": {
                "group": "comments", "sub_group": "", "unit": None, "unit_type": None, "data_type": "str",
                "explanation": "General comments for user"
            },

        }



RCF_DB_EMPTY_FIELDS = {
    # ===========================================
    # REFERENCE GROUP - Basic identification
    # ===========================================
    "specimen_id": "none", #The name of the specimen defined in the manuscript"
    "specimen_scale": 0.0,  # The scale of the specimen defined in the manuscript (1, 0.5, 0.1, ... etc)
    "source": "none",  # Site for reference source (webpage or doi)
    "title": "none",  # Title of the reference source
    "authors": "none",  # List of authors for the reference source (comma-separated string)
    "year": 0,  # Publication year of the reference source
    
    # ===========================================
    # FRAME GEOMETRY GROUP
    # ===========================================
    
    # Basic frame dimensions
    "frm_h": 0.0,  # Height of the frame calculated from the top surface of the base_beam to the top surface of the top_beam. (also known as floor to floor height)
    "frm_l": 0.0,  # Length of the frame calculated from the external surfaces of the columns.
    
    # Column rectangle cross section
    "col_h": 0.0,  # Column dimension parallel to frame plane
    "col_d": 0.0,  # Column dimension perpendicular to frame plane
    
    # Beam rectangle cross section
    "bm_h": 0.0,  # Beam height
    "bm_t": 0.0,  # Beam thickness

    # Base_Beam rectangle cross section
    "bbm_h": 0.0,  # Base_Beam height
    "bbm_t": 0.0,  # Base_Beam thickness
    
    # Slab section
    "slb_d": 0.0,  # Slab Depth (dimension perpendicular to frame plane)
    "slb_h": 0.0,  # Slab height (dimension parallel to frame plane)
    
    # Extensions
    "col_ext": 0.0,  # Column extension above Beam top surface
    "bm_ext": 0.0,  # Beam extension outside the external surfaces of the columns
    "bbm_ext": 0.0,  # Base Beam extension outside the external surfaces of the columns
    
    # ===========================================
    # INFILL GEOMETRY GROUP
    # ===========================================
    
    # Basic infill properties
    "inf_type": "none",  # 1. one_wythe 2. two_wythe 3. none
    "inf_opn_type": "none",  # 1. window 2. door 3. mix 4. none
    
    # Opening dimensions
    "inf_win_h": 0.0,  # Window horizontal dimension (length)
    "inf_win_v": 0.0,  # Window vertical dimension (height)
    "inf_win_ph": 0.0,  # Window horizontal position from main reference point
    "inf_win_pv": 0.0,  # Window vertical position from main reference point

    "inf_door_h": 0.0,  # Door horizontal dimension (length)
    "inf_door_v": 0.0,  # Door vertical dimension (height)
    "inf_door_ph": 0.0,  # Door horizontal position from main reference point
    "inf_door_pv": 0.0,  # Door vertical position from main reference point
    
    # Infill properties
    "inf_dp": 0.0,  # Infill depth from the main reference point
    "inf_bnd_pat": "none",  # Infill bond pattern  1. running 2. stack
    "inf_inff_intfc": "none",  # Infill infill frame interface condition info  1. mortar_bond  2. seismic_joint 3. dowels 4. gap
    
    # Infill interface information
    "inf_interface_bottom": 0.0,  # Infill interface fill/gap dimension at bottom
    "inf_interface_left": 0.0,  # Infill interface fill/gap dimension at left
    "inf_interface_top": 0.0,  # Infill interface fill/gap dimension at top
    "inf_interface_right": 0.0,  # Infill interface fill/gap dimension at right
             
    # Infill unit and joint info
    "inf_ul": 0.0,  # Infill unit length (horizontal)
    "inf_uh": 0.0,  # Infill unit height (vertical)
    "inf_ut": 0.0,  # Infill unit thickness (depth)
    "inf_uhead_t": 0.0,  # Infill head joint thickness (vertical)
    "inf_ubed_t": 0.0,  # Infill bed joint thickness (horizontal)
    
    # ===========================================
    # REINFORCEMENT DETAILS GROUP
    # ===========================================
    
    # Column rectangle reinforcement
    "col_cover": 0.0,  # Cover till the external surface of the transverse reinforcement
    "col_long_reinf_corner": "0#0",  # Column longitudinal reinforcement at corners (e.g., '4#20') - dimensions auto-convert
    "col_long_reinf_top": "0#0",  # Column longitudinal reinforcement at top (e.g., '2#16') - dimensions auto-convert
    "col_long_reinf_mid": "0#0",  # Column longitudinal reinforcement at mid-height (e.g., '2#16') - dimensions auto-convert
    "col_long_reinf_bot": "0#0",  # Column longitudinal reinforcement at bottom (e.g., '2#16') - dimensions auto-convert
    
    # Column transverse reinforcement
    "col_trans_crit_top_distance": 0.0,  # Column transverse reinforcement critical top region distance
    "col_trans_crit_top_reinf": "0#0@0",  # Column transverse reinforcement at critical top region (e.g., '2#8@150') - dimensions auto-convert
    "col_trans_crit_bot_distance": 0.0,  # Column transverse reinforcement critical bottom region distance
    "col_trans_crit_bot_reinf": "0#0@0",  # Column transverse reinforcement at critical bottom region (e.g., '2#8@150') - dimensions auto-convert
    "col_trans_mid_reinf": "0#0@0",  # Column transverse reinforcement at mid-height (e.g., '1#8@250') - dimensions auto-convert
    
    # Beam rectangle reinforcement
    "bm_cover": 0.0,  # Cover till the external surface of the transverse reinforcement
    "bm_long_reinf_corner": "0#0",  # Beam longitudinal reinforcement at corners (e.g., '2#20') - dimensions auto-convert
    "bm_long_reinf_top": "0#0",  # Beam longitudinal reinforcement at top (e.g., '3#16') - dimensions auto-convert
    "bm_long_reinf_mid": "0#0",  # Beam longitudinal reinforcement at mid-span (e.g., '2#16') - dimensions auto-convert
    "bm_long_reinf_bot": "0#0",  # Beam longitudinal reinforcement at bottom (e.g., '3#20') - dimensions auto-convert
    "bm_trans_crit_left_distance": 0.0,  # Beam transverse reinforcement critical left region distance
    "bm_trans_crit_left_reinf": "0#0@0",  # Beam transverse reinforcement at critical right region (e.g., '2#8@100') - dimensions auto-convert
    "bm_trans_crit_right_distance": 0.0,  # Beam transverse reinforcement critical right region distance
    "bm_trans_crit_right_reinf": "0#0@0",  # Beam transverse reinforcement at critical right region (e.g., '2#8@100') - dimensions auto-convert
    "bm_trans_mid_reinf": "0#0@0",  # Beam transverse reinforcement at mid-span (e.g., '1#8@200') - dimensions auto-convert

    # Base_Beam rectangle reinforcement
    "bbm_cover": 0.0,  # Cover till the external surface of the transverse reinforcement
    "bbm_long_reinf_corner": "0#0",  # Base_Beam longitudinal reinforcement at corners (e.g., '2#20') - dimensions auto-convert
    "bbm_long_reinf_top": "0#0",  # Base_Beam longitudinal reinforcement at top (e.g., '3#16') - dimensions auto-convert
    "bbm_long_reinf_mid": "0#0",  # Base_Beam longitudinal reinforcement at mid-span (e.g., '2#16') - dimensions auto-convert
    "bbm_long_reinf_bot": "0#0",  # Base_Beam longitudinal reinforcement at bottom (e.g., '3#20') - dimensions auto-convert
    "bbm_trans_crit_left_distance": 0.0,  # Base_Beam transverse reinforcement critical left region distance
    "bbm_trans_crit_left_reinf": "0#0@0",  # Base_Beam transverse reinforcement at critical left region (e.g., '2#8@100') - dimensions auto-convert
    "bbm_trans_crit_right_distance": 0.0,  # Base_Beam transverse reinforcement critical right region distance
    "bbm_trans_crit_right_reinf": "0#0@0",  # Base_Beam transverse reinforcement at critical right region (e.g., '2#8@100') - dimensions auto-convert
    "bbm_trans_mid_reinf": "0#0@0",  # Base_Beam transverse reinforcement at mid-span (e.g., '1#8@200') - dimensions auto-convert
    
    # Slab rectangle reinforcement
    "slb_cover": 0.0,  # Slab cover
    "slb_top_l_reinf": "0#0@0",  # Slab Top reinforcement parallel to frame plane (e.g., '#12@200') - dimensions auto-convert
    "slb_top_d_reinf": "0#0@0",  # Slab Top reinforcement perpendicular to frame plane (e.g., '#12@250') - dimensions auto-convert
    "slb_bot_l_reinf": "0#0@0",  # Slab Bottom reinforcement parallel to frame plane (e.g., '#12@200') - dimensions auto-convert
    "slb_bot_d_reinf": "0#0@0",  # Slab Bottom reinforcement perpendicular to frame plane (e.g., '#12@250') - dimensions auto-convert
    
    # ===========================================
    # CONCRETE PROPERTIES GROUP
    # ===========================================
    "fc": 0.0,  # Concrete compressive strength
    "Ec": 0.0,  # Concrete modulus of elasticity
    "conc_prop_day": 0.0,  # Concrete properties test age
    "conc_density": 0.0,  # Concrete density
    
    # ===========================================
    # STEEL PROPERTIES GROUP
    # ===========================================
    "fy": 0.0,  # Steel yield strength
    "fu": 0.0,  # Steel ultimate strength
    "Ey": 0.0,  # Steel modulus of elasticity
    "stl_density": 0.0,  # Steel density
    
    # ===========================================
    # INFILL MECHANICAL PROPERTIES
    # ===========================================
    "inf_unit_density": 0.0,  # Infill unit density
    "inf_mortar_density": 0.0,  # Infill mortar density
    "inf_unit_compressive_strength_length": 0.0,  # Infill unit compressive strength parallel to length
    "inf_unit_compressive_strength_height": 0.0,  # Infill unit compressive strength parallel to height
    "inf_unit_compressive_strength_width": 0.0,  # Infill unit compressive strength parallel to width
    "inf_mortar_type": "none",  # Infill mortar type classification
    "inf_mortar_compressive_strength": 0.0,  # Infill mortar compressive strength
    "inf_assembly_compressive_strength_height": 0.0,  # Infill assembly compressive strength in height direction
    "inf_assembly_compressive_strength_diagonal": 0.0,  # Infill assembly diagonal compressive strength
    
    
    # ===========================================
    # LOADING GROUP - IN-PLANE
    # ===========================================
    "inp_loading_protocol": "none",  # In-plane loading protocol. Options: 1. monotonic 2. cyclic 3. none (not_applicable)
    "inp_cyclic_number_of_cycles": 0,  # In-plane number of cycles per amplitude level
    "inp_cyclic_repetition": "none",  # In-plane cyclic repetition pattern. Options: 1. constant  2. increasing
    "inp_cyclic_protocol": "none",  # In-plane cyclic protocol standard: FEMA461, ACI374, etc none (not_applicable)
    "inp_column_vertical_load": 0.0,  # In-plane column vertical load
    "inp_beam_vertical_load": 0.0,  # In-plane beam distributed vertical load
    
    # ===========================================
    # LOADING GROUP - OUT-OF-PLANE
    # ===========================================
    "oop_loading_protocol": "none",  # Out-of-plane loading protocol. Options: 1. monotonic 2. cyclic 3. none (not_applicable)
    "oop_cyclic_number_of_cycles": 0,  # Out-of-plane number of cycles per amplitude level
    "oop_cyclic_repetition": "none",  # Out-of-plane cyclic repetition pattern. Options:  1. constant  2. increasing
    "oop_cyclic_protocol": "none",  # Out-of-plane cyclic protocol standard: FEMA461, ACI374, etc OR none (not_applicable)
    "oop_column_vertical_load": 0.0,  # Out-of-plane column vertical load
    "oop_beam_vertical_load": 0.0,  # Out-of-plane beam distributed vertical load
    
    # ===========================================
    # RESPONSE GROUP - GLOBAL
    # ===========================================
    "glb_initial_stiffness": 0.0,  # Global initial stiffness
    "glb_peak_lateral_load": 0.0,  # Global peak lateral load
    "glb_drift_at_peak_lateral_load": 0.0,  # Global drift ratio at peak lateral load
    "glb_peak_lateral_drift": 0.0,  # Global peak lateral drift ratio
    "glb_load_at_peak_lateral_drift": 0.0,  # Global load at peak lateral drift
    "glb_energy_dissipation": 0.0,  # Global energy dissipation
    "glb_failure_mode": "none",  # Global failure mode description
    
    # ===========================================
    # RESPONSE GROUP - LOCAL
    # ===========================================
    "lcl_crack_pattern": "none",  # Local crack pattern description
    "lcl_failure_mechanism": "none",  # Local failure mechanism description
    "lcl_damage_progression": "none",  # Local damage progression description
    "lcl_strain_distribution": "none",  # Local strain distribution description
    
    # ===========================================
    # RETROFIT TECHNIQUES
    # ===========================================
    "retrofit_techniques": "none",  # A maximum of four (4) sentences describing retrofitting techniques applied to the specimen.
    
    # ===========================================
    # GENERAL COMMENTS
    # ===========================================
    "comments": "none"  # General comments for user
}