import type { Ref, App, Reactive, ToRefs } from 'vue'
import type { Axios, AxiosRequestConfig, AxiosResponse } from 'axios'

export interface ExtendedInternalAxiosRequestConfig extends InternalAxiosRequestConfig {
  _retry?: boolean
}

type InternalAxiosRequestConfig = Omit<AxiosRequestConfig, 'baseURL' | 'data' | 'params' | 'method' | 'url'>

interface SharedOptions {
  /**
   * Axios configuration options to pass to the instance
   */
  axios?: InternalAxiosRequestConfig
  /**
   * The bearer for the autorization token of this endpoint
   * @default "Token"
   */
  bearer?: string
  /**
   * Disables both access and refresh token verification and workflow. This option
   * will override the `disableAccess` and `disableRefresh` options regardless of
   * what they are set to `true` or `false`.
   * @description This is useful for endpoints that do not require authentication
   * @default false
   */
  disableAuth?: boolean
}

export interface EndpointOptions extends SharedOptions {
  /**
   * Endpoint name
   */
  name: string
  /**
   * Adds a label to better identify the endpoint
   * in devtools
   * @default "Axios"
   */
  label?: string
  /**
   * Default development domain
   * @default "127.0.0.1"
   */
  dev?: string
  /**
   * Port for the default development domain
   * @default 8000
   */
  port?: string
  /**
   * The production domain
   * @example "example.com"
   */
  domain?: string
  /**
   * Path used to authenticate a user
   * @default "/v1/token"
   */
  accessEndpoint?: string
  /**
   * Path used to refresh an access token
   * @default "/v1/refresh/token"
   */
  refreshEnpoint?: string
  /**
   * Whether to use https for the development endpoint
   * @default false
   */
  https?: boolean
  /**
   * Key to the access token in the storage
   * @default "access"
   */
  accessKey?: string
  /**
   * Key to the refresh token in the storage
   * @default "refresh"
   */
  refreshKey?: string
  /**
   * Disables the access token verification
   * @default false
   */
  disableAccess?: boolean
  /**
   * Disables the refresh token refresh workflow
   * @default false
   */
  disableRefresh?: boolean
}

export interface PluginOptions extends SharedOptions {
  /**
   * Global to implement for all instances
   * @default 20000
   */
  timeout?: number
  /**
   * Options for the endpoint
   */
  endpoints: EndpointOptions[]
}

export type EndpointOptionKeys = keyof EndpointOptions

/**
 * @description For internal use
 */
export interface InternalEnpointOptions extends EndpointOptions {
  /**
   * Name used to identify the endpoint in
   * Vue's globalProperties
   * @example "$endpointAxios"
   */
  internalName: string
  /**
   * The full url for the endpoint
   */
  endpointDomain: string
  /**
   * The Axios instance for this endpoint
   */
  instance: Axios
}

export type InternalEndpointOptionKeys = keyof InternalEnpointOptions

export interface ComposableOptions<T> {
  /**
   * Provide a url to use which will supersede
   * the endpoint provided
   * ```js
   * const { execute } = useRequest('/path', {
   *  baseUrl: 'http://example.com'
   * })
   * await execute()
   * ```
   */
  baseUrl?: string
  /**
   * Metthod for the request
   * @default "get"
   */
  method?: Methods
  /**
   * Request body
   */
  body?: Record<string, unknown>
  /**
   * Request query
   */
  query?: Record<string, unknown>
  /**
   * Hook used to execute before the request starts
   */
  beforeStart?: () => void
  /**
   * Hook used after the request has finished
   * @param response The response for the request
   */
  completed?: (response: AxiosResponse<T>) => T
  /**
   * Watch and trigger requests based on a parameter
   */
  watch?: Ref<T>
}

export interface AsyncComposableOptions<T> extends ComposableOptions<T> {
  /**
   * Executes the request immediately
   * @default false
   */
  immediate?: boolean
  /**
   * Debounce the execution of the request
   * @default 0
   */
  debounce?: number
}

export type LoginComposableOptions<T> = Omit<ComposableOptions<T>, 'method' | 'body'>

/**
 * @todo rename to "HttpMethods"
 */
export type Methods = 'get' | 'post' | 'delete' | 'put' | 'patch'

export interface Credentials extends Record<string, string | undefined> {
  /**
   * Username to use
   */
  username?: string
  /**
   * Email to use
   */
  email?: string
  /**
   * Password to use
   */
  password: string
}

/**
 * Store
 */

/**
 * Container for the requests sent
 * @internal
 */
export interface RequestsContainer {
  name: string
  method: Methods
  statusText: string
  data: Record<string, unknown>
  headers: string
  path: string | undefined
}

/**
 * @internal
 */
export interface _DevtoolsTimelineObject {
  key: string
  value: string | boolean | ExtendedInternalAxiosRequestConfig | undefined
}

/**
 * Class that stores all the requests sent
 * @internal
 */
export interface RequestStoreClass {
  /**
   * Name of the instances created by the user
   */
  instanceNames: string[]
  /**
   * Last request sent
   */
  last: RequestsContainer
  /**
   * Container for the requests sent
   */
  container: RequestsContainer[]
  /**
   * Devtools Api
   */
  api: unknown
  /**
   * Returns a new endpoint
   * @param name Endpoint name
   */
  getEndpointValues: (name: string) => _DevtoolsTimelineObject[]
  /**
   * Filters requests by name
   * @param name Endpoint name
   */
  filterByName: (name: string) => RequestsContainer[]
  /**
   * Registers a new endpoint
   * @param name Endpoint name
   */
  registerName: (name: string) => void
  /**
   * Registers a new request
   */
  registerRequest: (params: RequestsContainer) => void
}

export interface RefreshApiResponse {
  access: string
}

/**
 * @internal
 */
export interface _VueAxiosManager {
  pluginOptions: PluginOptions | undefined
  endpoints: InternalEnpointOptions[]
  provideAttr: Record<string, InternalEnpointOptions>
  container: Record<string, RequestsContainer[]>
  initialize: (app: App, pluginOptions: PluginOptions) => void
  _getRequests: (name: string) => ToRefs<Reactive<RequestsContainer[]>>
  _getLast: (name: string) => Ref<RequestsContainer>
  _registerRequest: (method: string, endpoint: EndpointOptions | undefined, params: RequestsContainer, timelineLayerId?: string, isError?: boolean) => void
  _getEndpointValues: (name: string) => _DevtoolsTimelineObject[] | undefined
}
