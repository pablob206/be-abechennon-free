"""Sql Data Access Object module"""

# Built-In
from typing import Any, Dict, List, Literal, TypeVar

# Third-Party
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import lazyload

# App
from app.config import Base


class SqlDao:
    """SQL Data Access Object Pattern"""

    TypeModel = TypeVar("TypeModel", bound=Base)

    def __init__(self, db_session: AsyncSession) -> None:
        """Constructor"""

        self.db_session: AsyncSession = db_session

    async def get_query_factory(  # pylint: disable=too-many-arguments
        self,
        filters: Dict[str, Any],
        db_entity: TypeModel,
        order_by: Any | None = None,
        limit: int | None = None,
        query_method: Literal["one_or_none", "one", "first", "all"] | None = "one_or_none",
        is_lazyload: bool | None = False,
    ) -> Any:
        """
        Get query factory.

        :param query_method: str, default 'one_or_none'. Query method. I.e.:
            one_or_none(): This method executes the query and expects exactly one result or None.
                If the query returns more than one result, it raises a MultipleResultsFound exception.

            one(): This method executes the query and expects exactly one result.
                If the query returns more than one result or none, it raises a MultipleResultsFound
                or NoResultFound exception, respectively.

            first(): This method executes the query and returns the first result found.
                If there are no results, it returns None.

            all(): This method executes the query and returns all the results as a list.
                If there are no results, it returns an empty list.

        :param is_lazyload: bool, default False. If True, then lazyload all relationships.

        TODO: Implement order_by(desc/asc), I.e:
        sqlalchemy import desc, asc
        .order_by(desc(Contact.last_movement_at))
        """

        conditions: dict = {key: value for key, value in filters.items() if value is not None}
        query = select(db_entity).filter_by(**conditions)  # type: ignore

        if is_lazyload:
            query = query.options(lazyload("*"))

        query = await self.db_session.execute(statement=query)

        if order_by:
            ...

        if limit:
            query = query.limit(limit=limit)

        if query_method == "one_or_none":
            result: db_entity = query.scalars().one_or_none()  # type: ignore
        if query_method == "one":
            result: db_entity = query.scalars().one()  # type: ignore
        if query_method == "first":
            result: db_entity = query.scalars().first()  # type: ignore
        if query_method == "all":
            result: List[db_entity] = query.scalars().all()  # type: ignore

        return result

    async def persist_query_factory(
        self,
        db_instance: TypeModel,
    ) -> TypeModel:
        """Persist query factory (create or update instance)"""

        self.db_session.add(instance=db_instance)
        await self.db_session.commit()
        await self.db_session.refresh(instance=db_instance)
        return db_instance

    async def update_query_factory(
        self,
        db_instance: TypeModel,
        data_to_update: Dict,
    ) -> TypeModel:
        """Update query factory"""

        for key, value in data_to_update.items():
            # Exclude 'exclude_atypical_key' because @computed_field is not an
            # 'unset' argument or other causes ('exclude_unset' has no effect here).
            if key in ("exclude_atypical_key_1") and value is None:
                continue
            setattr(db_instance, key, value)

        return await self.persist_query_factory(db_instance=db_instance)

    async def delete_query_factory(
        self,
        db_entity: TypeModel,
    ) -> bool:
        """Delete permanently query factory"""

        await self.db_session.delete(db_entity)
        await self.db_session.commit()
        return True
