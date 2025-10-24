import { vueAxiosManager } from './base'

import type { InternalEnpointOptions } from './types'

declare global {
  interface Window {
    VueAxiosManager?: typeof vueAxiosManager
  }
}

declare module 'vue' {
  interface GlobalComponents { }

  export interface ComponentCustomProperties {
    $axiosEndpoints: Record<string, InternalEnpointOptions>
  }
}

// normally this is only needed in .d.ts files
export {}
