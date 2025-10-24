import type { EndpointOptions } from './types'

/**
 * Checks whether the application in prodcution
 */
export function inProduction(): boolean {
  return process.env.NODE_ENV === 'production'
}

/**
 * Creates an internal name for the endpoint
 * @param name The endpoint name
 * @example "$endpointAxios"
 * @internal
 */
export function createInternalEndpointName(name: string) {
  return `$${name}Axios`
}

/**
 * Helper function used to check that the domain does not
 * have a protocol (http, https) and does not have a host
 * @param domain The domain to check
 * @param endpoint The endpoint configuration options
 * @internal
 */
export function checkDomain(domain: string, endpoint: EndpointOptions) {
  if (domain.startsWith('http')) {
    throw new Error(`Endpoint "${endpoint.name}" should not start with "http" or "https"`)
  }
}
