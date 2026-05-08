"""
Base Module Interface - API Layer

This module defines the standard interface that all modules must implement
to communicate with the core system through the controlled API bridge.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseModuleAPI(ABC):
    """
    Interfaz base para todos los módulos del sistema.
    
    Todos los módulos (Python) deben heredar de esta clase e implementar
    el método execute() como punto de entrada estándar.
    """
    
    @abstractmethod
    def execute(self, command: str, **kwargs) -> Dict[str, Any]:
        """
        Punto de entrada estándar para todos los módulos.
        
        Args:
            command: Comando a ejecutar (ej: 'create', 'list', 'update')
            **kwargs: Parámetros específicos del comando
            
        Returns:
            Dict con resultado estandarizado:
            {
                'success': bool,
                'data': Any,
                'message': str,
                'error': Optional[str]
            }
        """
        pass
    
    @abstractmethod
    def get_commands(self) -> List[str]:
        """
        Retorna la lista de comandos soportados por el módulo.
        
        Returns:
            Lista de nombres de comandos disponibles
        """
        pass
    
    def validate_command(self, command: str) -> bool:
        """
        Verifica si el comando es soportado por el módulo.
        
        Args:
            command: Nombre del comando a validar
            
        Returns:
            True si el comando es válido, False en caso contrario
        """
        return command in self.get_commands()


class ModuleResult:
    """
    Clase estándar para resultados de módulos.
    Proporciona una estructura consistente para todas las respuestas.
    """
    
    def __init__(self, success: bool = True, data: Any = None, 
                 message: str = "", error: Optional[str] = None):
        self.success = success
        self.data = data
        self.message = message
        self.error = error
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario para serialización"""
        return {
            'success': self.success,
            'data': self.data,
            'message': self.message,
            'error': self.error
        }
    
    @classmethod
    def success_result(cls, data: Any = None, message: str = "") -> 'ModuleResult':
        """Crear resultado exitoso"""
        return cls(success=True, data=data, message=message)
    
    @classmethod
    def error_result(cls, message: str, data: Any = None) -> 'ModuleResult':
        """Crear resultado de error"""
        return cls(success=False, data=data, error=message)
