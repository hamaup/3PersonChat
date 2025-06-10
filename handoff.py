class HandoffService:
    """Decides whether to hand off conversation to human operator."""

    def __init__(self, threshold: float = 0.5, keywords: list[str] | None = None):
        self.threshold = threshold
        self.keywords = keywords or ["オペレーター", "人間"]

    def needs_handoff(self, user_message: str, confidence: float) -> bool:
        """Return True if the conversation should be escalated."""
        if confidence < self.threshold:
            return True
        for kw in self.keywords:
            if kw in user_message:
                return True
        return False
