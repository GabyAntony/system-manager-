# 🚀 Instalación y Uso Rápido

## Instalación

```bash
# 1. Clonar o descargar el proyecto
cd /home/gabyantony/Programacion/cli-productividad

# 2. Crear entorno virtual
python3 -m venv venv

# 3. Activar entorno virtual
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt
```

## Uso Inmediato

### Inicialización
```bash
python cli_standalone.py init --detect-vault
```

### Comandos Básicos

#### Tareas
```bash
# Agregar tarea
python cli_standalone.py task add "Comprar leche" --priority high

# Listar tareas
python cli_standalone.py task list

# Completar tarea
python cli_standalone.py task complete 1

# Eliminar tarea
python cli_standalone.py task delete 1
```

#### Pomodoro
```bash
# Iniciar sesión de 25 minutos
python cli_standalone.py pomodoro start 25

# Asociar a tarea específica
python cli_standalone.py pomodoro start 25 --task-id 1

# Iniciar descanso
python cli_standalone.py pomodoro break 5

# Ver estado
python cli_standalone.py pomodoro status
```

#### Notas Obsidian
```bash
# Crear nota
python cli_standalone.py note create "Reunión importante" --tag trabajo --content "Discutir proyecto"

# Listar notas
python cli_standalone.py note list

# Buscar notas
python cli_standalone.py note search "reunión"
```

#### Configuración
```bash
# Ver configuración
python cli_standalone.py config show

# Establecer configuración
python cli_standalone.py config set pomodoro.work_duration 30
```

#### Modo Interactivo
```bash
python cli_standalone.py interactive
```

## 🎯 Demostración Rápida

```bash
# 1. Inicializar
python cli_standalone.py init --detect-vault

# 2. Agregar algunas tareas
python cli_standalone.py task add "Estudiar Python" --priority high
python cli_standalone.py task add "Hacer ejercicio" --priority medium

# 3. Ver tareas
python cli_standalone.py task list

# 4. Iniciar Pomodoro
python cli_standalone.py pomodoro start 25 --task-id 1

# 5. Crear nota
python cli_standalone.py note create "Ideas proyecto" --tag ideas

# 6. Modo interactivo
python cli_standalone.py interactive
```

## ✅ Funcionalidades del MVP

- ✅ **Gestión de Tareas**: Crear, listar, completar, eliminar
- ✅ **Pomodoro Timer**: Sesiones con notificaciones y asociación a tareas
- ✅ **Notas Obsidian**: Crear, listar, buscar notas con tags
- ✅ **UI Rica**: Tablas coloreadas, paneles, notificaciones visuales
- ✅ **Comandos Simples**: CLI directa para operaciones rápidas
- ✅ **Modo Interactivo**: Menú navegable para usuarios TDAD
- ✅ **Configuración**: Sistema de configuración flexible

## 📁 Archivos Importantes

- `cli_standalone.py` - **Archivo principal** (ejecutable)
- `requirements.txt` - Dependencias Python
- `src/` - Código fuente completo (versión modular)
- `README.md` - Documentación completa

## 🎮 Características Especiales para TDAD

- **Interfaz visual clara** con colores y emojis
- **Comandos simples** sin parámetros complejos
- **Modo interactivo** con menús navegables
- **Notificaciones desktop** para Pomodoro
- **Feedback inmediato** en todas las operaciones

¡Listo para usar! 🚀
