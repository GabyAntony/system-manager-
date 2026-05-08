"""
Integración con Obsidian Vault
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any
from ...core import get_db, Note
from ...core.config import config
from ...utilitis.theme import print_success, print_error, print_warning, print_info


class ObsidianVault:
    """Gestor de integración con Obsidian"""
    
    def __init__(self):
        self.db = get_db()
        self.vault_path = config.get('obsidian.vault_path', '')
        self.notes_folder = config.get('obsidian.notes_folder', 'CLI-Notes')
    
    def is_configured(self) -> bool:
        """Verificar si Obsidian está configurado"""
        return bool(self.vault_path) and Path(self.vault_path).exists()
    
    def get_notes_path(self) -> Path:
        """Obtener ruta completa a la carpeta de notas"""
        vault = Path(self.vault_path)
        notes_dir = vault / self.notes_folder
        notes_dir.mkdir(exist_ok=True)
        return notes_dir
    
    def create_note(self, title: str, content: str = "", tags: List[str] = None) -> str:
        """Crear una nueva nota en Obsidian"""
        if not self.is_configured():
            raise ValueError("Obsidian vault no configurado")
        
        # Generar nombre de archivo seguro
        safe_title = self._sanitize_filename(title)
        filename = f"{safe_title}.md"
        
        # Crear contenido con frontmatter
        if tags is None:
            tags = []
        
        frontmatter = {
            "created": datetime.utcnow().isoformat(),
            "tags": tags
        }
        
        # Construir contenido completo
        full_content = self._build_frontmatter(frontmatter) + "\n" + content
        
        # Guardar archivo
        notes_path = self.get_notes_path()
        file_path = notes_path / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        # Guardar en base de datos
        note = Note(
            obsidian_path=str(file_path.relative_to(Path(self.vault_path))),
            title=title,
            content_preview=content[:200] + "..." if len(content) > 200 else content,
            tags=json.dumps(tags)
        )
        
        self.db.add(note)
        self.db.commit()
        
        return str(file_path)
    
    def list_notes(self, tag: str = None) -> List[Dict[str, Any]]:
        """Listar notas de Obsidian"""
        if not self.is_configured():
            return []
        
        notes = self.db.query(Note)
        
        if tag:
            notes = notes.filter(Note.tags.like(f'%"{tag}"%'))
        
        notes = notes.order_by(Note.updated_at.desc()).all()
        
        result = []
        for note in notes:
            note_data = note.to_dict()
            if note.tags:
                try:
                    note_data['tags'] = json.loads(note.tags)
                except:
                    note_data['tags'] = []
            result.append(note_data)
        
        return result
    
    def search_notes(self, query: str) -> List[Dict[str, Any]]:
        """Buscar notas por título o contenido"""
        if not self.is_configured():
            return []
        
        # Buscar en base de datos
        db_results = self.db.query(Note).filter(
            (Note.title.contains(query)) | 
            (Note.content_preview.contains(query))
        ).all()
        
        # También buscar en archivos (más completo)
        file_results = self._search_in_files(query)
        
        # Combinar resultados (evitar duplicados)
        combined_results = []
        seen_paths = set()
        
        for note in db_results:
            note_data = note.to_dict()
            note_data['path'] = note.obsidian_path
            if note_data['path'] not in seen_paths:
                combined_results.append(note_data)
                seen_paths.add(note_data['path'])
        
        for file_result in file_results:
            if file_result['path'] not in seen_paths:
                combined_results.append(file_result)
                seen_paths.add(file_result['path'])
        
        return combined_results
    
    def _search_in_files(self, query: str) -> List[Dict[str, Any]]:
        """Buscar directamente en archivos .md"""
        results = []
        notes_path = self.get_notes_path()
        
        try:
            for file_path in notes_path.glob("*.md"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if query.lower() in content.lower():
                        # Extraer título del contenido o del nombre
                        title = self._extract_title_from_content(content) or file_path.stem
                        
                        results.append({
                            'id': None,  # No está en BD
                            'title': title,
                            'path': str(file_path.relative_to(Path(self.vault_path))),
                            'content_preview': content[:200] + "..." if len(content) > 200 else content
                        })
                except Exception:
                    continue
        except Exception:
            pass
        
        return results
    
    def get_note_content(self, note_path: str) -> Optional[str]:
        """Obtener contenido completo de una nota"""
        if not self.is_configured():
            return None
        
        full_path = Path(self.vault_path) / note_path
        
        if not full_path.exists():
            return None
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return None
    
    def update_note(self, note_path: str, content: str) -> bool:
        """Actualizar contenido de una nota"""
        if not self.is_configured():
            return False
        
        full_path = Path(self.vault_path) / note_path
        
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Actualizar en base de datos
            note = self.db.query(Note).filter(Note.obsidian_path == note_path).first()
            if note:
                note.content_preview = content[:200] + "..." if len(content) > 200 else content
                note.updated_at = datetime.utcnow()
                self.db.commit()
            
            return True
        except Exception:
            return False
    
    def delete_note(self, note_path: str) -> bool:
        """Eliminar una nota"""
        if not self.is_configured():
            return False
        
        full_path = Path(self.vault_path) / note_path
        
        try:
            # Eliminar archivo
            if full_path.exists():
                full_path.unlink()
            
            # Eliminar de base de datos
            note = self.db.query(Note).filter(Note.obsidian_path == note_path).first()
            if note:
                self.db.delete(note)
                self.db.commit()
            
            return True
        except Exception:
            return False
    
    def _sanitize_filename(self, title: str) -> str:
        """Convertir título a nombre de archivo seguro"""
        # Reemplazar caracteres problemáticos
        unsafe_chars = '<>:"/\\|?*'
        safe_title = title
        
        for char in unsafe_chars:
            safe_title = safe_title.replace(char, '_')
        
        # Limitar longitud
        if len(safe_title) > 50:
            safe_title = safe_title[:50]
        
        return safe_title.strip()
    
    def _build_frontmatter(self, metadata: Dict[str, Any]) -> str:
        """Construir frontmatter YAML"""
        lines = ["---"]
        for key, value in metadata.items():
            if isinstance(value, list):
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
            else:
                lines.append(f"{key}: {value}")
        lines.append("---")
        return "\n".join(lines)
    
    def _extract_title_from_content(self, content: str) -> Optional[str]:
        """Extraer título del contenido (frontmatter o primer H1)"""
        lines = content.split('\n')
        
        # Buscar en frontmatter
        in_frontmatter = False
        for line in lines:
            line = line.strip()
            if line == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                else:
                    break
            
            if in_frontmatter and line.startswith("title:"):
                return line.split(":", 1)[1].strip().strip('"\'')
        
        # Buscar primer H1
        for line in lines:
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
        
        return None
