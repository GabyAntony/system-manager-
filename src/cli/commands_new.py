"""
Comandos CLI principales con Click - Refactored

Usa el Command Orchestrator para comunicarse con los módulos
sin acceder directamente al core.
"""

import click
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from ..core.orchestrator import CommandOrchestrator
from ..utilitis.theme import theme, print_success, print_error, print_warning, print_info, print_primary, print_accent, print_header, print_separator

# Instancia global del orquestador
orchestrator = CommandOrchestrator()

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
    result = orchestrator.execute_task_command(
        "create",
        title=title,
        priority=priority,
        description=description
    )
    
    if result.success:
        task_data = result.data
        print_success(result.message)
        print_primary(f"   Prioridad: {theme.format_priority(task_data['priority'])}")
        if task_data.get('description'):
            print_info(f"   Descripción: {task_data['description']}")
    else:
        print_error(result.error or result.message)


@task.command()
@click.option('--status', '-s', default='pending', type=click.Choice(['pending', 'completed', 'cancelled']))
@click.option('--priority', '-p', type=click.Choice(['high', 'medium', 'low']))
def list(status, priority):
    """Listar tareas"""
    result = orchestrator.execute_task_command(
        "list",
        status=status,
        priority=priority
    )
    
    if not result.success:
        print_error(result.error or result.message)
        return
    
    tasks = result.data
    
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
        created_at = datetime.fromisoformat(task['created_at'].replace('Z', '+00:00')) if isinstance(task['created_at'], str) else task['created_at']
        
        table.add_row(
            str(task['id']),
            task['title'],
            theme.format_priority(task['priority']),
            theme.format_status(task['status']),
            created_at.strftime("%d/%m %H:%M")
        )
    
    theme.console.print(table)


@task.command()
@click.argument('task_id', type=int)
def complete(task_id):
    """Marcar tarea como completada"""
    result = orchestrator.execute_task_command("complete", task_id=task_id)
    
    if result.success:
        print_success(result.message)
    else:
        print_error(result.error or result.message)


@task.command()
@click.argument('task_id', type=int)
@click.confirmation_option(prompt='¿Estás seguro de eliminar esta tarea?')
def delete(task_id):
    """Eliminar una tarea"""
    result = orchestrator.execute_task_command("delete", task_id=task_id)
    
    if result.success:
        print_success(result.message)
    else:
        print_error(result.error or result.message)


@task.command()
@click.argument('task_id', type=int)
@click.option('--title', '-t')
@click.option('--description', '-d')
@click.option('--priority', '-p', type=click.Choice(['high', 'medium', 'low']))
@click.option('--status', '-s', type=click.Choice(['pending', 'completed', 'cancelled']))
def update(task_id, title, description, priority, status):
    """Actualizar una tarea"""
    updates = {}
    
    if title is not None:
        updates['title'] = title
    if description is not None:
        updates['description'] = description
    if priority is not None:
        updates['priority'] = priority
    if status is not None:
        updates['status'] = status
    
    if not updates:
        print_warning("No se especificaron campos para actualizar")
        return
    
    result = orchestrator.execute_task_command("update", task_id=task_id, **updates)
    
    if result.success:
        print_success(result.message)
    else:
        print_error(result.error or result.message)


@task.command()
def stats():
    """Mostrar estadísticas de tareas"""
    result = orchestrator.execute_task_command("stats")
    
    if result.success:
        stats_data = result.data
        
        print_header("📊 Estadísticas de Tareas", "")
        
        table = Table(show_header=False, box=None)
        table.add_column("Métrica", style="cyan")
        table.add_column("Valor", style="yellow")
        
        table.add_row("Total de tareas", str(stats_data.get('total', 0)))
        table.add_row("Completadas", str(stats_data.get('completed', 0)))
        table.add_row("Pendientes", str(stats_data.get('pending', 0)))
        table.add_row("Tasa de completación", f"{stats_data.get('completion_rate', 0):.1f}%")
        
        theme.console.print(table)
    else:
        print_error(result.error or result.message)


@cli.group()
def pomodoro():
    """Gestión de sesiones Pomodoro"""
    pass


