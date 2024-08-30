from common.exceptions import BaseQtError


class GardenItemNotFoundError(BaseQtError):
    status = 404
    code = 'not_found'
    detail = 'Plant not found'
