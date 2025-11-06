# ============================================================================================================
# This is the third example for using the FRESCO Database
# Details of the manuscript 
#    - Status: Open Access
#    - Title: FRESCO: An Open Database for Fiber and Polymer Strengthening of Infilled RC Frame Systems
#    - Authors: Vachan Vanian, Theodoros Rousakis
#    - Year: 2025
#    - DOI: TODO AFTER PUBLICATION
#
# ------------------------------------------------------------------------------------------------------------
#
# The original specimen is from webpage: TODO AFTER PUBLICATION
# Details of the source manuscript (specimen origin)
#    - Status: Open Access
#    - Title: Experimental Evaluation of RC Structures with Brick Infills for Vertical Forest Adaptation in Seismic regions
#    - Authors: Theodoros Rousakis, Vachan Vanian, Martha Lappa, Adamantis G. Zapris, Ioannis P. Xynopoulos, 
#               Maristella Voutetaki, Stefanos Kellis, Georgios Sapidis, Maria Naoum, Nikolaos Papadopoulos, 
#               Violetta K. Kytinou, Martha Karampini, Constantin E. Chalioris, Athanasia Thomoglou, Emmanouil Golias
#    - Year: 2025
# ============================================================================================================


entry_rousakis_et_al_2025 = {
    # ===========================================
    # REFERENCE GROUP - Basic identification
    # ===========================================
    "specimen_id": "GREENERGY-1",  # The name of the specimen defined in the manuscript
    "specimen_scale": 0,  # The scale of the specimen defined in the manuscript (1, 0.5, 0.1, ... etc)
    "source": "none",  # Site for reference source (webpage or doi) TODO AFTER PUBLICATION
    "title": "Experimental Evaluation of RC Structures with Brick Infills for 2 Vertical Forest Adaptation in Seismic regions",  # Title of the reference source
    "authors": "Theodoros Rousakis, Vachan Vanian, Martha Lappa, Adamantis G. Zapris, Ioannis P. Xynopoulos, Maristella Voutetaki, Stefanos Kellis, Georgios Sapidis, Maria Naoum, Nikolaos Papadopoulos, Violetta K. Kytinou, Martha Karampini, Constantin E. Chalioris, Athanasia Thomoglou, Emmanouil Golias",  # List of authors for the reference source (comma-separated string)
    "year": 2025,  # Publication year of the reference source
    
    # ===========================================
    # FRAME GEOMETRY GROUP
    # ===========================================
    
    # Basic frame dimensions
    "frm_h": [1200, "mm"],  # Height of the frame calculated from the top surface of the base_beam to the top surface of the top_beam. (also known as floor to floor height)
    "frm_l": [1500, "mm"],  # Length of the frame calculated from the external surfaces of the columns.
    
    # Column rectangle cross section
    "col_h": [130, "mm"],  # Column dimension parallel to frame plane
    "col_d": [130, "mm"],  # Column dimension perpendicular to frame plane
    
    # Beam rectangle cross section
    "bm_h": [200, "mm"],  # Beam height
    "bm_t": [200, "mm"],  # Beam thickness

    # Base_Beam rectangle cross section
    "bbm_h": [250, "mm"],  # Base_Beam height
    "bbm_t": [200, "mm"],  # Base_Beam thickness
    
    # Slab section (not tru it is just for the model purposes)
    "slb_d": [1200, "mm"],  # Slab Depth (dimension perpendicular to frame plane)
    "slb_h": [200, "mm"],  # Slab height (dimension parallel to frame plane)
    
    # Extensions
    "col_ext": [500, "mm"],  # Column extension above Beam top surface
    "bm_ext": [600, "mm"],  # Beam extension outside the external surfaces of the columns
    "bbm_ext": [450, "mm"],  # Base Beam extension outside the external surfaces of the columns
    
    # ===========================================
    # INFILL GEOMETRY GROUP
    # ===========================================
    
    # Basic infill properties
    "inf_type": "one_wythe",  # 1. one_wythe 2. two_wythe 3. none
    "inf_opn_type": "none",  # 1. window 2. door 3. mix 4. none
    
    # Opening dimensions
    "inf_win_h": [float, "Length"],  # Window horizontal dimension (length)
    "inf_win_v": [float, "Length"],  # Window vertical dimension (height)
    "inf_win_ph": [float, "Length"],  # Window horizontal position from main reference point
    "inf_win_pv": [float, "Length"],  # Window vertical position from main reference point

    "inf_door_h": [float, "Length"],  # Door horizontal dimension (length)
    "inf_door_v": [float, "Length"],  # Door vertical dimension (height)
    "inf_door_ph": [float, "Length"],  # Door horizontal position from main reference point
    "inf_door_pv": [float, "Length"],  # Door vertical position from main reference point
    
    # Infill properties
    "inf_dp": [60/2, "mm"],  # Infill depth from the main reference point
    "inf_bnd_pat": "running",  # Infill bond pattern  1. running 2. stack
    "inf_inff_intfc": "mortar_bond",  # Infill infill frame interface condition info  1. mortar_bond  2. seismic_joint 3. dowels 4. gap
    
    # Infill interface information
    "inf_interface_bottom": [0.0, "mm"],  # Infill interface fill/gap dimension at bottom
    "inf_interface_left": [0.0, "mm"],  # Infill interface fill/gap dimension at left
    "inf_interface_top": [0.0, "mm"],  # Infill interface fill/gap dimension at top
    "inf_interface_right": [0.0, "mm"],  # Infill interface fill/gap dimension at right
             
    # Infill unit and joint info
    "inf_ul": [200, "mm"],  # Infill unit length (horizontal)
    "inf_uh": [100, "mm"],  # Infill unit height (vertical)
    "inf_ut": [60, "mm"],  # Infill unit thickness (depth)
    "inf_uhead_t": [0.0, "mm"],  # Infill head joint thickness (vertical)
    "inf_ubed_t": [0.0, "mm"],  # Infill bed joint thickness (horizontal)
    
    # ===========================================
    # REINFORCEMENT DETAILS GROUP
    # ===========================================
    
    # Column rectangle reinforcement
    "col_cover": [25.25, "mm"],  # Cover till the external surface of the transverse reinforcement
    "col_long_reinf_corner": ["4#8", "mm"],  # Column longitudinal reinforcement at corners (e.g., '4#20') - dimensions auto-convert
    "col_long_reinf_top": [str, "Length"],  # Column longitudinal reinforcement at top (e.g., '2#16') - dimensions auto-convert
    "col_long_reinf_mid": [str, "Length"],  # Column longitudinal reinforcement at mid-height (e.g., '2#16') - dimensions auto-convert
    "col_long_reinf_bot": [str, "Length"],  # Column longitudinal reinforcement at bottom (e.g., '2#16') - dimensions auto-convert
    
    # Column transverse reinforcement
    "col_trans_crit_top_distance": [float, "Length"],  # Column transverse reinforcement critical top region distance
    "col_trans_crit_top_reinf": [str, "Length"],  # Column transverse reinforcement at critical top region (e.g., '2#8@150') - dimensions auto-convert
    "col_trans_crit_bot_distance": [float, "Length"],  # Column transverse reinforcement critical bottom region distance
    "col_trans_crit_bot_reinf": [str, "Length"],  # Column transverse reinforcement at critical bottom region (e.g., '2#8@150') - dimensions auto-convert
    "col_trans_mid_reinf": ["1#5.5@60", "mm"],  # Column transverse reinforcement at mid-height (e.g., '1#8@250') - dimensions auto-convert
    
    # Beam rectangle reinforcement
    "bm_cover": [30, "mm"],  # Cover till the external surface of the transverse reinforcement
    "bm_long_reinf_corner": ["4#10", "mm"],  # Beam longitudinal reinforcement at corners (e.g., '2#20') - dimensions auto-convert
    "bm_long_reinf_top": ["1#10", "mm"],  # Beam longitudinal reinforcement at top (e.g., '3#16') - dimensions auto-convert
    "bm_long_reinf_mid": ["2#10", "mm"],  # Beam longitudinal reinforcement at mid-span (e.g., '2#16') - dimensions auto-convert
    "bm_long_reinf_bot": ["1#10", "mm"],  # Beam longitudinal reinforcement at bottom (e.g., '3#20') - dimensions auto-convert
    "bm_trans_crit_left_distance": [float, "Length"],  # Beam transverse reinforcement critical left region distance
    "bm_trans_crit_left_reinf": [str, "Length"],  # Beam transverse reinforcement at critical right region (e.g., '2#8@100') - dimensions auto-convert
    "bm_trans_crit_right_distance": [float, "Length"],  # Beam transverse reinforcement critical right region distance
    "bm_trans_crit_right_reinf": [str, "Length"],  # Beam transverse reinforcement at critical right region (e.g., '2#8@100') - dimensions auto-convert
    "bm_trans_mid_reinf": ["1#10@100", "mm"],  # Beam transverse reinforcement at mid-span (e.g., '1#8@200') - dimensions auto-convert

    # Base_Beam rectangle reinforcement
    "bbm_cover": [20, "mm"],  # Cover till the external surface of the transverse reinforcement
    "bbm_long_reinf_corner": ["4#14", "mm"],  # Base_Beam longitudinal reinforcement at corners (e.g., '2#20') - dimensions auto-convert
    "bbm_long_reinf_top": ["1#14", "mm"],  # Base_Beam longitudinal reinforcement at top (e.g., '3#16') - dimensions auto-convert
    "bbm_long_reinf_mid": ["2#14", "mm"],  # Base_Beam longitudinal reinforcement at mid-span (e.g., '2#16') - dimensions auto-convert
    "bbm_long_reinf_bot": ["1#14", "mm"],  # Base_Beam longitudinal reinforcement at bottom (e.g., '3#20') - dimensions auto-convert
    "bbm_trans_crit_left_distance": [float, "Length"],  # Base_Beam transverse reinforcement critical left region distance
    "bbm_trans_crit_left_reinf": [str, "Length"],  # Base_Beam transverse reinforcement at critical left region (e.g., '2#8@100') - dimensions auto-convert
    "bbm_trans_crit_right_distance": [float, "Length"],  # Base_Beam transverse reinforcement critical right region distance
    "bbm_trans_crit_right_reinf": [str, "Length"],  # Base_Beam transverse reinforcement at critical right region (e.g., '2#8@100') - dimensions auto-convert
    "bbm_trans_mid_reinf": ["1#8@100", "mm"],  # Base_Beam transverse reinforcement at mid-span (e.g., '1#8@200') - dimensions auto-convert
    
    # Slab rectangle reinforcement
    "slb_cover": [30, "mm"],  # Slab cover
    "slb_top_l_reinf": ["#10@100", "mm"],  # Slab Top reinforcement parallel to frame plane (e.g., '#12@200') - dimensions auto-convert
    "slb_top_d_reinf": ["#10@100", "mm"],  # Slab Top reinforcement perpendicular to frame plane (e.g., '#12@250') - dimensions auto-convert
    "slb_bot_l_reinf": ["#10@100", "mm"],  # Slab Bottom reinforcement parallel to frame plane (e.g., '#12@200') - dimensions auto-convert
    "slb_bot_d_reinf": ["#10@100", "mm"],  # Slab Bottom reinforcement perpendicular to frame plane (e.g., '#12@250') - dimensions auto-convert
    
    # ===========================================
    # CONCRETE PROPERTIES GROUP
    # ===========================================
    "fc": [float, "Pressure"],  # Concrete compressive strength
    "Ec": [float, "Pressure"],  # Concrete modulus of elasticity
    "conc_prop_day": [float, "Time"],  # Concrete properties test age
    "conc_density": [float, "Density"],  # Concrete density
    
    # ===========================================
    # STEEL PROPERTIES GROUP
    # ===========================================
    "fy": [float, "Pressure"],  # Steel yield strength
    "fu": [float, "Pressure"],  # Steel ultimate strength
    "Ey": [float, "Pressure"],  # Steel modulus of elasticity
    "stl_density": [float, "Density"],  # Steel density
    
    # ===========================================
    # INFILL MECHANICAL PROPERTIES
    # ===========================================
    "inf_unit_density": [float, "Density"],  # Infill unit density
    "inf_mortar_density": [float, "Density"],  # Infill mortar density
    "inf_unit_compressive_strength_length": [float, "Pressure"],  # Infill unit compressive strength parallel to length
    "inf_unit_compressive_strength_height": [float, "Pressure"],  # Infill unit compressive strength parallel to height
    "inf_unit_compressive_strength_width": [float, "Pressure"],  # Infill unit compressive strength parallel to width
    "inf_mortar_type": str,  # Infill mortar type classification
    "inf_mortar_compressive_strength": [float, "Pressure"],  # Infill mortar compressive strength
    "inf_assembly_compressive_strength_height": [float, "Pressure"],  # Infill assembly compressive strength in height direction
    "inf_assembly_compressive_strength_diagonal": [float, "Pressure"],  # Infill assembly diagonal compressive strength
    
    # ===========================================
    # LOADING GROUP - IN-PLANE
    # ===========================================
    "inp_loading_protocol": str,  # In-plane loading protocol. Options: 1. monotonic 2. cyclic 3. none (not_applicable)
    "inp_cyclic_number_of_cycles": int,  # In-plane number of cycles per amplitude level
    "inp_cyclic_repetition": str,  # In-plane cyclic repetition pattern. Options: 1. constant  2. increasing
    "inp_cyclic_protocol": str,  # In-plane cyclic protocol standard: FEMA461, ACI374, etc none (not_applicable)
    "inp_column_vertical_load": [float, "Concentrated_Force"],  # In-plane column vertical load
    "inp_beam_vertical_load": [float, "Distributed_Force"],  # In-plane beam distributed vertical load
    
    # ===========================================
    # LOADING GROUP - OUT-OF-PLANE
    # ===========================================
    "oop_loading_protocol": str,  # Out-of-plane loading protocol. Options: 1. monotonic 2. cyclic 3. none (not_applicable)
    "oop_cyclic_number_of_cycles": int,  # Out-of-plane number of cycles per amplitude level
    "oop_cyclic_repetition": str,  # Out-of-plane cyclic repetition pattern. Options:  1. constant  2. increasing
    "oop_cyclic_protocol": str,  # Out-of-plane cyclic protocol standard: FEMA461, ACI374, etc OR none (not_applicable)
    "oop_column_vertical_load": [float, "Concentrated_Force"],  # Out-of-plane column vertical load
    "oop_beam_vertical_load": [float, "Distributed_Force"],  # Out-of-plane beam distributed vertical load
    
    # ===========================================
    # RESPONSE GROUP - GLOBAL
    # ===========================================
    "glb_initial_stiffness": [float, "Distributed_Force"],  # Global initial stiffness
    "glb_peak_lateral_load": [float, "Concentrated_Force"],  # Global peak lateral load
    "glb_drift_at_peak_lateral_load": [float, "Strain"],  # Global drift ratio at peak lateral load
    "glb_peak_lateral_drift": [float, "Strain"],  # Global peak lateral drift ratio
    "glb_load_at_peak_lateral_drift": [float, "Concentrated_Force"],  # Global load at peak lateral drift
    "glb_energy_dissipation": [float, "Work"],  # Global energy dissipation
    "glb_failure_mode": str,  # Global failure mode description
    
    # ===========================================
    # RESPONSE GROUP - LOCAL
    # ===========================================
    "lcl_crack_pattern": str,  # Local crack pattern description
    "lcl_failure_mechanism": str,  # Local failure mechanism description
    "lcl_damage_progression": str,  # Local damage progression description
    "lcl_strain_distribution": str,  # Local strain distribution description
    
    # ===========================================
    # RETROFIT TECHNIQUES
    # ===========================================
    "retrofit_techniques": str,  # A maximum of four (4) sentences describing retrofitting techniques applied to the specimen.
    
    # ===========================================
    # GENERAL COMMENTS
    # ===========================================
    "comments": """1. The frame is spatial user need to properly define"
2. There are 2 types of infills (full and partial) and the last row of the bricks are inclind
3. Due to asymmetry some part of the model may be needed to cut """ # General comments for user

}