"""
Configuración de la aplicación
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Gestor de configuración de la CLI"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".cli-productividad"
        self.config_file = self.config_dir / "config.yaml"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Cargar configuración desde archivo o crear defaults"""
        default_config = {
            "obsidian": {
                "vault_path": "",
                "notes_folder": "CLI-Notes"
            },
            "database": {
                "path": str(self.config_dir / "data.db")
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
            }
        }
        
        # Crear directorio si no existe
        self.config_dir.mkdir(exist_ok=True)
        
        # Cargar configuración existente o crear default
        if self.config_file.exists():
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
            config = self.config
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        
        self.config = config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtener valor de configuración con notación de puntos"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Establecer valor de configuración con notación de puntos"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save_config()
    
    def detect_obsidian_vault(self) -> Optional[str]:
        """Detectar automáticamente vault de Obsidian"""
        # Buscar en ubicaciones comunes
        possible_paths = [
            Path.home() / "Documents" / "Obsidian",
            Path.home() / "Obsidian",
            Path.home() / "Dropbox" / "Obsidian",
            Path.home() / "OneDrive" / "Obsidian",
        ]
        
        for path in possible_paths:
            if path.exists() and path.is_dir():
                # Buscar archivos .obsidian
                for item in path.iterdir():
                    if item.name == ".obsidian" and item.is_dir():
                        return str(path)
        
        return None


# Instancia global de configuración
config = Config()
