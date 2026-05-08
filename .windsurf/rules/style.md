---
trigger: manual
name: "Hacker Anime CLI Aesthetic"
target: "command-line interface"
---

## Paleta de Colores

### Mapeo: Hex → ANSI 256 → Proposito

| Rol | Nombre | Hex | ANSI 256 | Uso | Ejemplo |
|-----|--------|-----|----------|-----|---------|
| **Fondo** | Negro puro | #060407 | 232 (black) | Terminal base, sin intervención | Fondo natural |
| **Texto primario** | Gris claro | #EAEAEA | 7 (white) | Cuerpo, labels | "Nombre: Juan" |
| **Primario/Éxito** | Cyan vibrante | #24C7BF | 36 (cyan) | OK, checkmarks, highlights | `✓ Completado` |
| **Secundario/Info** | Azul eléctrico | #2A4DBF | 33 (yellow/blue, ver nota) | Información, headers | Títulos de sección |
| **Advertencia** | Amarillo | #FFD700 | 226 (yellow) | Warnings, caution | `⚠ Requiere atención` |
| **Error/Crítico** | Rojo oscuro | #8A0038 | 196 (red) | Errores, fallos | `✗ Error fatal` |
| **Muted/Secundario** | Marrón/Beige | #6b5a61 | 240 (gray) | Dividers, hints, timestamps | `[14:32:10]` |
| **Púrpura (acentos)** | Púrpura oscuro | #331032 | 53 (purple) | Acentos, decoración sutil | Bordes animados |

**Nota ANSI**: Los 16 colores de terminal son limitados. Para mejores resultados en pantalla oscura (negra):
- **Blue ANSI 4** (`\033[34m`) = azul oscuro, **malo en fondo negro**
- **Bright Blue ANSI 12** (`\033[94m`) = azul electrónico, **mejor**
- **Cyan ANSI 6** (`\033[36m`) = cyan oscuro
- **Bright Cyan ANSI 14** (`\033[96m`) = cyan vibrante, **recomendado** para anime

---

## Tipografía & Monoespaciado

### Fuentes (terminal leerá monoespaciado automáticamente)
- **Terminal debe tener**: Mono font instalada (Monaco, JetBrains Mono, Fira Code)
- **No hardcodees fuente**: El usuario elige en settings de terminal
- **Tamaño sugerido**: 12-14px en terminal

### Ancho de columna
- **Para alineación**: Asumir 80 caracteres = ancho estándar CLI
- **Max width recomendado**: 120 caracteres (moderno, responsive)
- **Monoespaciado**: Cada carácter ocupa exactamente 1 espacio
---

## Restricciones para Terminal

### ✅ Permitido
- Monoespacio: es obligatorio
- Colores ANSI: 16 + 256 extendidos
- Unicode symbols: ✓ ✗ ⚠ ℹ → ← ↑ ↓ ◆ ● ○ □ ■
- Negrita, dim, subrayado
- Blink (parpadeo, evita si es posible)

### ❌ No Permitido / Difícil
- ❌ Fuentes personalizadas (terminal elige)
- ❌ Fondo coloreado (si lo necesitas, usa solubg: ANSI 40-47)
- ❌ RGB puro (#RRGGBB): usa ANSI 256 aproximado
- ❌ Emojis complejos (depende de terminal, puede romperse)
- ❌ Imágenes inline
- ❌ Transparencia

### Emojis Seguros
```
✓  ✗  ⨯  ⚠  ℹ  →  ←  ↑  ↓
◆  ●  ○  □  ■  ▪  ▬  ─  ┌  ┐  └  ┘  │
⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏  (spinner dots)
```

**Evita**: 😀 🎉 👍 (dependen del color emoji support)

---
Regla de Implementación UI:

Toda la lógica de color debe estar centralizada en src/utilitis/theme.py.

Los módulos NO deben usar códigos ANSI directamente; deben llamar a funciones como theme.print_success("mensaje").

Para los scripts .sh en submodules, el core debe proveer un "wrapper" que aplique estos colores automáticamente para mantener la consistencia.