import numpy as np
import json
from datetime import datetime

DIM = 50
CYCLE_COUNT = 0


def calculate_entropy(field, r, c):
    sub = field[max(0, r - 1):min(DIM, r + 2), max(0, c - 1):min(DIM, c + 2)]
    avg = np.mean(sub)
    variance = np.mean((sub - avg) ** 2)
    return variance


def diffuse_step(field, alpha=0.05):
    next_field = np.copy(field)
    for r in range(DIM):
        for c in range(DIM):
            sub = field[max(0, r - 1):min(DIM, r + 2), max(0, c - 1):min(DIM, c + 2)]
            avg = np.mean(sub)
            next_field[r, c] += alpha * (avg - field[r, c])
    return next_field


def inject_pattern(field, pattern, x=21, y=21):
    h, w = pattern.shape
    field[y:y+h, x:x+w] = pattern
    return field


def generate_anxiety_pattern():
    return np.random.rand(7, 7)


def generate_calm_pattern():
    return np.array([[0.5 + 0.1 * np.sin((r + c) / 2) for c in range(7)] for r in range(7)])


def export_output(field, last_pattern="none"):
    flat = field.flatten()
    avg = np.mean(flat)
    varianza = np.var(flat)
    max_entropia = -1
    pos_max = (0, 0)
    for r in range(DIM):
        for c in range(DIM):
            e = calculate_entropy(field, r, c)
            if e > max_entropia:
                max_entropia = e
                pos_max = (r, c)

    output = {
        "timestamp": datetime.utcnow().isoformat(),
        "patron_inyectado": last_pattern,
        "modo_inyeccion": "reemplazar",
        "zona_afectada": {"x": 21, "y": 21, "ancho": 7, "alto": 7},
        "entropia_global": float(varianza),
        "max_entropia": {
            "valor": float(max_entropia),
            "posicion": {"x": pos_max[1], "y": pos_max[0]}
        },
        "promedio_global": float(avg),
        "tiempo_disolucion_estimado": f"{max(10, 25 - int(varianza * 10000))} ciclos",
        "resonancia_detectada": bool(varianza > 0.006),
        "exportado_como_audio": "no",
        "notas": f"Respuesta al patrón '{last_pattern}'."
    }
    return output


def run_simulation(pattern_func, label, steps=25):
    field = np.random.uniform(0.4, 0.6, (DIM, DIM))
    pattern = pattern_func()
    field = inject_pattern(field, pattern)
    for _ in range(steps):
        field = diffuse_step(field)
    return export_output(field, last_pattern=label)


if __name__ == "__main__":
    print("\n--- Comparativa de patrones: Ansiedad vs. Calma ---\n")

    result_anxiety = run_simulation(generate_anxiety_pattern, "ansiedad")
    result_calm = run_simulation(generate_calm_pattern, "calma")

    print("\n--- Resultado: Ansiedad ---")
    print(json.dumps(result_anxiety, indent=2))

    print("\n--- Resultado: Calma ---")
    print(json.dumps(result_calm, indent=2))
