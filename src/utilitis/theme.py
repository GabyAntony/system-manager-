"""
Sistema de temas centralizado para CLI Productividad
Hacker Anime Aesthetic - Basado en .windsurf/rules/style.md
"""

import sys
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
from datetime import datetime


class ColorTheme:
    """Mapeo de colores ANSI 256 para Hacker Anime Aesthetic"""
    
    # Mapeo exacto según style.md
    COLORS = {
        'background': 232,      # #060407 negro puro
        'primary': 7,           # #EAEAEA gris claro (texto principal)
        'success': 36,          # #24C7BF cyan vibrante
        'info': 33,             # #2A4DBF azul eléctrico  
        'warning': 226,         # #FFD700 amarillo
        'error': 196,           # #8A0038 rojo oscuro
        'muted': 240,           # #6b5a61 marrón/beige
        'accent': 53,           # #331032 púrpura oscuro
    }
    
    # ASCII Art para headers old hacker vibes
    ASCII_ART = {
        'header_main': [
            '╔══════════════════════════════════════════════════════════════╗',
            '║  ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗     ║',
            '║  ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║     ║',
            '║     ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║     ║',
            '║     ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     ║',
            '║     ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗║',
            '║     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝║',
            '╚══════════════════════════════════════════════════════════════╝'
        ],
        'header_task': [
            '┌─────────────────────────────────────────────────────────────┐',
            '│  █▀▀ █   █ █▀▀ █▀▀   █ █ █ █▀▀ █▀▀ █▀▀ █▀█ █▀▀ █▀▀ █▀▀   │',
            '│  █▀▀ █▄▄ █ █▀▀ █▀▀   ▀▄▀▄▀ █▀  █▀  █▀▀ █▀▄ █▀  █▀▀ █▀▀   │',
            '│  ▀▀▀ ▄▄█ ▀▀▀ ▀▀▀   ▀ ▀ ▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀ ▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀   │',
            '└─────────────────────────────────────────────────────────────┘'
        ],
        'header_pomodoro': [
            '┌─────────────────────────────────────────────────────────────┐',
            '│  █▀▄ █▀▀ █▀▀ █ █ █▄█ █▀▀ █▀█ █▀▀ █▀▀   █▀▀ █▀▀ █▀▀ █▀▀ █▀█ │',
            '│  █▀  █▀▀ ▀▀▀ █▀▄ █ █ █ █▀  █▀▄ █▀  █▀▀   █▀  █▀  █▀  █▀▄ █▀█ │',
            '│  ▀▀▀ ▀▀▀ ▀▀▀ ▀ ▀ ▀▀▀ ▀▀▀ ▀ ▀ ▀▀▀ ▀▀▀   ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀ ▀ │',
            '└─────────────────────────────────────────────────────────────┘'
        ],
        'border_thick': [
            '╔══════════════════════════════════════════════════════════════╗',
            '║                                                               ║',
            '╚══════════════════════════════════════════════════════════════╝'
        ],
        'border_thin': [
            '┌─────────────────────────────────────────────────────────────┐',
            '│                                                             │',
            '└─────────────────────────────────────────────────────────────┘'
        ],
        'border_double': [
            '╔══════════════════════════════════════════════════════════════╗',
            '║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║ ║',
            '╚══════════════════════════════════════════════════════════════╝'
        ]
    }
    
    # Símbolos Unicode + ASCII old hacker
    SYMBOLS = {
        'success': '[+]',
        'error': '[!]',
        'warning': '[*]',
        'info': '[i]',
        'arrow_right': '>>',
        'arrow_left': '<<',
        'arrow_up': '^^',
        'arrow_down': 'vv',
        'diamond': '<>',
        'bullet': '●',
        'circle': '○',
        'square': '■',
        'hollow_square': '[ ]',
        'block': '██',
        'line': '─',
        'corner_tl': '┌',
        'corner_tr': '┐',
        'corner_bl': '└',
        'corner_br': '┘',
        'vertical': '│',
        'timer': '⠋',
        'note': '[N]',
        'search': '[S]',
        'loading': ['◐', '◓', '◑', '◒'],
        'progress': ['░', '▒', '▓', '█'],
        'scan': ['|', '/', '-', '\\'],
        'spinner': ['▂', '▄', '▆', '█'],
        'loading_frames': ['|', '/', '-', '\\'],
        'progress_frames': ['░', '▒', '▓', '█'],
        'scan_frames': ['▂', '▄', '▆', '█'],
    }
    
    # Frames para animaciones old hacker
    SPINNER_FRAMES = ['◐', '◓', '◑', '◒']
    LOADING_FRAMES = ['|', '/', '-', '\\']
    PROGRESS_FRAMES = ['░', '▒', '▓', '█']
    SCAN_FRAMES = ['▂', '▄', '▆', '█']
    
    @classmethod
    def get_color_code(cls, color_name: str) -> str:
        """Obtener código ANSI para un color"""
        if color_name not in cls.COLORS:
            color_name = 'primary'
        return f"\033[38;5;{cls.COLORS[color_name]}m"
    
    @classmethod
    def reset_color(cls) -> str:
        """Resetear color a default"""
        return "\033[0m"


