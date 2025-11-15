import React from "react";

export default function Semaforo({ id, color }) {
  const estiloCirculo = (activo) => ({
    width: 36,
    height: 36,
    borderRadius: "50%",
    display: "block",
    margin: "6px auto",
    boxShadow: activo ? "0 0 8px rgba(0,0,0,0.3)" : "none"
  });

  const colorAProp = (col) => {
    if (col === "green") return "green";
    if (col === "yellow") return "goldenrod";
    if (col === "red") return "crimson";
    return undefined;
  };

  return (
    <div style={{ width: 120, textAlign: "center", padding: 10, border: "1px solid #ddd", borderRadius: 8 }}>
      <div style={{ fontWeight: "bold", marginBottom: 8 }}>{id}</div>
      <div style={{ background: "#222", padding: 10, borderRadius: 8 }}>
        <div style={{ ...estiloCirculo(color === "red"), backgroundColor: color === "red" ? colorAProp("red") : "#333" }} />
        <div style={{ ...estiloCirculo(color === "yellow"), backgroundColor: color === "yellow" ? colorAProp("yellow") : "#333" }} />
        <div style={{ ...estiloCirculo(color === "green"), backgroundColor: color === "green" ? colorAProp("green") : "#333" }} />
      </div>
      <div style={{ marginTop: 8 }}>{color}</div>
    </div>
  );
}
