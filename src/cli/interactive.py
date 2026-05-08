"""
Menú interactivo con Rich
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.layout import Layout
from rich.text import Text
from typing import Optional

from src.modules.tasks.manager import TaskManager
from src.modules.pomodoro.timer import PomodoroTimer
from src.modules.obsidian.vault import ObsidianVault

console = Console()


class InteractiveMenu:
    """Menú interactivo principal de la CLI"""
    
    def __init__(self):
        self.task_manager = TaskManager()
        self.pomodoro_timer = PomodoroTimer()
        self.obsidian_vault = ObsidianVault()
    
    def run(self):
        """Ejecutar el menú interactivo"""
        while True:
            self._show_main_menu()
            choice = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5", "0"], default="0")
            
            if choice == "1":
                self._tasks_menu()
            elif choice == "2":
                self._pomodoro_menu()
            elif choice == "3":
                self._notes_menu()
            elif choice == "4":
                self._stats_menu()
            elif choice == "5":
                self._config_menu()
            elif choice == "0":
                console.print("👋 ¡Hasta luego!", style="bold green")
                break
    
    def _show_main_menu(self):
        """Mostrar menú principal"""
        menu_text = """
[1] 📋 Gestión de Tareas
[2] 🍅 Pomodoro Timer  
[3] 📓 Notas Obsidian
[4] 📊 Estadísticas
[5] ⚙️  Configuración
[0] 🚪 Salir
        """
        
        console.print(Panel.fit(
            Text.from_markup(menu_text, justify="center"),
            title="🧠 CLI Productividad TDAD",
            border_style="bright_blue",
            padding=(1, 2)
        ))
    
    def _tasks_menu(self):
        """Menú de gestión de tareas"""
        while True:
            self._show_tasks_menu()
            choice = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5", "6", "0"], default="0")
            
            if choice == "1":
                self._add_task_interactive()
            elif choice == "2":
                self._list_tasks_interactive()
            elif choice == "3":
                self._complete_task_interactive()
            elif choice == "4":
                self._delete_task_interactive()
            elif choice == "5":
                self._search_tasks_interactive()
            elif choice == "6":
                self._task_stats_interactive()
            elif choice == "0":
                break
    
    def _show_tasks_menu(self):
        """Mostrar menú de tareas"""
        # Obtener estadísticas rápidas
        stats = self.task_manager.get_task_stats()
        
        menu_text = f"""
[1] ➕ Agregar Tarea
[2] 📝 Listar Tareas
[3] ✅ Completar Tarea  
[4] 🗑️  Eliminar Tarea
[5] 🔍 Buscar Tareas
[6] 📊 Estadísticas
[0] ⬅️  Volver

