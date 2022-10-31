from .models import InternshipBaseModel


# Used to create new internships and specify specific data
#   attributes only used when creating an internship
class InternshipCreate(InternshipBaseModel):
    pass

# The actual model the GUI Application uses
class Internship(InternshipBaseModel):
    id: int

    class Config:
        orm_mode = True
