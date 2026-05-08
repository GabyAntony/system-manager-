"""
Validadores de datos
"""

from typing import Optional


def validate_priority(priority: str) -> Optional[str]:
    """Validar y normalizar prioridad"""
    valid_priorities = ["high", "medium", "low"]
    
    if priority.lower() in valid_priorities:
        return priority.lower()
    
    return None


def validate_task_title(title: str) -> bool:
    """Validar título de tarea"""
    if not title or not title.strip():
        return False
    
    if len(title.strip()) < 2:
        return False
    
    if len(title.strip()) > 200:
        return False
    
    return True


def validate_pomodoro_duration(duration: int) -> bool:
    """Validar duración de Pomodoro"""
    if not isinstance(duration, int):
        return False
    
    if duration < 1 or duration > 180:  # Máximo 3 horas
        return False
    
    return True


def validate_note_title(title: str) -> bool:
    """Validar título de nota"""
    if not title or not title.strip():
        return False
    
    if len(title.strip()) < 1:
        return False
    
    if len(title.strip()) > 100:
        return False
    
    return True


def sanitize_filename(filename: str) -> str:
    """Sanitizar nombre de archivo"""
    # Reemplazar caracteres problemáticos
    unsafe_chars = '<>:"/\\|?*'
    safe_name = filename
    
    for char in unsafe_chars:
        safe_name = safe_name.replace(char, '_')
    
    # Limitar longitud
    if len(safe_name) > 50:
        safe_name = safe_name[:50]
    
    return safe_name.strip()
