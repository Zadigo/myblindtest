/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_DJANGO_PROD_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
