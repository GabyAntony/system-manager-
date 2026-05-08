"""
Pomodoro Module - New API Pattern

This module implements BaseModuleAPI interface for Pomodoro timer management,
communicating with core through controlled API bridge.
"""

import time
import threading
from datetime import datetime
from typing import Any, Dict, List
from ...api.base import BaseModuleAPI, ModuleResult


class PomodoroModule(BaseModuleAPI):
    """
    Módulo de gestión Pomodoro implementando BaseModuleAPI.
    
    Se comunica con el core a través del CoreAPI sin acceder
    directamente a la base de datos.
    """
    
    def __init__(self):
        self._core_api = None
        self._current_session = None
        self._timer_thread = None
        self._stop_event = threading.Event()
        self._start_time = None
        self._duration = 0
        self._session_type = "work"
        self._task_id = None
    
    def set_core_api(self, core_api):
        """Inyectar instancia de CoreAPI"""
        self._core_api = core_api
    
    def execute(self, command: str, **kwargs) -> ModuleResult:
        """
        Ejecutar comando de Pomodoro.
        
        Args:
            command: Comando a ejecutar
            **kwargs: Parámetros del comando
            
        Returns:
            ModuleResult con el resultado
        """
        if self._core_api is None:
            return ModuleResult.error_result("CoreAPI no inicializado")
        
        if command == "start":
            return self._start_session(**kwargs)
        elif command == "stop":
            return self._stop_session(**kwargs)
        elif command == "status":
            return self._get_status(**kwargs)
        elif command == "list":
            return self._list_sessions(**kwargs)
        elif command == "stats":
            return self._get_stats(**kwargs)
        else:
            return ModuleResult.error_result(f"Comando '{command}' no reconocido")
    
    def get_commands(self) -> List[str]:
        """Retornar lista de comandos disponibles"""
        return ["start", "stop", "status", "list", "stats"]
    
    def _start_session(self, duration: int, session_type: str = "work", task_id: int = None) -> ModuleResult:
        """Iniciar una sesión Pomodoro"""
        if self._timer_thread and self._timer_thread.is_alive():
            return ModuleResult.error_result("Ya hay una sesión Pomodoro activa")
        
        if not duration or duration <= 0:
            return ModuleResult.error_result("La duración debe ser un número positivo")
        
        if session_type not in ["work", "break", "long_break"]:
            return ModuleResult.error_result("El tipo de sesión debe ser 'work', 'break' o 'long_break'")
        
        # Crear sesión en base de datos a través del CoreAPI
        session_result = self._core_api.create_pomodoro_session(
            duration=duration,
            session_type=session_type,
            task_id=task_id
        )
        
        if not session_result.success:
            return session_result
        
        session_data = session_result.data
        
        # Iniciar timer
        self._current_session = session_data
        self._duration = duration * 60  # Convertir a segundos
        self._session_type = session_type
        self._task_id = task_id
        self._start_time = datetime.utcnow()
        self._stop_event.clear()
        
        # Iniciar thread del timer
        self._timer_thread = threading.Thread(target=self._timer_worker)
        self._timer_thread.daemon = True
        self._timer_thread.start()
        
        return ModuleResult.success_result(
            data={
                'session_id': session_data['id'],
                'duration': duration,
                'session_type': session_type,
                'task_id': task_id,
                'status': 'running'
            },
            message=f"Sesión Pomodoro {session_type} iniciada (ID: {session_data['id']})"
        )
    
    def _stop_session(self, **kwargs) -> ModuleResult:
        """Detener la sesión actual"""
        if not self._timer_thread or not self._timer_thread.is_alive():
            return ModuleResult.error_result("No hay una sesión activa")
        
        # Detener timer
        self._stop_event.set()
        self._timer_thread.join(timeout=5)
        
        # Calcular si se completó
        elapsed = (datetime.utcnow() - self._start_time).total_seconds()
        was_completed = elapsed >= self._duration
        
        # Actualizar sesión en base de datos
        update_data = {
            'completed_at': datetime.utcnow(),
            'was_completed': was_completed
        }
        
        update_result = self._core_api.update_pomodoro_session(
            self._current_session['id'],
            **update_data
        )
        
        # Limpiar estado
        session_id = self._current_session['id']
        self._current_session = None
        self._timer_thread = None
        
        status_text = "completada" if was_completed else "cancelada"
        
        return ModuleResult.success_result(
            data={
                'session_id': session_id,
                'status': 'stopped',
                'was_completed': was_completed,
                'elapsed_seconds': elapsed
            },
            message=f"Sesión {session_id} {status_text}"
        )
    
    def _get_status(self, **kwargs) -> ModuleResult:
        """Obtener estado de la sesión actual"""
        if not self._current_session:
            return ModuleResult.success_result(
                data={'status': 'idle'},
                message="No hay sesión activa"
            )
        
        if not self._timer_thread or not self._timer_thread.is_alive():
            return ModuleResult.success_result(
                data={'status': 'stopped'},
                message="Sesión detenida"
            )
        
        # Calcular tiempo restante
        elapsed = (datetime.utcnow() - self._start_time).total_seconds()
        remaining = max(0, self._duration - elapsed)
        
        return ModuleResult.success_result(
            data={
                'status': 'running',
                'session_id': self._current_session['id'],
                'session_type': self._session_type,
                'duration': self._duration / 60,  # Convertir a minutos
                'elapsed_seconds': elapsed,
                'remaining_seconds': remaining,
                'progress_percentage': (elapsed / self._duration) * 100 if self._duration > 0 else 0
            }
        )
    
    def _list_sessions(self, limit: int = 50) -> ModuleResult:
        """Listar sesiones recientes"""
        if limit and limit <= 0:
            return ModuleResult.error_result("El límite debe ser un número positivo")
        
        return self._core_api.get_pomodoro_sessions(limit=limit or 50)
    
    def _get_stats(self, **kwargs) -> ModuleResult:
        """Obtener estadísticas de Pomodoro"""
        return self._core_api.get_statistics("pomodoro", kwargs)
    
    def _timer_worker(self):
        """Worker del timer en background"""
        try:
            # Esperar hasta que se complete el tiempo o se detenga
            if self._stop_event.wait(timeout=self._duration):
                # Fue detenido manualmente
                return
            
            # El timer se completó naturalmente
            if self._current_session:
                # Actualizar como completado
                self._core_api.update_pomodoro_session(
                    self._current_session['id'],
                    completed_at=datetime.utcnow(),
                    was_completed=True
                )
                
                # Enviar notificación (si está habilitado)
                self._send_completion_notification()
                
        except Exception as e:
            # Log error pero no interrumpir
            pass
    
    def _send_completion_notification(self):
        """Enviar notificación de completion"""
        try:
            # Obtener configuración de notificaciones
            config_result = self._core_api.get_config("pomodoro.notifications")
            
            if config_result.success and config_result.data:
                # Aquí se podría integrar con un sistema de notificaciones
                # Por ahora solo registramos en consola
                session_type_text = {
                    'work': 'Trabajo',
                    'break': 'Descanso',
                    'long_break': 'Descanso largo'
                }.get(self._session_type, self._session_type)
                
                print(f"✅ Sesión de {session_type_text} completada!")
                
        except Exception:
            # Ignorar errores de notificación
            pass
