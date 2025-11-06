from src.ppee_model import PPEEFrameGenerator

# USER Configuration
DATABASE_FOLDER_PATH = "Database/"
CAD_FOLDER_PATH = "Models/"
DATABASE_NAME = "fresco_v1"
DATABASE_ENTRY_ID = 2
MODEL_NAME = None


generator = PPEEFrameGenerator(DATABASE_FOLDER_PATH, 
                               CAD_FOLDER_PATH, 
                               DATABASE_NAME, 
                               DATABASE_ENTRY_ID, 
                               MODEL_NAME)
generator.generate_frame()
