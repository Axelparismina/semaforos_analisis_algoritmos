import React, { useEffect, useRef, useState } from "react";
import Semaforo from "./Semaforo";

const URL_WS = (host = "localhost", port = 8000) => `ws://${host}:${port}/ws`;

export default function App() {
  const [estado, setEstado] = useState({
    S1: "red",
    S2: "red",
    S3: "red",
    S4: "red",
  });
  const [tick, setTick] = useState(0);
  const wsRef = useRef(null);
  const intentoRef = useRef(0);

  useEffect(() => {
    let detenido = false;

    const conectar = () => {
      const ws = new WebSocket(URL_WS());
      wsRef.current = ws;

      ws.onopen = () => {
        console.log("WebSocket conectado");
        intentoRef.current = 0;
        ws.send(JSON.stringify({ accion: "get_estado" }));
      };

      ws.onmessage = (evt) => {
        try {
          const msg = JSON.parse(evt.data);
          if (msg.type === "estado") {
            setEstado(prev => ({ ...prev, ...msg.estado }));
            if (typeof msg.tick !== "undefined") setTick(msg.tick);
          }
        } catch (err) {
          console.error("Error parseando mensaje WebSocket:", err);
        }
      };

      ws.onclose = () => {
        console.log("WebSocket cerrado. Intentando reconectar...");
        if (detenido) return;
        intentoRef.current = Math.min(10, intentoRef.current + 1);
        const espera = Math.min(5000, 500 * 2 ** intentoRef.current);
        setTimeout(() => {
          if (!detenido) conectar();
        }, espera);
      };

      ws.onerror = (e) => {
        console.error("Error WebSocket:", e);
        try { ws.close(); } catch (_) {}
      };
    };

    conectar();

    return () => {
      detenido = true;
      try { wsRef.current?.close(); } catch (_) {}
    };
  }, []);

  return (
    <div style={{ padding: 20, fontFamily: "Arial, sans-serif" }}>
      <h2>Simulación: 4 Semáforos (tick {tick})</h2>
      <div style={{ display: "flex", gap: 20 }}>
        <Semaforo id="S1" color={estado.S1} />
        <Semaforo id="S2" color={estado.S2} />
        <Semaforo id="S3" color={estado.S3} />
        <Semaforo id="S4" color={estado.S4} />
      </div>
    </div>
  );
}
