from src.schemas.review import ReviewComment


class LLMClient:
    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    async def review_code(self, file_name: str, language: str, code: str) -> list[ReviewComment]:
        raise NotImplementedError
