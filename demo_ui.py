#!/usr/bin/env python3
"""
Demostración del nuevo sistema UI Hacker Anime Aesthetic
"""

import time
import random
from src.utilitis.theme import (
    theme, print_success, print_error, print_warning, print_info, 
    print_primary, print_muted, print_accent, print_header, print_separator,
    ColorTheme
)
from src.utilitis.ui_components import (
    DataTable, StatusPanel, ProgressBar, AnimatedSpinner, 
    MenuRenderer, Card, Timeline, create_table, create_panel, 
    create_progress_bar, create_spinner, create_menu, create_card, create_timeline
)


def demo_colors_and_symbols():
    """Demostrar paleta old hacker"""
    theme.header("SYSTEM INTERFACE", "OLD HACKER AESTHETIC V2.0")
    theme.separator('═', 60)
    
    print_success("[+] OPERATION SUCCESSFUL")
    print_error("[!] CRITICAL ERROR DETECTED")
    print_warning("[*] SYSTEM WARNING")
    print_info("[i] SYSTEM INFORMATION")
    print_primary("PRIMARY TERMINAL OUTPUT")
    print_muted("secondary system data")
    print_accent("accent system highlight")
    
    theme.separator('─', 40)
    print_primary("AVAILABLE SYSTEM SYMBOLS:")
    symbols_demo = [
        ("Navigation", ">> << ^^ vv"),
        ("Status", "[+] [!] [*] [i]"),
        ("Progress", "░ ▒ ▓ █"),
        ("Borders", "┌ ┐ └ ┘ │ ─"),
        ("Loading", "| / - \\")
    ]
    
    for name, symbols in symbols_demo:
        print_muted(f"  {name}: {symbols}")
    
    input("\n[PRESS ENTER TO CONTINUE]")


def demo_tables():
    """Demostrar tablas old hacker"""
    theme.header("DATA TABLES", "COMPACT TERMINAL DISPLAY")
    theme.separator('═', 60)
    
    # Tabla de tareas
    table = create_table("TASK MANAGER", "hacker")
    table.add_column("ID", style="cyan", width=4)
    table.add_column("TITLE", style="white")
    table.add_column("PRIO", style="yellow", width=4)
    table.add_column("STATUS", style="green", width=6)
    table.add_column("PROG", style="blue", width=5)
    
    tasks_data = [
        ["1", "Theme System", "HIGH", "[DONE]", "100%"],
        ["2", "Commands Refactor", "MED", "[DONE]", "100%"],
        ["3", "UI Components", "MED", "[DONE]", "100%"],
        ["4", "Module Updates", "LOW", "[PEND]", "75%"],
        ["5", "Documentation", "LOW", "[PEND]", "30%"]
    ]
    
    table.add_rows(tasks_data)
    table.render()
    
    theme.separator('─', 40)
    
    # Tabla de estadísticas
    stats_table = create_table("SYSTEM METRICS", "hacker")
    stats_table.add_column("METRIC", style="cyan")
    stats_table.add_column("VALUE", style="white")
    stats_table.add_column("TREND", style="green")
    
    stats_data = [
        ["Tasks Completed", "42", "↑ +15%"],
        ["Pomodoro Sessions", "156", "↑ +8%"],
        ["Notes Created", "89", "↑ +22%"],
        ["Productivity", "87%", "↑ +5%"]
    ]
    
    stats_table.add_rows(stats_data)
    stats_table.render()
    
    input("\n[PRESS ENTER TO CONTINUE]")


def demo_panels():
    """Demostrar paneles old hacker"""
    theme.header("STATUS PANELS", "SYSTEM MESSAGES")
    theme.separator('═', 60)
    
    # Panel de éxito
    success_panel = create_panel("[+] SUCCESS", "green")
    success_panel.success("Theme system implementation complete")
    
    # Panel de advertencia
    warning_panel = create_panel("[*] WARNING", "yellow")
    warning_panel.warning("High priority tasks pending")
    
    # Panel de error
    error_panel = create_panel("[!] ERROR", "red")
    error_panel.error("Database connection failed")
    
    # Panel informativo
    info_panel = create_panel("[i] SYSTEM INFO", "cyan")
    info_content = f"""Version: 1.0.0
Status: ACTIVE
Memory: {random.randint(100, 500)}MB
CPU: {random.randint(10, 30)}%
Uptime: {random.randint(1, 24)}h"""
    info_panel.show(info_content)
    
    input("\n[PRESS ENTER TO CONTINUE]")


def demo_progress():
    """Demostrar progreso grande y animaciones"""
    theme.header("PROGRESS SYSTEM", "LARGE VISUAL FEEDBACK")
    theme.separator('═', 60)
    
    # Barra de progreso grande
    print_info("SYSTEM PROGRESS TRACKER:")
    progress = create_progress_bar(100, "PROCESSING SYSTEM FILES")
    
    for i in range(0, 101, 5):
        progress.set_progress(i)
        time.sleep(0.1)
    
    print_success("PROCESSING COMPLETE")
    theme.separator('─', 40)
    
    # Spinner animado
    print_info("SYSTEM SCAN INITIATED:")
    with create_spinner("SCANNING SYSTEM FILES"):
        time.sleep(2)
    
    print_success("SCAN COMPLETE")
    
    input("\n[PRESS ENTER TO CONTINUE]")


