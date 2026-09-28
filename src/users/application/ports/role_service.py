from abc import ABC, abstractmethod


class RoleServicePort(ABC):
    @abstractmethod
    def role_exists(self, role_id: str) -> bool:
        pass
