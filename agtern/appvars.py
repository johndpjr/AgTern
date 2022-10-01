from enum import Enum


class VarProfile(Enum):
    WIN_SIZE = 'profile.win_size'
    NAME = 'profile.name'
    MAJOR = 'profile.major'
    GRAD_YEAR = 'profile.grad_year'
    GRAD_MONTH = 'profile.grad_month'
    ERROR_MSG = 'profile.err_msg'

class VarInternship(Enum):
    COMPANY = 'internship.company'
    TITLE = 'internship.title'
    YEAR = 'internship.year'
    PERIOD = 'internship.period'
    LINK = 'internship.link'