📈 Resumen: {stats['pending']} pendientes, {stats['completed']} completadas
        """
        
        console.print(Panel.fit(
            Text.from_markup(menu_text, justify="center"),
            title="📋 Gestión de Tareas",
            border_style="green"
        ))
    
    def _add_task_interactive(self):
        """Agregar tarea interactiva"""
        console.print("\n➕ [bold green]Agregar Nueva Tarea[/bold green]")
        
        title = Prompt.ask("Título de la tarea")
        if not title.strip():
            console.print("❌ El título no puede estar vacío")
            return
        
        description = Prompt.ask("Descripción (opcional)", default="")
        priority = Prompt.ask("Prioridad", choices=["high", "medium", "low"], default="medium")
        
        task = self.task_manager.create_task(title, description, priority)
        
        console.print(f"\n✅ Tarea creada exitosamente!")
        console.print(f"   📝 {task.title}")
        console.print(f"   🎯 Prioridad: {task.priority}")
        console.print(f"   🆔 ID: {task.id}")
        
        if description:
            console.print(f"   📄 Descripción: {description}")
    
    def _list_tasks_interactive(self):
        """Listar tareas interactivamente"""
        # Opciones de filtrado
        console.print("\n📝 [bold green]Listar Tareas[/bold green]")
        
        filter_by = Prompt.ask(
            "Filtrar por", 
            choices=["all", "pending", "completed", "high"], 
            default="pending"
        )
        
        if filter_by == "all":
            tasks = self.task_manager.list_tasks()
        elif filter_by == "pending":
            tasks = self.task_manager.get_pending_tasks()
        elif filter_by == "completed":
            tasks = self.task_manager.get_completed_tasks()
        elif filter_by == "high":
            tasks = self.task_manager.get_high_priority_tasks()
        
        if not tasks:
            console.print("📝 No hay tareas para mostrar")
            return
        
        table = Table(title=f"📋 Tareas ({filter_by})")
        table.add_column("ID", style="cyan", width=6)
        table.add_column("Título", style="white", min_width=30)
        table.add_column("Prioridad", style="yellow", width=10)
        table.add_column("Estado", style="green", width=12)
        table.add_column("Creada", style="blue", width=12)
        
        for task in tasks:
            priority_color = {"high": "red", "medium": "yellow", "low": "green"}[task.priority]
            status_color = {"pending": "yellow", "completed": "green", "cancelled": "red"}[task.status]
            
            table.add_row(
                str(task.id),
                task.title,
                f"[{priority_color}]{task.priority}[/{priority_color}]",
                f"[{status_color}]{task.status}[/{status_color}]",
                task.created_at.strftime("%d/%m %H:%M")
            )
        
        console.print(table)
        console.print(f"\nTotal: {len(tasks)} tareas")
    
    def _complete_task_interactive(self):
        """Completar tarea interactivamente"""
        console.print("\n✅ [bold green]Completar Tarea[/bold green]")
        
        task_id = IntPrompt.ask("ID de la tarea a completar")
        
        success = self.task_manager.complete_task(task_id)
        
        if success:
            console.print(f"✅ Tarea {task_id} marcada como completada")
        else:
            console.print(f"❌ No se encontró la tarea {task_id}")
    
    def _delete_task_interactive(self):
        """Eliminar tarea interactivamente"""
        console.print("\n🗑️  [bold red]Eliminar Tarea[/bold red]")
        
        task_id = IntPrompt.ask("ID de la tarea a eliminar")
        
        # Confirmar
        if not Confirm.ask(f"¿Estás seguro de eliminar la tarea {task_id}?"):
            console.print("❌ Operación cancelada")
            return
        
        success = self.task_manager.delete_task(task_id)
        
        if success:
            console.print(f"🗑️  Tarea {task_id} eliminada")
        else:
            console.print(f"❌ No se encontró la tarea {task_id}")
    
    def _search_tasks_interactive(self):
        """Buscar tareas interactivamente"""
        console.print("\n🔍 [bold green]Buscar Tareas[/bold green]")
        
        query = Prompt.ask("Término de búsqueda")
        
        tasks = self.task_manager.list_tasks()
        results = [t for t in tasks if query.lower() in t.title.lower() or 
                   (t.description and query.lower() in t.description.lower())]
        
        if not results:
            console.print(f"🔍 No se encontraron tareas con: '{query}'")
            return
        
        console.print(f"\n🔍 Se encontraron {len(results)} tareas:")
        
        for task in results:
            console.print(f"  🆔 {task.id}: {task.title}")
            if task.description:
                console.print(f"     📄 {task.description}")
    
    def _task_stats_interactive(self):
        """Mostrar estadísticas de tareas"""
        stats = self.task_manager.get_task_stats()
        
        stats_text = f"""
📊 Estadísticas de Tareas

📈 Total de tareas: {stats['total']}
⏳ Pendientes: {stats['pending']}
✅ Completadas: {stats['completed']}
❌ Canceladas: {stats['cancelled']}
🔥 Alta prioridad pendientes: {stats['high_priority']}
📈 Tasa de completado: {stats['completion_rate']:.1f}%
        """
        
        console.print(Panel.fit(
            Text.from_markup(stats_text),
            title="📊 Estadísticas",
            border_style="blue"
        ))
    
    def _pomodoro_menu(self):
        """Menú de Pomodoro"""
        while True:
            self._show_pomodoro_menu()
            choice = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5", "0"], default="0")
            
            if choice == "1":
                self._start_pomodoro_interactive()
            elif choice == "2":
                self._start_break_interactive()
            elif choice == "3":
                self._pomodoro_status_interactive()
            elif choice == "4":
                self._stop_pomodoro_interactive()
            elif choice == "5":
                self._pomodoro_history_interactive()
            elif choice == "0":
                break
    
    def _show_pomodoro_menu(self):
        """Mostrar menú Pomodoro"""
        status = self.pomodoro_timer.get_status()
        
        if status["is_active"]:
            status_text = f"⏱️  Activo: {status['session_type']} - {status['remaining_seconds']//60}:{status['remaining_seconds']%60:02d}"
        else:
            status_text = "🍅 Inactivo"
        
        menu_text = f"""
