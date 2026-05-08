"""
Comandos CLI principales con Click
"""

import click
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from core import get_db, Task, PomodoroSession, Note
from modules.tasks.manager import TaskManager
from modules.pomodoro.timer import PomodoroTimer
from modules.obsidian.vault import ObsidianVault
from utilitis.theme import theme, print_success, print_error, print_warning, print_info, print_primary, print_accent, print_header, print_separator

# CLI Group
@click.group()
@click.version_option(version="1.0.0", prog_name="CLI Productividad")
def cli():
    """CLI Productividad Personal - Optimizada para TDAD"""
    print_header("CLI Productividad", "Sistema Hacker Anime Aesthetic")
    print_separator()


@cli.group()
def task():
    """Gestión de tareas"""
    pass


@task.command()
@click.argument('title')
@click.option('--priority', '-p', default='medium', type=click.Choice(['high', 'medium', 'low']))
@click.option('--description', '-d', default='')
def add(title, priority, description):
    """Agregar una nueva tarea"""
    task_manager = TaskManager()
    task = task_manager.create_task(title, description, priority)
    
    print_success(f"Tarea creada: {task.title} (ID: {task.id})")
    print_primary(f"   Prioridad: {theme.format_priority(task.priority)}")
    if task.description:
        print_muted(f"   Descripción: {task.description}")


@task.command()
@click.option('--status', '-s', default='pending', type=click.Choice(['pending', 'completed', 'cancelled']))
@click.option('--priority', '-p', type=click.Choice(['high', 'medium', 'low']))
def list(status, priority):
    """Listar tareas"""
    task_manager = TaskManager()
    tasks = task_manager.list_tasks(status=status, priority=priority)
    
    if not tasks:
        print_info("No hay tareas para mostrar")
        return
    
    table = theme.print_table([], "📋 Tareas", "anime")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Título", style="white")
    table.add_column("Prioridad", style="yellow")
    table.add_column("Estado", style="green")
    table.add_column("Creada", style="blue")
    
    for task in tasks:
        table.add_row(
            str(task.id),
            task.title,
            theme.format_priority(task.priority),
            theme.format_status(task.status),
            task.created_at.strftime("%d/%m %H:%M")
        )
    
    theme.console.print(table)


@task.command()
@click.argument('task_id', type=int)
def complete(task_id):
    """Marcar tarea como completada"""
    task_manager = TaskManager()
    success = task_manager.complete_task(task_id)
    
    if success:
        print_success(f"Tarea {task_id} marcada como completada")
    else:
        print_error(f"No se encontró la tarea {task_id}")


@task.command()
@click.argument('task_id', type=int)
@click.confirmation_option(prompt='¿Estás seguro de eliminar esta tarea?')
def delete(task_id):
    """Eliminar una tarea"""
    task_manager = TaskManager()
    success = task_manager.delete_task(task_id)
    
    if success:
        print_success(f"Tarea {task_id} eliminada")
    else:
        print_error(f"No se encontró la tarea {task_id}")


@cli.group()
def pomodoro():
    """Gestión de sesiones Pomodoro"""
    pass


@pomodoro.command()
@click.argument('duration', type=int, default=25)
@click.option('--task-id', '-t', type=int, help='Asociar a tarea específica')
def start(duration, task_id):
    """Iniciar sesión Pomodoro"""
    timer = PomodoroTimer()
    
    if task_id:
        # Verificar que la tarea existe
        task_manager = TaskManager()
        task = task_manager.get_task(task_id)
        if not task:
            print_error(f"No se encontró la tarea {task_id}")
            return
        print_info(f"Pomodoro asociado a tarea: {task.title}")
    
    print_info(f"Iniciando Pomodoro de {duration} minutos...")
    timer.start_session(duration, "work", task_id)


@pomodoro.command()
@click.argument('duration', type=int, default=5)
def break_cmd(duration):
    """Iniciar descanso"""
    timer = PomodoroTimer()
    print_info(f"Iniciando descanso de {duration} minutos...")
    timer.start_session(duration, "break")


