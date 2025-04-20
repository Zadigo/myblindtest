import { computed, type App } from 'vue'
import { installAxiosClient } from './client'

import dayjs from 'dayjs'
import calendar from 'dayjs/plugin/calendar'
import duration from 'dayjs/plugin/duration'
import relativeTime from 'dayjs/plugin/relativeTime'
import timezone from 'dayjs/plugin/timezone'
import utc from 'dayjs/plugin/utc'

import './fontawesome'

/**
 *
 */
// async function autoLoadComponents(app: App) {
//   const components = import.meta.glob('../components/ui/**/*.vue')

//   for (const [path, loader] of Object.entries(components)) {
//     const fileName = path.split('/').pop()
//     if (!fileName) {
//       continue
//     } else {
//       const componentName = fileName.replace(/\.\w+$/, '')
//       app.component(componentName, defineAsyncComponent(loader))
//     }
//   }
// }

/**
 *
 */
function useDayJs() {
  const instance = dayjs

  const currentDate = computed(() => {
    return instance()
  })

  const currentYear = computed(() => {
    return currentDate.value.year()
  })

  return {
    currentDate,
    currentYear,
    instance
  }
}

export default function installPlugins() {
  dayjs.extend(calendar)
  dayjs.extend(duration)
  dayjs.extend(utc)
  dayjs.extend(timezone)
  dayjs.extend(relativeTime)

  return {
    install(app: App) {
      // autoLoadComponents(app)
      installAxiosClient(app)
      app.config.globalProperties.$data = dayjs
    }
  }
}

export {
  useDayJs
}
