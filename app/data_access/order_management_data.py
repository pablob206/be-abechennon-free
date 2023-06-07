"""Order management data-access layer module"""
# Built-In
from typing import List

# Third-Party
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# App
from app.models import Order


async def get_orders_query(
    db_session: AsyncSession,
    _id: int | None = None,
) -> List[Order]:
    """
    Get orders query
    """

    query = select(Order)
    if _id:
        query = query.where(Order.id == _id)
    result = await db_session.exec(query)
    return result.all()
