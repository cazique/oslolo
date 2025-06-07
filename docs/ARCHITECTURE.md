# Arquitectura de OSLolo

OSLolo está diseñado siguiendo los principios de la Arquitectura Limpia (Clean Architecture) para asegurar una clara separación de responsabilidades, alta cohesión y bajo acoplamiento.

## Capas Principales

### 1. `core` (Dominio y Lógica de Aplicación)
Esta es la capa central y no depende de ninguna otra capa externa.
- **`archive_manager.py`**: El Facade principal. Proporciona una API de alto nivel (`extract`, `create`, `list`) que las interfaces de usuario consumen. No sabe nada sobre GUI, TUI o CLI.
- **`compression_engine.py`**: Orquesta las operaciones. Usa `format_detector` para elegir el `handler` correcto.
- **`format_detector.py`**: Un componente simple que determina el tipo de archivo (y por tanto, el handler a usar) basándose en la extensión.
- **`format_handlers/`**: Implementaciones concretas para cada formato de archivo (`zip`, `rar`, `7z`, `tar`). Cada handler hereda de `BaseHandler` y encapsula la lógica específica de la librería correspondiente (e.g., `py7zr`, `rarfile`).

### 2. `launchers` y `main.py` (Punto de Entrada)
- **`main.py`**: Es el punto de entrada principal del programa (`entry_point`). Su única responsabilidad es parsear los argumentos iniciales (`--tui`, `--gui`, o un comando CLI) y delegar la ejecución al `launcher` apropiado.
- **`launchers/*.py`**: Cada `launcher` (`gui_launcher`, `tui_launcher`, `cli_launcher`) se encarga de inicializar y ejecutar su respectiva interfaz de usuario.

### 3. `gui`, `tui`, `cli` (Presentación / Interfaces de Usuario)
Estas capas contienen todo el código relacionado con la interacción con el usuario. Todas ellas dependen de la capa `core` (específicamente de `ArchiveManager`) para realizar las operaciones.

- **`gui/` (PyQt6)**:
  - Sigue un patrón similar a MVC (Model-View-Controller).
  - **`views/`**: Las clases de QWidget/QMainWindow (`main_window.py`) que definen la apariencia.
  - **`controllers/`**: La lógica de la UI (`main_controller.py`). Conecta los eventos de la vista (clics de botón) con las llamadas al `ArchiveManager`. Usa `QThreadPool` para ejecutar operaciones del `core` en hilos separados y no bloquear la UI.
  - **`components/`**: Widgets reutilizables (`DragDropTreeWidget`).

- **`tui/` (Textual)**:
  - **`app.py`**: La clase principal `App` de Textual.
  - **`screens/`**: Define las diferentes pantallas de la aplicación (e.g., `main_screen.py`).
  - **`widgets/`**: Componentes de la UI como el `DualPanel` y `FileBrowser`.

- **`cli/` (Click)**:
  - **`commands/`**: Cada archivo define un comando (`extract`, `create`, etc.). Usan decoradores de Click y llaman directamente a los métodos del `ArchiveManager`.

## Flujo de Datos
Un ejemplo de flujo para `oslolo extract archive.zip`:
1.  **`main.py`** detecta el comando `extract`.
2.  Delega a **`cli_launcher.cli()`**.
3.  **Click** invoca la función `extract()` en **`cli/commands/extract.py`**.
4.  La función `extract()` instancia `ArchiveManager` desde **`core`**.
5.  Llama a `manager.extract('archive.zip', ...)`.
6.  `ArchiveManager` llama a `engine.extract(...)`.
7.  `CompressionEngine` usa `detect_format` para identificarlo como 'zip'.
8.  Obtiene una instancia de `ZipHandler` desde `get_handler`.
9.  Llama a `zip_handler.extract()`, que finalmente usa la librería `zipfile` de Python para hacer el trabajo.
10. El resultado (éxito o error) burbujea hacia arriba hasta la CLI, que lo imprime al usuario.
