import type { DataPoint } from './charts'

export interface LabelValueData {
  labels: string[]
  values: number[]
}

export interface HeatmapRawData {
  xLabels: string[]
  yLabels: string[]
  data: number[][]
  title: string
}

export interface ComparativeDataset {
  label: string
  data: number[]
  color: string
}

export interface ComparativeRawData {
  labels: string[]
  datasets: ComparativeDataset[]
}

export interface GraduateInsights {
  total: number
  top_lenguajes: DataPoint[]
  top_frameworks: DataPoint[]
  top_rol: DataPoint[]
  top_factor_seleccion: DataPoint[]
  top_tiempo_empleo: DataPoint[]
  top_nivel_ingles: DataPoint[]
  frecuencia_ia: DataPoint[]
  impacto_ia: DataPoint[]
  trabaja_sector_pct: number
  usa_ia_diario_pct: number
}

export interface StudentInsights {
  estudiantes: {
    total: number
    top_lenguajes: DataPoint[]
    top_frameworks: DataPoint[]
    top_areas: DataPoint[]
    distribucion_horas: DataPoint[]
    factor_empleo: DataPoint[]
    impacto_ia: DataPoint[]
    frecuencia_ia: DataPoint[]
    meta_graduacion: DataPoint[]
    uso_diario_ia_pct: number
    impacto_positivo_ia_pct: number
  }
  egresados: GraduateInsights
}

export interface StudentSectionData {
  semestre: LabelValueData
  lenguajes: LabelValueData
  frameworks: LabelValueData
  areaAspirada: LabelValueData
  horasAutonomas: LabelValueData
  factorEmpleo: LabelValueData
  impactoIa: LabelValueData
  metaGraduacion: LabelValueData
  frecuenciaIa: LabelValueData
  heatmap: HeatmapRawData
}

export interface GraduateSectionData {
  rol: LabelValueData
  lenguajes: LabelValueData
  frameworks: LabelValueData
  tiempoEmpleo: LabelValueData
  trabajaSector: LabelValueData
  nivelIngles: LabelValueData
  frecuenciaIa: LabelValueData
  impactoIa: LabelValueData
  factorSeleccion: LabelValueData
}

export interface ComparativeSectionData {
  lenguajes: ComparativeRawData
  frameworks: ComparativeRawData
  frecuenciaIa: ComparativeRawData
}

export interface AllSurveyData {
  estLenguajes: LabelValueData
  estFrameworks: LabelValueData
  estAreaAspirada: LabelValueData
  estFactorEmpleo: LabelValueData
  estFrecuenciaIa: LabelValueData
  estHorasAutonomas: LabelValueData
  estImpactoIa: LabelValueData
  estMetaGraduacion: LabelValueData
  estSemestre: LabelValueData
  heatmap: HeatmapRawData
  insights: StudentInsights
  gradAnosGraduacion: LabelValueData
  gradTrabajaSector: LabelValueData
  gradRol: LabelValueData
  gradTiempoEmpleo: LabelValueData
  gradNivelIngles: LabelValueData
  gradFrecuenciaIa: LabelValueData
  gradImpactoIa: LabelValueData
  gradFactorSeleccion: LabelValueData
  gradLenguajes: LabelValueData
  gradFrameworks: LabelValueData
  compLenguajes: ComparativeRawData
  compFrameworks: ComparativeRawData
  compFrecuenciaIa: ComparativeRawData
}
