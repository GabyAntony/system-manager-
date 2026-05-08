#!/usr/bin/env python3
"""
Script para ejecutar la CLI simplificada
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from cli.commands_simple import cli

if __name__ == "__main__":
    cli()
