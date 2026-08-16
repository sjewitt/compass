from fastapi import HTTPException

class UserNotFound(HTTPException):
    pass

class CompassNotFound(HTTPException):
    pass

class QuadrantNotFound(HTTPException):
    pass


class SectorNotFound(HTTPException):
    pass


class CompetencyNotFound(HTTPException):
    pass


class CompassDefinitionIncomplete(HTTPException):
    pass

# this one may be unnecessary:
class CompetencyOutOfRange(HTTPException):
    pass


class CompetenciesForUserNotFound(HTTPException):
    pass


class CompassForUserNotFound(HTTPException):
    pass