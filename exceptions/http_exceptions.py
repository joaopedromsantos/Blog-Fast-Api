from fastapi import HTTPException, status

NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not found"
)

FORBIDDEN_EXCEPTION = HTTPException(status_code=403, detail="You do not have permission")