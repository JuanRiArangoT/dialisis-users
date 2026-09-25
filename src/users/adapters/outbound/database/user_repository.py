from sqlalchemy import select
from sqlalchemy.orm import Session

from users.application.ports.user_repository import UserRepositoryPort
from users.domain.entities.user import User

from .models import UserModel


class PostgresUserRepository(UserRepositoryPort):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, user: User) -> User:
        model = UserModel(
            id=user.id,
            auth0_user_id=user.auth0_user_id,
            email=user.email,
            full_name=user.full_name,
            tipo_documento=user.tipo_documento,
            numero_documento=user.numero_documento,
            is_active=user.is_active,
        )

        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)

        return self._to_entity(model)

    def get_by_id(self, user_id: str) -> User | None:
        model = self._session.get(UserModel, user_id)

        if model is None:
            return None

        return self._to_entity(model)

    def get_by_auth0_id(self, auth0_user_id: str) -> User | None:
        statement = select(UserModel).where(UserModel.auth0_user_id == auth0_user_id)

        model = self._session.scalar(statement)

        if model is None:
            return None

        return self._to_entity(model)

    def get_by_email(self, email: str) -> User | None:
        statement = select(UserModel).where(UserModel.email == email)

        model = self._session.scalar(statement)

        if model is None:
            return None

        return self._to_entity(model)

    def update(self, user: User) -> User:
        model = self._session.get(UserModel, user.id)

        if model is None:
            raise ValueError(f"User not found: {user.id}")

        model.auth0_user_id = user.auth0_user_id
        model.email = user.email
        model.full_name = user.full_name
        model.tipo_documento = user.tipo_documento
        model.numero_documento = user.numero_documento
        model.is_active = user.is_active

        self._session.commit()
        self._session.refresh(model)

        return self._to_entity(model)

    def delete(self, user_id: str) -> None:
        model = self._session.get(UserModel, user_id)

        if model is None:
            return

        self._session.delete(model)
        self._session.commit()

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        return User(
            id=model.id,
            auth0_user_id=model.auth0_user_id,
            email=model.email,
            full_name=model.full_name,
            tipo_documento=model.tipo_documento,
            numero_documento=model.numero_documento,
            is_active=model.is_active,
        )

    def get_by_document_number(
        self,
        numero_documento: str,
    ) -> User | None:
        statement = select(UserModel).where(
            UserModel.numero_documento == numero_documento
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return self._to_entity(model)
