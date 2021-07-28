from typing import List
import sqlalchemy as sa
from sqlalchemy import select, delete

from prefect.orion.models import orm
from prefect.orion import schemas


async def create_flow_run(
    session: sa.orm.Session, flow_run: schemas.actions.FlowRunCreate
) -> orm.FlowRun:
    """Creates a new flow run

    Args:
        session (sa.orm.Session): a database session
        flow_run (schemas.actions.FlowRunCreate): a flow run model

    Returns:
        orm.FlowRun: the newly-created flow run
    """
    new_flow_run = orm.FlowRun(**flow_run.dict())
    session.add(new_flow_run)
    await session.flush()
    return new_flow_run


async def read_flow_run(session: sa.orm.Session, flow_run_id: str) -> orm.FlowRun:
    """Reads a flow run by id

    Args:
        session (sa.orm.Session): A database session
        flow_run_id (str): a flow run id

    Returns:
        orm.FlowRun: the flow run
    """
    query = select(orm.FlowRun).filter_by(id=flow_run_id)
    result = await session.execute(query)
    return result.scalar()


async def read_flow_runs(
    session: sa.orm.Session,
    offset: int = 0,
    limit: int = 10,
) -> List[orm.FlowRun]:
    """Read flow runs

    Args:
        session (sa.orm.Session): A database session
        offset (int): Query offset
        limit(int): Query limit

    Returns:
        List[orm.FlowRun]: flow runs
    """
    query = select(orm.FlowRun).offset(offset).limit(limit).order_by(orm.FlowRun.id)
    result = await session.execute(query)
    return result.scalars().unique().all()


async def delete_flow_run(session: sa.orm.Session, flow_run_id: str) -> bool:
    """Delete a flow run by flow_run_id

    Args:
        session (sa.orm.Session): A database session
        flow_run_id (str): a flow run id

    Returns:
        bool: whether or not the flow run was deleted
    """
    result = await session.execute(
        delete(orm.FlowRun).where(orm.FlowRun.id == flow_run_id)
    )
    return result.rowcount > 0
