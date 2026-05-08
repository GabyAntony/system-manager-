"""
Obsidian Module - New API Pattern

This module implements BaseModuleAPI interface for Obsidian vault management,
communicating with core through controlled API bridge.
"""

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
from ...api.base import BaseModuleAPI, ModuleResult


class ObsidianModule(BaseModuleAPI):
    """
    Módulo de gestión Obsidian implementando BaseModuleAPI.
    
    Se comunica con el core a través del CoreAPI y contiene
    la lógica de detección de vaults que estaba en el core.
    """
    
    def __init__(self):
        self._core_api = None
    
    def set_core_api(self, core_api):
        """Inyectar instancia de CoreAPI"""
        self._core_api = core_api
    
    def execute(self, command: str, **kwargs) -> ModuleResult:
        """
        Ejecutar comando de Obsidian.
        
        Args:
            command: Comando a ejecutar
            **kwargs: Parámetros del comando
            
        Returns:
            ModuleResult con el resultado
        """
        if self._core_api is None:
            return ModuleResult.error_result("CoreAPI no inicializado")
        
        if command == "detect_vault":
            return self._detect_vault(**kwargs)
        elif command == "set_vault":
            return self._set_vault(**kwargs)
        elif command == "get_vault":
            return self._get_vault(**kwargs)
        elif command == "index_notes":
            return self._index_notes(**kwargs)
        elif command == "search_notes":
            return self._search_notes(**kwargs)
        elif command == "create_note":
            return self._create_note(**kwargs)
        elif command == "list_notes":
            return self._list_notes(**kwargs)
        elif command == "get_note":
            return self._get_note(**kwargs)
        else:
            return ModuleResult.error_result(f"Comando '{command}' no reconocido")
    
    def get_commands(self) -> List[str]:
        """Retornar lista de comandos disponibles"""
        return [
            "detect_vault", "set_vault", "get_vault", 
            "index_notes", "search_notes", "create_note", 
            "list_notes", "get_note"
        ]
    
    def _detect_vault(self, **kwargs) -> ModuleResult:
        """Detectar automáticamente vault de Obsidian"""
        possible_paths = [
            Path.home() / "Documents" / "Obsidian",
            Path.home() / "Obsidian",
            Path.home() / "Dropbox" / "Obsidian",
            Path.home() / "OneDrive" / "Obsidian",
        ]
        
        found_vaults = []
        
        for path in possible_paths:
            if path.exists() and path.is_dir():
                # Buscar archivos .obsidian
                for item in path.iterdir():
                    if item.name == ".obsidian" and item.is_dir():
                        found_vaults.append({
                            'path': str(path),
                            'name': path.name,
                            'is_default': False
                        })
                        break
        
        if not found_vaults:
            return ModuleResult.success_result(
                data={'vaults': []},
                message="No se encontraron vaults de Obsidian"
            )
        
        # Marcar el primero como default
        found_vaults[0]['is_default'] = True
        
        return ModuleResult.success_result(
            data={'vaults': found_vaults},
            message=f"Se encontraron {len(found_vaults)} vault(s) de Obsidian"
        )
    
    def _set_vault(self, vault_path: str, **kwargs) -> ModuleResult:
        """Establecer ruta del vault de Obsidian"""
        if not vault_path:
            return ModuleResult.error_result("La ruta del vault es requerida")
        
        vault_path_obj = Path(vault_path)
        
        if not vault_path_obj.exists():
            return ModuleResult.error_result(f"La ruta {vault_path} no existe")
        
        if not vault_path_obj.is_dir():
            return ModuleResult.error_result(f"La ruta {vault_path} no es un directorio")
        
        # Verificar que es un vault de Obsidian
        obsidian_dir = vault_path_obj / ".obsidian"
        if not obsidian_dir.exists() or not obsidian_dir.is_dir():
            return ModuleResult.error_result(f"La ruta {vault_path} no parece ser un vault de Obsidian")
        
        # Guardar en configuración
        config_result = self._core_api.set_config("obsidian.vault_path", vault_path)
        
        if not config_result.success:
            return config_result
        
        return ModuleResult.success_result(
            data={'vault_path': vault_path},
            message=f"Vault de Obsidian configurado: {vault_path}"
        )
    
    def _get_vault(self, **kwargs) -> ModuleResult:
        """Obtener configuración actual del vault"""
        config_result = self._core_api.get_config("obsidian.vault_path")
        
        if not config_result.success:
            return config_result
        
        vault_path = config_result.data
        
        if not vault_path:
            return ModuleResult.success_result(
                data={'vault_path': None, 'configured': False},
                message="No hay vault configurado"
            )
        
        vault_path_obj = Path(vault_path)
        
        if not vault_path_obj.exists():
            return ModuleResult.success_result(
                data={'vault_path': vault_path, 'configured': False, 'exists': False},
                message=f"El vault configurado {vault_path} no existe"
            )
        
        return ModuleResult.success_result(
            data={
                'vault_path': vault_path,
                'configured': True,
                'exists': True,
                'name': vault_path_obj.name
            }
        )
    
    def _index_notes(self, force_reindex: bool = False, **kwargs) -> ModuleResult:
        """Indexar notas del vault"""
        vault_result = self._get_vault()
        
        if not vault_result.success:
            return vault_result
        
        vault_data = vault_result.data
        
        if not vault_data.get('configured') or not vault_data.get('exists'):
            return ModuleResult.error_result("No hay un vault válido configurado")
        
        vault_path = Path(vault_data['vault_path'])
        
        # Buscar archivos markdown
        markdown_files = list(vault_path.glob("**/*.md"))
        
        indexed_count = 0
        updated_count = 0
        
        for md_file in markdown_files:
            try:
                # Extraer metadatos básicos
                title = md_file.stem
                
                # Leer primeras líneas para preview
                content_preview = ""
                tags = ""
                
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        
                        # Buscar tags en las primeras líneas
                        for line in lines[:10]:
                            if line.strip().startswith('#'):
                                title = line.strip().lstrip('#').strip()
                            elif '#' in line and not line.strip().startswith('#'):
                                # Extraer tags
                                tag_matches = re.findall(r'#(\w+)', line)
                                if tag_matches:
                                    tags = ','.join(tag_matches)
                            elif len(content_preview) < 200:
                                content_preview += line.strip()
                
                except Exception:
                    # Si no se puede leer el archivo, continuar con datos básicos
                    pass
                
                # Normalizar ruta relativa
                relative_path = str(md_file.relative_to(vault_path))
                
                # Crear o actualizar nota en la base de datos
                note_result = self._core_api.create_note(
                    obsidian_path=relative_path,
                    title=title,
                    content_preview=content_preview[:200],
                    tags=tags
                )
                
                if note_result.success:
                    indexed_count += 1
                    if 'updated' in note_result.message.lower():
                        updated_count += 1
                        
            except Exception:
                # Ignorar archivos que no se puedan procesar
                continue
        
        return ModuleResult.success_result(
            data={
                'indexed_count': indexed_count,
                'updated_count': updated_count,
                'vault_path': str(vault_path)
            },
            message=f"Indexadas {indexed_count} notas ({updated_count} actualizadas)"
        )
    
    def _search_notes(self, query: str, limit: int = 50, **kwargs) -> ModuleResult:
        """Buscar notas en la base de datos"""
        if not query:
            return ModuleResult.error_result("El query de búsqueda es requerido")
        
        # Por ahora, obtener todas las notas y filtrar localmente
        # En el futuro, esto podría usar búsqueda全文 en la base de datos
        notes_result = self._core_api.get_notes(limit=limit)
        
        if not notes_result.success:
            return notes_result
        
        notes = notes_result.data
        query_lower = query.lower()
        
        # Filtrar notas que coincidan con el query
        matching_notes = []
        for note in notes:
            if (query_lower in note.get('title', '').lower() or 
                query_lower in note.get('content_preview', '').lower() or
                query_lower in note.get('tags', '').lower()):
                matching_notes.append(note)
        
        return ModuleResult.success_result(
            data={
                'notes': matching_notes[:limit],
                'query': query,
                'total_found': len(matching_notes),
                'returned': min(len(matching_notes), limit)
            },
            message=f"Se encontraron {len(matching_notes)} notas para '{query}'"
        )
    
    def _create_note(self, title: str, content: str = "", tags: List[str] = None, **kwargs) -> ModuleResult:
        """Crear una nueva nota en el vault"""
        if not title:
            return ModuleResult.error_result("El título es requerido")
        
        vault_result = self._get_vault()
        
        if not vault_result.success:
            return vault_result
        
        vault_data = vault_result.data
        
        if not vault_data.get('configured') or not vault_data.get('exists'):
            return ModuleResult.error_result("No hay un vault válido configurado")
        
        vault_path = Path(vault_data['vault_path'])
        
        # Crear nombre de archivo seguro
        safe_title = re.sub(r'[^\w\s-]', '', title).strip()
        filename = f"{safe_title}.md"
        file_path = vault_path / filename
        
        # Si el archivo ya existe, añadir timestamp
        if file_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_title}_{timestamp}.md"
            file_path = vault_path / filename
        
        # Crear contenido con formato markdown
        tags_str = ""
        if tags:
            tags_str = "\n" + " ".join([f"#{tag}" for tag in tags])
        
        full_content = f"# {title}{tags_str}\n\n{content}"
        
        try:
            # Escribir archivo
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            # Registrar en base de datos
            relative_path = str(file_path.relative_to(vault_path))
            note_result = self._core_api.create_note(
                obsidian_path=relative_path,
                title=title,
                content_preview=content[:200],
                tags=",".join(tags) if tags else ""
            )
            
            if note_result.success:
                return ModuleResult.success_result(
                    data={
                        'file_path': str(file_path),
                        'relative_path': relative_path,
                        'title': title
                    },
                    message=f"Nota '{title}' creada en {filename}"
                )
            else:
                return note_result
                
        except Exception as e:
            return ModuleResult.error_result(f"Error creando nota: {str(e)}")
    
    def _list_notes(self, limit: int = 100, **kwargs) -> ModuleResult:
        """Listar notas indexadas"""
        return self._core_api.get_notes(limit=limit)
    
    def _get_note(self, note_id: int, **kwargs) -> ModuleResult:
        """Obtener detalles de una nota específica"""
        # Por ahora, obtener de la lista de notas
        # En el futuro, esto podría tener un método específico en CoreAPI
        notes_result = self._core_api.get_notes(limit=1000)
        
        if not notes_result.success:
            return notes_result
        
        notes = notes_result.data
        
        for note in notes:
            if note.get('id') == note_id:
                return ModuleResult.success_result(data=note)
        
        return ModuleResult.error_result(f"Nota con ID {note_id} no encontrada")