[1] 🍅 Iniciar Pomodoro
[2] ☕ Iniciar Descanso  
[3] ⏱️  Ver Estado
[4] ⏹️  Detener Sesión
[5] 📜 Historial
[0] ⬅️  Volver

{status_text}
        """
        
        console.print(Panel.fit(
            Text.from_markup(menu_text, justify="center"),
            title="🍅 Pomodoro Timer",
            border_style="red"
        ))
    
    def _start_pomodoro_interactive(self):
        """Iniciar Pomodoro interactivo"""
        console.print("\n🍅 [bold green]Iniciar Pomodoro[/bold green]")
        
        duration = IntPrompt.ask("Duración en minutos", default=25)
        
        # Opcional: asociar a tarea
        associate_task = Confirm.ask("¿Asociar a una tarea existente?", default=False)
        task_id = None
        
        if associate_task:
            task_id = IntPrompt.ask("ID de la tarea")
        
        self.pomodoro_timer.start_session(duration, "work", task_id)
        console.print(f"🍅 Pomodoro de {duration} minutos iniciado")
    
    def _start_break_interactive(self):
        """Iniciar descanso interactivo"""
        console.print("\n☕ [bold green]Iniciar Descanso[/bold green]")
        
        duration = IntPrompt.ask("Duración en minutos", default=5)
        
        self.pomodoro_timer.start_session(duration, "break")
        console.print(f"☕ Descanso de {duration} minutos iniciado")
    
    def _pomodoro_status_interactive(self):
        """Mostrar estado Pomodoro"""
        status = self.pomodoro_timer.get_status()
        
        if status["is_active"]:
            remaining = status["remaining_seconds"]
            minutes, seconds = divmod(remaining, 60)
            
            status_text = f"""
⏱️  [bold green]Sesión Activa[/bold green]

🍅 Tipo: {status['session_type']}
⏰ Tiempo restante: {minutes:02d}:{seconds:02d}
🕐 Iniciado: {status['started_at']}
            """
            
            if status["task_id"]:
                status_text += f"\n🎯 Tarea asociada: {status['task_id']}"
        else:
            status_text = """
🍅 [bold yellow]Sin Sesión Activa[/bold yellow]

No hay ninguna sesión Pomodoro en curso.
            """
        
        console.print(Panel.fit(
            Text.from_markup(status_text),
            title="🍅 Estado Pomodoro",
            border_style="red"
        ))
    
    def _stop_pomodoro_interactive(self):
        """Detener Pomodoro"""
        if Confirm.ask("¿Detener sesión actual?"):
            self.pomodoro_timer.stop_session()
    
    def _pomodoro_history_interactive(self):
        """Mostrar historial Pomodoro"""
        history = self.pomodoro_timer.get_session_history()
        
        if not history:
            console.print("📜 No hay sesiones anteriores")
            return
        
        table = Table(title="📜 Historial de Sesiones")
        table.add_column("ID", style="cyan", width=6)
        table.add_column("Tipo", style="white", width=12)
        table.add_column("Duración", style="yellow", width=10)
        table.add_column("Completada", style="green", width=10)
        table.add_column("Fecha", style="blue", width=16)
        
        for session in history:
            completed = "✅" if session["was_completed"] else "❌"
            started = session["started_at"][:19] if session["started_at"] else "N/A"
            
            table.add_row(
                str(session["id"]),
                session["session_type"],
                f"{session['duration']} min",
                completed,
                started
            )
        
        console.print(table)
    
    def _notes_menu(self):
        """Menú de notas"""
        while True:
            self._show_notes_menu()
            choice = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "5", "0"], default="0")
            
            if choice == "1":
                self._create_note_interactive()
            elif choice == "2":
                self._list_notes_interactive()
            elif choice == "3":
                self._search_notes_interactive()
            elif choice == "4":
                self._view_note_interactive()
            elif choice == "5":
                self._delete_note_interactive()
            elif choice == "0":
                break
    
    def _show_notes_menu(self):
        """Mostrar menú de notas"""
        if not self.obsidian_vault.is_configured():
            status = "❌ No configurado"
        else:
            notes_count = len(self.obsidian_vault.list_notes())
            status = f"✅ {notes_count} notas"
        
        menu_text = f"""
