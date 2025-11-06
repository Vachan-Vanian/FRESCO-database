AVAILABLE_UNITS_FOR_TEMPLATE_RCF = {
    
    # ===========================================
    # LENGTH UNITS
    # ===========================================
    'Length': [
        'm',        # meters
        'cm',       # centimeters
        'mm',       # millimeters  
        'in',       # inches
        'ft'        # feet
    ],
    
    # ===========================================
    # TIME UNITS
    # ===========================================
    'Time': [
        's',        # seconds
        'min',      # minutes
        'hr',       # hours
        'day'       # days
    ],
    
    # ===========================================
    # MASS UNITS
    # ===========================================
    'Mass': [
        'kg',       # kilograms
        'g',        # grams
        'tonne',    # tonnes
        'lb'        # pounds
    ],
    
    # ===========================================
    # TEMPERATURE UNITS
    # ===========================================
    'Temperature': [
        'K',        # Kelvin
        'C',        # Celsius
        'F'         # Fahrenheit
    ],
    
    # ===========================================
    # PRESSURE UNITS
    # ===========================================
    'Pressure': [
        'Pa',       # Pascal
        'kPa',      # kilopascal
        'MPa',      # megapascal
        'GPa',      # gigapascal
        'N/mm^2',   # Newton per square millimeter
        'psi',      # pounds per square inch
        'ksi'       # kips per square inch
    ],
    
    # ===========================================
    # CONCENTRATED FORCE UNITS
    # ===========================================
    'Concentrated_Force': [
        'N',        # Newton
        'kN',       # kilonewton
        'MN',       # meganewton
        'lbf',      # pound-force
        'kip'       # kip
    ],
    
    # ===========================================
    # DISTRIBUTED FORCE UNITS
    # ===========================================
    'Distributed_Force': [
        'N/m',      # Newton per meter
        'kN/m',     # kilonewton per meter
        'N/mm',     # Newton per millimeter
        'lbf/ft',   # pound-force per foot
        'kip/ft',   # kip per foot
    ],
    
    # ===========================================
    # WORK/ENERGY UNITS
    # ===========================================
    'Work': [
        'J',        # Joule
        'kJ',       # kilojoule
        'N*m',      # Newton-meter
        'kN*m',     # kilonewton-meter
        'N*mm',     # Newton-millimeter
        'kN*mm',    # kilonewton-millimeter
        'lbf*in',   # pound-force inch
        'lbf*ft',   # pound-force foot
        'kip*in',   # kip-inch
        'kip*ft'    # kip-foot
    ],
    
    # ===========================================
    # DENSITY UNITS
    # ===========================================
    'Density': [
        'kg/m^3',   # kilogram per cubic meter
        'g/cm^3',   # gram per cubic centimeter
        'lb/ft^3',  # pound per cubic foot
        'pcf'       # pounds per cubic foot
    ],
    
    # ===========================================
    # STRAIN UNITS (DIMENSIONLESS)
    # ===========================================
    'Strain': [
        'strain',   # strain (dimensionless)
        'percent',  # percent
        '%',        # percent symbol
        'ratio'     # ratio (same as strain)
    ]
}


