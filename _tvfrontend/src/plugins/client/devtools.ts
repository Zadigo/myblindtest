import { setupDevtoolsPlugin } from '@vue/devtools-api'

import type { App } from 'vue'
import { vueAxiosManager } from './base'

const inspectorId = 'axios-manager'
const timelineLayerId = 'axios-manager'

export function setupAxiosManagerDevtools(app: App) {
  setupDevtoolsPlugin({
    app,
    id: 'axios-manager',
    label: 'Axios Manager',
    packageName: 'axios-manager',
    homepage: '',
    settings: {
      // https://devtools-v6.vuejs.org/plugin/plugins-guide.html#plugin-settings
    }
  }, (api) => {
    // https://devtools-v6.vuejs.org/plugin/plugins-guide.html#custom-inspector

    vueAxiosManager.api = api

    api.addInspector({
      id: inspectorId,
      label: 'Axios Manager',
      icon: 'web_traffic'
    })

    // Inspector Tree

    api.on.getInspectorTree((payload) => {
      if (payload.inspectorId === inspectorId) {
        let rootNodes = []

        rootNodes = vueAxiosManager.endpoints.map(endpoint => ({
          id: endpoint.name,
          label: endpoint.name,
          tags: [
            {
              label: endpoint.label?.toLowerCase().trim() || 'Axios',
              textColor: 0xffffff,
              backgroundColor: 0x000000
            }
          ]
        }))

        payload.rootNodes = rootNodes
      }
    })

    api.on.getInspectorState((payload) => {
      if (payload.inspectorId === inspectorId) {
        const options = vueAxiosManager._getEndpointValues(payload.nodeId)

        payload.state = {
          options: options || []
        }
      }
    })

    // Timeline

    api.addTimelineLayer({
      id: timelineLayerId,
      color: 0xff984f,
      label: 'Axios Manager'
    })
  })
}
