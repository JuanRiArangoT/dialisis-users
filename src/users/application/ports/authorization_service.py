from abc import ABC, abstractmethod


class AuthorizationServicePort(ABC):
    @abstractmethod
    def has_permission(
        self,
        role_id: str,
        permission_name: str,
    ) -> bool:
        pass