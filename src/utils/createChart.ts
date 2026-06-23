import {
  Chart,
  BarController,
  BarElement,
  DoughnutController,
  ArcElement,
  LineController,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from 'chart.js'

Chart.register(
  BarController,
  BarElement,
  DoughnutController,
  ArcElement,
  LineController,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
)

const COLOR_PALETTE = [
  '#3b82f6', //
  '#10b981',
  '#f59e0b',
  '#ef4444',
  '#8b5cf6',
  '#ec4899',
  '#14b8a6',
  '#f97316',
]

const COLORS_BY_NIVEL = {
  1: '#93c5fd',
  2: '#60a5fa',
  3: '#3b82f6',
  4: '#2563eb',
  5: '#1d4ed8',
}

function truncateLabel(text: string, max = 30): string {
  return text.length > max ? text.slice(0, max) + '…' : text
}

export function createBarChart(canvas: HTMLCanvasElement, data: Record<string, string>[], title: string) {
  Chart.getChart(canvas)?.destroy()
  return new Chart(canvas, {
    type: 'bar',
    data: {
      labels: data.map((d) => d.label),
      datasets: [
        {
          label: title,
          data: data.map((d) => d.value),
          backgroundColor: COLOR_PALETTE.slice(0, data.length),
          borderRadius: 6,
          barPercentage: 0.65,
          categoryPercentage: 0.85,
        },
      ],
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.parsed.x} respuestas`,
          },
        },
      },
      scales: {
        x: {
          beginAtZero: true,
          ticks: { stepSize: 1 },
        },
        y: {
          ticks: {
            autoSkip: false,
            callback(_value, _index, _ticks) {
              return truncateLabel(this.chart.data.labels[_index] as string)
            },
          },
        },
      },
    },
  })
}

export function createPieChart(canvas: HTMLCanvasElement, data: Record<string, string>[], title: string) {
  return new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels: data.map((d) => d.label),
      datasets: [
        {
          data: data.map((d) => d.value),
          backgroundColor: COLOR_PALETTE.slice(0, data.length),
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              const total = ctx.dataset.data.reduce((a, b) => a + b, 0)
              const pct = ((ctx.parsed / total) * 100).toFixed(1)
              return `${ctx.label}: ${ctx.parsed} (${pct}%)`
            },
          },
        },
      },
    },
  })
}

export function createLineChart(canvas: HTMLCanvasElement, data: any[]) {
  return new Chart(canvas, {
    type: 'line',
    data: {
      // labels: datos.anios,
      datasets: data.datasets.map((ds, i) => ({
        ...ds,
        borderColor: COLOR_PALETTE[i % COLOR_PALETTE.length],
        backgroundColor: COLOR_PALETTE[i % COLOR_PALETTE.length] + '20',
        fill: false,
        tension: 0.3,
        pointRadius: 4,
        pointHoverRadius: 6,
      })),
    },
    options: {
      responsive: true,
      plugins: {
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${ctx.parsed.y?.toFixed(2)}`,
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 5,
          ticks: { stepSize: 1 },
        },
      },
    },
  })
}

export function createGroupedBarChart(
  canvas: HTMLCanvasElement,
  data: { labels: string[]; datasets: { label: string; data: number[]; color: string }[] },
  title: string,
) {
  Chart.getChart(canvas)?.destroy()
  return new Chart(canvas, {
    type: 'bar',
    data: {
      labels: data.labels,
      datasets: data.datasets.map((ds) => ({
        label: ds.label,
        data: ds.data,
        backgroundColor: ds.color,
        borderRadius: 6,
        barPercentage: 0.65,
        categoryPercentage: 0.85,
      })),
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom' },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${ctx.parsed.x}%`,
          },
        },
      },
      scales: {
        x: {
          beginAtZero: true,
          max: 100,
          ticks: { stepSize: 10 },
        },
        y: {
          ticks: {
            autoSkip: false,
            callback(_value, _index, _ticks) {
              return truncateLabel(this.chart.data.labels[_index] as string)
            },
          },
        },
      },
    },
  })
}
