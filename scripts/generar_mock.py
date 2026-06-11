import csv
import random
import os

random.seed(42)

# === Categorías exactas de los CSVs existentes ===

EST_SEMESTRES = [str(i) for i in range(1, 11)]
EST_SEMESTRES_PESOS = [3, 3, 2.5, 2, 2, 1.5, 1.5, 1, 1, 0.5]

EST_AREA_ASPIRADA = [
    "Desarrollo Web Frontend",
    "Desarrollo Web Backend",
    "Desarrollo Web Fullstack",
    "Ciencia de Datos / Analítica",
    "Desarrollo de IA",
    "Ciberseguridad",
    "Redes / Infraestructura",
    "DevOps / Cloud",
    "Gestión de Proyectos",
    "No lo sé aún",
]
EST_AREA_ASPIRADA_PESOS = [2, 2, 1.5, 2, 1.5, 1, 1, 1.5, 1, 1]

EST_META_GRADUACION = [
    "Trabajar en empresa local",
    "Trabajar de forma remota",
    "Emprender",
    "No lo sé aún",
]
EST_META_PESOS = [3, 3, 1.5, 1]

EST_FRECUENCIA_IA = ["Nunca", "Rara vez", "Ocasionalmente", "Diariamente"]
EST_FRECUENCIA_IA_PESOS = [0.5, 1, 2.5, 4]

EST_IMPACTO_IA = [
    "Será una herramienta obligatoria",
    "Reemplazará gran parte del trabajo humano",
    "No estoy seguro",
    "Tendrá un impacto menor",
]
EST_IMPACTO_IA_PESOS = [4, 2, 1, 1]

EST_HORAS_AUTONOMAS = ["0 horas", "De 1 a 5 horas", "De 6 a 10 horas", "Más de 10 horas"]
EST_HORAS_AUTONOMAS_PESOS = [1, 3, 2.5, 1.5]

EST_FACTOR_EMPLEO = [
    "Portafolio",
    "El título universitario",
    "Certificaciones externas",
    "Inglés y habilidades blandas",
    "Mi portafolio de proyectos",
]
EST_FACTOR_EMPLEO_PESOS = [3, 2, 2, 2, 1]

EST_LENGUAJES_OPTS = [
    "JavaScript / TypeScript",
    "Python",
    "Java",
    "SQL",
    "C++",
    "C",
    "Go",
]
EST_FRAMEWORKS_OPTS = [
    "React / Next.js",
    "Node.js",
    "Django / FastAPI",
    "Spring Boot",
    "Angular",
    "React",
    "Django",
]
EST_HERRAMIENTAS_OPTS = [
    "Git",
    "GitHub",
    "Docker",
    "Linux",
    "AWS",
    "Jira",
    "Kubernetes",
    "GitHub Actions",
    "Scrum",
]

# === Egresados ===

EGR_ANIOS = ["Menos de 1 año", "1-3 años", "4-6 años", "Más de 6 años"]
EGR_ANIOS_PESOS = [2, 3, 2, 1]

EGR_TRABAJA = ["Sí", "No"]
EGR_TRABAJA_PESOS = [8, 1]

EGR_ROL = [
    "Desarrollo Web Frontend",
    "Desarrollo Web Backend",
    "Desarrollo Web Fullstack",
    "Ciencia de Datos / Analítica",
    "Desarrollo de IA",
    "Ciberseguridad",
    "Redes / Infraestructura",
    "DevOps / Cloud",
    "Gestión de Proyectos",
]
EGR_ROL_PESOS = [1.5, 2, 1.5, 1.5, 1, 0.5, 0.5, 1.5, 1]

EGR_TIEMPO_EMPLEO = [
    "Ya trabajaba antes de graduarme",
    "Menos de 3 meses",
    "3-6 meses",
    "Más de un año",
]
EGR_TIEMPO_PESOS = [2, 3, 2, 1]

EGR_NIVEL_INGLES = ["Básico", "Intermedio", "Avanzado", "Fluido / Nativo"]
EGR_NIVEL_INGLES_PESOS = [1, 3, 3, 1.5]

EGR_FRECUENCIA_IA = ["Nunca", "Ocasionalmente", "Diariamente"]
EGR_FRECUENCIA_IA_PESOS = [0.5, 2, 4]

EGR_IMPACTO_IA = [
    "Me permite resolver más rápido",
    "Me permite asumir tareas más complejas",
    "No ha tenido impacto significativo",
    "Tendrá un impacto menor",
]
EGR_IMPACTO_IA_PESOS = [4, 3, 1, 0.5]

EGR_FACTOR_CONTRATACION = [
    "Portafolio",
    "Experiencia / Portafolio",
    "Pruebas técnicas",
    "Inglés y habilidades blandas",
    "Certificaciones externas",
]
EGR_FACTOR_PESOS = [2, 2.5, 2, 1.5, 1]

EGR_INGRESOS = ["500-1000", "1001-2000", "2001-4000", "Más de 4000"]
EGR_INGRESOS_PESOS = [2, 3, 2, 1]

