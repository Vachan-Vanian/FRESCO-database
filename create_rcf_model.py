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
