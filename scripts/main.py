import pandas as pd
import json
import os
from collections import Counter

# Configuración
BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_ESTUDIANTES = os.path.join(BASE, "mock/estudiantes.csv")
RUTA_EGRESADOS = os.path.join(BASE, "mock/egresados.csv")
CARPETA_JSON = os.path.join(BASE, "json_data")

os.makedirs(CARPETA_JSON, exist_ok=True)

# ===== 1. Carga y limpieza básica =====
df_est = pd.read_csv(RUTA_ESTUDIANTES)
df_egr = pd.read_csv(RUTA_EGRESADOS)

# Limpieza común: strip espacios, normalizar texto
for col in df_est.columns:
    if df_est[col].dtype == object:
        df_est[col] = df_est[col].str.strip()
for col in df_egr.columns:
    if df_egr[col].dtype == object:
        df_egr[col] = df_egr[col].str.strip()

# Convertir listas separadas por coma en listas reales para preguntas múltiples
def parse_lista(cadena):
    if pd.isna(cadena) or cadena.strip() == '':
        return []
    items = [x.strip() for x in cadena.split(',')]
    return [x for x in items if x != '']

df_est['lenguajes_lista'] = df_est['lenguajes'].apply(parse_lista)
df_est['frameworks_lista'] = df_est['frameworks'].apply(parse_lista)
df_est['herramientas_lista'] = df_est['herramientas'].apply(parse_lista)

df_egr['lenguajes_lista'] = df_egr['lenguajes'].apply(parse_lista)
df_egr['frameworks_lista'] = df_egr['frameworks'].apply(parse_lista)
df_egr['herramientas_lista'] = df_egr['herramientas'].apply(parse_lista)

