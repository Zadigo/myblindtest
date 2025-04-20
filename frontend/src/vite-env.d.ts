/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_DJANGO_PROD_URL: string

  // Google
  readonly GOOGLE_CLIENT_ID: string
  readonly GOOGLE_CLIENT_SECRET: string

  // Firebase
  readonly VITE_FIREBASE_API_KEY: string
  readonly VITE_FIREBASE_AUTH_DOMAIN: string
  readonly VITE_FIREBASE_DB_URL: string
  readonly VITE_FIREBASE_PROJECT_ID: string
  readonly VITE_FIREBASE_STORAGE_BUCKET: string
  readonly VITE_FIREBASE_MESSAGE_SENDER_ID: string
  readonly VITE_FIREBASE_APP_ID: string
  readonly VITE_FIREBASE_MEASUREMENT_ID: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
