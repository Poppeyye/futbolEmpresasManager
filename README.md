# Manager de FutbolEmpresas

Este proyecto de Python scrapea información de FutbolEmpresas y envía un evento al calendario del equipo
en función de los partidos de fútbol que aparezcan en la web.

## Requisitos

- Python 3.x
- Credenciales de Google API
- API de Google Calendar habilitada
- Variables de entorno:
    - creds: Ruta al archivo de credenciales de Google API
    - token: Ruta al archivo de token de Google API
    - emails_file
    - team: Nombre del equipo con guiones (amigos-del-deporte)