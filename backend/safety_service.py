import pandas as pd

class SafetyService:
    def __init__(self, file_path="Dataset/safety_monitoring.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(self.file_path)

    def get_safety_alerts(self, user_id):
        """Fetch latest safety alerts for a user."""
        user_safety = self.data[self.data["Device-ID/User-ID"] == user_id]
        if user_safety.empty:
            return "No safety alerts found."
        return user_safety.iloc[-1].to_dict()  # Latest alert
    
