#!/usr/bin/env python3
"""
CLI Productividad Personal - Entry Point
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent))

import click
from rich.console import Console
from rich.panel import Panel

from cli.commands import cli
from core.config import config

console = Console()


@cli.command()
@click.option('--detect-vault', is_flag=True, help='Detectar automáticamente vault de Obsidian')
def init(detect_vault):
    """Inicializar configuración de la CLI"""
    console.print(Panel.fit("🚀 Inicializando CLI Productividad", style="bold blue"))
    
    if detect_vault:
        vault_path = config.detect_obsidian_vault()
        if vault_path:
            config.set('obsidian.vault_path', vault_path)
            console.print(f"✅ Vault de Obsidian detectado: {vault_path}")
        else:
            console.print("❌ No se detectó ningún vault de Obsidian")
            console.print("Por favor, configura manualmente con: cli config set obsidian.vault_path /ruta/al/vault")
    
    console.print("✅ Configuración inicial completada")
    console.print(f"📁 Configuración guardada en: {config.config_file}")
    
    # Mostrar configuración actual
    console.print("\n📋 Configuración actual:")
    console.print(f"   Vault Obsidian: {config.get('obsidian.vault_path', 'No configurado')}")
    console.print(f"   Base de datos: {config.get('database.path')}")
    console.print(f"   Duración Pomodoro: {config.get('pomodoro.work_duration')} min")


if __name__ == "__main__":
    cli()
