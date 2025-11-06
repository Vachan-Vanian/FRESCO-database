from src.database_editor import FrescoDatabase
from fresco_v1.entries import entries


DATABASE_ENTRY_ID=0
for key, value in entries.items():
    DATABASE_NAME = "fresco_v1"
    DATABASE_ENTRY_ID = DATABASE_ENTRY_ID+1
    print("\n", key, " - ", DATABASE_ENTRY_ID)
    
    db = FrescoDatabase(f"Database/{DATABASE_NAME}", 
                        compress_db=False, 
                        auto_back_up=False,
                        show_conversion=False,
                        show_invalid_object=False)
   
    db.add_entry(
        overwrite=True,
        entry_id=DATABASE_ENTRY_ID,
        entry_data = value,
        show_error_fields=False
    )

    DATABSE_FOLDER_PATH = "Database/"
    CAD_FOLDER_PATH = "Models/"
    CAD_NAME = key

db.export_to_csv('Database/fresco_v1')
