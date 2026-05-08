---
trigger: manual
---
# Windsurf Rule: Personal CLI Architecture (Productivity Tool)

## Project Overview
You are working on a Python-based Modular CLI for productivity (Tasks, Pomodoro, Obsidian integration). 
The core philosophy is **"Strict Core / Expandable Shell"**.

## 1. Directory Structure
Adhere strictly to this hierarchy to avoid logic pollution:
- `/src/core/`: **LOGIC ONLY.** Should never be modified by module requests. Contains the command orchestrator, security manager, and DB adapters.
- `/src/api/`: Internal bridge. Defines how modules talk to the core.
- `/src/modules/`: Official Python-based extensions.
- `/src/submodules/`: External `.sh` scripts.
- `/src/database/`: Storage layer (MySQL/Plain text).
- `/src/utilitis/`: Shared helper functions (e.g., Obsidian file parsing).
- `/src/config/`: External settings (`config.yml`).

## 2. The "Intouchable Core" Rule
- **NEVER** modify files in `/src/core/` unless explicitly instructed to refactor the base engine.
- If a new feature is needed, implement it as a new file in `/src/modules/`.
- If a module needs a new capability from the core, add a method to the `api` layer instead of exposing core internals.

## 3. Modular Communication (The Bridge)
- **Python Modules:** Must inherit from a base class (if defined) or follow a standard `execute()` entry point.
- **Shell Submodules (.sh):** Must be treated as external entities. 
    - They communicate with the DB/Stats via CLI arguments to the core (e.g., `python main.py db-write ...`).
    - The core acts as a proxy for them.

## 4. Security & Identifier Protocol
- Every time a submodule in `/src/submodules/` is accessed:
    1. **Scan:** Compute the file hash.
    2. **Permission Check:** If the hash is unrecognized or changed, revoke execution permissions (`chmod 000`) and prompt the user.
    3. **Identifier:** Use a local manifest or DB table to store "trusted" hashes.

## 5. Statistics Engine
- The statistics module in `/src/core/` or `/src/modules/` must be a "pure service".
- It should accept a standardized JSON input: `{"type": "bar|line", "data": [[x_list], [y_list]]}`.
- It should output a path to a saved graphic or update the DB.

## 6. Obsidian Integration
- Treat Obsidian vaults as a directory of Markdown files.
- Use the `utilitis` layer to perform fast indexing (mimicking `ripgrep`) without loading heavy libraries if possible.

## 7. Development Mode (Vibecoding)
- Prioritize **Python** for the main engine and API.
- Use **Shell scripts** for lightweight, quick-and-dirty automation that doesn't require complex config.
- Ensure all AI-generated code includes docstrings explaining which architectural layer it belongs to.


