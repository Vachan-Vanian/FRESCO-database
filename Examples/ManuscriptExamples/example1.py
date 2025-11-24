# ============================================================================================================
# This is the first example for using the FRESCO Database
# Details of the manuscript 
#    - Status: Open Access
#    - Title: FRESCO: An Open Database for Fiber and Polymer Strengthening of Infilled RC Frame Systems
#    - Authors: Vachan Vanian, Theodoros Rousakis
#    - Year: 2025
#    - DOI: https://doi.org/10.3390/fib13110152
#
# ------------------------------------------------------------------------------------------------------------
#
# The original specimen is from: https://doi.org/10.1061/(ASCE)CC.1943-5614.0000911
# Details of the source manuscript (specimen origin)
#    - Status: Open Access
#    - Title: Out-of-Plane Strengthening of Masonry-Infilled RC Frames with Textile-Reinforced Mortar Jackets
#    - Authors: Lampros N. Koutas, Dionysios A. Bournas
#    - Year: 2019
# ============================================================================================================





entry_koutas_and_bournas_2019= {
    # ===========================================
    # REFERENCE GROUP - Basic identification
    # ===========================================
    "specimen_id": "S_CON",  # The name of the specimen defined in the manuscript
    "specimen_scale": 0.5,  # The scale of the specimen defined in the manuscript (1:1, 1:2, 1:10, ... etc)
    "source": "https://doi.org/10.1061/(ASCE)CC.1943-5614.0000911",  # Site for reference source (webpage or doi)
    "title": "Out-of-Plane Strengthening of Masonry-Infilled RC Frames with Textile-Reinforced Mortar Jackets",  # Title of the reference source
    "authors": "Lampros N. Koutas, Dionysios A. Bournas",  # List of authors for the reference source (comma-separated string)
    "year": 2019,  # Publication year of the reference source
    
    # ===========================================
    # FRAME GEOMETRY GROUP
    # ===========================================
    
    # Basic frame dimensions
    "frm_h": [1500, "mm"],  # Height of the frame calculated from the top surface of the base_beam to the top surface of the top_beam. (also known as floor to floor height)
    "frm_l": [2100, "mm"],  # Length of the frame calculated from the external surfaces of the columns.
    
    # Column rectangle cross section
    "col_h": [200, "mm"],  # Column dimension parallel to frame plane
    "col_d": [140, "mm"],  # Column dimension perpendicular to frame plane
    
    # Beam rectangle cross section
    "bm_h": [160+90, "mm"],  # Beam height
    "bm_t": [140, "mm"],  # Beam thickness

    # Base_Beam rectangle cross section
    "bbm_h": [250, "mm"],  # Base_Beam height
    "bbm_t": [540, "mm"],  # Base_Beam thickness
    
    # Slab section
    "slb_d": [320, "mm"],  # Slab Depth (dimension perpendicular to frame plane)
    "slb_h": [90, "mm"],  # Slab height (dimension parallel to frame plane)
    
    # Extensions
    "col_ext": [0.0, "mm"],  # Column extension above Beam top surface
    "bm_ext": [0.0, "mm"],  # Beam extension outside the external surfaces of the columns
    "bbm_ext": [(2500-2100)/2, "mm"],  # Base Beam extension outside the external surfaces of the columns
    
    # ===========================================
    # INFILL GEOMETRY GROUP
    # ===========================================
    
    # Basic infill properties
    "inf_type": "one_wythe",  # 1. one_wythe 2. two_wythe  3. none
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
    "inf_dp": [80/2, "mm"],  # Infill depth from the main reference point
    "inf_bnd_pat": "running",  # Infill bond pattern  1. running 2. stack
    "inf_inff_intfc": "mortar_bond",  # Infill infill frame interface condition info  1. mortar_bond  2. seismic_joint 3. dowels 4. gap
    
    # Infill interface information
    "inf_interface_bottom": [10, "mm"],  # Infill interface fill/gap dimension at bottom
    "inf_interface_left": [10, "mm"],  # Infill interface fill/gap dimension at left
    "inf_interface_top": [10, "mm"],  # Infill interface fill/gap dimension at top
    "inf_interface_right": [10, "mm"],  # Infill interface fill/gap dimension at right
             
    # Infill unit and joint info
    "inf_ul": [215, "mm"],  # Infill unit length (horizontal)
    "inf_uh": [102.5, "mm"],  # Infill unit height (vertical)
    "inf_ut": [65, "mm"],  # Infill unit thickness (depth)
    "inf_uhead_t": [10, "mm"],  # Infill head joint thickness (vertical)
    "inf_ubed_t": [10, "mm"],  # Infill bed joint thickness (horizontal)
    
    # ===========================================
    # REINFORCEMENT DETAILS GROUP
    # ===========================================
    
    # Column rectangle reinforcement
    "col_cover": [10, "mm"],  # Cover till the external surface of the transverse reinforcement
    "col_long_reinf_corner": ["4#10", "mm"],  # Column longitudinal reinforcement at corners (e.g., '4#20') - dimensions auto-convert
    "col_long_reinf_top": [str, "Length"],  # Column longitudinal reinforcement at top (e.g., '2#16') - dimensions auto-convert
    "col_long_reinf_mid": [str, "Length"],  # Column longitudinal reinforcement at mid-height (e.g., '2#16') - dimensions auto-convert
    "col_long_reinf_bot": [str, "Length"],  # Column longitudinal reinforcement at bottom (e.g., '2#16') - dimensions auto-convert

    # Column transverse reinforcement
    "col_trans_crit_top_distance": [float, "Length"],  # Column transverse reinforcement critical top region distance
    "col_trans_crit_top_reinf": [str, "Length"],  # Column transverse reinforcement at critical top region (e.g., '2#8@150') - dimensions auto-convert
    "col_trans_crit_bot_distance": [float, "Length"],  # Column transverse reinforcement critical bottom region distance
    "col_trans_crit_bot_reinf": [str, "Length"],  # Column transverse reinforcement at critical bottom region (e.g., '2#8@150') - dimensions auto-convert
    "col_trans_mid_reinf": ["1#6@150", "mm"],  # Column transverse reinforcement at mid-height (e.g., '1#8@250') - dimensions auto-convert
    
    # Beam rectangle reinforcement
    "bm_cover": [20, "mm"],  # Cover till the external surface of the transverse reinforcement
    "bm_long_reinf_corner": ["4#10", "mm"],  # Beam longitudinal reinforcement at corners (e.g., '2#20') - dimensions auto-convert
    "bm_long_reinf_top": [str, "Length"],  # Beam longitudinal reinforcement at top (e.g., '3#16') - dimensions auto-convert
    "bm_long_reinf_mid": [str, "Length"],  # Beam longitudinal reinforcement at mid-span (e.g., '2#16') - dimensions auto-convert
    "bm_long_reinf_bot": [str, "Length"],  # Beam longitudinal reinforcement at bottom (e.g., '3#20') - dimensions auto-convert
    "bm_trans_crit_left_distance": [float, "Length"],  # Beam transverse reinforcement critical left region distance
    "bm_trans_crit_left_reinf": [str, "Length"],  # Beam transverse reinforcement at critical right region (e.g., '2#8@100') - dimensions auto-convert
    "bm_trans_crit_right_distance": [float, "Length"],  # Beam transverse reinforcement critical left region distance
    "bm_trans_crit_right_reinf": [str, "Length"],  # Beam transverse reinforcement at critical right region (e.g., '2#8@100') - dimensions auto-convert
    "bm_trans_mid_reinf": ["1#6@150", "mm"],  # Beam transverse reinforcement at mid-span (e.g., '1#8@200') - dimensions auto-convert

    # Base_Beam rectangle reinforcement (Estimated heavy)
    "bbm_cover": [30, "Length"],  # Cover till the external surface of the transverse reinforcement
    "bbm_long_reinf_corner": ["4#20", "mm"],  # Base_Beam longitudinal reinforcement at corners (e.g., '2#20') - dimensions auto-convert
    "bbm_long_reinf_top": ["3#20", "mm"],  # Base_Beam longitudinal reinforcement at top (e.g., '3#16') - dimensions auto-convert
    "bbm_long_reinf_mid": ["2#20", "mm"],  # Base_Beam longitudinal reinforcement at mid-span (e.g., '2#16') - dimensions auto-convert
    "bbm_long_reinf_bot": ["3#20", "mm"],  # Base_Beam longitudinal reinforcement at bottom (e.g., '3#20') - dimensions auto-convert
    "bbm_trans_crit_left_distance": [float, "Length"],  # Base_Beam transverse reinforcement critical left region distance
    "bbm_trans_crit_left_reinf": [str, "Length"],  # Base_Beam transverse reinforcement at critical left region (e.g., '2#8@100') - dimensions auto-convert
    "bbm_trans_crit_right_distance": [float, "Length"],  # Base_Beam transverse reinforcement critical right region distance
    "bbm_trans_crit_right_reinf": [str, "Length"],  # Base_Beam transverse reinforcement at critical right region (e.g., '2#8@100') - dimensions auto-convert
    "bbm_trans_mid_reinf": ["#10@100", "mm"],  # Base_Beam transverse reinforcement at mid-span (e.g., '1#8@200') - dimensions auto-convert
    
    # Slab rectangle reinforcement
    "slb_cover": [10, "mm"],  # Slab cover
    "slb_top_l_reinf": ["#10@150", "mm"],  # Slab Top reinforcement parallel to frame plane (e.g., '#12@200') - dimensions auto-convert
    "slb_top_d_reinf": ["#10@150", "mm"],  # Slab Top reinforcement perpendicular to frame plane (e.g., '#12@250') - dimensions auto-convert
    "slb_bot_l_reinf": [str, "Length"],  # Slab Bottom reinforcement parallel to frame plane (e.g., '#12@200') - dimensions auto-convert
    "slb_bot_d_reinf": [str, "Length"],  # Slab Bottom reinforcement perpendicular to frame plane (e.g., '#12@250') - dimensions auto-convert
    
    # ===========================================
    # CONCRETE PROPERTIES GROUP
    # ===========================================
    "fc": [22.1, "MPa"],  # Concrete compressive strength
    "Ec": [float, "Pressure"],  # Concrete modulus of elasticity
    "conc_prop_day": [28, "day"],  # Concrete properties test age
    "conc_density": [2400.0, "kg/m^3"],  # Concrete density
    
    # ===========================================
    # STEEL PROPERTIES GROUP
    # ===========================================
    "fy": [545.0, "MPa"],  # Steel yield strength
    "fu": [637.0, "MPa"],  # Steel ultimate strength
    "Ey": [200000.0, "MPa"],  # Steel modulus of elasticity
    "stl_density": [7850, "kg/m^3"],  # Steel density
    
    # ===========================================
    # INFILL MECHANICAL PROPERTIES
    # ===========================================
    "inf_unit_density": [1900.0, "kg/m^3"],  # Infill unit density
    "inf_mortar_density": [2000.0, "kg/m^3"],  # Infill mortar density
    "inf_unit_compressive_strength_length": [float, "Pressure"],  # Infill unit compressive strength parallel to length
    "inf_unit_compressive_strength_height": [float, "Pressure"],  # Infill unit compressive strength parallel to height
    "inf_unit_compressive_strength_width": [21.2, "MPa"],  # Infill unit compressive strength parallel to width
    "inf_mortar_type": "1:4 cement:sand",  # Infill mortar type classification
    "inf_mortar_compressive_strength": [11.5, "MPa"],  # Infill mortar compressive strength
    "inf_assembly_compressive_strength_height": [9.7, "MPa"],  # Infill assembly compressive strength in height direction
    "inf_assembly_compressive_strength_diagonal": [float, "Pressure"],  # Infill assembly diagonal compressive strength
    
    
    # ===========================================
    # LOADING GROUP - IN-PLANE
    # ===========================================
    "inp_loading_protocol": "none",  # In-plane loading protocol. Options: 1. monotonic 2. cyclic 3. none (not_applicable)
    "inp_cyclic_number_of_cycles": int,  # In-plane number of cycles per amplitude level
    "inp_cyclic_repetition": str,  # In-plane cyclic repetition pattern. Options: 1. constant  2. increasing
    "inp_cyclic_protocol": "none",  # In-plane cyclic protocol standard: FEMA461, ACI374, etc OR none (not_applicable)
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
    "glb_initial_stiffness": [7.4, "kN/mm"],  # Global initial stiffness
    "glb_peak_lateral_load": [29.0, "kN"],  # Global peak lateral load
    "glb_drift_at_peak_lateral_load": [1.5, "%"],  # Global drift ratio at peak lateral load
    "glb_peak_lateral_drift": [1.5, "%"],  # Global peak lateral drift ratio
    "glb_load_at_peak_lateral_drift": [29.0, "kN"],  # Global load at peak lateral drift
    "glb_energy_dissipation": [1.53, "kJ"],  # Global energy dissipation
    "glb_failure_mode": "Arching action with step-cracking in mortar joints, gradual load drop",  # Global failure mode description
    
    # ===========================================
    # RESPONSE GROUP - LOCAL
    # ===========================================
    "lcl_crack_pattern": "Step-cracking mainly following mortar joints from center toward corners on back face",  # Local crack pattern description
    "lcl_failure_mechanism": "Wall separation from RC frame perimeter, arching action degradation",  # Local failure mechanism description
    "lcl_damage_progression": "First cracks at 10kN in central bed joint, propagation toward corners, wall detachment from frame",  # Local damage progression description
    "lcl_strain_distribution": "Tension strains concentrated at mortar joints, compression at loading points",  # Local strain distribution description
    
    # ===========================================
    # RETROFIT TECHNIQUES
    # ===========================================
    "retrofit_techniques": "No retrofitting applied - this is the control specimen serving as reference for comparison with TRM-strengthened specimens.",  # A maximum of four (4) sentences describing retrofitting techniques applied to the specimen.
    
    # ===========================================
    # GENERAL COMMENTS
    # ===========================================
    "comments": str # General comments for user
}