@pomodoro.command()
@click.argument('duration', type=int)
@click.option('--type', '-t', default='work', type=click.Choice(['work', 'break', 'long_break']))
@click.option('--task-id', type=int)
def start(duration, type, task_id):
    """Iniciar sesión Pomodoro"""
    result = orchestrator.execute_pomodoro_command(
        "start",
        duration=duration,
        session_type=type,
        task_id=task_id
    )
    
    if result.success:
        session_data = result.data
        print_success(result.message)
        print_info(f"   Duración: {session_data['duration']} minutos")
        print_info(f"   Tipo: {session_data['session_type']}")
        if session_data.get('task_id'):
            print_info(f"   Tarea asociada: {session_data['task_id']}")
    else:
        print_error(result.error or result.message)


@pomodoro.command()
def stop():
    """Detener sesión Pomodoro actual"""
    result = orchestrator.execute_pomodoro_command("stop")
    
    if result.success:
        session_data = result.data
        print_success(result.message)
        if session_data.get('was_completed'):
            print_success("   ¡Sesión completada exitosamente!")
        else:
            print_warning(f"   Sesión cancelada después de {session_data.get('elapsed_seconds', 0):.0f} segundos")
    else:
        print_error(result.error or result.message)


@pomodoro.command()
def status():
    """Mostrar estado de la sesión actual"""
    result = orchestrator.execute_pomodoro_command("status")
    
    if result.success:
        status_data = result.data
        
        if status_data['status'] == 'idle':
            print_info("No hay sesión activa")
        else:
            print_header("🍅 Sesión Pomodoro Activa", "")
            
            table = Table(show_header=False, box=None)
            table.add_column("Propiedad", style="cyan")
            table.add_column("Valor", style="yellow")
            
            table.add_row("ID de sesión", str(status_data['session_id']))
            table.add_row("Tipo", status_data['session_type'])
            table.add_row("Duración", f"{status_data['duration']} minutos")
            table.add_row("Tiempo transcurrido", f"{status_data.get('elapsed_seconds', 0):.0f} segundos")
            table.add_row("Tiempo restante", f"{status_data.get('remaining_seconds', 0):.0f} segundos")
            table.add_row("Progreso", f"{status_data.get('progress_percentage', 0):.1f}%")
            
            theme.console.print(table)
    else:
        print_error(result.error or result.message)


@pomodoro.command()
@click.option('--limit', '-l', default=20, type=int)
def list(limit):
    """Listar sesiones recientes"""
    result = orchestrator.execute_pomodoro_command("list", limit=limit)
    
    if not result.success:
        print_error(result.error or result.message)
        return
    
    sessions = result.data
    
    if not sessions:
        print_info("No hay sesiones para mostrar")
        return
    
    table = theme.print_table([], "🍅 Sesiones Pomodoro", "anime")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Tipo", style="white")
    table.add_column("Duración", style="yellow")
    table.add_column("Completada", style="green")
    table.add_column("Iniciada", style="blue")
    
    for session in sessions:
        started_at = datetime.fromisoformat(session['started_at'].replace('Z', '+00:00')) if isinstance(session['started_at'], str) else session['started_at']
        
        table.add_row(
            str(session['id']),
            session['session_type'],
            f"{session['duration']} min",
            "✅" if session['was_completed'] else "❌",
            started_at.strftime("%d/%m %H:%M")
        )
    
    theme.console.print(table)


@pomodoro.command()
def stats():
    """Mostrar estadísticas de Pomodoro"""
    result = orchestrator.execute_pomodoro_command("stats")
    
    if result.success:
        stats_data = result.data
        
        print_header("📊 Estadísticas Pomodoro", "")
        
        table = Table(show_header=False, box=None)
        table.add_column("Métrica", style="cyan")
        table.add_column("Valor", style="yellow")
        
        table.add_row("Total de sesiones", str(stats_data.get('total_sessions', 0)))
        table.add_row("Sesiones completadas", str(stats_data.get('completed_sessions', 0)))
        table.add_row("Tasa de completación", f"{stats_data.get('completion_rate', 0):.1f}%")
        table.add_row("Tiempo total", f"{stats_data.get('total_minutes', 0)} minutos")
        table.add_row("Tiempo total", f"{stats_data.get('total_hours', 0):.1f} horas")
        
        theme.console.print(table)
    else:
        print_error(result.error or result.message)


@cli.group()
def obsidian():
    """Gestión de vault de Obsidian"""
    pass


