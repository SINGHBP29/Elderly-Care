import pandas as pd
import os

def load_dataset(file_name='daily_reminder.csv', folder_name='dataset'):
    dataset_path = os.path.join(os.getcwd(), folder_name, file_name)

    try:
        data = pd.read_csv(dataset_path)
        print("Data loaded successfully!")
        print(data.head())  # Display the first few rows of the dataset
        return data
    except FileNotFoundError:
        print(f"File not found at {dataset_path}. Please check the path and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return None
