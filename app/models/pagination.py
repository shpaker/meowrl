from pydantic import BaseModel


class PaginationParametersModel(BaseModel):
    page: int
    per_page: int


class PaginationResponseModel(PaginationParametersModel):
    total: int
