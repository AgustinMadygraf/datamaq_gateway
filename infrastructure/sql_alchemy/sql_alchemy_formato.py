# filepath: c:\AppServ\www\datamaq_gateway\infrastructure\sql_alchemy\sql_alchemy_formato.py
"""
Path: infrastructure/sql_alchemy/sql_alchemy_formato.py
"""

from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from shared.config import get_mysql_config

from entities.formato import Formato
from interface_adapters.gateway.repositories import FormatoRepository

class SQLAlchemyFormatoRepository(FormatoRepository):
    "Repositorio SQLAlchemy para Formatos"
    def __init__(self):
        cfg = get_mysql_config()
        url = (
            "mysql+pymysql://"
            f"{cfg['user']}:"
            f"{cfg['password']}@"
            f"{cfg['host']}:"
            f"{cfg['port']}/"
            f"{cfg['database']}"
        )
        self.engine = create_engine(url)
        self.session = sessionmaker(bind=self.engine)

    def get_ultimo_formato(self) -> Optional[Formato]:
        with self.session() as session:
            result = session.execute(
                text(
                    "SELECT ID_formato as id_formato, "
                    "formato, "
                    "ancho as ancho_bobina_mm "
                    "FROM tabla_1 "
                    "ORDER BY ID_formato DESC "
                    "LIMIT 1"
                )
            ).fetchone()
            if result is None:
                print("[ERROR] No se encontró formato en la base de datos.")
                return None
            return Formato(**result._mapping)
