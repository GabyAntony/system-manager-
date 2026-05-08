"""
Funciones helper generales
"""

from datetime import datetime, timedelta
from typing import Union


def format_duration(seconds: int) -> str:
    """Formatear duración en segundos a texto legible"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def format_time_remaining(seconds: int) -> str:
    """Formatear tiempo restante como MM:SS"""
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"


def calculate_completion_rate(completed: int, total: int) -> float:
    """Calcular tasa de completado"""
    if total == 0:
        return 0.0
    
    return (completed / total) * 100


def get_time_ago(dt: datetime) -> str:
    """Obtener texto de "hace X tiempo" """
    now = datetime.utcnow()
    diff = now - dt
    
    if diff < timedelta(minutes=1):
        return "ahora"
    elif diff < timedelta(hours=1):
        minutes = diff.seconds // 60
        return f"hace {minutes} min"
    elif diff < timedelta(days=1):
        hours = diff.seconds // 3600
        return f"hace {hours} h"
    elif diff < timedelta(weeks=1):
        days = diff.days
        return f"hace {days} días"
    else:
        weeks = diff.days // 7
        return f"hace {weeks} semanas"


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncar texto con elipsis"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."


def get_priority_color(priority: str) -> str:
    """Obtener color para prioridad"""
    colors = {
        "high": "red",
        "medium": "yellow", 
        "low": "green"
    }
    return colors.get(priority, "white")


def get_status_color(status: str) -> str:
    """Obtener color para estado"""
    colors = {
        "pending": "yellow",
        "completed": "green",
        "cancelled": "red"
    }
    return colors.get(status, "white")


def format_task_title(title: str, max_length: int = 30) -> str:
    """Formatear título de tarea"""
    return truncate_text(title, max_length)


def is_today(dt: datetime) -> bool:
    """Verificar si fecha es hoy"""
    return dt.date() == datetime.utcnow().date()


def is_this_week(dt: datetime) -> bool:
    """Verificar si fecha es esta semana"""
    now = datetime.utcnow()
    week_start = now - timedelta(days=now.weekday())
    return dt >= week_start


def get_week_number(dt: datetime) -> int:
    """Obtener número de semana del año"""
    return dt.isocalendar()[1]


def get_month_name(dt: datetime) -> str:
    """Obtener nombre del mes en español"""
    months = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    return months[dt.month - 1]


def format_date_short(dt: datetime) -> str:
    """Formatear fecha corta"""
    return dt.strftime("%d/%m")


def format_datetime_short(dt: datetime) -> str:
    """Formatear fecha y hora cortas"""
    return dt.strftime("%d/%m %H:%M")
