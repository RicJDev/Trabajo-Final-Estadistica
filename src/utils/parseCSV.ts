import { resolve } from 'node:path'
import { readFileSync } from 'node:fs'

export function parseCSV(filePath: string) {
  const content = readFileSync(resolve(filePath), 'utf-8')
  const lines = content.trim().split('\n')
  const headers = lines[0].split(',').map((h) => h.trim())

  return lines.slice(1).map((line) => {
    const values = line.split(',')
    const row: Record<string, string> = {}

    headers.forEach((h, i) => {
      row[h] = values[i]?.trim()
    })

    return row
  })
}
