/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_PROD_DOMAIN: string
  readonly VITE_PROD_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
