import { computed, type App } from "vue";
import { installAxiosClient } from "./client";

import dayjs from 'dayjs';
import calendar from 'dayjs/plugin/calendar';
import duration from 'dayjs/plugin/duration';
import relativeTime from 'dayjs/plugin/relativeTime';
import timezone from 'dayjs/plugin/timezone';
import utc from 'dayjs/plugin/utc';

dayjs.extend(calendar)
dayjs.extend(duration)
dayjs.extend(utc)
dayjs.extend(timezone)
dayjs.extend(relativeTime)

import './fontawesome';

export default function installPlugins () {
    return {
        install(app: App) {
            installAxiosClient(app)
            app.config.globalProperties.$data = dayjs
        }
    }
}

function useDayJs () {
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

export {
    useDayJs
};

