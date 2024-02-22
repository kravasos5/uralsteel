from utils.service_base import ServiceBase


class RefreshTokenService(ServiceBase):
    """Сервис для работы с refresh токенами"""
    repository = 'refresh_token_repo'


class RefreshTokenBlacklistService(ServiceBase):
    """Сервис для работы с refresh токенами из чёрного списка"""
    repository = 'refresh_token_bl_repo'
