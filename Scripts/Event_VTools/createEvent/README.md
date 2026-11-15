# IEEE vTools - Llenado automático de eventos (GUI)

Interfaz de escritorio (Tkinter) que reutiliza tu script de Playwright para
llenar el formulario de creación de eventos de IEEE vTools.

## Estructura

```
Event_VTools/
├── run_gui.py                  # launcher (PyInstaller / doble clic)
└── createEvent/
    ├── __main__.py             # python -m createEvent
    ├── data/
    │   └── EventsVtools.py     # tu lista de eventos, sin modificar
    ├── automation/             # lógica de Playwright (antes event_filler.py)
    │   ├── __init__.py         # reexporta todo: automation.<función> sigue funcionando
    │   ├── constants.py        # URL, puerto, meses, _noop
    │   ├── dates.py            # validación/formateo de fechas
    │   ├── chrome.py           # detectar y lanzar Chrome
    │   ├── login.py
    │   ├── tinymce.py
    │   ├── form.py             # fill_event_form (orquestación)
    │   ├── controller.py       # AutomationController
    │   └── sections/           # host, details, location, registration,
    │                           # speakers, reporting, navigation
    └── gui/                    # interfaz Tkinter (antes gui_app.py)
        ├── app.py              # ventana principal + main()
        ├── actions.py          # ejecutar / guardar / cerrar / log
        ├── event_binding.py    # evento seleccionado <-> formulario
        ├── datetime_picker.py, helpers.py, constants.py
        └── tabs/               # general, fecha, ubicacion, chrome, cohosts
```

Los imports internos son todos relativos (`from ..data.EventsVtools import events`,
`from .. import automation`), así que el paquete funciona sin importar en qué
ruta del repositorio esté. Cada archivo es pequeño y de una sola responsabilidad.

Otros archivos del proyecto (`.env.example`, `requirements.txt`, `build_*.bat`,
`build_*.sh`) no cambian de lugar, salvo que los scripts de build deben apuntar
a `run_gui.py` en lugar de `gui_app.py` (ver "Empaquetar").

## Cómo funciona el switch "Iniciar Chrome automáticamente"

- **Activado (ON):** la app busca Chrome instalado (Windows o Linux, ver
  `find_chrome_executable()` en `event_filler.py`), lo abre con un perfil
  temporal y `--remote-debugging-port=9222`, navega directo a la URL de
  creación de evento y, si detecta el formulario de login, **ingresa las
  credenciales automáticamente** con las que pongas en la interfaz (o las
  que se hayan cargado desde `.env`).
- **Desactivado (OFF):** la app asume que tú ya tienes Chrome abierto
  manualmente en modo depuración (igual que en tu flujo original):

  ```bash
  # Linux
  google-chrome-stable --user-data-dir=/tmp/chrome-playwright --remote-debugging-port=9222

  # Windows (cmd)
  "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir=C:\chrome-playwright
  ```

  y ya con sesión iniciada. La app solo se conecta vía CDP, sin lanzar nada.

En ambos casos, antes de llenar el formulario la app revisa si el campo
`#username` está visible; si lo está, hace login con las credenciales
indicadas — así que aunque tú abras Chrome manualmente sin loguearte, el
login automático también se activa.

## Campos sensibles (fecha/hora)

El datepicker de vTools no lanza ningún error si el texto no calza con su
formato exacto: simplemente deja el campo vacío o mal interpretado. Por eso
las fechas ya no se escriben como texto libre:

- La pestaña "Fecha y hora" usa un **calendario** (`tkcalendar.DateEntry`)
  para el día, y **listas desplegables de solo lectura** para hora, minuto
  y AM/PM. Es imposible escribir un valor fuera de formato.
- Internamente el valor se sigue traduciendo al formato exacto que exige
  vTools (`DD Mon YYYY hh:mm AM/PM`, ej. `09 Jul 2026 02:03 PM`), pero eso
  ya no depende de que el usuario lo escriba bien.
- El parseo/formateo de fechas ya no usa `strftime`/`strptime` con `%b`
  (que depende del idioma del sistema operativo); usa una tabla fija de
  abreviaturas en inglés, así que funciona igual en un Windows en español
  que en uno en inglés.
- Se sigue validando que la fecha de fin sea posterior a la de inicio antes
  de tocar el navegador.

## Todos los campos editables

- **Contenido:** título, descripción, encabezado, pie de página, agenda,
  keywords, URL de encuesta. Los campos de texto largo aceptan HTML
  (`<p>...</p>`) o texto plano — si escribes texto plano se envuelve
  automáticamente en `<p>`.
- **Fecha y hora:** inicio, fin (calendario) y zona horaria.
- **Ubicación:** tipo (física / virtual / híbrida) con radio buttons que
  habilitan/deshabilitan los campos correspondientes — dirección 1 y 2,
  ciudad, código postal, edificio, país, estado, e información virtual
  (link/instrucciones, solo si el tipo es virtual o híbrida).
- **Host / Chrome:** organización anfitriona (nombre, SPOID, email de
  contacto), switch de Chrome automático, usuario y contraseña.
- **Co-hosts:** casillas y campos para activar primero "Add cohost" en el
  formulario y luego completar uno o más cohosts desde la interfaz.

Nota: los *speakers* (ponentes) de los eventos de ejemplo siguen viniendo
del preset en `EventsVtools.py` y no tienen campos en la interfaz todavía;
si los necesitas editables dime y agrego esa sección.

## Instalación (para desarrollo o para generar el .exe)

```bash
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

No necesitas correr `playwright install chromium`: la app se conecta al
Chrome real ya instalado en el sistema vía CDP, no usa los navegadores
propios de Playwright.

Copia `.env.example` a `.env` y coloca tus credenciales reales (opcional,
también puedes escribirlas directamente en la interfaz cada vez).

## Ejecutar sin empaquetar

Desde la carpeta que contiene `createEvent/` (es decir, `Event_VTools/`):

```bash
python -m createEvent
# o bien
python run_gui.py
```

## Empaquetar como ejecutable

**Windows** (ejecutar en una máquina Windows):
```cmd
build_windows.bat
```

**Linux**:
```bash
chmod +x build_linux.sh
./build_linux.sh
```

Ambos usan:
```bash
pyinstaller --onefile --windowed --name IEEE_vTools_Filler --collect-all playwright run_gui.py
```

`--collect-all playwright` es necesario para que PyInstaller incluya el
driver interno de Playwright (si no, el .exe falla al iniciar Playwright).

El ejecutable queda en `dist/`. **Copia el archivo `.env` junto al ejecutable**
si quieres que las credenciales se autocompleten al abrir la app (la app
busca el `.env` en la misma carpeta del `.exe` cuando corre empaquetada; en
desarrollo lo busca dentro de `createEvent/`).

## Notas de seguridad

- Las credenciales nunca se escriben en el código ni se registran en el log.
- El `.env` con credenciales reales no debe subirse a ningún repositorio;
  agrégalo a tu `.gitignore`.
- Chrome se lanza siempre con un **perfil temporal** (no tu perfil normal),
  para no mezclar sesiones ni depender de que ya tengas Chrome abierto.