@obsidian.command()
def detect():
    """Detectar vaults de Obsidian"""
    result = orchestrator.execute_obsidian_command("detect_vault")
    
    if result.success:
        vaults_data = result.data
        vaults = vaults_data['vaults']
        
        if not vaults:
            print_info("No se encontraron vaults de Obsidian")
            return
        
        print_success(f"Se encontraron {len(vaults)} vault(s):")
        
        for i, vault in enumerate(vaults, 1):
            default_mark = " (default)" if vault.get('is_default') else ""
            print_info(f"  {i}. {vault['path']}{default_mark}")
    else:
        print_error(result.error or result.message)


@obsidian.command()
@click.argument('vault_path')
def set_vault(vault_path):
    """Establecer vault de Obsidian"""
    result = orchestrator.execute_obsidian_command("set_vault", vault_path=vault_path)
    
    if result.success:
        print_success(result.message)
    else:
        print_error(result.error or result.message)


@obsidian.command()
def get_vault():
    """Obtener información del vault actual"""
    result = orchestrator.execute_obsidian_command("get_vault")
    
    if result.success:
        vault_data = result.data
        
        if not vault_data.get('configured'):
            print_warning("No hay vault configurado")
        elif not vault_data.get('exists'):
            print_warning(f"Vault configurado no existe: {vault_data['vault_path']}")
        else:
            print_success(f"Vault configurado: {vault_data['vault_path']}")
            print_info(f"Nombre: {vault_data['name']}")
    else:
        print_error(result.error or result.message)


@obsidian.command()
@click.option('--force', is_flag=True, help='Forzar reindexación completa')
def index(force):
    """Indexar notas del vault"""
    result = orchestrator.execute_obsidian_command("index_notes", force_reindex=force)
    
    if result.success:
        index_data = result.data
        print_success(result.message)
        print_info(f"   Vault: {index_data['vault_path']}")
        print_info(f"   Notas indexadas: {index_data['indexed_count']}")
        if index_data.get('updated_count', 0) > 0:
            print_info(f"   Notas actualizadas: {index_data['updated_count']}")
    else:
        print_error(result.error or result.message)


@obsidian.command()
@click.argument('query')
@click.option('--limit', '-l', default=20, type=int)
def search(query, limit):
    """Buscar notas"""
    result = orchestrator.execute_obsidian_command("search", query=query, limit=limit)
    
    if not result.success:
        print_error(result.error or result.message)
        return
    
    search_data = result.data
    notes = search_data['notes']
    
    if not notes:
        print_info(f"No se encontraron notas para '{query}'")
        return
    
    print_success(f"Se encontraron {search_data['total_found']} notas (mostrando {search_data['returned']}):")
    
    table = theme.print_table([], f"🔍 Resultados para '{query}'", "anime")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Título", style="white")
    table.add_column("Preview", style="yellow")
    table.add_column("Tags", style="green")
    
    for note in notes:
        table.add_row(
            str(note['id']),
            note['title'],
            note.get('content_preview', '')[:50] + "..." if note.get('content_preview') else "",
            note.get('tags', '')[:30]
        )
    
    theme.console.print(table)


@obsidian.command()
@click.argument('title')
@click.option('--content', '-c', default='')
@click.option('--tags', '-t', multiple=True)
def create(title, content, tags):
    """Crear nueva nota"""
    result = orchestrator.execute_obsidian_command(
        "create_note",
        title=title,
        content=content,
        tags=list(tags)
    )
    
    if result.success:
        note_data = result.data
        print_success(result.message)
        print_info(f"   Archivo: {note_data['file_path']}")
    else:
        print_error(result.error or result.message)


@obsidian.command()
@click.option('--limit', '-l', default=50, type=int)
def list_notes(limit):
    """Listar notas indexadas"""
    result = orchestrator.execute_obsidian_command("list_notes", limit=limit)
    
    if not result.success:
        print_error(result.error or result.message)
        return
    
    notes = result.data
    
    if not notes:
        print_info("No hay notas indexadas")
        return
    
    table = theme.print_table([], "📝 Notas Indexadas", "anime")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Título", style="white")
    table.add_column("Preview", style="yellow")
    table.add_column("Actualizada", style="blue")
    
    for note in notes:
        updated_at = datetime.fromisoformat(note['updated_at'].replace('Z', '+00:00')) if isinstance(note['updated_at'], str) else note['updated_at']
        
        table.add_row(
            str(note['id']),
            note['title'],
            note.get('content_preview', '')[:50] + "..." if note.get('content_preview') else "",
            updated_at.strftime("%d/%m %H:%M")
        )
    
    theme.console.print(table)


