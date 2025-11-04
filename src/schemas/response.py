from pydantic import BaseModel, Field


class ResponseCreate(BaseModel):
    question_id: int = Field(..., description="ID вопроса")
    is_agree: bool = Field(..., description="Согласие или несогласие с вопросом")

class StatisticResponse(BaseModel):
    question_id: int
    agree_count: int
    disagree_count: int