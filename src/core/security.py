"""
Security Manager - Core Layer

This module handles security verification for external submodules,
implementing the hash-based verification protocol defined in the architecture.
"""

import os
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Dict, Optional, Set
from datetime import datetime


class SecurityManager:
    """
    Gestor de seguridad para submódulos externos.
    
    Implementa el protocolo de verificación por hash para garantizar
    que solo se ejecuten submódulos confiables.
    """
    
    def __init__(self, manifest_path: str = None):
        if manifest_path is None:
            # Usar directorio de configuración de la CLI
            config_dir = Path.home() / ".cli-productividad"
            config_dir.mkdir(exist_ok=True)
            manifest_path = str(config_dir / "trusted_submodules.json")
        
        self.manifest_path = manifest_path
        self._trusted_hashes = self._load_manifest()
    
    def _load_manifest(self) -> Dict[str, Dict]:
        """Cargar manifest de submódulos confiables"""
        try:
            if os.path.exists(self.manifest_path):
                with open(self.manifest_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Crear manifest vacío
                self._save_manifest({})
                return {}
        except Exception:
            return {}
    
    def _save_manifest(self, manifest: Dict = None):
        """Guardar manifest de submódulos confiables"""
        if manifest is None:
            manifest = self._trusted_hashes
        
        try:
            with open(self.manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            self._trusted_hashes = manifest
        except Exception as e:
            raise Exception(f"No se pudo guardar el manifest: {str(e)}")
    
    def _compute_file_hash(self, file_path: str) -> str:
        """Calcular hash SHA256 de un archivo"""
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                # Leer archivo en chunks para manejar archivos grandes
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except Exception as e:
            raise Exception(f"No se pudo calcular hash de {file_path}: {str(e)}")
    
    def verify_submodule(self, module_path: str) -> Dict[str, any]:
        """
        Verificar si un submódulo es confiable.
        
        Args:
            module_path: Ruta al archivo del submódulo
            
        Returns:
            Dict con resultado de verificación:
            {
                'trusted': bool,
                'hash': str,
                'registered': bool,
                'message': str
            }
        """
        try:
            path = Path(module_path)
            
            # Verificar que el archivo existe
            if not path.exists():
                return {
                    'trusted': False,
                    'hash': '',
                    'registered': False,
                    'message': f"El archivo {module_path} no existe"
                }
            
            # Verificar que es un archivo ejecutable (.sh)
            if path.suffix != '.sh':
                return {
                    'trusted': False,
                    'hash': '',
                    'registered': False,
                    'message': f"El archivo {module_path} no es un submódulo .sh válido"
                }
            
            # Calcular hash actual
            current_hash = self._compute_file_hash(module_path)
            relative_path = str(path.relative_to(Path.cwd()))
            
            # Verificar si está registrado
            if relative_path not in self._trusted_hashes:
                return {
                    'trusted': False,
                    'hash': current_hash,
                    'registered': False,
                    'message': f"Submódulo {relative_path} no está registrado"
                }
            
            # Verificar si el hash coincide
            trusted_info = self._trusted_hashes[relative_path]
            if trusted_info['hash'] != current_hash:
                return {
                    'trusted': False,
                    'hash': current_hash,
                    'registered': True,
                    'message': f"Hash de {relative_path} no coincide. Posible modificación no autorizada"
                }
            
            return {
                'trusted': True,
                'hash': current_hash,
                'registered': True,
                'message': f"Submódulo {relative_path} verificado correctamente"
            }
            
        except Exception as e:
            return {
                'trusted': False,
                'hash': '',
                'registered': False,
                'message': f"Error verificando submódulo: {str(e)}"
            }
    
    def register_submodule(self, module_path: str, description: str = "") -> Dict[str, any]:
        """
        Registrar un submódulo como confiable.
        
        Args:
            module_path: Ruta al archivo del submódulo
            description: Descripción opcional del submódulo
            
        Returns:
            Dict con resultado del registro
        """
        try:
            path = Path(module_path)
            
            if not path.exists():
                return {
                    'success': False,
                    'message': f"El archivo {module_path} no existe"
                }
            
            if path.suffix != '.sh':
                return {
                    'success': False,
                    'message': f"El archivo {module_path} no es un submódulo .sh válido"
                }
            
            # Calcular hash
            file_hash = self._compute_file_hash(module_path)
            relative_path = str(path.relative_to(Path.cwd()))
            
            # Registrar en manifest
            self._trusted_hashes[relative_path] = {
                'hash': file_hash,
                'description': description,
                'registered_at': datetime.now().isoformat(),
                'size': path.stat().st_size
            }
            
            self._save_manifest()
            
            return {
                'success': True,
                'message': f"Submódulo {relative_path} registrado exitosamente",
                'hash': file_hash
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f"Error registrando submódulo: {str(e)}"
            }
    
    def revoke_permissions(self, module_path: str) -> Dict[str, any]:
        """
        Revocar permisos de ejecución de un submódulo no confiable.
        
        Args:
            module_path: Ruta al archivo del submódulo
            
        Returns:
            Dict con resultado de la revocación
        """
        try:
            path = Path(module_path)
            
            if not path.exists():
                return {
                    'success': False,
                    'message': f"El archivo {module_path} no existe"
                }
            
            # Revocar permisos de ejecución (chmod 000)
            subprocess.run(['chmod', '000', str(path)], check=True)
            
            return {
                'success': True,
                'message': f"Permisos revocados para {module_path}"
            }
            
        except subprocess.CalledProcessError as e:
            return {
                'success': False,
                'message': f"No se pudieron revocar permisos: {str(e)}"
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Error revocando permisos: {str(e)}"
            }
    
    def list_trusted_submodules(self) -> Dict[str, any]:
        """
        Listar todos los submódulos confiables registrados.
        
        Returns:
            Dict con lista de submódulos confiables
        """
        try:
            return {
                'success': True,
                'submodules': self._trusted_hashes,
                'count': len(self._trusted_hashes)
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Error listando submódulos: {str(e)}",
                'submodules': {},
                'count': 0
            }
    
    def remove_submodule(self, module_path: str) -> Dict[str, any]:
        """
        Eliminar un submódulo del registro de confiables.
        
        Args:
            module_path: Ruta al archivo del submódulo
            
        Returns:
            Dict con resultado de la eliminación
        """
        try:
            path = Path(module_path)
            relative_path = str(path.relative_to(Path.cwd()))
            
            if relative_path in self._trusted_hashes:
                del self._trusted_hashes[relative_path]
                self._save_manifest()
                
                return {
                    'success': True,
                    'message': f"Submódulo {relative_path} eliminado del registro"
                }
            else:
                return {
                    'success': False,
                    'message': f"Submódulo {relative_path} no estaba registrado"
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f"Error eliminando submódulo: {str(e)}"
            }
    
    def scan_submodules_directory(self, directory_path: str = "src/submodules") -> Dict[str, any]:
        """
        Escanear directorio de submódulos en busca de archivos no registrados.
        
        Args:
            directory_path: Ruta al directorio de submódulos
            
        Returns:
            Dict con resultados del escaneo
        """
        try:
            submodules_dir = Path(directory_path)
            
            if not submodules_dir.exists():
                return {
                    'success': False,
                    'message': f"Directorio {directory_path} no existe"
                }
            
            # Encontrar todos los archivos .sh
            sh_files = list(submodules_dir.glob("**/*.sh"))
            
            unregistered = []
            modified = []
            trusted = []
            
            for sh_file in sh_files:
                verification = self.verify_submodule(str(sh_file))
                
                if not verification['registered']:
                    unregistered.append({
                        'path': str(sh_file),
                        'hash': verification['hash']
                    })
                elif not verification['trusted']:
                    modified.append({
                        'path': str(sh_file),
                        'current_hash': verification['hash'],
                        'trusted_hash': self._trusted_hashes.get(str(sh_file.relative_to(Path.cwd())), {}).get('hash', '')
                    })
                else:
                    trusted.append(str(sh_file))
            
            return {
                'success': True,
                'total_found': len(sh_files),
                'trusted': trusted,
                'unregistered': unregistered,
                'modified': modified,
                'message': f"Escaneo completado: {len(trusted)} confiables, {len(unregistered)} no registrados, {len(modified)} modificados"
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f"Error escaneando directorio: {str(e)}",
                'total_found': 0,
                'trusted': [],
                'unregistered': [],
                'modified': []
            }
