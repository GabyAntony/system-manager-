#!/usr/bin/env python3
"""
Test directo de la CLI
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Importar directamente el módulo
import cli.commands_simple as commands_module
cli = commands_module.cli

if __name__ == "__main__":
    cli()