@cli.group()
def system():
    """Comandos del sistema"""
    pass


@system.command()
def status():
    """Mostrar estado del sistema"""
    system_status = orchestrator.get_system_status()
    
    print_header("🔧 Estado del Sistema", "")
    
    # Módulos
    modules_info = system_status.get('modules', {})
    print_accent("Módulos Cargados:")
    for name, info in modules_info.items():
        status_icon = "✅" if info.get('loaded') else "❌"
        commands = info.get('commands', [])
        print_info(f"  {status_icon} {name}: {len(commands)} comandos")
    
    # Seguridad
    security_info = system_status.get('security', {})
    if security_info.get('success'):
        trusted_count = security_info.get('count', 0)
        print_accent(f"Submódulos Confiables: {trusted_count}")
    else:
        print_warning("Error en sistema de seguridad")
    
    # Base de datos
    db_info = system_status.get('database', {})
    if not db_info.get('error'):
        print_accent(f"Base de Datos: {db_info.get('size_mb', 0):.2f} MB")
        table_counts = db_info.get('table_counts', {})
        for table, count in table_counts.items():
            print_info(f"  {table}: {count} registros")
    else:
        print_warning("Error en base de datos")


@system.command()
def validate():
    """Validar integridad del sistema"""
    validation = orchestrator.validate_system()
    
    print_header("🔍 Validación del Sistema", "")
    
    if validation['valid']:
        print_success("✅ Sistema válido")
    else:
        print_error("❌ Se encontraron problemas")
    
    if validation.get('issues'):
        print_error("Problemas críticos:")
        for issue in validation['issues']:
            print_error(f"  • {issue}")
    
    if validation.get('warnings'):
        print_warning("Advertencias:")
        for warning in validation['warnings']:
            print_warning(f"  • {warning}")
    
    print_info(validation['summary'])


@cli.group()
def security():
    """Gestión de seguridad de submódulos"""
    pass


@security.command()
@click.argument('module_path')
def register(module_path):
    """Registrar un submódulo como confiable"""
    security_manager = orchestrator.get_security_manager()
    result = security_manager.register_submodule(module_path)
    
    if result['success']:
        print_success(result['message'])
    else:
        print_error(result['message'])


@security.command()
def list_trusted():
    """Listar submódulos confiables"""
    security_manager = orchestrator.get_security_manager()
    result = security_manager.list_trusted_submodules()
    
    if result['success']:
        submodules = result['submodules']
        
        if not submodules:
            print_info("No hay submódulos confiables registrados")
            return
        
        print_success(f"Submódulos confiables ({result['count']}):")
        
        for path, info in submodules.items():
            print_info(f"  📁 {path}")
            print_info(f"     Hash: {info['hash'][:16]}...")
            print_info(f"     Registrado: {info['registered_at']}")
            if info.get('description'):
                print_info(f"     Descripción: {info['description']}")
            print_info("")
    else:
        print_error(result['message'])


@security.command()
@click.argument('module_path')
def verify(module_path):
    """Verificar un submódulo"""
    security_manager = orchestrator.get_security_manager()
    verification = security_manager.verify_submodule(module_path)
    
    if verification['trusted']:
        print_success(verification['message'])
    else:
        print_error(verification['message'])
        
        if not verification['registered']:
            print_warning("  El submódulo no está registrado. Use 'security register' para agregarlo.")
        else:
            print_warning("  El hash no coincide. Posible modificación no autorizada.")


@security.command()
@click.option('--directory', '-d', default='src/submodules')
def scan(directory):
    """Escanear directorio de submódulos"""
    security_manager = orchestrator.get_security_manager()
    scan_result = security_manager.scan_submodules_directory(directory)
    
    if not scan_result['success']:
        print_error(scan_result['message'])
        return
    
    print_success(scan_result['message'])
    
    if scan_result['unregistered']:
        print_warning(f"Submódulos no registrados ({len(scan_result['unregistered'])}):")
        for item in scan_result['unregistered']:
            print_warning(f"  📁 {item['path']}")
    
    if scan_result['modified']:
        print_error(f"Submódulos modificados ({len(scan_result['modified'])}):")
        for item in scan_result['modified']:
            print_error(f"  📁 {item['path']}")
            print_error(f"     Hash actual: {item['current_hash'][:16]}...")
            print_error(f"     Hash esperado: {item['trusted_hash'][:16]}...")


if __name__ == '__main__':
    cli()
