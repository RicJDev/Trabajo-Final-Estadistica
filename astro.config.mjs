// @ts-check
import { defineConfig } from 'astro/config'

import tailwindcss from '@tailwindcss/vite'

// https://astro.build/config
export default defineConfig({
  site: 'https://ricjdev.github.io',
  base: '/Trabajo-Final-Estadistica/',

  vite: {
    plugins: [tailwindcss()],
  },
})
