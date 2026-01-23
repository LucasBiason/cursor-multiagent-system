"""
FastAPI Repository Snippet - Template/Snippet Reutilizável

This module provides a base repository class with common CRUD operations
and raw SQL query methods with parameter binding for security.

**IMPORTANTE:** Este é um template/snippet. Copie e adapte para seu projeto.

Usage:
    from core.templates.database.fastapi_repository_snippet import BaseRepository
    from sqlalchemy.orm import Session
    from myapp.models import User

    class UserRepository(BaseRepository[User]):
        def __init__(self, db: Session):
            super().__init__(db)

        def get_by_email(self, email: str) -> Optional[User]:
            return self._query_one(
                "SELECT * FROM users WHERE email = :email",
                {"email": email}
            )

    # Usage
    user_repo = UserRepository(db)
    user = user_repo.get_by_email("user@example.com")
"""

from typing import Any, Dict, Generic, List, Optional, TypeVar
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Session


T = TypeVar('T')


class BaseRepository(Generic[T]):
    """
    Base repository class providing common CRUD operations and raw SQL queries.

    Generic type T should be a SQLAlchemy model class.
    """

    def __init__(self, db: Session):
        """
        Initialize the repository with a database session.

        Args:
            db: SQLAlchemy database session.
        """
        self.db: Session = db

    def _create(self, model: T) -> T:
        """
        Create a new model instance in the database.

        Args:
            model: The model instance to create.

        Returns:
            T: The created model instance.
        """
        if hasattr(model, 'is_active'):
            model.is_active = True
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def _read(self, model_class: type[T], id: UUID) -> Optional[T]:
        """
        Read a model instance by its ID.

        Args:
            model_class: The model class.
            id: The UUID of the model to retrieve.

        Returns:
            Optional[T]: The model instance if found, None otherwise.
        """
        return self.db.query(model_class).filter(model_class.id == id).first()

    def list(self, model_class: type[T] = None) -> List[T]:
        """
        List all model instances.

        Args:
            model_class: The model class. If None, uses the generic type.

        Returns:
            List[T]: List of all model instances.
        """
        if model_class is None:
            raise NotImplementedError("Subclasses must implement list() method or provide model_class")
        if hasattr(model_class, 'is_active'):
            return self.db.query(model_class).filter(model_class.is_active == True).all()
        return self.db.query(model_class).all()

    def _list(self, model_class: type[T], filters: Any, order_by: Any) -> List[T]:
        """
        List model instances with filters and ordering.

        Args:
            model_class: The model class.
            filters: SQLAlchemy filter conditions.
            order_by: SQLAlchemy ordering conditions.

        Returns:
            List[T]: List of model instances.
        """
        return self.db.query(model_class).filter(filters).order_by(order_by).all()

    def _list_single(self, model_class: type[T], filters: Any, order_by: Any) -> Optional[T]:
        """
        Get a single model instance with filters and ordering.

        Args:
            model_class: The model class.
            filters: SQLAlchemy filter conditions.
            order_by: SQLAlchemy ordering conditions.

        Returns:
            Optional[T]: The model instance if found, None otherwise.
        """
        return self.db.query(model_class).filter(filters).order_by(order_by).first()

    def _update(self, model: T) -> T:
        """
        Update a model instance in the database.

        Args:
            model: The model instance to update.

        Returns:
            T: The updated model instance.
        """
        self.db.commit()
        self.db.refresh(model)
        return model

    def _soft_delete(self, model: T) -> bool:
        """
        Soft delete a model instance (sets is_active=False).

        Args:
            model: The model instance to soft delete.

        Returns:
            bool: True if the model was soft deleted successfully.
        """
        if hasattr(model, 'soft_delete'):
            model.soft_delete()
        elif hasattr(model, 'is_active'):
            model.is_active = False
        else:
            raise AttributeError("Model does not support soft delete")
        self.db.commit()
        return True

    def _hard_delete(self, model: T) -> bool:
        """
        Hard delete a model instance from the database.

        Args:
            model: The model instance to hard delete.

        Returns:
            bool: True if the model was hard deleted successfully.
        """
        self.db.delete(model)
        self.db.commit()
        return True

    def _restore(self, model: T) -> T:
        """
        Restore a soft deleted model instance.

        Args:
            model: The model instance to restore.

        Returns:
            T: The restored model instance.
        """
        if hasattr(model, 'restore'):
            model.restore()
        elif hasattr(model, 'is_active'):
            model.is_active = True
        else:
            raise AttributeError("Model does not support restore")
        self.db.commit()
        self.db.refresh(model)
        return model

    def _query_one(self, sql_text: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Execute a raw SQL query and return a single result.

        Uses parameter binding to protect against SQL injection.

        Args:
            sql_text: The SQL query to execute (use :param_name for named parameters).
            params: Optional dictionary of parameters to bind to the SQL query.

        Returns:
            Optional[Dict[str, Any]]: A single row as a dictionary, or None if no results found.
        """
        try:
            result = self.db.execute(
                text(sql_text),
                params or {}
            )
            row = result.fetchone()
            if not row:
                return None
            return dict(row._mapping)
        except Exception as e:
            self.db.rollback()
            raise

    def _query_list(self, sql_text: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Execute a raw SQL query and return multiple results.

        Uses parameter binding to protect against SQL injection.

        Args:
            sql_text: The SQL query to execute (use :param_name for named parameters).
            params: Optional dictionary of parameters to bind to the SQL query.

        Returns:
            List[Dict[str, Any]]: A list of rows as dictionaries.
        """
        try:
            result = self.db.execute(
                text(sql_text),
                params or {}
            )
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]
        except Exception as e:
            self.db.rollback()
            raise

    def _query_scalar(self, sql_text: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute a raw SQL query and return a scalar value.

        Uses parameter binding to protect against SQL injection.

        Args:
            sql_text: The SQL query to execute (use :param_name for named parameters).
            params: Optional dictionary of parameters for the query.

        Returns:
            Any: The scalar result of the query.
        """
        try:
            result = self.db.execute(
                text(sql_text),
                params or {}
            )
            return result.scalar()
        except Exception as e:
            self.db.rollback()
            raise

