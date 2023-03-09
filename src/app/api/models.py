from pydantic import BaseModel, Field


class EventSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    category: str = Field(..., min_length=3, max_length=50)


class EventDB(EventSchema):
    id: int