import axios from 'axios'

import { markRaw, reactive, toRefs } from 'vue'
import { setupAxiosManagerDevtools } from './devtools'
import { checkDomain, createInternalEndpointName, inProduction } from './utils'

import type { App, Plugin } from 'vue'
import type { _DevtoolsTimelineObject, _VueAxiosManager, EndpointOptions, InternalEndpointOptionKeys, InternalEnpointOptions, PluginOptions, RequestsContainer } from './types'

/**
 * Manager that centralizes the different options
 * of the application for different functions
 * @internal
 */
export class VueAxiosManager implements _VueAxiosManager {
  public pluginOptions: PluginOptions | undefined
  public endpoints: InternalEnpointOptions[]
  public provideAttr: Record<string, InternalEnpointOptions>

  public api: unknown
  public container: Record<string, RequestsContainer[]>

  constructor() {
    this.pluginOptions = undefined
    this.endpoints = []
    this.provideAttr = {}
    this.container = {}
  }

  /**
   * Initialize the manager
   * @param app The vue application
   * @param pluginOptions The optioons for the plugin
   */
  public initialize(app: App, pluginOptions: PluginOptions) {
    this.pluginOptions = pluginOptions

    this.endpoints = pluginOptions.endpoints.map((endpointOptions) => {
      const result = createAxiosInstance(pluginOptions, endpointOptions)
      app.config.globalProperties[result.internalName] = result.instance
      return result
    })

    this.endpoints.forEach((endpoint) => {
      this.provideAttr[endpoint.name] = endpoint
      this.container[endpoint.name] = []
    })
  }

  /**
   * Return the requests for a given endpoint
   * @param name The name of the endpoint
   */
  public _getRequests(name: string) {
    return toRefs(reactive(this.container[name]))
  }

  /**
   * The last request of the given array
   * @param name Return the last request sent by a given enpoint
   */
  public _getLast(name: string) {
    const requests = this._getRequests(name)
    // @ts-expect-error length is Ref.length
    return requests[requests.length - 1]
  }

  /**
   * Register a new request
   * @param options The options for the request
   */
  public _registerRequest(method: string, endpoint: EndpointOptions | undefined, params: RequestsContainer, timelineLayerId?: string, isError: boolean = false) {
    if (!endpoint) {
      return
    }

    if (!inProduction()) {
      if (this.api) {
        // @ts-expect-error no export
        this.api.addTimelineEvent({
          layerId: timelineLayerId || 'axios-manager',
          event: {
            // @ts-expect-error no export
            time: this.api.now(),
            title: method,
            subtitle: 'Axios Request',
            logType: isError ? 'error' : 'default',
            groupId: method,
            data: params
          }
        })
      }

      try {
        // console.log('VueAxiosManager.container', this.container)
        this.container[endpoint.name].push(params)
      } catch (e: unknown) {
        // @ts-expect-error Unknown error
        throw new Error(e)
      }
    }
  }

  /**
   * @param name The name of the endpoint to get
   */
  public _getEndpointValues(name: string): _DevtoolsTimelineObject[] | undefined {
    const option = this.endpoints.find(item => item.name === name)
    const optionsForDevtool: _DevtoolsTimelineObject[] = []

    // // console.log('RequestStore: : option', option)

    if (option) {
      const keys = Object.keys(option) as InternalEndpointOptionKeys[]

      // console.log('option', option, keys)

      keys.filter(key => key !== 'instance').forEach((key) => {
        const value = option[key]

        if (value) {
          optionsForDevtool.push({
            key: key,
            value
          })
        }
      })
      // console.log('getEndpoint', optionsForDevtool)
      return optionsForDevtool
    }
  }
}

export const vueAxiosManager = new VueAxiosManager()

/**
 * Creates a new axios instance with the provided name
 * @param endpoint Endpoint for which the instance should be create
 * @example
 * ```js
 * const result = createAxiosInstance({ name: 'companies' })
 * console.log(result)
 * { name: "companiesAxios", instance: Axios }
 * ```
 * @internal
 */
export function createAxiosInstance(pluginOptions: PluginOptions, endpoint: EndpointOptions): InternalEnpointOptions {
  const protocole = endpoint.https ? 'https' : 'http'
  const devDomain = endpoint.dev || `127.0.0.1:${endpoint.port || 8000}`

  checkDomain(devDomain, endpoint)

  let baseDomain: string = `${protocole}://${devDomain}`

  if (inProduction()) {
    if (!endpoint.domain) {
      throw new Error(`You need to set domain for "${endpoint.name}" endpoint for production environments`)
    } else {
      baseDomain = endpoint.domain
      checkDomain(baseDomain, endpoint)
    }
  }

  // console.log('createAxiosInstance.baseDomain', baseDomain)

  const axiosOptions = pluginOptions.axios || endpoint.axios || {}
  const instance = axios.create({
    baseURL: baseDomain,
    ...axiosOptions
  })

  const finalOptions = {
    ...endpoint,
    internalName: createInternalEndpointName(endpoint.name),
    endpointDomain: baseDomain,
    instance
  }

  if (finalOptions.disableAccess === undefined) {
    finalOptions.disableAccess = false
  }

  if (finalOptions.disableRefresh === undefined) {
    finalOptions.disableRefresh = false
  }

  if (pluginOptions.disableAuth) {
    finalOptions.disableAccess = true
    finalOptions.disableRefresh = true
  }

  return finalOptions
}

/**
 *
 * @param options Options for the endpoints to create
 */
export function createVueAxiosManager(options: PluginOptions): Plugin {
  return {
    install(app) {
      vueAxiosManager.initialize(app, options)

      app.mixin({
        provide: {
          $axiosManager: markRaw(vueAxiosManager)
        }
      })

      if (!inProduction()) {
        window.VueAxiosManager = vueAxiosManager
        setupAxiosManagerDevtools(app)
      }
    }
  }
}
