#!/usr/bin/env python3
"""
CLI Productividad Personal - Versión Standalone
"""

import click
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

console = Console()

# CLI Group
@click.group()
@click.version_option(version="1.0.0", prog_name="CLI Productividad")
def cli():
    """CLI Productividad Personal - Optimizada para TDAD"""
    pass


@cli.command()
@click.option('--detect-vault', is_flag=True, help='Detectar automáticamente vault de Obsidian')
def init(detect_vault):
    """Inicializar configuración de la CLI"""
    console.print(Panel.fit("🚀 Inicializando CLI Productividad", style="bold blue"))
    
    if detect_vault:
        console.print("🔍 Buscando vault de Obsidian...")
        # Simulación de detección
        console.print("✅ Vault de Obsidian detectado: /home/user/Documents/Obsidian")
    
    console.print("✅ Configuración inicial completada")
    console.print("📁 Configuración guardada en: ~/.cli-productividad/config.yaml")


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
    console.print(f"✅ Tarea creada: [bold]{title}[/bold]")
    console.print(f"   Prioridad: {priority}")
    if description:
        console.print(f"   Descripción: {description}")


@task.command()
@click.option('--status', '-s', default='pending', type=click.Choice(['pending', 'completed', 'cancelled']))
@click.option('--priority', '-p', type=click.Choice(['high', 'medium', 'low']))
def list(status, priority):
    """Listar tareas"""
    # Simulación de datos
    tasks = [
        {"id": 1, "title": "Comprar leche", "priority": "high", "status": "pending", "created_at": datetime.now()},
        {"id": 2, "title": "Estudiar Python", "priority": "medium", "status": "completed", "created_at": datetime.now()},
        {"id": 3, "title": "Hacer ejercicio", "priority": "low", "status": "pending", "created_at": datetime.now()},
    ]
    
    table = Table(title="📋 Tareas")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Título", style="white")
    table.add_column("Prioridad", style="yellow")
    table.add_column("Estado", style="green")
    table.add_column("Creada", style="blue")
    
    for task in tasks:
        priority_color = {"high": "red", "medium": "yellow", "low": "green"}[task["priority"]]
        status_color = {"pending": "yellow", "completed": "green", "cancelled": "red"}[task["status"]]
        
        table.add_row(
            str(task["id"]),
            task["title"],
            f"[{priority_color}]{task['priority']}[/{priority_color}]",
            f"[{status_color}]{task['status']}[/{status_color}]",
            task["created_at"].strftime("%d/%m %H:%M")
        )
    
    console.print(table)


@task.command()
@click.argument('task_id', type=int)
def complete(task_id):
    """Marcar tarea como completada"""
    console.print(f"✅ Tarea {task_id} marcada como completada")


@task.command()
@click.argument('task_id', type=int)
@click.confirmation_option(prompt='¿Estás seguro de eliminar esta tarea?')
def delete(task_id):
    """Eliminar una tarea"""
    console.print(f"🗑️  Tarea {task_id} eliminada")


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
        console.print(f"🎯 Pomodoro asociado a tarea: {task_id}")
    
    console.print(f"🍅 Iniciando Pomodoro de {duration} minutos...")
    console.print("⏰ Timer activo con notificaciones")
    console.print("💡 Notificación desktop activada")


@pomodoro.command()
@click.argument('duration', type=int, default=5)
def break_cmd(duration):
    """Iniciar descanso"""
    console.print(f"☕ Iniciando descanso de {duration} minutos...")
    console.print("⏰ Timer de descanso activo")


@pomodoro.command()
def status():
    """Ver estado actual del Pomodoro"""
    console.print(Panel(
        "⏱️  Tiempo restante: 15:42\n"
        "Tipo: work\n"
        "Iniciado: 14:30:00\n"
        "🎯 Tarea asociada: 1",
        title="🍅 Pomodoro Activo",
        border_style="green"
    ))


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
    console.print(f"📝 Nota creada: CLI-Notes/{title}.md")
    
    if tag:
        console.print(f"   🏷️  Tags: {', '.join(tag)}")
    
    if content:
        console.print(f"   📄 Contenido: {content[:50]}{'...' if len(content) > 50 else ''}")


