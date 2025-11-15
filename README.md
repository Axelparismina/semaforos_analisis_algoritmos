Simulación de Semáforos — Instrucciones para probar

Requisitos:
- Python 3.10 o superior
- Node.js (LTS) y npm

1) Backend (FastAPI)
- Abrir terminal en la carpeta backend:
  cd backend

- Crear y activar entorno virtual (PowerShell):
  * python -m venv .venv
  * Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force 
  * .\\.venv\Scripts\Activate.ps1

- Instalar dependencias:
  * python -m pip install --upgrade pip
  * python -m pip install fastapi "uvicorn[standard]"

- Ejecutar servidor:
  uvicorn server:app --reload --port 8000

- Verificar:
  Abrir http://127.0.0.1:8000/ en el navegador.
  WebSocket: ws://localhost:8000/ws

2) Frontend (React)
- En otra terminal, ir a la carpeta del frontend:
  cd semaforos-frontend

- Instalar dependencias (si procede):
  npm install

- Ejecutar la app:
  npm start

- Verificar:
  Abrir http://localhost:3000 en el navegador. La UI se conectará al WebSocket del backend y mostrará los 4 semáforos.

Notas:
- Asegúrese de activar el entorno virtual antes de instalar paquetes o ejecutar el servidor.
- Si necesita cambiar puertos, actualice la URL WebSocket en src/App.jsx.
