"""
Gestor de tareas
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from ...core import get_db, Task


class TaskManager:
    """Gestor de tareas de la CLI"""
    
    def __init__(self):
        self.db: Session = get_db()
    
    def create_task(self, title: str, description: str = "", priority: str = "medium") -> Task:
        """Crear una nueva tarea"""
        task = Task(
            title=title,
            description=description,
            priority=priority,
            status="pending"
        )
        
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        
        return task
    
    def list_tasks(self, status: str = None, priority: str = None) -> List[Task]:
        """Listar tareas con filtros opcionales"""
        query = self.db.query(Task)
        
        if status:
            query = query.filter(Task.status == status)
        
        if priority:
            query = query.filter(Task.priority == priority)
        
        return query.order_by(Task.created_at.desc()).all()
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Obtener una tarea por ID"""
        return self.db.query(Task).filter(Task.id == task_id).first()
    
    def complete_task(self, task_id: int) -> bool:
        """Marcar tarea como completada"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        task.status = "completed"
        task.completed_at = datetime.utcnow()
        
        self.db.commit()
        return True
    
    def delete_task(self, task_id: int) -> bool:
        """Eliminar una tarea"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        self.db.delete(task)
        self.db.commit()
        return True
    
    def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        """Actualizar una tarea"""
        task = self.get_task(task_id)
        if not task:
            return None
        
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def get_pending_tasks(self) -> List[Task]:
        """Obtener tareas pendientes"""
        return self.list_tasks(status="pending")
    
    def get_completed_tasks(self) -> List[Task]:
        """Obtener tareas completadas"""
        return self.list_tasks(status="completed")
    
    def get_high_priority_tasks(self) -> List[Task]:
        """Obtener tareas de alta prioridad"""
        return self.list_tasks(priority="high", status="pending")
    
    def get_task_stats(self) -> dict:
        """Obtener estadísticas de tareas"""
        total = self.db.query(Task).count()
        pending = self.db.query(Task).filter(Task.status == "pending").count()
        completed = self.db.query(Task).filter(Task.status == "completed").count()
        cancelled = self.db.query(Task).filter(Task.status == "cancelled").count()
        
        high_priority = self.db.query(Task).filter(
            Task.priority == "high", 
            Task.status == "pending"
        ).count()
        
        return {
            "total": total,
            "pending": pending,
            "completed": completed,
            "cancelled": cancelled,
            "high_priority": high_priority,
            "completion_rate": (completed / total * 100) if total > 0 else 0
        }
