"""
Componentes UI reutilizables para CLI Productividad
Hacker Anime Aesthetic - Componentes visuales consistentes
"""

from typing import List, Dict, Any, Optional, Callable
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich import print as rprint
import time
import threading

from .theme import theme, ColorTheme


class DataTable:
    """Tabla con estilo Hacker Anime para datos estructurados"""
    
    def __init__(self, title: str = "", style: str = "anime"):
        self.title = title
        self.style = style
        self.table = theme.print_table([], title, style)
    
    def add_column(self, name: str, style: str = "white", width: Optional[int] = None):
        """Agregar columna a la tabla"""
        self.table.add_column(name, style=style, width=width)
    
    def add_row(self, *args: str):
        """Agregar fila a la tabla"""
        self.table.add_row(*args)
    
    def add_rows(self, rows: List[List[str]]):
        """Agregar múltiples filas"""
        for row in rows:
            self.add_row(*row)
    
    def render(self):
        """Renderizar la tabla"""
        theme.console.print(self.table)
    
    def from_dict_list(self, data: List[Dict[str, Any]], columns: Dict[str, str]):
        """Crear tabla desde lista de diccionarios"""
        # Configurar columnas
        for col_name, col_style in columns.items():
            self.add_column(col_name, col_style)
        
        # Agregar filas
        for item in data:
            row = [str(item.get(col, "")) for col in columns.keys()]
            self.add_row(*row)


class StatusPanel:
    """Panel con bordes animados para estado del sistema"""
    
    def __init__(self, title: str = "", border_style: str = "purple"):
        self.title = title
        self.border_style = border_style
    
    def show(self, content: str, subtitle: str = ""):
        """Mostrar panel con contenido"""
        if subtitle:
            content = f"{subtitle}\n\n{content}"
        theme.print_panel(content, self.title, self.border_style)
    
    def success(self, message: str):
        """Panel de éxito"""
        self.show(message, f"{ColorTheme.SYMBOLS['success']} Operación Exitosa")
    
    def error(self, message: str):
        """Panel de error"""
        self.show(message, f"{ColorTheme.SYMBOLS['error']} Error Detectado")
    
    def warning(self, message: str):
        """Panel de advertencia"""
        self.show(message, f"{ColorTheme.SYMBOLS['warning']} Advertencia")
    
    def info(self, message: str):
        """Panel informativo"""
        self.show(message, f"{ColorTheme.SYMBOLS['info']} Información")


class ProgressBar:
    """Barra de progreso con estilo Hacker Anime"""
    
    def __init__(self, total: int, description: str = "Procesando"):
        self.total = total
        self.current = 0
        self.description = description
    
    def update(self, increment: int = 1):
        """Actualizar progreso"""
        self.current = min(self.current + increment, self.total)
        self._display()
    
    def set_progress(self, current: int):
        """Establecer progreso específico"""
        self.current = min(current, self.total)
        self._display()
    
    def _display(self):
        """Mostrar barra de progreso grande old hacker"""
        percentage = (self.current / self.total) * 100 if self.total > 0 else 0
        bar_width = 50  # Más grande
        filled = int((self.current / self.total) * bar_width) if self.total > 0 else 0
        empty = bar_width - filled
        
        # Usar frames de progreso más densos
        progress_frames = ColorTheme.PROGRESS_FRAMES
        bar = ""
        
        for i in range(bar_width):
            if i < filled:
                bar += progress_frames[-1]  # █
            else:
                bar += progress_frames[0]  # ░
        
        percentage_str = f"{percentage:.1f}%" if self.total > 0 else "0.0%"
        progress_text = f"{self.description}: [{theme._colorize(bar, 'success')}] {percentage_str} ({self.current}/{self.total})"
        
        print(f"\r{progress_text}", end="", flush=True)
        
        if self.current >= self.total:
            print()  # Nueva línea al completar
    
    def complete(self):
        """Marcar como completado"""
        self.set_progress(self.total)
        theme.success("Proceso completado")


