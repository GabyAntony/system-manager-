"""
Configuración y gestión de base de datos
"""

import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base


class Database:
    """Gestor de base de datos SQLite"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Crear directorio ~/.cli-productividad si no existe
            home_dir = Path.home()
            cli_dir = home_dir / ".cli-productividad"
            cli_dir.mkdir(exist_ok=True)
            db_path = str(cli_dir / "data.db")
        
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Crear tablas si no existen
        self.create_tables()
    
    def create_tables(self):
        """Crear todas las tablas de la base de datos"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self) -> Session:
        """Obtener una sesión de base de datos"""
        return self.SessionLocal()
    
    def close(self):
        """Cerrar la conexión a la base de datos"""
        self.engine.dispose()


# Instancia global de la base de datos
db = Database()


def get_db() -> Session:
    """Dependency para obtener sesión de base de datos"""
    return db.get_db()
