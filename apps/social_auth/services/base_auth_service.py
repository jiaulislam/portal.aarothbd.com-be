from abc import ABC, abstractmethod


class BaseSocialAuthProviderService(ABC):
    @abstractmethod
    def validate_token(self, *args, **kwargs):
        """validate the oauth2 provider token"""
        raise NotImplementedError
