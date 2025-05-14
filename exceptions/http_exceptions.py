from fastapi import HTTPException, status

NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not found"
)

S3_DELETE_FAILED_EXCEPTION = HTTPException(
    status_code=status.HTTP_207_MULTI_STATUS,
    detail="Post deleted, but failed to delete image from S3"
)