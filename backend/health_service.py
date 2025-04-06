import pandas as pd

class HealthService:
    def __init__(self, file_path="Dataset/health_monitoring.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(self.file_path)

        # Ensure column names are correctly mapped
        self.data.rename(columns={"Device-ID/User-ID": "user_id"}, inplace=True)

    def get_health_status(self, user_id):
        """Fetch health data for a specific user."""
        if "user_id" not in self.data.columns:
            return "Error: 'Device-ID/User-ID' column missing in dataset."

        user_health = self.data[self.data["user_id"] == user_id]
        if user_health.empty:
            return "No health data found."
        return user_health.to_dict(orient="records")
