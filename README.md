
# OSLolo v1.0 - Universal Archive Manager

OSLolo es un gestor de archivos universal multiplataforma (Windows, macOS, Linux) con tres modos de operación:
1.  **GUI**: Una interfaz gráfica moderna inspirada en WinRAR.
2.  **TUI**: Una interfaz de usuario de terminal estilo Norton Commander.
3.  **CLI**: Una potente interfaz de línea de comandos para scripting.

## Instalación

1.  Clona este repositorio:
    ```sh
    git clone [https://github.com/your-repo/oslolo.git](https://github.com/your-repo/oslolo.git)
    cd oslolo
    ```

2.  Crea un entorno virtual e instálalo en modo editable:
    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install -e .
    ```
    
3. Para el soporte de RAR, asegúrate de tener el binario `unrar` instalado y en tu PATH del sistema.

## Uso

### Modo GUI (predeterminado)
```sh
oslolo
oslolo archive.zip  # Abrir un archivo directamente
