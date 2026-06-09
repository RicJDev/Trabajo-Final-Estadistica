import fs from 'node:fs'
import path from 'node:path'

const CSV_PATH = path.resolve('public/data/respuestas.csv')

export function parseCSV() {
  const content = fs.readFileSync(CSV_PATH, 'utf-8')
  const lines = content.trim().split('\n')
  const headers = lines[0].split(',').map((h) => h.trim())
  return lines.slice(1).map((line) => {
    const values = line.split(',')
    const row = {}
    headers.forEach((h, i) => {
      row[h] = values[i]?.trim()
    })
    return row
  })
}

function contarRespuestas(rows, columna) {
  const conteo = {}
  for (const row of rows) {
    const val = row[columna]
    conteo[val] = (conteo[val] || 0) + 1
  }
  return Object.entries(conteo)
    .map(([label, value]) => ({ label, value }))
    .sort((a, b) => b.value - a.value)
}

function promedio(rows, columna) {
  const nums = rows.map((r) => Number(r[columna])).filter((n) => !isNaN(n))
  return nums.length ? nums.reduce((a, b) => a + b, 0) / nums.length : 0
}

export function resumenGeneral() {
  const rows = parseCSV()
  return {
    total: rows.length,
    satisfaccionGeneral: contarRespuestas(rows, 'satisfaccion_general'),
    calidadDocente: contarRespuestas(rows, 'calidad_docente'),
    instalaciones: contarRespuestas(rows, 'instalaciones'),
    contenidoCurricular: contarRespuestas(rows, 'contenido_curricular'),
    soporteTecnologico: contarRespuestas(rows, 'soporte_tecnologico'),
    planesFuturo: contarRespuestas(rows, 'plan_futuro'),
    horasEstudio: contarRespuestas(rows, 'horas_estudio'),
    porAnio: rows.reduce((acc, row) => {
      const anio = row.anio
      if (!acc[anio]) acc[anio] = []
      acc[anio].push(row)
      return acc
    }, {}),
  }
}

export function satisfaccionPorAnio() {
  const rows = parseCSV()
  const anios = [...new Set(rows.map((r) => r.anio))].sort()
  const categorias = [
    'satisfaccion_general',
    'calidad_docente',
    'instalaciones',
    'contenido_curricular',
    'soporte_tecnologico',
  ]
  const etiquetas = {
    satisfaccion_general: 'Satisfacción general',
    calidad_docente: 'Calidad docente',
    instalaciones: 'Instalaciones',
    contenido_curricular: 'Contenido curricular',
    soporte_tecnologico: 'Soporte tecnológico',
  }
  return {
    anios,
    datasets: categorias.map((cat) => ({
      label: etiquetas[cat],
      data: anios.map((a) =>
        promedio(
          rows.filter((r) => r.anio === a),
          cat,
        ),
      ),
    })),
  }
}

export function promedioGeneral() {
  const rows = parseCSV()
  const categorias = [
    'satisfaccion_general',
    'calidad_docente',
    'instalaciones',
    'contenido_curricular',
    'soporte_tecnologico',
  ]
  const etiquetas = {
    satisfaccion_general: 'Satisfacción general',
    calidad_docente: 'Calidad docente',
    instalaciones: 'Instalaciones',
    contenido_curricular: 'Contenido curricular',
    soporte_tecnologico: 'Soporte tecnológico',
  }
  return categorias.map((cat) => ({
    label: etiquetas[cat],
    value: Math.round(promedio(rows, cat) * 100) / 100,
  }))
}