[1] ➕ Crear Nota
[2] 📝 Listar Notas
[3] 🔍 Buscar Notas
[4] 👁️  Ver Nota
[5] 🗑️  Eliminar Nota
[0] ⬅️  Volver

Estado: {status}
        """
        
        console.print(Panel.fit(
            Text.from_markup(menu_text, justify="center"),
            title="📓 Notas Obsidian",
            border_style="purple"
        ))
    
    def _create_note_interactive(self):
        """Crear nota interactiva"""
        if not self.obsidian_vault.is_configured():
            console.print("❌ Obsidian no está configurado")
            return
        
        console.print("\n➕ [bold green]Crear Nueva Nota[/bold green]")
        
        title = Prompt.ask("Título de la nota")
        if not title.strip():
            console.print("❌ El título no puede estar vacío")
            return
        
        content = Prompt.ask("Contenido (opcional)", default="")
        
        # Tags
        add_tags = Confirm.ask("¿Agregar tags?", default=False)
        tags = []
        
        if add_tags:
            while True:
                tag = Prompt.ask("Tag (dejar vacío para terminar)", default="")
                if not tag.strip():
                    break
                tags.append(tag.strip())
        
        try:
            note_path = self.obsidian_vault.create_note(title, content, tags)
            console.print(f"✅ Nota creada: {note_path}")
            
            if tags:
                console.print(f"   🏷️  Tags: {', '.join(tags)}")
        except Exception as e:
            console.print(f"❌ Error al crear nota: {e}")
    
    def _list_notes_interactive(self):
        """Listar notas interactivamente"""
        if not self.obsidian_vault.is_configured():
            console.print("❌ Obsidian no está configurado")
            return
        
        filter_tag = Prompt.ask("Filtrar por tag (dejar vacío para todas)", default="")
        
        notes = self.obsidian_vault.list_notes(filter_tag if filter_tag else None)
        
        if not notes:
            console.print("📝 No hay notas para mostrar")
            return
        
        table = Table(title=f"📓 Notas {'- ' + filter_tag if filter_tag else ''}")
        table.add_column("ID", style="cyan", width=6)
        table.add_column("Título", style="white", min_width=25)
        table.add_column("Tags", style="yellow", width=15)
        table.add_column("Actualizada", style="blue", width=12)
        
        for note in notes:
            tags_str = note.get('tags', 'N/A')
            if isinstance(tags_str, list):
                tags_str = ', '.join(tags_str) if tags_str else 'Sin tags'
            
            updated = note.get('updated_at')
            if updated and hasattr(updated, 'strftime'):
                updated_str = updated.strftime("%d/%m %H:%M")
            else:
                updated_str = 'N/A'
            
            table.add_row(
                str(note['id']),
                note['title'],
                tags_str,
                updated_str
            )
        
        console.print(table)
    
    def _search_notes_interactive(self):
        """Buscar notas interactivamente"""
        if not self.obsidian_vault.is_configured():
            console.print("❌ Obsidian no está configurado")
            return
        
        query = Prompt.ask("Término de búsqueda")
        
        results = self.obsidian_vault.search_notes(query)
        
        if not results:
            console.print(f"🔍 No se encontraron notas para: '{query}'")
            return
        
        console.print(f"\n🔍 Se encontraron {len(results)} notas:")
        
        for note in results:
            console.print(f"  📄 {note['title']} - {note['path']}")
    
    def _view_note_interactive(self):
        """Ver contenido de nota"""
        if not self.obsidian_vault.is_configured():
            console.print("❌ Obsidian no está configurado")
            return
        
        path = Prompt.ask("Ruta de la nota (ej: CLI-Notes/mi-nota.md)")
        
        content = self.obsidian_vault.get_note_content(path)
        
        if content:
            console.print(f"\n📄 [bold green]Contenido de {path}[/bold green]")
            console.print(Panel(content, title=path, border_style="blue"))
        else:
            console.print(f"❌ No se encontró la nota: {path}")
    
    def _delete_note_interactive(self):
        """Eliminar nota interactivamente"""
        if not self.obsidian_vault.is_configured():
            console.print("❌ Obsidian no está configurado")
            return
        
        path = Prompt.ask("Ruta de la nota a eliminar")
        
        if Confirm.ask(f"¿Eliminar la nota '{path}'?"):
            success = self.obsidian_vault.delete_note(path)
            
            if success:
                console.print(f"🗑️  Nota eliminada: {path}")
            else:
                console.print(f"❌ No se pudo eliminar la nota: {path}")
    
    def _stats_menu(self):
        """Menú de estadísticas"""
        console.print("\n📊 [bold green]Estadísticas Generales[/bold green]")
        
        # Estadísticas de tareas
        task_stats = self.task_manager.get_task_stats()
        pomodoro_stats = self.pomodoro_timer.get_today_stats()
        
        stats_text = f"""
