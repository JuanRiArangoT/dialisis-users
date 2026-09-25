from users.application.ports.user_repository import UserRepositoryPort


class DeleteUserUseCase:
    def __init__(self, user_repository: UserRepositoryPort) -> None:
        self._user_repository = user_repository

    def execute(self, user_id: str) -> bool:
        user = self._user_repository.get_by_id(user_id)

        if user is None:
            return False

        self._user_repository.delete(user_id)

        return True
