"""
Core API - Controlled Bridge Between Modules and Core

This module provides a secure, controlled interface for modules to interact
with the core system without exposing core internals directly.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime

from ..core.database_manager import DatabaseManager
from ..core.config_manager import ConfigManager
from ..core.models import Task, PomodoroSession, Note, Habit
from .base import ModuleResult


class CoreAPI:
    """
    Puente controlado entre módulos y el core del sistema.
    
    Proporciona métodos seguros para que los módulos accedan a la base de datos
    y configuración sin exponer los internos del core.
    """
    
    def __init__(self):
        self._db_manager = DatabaseManager()
        self._config_manager = ConfigManager()
    
    # === Task Management Methods ===
    
    def create_task(self, title: str, description: str = "", priority: str = "medium") -> ModuleResult:
        """Crear una nueva tarea de forma segura"""
        try:
            with self._db_manager.get_session() as session:
                task = Task(
                    title=title,
                    description=description,
                    priority=priority,
                    status="pending"
                )
                
                session.add(task)
                session.commit()
                session.refresh(task)
                
                return ModuleResult.success_result(
                    data=self._serialize_task(task),
                    message=f"Tarea creada: {task.title} (ID: {task.id})"
                )
        except Exception as e:
            return ModuleResult.error_result(f"Error al crear tarea: {str(e)}")
    
    def get_tasks(self, status: Optional[str] = None, priority: Optional[str] = None) -> ModuleResult:
        """Obtener tareas con filtros opcionales"""
        try:
            with self._db_manager.get_session() as session:
                query = session.query(Task)
                
                if status:
                    query = query.filter(Task.status == status)
                
                if priority:
                    query = query.filter(Task.priority == priority)
                
                tasks = query.order_by(Task.created_at.desc()).all()
                
                return ModuleResult.success_result(
                    data=[self._serialize_task(task) for task in tasks],
                    message=f"Se encontraron {len(tasks)} tareas"
                )
        except Exception as e:
            return ModuleResult.error_result(f"Error al obtener tareas: {str(e)}")
    
    def get_task(self, task_id: int) -> ModuleResult:
        """Obtener una tarea por ID"""
        try:
            with self._db_manager.get_session() as session:
                task = session.query(Task).filter(Task.id == task_id).first()
                
                if not task:
                    return ModuleResult.error_result(f"Tarea con ID {task_id} no encontrada")
                
                return ModuleResult.success_result(data=self._serialize_task(task))
        except Exception as e:
            return ModuleResult.error_result(f"Error al obtener tarea: {str(e)}")
    
    def update_task(self, task_id: int, **kwargs) -> ModuleResult:
        """Actualizar una tarea"""
        try:
            with self._db_manager.get_session() as session:
                task = session.query(Task).filter(Task.id == task_id).first()
                
                if not task:
                    return ModuleResult.error_result(f"Tarea con ID {task_id} no encontrada")
                
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                
                if 'status' in kwargs and kwargs['status'] == 'completed':
                    task.completed_at = datetime.utcnow()
                
                session.commit()
                session.refresh(task)
                
                return ModuleResult.success_result(
                    data=self._serialize_task(task),
                    message=f"Tarea {task_id} actualizada"
                )
        except Exception as e:
            return ModuleResult.error_result(f"Error al actualizar tarea: {str(e)}")
    
    def delete_task(self, task_id: int) -> ModuleResult:
        """Eliminar una tarea"""
        try:
            with self._db_manager.get_session() as session:
                task = session.query(Task).filter(Task.id == task_id).first()
                
                if not task:
                    return ModuleResult.error_result(f"Tarea con ID {task_id} no encontrada")
                
                session.delete(task)
                session.commit()
                
                return ModuleResult.success_result(
                    message=f"Tarea {task_id} eliminada"
                )
        except Exception as e:
            return ModuleResult.error_result(f"Error al eliminar tarea: {str(e)}")
    
    # === Pomodoro Session Methods ===
    
    def create_pomodoro_session(self, duration: int, session_type: str = "work", task_id: Optional[int] = None) -> ModuleResult:
        """Crear una nueva sesión Pomodoro"""
        try:
            with self._db_manager.get_session() as session:
                pomodoro_session = PomodoroSession(
                    duration=duration,
                    session_type=session_type,
                    task_id=task_id
                )
                
                session.add(pomodoro_session)
                session.commit()
                session.refresh(pomodoro_session)
                
                return ModuleResult.success_result(
                    data=self._serialize_pomodoro_session(pomodoro_session),
                    message=f"Sesión Pomodoro creada (ID: {pomodoro_session.id})"
                )
        except Exception as e:
            return ModuleResult.error_result(f"Error al crear sesión Pomodoro: {str(e)}")
    
    def get_pomodoro_sessions(self, limit: int = 50) -> ModuleResult:
        """Obtener sesiones Pomodoro recientes"""
        try:
            with self._db_manager.get_session() as session:
                sessions = session.query(PomodoroSession)\
                    .order_by(PomodoroSession.started_at.desc())\
                    .limit(limit)\
                    .all()
                
                return ModuleResult.success_result(
                    data=[self._serialize_pomodoro_session(session) for session in sessions],
                    message=f"Se encontraron {len(sessions)} sesiones"
                )
        except Exception as e:
            return ModuleResult.error_result(f"Error al obtener sesiones Pomodoro: {str(e)}")
    
    def update_pomodoro_session(self, session_id: int, **kwargs) -> ModuleResult:
        """Actualizar una sesión Pomodoro"""
        try:
            with self._db_manager.get_session() as session:
                pomodoro_session = session.query(PomodoroSession)\
                    .filter(PomodoroSession.id == session_id)\
                    .first()
                
                if not pomodoro_session:
                    return ModuleResult.error_result(f"Sesión con ID {session_id} no encontrada")
                
                for key, value in kwargs.items():
                    if hasattr(pomodoro_session, key):
                        setattr(pomodoro_session, key, value)
                
                session.commit()
                session.refresh(pomodoro_session)
                
                return ModuleResult.success_result(
                    data=self._serialize_pomodoro_session(pomodoro_session),
                    message=f"Sesión {session_id} actualizada"
                )
        except Exception as e:
            return ModuleResult.error_result(f"Error al actualizar sesión: {str(e)}")
    
    # === Note Management Methods ===
    
    def create_note(self, obsidian_path: str, title: str, content_preview: str = "", tags: str = "") -> ModuleResult:
        """Crear metadatos de nota de Obsidian"""
        try:
            with self._db_manager.get_session() as session:
                note = Note(
                    obsidian_path=obsidian_path,
                    title=title,
                    content_preview=content_preview,
                    tags=tags
                )
                
                session.add(note)
                session.commit()
                session.refresh(note)
                
                return ModuleResult.success_result(
                    data=self._serialize_note(note),
                    message=f"Nota '{title}' registrada"
                )
        except Exception as e:
            return ModuleResult.error_result(f"Error al crear nota: {str(e)}")
    
    def get_notes(self, limit: int = 100) -> ModuleResult:
        """Obtener notas recientes"""
        try:
            with self._db_manager.get_session() as session:
                notes = session.query(Note)\
                    .order_by(Note.updated_at.desc())\
                    .limit(limit)\
                    .all()
                
                return ModuleResult.success_result(
                    data=[self._serialize_note(note) for note in notes],
                    message=f"Se encontraron {len(notes)} notas"
                )
        except Exception as e:
            return ModuleResult.error_result(f"Error al obtener notas: {str(e)}")
    
    # === Configuration Methods ===
    
    def get_config(self, key: str = None, default: Any = None) -> ModuleResult:
        """Obtener valor de configuración"""
        try:
            if key:
                value = self._config_manager.get(key, default)
                return ModuleResult.success_result(data=value)
            else:
                config = self._config_manager.get_all()
                return ModuleResult.success_result(data=config)
        except Exception as e:
            return ModuleResult.error_result(f"Error al obtener configuración: {str(e)}")
    
    def set_config(self, key: str, value: Any) -> ModuleResult:
        """Establecer valor de configuración"""
        try:
            self._config_manager.set(key, value)
            return ModuleResult.success_result(
                message=f"Configuración '{key}' actualizada"
            )
        except Exception as e:
            return ModuleResult.error_result(f"Error al establecer configuración: {str(e)}")
    
    # === Statistics Methods ===
    
    def get_statistics(self, module: str, filters: Dict = None) -> ModuleResult:
        """Obtener estadísticas para un módulo específico"""
        try:
            # Implementación básica - puede ser extendida
            if module == "tasks":
                return self._get_task_statistics(filters)
            elif module == "pomodoro":
                return self._get_pomodoro_statistics(filters)
            else:
                return ModuleResult.error_result(f"Módulo '{module}' no soportado para estadísticas")
        except Exception as e:
            return ModuleResult.error_result(f"Error al obtener estadísticas: {str(e)}")
    
    def _get_task_statistics(self, filters: Dict = None) -> ModuleResult:
        """Obtener estadísticas de tareas"""
        with self._db_manager.get_session() as session:
            total_tasks = session.query(Task).count()
            completed_tasks = session.query(Task).filter(Task.status == 'completed').count()
            pending_tasks = session.query(Task).filter(Task.status == 'pending').count()
            
            stats = {
                'total': total_tasks,
                'completed': completed_tasks,
                'pending': pending_tasks,
                'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            }
            
            return ModuleResult.success_result(data=stats)
    
    def _get_pomodoro_statistics(self, filters: Dict = None) -> ModuleResult:
        """Obtener estadísticas de Pomodoro"""
        with self._db_manager.get_session() as session:
            total_sessions = session.query(PomodoroSession).count()
            completed_sessions = session.query(PomodoroSession).filter(PomodoroSession.was_completed == True).count()
            
            # Calcular tiempo total en minutos
            sessions = session.query(PomodoroSession).all()
            total_minutes = sum(s.duration for s in sessions if s.was_completed)
            
            stats = {
                'total_sessions': total_sessions,
                'completed_sessions': completed_sessions,
                'completion_rate': (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0,
                'total_minutes': total_minutes,
                'total_hours': total_minutes / 60
            }
            
            return ModuleResult.success_result(data=stats)
    
    # === Serialization Methods ===
    
    def _serialize_task(self, task) -> Dict[str, Any]:
        """Serialize Task model to dictionary"""
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "status": task.status,
            "created_at": task.created_at,
            "completed_at": task.completed_at
        }
    
    def _serialize_pomodoro_session(self, session) -> Dict[str, Any]:
        """Serialize PomodoroSession model to dictionary"""
        return {
            "id": session.id,
            "duration": session.duration,
            "session_type": session.session_type,
            "started_at": session.started_at,
            "completed_at": session.completed_at,
            "was_completed": session.was_completed,
            "task_id": session.task_id
        }
    
    def _serialize_note(self, note) -> Dict[str, Any]:
        """Serialize Note model to dictionary"""
        return {
            "id": note.id,
            "obsidian_path": note.obsidian_path,
            "title": note.title,
            "content_preview": note.content_preview,
            "tags": note.tags,
            "created_at": note.created_at,
            "updated_at": note.updated_at
        }
    
    def _serialize_habit(self, habit) -> Dict[str, Any]:
        """Serialize Habit model to dictionary"""
        return {
            "id": habit.id,
            "name": habit.name,
            "description": habit.description,
            "target_frequency": habit.target_frequency,
            "created_at": habit.created_at,
            "is_active": habit.is_active
        }
