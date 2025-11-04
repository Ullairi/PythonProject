from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=50, description="Category name")

class QuestionCreate(BaseModel):
    text: str = Field(..., min_length=12)
    category_id: int = Field(..., description="Question category id")

class QuestionResponse(BaseModel):
    id: int
    text: str
    category: CategoryBase

class MessageResponse(BaseModel):
    message: str