def demo_cards():
    """Demostrar tarjetas old hacker"""
    theme.header("INFO CARDS", "COMPACT DISPLAY")
    theme.separator('═', 60)
    
    # Tarjeta de información
    info_card = create_card(
        "SYSTEM STATUS",
        "Old hacker aesthetic\n" +
        "ASCII art compatible\n" +
        "Minimal design",
        "info"
    )
    info_card.render()
    
    theme.separator('─', 30)
    
    # Tarjeta de éxito
    success_card = create_card(
        "[+] IMPLEMENTATION",
        "All UI components refactored\n" +
        "Centralized theme system\n" +
        "Style.md compliance",
        "success"
    )
    success_card.render()
    
    theme.separator('─', 30)
    
    # Tarjeta de advertencia
    warning_card = create_card(
        "[*] NEXT STEPS",
        "Config integration\n" +
        "Advanced animations\n" +
        "Custom themes",
        "warning"
    )
    warning_card.render()
    
    input("\n[PRESS ENTER TO CONTINUE]")


def demo_timeline():
    """Demostrar línea de tiempo old hacker"""
    theme.header("SYSTEM TIMELINE", "EVENT TRACKER")
    theme.separator('═', 60)
    
    timeline = create_timeline()
    timeline.add_event("09:00", "Project Start", "Repository creation", "info")
    timeline.add_event("10:30", "Requirements", "Theme system definition", "info")
    timeline.add_event("12:00", "Base Implementation", "Centralized theme", "success")
    timeline.add_event("14:00", "Refactoring", "Commands.py updated", "success")
    timeline.add_event("16:00", "UI Components", "Reusable components", "success")
    timeline.add_event("18:00", "Integration", "All modules updated", "success")
    timeline.add_event("20:00", "Demo", "System complete", "info")
    
    timeline.render()
    
    input("\n[PRESS ENTER TO CONTINUE]")


def demo_menu():
    """Demostrar menú old hacker"""
    theme.header("INTERACTIVE MENU", "COMMAND INTERFACE")
    theme.separator('═', 60)
    
    menu = create_menu("MAIN SYSTEM MENU")
    menu.add_option("1", "Task Manager", "Create and manage tasks")
    menu.add_option("2", "Pomodoro Timer", "Focus sessions")
    menu.add_option("3", "Notes System", "Document management")
    menu.add_option("4", "Configuration", "System settings")
    menu.add_option("5", "Statistics", "Reports and metrics")
    menu.add_option("x", "Exit", "Terminate session")
    
    # Simular selección
    print_info("SIMULATING USER SELECTION...")
    time.sleep(1)
    choice = "1"
    print_primary(f"OPTION SELECTED: {choice}")
    
    if choice == "1":
        print_info("LOADING TASK MANAGER...")
        time.sleep(1)
        print_success("TASK MANAGER LOADED")
    
    input("\n[PRESS ENTER TO CONTINUE]")


def demo_formatting():
    """Demostrar formato old hacker"""
    theme.header("FORMATTING SYSTEM", "TEXT STYLES")
    theme.separator('═', 60)
    
    # Formato de prioridades
    print_primary("PRIORITY FORMATTING:")
    priorities = ["high", "medium", "low"]
    for priority in priorities:
        formatted = theme.format_priority(priority)
        print(f"  {formatted}")
    
    theme.separator('─', 30)
    
    # Formato de estados
    print_primary("STATUS FORMATTING:")
    statuses = ["pending", "completed", "cancelled"]
    for status in statuses:
        formatted = theme.format_status(status)
        print(f"  {formatted}")
    
    theme.separator('─', 30)
    
    # Formato de tags
    print_primary("TAG FORMATTING:")
    tags_list = [["work", "urgent"], ["ideas", "project"], ["personal"]]
    for tags in tags_list:
        formatted = theme.format_tags(tags)
        print(f"  {formatted}")
    
    theme.separator('─', 30)
    
    # Timestamp
    print_primary("SYSTEM TIMESTAMP:")
    timestamp = theme.timestamp()
    print(f"  {timestamp}")
    
    input("\n[PRESS ENTER TO CONTINUE]")


def main():
    """Función principal de demostración old hacker"""
    theme.header("CLI PRODUCTIVITY SYSTEM", "OLD HACKER AESTHETIC V2.0")
    theme.separator('═', 60)
    print_info("WELCOME TO THE NEW UI SYSTEM DEMO")
    print_muted("This demonstration shows all capabilities of the refactored system")
    theme.separator('═', 60)
    
    demos = [
        ("Colors & Symbols", demo_colors_and_symbols),
        ("Data Tables", demo_tables),
        ("Status Panels", demo_panels),
        ("Progress & Animation", demo_progress),
        ("Info Cards", demo_cards),
        ("Timeline", demo_timeline),
        ("Interactive Menu", demo_menu),
        ("Formatting", demo_formatting)
    ]
    
    while True:
        theme.header("DEMO SELECTION", "AVAILABLE OPTIONS")
        
        for i, (name, _) in enumerate(demos, 1):
            print(f"  {i}. {name.upper()}")
        
        print(f"  X. EXIT")
        theme.separator('═', 50)
        
        choice = input(f"{ColorTheme.SYMBOLS['arrow_right']} SELECT DEMO: ").strip()
        
        if choice.lower() == 'x':
            print_info("TERMINATING SESSION...")
            break
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(demos):
                name, func = demos[index]
                print_info(f"EXECUTING: {name.upper()}")
                theme.separator('─', 30)
                func()
                theme.separator('═', 60)
            else:
                print_warning("INVALID SELECTION")
        except ValueError:
            print_warning("ENTER VALID NUMBER")
    
    print_success("DEMO COMPLETE")
    print_muted("THANKS FOR TESTING THE OLD HACKER AESTHETIC SYSTEM")


if __name__ == "__main__":
    main()
