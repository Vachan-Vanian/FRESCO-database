from src.database_editor import FrescoDatabase
from fresco_v1.entries import entries

DATABASE_NAME = "fresco_v1"
DB_PATH = f"Database/{DATABASE_NAME}"
DATABASE_ENTRY_ID=0

db = FrescoDatabase(DB_PATH, 
                    compress_db=False, 
                    auto_back_up=False,
                    auto_save=False,
                    show_conversion=False,
                    show_invalid_object=False)

for key, value in entries.items():
    DATABASE_ENTRY_ID = DATABASE_ENTRY_ID+1
    print("\n", key, " - ", DATABASE_ENTRY_ID)
    
    db.add_entry(
        overwrite=True,
        entry_id=DATABASE_ENTRY_ID,
        entry_data = value,
        show_error_fields=False
    )

db.save()
db.export_to_csv(DB_PATH)
