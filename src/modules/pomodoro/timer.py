"""
Temporizador Pomodoro con notificaciones
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from plyer import notification
from sqlalchemy.orm import Session
from ...core import get_db, PomodoroSession, Task
from ...utilitis.theme import print_success, print_error, print_warning, print_info


class PomodoroTimer:
    """Gestor de sesiones Pomodoro"""
    
    def __init__(self):
        self.db = get_db()
        self._current_session = None
        self._timer_thread = None
        self._stop_event = threading.Event()
        self._start_time = None
        self._duration = 0
        self._session_type = "work"
        self._task_id = None
    
    def start_session(self, duration: int, session_type: str = "work", task_id: int = None):
        """Iniciar una sesión Pomodoro"""
        if self._timer_thread and self._timer_thread.is_alive():
            print_error("Ya hay una sesión Pomodoro activa")
            return
        
        # Crear sesión en base de datos
        session = PomodoroSession(
            duration=duration,
            session_type=session_type,
            task_id=task_id
        )
        
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        
        # Iniciar timer
        self._current_session = session
        self._duration = duration * 60  # Convertir a segundos
        self._session_type = session_type
        self._task_id = task_id
        self._start_time = datetime.utcnow()
        self._stop_event.clear()
        
        # Iniciar thread
        self._timer_thread = threading.Thread(target=self._run_timer)
        self._timer_thread.daemon = True
        self._timer_thread.start()
        
        # Notificación de inicio
        self._notify_start()
    
    def _run_timer(self):
        """Ejecutar el timer en background"""
        elapsed = 0
        
        while not self._stop_event.is_set() and elapsed < self._duration:
            time.sleep(1)
            elapsed += 1
        
        if not self._stop_event.is_set():
            # Sesión completada
            self._complete_session()
    
    def _complete_session(self):
        """Marcar sesión como completada"""
        if self._current_session:
            self._current_session.completed_at = datetime.utcnow()
            self._current_session.was_completed = True
            self.db.commit()
            
            # Notificación de completado
            self._notify_complete()
        
        self._current_session = None
    
    def stop_session(self):
        """Detener la sesión actual"""
        if self._timer_thread and self._timer_thread.is_alive():
            self._stop_event.set()
            self._timer_thread.join()
            
            if self._current_session:
                self._current_session.completed_at = datetime.utcnow()
                self._current_session.was_completed = False
                self.db.commit()
            
            self._current_session = None
            print_info("Sesión Pomodoro detenida")
    
    def get_status(self) -> Dict[str, Any]:
        """Obtener estado actual del timer"""
        if not self._current_session or not self._timer_thread or not self._timer_thread.is_alive():
            return {
                "is_active": False,
                "session_type": None,
                "remaining_seconds": 0,
                "started_at": None
            }
        
        elapsed = (datetime.utcnow() - self._start_time).total_seconds()
        remaining = max(0, self._duration - elapsed)
        
        return {
            "is_active": True,
            "session_type": self._session_type,
            "remaining_seconds": int(remaining),
            "started_at": self._start_time.strftime("%H:%M:%S"),
            "task_id": self._task_id
        }
    
    def _notify_start(self):
        """Enviar notificación de inicio"""
        titles = {
            "work": "◆ Pomodoro Iniciado",
            "break": "◆ Descanso Iniciado", 
            "long_break": "◆ Descanso Largo Iniciado"
        }
        
        messages = {
            "work": f"Tiempo de concentración por {self._duration // 60} minutos",
            "break": f"Tiempo de descanso por {self._duration // 60} minutos",
            "long_break": f"Descanso largo por {self._duration // 60} minutos"
        }
        
        try:
            notification.notify(
                title=titles.get(self._session_type, "Pomodoro"),
                message=messages.get(self._session_type, ""),
                timeout=5
            )
        except Exception:
            pass  # Silenciosamente fallar si no hay notificaciones
    
    def _notify_complete(self):
        """Enviar notificación de completado"""
        titles = {
            "work": "✓ Pomodoro Completado",
            "break": "✓ Descanso Completado",
            "long_break": "✓ Descanso Largo Completado"
        }
        
        messages = {
            "work": "¡Buen trabajo! Tiempo de un descanso",
            "break": "Descanso terminado. ¡Listo para seguir!",
            "long_break": "Descanso largo completado. ¡A seguir!"
        }
        
        try:
            notification.notify(
                title=titles.get(self._session_type, "Pomodoro"),
                message=messages.get(self._session_type, ""),
                timeout=10
            )
        except Exception:
            pass
    
    def get_session_history(self, limit: int = 10) -> list:
        """Obtener historial de sesiones"""
        sessions = self.db.query(PomodoroSession).order_by(
            PomodoroSession.started_at.desc()
        ).limit(limit).all()
        
        return [session.to_dict() for session in sessions]
    
    def get_today_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de hoy"""
        today = datetime.utcnow().date()
        
        sessions_today = self.db.query(PomodoroSession).filter(
            PomodoroSession.started_at >= today
        ).all()
        
        work_sessions = [s for s in sessions_today if s.session_type == "work"]
        completed_work = [s for s in work_sessions if s.was_completed]
        
        total_minutes = sum(s.duration for s in completed_work)
        
        return {
            "total_sessions": len(sessions_today),
            "work_sessions": len(work_sessions),
            "completed_work_sessions": len(completed_work),
            "total_work_minutes": total_minutes,
            "completion_rate": (len(completed_work) / len(work_sessions) * 100) if work_sessions else 0
        }