class ThemeConsole:
    """Console con tema Hacker Anime"""
    
    def __init__(self):
        self.console = Console()
        self.theme = ColorTheme()
    
    def _colorize(self, text: str, color_name: str, bold: bool = False) -> str:
        """Aplicar color a texto"""
        color_code = self.theme.get_color_code(color_name)
        reset = self.theme.reset_color()
        
        if bold:
            return f"{color_code}\033[1m{text}{reset}"
        return f"{color_code}{text}{reset}"
    
    def print(self, text: str, color_name: str = 'primary', bold: bool = False):
        """Imprimir texto con color"""
        colored_text = self._colorize(text, color_name, bold)
        print(colored_text)
    
    def success(self, text: str):
        """Mensaje de éxito"""
        symbol = self.theme.SYMBOLS['success']
        self.print(f"{symbol} {text}", 'success')
    
    def error(self, text: str):
        """Mensaje de error"""
        symbol = self.theme.SYMBOLS['error']
        self.print(f"{symbol} {text}", 'error')
    
    def warning(self, text: str):
        """Mensaje de advertencia"""
        symbol = self.theme.SYMBOLS['warning']
        self.print(f"{symbol} {text}", 'warning')
    
    def info(self, text: str):
        """Mensaje informativo"""
        symbol = self.theme.SYMBOLS['info']
        self.print(f"{symbol} {text}", 'info')
    
    def primary(self, text: str):
        """Mensaje principal"""
        self.print(text, 'primary')
    
    def muted(self, text: str):
        """Texto secundario"""
        self.print(text, 'muted')
    
    def accent(self, text: str):
        """Texto con acento"""
        self.print(text, 'accent')
    
    def header(self, title: str, subtitle: str = "", style: str = "main"):
        """Header con ASCII art old hacker"""
        ascii_art = self.theme.ASCII_ART.get(f'header_{style}', self.theme.ASCII_ART['header_main'])
        
        # Imprimir ASCII art
        for line in ascii_art:
            self.accent(line)
        
        # Título y subtítulo
        if title:
            self.primary(f"  {title.upper()}")
        if subtitle:
            self.muted(f"  {subtitle}")
        
        # Línea separadora
        self.accent("  " + "═" * 60)
    
    def separator(self, char: str = '═', length: int = 60):
        """Línea separadora thick"""
        separator = char * length
        self.muted(separator)
    
    def timestamp(self) -> str:
        """Timestamp formateado"""
        now = datetime.now()
        timestamp = now.strftime("[%H:%M:%S]")
        return self._colorize(timestamp, 'muted')
    
    def print_table(self, data: List[Dict[str, Any]], title: str = "", style: str = "hacker") -> Table:
        """Crear tabla con estilo old hacker"""
        table = Table(title=title if title else None, show_header=True, show_lines=False, padding=(0, 1))
        
        # Configurar colores old hacker
        if style == "hacker":
            table.border_style = "cyan"
            table.header_style = "bold green"
            table.row_styles = ["none"]
            table.box = None  # Sin bordes externos
        
        return table
    
    def print_panel(self, content: str, title: str = "", border_style: str = "cyan") -> None:
        """Crear panel con estilo old hacker sin padding extra"""
        # Usar bordes ASCII
        border_top = "╔" + "═" * (len(content) + 4) + "╗"
        border_bottom = "╚" + "═" * (len(content) + 4) + "╝"
        
        self.accent(border_top)
        if title:
            title_line = "║ " + title.center(len(content) + 2) + " ║"
            self.accent(title_line)
            self.accent("║ " + " " * (len(content) + 2) + " ║")
        
        for line in content.split('\n'):
            content_line = "║ " + line.ljust(len(content) + 2) + " ║"
            self.primary(content_line)
        
        self.accent(border_bottom)
    
    def create_spinner(self, text: str = "Procesando...") -> Progress:
        """Crear spinner animado"""
        return Progress(
            SpinnerColumn("dots"),
            TextColumn(text),
            console=self.console
        )
    
    def format_priority(self, priority: str) -> str:
        """Formatear prioridad con estilo old hacker"""
        colors = {
            'high': 'error',
            'medium': 'warning', 
            'low': 'success'
        }
        symbols = {
            'high': '[HIGH]',
            'medium': '[MED]',
            'low': '[LOW]'
        }
        
        color = colors.get(priority, 'primary')
        symbol = symbols.get(priority, '[MED]')
        
        return self._colorize(symbol, color)
    
    def format_status(self, status: str) -> str:
        """Formatear estado con estilo old hacker"""
        symbols = {
            'pending': '[PEND]',
            'completed': '[DONE]',
            'cancelled': '[KILL]'
        }
        colors = {
            'pending': 'warning',
            'completed': 'success',
            'cancelled': 'error'
        }
        
        symbol = symbols.get(status, '[PEND]')
        color = colors.get(status, 'primary')
        
        return self._colorize(symbol, color)
    
    def format_tags(self, tags: List[str]) -> str:
        """Formatear tags con estilo old hacker"""
        if not tags:
            return ""
        
        formatted_tags = []
        for tag in tags:
            formatted_tag = self._colorize(f"<{tag}>", 'accent')
            formatted_tags.append(formatted_tag)
        
        return " ".join(formatted_tags)
    
    def menu_item(self, index: int, text: str, description: str = "") -> str:
        """Formatear item de menú old hacker"""
        arrow = self.theme.SYMBOLS['arrow_right']
        item = f"{index}. {self._colorize(text.upper(), 'info')} {arrow}"
        
        if description:
            item += f" {self._colorize(f'[{description}]', 'muted')}"
        
        return item
    
    def progress_bar(self, current: int, total: int, width: int = 40) -> str:
        """Crear barra de progreso grande old hacker"""
        filled = int((current / total) * width) if total > 0 else 0
        empty = width - filled
        
        # Usar frames de progreso
        progress_chars = self.theme.PROGRESS_FRAMES
        bar = ""
        
        for i in range(width):
            if i < filled:
                bar += progress_chars[-1]  # █
            else:
                bar += progress_chars[0]  # ░
        
        percentage = f"{(current/total)*100:.1f}%" if total > 0 else "0.0%"
        
        return f"[{self._colorize(bar, 'success')}] {percentage} ({current}/{total})"


# Instancia global para uso en toda la aplicación
theme = ThemeConsole()


# Funciones de conveniencia para uso directo
def print_success(text: str):
    """Alias para theme.success()"""
    theme.success(text)


def print_error(text: str):
    """Alias para theme.error()"""
    theme.error(text)


def print_warning(text: str):
    """Alias para theme.warning()"""
    theme.warning(text)


def print_info(text: str):
    """Alias para theme.info()"""
    theme.info(text)


def print_primary(text: str):
    """Alias para theme.primary()"""
    theme.primary(text)


def print_muted(text: str):
    """Alias para theme.muted()"""
    theme.muted(text)


def print_accent(text: str):
    """Alias para theme.accent()"""
    theme.accent(text)


def print_header(title: str, subtitle: str = ""):
    """Alias para theme.header()"""
    theme.header(title, subtitle)


def print_separator(char: str = '─', length: int = 40):
    """Alias para theme.separator()"""
    theme.separator(char, length)


def get_timestamp() -> str:
    """Alias para theme.timestamp()"""
    return theme.timestamp()
