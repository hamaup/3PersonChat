class BotService:
    """Simple AI bot service."""

    def generate_response(self, user_message: str) -> tuple[str, float]:
        """Generate a response and return a confidence score."""
        # Very naive logic: if question ends with '?', confidence low
        if user_message.strip().endswith('?'):
            response = "ご質問ありがとうございます。担当者が確認いたします。"
            confidence = 0.4
        else:
            response = f"自動応答: {user_message}"
            confidence = 0.9
        return response, confidence
