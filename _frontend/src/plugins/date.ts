import dayjs from 'dayjs'
import calendar from 'dayjs/plugin/calendar'
import duration from 'dayjs/plugin/duration'
import relativeTime from 'dayjs/plugin/relativeTime'
import timezone from 'dayjs/plugin/timezone'
import utc from 'dayjs/plugin/utc'

dayjs.extend(calendar)
dayjs.extend(duration)
dayjs.extend(utc)
dayjs.extend(timezone)
dayjs.extend(relativeTime)

/**
 *
 */
export function useDayJs() {
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