EGR_LENGUAJES_OPTS = [
    "JavaScript / TypeScript",
    "Python",
    "Java",
    "SQL",
    "Go",
    "C",
    "C++",
]
EGR_FRAMEWORKS_OPTS = [
    "React / Next.js",
    "Node.js",
    "Django / FastAPI",
    "Spring Boot",
    "Angular",
    "React",
    "FastAPI",
]
EGR_HERRAMIENTAS_OPTS = [
    "Git",
    "GitHub",
    "Docker",
    "Linux",
    "AWS",
    "Jira",
    "Kubernetes",
    "GitHub Actions",
    "Terraform",
    "Scrum",
    "Confluence",
    "Cisco",
]


def elegir(vals, pesos=None, k=1):
    if pesos:
        return random.choices(vals, weights=pesos, k=k)
    return random.choices(vals, k=k)


def elegir_multi(opts, max_n=3, none_val="Ninguno"):
    pesos = [1, 2, 3, 1.5] + [1] * (max_n - 3)
    n = random.choices(range(0, max_n + 1), weights=pesos[: max_n + 1])[0]
    if n == 0:
        return none_val
    return ",".join(sorted(random.sample(opts, k=min(n, len(opts)))))


def generar_estudiante():
    return {
        "semestre": elegir(EST_SEMESTRES, EST_SEMESTRES_PESOS)[0],
        "area_aspirada": elegir(EST_AREA_ASPIRADA, EST_AREA_ASPIRADA_PESOS)[0],
        "meta_graduacion": elegir(EST_META_GRADUACION, EST_META_PESOS)[0],
        "frecuencia_ia": elegir(EST_FRECUENCIA_IA, EST_FRECUENCIA_IA_PESOS)[0],
        "impacto_ia": elegir(EST_IMPACTO_IA, EST_IMPACTO_IA_PESOS)[0],
        "horas_autonomas": elegir(EST_HORAS_AUTONOMAS, EST_HORAS_AUTONOMAS_PESOS)[0],
        "factor_empleo": elegir(EST_FACTOR_EMPLEO, EST_FACTOR_EMPLEO_PESOS)[0],
        "lenguajes": elegir_multi(EST_LENGUAJES_OPTS, none_val="Ninguno"),
        "frameworks": elegir_multi(EST_FRAMEWORKS_OPTS, none_val="Ninguno"),
        "herramientas": elegir_multi(
            EST_HERRAMIENTAS_OPTS, max_n=4, none_val="Ninguna"
        ),
    }


def generar_egresado():
    trabaja = elegir(EGR_TRABAJA, EGR_TRABAJA_PESOS)[0]
    return {
        "anios_egresado": elegir(EGR_ANIOS, EGR_ANIOS_PESOS)[0],
        "trabaja_en_sector": trabaja,
        "rol_actual": (
            elegir(EGR_ROL, EGR_ROL_PESOS)[0] if trabaja == "Sí" else ""
        ),
        "tiempo_empleo": elegir(EGR_TIEMPO_EMPLEO, EGR_TIEMPO_PESOS)[0],
        "nivel_ingles": elegir(EGR_NIVEL_INGLES, EGR_NIVEL_INGLES_PESOS)[0],
        "frecuencia_ia": elegir(EGR_FRECUENCIA_IA, EGR_FRECUENCIA_IA_PESOS)[0],
        "impacto_ia": elegir(EGR_IMPACTO_IA, EGR_IMPACTO_IA_PESOS)[0],
        "factor_contratacion": elegir(EGR_FACTOR_CONTRATACION, EGR_FACTOR_PESOS)[0],
        "ingresos": elegir(EGR_INGRESOS, EGR_INGRESOS_PESOS)[0],
        "lenguajes": elegir_multi(EGR_LENGUAJES_OPTS, none_val="No utilizo lenguajes de programación en mi rol actual"),
        "frameworks": elegir_multi(EGR_FRAMEWORKS_OPTS, none_val="Ninguno"),
        "herramientas": elegir_multi(
            EGR_HERRAMIENTAS_OPTS, max_n=4, none_val="Ninguna"
        ),
    }


def agregar_filas(ruta, columnas, generador, n):
    filas_existentes = 0
    if os.path.exists(ruta):
        with open(ruta, newline="") as f:
            filas_existentes = sum(1 for _ in f) - 1
    with open(ruta, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columnas)
        for _ in range(n):
            writer.writerow(generador())
    print(
        f"✓ {ruta}: {filas_existentes} → {filas_existentes + n} filas"
    )


COLUMNAS_EST = [
    "semestre",
    "area_aspirada",
    "meta_graduacion",
    "frecuencia_ia",
    "impacto_ia",
    "horas_autonomas",
    "factor_empleo",
    "lenguajes",
    "frameworks",
    "herramientas",
]

COLUMNAS_EGR = [
    "anios_egresado",
    "trabaja_en_sector",
    "rol_actual",
    "tiempo_empleo",
    "nivel_ingles",
    "frecuencia_ia",
    "impacto_ia",
    "factor_contratacion",
    "ingresos",
    "lenguajes",
    "frameworks",
    "herramientas",
]

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    agregar_filas("mock/estudiantes.csv", COLUMNAS_EST, generar_estudiante, 200)
    agregar_filas("mock/egresados.csv", COLUMNAS_EGR, generar_egresado, 200)
    print("Listo.")