📊 [bold blue]Estadísticas de Hoy[/bold blue]

📋 Tareas:
   • Total: {task_stats['total']}
   • Pendientes: {task_stats['pending']}
   • Completadas: {task_stats['completed']}
   • Tasa de completado: {task_stats['completion_rate']:.1f}%

🍅 Pomodoro:
   • Sesiones totales: {pomodoro_stats['total_sessions']}
   • Sesiones de trabajo: {pomodoro_stats['work_sessions']}
   • Completadas: {pomodoro_stats['completed_work_sessions']}
   • Minutos de trabajo: {pomodoro_stats['total_work_minutes']}
   • Tasa de completado: {pomodoro_stats['completion_rate']:.1f}%

📓 Notas:
   • Total: {len(self.obsidian_vault.list_notes())}
        """
        
        console.print(Panel.fit(
            Text.from_markup(stats_text),
            title="📊 Estadísticas",
            border_style="blue"
        ))
        
        Prompt.ask("Presione Enter para continuar", default="")
    
    def _config_menu(self):
        """Menú de configuración"""
        while True:
            self._show_config_menu()
            choice = Prompt.ask("Seleccione una opción", choices=["1", "2", "3", "4", "0"], default="0")
            
            if choice == "1":
                self._show_config_interactive()
            elif choice == "2":
                self._set_config_interactive()
            elif choice == "3":
                self._detect_obsidian_interactive()
            elif choice == "4":
                self._reset_config_interactive()
            elif choice == "0":
                break
    
    def _show_config_menu(self):
        """Mostrar menú de configuración"""
        menu_text = """
[1] 📋 Ver Configuración
[2] ⚙️  Establecer Configuración
[3] 🔍 Detectar Obsidian
[4] 🔄 Resetear Configuración
[0] ⬅️  Volver
        """
        
        console.print(Panel.fit(
            Text.from_markup(menu_text, justify="center"),
            title="⚙️ Configuración",
            border_style="yellow"
        ))
    
    def _show_config_interactive(self):
        """Mostrar configuración actual"""
        from src.core.config import config
        import yaml
        
        console.print("\n📋 [bold green]Configuración Actual[/bold green]")
        console.print(yaml.dump(config.config, default_flow_style=False, allow_unicode=True))
    
    def _set_config_interactive(self):
        """Establecer configuración"""
        key = Prompt.ask("Clave de configuración (ej: pomodoro.work_duration)")
        value = Prompt.ask("Valor")
        
        from src.core.config import config
        
        # Intentar convertir a tipo apropiado
        if value.lower() in ['true', 'false']:
            value = value.lower() == 'true'
        elif value.isdigit():
            value = int(value)
        
        config.set(key, value)
        console.print(f"✅ Configuración actualizada: {key} = {value}")
    
    def _detect_obsidian_interactive(self):
        """Detectar vault de Obsidian"""
        from src.core.config import config
        
        vault_path = config.detect_obsidian_vault()
        
        if vault_path:
            config.set('obsidian.vault_path', vault_path)
            console.print(f"✅ Vault detectado: {vault_path}")
        else:
            console.print("❌ No se detectó ningún vault")
    
    def _reset_config_interactive(self):
        """Resetear configuración"""
        if Confirm.ask("¿Estás seguro de resetear toda la configuración?"):
            from src.core.config import config
            
            # Eliminar archivo de configuración
            if config.config_file.exists():
                config.config_file.unlink()
            
            # Recargar configuración default
            config.config = config._load_config()
            
            console.print("✅ Configuración reseteada a valores por defecto")
