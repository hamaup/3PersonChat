class OperatorService:
    """Simulated human operator service."""

    def handle_message(self, user_message: str) -> str:
        """Return a human-crafted response."""
        # In a real system, this would notify a human operator.
        # Here we simply ask the developer/operator for input.
        print("\n[オペレーター通知] ユーザーからのメッセージ: " + user_message)
        reply = input("オペレーターの回答を入力してください: ")
        return reply
