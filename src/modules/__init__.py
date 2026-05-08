"""
Módulos de la CLI
"""

# Import new API modules
from .tasks.task_module import TaskModule
from .pomodoro.pomodoro_module import PomodoroModule
from .obsidian.obsidian_module import ObsidianModule

# Keep old imports for backward compatibility
from .tasks import TaskManager
from .pomodoro import PomodoroTimer
from .obsidian import ObsidianVault

__all__ = [
    "TaskModule", "PomodoroModule", "ObsidianModule",
    "TaskManager", "PomodoroTimer", "ObsidianVault"
]