TEMPLATE_RCF = {
    # ===========================================
    # REFERENCE GROUP - Basic identification
    # ===========================================
    "specimen_id": str, # The name of the specimen defined in the manuscript
    "specimen_scale": float,  # The scale of the specimen defined in the manuscript (1, 0.5, 0.1, ... etc)
    "source": str,  # Site for reference source (webpage or doi)
    "title": str,  # Title of the reference source
    "authors": str,  # List of authors for the reference source (comma-separated string)
    "year": int,  # Publication year of the reference source
    
    # ===========================================
    # FRAME GEOMETRY GROUP
    # ===========================================
    
    # Basic frame dimensions
    "frm_h": [float, "Length"],  # Height of the frame calculated from the top surface of the base_beam to the top surface of the top_beam. (also known as floor to floor height)
    "frm_l": [float, "Length"],  # Length of the frame calculated from the external surfaces of the columns.
    
    # Column rectangle cross section
    "col_h": [float, "Length"],  # Column dimension parallel to frame plane
    "col_d": [float, "Length"],  # Column dimension perpendicular to frame plane
    
    # Beam rectangle cross section
    "bm_h": [float, "Length"],  # Beam height
    "bm_t": [float, "Length"],  # Beam thickness

    # Base_Beam rectangle cross section
    "bbm_h": [float, "Length"],  # Base_Beam height
    "bbm_t": [float, "Length"],  # Base_Beam thickness
    
    # Slab section
    "slb_d": [float, "Length"],  # Slab Depth (dimension perpendicular to frame plane)
    "slb_h": [float, "Length"],  # Slab height (dimension parallel to frame plane)
    
    # Extensions
    "col_ext": [float, "Length"],  # Column extension above Beam top surface
    "bm_ext": [float, "Length"],  # Beam extension outside the external surfaces of the columns
    "bbm_ext": [float, "Length"],  # Base Beam extension outside the external surfaces of the columns
    
    # ===========================================
    # INFILL GEOMETRY GROUP
    # ===========================================
    
    # Basic infill properties
    "inf_type": str,  # 1. one_wythe 2. two_wythe 3. none
    "inf_opn_type": str,  # 1. window 2. door 3. mix 4. none
    
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
    "inf_dp": [float, "Length"],  # Infill depth from the main reference point
    "inf_bnd_pat": str,  # Infill bond pattern  1. running 2. stack
    "inf_inff_intfc": str,  # Infill infill frame interface condition info  1. mortar_bond  2. seismic_joint 3. dowels 4. gap
    
    # Infill interface information
    "inf_interface_bottom": [float, "Length"],  # Infill interface fill/gap dimension at bottom
    "inf_interface_left": [float, "Length"],  # Infill interface fill/gap dimension at left
    "inf_interface_top": [float, "Length"],  # Infill interface fill/gap dimension at top
    "inf_interface_right": [float, "Length"],  # Infill interface fill/gap dimension at right
             
    # Infill unit and joint info
    "inf_ul": [float, "Length"],  # Infill unit length (horizontal)
    "inf_uh": [float, "Length"],  # Infill unit height (vertical)
    "inf_ut": [float, "Length"],  # Infill unit thickness (depth)
    "inf_uhead_t": [float, "Length"],  # Infill head joint thickness (vertical)
    "inf_ubed_t": [float, "Length"],  # Infill bed joint thickness (horizontal)
    
    # ===========================================
    # REINFORCEMENT DETAILS GROUP
    # ===========================================
    
    # Column rectangle reinforcement
    "col_cover": [float, "Length"],  # Cover till the external surface of the transverse reinforcement
    "col_long_reinf_corner": [str, "Length"],  # Column longitudinal reinforcement at corners (e.g., '4#20') - dimensions auto-convert
    "col_long_reinf_top": [str, "Length"],  # Column longitudinal reinforcement at top (e.g., '2#16') - dimensions auto-convert
    "col_long_reinf_mid": [str, "Length"],  # Column longitudinal reinforcement at mid-height (e.g., '2#16') - dimensions auto-convert
    "col_long_reinf_bot": [str, "Length"],  # Column longitudinal reinforcement at bottom (e.g., '2#16') - dimensions auto-convert
    
    # Column transverse reinforcement
    "col_trans_crit_top_distance": [float, "Length"],  # Column transverse reinforcement critical top region distance
    "col_trans_crit_top_reinf": [str, "Length"],  # Column transverse reinforcement at critical top region (e.g., '2#8@150') - dimensions auto-convert
    "col_trans_crit_bot_distance": [float, "Length"],  # Column transverse reinforcement critical bottom region distance
    "col_trans_crit_bot_reinf": [str, "Length"],  # Column transverse reinforcement at critical bottom region (e.g., '2#8@150') - dimensions auto-convert
    "col_trans_mid_reinf": [str, "Length"],  # Column transverse reinforcement at mid-height (e.g., '1#8@250') - dimensions auto-convert
    
    # Beam rectangle reinforcement
    "bm_cover": [float, "Length"],  # Cover till the external surface of the transverse reinforcement
    "bm_long_reinf_corner": [str, "Length"],  # Beam longitudinal reinforcement at corners (e.g., '2#20') - dimensions auto-convert
    "bm_long_reinf_top": [str, "Length"],  # Beam longitudinal reinforcement at top (e.g., '3#16') - dimensions auto-convert
    "bm_long_reinf_mid": [str, "Length"],  # Beam longitudinal reinforcement at mid-span (e.g., '2#16') - dimensions auto-convert
    "bm_long_reinf_bot": [str, "Length"],  # Beam longitudinal reinforcement at bottom (e.g., '3#20') - dimensions auto-convert
    "bm_trans_crit_left_distance": [float, "Length"],  # Beam transverse reinforcement critical left region distance
    "bm_trans_crit_left_reinf": [str, "Length"],  # Beam transverse reinforcement at critical right region (e.g., '2#8@100') - dimensions auto-convert
    "bm_trans_crit_right_distance": [float, "Length"],  # Beam transverse reinforcement critical right region distance
    "bm_trans_crit_right_reinf": [str, "Length"],  # Beam transverse reinforcement at critical right region (e.g., '2#8@100') - dimensions auto-convert
    "bm_trans_mid_reinf": [str, "Length"],  # Beam transverse reinforcement at mid-span (e.g., '1#8@200') - dimensions auto-convert

    # Base_Beam rectangle reinforcement
    "bbm_cover": [float, "Length"],  # Cover till the external surface of the transverse reinforcement
    "bbm_long_reinf_corner": [str, "Length"],  # Base_Beam longitudinal reinforcement at corners (e.g., '2#20') - dimensions auto-convert
    "bbm_long_reinf_top": [str, "Length"],  # Base_Beam longitudinal reinforcement at top (e.g., '3#16') - dimensions auto-convert
    "bbm_long_reinf_mid": [str, "Length"],  # Base_Beam longitudinal reinforcement at mid-span (e.g., '2#16') - dimensions auto-convert
    "bbm_long_reinf_bot": [str, "Length"],  # Base_Beam longitudinal reinforcement at bottom (e.g., '3#20') - dimensions auto-convert
    "bbm_trans_crit_left_distance": [float, "Length"],  # Base_Beam transverse reinforcement critical left region distance
    "bbm_trans_crit_left_reinf": [str, "Length"],  # Base_Beam transverse reinforcement at critical left region (e.g., '2#8@100') - dimensions auto-convert
    "bbm_trans_crit_right_distance": [float, "Length"],  # Base_Beam transverse reinforcement critical right region distance
    "bbm_trans_crit_right_reinf": [str, "Length"],  # Base_Beam transverse reinforcement at critical right region (e.g., '2#8@100') - dimensions auto-convert
    "bbm_trans_mid_reinf": [str, "Length"],  # Base_Beam transverse reinforcement at mid-span (e.g., '1#8@200') - dimensions auto-convert
    
    # Slab rectangle reinforcement
    "slb_cover": [float, "Length"],  # Slab cover
    "slb_top_l_reinf": [str, "Length"],  # Slab Top reinforcement parallel to frame plane (e.g., '#12@200') - dimensions auto-convert
    "slb_top_d_reinf": [str, "Length"],  # Slab Top reinforcement perpendicular to frame plane (e.g., '#12@250') - dimensions auto-convert
    "slb_bot_l_reinf": [str, "Length"],  # Slab Bottom reinforcement parallel to frame plane (e.g., '#12@200') - dimensions auto-convert
    "slb_bot_d_reinf": [str, "Length"],  # Slab Bottom reinforcement perpendicular to frame plane (e.g., '#12@250') - dimensions auto-convert
    
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
    "comments": str # General comments for user

}

