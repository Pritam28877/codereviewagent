from src.repositories.review.review_repository import ReviewRepository
from src.schemas.review import ReviewRequest, ReviewResponse
from src.services.review.llm_client import LLMClient


class ReviewService:
    def __init__(self, repository: ReviewRepository, llm: LLMClient) -> None:
        self.repository = repository
        self.llm = llm

    async def create_review(self, payload: ReviewRequest) -> ReviewResponse:
        raise NotImplementedError

    async def get_review(self, review_id: str) -> ReviewResponse:
        raise NotImplementedError


def get_review_service() -> ReviewService:
    raise NotImplementedError
