from fastapi import HTTPException

class UserNotFound(HTTPException):
    pass


class CompetencyNotFound(HTTPException):
    pass

class CompetencyOutOfRange(HTTPException):
    pass

class CompetenciesForUserNotFound(HTTPException):
    pass