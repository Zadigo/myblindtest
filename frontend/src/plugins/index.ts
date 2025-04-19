import { computed, type App, defineAsyncComponent } from 'vue'
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
async function autoLoadComponents(app: App) {
  const components = import.meta.glob('../components/ui/**/*.vue')

  for (const [path, loader] of Object.entries(components)) {
    const fileName = path.split('/').pop()
    if (!fileName) {
      continue
    } else {
      const componentName = fileName.replace(/\.\w+$/, '')
      app.component(componentName, defineAsyncComponent(loader))
    }
  }

  // Object.entries(components).forEach(([path, component]) => {
  //     // console.log(path, component)
  //     if (path) {
  //         const result = path.split('/').pop()
  //         if (result) {
  //             const item = result.replace(/\.\w+$/, '')
  //             console.log(item, component.default)
  //             app.component(item, component.default)
  //         }
  //     }
  // })
}

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
      autoLoadComponents(app)
      installAxiosClient(app)
      app.config.globalProperties.$data = dayjs
    }
  }
}

export {
  useDayJs
}