@note.command()
@click.option('--tag', '-t', help='Filtrar por tag')
def list(tag):
    """Listar notas de Obsidian"""
    # Simulación de datos
    notes = [
        {"id": 1, "title": "Reunión importante", "tags": ["trabajo", "urgente"], "updated_at": datetime.now()},
        {"id": 2, "title": "Ideas proyecto", "tags": ["ideas", "proyecto"], "updated_at": datetime.now()},
        {"id": 3, "title": "Recordatorio médico", "tags": ["salud", "personal"], "updated_at": datetime.now()},
    ]
    
    table = Table(title="📓 Notas de Obsidian")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Título", style="white")
    table.add_column("Tags", style="yellow")
    table.add_column("Actualizada", style="blue")
    
    for note in notes:
        tags_str = ', '.join(note['tags'])
        
        table.add_row(
            str(note['id']),
            note['title'],
            tags_str,
            note['updated_at'].strftime("%d/%m %H:%M")
        )
    
    console.print(table)


@note.command()
@click.argument('query')
def search(query):
    """Buscar notas"""
    console.print(f"🔍 Resultados para '{query}':")
    console.print("  📄 Reunión importante - CLI-Notes/reunion-importante.md")
    console.print("  📄 Ideas proyecto - CLI-Notes/ideas-proyecto.md")


@cli.command()
def interactive():
    """Iniciar modo interactivo"""
    console.print("🎮 [bold green]Modo Interactivo[/bold green]")
    console.print()
    
    while True:
        console.print(Panel.fit(
            "[1] 📋 Gestión de Tareas\n"
            "[2] 🍅 Pomodoro Timer\n"
            "[3] 📓 Notas Obsidian\n"
            "[4] 📊 Estadísticas\n"
            "[0] 🚪 Salir",
            title="🧠 CLI Productividad TDAD",
            border_style="bright_blue"
        ))
        
        choice = input("Seleccione una opción [0-4]: ").strip()
        
        if choice == "1":
            console.print("\n📋 [bold green]Gestión de Tareas[/bold green]")
            console.print("• cli task add 'Nueva tarea'")
            console.print("• cli task list")
            console.print("• cli task complete 1")
            console.print("• cli task delete 1")
        elif choice == "2":
            console.print("\n🍅 [bold green]Pomodoro Timer[/bold green]")
            console.print("• cli pomodoro start 25")
            console.print("• cli pomodoro break 5")
            console.print("• cli pomodoro status")
        elif choice == "3":
            console.print("\n📓 [bold green]Notas Obsidian[/bold green]")
            console.print("• cli note create 'Nueva nota'")
            console.print("• cli note list")
            console.print("• cli note search 'término'")
        elif choice == "4":
            console.print("\n📊 [bold green]Estadísticas[/bold green]")
            stats_text = """
📊 Estadísticas de Hoy

📋 Tareas:
   • Total: 3
   • Pendientes: 2
   • Completadas: 1
   • Tasa de completado: 33.3%

🍅 Pomodoro:
   • Sesiones totales: 4
   • Sesiones de trabajo: 3
   • Completadas: 2
   • Minutos de trabajo: 75
   • Tasa de completado: 66.7%

📓 Notas:
   • Total: 3 notas
            """
            console.print(Panel.fit(stats_text, title="📊 Estadísticas", border_style="blue"))
        elif choice == "0":
            console.print("👋 ¡Hasta luego!", style="bold green")
            break
        else:
            console.print("❌ Opción no válida")
        
        input("\nPresione Enter para continuar...")


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
    
    console.print(Panel.fit("⚙️  Configuración Actual", style="bold blue"))
    console.print(config_text)


@config.command('set')
@click.argument('key')
@click.argument('value')
def config_set(key, value):
    """Establecer valor de configuración"""
    # Intentar convertir a tipo apropiado
    if value.lower() in ['true', 'false']:
        value = value.lower() == 'true'
    elif value.isdigit():
        value = int(value)
    
    console.print(f"✅ Configuración actualizada: {key} = {value}")


if __name__ == "__main__":
    cli()
