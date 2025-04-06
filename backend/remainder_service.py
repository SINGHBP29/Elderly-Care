import pandas as pd

class ReminderService:
    def __init__(self, file_path="Dataset/daily_reminder.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(self.file_path)

        # Rename columns to standard names
        self.data.rename(columns={
            "Device-ID/User-ID": "user_id",
            "Reminder Type": "reminder_text",
            "Scheduled Time": "time",
            "Reminder Sent (Yes/No)": "sent",
            "Acknowledged (Yes/No)": "acknowledged"
        }, inplace=True)

    # def get_reminders(self, user_id):
    #     """Fetch reminders for a specific user."""
    #     if "user_id" not in self.data.columns:
    #         return "Error: 'user_id' column missing in dataset."

    #     user_reminders = self.data[self.data["Device-ID/User-ID"] == user_id]
    #     if user_reminders.empty:
    #         return "No reminders found."
    #     return user_reminders.to_dict(orient="records")
    
    def get_reminders(self, user_id):
        self.data.columns = self.data.columns.str.strip()  # Clean column names
        if "user_id" not in self.data.columns:
            print("Available columns:", self.data.columns.tolist())
            raise ValueError("Expected column 'user_id' not found in data.")
        user_reminders = self.data[self.data["user_id"] == user_id]
        return user_reminders

