from src.schemas.review import ReviewResponse


class ReviewRepository:
    async def save(self, review: ReviewResponse) -> None:
        raise NotImplementedError

    async def get_by_id(self, review_id: str) -> ReviewResponse | None:
        raise NotImplementedError
