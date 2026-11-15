"""
event_filler.py

Toda la lógica de automatización de Playwright para el formulario de
creación de eventos de IEEE vTools. Este módulo NO tiene interfaz propia:
lo consume gui_app.py.

Puntos clave de diseño:
- Nunca se hardcodean credenciales aquí; siempre se reciben como parámetros.
- Todas las funciones "de negocio" (fill_*) aceptan un callback `log(str)`
  opcional para reportar progreso a la GUI sin acoplarse a tkinter.
- Los campos de fecha/hora se consideran "sensibles" porque el datepicker
  de vTools es frágil: un formato incorrecto lo deja en blanco o con la
  fecha equivocada sin lanzar ningún error visible. Por eso se valida el
  formato ANTES de escribir nada en la página.


  google-chrome-stable --user-data-dir=/tmp/chrome-playwright --remote-debugging-port=9222

  https://events.vtools.ieee.org/tego_/event/create

"""

from __future__ import annotations

from .constants import (
    CREATE_EVENT_URL,
    DEBUG_PORT,
    DATETIME_FORMAT,
    MONTHS_EN,
    _noop,
)
from .dates import (
    validate_datetime_str,
    format_vtools_datetime,
    validate_event_dates,
)
from .chrome import (
    find_chrome_executable,
    _port_is_open,
    launch_chrome_with_debugging,
)
from .login import (
    login_if_needed,
)
from .tinymce import (
    fill_tinymce,
)
from .sections.host import (
    fill_host_organizational_unit,
    fill_contact_email,
    fill_extra_contact_info,
    enable_add_cohost,
    add_cohost,
    fill_cohost,
    fill_cohosts,
)
from .sections.details import (
    fill_title,
    select_category,
    select_subcategory,
    set_wie_event,
    fill_start_end_time,
    select_timezone,
    fill_description,
    fill_header,
    fill_footer,
    fill_agenda,
    fill_keywords,
    fill_survey_url,
)
from .sections.location import (
    open_location_section,
    select_location_type,
    fill_virtual_info,
    fill_physical_address,
    select_country,
    select_state,
    set_override_lat_lng,
    fill_location,
)
from .sections.registration import (
    open_registration_section,
    select_registration_type_none,
)
from .sections.speakers import (
    open_speakers_section,
    add_speaker,
    expand_speaker_panel,
    fill_speaker,
    fill_speakers,
)
from .sections.reporting import (
    open_reporting_section,
    fill_IEEE_Attendance,
    fill_Guest_Attendance,
)
from .sections.navigation import (
    open_details_section,
    save_as_draft,
)
from .form import (
    fill_event_form,
)
from .controller import (
    AutomationController,
)
