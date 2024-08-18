from common.exceptions import BaseQtError


class SpaceNotFoundError(BaseQtError):
    status = 404
    code = 'not_found'
    detail = 'Not found'


class SpaceConflictError(BaseQtError):
    status = 409
    code = 'conflict'
    detail = 'Space with this name already exists'
