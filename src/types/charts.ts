export interface DataPoint {
  label: string
  value: number
}

export interface ChartDataset {
  label: string
  data: number[]
  color?: string
}

export interface BarChartProps {
  datos: DataPoint[]
  titulo: string
  descripcion?: string
  id?: string
}

export interface PieChartProps {
  datos: DataPoint[]
  titulo: string
  descripcion?: string
  id?: string
}

export interface GroupedBarChartProps {
  labels: string[]
  datasets: ChartDataset[]
  titulo: string
  id?: string
}

export interface HeatmapChartProps {
  xLabels: string[]
  yLabels: string[]
  data: number[][]
  titulo: string
  descripcion?: string
  id?: string
}

export interface LineChartProps {
  anios: string[]
  datasets: Omit<ChartDataset, 'color'>[]
  titulo: string
}

export interface GroupedBarChartData {
  labels: string[]
  datasets: { label: string; data: number[]; color: string }[]
}
