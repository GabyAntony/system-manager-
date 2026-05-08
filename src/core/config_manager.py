"""
Config Manager - Core Layer (Logic Only)

This module provides pure configuration management without business logic.
It handles loading, saving, and accessing configuration values only.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """
    Gestor puro de configuración de la CLI.
    
    Contiene solo lógica de gestión de configuración sin implementaciones
    específicas de negocio (como detección de Obsidian).
    """
    
    def __init__(self, config_file: str = None):
        if config_file is None:
            config_dir = Path.home() / ".cli-productividad"
            config_dir.mkdir(exist_ok=True)
            config_file = str(config_dir / "config.yaml")
        
        self.config_file = config_file
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Cargar configuración desde archivo o crear defaults"""
        default_config = {
            "obsidian": {
                "vault_path": "",
                "notes_folder": "CLI-Notes"
            },
            "database": {
                "path": str(Path.home() / ".cli-productividad" / "data.db")
            },
            "pomodoro": {
                "work_duration": 25,
                "break_duration": 5,
                "long_break_duration": 15,
                "notifications": True
            },
            "ui": {
                "theme": "dark",
                "colors": True,
                "animations": True
            },
            "tasks": {
                "default_priority": "medium",
                "auto_archive_completed": False
            },
            "security": {
                "auto_register_submodules": False,
                "prompt_on_unknown_hash": True
            }
        }
        
        # Cargar configuración existente o crear default
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f) or {}
                # Merge con defaults
                config = {**default_config, **user_config}
                # Asegurar que todas las secciones existan
                for section, defaults in default_config.items():
                    if section not in config:
                        config[section] = defaults
                    else:
                        config[section] = {**defaults, **config[section]}
                return config
            except Exception:
                return default_config
        else:
            # Crear archivo de configuración default
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config: Dict[str, Any] = None):
        """Guardar configuración a archivo"""
        if config is None:
            config = self._config
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        
        self._config = config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtener valor de configuración con notación de puntos"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_all(self) -> Dict[str, Any]:
        """Obtener toda la configuración"""
        return self._config.copy()
    
    def set(self, key: str, value: Any):
        """Establecer valor de configuración con notación de puntos"""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save_config()
    
    def update_section(self, section: str, updates: Dict[str, Any]):
        """Actualizar una sección completa de configuración"""
        if section not in self._config:
            self._config[section] = {}
        
        self._config[section].update(updates)
        self.save_config()
    
    def remove_key(self, key: str):
        """Eliminar una clave de configuración"""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if isinstance(value := config.get(k), dict):
                config = value
            else:
                return  # La clave no existe
        
        if keys[-1] in config:
            del config[keys[-1]]
            self.save_config()
    
    def has_key(self, key: str) -> bool:
        """Verificar si existe una clave de configuración"""
        return self.get(key) is not None
    
    def reload(self):
        """Recargar configuración desde archivo"""
        self._config = self._load_config()
    
    def get_config_file_path(self) -> str:
        """Obtener ruta del archivo de configuración"""
        return self.config_file
    
    def backup_config(self, backup_suffix: str = None) -> str:
        """Crear backup del archivo de configuración"""
        if backup_suffix is None:
            from datetime import datetime
            backup_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        backup_path = f"{self.config_file}.backup_{backup_suffix}"
        
        try:
            import shutil
            shutil.copy2(self.config_file, backup_path)
            return backup_path
        except Exception as e:
            raise Exception(f"No se pudo crear backup: {str(e)}")
    
    def restore_config(self, backup_path: str):
        """Restaurar configuración desde backup"""
        try:
            import shutil
            shutil.copy2(backup_path, self.config_file)
            self.reload()
        except Exception as e:
            raise Exception(f"No se pudo restaurar backup: {str(e)}")
    
    def validate_config(self) -> Dict[str, Any]:
        """Validar estructura y valores de configuración"""
        issues = []
        warnings = []
        
        # Validar secciones requeridas
        required_sections = ["obsidian", "database", "pomodoro", "ui", "tasks"]
        for section in required_sections:
            if section not in self._config:
                issues.append(f"Falta sección requerida: {section}")
        
        # Validar tipos de datos
        type_validations = {
            "pomodoro.work_duration": int,
            "pomodoro.break_duration": int,
            "pomodoro.long_break_duration": int,
            "pomodoro.notifications": bool,
            "ui.colors": bool,
            "ui.animations": bool,
            "tasks.default_priority": str,
            "tasks.auto_archive_completed": bool
        }
        
        for key, expected_type in type_validations.items():
            value = self.get(key)
            if value is not None and not isinstance(value, expected_type):
                issues.append(f"Tipo incorrecto para {key}: se esperaba {expected_type.__name__}")
        
        # Validar valores específicos
        if self.get("tasks.default_priority") not in ["high", "medium", "low"]:
            warnings.append("default_priority debe ser 'high', 'medium' o 'low'")
        
        work_duration = self.get("pomodoro.work_duration")
        if work_duration and (work_duration < 1 or work_duration > 120):
            warnings.append("work_duration debería estar entre 1 y 120 minutos")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }
