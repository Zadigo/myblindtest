import dayjs from 'dayjs'
import en from 'dayjs/locale/en'
import fr from 'dayjs/locale/fr'
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
dayjs.locale(en)
dayjs.locale(fr)

/**
 * A composable that provides Day.js functionalities
 */
export function useDayJs() {
  const instance = reactify(() => dayjs())

  const currentDate = computed(() => instance().value.toDate())
  const currentYear = computed(() => instance().value.year())

  return {
    /**
     * Returns the current Day.js instance
     */
    currentDate,
    /**
     * Returns the current year
     */
    currentYear,
    /**
     * Returns the Day.js instance
     */
    instance
  }
}
