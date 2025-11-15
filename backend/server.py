# server.py
"""
Servidor de simulación de semáforos (FastAPI + WebSocket).
"""

import asyncio
import json
from typing import Set, Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

class GestorConexiones:
    def __init__(self):
        self.activos: Set[WebSocket] = set()

    async def conectar(self, websocket: WebSocket):
        await websocket.accept()
        self.activos.add(websocket)

    def desconectar(self, websocket: WebSocket):
        self.activos.discard(websocket)

    async def transmitir(self, mensaje: Dict):
        datos = json.dumps(mensaje)
        por_eliminar = []
        for ws in list(self.activos):
            try:
                await ws.send_text(datos)
            except Exception:
                por_eliminar.append(ws)
        for ws in por_eliminar:
            self.desconectar(ws)

gestor = GestorConexiones()

# Parámetros de simulación
DUR_VERDE = 6
DUR_AMARILLO = 2
DUR_ROJO = 8
CICLO_TOTAL = DUR_VERDE + DUR_AMARILLO + DUR_ROJO

DESFASES = {
    "S1": 0,
    "S2": CICLO_TOTAL // 4,
    "S3": (CICLO_TOTAL // 2),
    "S4": (3 * CICLO_TOTAL) // 4,
}

estado: Dict[str, str] = {nombre: "red" for nombre in DESFASES.keys()}

evento_tick = asyncio.Event()
contador_tick = 0

def color_por_fase(fase_local: int) -> str:
    if fase_local < DUR_VERDE:
        return "green"
    elif fase_local < DUR_VERDE + DUR_AMARILLO:
        return "yellow"
    else:
        return "red"

async def tarea_semaforo(nombre: str, desfase: int):
    global contador_tick
    color_anterior = None
    while True:
        await evento_tick.wait()
        fase_local = (contador_tick + desfase) % CICLO_TOTAL
        color = color_por_fase(fase_local)
        if color != color_anterior:
            estado[nombre] = color
            color_anterior = color
            await gestor.transmitir({"type": "estado", "estado": estado, "tick": contador_tick})
        await asyncio.sleep(0)

async def generador_tick(intervalo_seg=1):
    global contador_tick
    while True:
        await asyncio.sleep(intervalo_seg)
        contador_tick += 1
        evento_tick.set()
        await asyncio.sleep(0)
        evento_tick.clear()

@app.on_event("startup")
async def inicio():
    for nombre, desfase in DESFASES.items():
        asyncio.create_task(tarea_semaforo(nombre, desfase))
    asyncio.create_task(generador_tick(intervalo_seg=1))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await gestor.conectar(websocket)
    try:
        await websocket.send_text(json.dumps({"type": "estado", "estado": estado, "tick": contador_tick}))

        async def recibir():
            while True:
                try:
                    texto = await websocket.receive_text()
                except WebSocketDisconnect:
                    break
                except Exception:
                    await asyncio.sleep(0.1)
                    continue
                try:
                    msg = json.loads(texto)
                    if msg.get("accion") == "get_estado":
                        await websocket.send_text(json.dumps({"type": "estado", "estado": estado, "tick": contador_tick}))
                except json.JSONDecodeError:
                    pass

        tarea_receptor = asyncio.create_task(recibir())

        while not tarea_receptor.done():
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        gestor.desconectar(websocket)
    finally:
        gestor.desconectar(websocket)

@app.get("/")
async def index():
    return HTMLResponse(
        "<html><body><h3>Servidor de semáforos en ejecución</h3><p>Conéctese al WebSocket en /ws</p></body></html>"
    )
