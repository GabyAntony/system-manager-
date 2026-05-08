"""
Command Orchestrator - Core Layer

This module coordinates command execution between CLI, modules, and core systems.
It implements the centralized command pattern defined in the architecture.
"""

import importlib
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
from ..api.core_api import CoreAPI
from ..api.base import ModuleResult
from .security import SecurityManager


class CommandOrchestrator:
    """
    Orquestador de comandos - coordina módulos sin exponer core.
    
    Actúa como punto central de coordinación entre la CLI y los módulos,
    gestionando seguridad y ejecución de comandos.
    """
    
    def __init__(self):
        self._core_api = CoreAPI()
        self._security_manager = SecurityManager()
        self._loaded_modules = {}
        self._initialize_modules()
    
    def _initialize_modules(self):
        """Cargar módulos Python registrados"""
        modules_dir = Path(__file__).parent.parent / "modules"
        
        if not modules_dir.exists():
            return
        
        # Cargar módulos automáticamente
        for module_dir in modules_dir.iterdir():
            if module_dir.is_dir() and (module_dir / "__init__.py").exists():
                try:
                    module_name = f"src.modules.{module_dir.name}"
                    module = importlib.import_module(module_name)
                    
                    # Buscar clases que hereden de BaseModuleAPI
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (hasattr(attr, '__bases__') and 
                            any('BaseModuleAPI' in base.__name__ for base in attr.__bases__)):
                            
                            instance = attr()
                            self._loaded_modules[module_dir.name] = instance
                            break
                            
                except Exception as e:
                    # Ignorar módulos que no se puedan cargar
                    pass
    
    def execute_module_command(self, module_name: str, command: str, **kwargs) -> ModuleResult:
        """
        Ejecutar comando de módulo a través del API layer.
        
        Args:
            module_name: Nombre del módulo
            command: Comando a ejecutar
            **kwargs: Parámetros del comando
            
        Returns:
            ModuleResult con el resultado de la ejecución
        """
        try:
            # Verificar que el módulo existe
            if module_name not in self._loaded_modules:
                return ModuleResult.error_result(
                    f"Módulo '{module_name}' no encontrado o no cargado"
                )
            
            module = self._loaded_modules[module_name]
            
            # Verificar que el comando es válido
            if not module.validate_command(command):
                available_commands = module.get_commands()
                return ModuleResult.error_result(
                    f"Comando '{command}' no válido. Comandos disponibles: {available_commands}"
                )
            
            # Inyectar CoreAPI en el módulo si lo necesita
            if hasattr(module, 'set_core_api'):
                module.set_core_api(self._core_api)
            
            # Ejecutar comando
            result = module.execute(command, **kwargs)
            
            # Asegurar que el resultado sea un ModuleResult
            if not isinstance(result, ModuleResult):
                return ModuleResult.success_result(data=result)
            
            return result
            
        except Exception as e:
            return ModuleResult.error_result(
                f"Error ejecutando comando '{command}' en módulo '{module_name}': {str(e)}"
            )
    
    def execute_submodule_command(self, submodule_path: str, args: List[str]) -> ModuleResult:
        """
        Ejecutar submódulo externo (.sh) con verificación de seguridad.
        
        Args:
            submodule_path: Ruta al submódulo
            args: Argumentos para el submódulo
            
        Returns:
            ModuleResult con el resultado de la ejecución
        """
        try:
            # Verificar seguridad del submódulo
            verification = self._security_manager.verify_submodule(submodule_path)
            
            if not verification['trusted']:
                if not verification['registered']:
                    # Submódulo no registrado - preguntar al usuario
                    return ModuleResult.error_result(
                        f"Submódulo no registrado: {verification['message']}. "
                        f"Registrelo primero con el comando 'security register'"
                    )
                else:
                    # Hash no coincide - revocar permisos
                    self._security_manager.revoke_permissions(submodule_path)
                    return ModuleResult.error_result(
                        f"Submódulo modificado no autorizado: {verification['message']}. "
                        f"Permisos revocados por seguridad."
                    )
            
            # Ejecutar submódulo
            try:
                result = subprocess.run(
                    ['python', 'main.py'] + args,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minutos timeout
                )
                
                if result.returncode == 0:
                    return ModuleResult.success_result(
                        data=result.stdout.strip(),
                        message=f"Submódulo {submodule_path} ejecutado exitosamente"
                    )
                else:
                    return ModuleResult.error_result(
                        f"Error ejecutando submódulo: {result.stderr.strip()}"
                    )
                    
            except subprocess.TimeoutExpired:
                return ModuleResult.error_result(
                    f"Timeout ejecutando submódulo {submodule_path}"
                )
            except Exception as e:
                return ModuleResult.error_result(
                    f"Error ejecutando submódulo: {str(e)}"
                )
                
        except Exception as e:
            return ModuleResult.error_result(
                f"Error en orquestador ejecutando submódulo: {str(e)}"
            )
    
    def get_available_modules(self) -> List[str]:
        """
        Obtener lista de módulos disponibles.
        
        Returns:
            Lista de nombres de módulos cargados
        """
        return list(self._loaded_modules.keys())
    
    def get_module_commands(self, module_name: str) -> List[str]:
        """
        Obtener comandos disponibles para un módulo.
        
        Args:
            module_name: Nombre del módulo
            
        Returns:
            Lista de comandos disponibles o vacía si el módulo no existe
        """
        if module_name in self._loaded_modules:
            try:
                return self._loaded_modules[module_name].get_commands()
            except Exception:
                return []
        return []
    
    def reload_modules(self):
        """Recargar todos los módulos"""
        self._loaded_modules.clear()
        self._initialize_modules()
    
    def get_security_manager(self) -> SecurityManager:
        """Obtener instancia del Security Manager"""
        return self._security_manager
    
    def get_core_api(self) -> CoreAPI:
        """Obtener instancia del Core API"""
        return self._core_api
    
    # === Métodos de conveniencia para comandos comunes ===
    
    def execute_task_command(self, command: str, **kwargs) -> ModuleResult:
        """Ejecutar comando de tareas"""
        return self.execute_module_command('tasks', command, **kwargs)
    
    def execute_pomodoro_command(self, command: str, **kwargs) -> ModuleResult:
        """Ejecutar comando de Pomodoro"""
        return self.execute_module_command('pomodoro', command, **kwargs)
    
    def execute_obsidian_command(self, command: str, **kwargs) -> ModuleResult:
        """Ejecutar comando de Obsidian"""
        return self.execute_module_command('obsidian', command, **kwargs)
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Obtener estado general del sistema.
        
        Returns:
            Dict con información del sistema
        """
        try:
            # Información de módulos
            modules_info = {}
            for name, module in self._loaded_modules.items():
                try:
                    modules_info[name] = {
                        'commands': module.get_commands(),
                        'loaded': True
                    }
                except Exception:
                    modules_info[name] = {
                        'commands': [],
                        'loaded': False,
                        'error': True
                    }
            
            # Información de seguridad
            trusted_submodules = self._security_manager.list_trusted_submodules()
            
            # Información de base de datos
            db_info = self._core_api._db_manager.get_database_info()
            
            return {
                'modules': modules_info,
                'security': trusted_submodules,
                'database': db_info,
                'status': 'healthy'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'modules': {},
                'security': {},
                'database': {}
            }
    
    def validate_system(self) -> Dict[str, Any]:
        """
        Validar integridad del sistema.
        
        Returns:
            Dict con resultado de validación
        """
        issues = []
        warnings = []
        
        # Validar módulos
        for name, module in self._loaded_modules.items():
            try:
                commands = module.get_commands()
                if not commands:
                    warnings.append(f"Módulo '{name}' no tiene comandos disponibles")
            except Exception as e:
                issues.append(f"Error en módulo '{name}': {str(e)}")
        
        # Validar base de datos
        try:
            db_integrity = self._core_api._db_manager.check_integrity()
            if not db_integrity['integrity_ok']:
                issues.append("Problemas de integridad en la base de datos")
        except Exception as e:
            issues.append(f"Error verificando base de datos: {str(e)}")
        
        # Validar configuración
        try:
            config_validation = self._core_api._config_manager.validate_config()
            if not config_validation['valid']:
                issues.extend(config_validation['issues'])
            warnings.extend(config_validation['warnings'])
        except Exception as e:
            issues.append(f"Error validando configuración: {str(e)}")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'summary': f"{'Sistema válido' if len(issues) == 0 else f'{len(issues)} problemas encontrados'}"
        }
