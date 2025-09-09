# Empresa → Gerencias → Trabajadores → Propiedades
empresa = {
    "nombre": "Tech Perú S.A.C.",
    "gerencias": {
        "Marketing": {
            "trabajadores": {
                "MKT-001": {"nombre": "Ana Ruiz",  "edad": 28, "profesion": "Comunicadora"},
                "MKT-002": {"nombre": "Luis Peña", "edad": 31, "profesion": "Diseñador"},
            }
        },
        "Contabilidad": {
            "trabajadores": {
                "ACC-001": {"nombre": "María Torres", "edad": 35, "profesion": "Contadora"},
            }
        },
        "Operaciones": {
            "trabajadores": {
                "OPS-001": {"nombre": "Jorge Silva", "edad": 40, "profesion": "Ingeniero"},
            }
        },
    }
}

# ===== Lecturas puntuales =====
print(f"La empresa {empresa["nombre"]} se presenta con el jefe del area de marketing {empresa['gerencias']['Marketing']["trabajadores"]["MKT-001"]["nombre"]}")
print("Nombre de MKT-001:", empresa["gerencias"]["Marketing"]["trabajadores"]["MKT-001"]["nombre"])
print("Profesión de ACC-001:", empresa["gerencias"]["Contabilidad"]["trabajadores"]["ACC-001"]["profesion"])

# ===== Agregar un trabajador (directo en el dict) =====
empresa["gerencias"]["Contabilidad"]["trabajadores"]["ACC-002"] = {
    "nombre": "Diego López", "edad": 27, "profesion": "Asistente Contable"
}

# ===== Actualizar un dato =====
empresa["gerencias"]["Marketing"]["trabajadores"]["MKT-002"]["profesion"] = "Ilustrador"

# ===== Eliminar un trabajador =====
del empresa["gerencias"]["Operaciones"]["trabajadores"]["OPS-001"]

# ===== Listar todos (gerencia, ID, nombre, profesión) =====
print("\nListado general:")
for gerencia, gdata in empresa["gerencias"].items():
    for tid, tdata in gdata["trabajadores"].items():
        print(f"- {gerencia} | {tid} | {tdata['nombre']} ({tdata['profesion']}, {tdata['edad']} años)")

# ===== Pequeño “kpi” de conteo por gerencia (solo diccionarios/comprensiones) =====
conteo_por_gerencia = {
    ger: len(gdata["trabajadores"])
    for ger, gdata in empresa["gerencias"].items()
}
print("\nTrabajadores por gerencia:", conteo_por_gerencia)