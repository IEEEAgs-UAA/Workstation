"""
Launcher fuera del paquete, para PyInstaller o doble clic.
Los scripts de entrada no pueden usar imports relativos, por eso vive
junto a la carpeta createEvent/ y no dentro de ella.
"""

from createEvent.gui.app import main

if __name__ == "__main__":
    main()
