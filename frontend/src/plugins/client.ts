import axios from 'axios'
import type { App } from 'vue'


function getBaseUrl (path: string, altDomain?: string, port: number = 8000) {
    const isSecure = window.location.href.startsWith('https://')
    const loc = isSecure ? 'https' : 'http'
    const domain = import.meta.env.DEV ? '127.0.0.1' : altDomain || import.meta.env.VITE_BASE_DOMAIN
    console.info(domain)
    return `${loc}://${domain}:${port}${path}`
}

export default function createClient (path?: string, altDomain?: string, port?: 8000) {
    const basePath = path || '/api/v1/'
    const instance =  axios.create({
        baseURL: getBaseUrl(basePath, altDomain, port),
        headers: { "Content-Type": 'application/json' },
        timeout: 10000,
        withCredentials: true
    })

    instance.interceptors.request.use(
        config => {
            return config
        },
        error => {
            return Promise.reject(error)
        }
    )

    instance.interceptors.response.use(
        response => {
            return response
        },
        error => {
            return Promise.reject(error)
        }
    )

    return instance
}

const client = createClient()

function installAxiosClient (app: App) {
    app.config.globalProperties.$client = client
}

function useAxiosClient () {
    const client = createClient()

    return {
        client
    }
}

export {
    client, getBaseUrl,
    installAxiosClient, useAxiosClient
}

