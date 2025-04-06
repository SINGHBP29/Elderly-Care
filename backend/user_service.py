class UserService:
    def __init__(self, ai_service):
        self.ai_service = ai_service

    def handle_user_query(self, user_query, user_id):
        """Handles user input and interacts with the AI service."""
        return self.ai_service.generate_response(user_query, user_id)
