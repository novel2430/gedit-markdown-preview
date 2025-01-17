import { defineConfig } from 'vite';

export default defineConfig({
  base: './',
  build: {
    outDir: '../md_preview/dist',
    emptyOutDir: true,
  },
});

