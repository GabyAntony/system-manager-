"""
Database Manager - Core Layer (Logic Only)

This module provides pure database management without business logic.
It handles database connections, sessions, and basic operations only.
"""

import os
from pathlib import Path
from contextlib import contextmanager
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base


class DatabaseManager:
    """
    Gestor puro de base de datos SQLite.
    
    Contiene solo lógica de gestión de base de datos sin lógica de negocio.
    Proporciona conexiones y sesiones de forma segura.
    """
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Crear directorio ~/.cli-productividad si no existe
            home_dir = Path.home()
            cli_dir = home_dir / ".cli-productividad"
            cli_dir.mkdir(exist_ok=True)
            db_path = str(cli_dir / "data.db")
        
        self.db_path = db_path
        self._engine = None
        self._session_factory = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Inicializar motor de base de datos y fábrica de sesiones"""
        try:
            self._engine = create_engine(
                f"sqlite:///{self.db_path}",
                echo=False,
                pool_pre_ping=True
            )
            self._session_factory = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine
            )
            
            # Crear tablas si no existen
            self.create_tables()
            
        except Exception as e:
            raise Exception(f"No se pudo inicializar la base de datos: {str(e)}")
    
    def create_tables(self):
        """Crear todas las tablas de la base de datos"""
        try:
            Base.metadata.create_all(bind=self._engine)
        except Exception as e:
            raise Exception(f"No se pudieron crear las tablas: {str(e)}")
    
    def get_session(self) -> Session:
        """Obtener una sesión de base de datos"""
        if self._session_factory is None:
            raise Exception("DatabaseManager no está inicializado")
        
        return self._session_factory()
    
    @contextmanager
    def session_scope(self):
        """
        Context manager para manejo automático de sesiones.
        
        Usage:
            with db_manager.session_scope() as session:
                # Operaciones de base de datos
                session.add(obj)
                # Commit automático al salir del contexto
        """
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def close(self):
        """Cerrar la conexión a la base de datos"""
        if self._engine:
            self._engine.dispose()
            self._engine = None
            self._session_factory = None
    
    def get_db_path(self) -> str:
        """Obtener ruta del archivo de base de datos"""
        return self.db_path
    
    def backup_database(self, backup_path: str = None) -> str:
        """
        Crear backup de la base de datos.
        
        Args:
            backup_path: Ruta donde guardar el backup
            
        Returns:
            Ruta del backup creado
        """
        if backup_path is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{self.db_path}.backup_{timestamp}"
        
        try:
            import shutil
            # Cerrar conexiones antes del backup
            self.close()
            
            # Copiar archivo
            shutil.copy2(self.db_path, backup_path)
            
            # Re-inicializar
            self._initialize_database()
            
            return backup_path
            
        except Exception as e:
            # Intentar re-inicializar si falló
            try:
                self._initialize_database()
            except:
                pass
            raise Exception(f"No se pudo crear backup: {str(e)}")
    
    def restore_database(self, backup_path: str):
        """
        Restaurar base de datos desde backup.
        
        Args:
            backup_path: Ruta del backup a restaurar
        """
        try:
            import shutil
            
            # Verificar que el backup existe
            if not os.path.exists(backup_path):
                raise Exception(f"El backup {backup_path} no existe")
            
            # Cerrar conexiones
            self.close()
            
            # Restaurar archivo
            shutil.copy2(backup_path, self.db_path)
            
            # Re-inicializar
            self._initialize_database()
            
        except Exception as e:
            # Intentar re-inicializar si falló
            try:
                self._initialize_database()
            except:
                pass
            raise Exception(f"No se pudo restaurar backup: {str(e)}")
    
    def get_database_info(self) -> dict:
        """
        Obtener información sobre la base de datos.
        
        Returns:
            Dict con información de la base de datos
        """
        try:
            db_file = Path(self.db_path)
            
            # Obtener tamaño del archivo
            size_bytes = db_file.stat().st_size if db_file.exists() else 0
            size_mb = size_bytes / (1024 * 1024)
            
            # Obtener fecha de modificación
            modified_time = db_file.stat().st_mtime if db_file.exists() else None
            
            # Contar registros en cada tabla
            table_counts = {}
            with self.session_scope() as session:
                for table in Base.metadata.tables.keys():
                    try:
                        count = session.execute(f"SELECT COUNT(*) FROM {table}").scalar()
                        table_counts[table] = count
                    except Exception:
                        table_counts[table] = 0
            
            return {
                'path': self.db_path,
                'size_bytes': size_bytes,
                'size_mb': round(size_mb, 2),
                'modified_time': modified_time,
                'table_counts': table_counts,
                'tables': list(Base.metadata.tables.keys())
            }
            
        except Exception as e:
            return {
                'path': self.db_path,
                'error': str(e),
                'tables': []
            }
    
    def vacuum_database(self):
        """
        Optimizar la base de datos con VACUUM.
        """
        try:
            with self.session_scope() as session:
                session.execute("VACUUM")
                
        except Exception as e:
            raise Exception(f"No se pudo optimizar la base de datos: {str(e)}")
    
    def check_integrity(self) -> dict:
        """
        Verificar integridad de la base de datos.
        
        Returns:
            Dict con resultado de la verificación
        """
        try:
            with self.session_scope() as session:
                result = session.execute("PRAGMA integrity_check").fetchall()
                
                # SQLite devuelve "ok" si todo está bien
                is_ok = len(result) == 1 and result[0][0] == "ok"
                
                return {
                    'integrity_ok': is_ok,
                    'details': [row[0] for row in result]
                }
                
        except Exception as e:
            return {
                'integrity_ok': False,
                'error': str(e),
                'details': []
            }
    
    def execute_raw_query(self, query: str, params: dict = None) -> list:
        """
        Ejecutar consulta SQL cruda (solo para operaciones de mantenimiento).
        
        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros de la consulta
            
        Returns:
            Lista de resultados
        """
        try:
            with self.session_scope() as session:
                if params:
                    result = session.execute(query, params)
                else:
                    result = session.execute(query)
                
                return result.fetchall()
                
        except Exception as e:
            raise Exception(f"Error ejecutando consulta: {str(e)}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