@pomodoro.command()
def status():
    """Ver estado actual del Pomodoro"""
    timer = PomodoroTimer()
    status_info = timer.get_status()
    
    if status_info["is_active"]:
        remaining = status_info["remaining_seconds"]
        minutes, seconds = divmod(remaining, 60)
        content = f"{theme.SYMBOLS['timer']} Tiempo restante: {minutes:02d}:{seconds:02d}\n"
        content += f"Tipo: {status_info['session_type']}\n"
        content += f"Iniciado: {status_info['started_at']}"
        theme.print_panel(content, "◆ Pomodoro Activo", "green")
    else:
        print_info("No hay sesión Pomodoro activa")


@cli.group()
def note():
    """Gestión de notas en Obsidian"""
    pass


@note.command()
@click.argument('title')
@click.option('--tag', '-t', multiple=True, help='Tags para la nota')
@click.option('--content', '-c', default='', help='Contenido inicial')
def create(title, tag, content):
    """Crear nueva nota en Obsidian"""
    vault = ObsidianVault()
    
    if not vault.is_configured():
        print_error("Obsidian no está configurado. Ejecuta 'cli init --detect-vault'")
        return
    
    note_path = vault.create_note(title, content, list(tag))
    print_success(f"Nota creada: {note_path}")
    
    if tag:
        print_primary(f"   Tags: {theme.format_tags(list(tag))}")


@note.command()
@click.option('--tag', '-t', help='Filtrar por tag')
def list(tag):
    """Listar notas de Obsidian"""
    vault = ObsidianVault()
    
    if not vault.is_configured():
        print_error("Obsidian no está configurado. Ejecuta 'cli init --detect-vault'")
        return
    
    notes = vault.list_notes(tag)
    
    if not notes:
        print_info("No hay notas para mostrar")
        return
    
    table = theme.print_table([], "📓 Notas de Obsidian", "anime")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Título", style="white")
    table.add_column("Tags", style="yellow")
    table.add_column("Actualizada", style="blue")
    
    for note in notes:
        tags_str = note.get('tags', [])
        if isinstance(tags_str, str):
            tags_str = [tags_str]
        
        table.add_row(
            str(note['id']),
            note['title'],
            theme.format_tags(tags_str),
            note['updated_at'].strftime("%d/%m %H:%M") if note.get('updated_at') else 'N/A'
        )
    
    theme.console.print(table)


@note.command()
@click.argument('query')
def search(query):
    """Buscar notas"""
    vault = ObsidianVault()
    
    if not vault.is_configured():
        print_error("Obsidian no está configurado")
        return
    
    results = vault.search_notes(query)
    
    if not results:
        print_warning(f"No se encontraron notas para: '{query}'")
        return
    
    print_info(f"Resultados para '{query}':")
    for note in results:
        print_muted(f"  {theme.SYMBOLS['note']} {note['title']} - {note['path']}")


@cli.command()
def interactive():
    """Iniciar modo interactivo"""
    from cli.interactive import InteractiveMenu
    menu = InteractiveMenu()
    menu.run()


@cli.group()
def config():
    """Configuración de la CLI"""
    pass


@config.command('set')
@click.argument('key')
@click.argument('value')
def config_set(key, value):
    """Establecer valor de configuración"""
    from core import config
    
    # Intentar convertir a tipo apropiado
    if value.lower() in ['true', 'false']:
        value = value.lower() == 'true'
    elif value.isdigit():
        value = int(value)
    
    config.set(key, value)
    print_success(f"Configuración actualizada: {key} = {value}")


@config.command('get')
@click.argument('key')
def config_get(key):
    """Obtener valor de configuración"""
    from core import config
    
    value = config.get(key)
    if value is not None:
        print_primary(f"{key} = {value}")
    else:
        print_error(f"Clave de configuración no encontrada: {key}")


@config.command('show')
def config_show():
    """Mostrar toda la configuración"""
    from core import config
    import yaml
    
    theme.print_panel(yaml.dump(config.config, default_flow_style=False, allow_unicode=True), "⚙️  Configuración Actual", "blue")


if __name__ == "__main__":
    cli()
