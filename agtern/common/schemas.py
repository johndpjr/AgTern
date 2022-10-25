from pydantic import BaseModel


# TODO: separate Database model from Client model
class InternshipBase(BaseModel):
    company: str = ""
    title: str = ""
    year: str | None = ""
    period: str | None = ""
    link: str | None = ""
    location: str | None = ""
    description: str | None = ""

# Used to create new internships
class InternshipCreate(InternshipBase):
    pass

class Internship(InternshipBase):
    id: int

    class Config:
        orm_mode = True
