# 🧠 CLI Productividad Personal

CLI personalizada para gestión de productividad optimizada para TDAD con integración Obsidian, tareas, Pomodoro y base de datos local.

## 🚀 Características

- **📋 Gestión de Tareas**: Crear, listar, completar y eliminar tareas con prioridades
- **🍅 Pomodoro Timer**: Sesiones de trabajo con notificaciones desktop
- **📓 Integración Obsidian**: Crear y gestionar notas en tu vault
- **🎯 Interfaz Dual**: Comandos simples y menú interactivo
- **💾 Base de Datos Local**: Persistencia con SQLite
- **📊 Estadísticas**: Seguimiento de productividad

## 📦 Instalación

### 1. Clonar repositorio
```bash
git clone <repo-url> cli-productividad
cd cli-productividad
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
# O development mode
pip install -e .
```

### 3. Inicializar configuración
```bash
python src/main.py init --detect-vault
```

## 🎯 Uso Rápido

### Comandos Simples

```bash
# Tareas
cli task add "Comprar leche" --priority high
cli task list
cli task complete 1

# Pomodoro
cli pomodoro start 25
cli pomodoro break 5
cli pomodoro status

# Notas Obsidian
cli note create "Reunión importante" --tag trabajo --content "Discuss project"
cli note list --tag trabajo
cli note search "reunión"
```

### Menú Interactivo

```bash
cli interactive
```

## 📋 Comandos Disponibles

### Tareas
```bash
cli task add <title> [--priority high|medium|low] [--description "desc"]
cli task list [--status pending|completed|cancelled] [--priority high|medium|low]
cli task complete <task_id>
cli task delete <task_id>
```

### Pomodoro
```bash
cli pomodoro start [duration] [--task-id <id>]
cli pomodoro break [duration]
cli pomodoro status
```

### Notas Obsidian
```bash
cli note create <title> [--tag tag1] [--tag tag2] [--content "text"]
cli note list [--tag <tag>]
cli note search <query>
```

### Configuración
```bash
cli config show
cli config get <key>
cli config set <key> <value>
```

## ⚙️ Configuración

La configuración se guarda en `~/.cli-productividad/config.yaml`:

```yaml
obsidian:
  vault_path: "/path/to/obsidian/vault"
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
```

## 🗂️ Estructura del Proyecto

```
cli-productividad/
├── src/
│   ├── main.py              # Entry point
│   ├── cli/                 # Comandos CLI
│   │   ├── commands.py      # Comandos Click
│   │   └── interactive.py   # Menú interactivo
│   ├── core/                # Base de datos y configuración
│   │   ├── database.py      # SQLAlchemy setup
│   │   ├── models.py        # Modelos de datos
│   │   └── config.py        # Gestión de configuración
│   ├── modules/             # Módulos funcionales
│   │   ├── tasks/           # Gestión de tareas
│   │   ├── pomodoro/        # Timer Pomodoro
│   │   └── obsidian/        # Integración Obsidian
│   └── utils/               # Utilidades
├── tests/
├── requirements.txt
├── setup.py
└── README.md
```

## 🎨 Ejemplos de Uso

### Flujo de trabajo diario

```bash
# 1. Ver tareas pendientes
cli task list --status pending

# 2. Iniciar Pomodoro para tarea importante
cli pomodoro start 25 --task-id 1

# 3. Durante el trabajo, crear nota rápida
cli note create "Idea proyecto" --tag ideas --content "Implementar feature X"

# 4. Al completar, marcar tarea
cli task complete 1

# 5. Ver estadísticas del día
cli interactive  # Opción 4 - Estadísticas
```

### Menú Interactivo

El modo interactivo ofrece una experiencia más visual:

```bash
cli interactive
```

Menú principal:
```
┌─ 🧠 CLI Productividad TDAD ───────────────────────┐
│                                                  │
│  1️⃣  Gestión de Tareas                          │
│  2️⃣  Pomodoro Timer                            │
│  3️⃣  Notas Obsidian                            │
│  4️⃣  Estadísticas                              │
│  5️⃣  Configuración                             │
│  0️⃣  Salir                                     │
│                                                  │
└──────────────────────────────────────────────────┘
```

## 🔧 Desarrollo

### Tests
```bash
python -m pytest tests/
```

### Formato
```bash
black src/
```

### New Features
1. Crear módulo en `src/modules/`
2. Agregar comandos en `src/cli/commands.py`
3. Actualizar `src/cli/interactive.py` para UI

## 🚧 Roadmap

### v1.1 (Próxima semana)
- [ ] Hábitos y seguimiento diario
- [ ] Planificación semanal
- [ ] Estadísticas avanzadas

### v1.2 (Mes siguiente)
- [ ] Integración Notion
- [ ] Calendar integration
- [ ] AI suggestions

### v2.0 (Largo plazo)
- [ ] Web dashboard
- [ ] Mobile companion
- [ ] Team features

## 📝 Licencia

MIT License - ver archivo LICENSE para detalles.

## 🤝 Contribuciones

Welcome! Issues y PRs son bienvenidos.

---

**Hecho con ❤️ para personas con TDAD**
