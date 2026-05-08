"""
Task Module - New API Pattern

This module implements the BaseModuleAPI interface for task management,
communicating with the core through the controlled API bridge.
"""

from typing import Any, Dict, List
from ...api.base import BaseModuleAPI, ModuleResult


class TaskModule(BaseModuleAPI):
    """
    Módulo de gestión de tareas implementando BaseModuleAPI.
    
    Se comunica con el core a través del CoreAPI sin acceder
    directamente a la base de datos.
    """
    
    def __init__(self):
        self._core_api = None
    
    def set_core_api(self, core_api):
        """Inyectar instancia de CoreAPI"""
        self._core_api = core_api
    
    def execute(self, command: str, **kwargs) -> ModuleResult:
        """
        Ejecutar comando de tareas.
        
        Args:
            command: Comando a ejecutar
            **kwargs: Parámetros del comando
            
        Returns:
            ModuleResult con el resultado
        """
        if self._core_api is None:
            return ModuleResult.error_result("CoreAPI no inicializado")
        
        if command == "create":
            return self._create_task(**kwargs)
        elif command == "list":
            return self._list_tasks(**kwargs)
        elif command == "get":
            return self._get_task(**kwargs)
        elif command == "update":
            return self._update_task(**kwargs)
        elif command == "complete":
            return self._complete_task(**kwargs)
        elif command == "delete":
            return self._delete_task(**kwargs)
        elif command == "stats":
            return self._get_task_stats(**kwargs)
        else:
            return ModuleResult.error_result(f"Comando '{command}' no reconocido")
    
    def get_commands(self) -> List[str]:
        """Retornar lista de comandos disponibles"""
        return ["create", "list", "get", "update", "complete", "delete", "stats"]
    
    def _create_task(self, title: str, description: str = "", priority: str = "medium") -> ModuleResult:
        """Crear una nueva tarea"""
        if not title:
            return ModuleResult.error_result("El título es requerido")
        
        if priority not in ["high", "medium", "low"]:
            return ModuleResult.error_result("La prioridad debe ser 'high', 'medium' o 'low'")
        
        return self._core_api.create_task(
            title=title,
            description=description,
            priority=priority
        )
    
    def _list_tasks(self, status: str = None, priority: str = None) -> ModuleResult:
        """Listar tareas con filtros opcionales"""
        # Validar filtros
        if status and status not in ["pending", "completed", "cancelled"]:
            return ModuleResult.error_result("El estado debe ser 'pending', 'completed' o 'cancelled'")
        
        if priority and priority not in ["high", "medium", "low"]:
            return ModuleResult.error_result("La prioridad debe ser 'high', 'medium' o 'low'")
        
        return self._core_api.get_tasks(status=status, priority=priority)
    
    def _get_task(self, task_id: int) -> ModuleResult:
        """Obtener una tarea por ID"""
        if not task_id or task_id <= 0:
            return ModuleResult.error_result("ID de tarea inválido")
        
        return self._core_api.get_task(task_id)
    
    def _update_task(self, task_id: int, **kwargs) -> ModuleResult:
        """Actualizar una tarea"""
        if not task_id or task_id <= 0:
            return ModuleResult.error_result("ID de tarea inválido")
        
        # Validar campos actualizables
        valid_fields = ["title", "description", "priority", "status"]
        updates = {}
        
        for field, value in kwargs.items():
            if field in valid_fields:
                # Validaciones específicas
                if field == "priority" and value not in ["high", "medium", "low"]:
                    return ModuleResult.error_result("La prioridad debe ser 'high', 'medium' o 'low'")
                
                if field == "status" and value not in ["pending", "completed", "cancelled"]:
                    return ModuleResult.error_result("El estado debe ser 'pending', 'completed' o 'cancelled'")
                
                updates[field] = value
        
        if not updates:
            return ModuleResult.error_result("No hay campos válidos para actualizar")
        
        return self._core_api.update_task(task_id, **updates)
    
    def _complete_task(self, task_id: int) -> ModuleResult:
        """Marcar tarea como completada"""
        if not task_id or task_id <= 0:
            return ModuleResult.error_result("ID de tarea inválido")
        
        return self._core_api.update_task(task_id, status="completed")
    
    def _delete_task(self, task_id: int) -> ModuleResult:
        """Eliminar una tarea"""
        if not task_id or task_id <= 0:
            return ModuleResult.error_result("ID de tarea inválido")
        
        return self._core_api.delete_task(task_id)
    
    def _get_task_stats(self, **kwargs) -> ModuleResult:
        """Obtener estadísticas de tareas"""
        return self._core_api.get_statistics("tasks", kwargs)
