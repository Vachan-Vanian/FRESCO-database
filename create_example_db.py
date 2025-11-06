from src.database_editor import FrescoDatabase
from Examples.ManuscriptExamples.example1 import entry_koutas_and_bournas_2019
from Examples.ManuscriptExamples.example2 import entry_akhoundi_et_al_2018
from Examples.ManuscriptExamples.example3 import entry_rousakis_et_al_2025


db = FrescoDatabase("Database/example_db", compress_db=False, auto_back_up=False)

db.add_entry(
    overwrite=True,
    entry_id=1,
    entry_data = entry_koutas_and_bournas_2019,
    show_error_fields=False
)

db.add_entry(
    overwrite=True,
    entry_id=2,
    entry_data = entry_akhoundi_et_al_2018,
    show_error_fields=False
)

db.add_entry(
    overwrite=True,
    entry_id=3,
    entry_data = entry_rousakis_et_al_2025,
    show_error_fields=False
)

db.get_info()

db.export_to_csv("Database/example_db.csv")
