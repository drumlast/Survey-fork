from typing import List, Optional, Any

from pydantic import BaseModel


class Punct(BaseModel):
    id: int
    title: str
    range_min: int
    range_max: int
    prompt: Optional[str] = None
    comment: Optional[str] = None
    subcriterion_id: int


class Subcriterion(BaseModel):
    id: int
    question_number: int
    title: str
    weight: float
    prompt: Optional[str] = None
    detailed_response: bool
    criterion_id: int
    puncts: List[Punct]


class Criterion(BaseModel):
    id: int
    title: str
    number: str
    question_number: int = 0
    weight: float = 0.0
    question: Optional[Optional[str]] = None
    prompt: Optional[str] = None
    is_interview: bool = False
    detailed_response: bool = False
    direction_id: int
    subcriterions: List[Subcriterion]


class Direction(BaseModel):
    id: int
    title: str
    coefficient: Optional[int] = None
    survey_id: int
    criterions: List[Criterion]


class SurveyInstruction(BaseModel):
    id: int
    title: str
    body_html: str
    survey_id: int


class SurveySettings(BaseModel):
    id: int
    name: str
    key: str
    value: str
    survey_id: int


class SurveySchema(BaseModel):
    id: int
    title: str
    slug: str
    introduction: Optional[str]
    directions: List[Direction]
    survey_instructions: Optional[List[SurveyInstruction]]
    survey_settings: Optional[List[SurveySettings]]


class SurveyList(BaseModel):
    surveys: Optional[List[SurveySchema]]


class CommitteeSchema(BaseModel):
    id: int
    name: str
    info: Optional[str] = None
    parend_id: Optional[int] = None
    parent: Optional[Any] = None