class AnimatedSpinner:
    """Spinner animado con caracteres Unicode"""
    
    def __init__(self, text: str = "Procesando"):
        self.text = text
        self.running = False
        self.thread = None
        self.current_frame = 0
    
    def start(self):
        """Iniciar animación"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        """Detener animación"""
        self.running = False
        if self.thread:
            self.thread.join()
        # Limpiar línea
        print("\r" + " " * (len(self.text) + 10) + "\r", end="")
    
    def _animate(self):
        """Animación del spinner old hacker"""
        while self.running:
            # Usar diferentes tipos de animación
            frames = ColorTheme.LOADING_FRAMES
            frame = frames[self.current_frame]
            spinner_text = f"\r{theme._colorize(frame, 'info')} {self.text}"
            print(spinner_text, end="", flush=True)
            
            self.current_frame = (self.current_frame + 1) % len(frames)
            time.sleep(0.15)  # Un poco más lento para dar efecto
    
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()


class MenuRenderer:
    """Renderizador de menús interactivos con estilo Hacker Anime"""
    
    def __init__(self, title: str = "Menú Principal"):
        self.title = title
        self.options = []
    
    def add_option(self, key: str, text: str, description: str = ""):
        """Agregar opción al menú"""
        self.options.append({
            'key': key,
            'text': text,
            'description': description
        })
    
    def show(self):
        """Mostrar menú old hacker compacto"""
        theme.header(self.title, "OLD HACKER INTERFACE")
        theme.separator('═', 50)
        
        for option in self.options:
            item_text = theme.menu_item(option['key'], option['text'], option['description'])
            print(item_text)
        
        theme.separator('═', 50)
    
    def get_choice(self) -> str:
        """Obtener elección del usuario old hacker"""
        self.show()
        choice = input(f"{ColorTheme.SYMBOLS['arrow_right']} SELECT OPTION: ").strip()
        return choice
        return choice
    
    def interactive_menu(self, actions: Dict[str, Callable]) -> bool:
        """Menú interactivo old hacker"""
        while True:
            choice = self.get_choice()
            
            if choice.lower() in ['q', 'quit', 'exit', 'x']:
                print_info("TERMINATING SESSION...")
                return False
            
            if choice in actions:
                try:
                    print_info(f"EXECUTING: {choice}")
                    result = actions[choice]()
                    if result is False:
                        return False
                except Exception as e:
                    print_error(f"SYSTEM ERROR: {e}")
            else:
                print_warning(f"INVALID COMMAND: {choice}")
            
            theme.separator('─', 30)


class Card:
    """Tarjeta visual para información destacada"""
    
    def __init__(self, title: str, content: str, style: str = "info"):
        self.title = title
        self.content = content
        self.style = style
    
    def render(self):
        """Renderizar tarjeta old hacker compacta"""
        # Usar bordes simples sin padding extra
        content_lines = self.content.split('\n')
        max_width = max(len(self.title), max(len(line) for line in content_lines)) + 4
        
        border = "─" * max_width
        
        print(theme._colorize(f"┌{border}┐", 'accent'))
        print(theme._colorize(f"│ {self.title.center(max_width - 2)} │", 'primary'))
        print(theme._colorize(f"│{' ' * (max_width - 2)}│", 'muted'))
        
        for line in content_lines:
            print(theme._colorize(f"│ {line.ljust(max_width - 3)} │", 'primary'))
        
        print(theme._colorize(f"└{border}┘", 'accent'))


class Timeline:
    """Línea de tiempo visual para eventos"""
    
    def __init__(self):
        self.events = []
    
    def add_event(self, time: str, title: str, description: str = "", status: str = "info"):
        """Agregar evento a la línea de tiempo"""
        self.events.append({
            'time': time,
            'title': title,
            'description': description,
            'status': status
        })
    
    def render(self):
        """Renderizar línea de tiempo old hacker"""
        for i, event in enumerate(self.events):
            # Símbolos old hacker
            status_symbols = {
                'info': '[INFO]',
                'success': '[+]',
                'warning': '[*]',
                'error': '[!]'
            }
            
            symbol = status_symbols.get(event['status'], '[INFO]')
            color = event['status']
            
            # Conector simple
            if i < len(self.events) - 1:
                connector = '│'
                print(theme._colorize(f"  {connector}", 'muted'))
            
            # Evento compacto
            time_str = theme._colorize(f"[{event['time']}]", 'muted')
            symbol_colored = theme._colorize(symbol, color)
            title_colored = theme._colorize(event['title'].upper(), 'primary')
            
            print(f"  {symbol_colored} {time_str} {title_colored}")
            
            if event['description']:
                desc_colored = theme._colorize(f"    >> {event['description']}", 'muted')
                print(desc_colored)


# Funciones de conveniencia
def create_table(title: str = "", style: str = "hacker") -> DataTable:
    """Crear tabla con estilo old hacker"""
    return DataTable(title, style)


def create_panel(title: str = "", border_style: str = "cyan") -> StatusPanel:
    """Crear panel con estilo old hacker"""
    return StatusPanel(title, border_style)


def create_progress_bar(total: int, description: str = "Processing...") -> ProgressBar:
    """Crear barra de progreso grande"""
    return ProgressBar(total, description)


def create_spinner(text: str = "Processing...") -> AnimatedSpinner:
    """Crear spinner animado"""
    return AnimatedSpinner(text)


def create_menu(title: str) -> MenuRenderer:
    """Crear menú old hacker"""
    return MenuRenderer(title)


def create_card(title: str, content: str, style: str = "info") -> Card:
    """Crear tarjeta old hacker"""
    return Card(title, content, style)


def create_timeline() -> Timeline:
    """Crear línea de tiempo"""
    return Timeline()


# Importar funciones del tema para conveniencia
from .theme import (
    print_header, print_separator, print_success, print_error, 
    print_warning, print_info, print_primary, print_muted, print_accent
)
