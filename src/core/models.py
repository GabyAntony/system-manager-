"""
Modelos de datos para la CLI de productividad
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Task(Base):
    """Modelo de tareas"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(10), default="medium")  # high, medium, low
    status = Column(String(20), default="pending")  # pending, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    

class PomodoroSession(Base):
    """Modelo de sesiones Pomodoro"""
    __tablename__ = "pomodoro_sessions"
    
    id = Column(Integer, primary_key=True)
    duration = Column(Integer, nullable=False)  # minutos
    session_type = Column(String(10), nullable=False)  # work, break, long_break
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    was_completed = Column(Boolean, default=False)
    task_id = Column(Integer, nullable=True)  # Opcional: asociar a tarea
    
    

class Note(Base):
    """Modelo de metadatos de notas de Obsidian"""
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True)
    obsidian_path = Column(String(500), nullable=False)
    title = Column(String(200), nullable=False)
    content_preview = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)  # JSON string de tags
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    

class Habit(Base):
    """Modelo de hábitos (para futura expansión)"""
    __tablename__ = "habits"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    target_frequency = Column(String(20), default="daily")  # daily, weekly, monthly
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    
