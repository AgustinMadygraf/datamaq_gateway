"""
Path: infrastructure/sql_alchemy/sql_alchemy_dashboard.py
"""


from typing import Optional, Sequence
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from entities.dashboard_point import DashboardPoint
from interface_adapters.gateway.repositories import DashboardRepository
from shared.config import get_mysql_config

class SQLAlchemyDashboardRepository(DashboardRepository):
    "Repositorio SQLAlchemy para Dashboard"
    def __init__(self):
        cfg = get_mysql_config()
        self.engine: Engine = create_engine(
            f"mysql+pymysql://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}?charset=utf8mb4",
            connect_args={"connect_timeout": cfg.get("connect_timeout", 3)}
        )

    def get_last_point(self) -> Optional[DashboardPoint]:
        with self.engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT unixtime, hr_counter1, hr_counter2 "
                    "FROM intervalproduction "
                    "ORDER BY unixtime DESC "
                    "LIMIT 1"
                )
            )
            row = result.mappings().first()
            if row:
                return DashboardPoint(**row)
            return None

    def get_points_between(self, t1: int, t2: int) -> Sequence[DashboardPoint]:
        with self.engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT unixtime, hr_counter1, hr_counter2 "
                    "FROM intervalproduction "
                    "WHERE unixtime > :t1 "
                    "AND unixtime <= :t2 "
                    "ORDER BY unixtime ASC"
                ),
                {"t1": t1, "t2": t2}
            )
            rows = result.mappings().all()
            return [DashboardPoint(**row) for row in rows]
