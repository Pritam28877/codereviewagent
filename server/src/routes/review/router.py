from fastapi import APIRouter, Depends

from src.schemas.review import ReviewRequest, ReviewResponse
from src.services.review.review_service import ReviewService, get_review_service

router = APIRouter()


@router.post("", response_model=ReviewResponse)
async def create_review(
    payload: ReviewRequest,
    service: ReviewService = Depends(get_review_service),
) -> ReviewResponse:
    raise NotImplementedError


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(
    review_id: str,
    service: ReviewService = Depends(get_review_service),
) -> ReviewResponse:
    raise NotImplementedError