# ===== 2. Funciones auxiliares para generar JSON =====
def guardar_json(nombre, datos):
    with open(os.path.join(CARPETA_JSON, f"{nombre}.json"), "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    print(f"✓ {nombre}.json guardado")

def frecuencia_unica(serie, orden=None):
    conteo = serie.value_counts().to_dict()
    if orden:
        labels = [c for c in orden if c in conteo]
        values = [conteo.get(c, 0) for c in labels]
    else:
        labels = list(conteo.keys())
        values = list(conteo.values())
    return {"labels": labels, "values": values}

def frecuencia_multi(serie_lista, top=15):
    contador = Counter()
    for lista in serie_lista:
        contador.update(lista)
    mas_comunes = contador.most_common(top)
    return {"labels": [x[0] for x in mas_comunes], "values": [x[1] for x in mas_comunes]}

# ===== 3. Gráficos individuales (univariados) =====

# --- Estudiantes ---
guardar_json("est_area_aspirada", frecuencia_unica(df_est['area_aspirada']))
guardar_json("est_meta_graduacion", frecuencia_unica(df_est['meta_graduacion']))
guardar_json("est_frecuencia_ia", frecuencia_unica(df_est['frecuencia_ia'],
    orden=["Nunca", "Rara vez", "Ocasionalmente", "Diariamente"]))
guardar_json("est_impacto_ia", frecuencia_unica(df_est['impacto_ia']))
guardar_json("est_horas_autonomas", frecuencia_unica(df_est['horas_autonomas'],
    orden=["0 horas", "De 1 a 5 horas", "De 6 a 10 horas", "Más de 10 horas"]))
guardar_json("est_factor_empleo", frecuencia_unica(df_est['factor_empleo']))

guardar_json("est_lenguajes", frecuencia_multi(df_est['lenguajes_lista']))
guardar_json("est_frameworks", frecuencia_multi(df_est['frameworks_lista']))
guardar_json("est_herramientas", frecuencia_multi(df_est['herramientas_lista']))

# --- Egresados ---
guardar_json("egr_anios_egresado", frecuencia_unica(df_egr['anios_egresado']))
guardar_json("egr_rol_actual", frecuencia_unica(df_egr['rol_actual']))
guardar_json("egr_tiempo_empleo", frecuencia_unica(df_egr['tiempo_empleo']))
guardar_json("egr_nivel_ingles", frecuencia_unica(df_egr['nivel_ingles'],
    orden=["No se requiere","Básico","Intermedio","Avanzado","Fluido / Nativo"]))
guardar_json("egr_frecuencia_ia", frecuencia_unica(df_egr['frecuencia_ia']))
guardar_json("egr_impacto_ia", frecuencia_unica(df_egr['impacto_ia']))
guardar_json("egr_factor_contratacion", frecuencia_unica(df_egr['factor_contratacion']))
guardar_json("egr_ingresos", frecuencia_unica(df_egr['ingresos'],
    orden=["500-1000", "1001-2000", "2001-4000", "Más de 4000"]))

guardar_json("egr_lenguajes", frecuencia_multi(df_egr['lenguajes_lista']))
guardar_json("egr_frameworks", frecuencia_multi(df_egr['frameworks_lista']))
guardar_json("egr_herramientas", frecuencia_multi(df_egr['herramientas_lista']))

# ===== 4. Comparativas Estudiantes vs Egresados =====
# Aseguramos mismos labels para ambos grupos en preguntas equivalentes
def comparar_frecuencias(serie_est, serie_egr, labels_comunes, nombre_archivo):
    conteo_est = serie_est.value_counts()
    conteo_egr = serie_egr.value_counts()
    data_est = [int(conteo_est.get(l, 0)) for l in labels_comunes]
    data_egr = [int(conteo_egr.get(l, 0)) for l in labels_comunes]
    json_data = {
        "labels": labels_comunes,
        "dataset1": {"label": "Estudiantes", "data": data_est, "color": "#3B82F6"},
        "dataset2": {"label": "Egresados", "data": data_egr, "color": "#F59E0B"}
    }
    guardar_json(nombre_archivo, json_data)

# Área aspirada vs Rol actual (mapear categorías equivalentes)
areas_orden = [
    "Desarrollo Web Frontend", "Desarrollo Web Backend", "Desarrollo Web Fullstack",
    "Ciencia de Datos / Analítica", "Desarrollo de IA", "Ciberseguridad",
    "Redes / Infraestructura", "DevOps / Cloud", "Gestión de Proyectos",
    "No lo sé aún"
]
df_est['area_norm'] = df_est['area_aspirada']
df_egr['rol_norm'] = df_egr['rol_actual']

comparar_frecuencias(df_est['area_norm'], df_egr['rol_norm'], areas_orden, "comp_area")

freq_orden = ["Nunca", "Rara vez", "Ocasionalmente", "Diariamente"]
comparar_frecuencias(df_est['frecuencia_ia'], df_egr['frecuencia_ia'], freq_orden, "comp_frecuencia_ia")

# Impacto IA
impacto_orden = [
    "Reemplazará gran parte del trabajo humano",
    "Será una herramienta obligatoria",
    "Tendrá un impacto menor",
    "No estoy seguro"
]
comparar_frecuencias(df_est['impacto_ia'], df_egr['impacto_ia'], impacto_orden, "comp_impacto_ia")

# Tecnologías (multi): combinamos listas y comparamos
lenguajes_comunes = ["JavaScript / TypeScript","Python","Java","C++","C","Go","SQL","Ninguno","No utilizo lenguajes de programación en mi rol actual"]
def comparar_multi(serie_est_listas, serie_egr_listas, items, nombre):
    cont_est = Counter()
    for lst in serie_est_listas: cont_est.update(lst)
    cont_egr = Counter()
    for lst in serie_egr_listas: cont_egr.update(lst)
    data_est = [cont_est.get(item,0) for item in items]
    data_egr = [cont_egr.get(item,0) for item in items]
    guardar_json(nombre, {
        "labels": items,
        "dataset1": {"label": "Estudiantes", "data": data_est, "color": "#3B82F6"},
        "dataset2": {"label": "Egresados", "data": data_egr, "color": "#F59E0B"}
    })

comparar_multi(df_est['lenguajes_lista'], df_egr['lenguajes_lista'], lenguajes_comunes, "comp_lenguajes")
comparar_multi(df_est['frameworks_lista'], df_egr['frameworks_lista'],
    ["React / Next.js","Angular","Node.js","Spring Boot","Django / FastAPI","Django","FastAPI","React","Ninguno"],
    "comp_frameworks")
comparar_multi(df_est['herramientas_lista'], df_egr['herramientas_lista'],
    ["Git","GitHub","GitLab","Docker","Kubernetes","AWS","Azure","Google Cloud","Linux","Jenkins","GitHub Actions","Jira","Trello","Scrum","Ninguna"],
    "comp_herramientas")

# ===== 5. Tablas de calor (co-ocurrencia) =====
def coocurrencia(serie_l1, serie_l2, items1, items2, nombre):
    matriz = []
    for i in items1:
        fila = []
        for j in items2:
            conteo = 0
            for lst1, lst2 in zip(serie_l1, serie_l2):
                if i in lst1 and j in lst2:
                    conteo += 1
            fila.append(conteo)
        matriz.append(fila)
    guardar_json(nombre, {
        "title": "Co‑ocurrencia Lenguajes / Frameworks",
        "xLabels": items2,
        "yLabels": items1,
        "data": matriz
    })

lengs = ["JavaScript / TypeScript","Python","Java","C","C++","Go","SQL"]
frameworks = ["React / Next.js","Angular","Node.js","Spring Boot","Django / FastAPI","React","Django"]
coocurrencia(df_est['lenguajes_lista'], df_est['frameworks_lista'], lengs, frameworks, "heatmap_lenguajes_frameworks")

print("Todos los JSON generados en la carpeta 'graficos_json'.")
