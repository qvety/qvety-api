from common.exceptions import BaseQtError


class InvalidCredentialsError(BaseQtError):
    status = 401
    code = 'unauthorized'
    detail = 'Invalid credentials'


class UserAlreadyExistsError(BaseQtError):
    status = 409
    code = 'conflict'
    detail = 'User already exists'


class UserEmailAlreadyExistsError(UserAlreadyExistsError):
    detail = 'Email is already taken'


class UsernameAlreadyExistsError(UserAlreadyExistsError):
    detail = 'Username is already taken'


class JWTError(BaseQtError):
    status = 401
    code = 'unauthorized'
    detail = 'JWT token decode error'


class JWTExpiredError(JWTError):
    detail = 'JWT token expired'


class InvalidJWTRefreshTypeError(JWTError):
    detail = 'Token type is not refresh'


class JWTTokenRevokedError(JWTError):
    detail = 'Refresh token has been revoked'


class UserNotFoundJWTError(JWTError):
    detail = 'User not found'


class InvalidPayloadError(JWTError):
    detail = 'Invalid payload'
