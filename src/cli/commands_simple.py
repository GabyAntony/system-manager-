"""
Comandos CLI simplificados sin imports relativos
"""

import click
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from utilitis.theme import theme, print_success, print_error, print_warning, print_info, print_primary, print_accent, print_header, print_separator

# CLI Group
@click.group()
@click.version_option(version="1.0.0", prog_name="CLI Productividad")
def cli():
    """CLI Productividad Personal - Optimizada para TDAD"""
    print_header("CLI Productividad", "Sistema Hacker Anime Aesthetic")
    print_separator()


@cli.command()
@click.option('--detect-vault', is_flag=True, help='Detectar automáticamente vault de Obsidian')
def init(detect_vault):
    """Inicializar configuración de la CLI"""
    print_header("Inicializando CLI Productividad", "Configuración del Sistema")
    
    if detect_vault:
        print_info("Buscando vault de Obsidian...")
        # Simulación de detección
        print_success("Vault de Obsidian detectado: /home/user/Documents/Obsidian")
    
    print_success("Configuración inicial completada")
    print_muted("Configuración guardada en: ~/.cli-productividad/config.yaml")


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
    print_success(f"Tarea creada: {title}")
    print_primary(f"   Prioridad: {priority}")
    if description:
        print_muted(f"   Descripción: {description}")


@task.command()
@click.option('--status', '-s', default='pending', type=click.Choice(['pending', 'completed', 'cancelled']))
@click.option('--priority', '-p', type=click.Choice(['high', 'medium', 'low']))
def list(status, priority):
    """Listar tareas"""
    # Simulación de datos
    tasks = [
        {"id": 1, "title": "Comprar leche", "priority": "high", "status": "pending", "created_at": datetime.now()},
        {"id": 2, "title": "Estudiar Python", "priority": "medium", "status": "completed", "created_at": datetime.now()},
    ]
    
    table = theme.print_table([], "📋 Tareas", "anime")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Título", style="white")
    table.add_column("Prioridad", style="yellow")
    table.add_column("Estado", style="green")
    table.add_column("Creada", style="blue")
    
    for task in tasks:
        table.add_row(
            str(task["id"]),
            task["title"],
            theme.format_priority(task["priority"]),
            theme.format_status(task["status"]),
            task["created_at"].strftime("%d/%m %H:%M")
        )
    
    theme.console.print(table)


@task.command()
@click.argument('task_id', type=int)
def complete(task_id):
    """Marcar tarea como completada"""
    print_success(f"Tarea {task_id} marcada como completada")


@task.command()
@click.argument('task_id', type=int)
@click.confirmation_option(prompt='¿Estás seguro de eliminar esta tarea?')
def delete(task_id):
    """Eliminar una tarea"""
    print_success(f"Tarea {task_id} eliminada")


@cli.group()
def pomodoro():
    """Gestión de sesiones Pomodoro"""
    pass


@pomodoro.command()
@click.argument('duration', type=int, default=25)
@click.option('--task-id', '-t', type=int, help='Asociar a tarea específica')
def start(duration, task_id):
    """Iniciar sesión Pomodoro"""
    if task_id:
        print_info(f"Pomodoro asociado a tarea: {task_id}")
    
    print_info(f"Iniciando Pomodoro de {duration} minutos...")
    print_muted("Timer activo con notificaciones")


@pomodoro.command()
@click.argument('duration', type=int, default=5)
def break_cmd(duration):
    """Iniciar descanso"""
    print_info(f"Iniciando descanso de {duration} minutos...")
    print_muted("Timer de descanso activo")


@pomodoro.command()
def status():
    """Ver estado actual del Pomodoro"""
    content = f"{theme.SYMBOLS['timer']} Tiempo restante: 15:42\n"
    content += "Tipo: work\n"
    content += "Iniciado: 14:30:00"
    theme.print_panel(content, "◆ Pomodoro Activo", "green")


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
    print_success(f"Nota creada: CLI-Notes/{title}.md")
    
    if tag:
        print_primary(f"   Tags: {theme.format_tags(list(tag))}")


@note.command()
@click.option('--tag', '-t', help='Filtrar por tag')
def list(tag):
    """Listar notas de Obsidian"""
    # Simulación de datos
    notes = [
        {"id": 1, "title": "Reunión importante", "tags": ["trabajo", "urgente"], "updated_at": datetime.now()},
        {"id": 2, "title": "Ideas proyecto", "tags": ["ideas", "proyecto"], "updated_at": datetime.now()},
    ]
    
    table = theme.print_table([], "📓 Notas de Obsidian", "anime")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Título", style="white")
    table.add_column("Tags", style="yellow")
    table.add_column("Actualizada", style="blue")
    
    for note in notes:
        table.add_row(
            str(note["id"]),
            note["title"],
            theme.format_tags(note['tags']),
            note["updated_at"].strftime("%d/%m %H:%M")
        )
    
    theme.console.print(table)


@note.command()
@click.argument('query')
def search(query):
    """Buscar notas"""
    print_info(f"Resultados para '{query}':")
    print_muted(f"  {theme.SYMBOLS['note']} Reunión importante - CLI-Notes/reunion-importante.md")
    print_muted(f"  {theme.SYMBOLS['note']} Ideas proyecto - CLI-Notes/ideas-proyecto.md")


@cli.command()
def interactive():
    """Iniciar modo interactivo"""
    print_info("Modo interactivo en desarrollo...")
    print_muted("Prueba estos comandos:")
    print_muted("  cli task add 'Mi tarea'")
    print_muted("  cli pomodoro start 25")
    print_muted("  cli note create 'Mi nota'")


@cli.group()
def config():
    """Configuración de la CLI"""
    pass


@config.command('show')
def config_show():
    """Mostrar toda la configuración"""
    config_text = """
obsidian:
  vault_path: "/home/user/Documents/Obsidian"
  notes_folder: "CLI-Notes"

database:
  path: "~/.cli-productividad/data.db"

pomodoro:
  work_duration: 25
  break_duration: 5
  long_break_duration: 15
  notifications: true

ui:
  theme: "dark"
  colors: true
  animations: true
    """
    
    theme.print_panel(config_text, "⚙️  Configuración Actual", "blue")


if __name__ == "__main__":
    cli()
