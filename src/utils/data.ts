import fs from 'node:fs'
import path from 'node:path'
import type { DataPoint, LabelValueData } from '../types'

const DATA_DIR = path.resolve('public/json_data')

function loadJSON<T>(filename: string): T {
  return JSON.parse(fs.readFileSync(path.join(DATA_DIR, filename), 'utf-8')) as T
}

function toEntries(data: LabelValueData): DataPoint[]
function toEntries(labels: string[], values: number[]): DataPoint[]
function toEntries(labelsOrData: string[] | LabelValueData, values?: number[]): DataPoint[] {
  if (Array.isArray(labelsOrData)) {
    return labelsOrData.map((label, i) => ({ label, value: values![i] }))
  }
  return labelsOrData.labels.map((label, i) => ({ label, value: labelsOrData.values[i] }))
}

function groupSinglesAsOther(data: LabelValueData): DataPoint[] {
  const main = data.labels.map((label, i) => ({ label, value: data.values[i] })).filter((e) => e.value > 1)
  const otherCount = data.values.reduce((sum, v) => (v === 1 ? sum + v : sum), 0)
  if (otherCount > 0) main.push({ label: 'Otra', value: otherCount })
  return main
}

export { loadJSON, toEntries, groupSinglesAsOther }
