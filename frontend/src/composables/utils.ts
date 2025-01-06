/* eslint-disable  @typescript-eslint/no-this-alias */
/* eslint-disable  @typescript-eslint/no-explicit-any */

import { ref } from "vue"

export function useDebounce () {
    function debounce(func: (...args: any[]) => void, wait: number, immediate: boolean) {
        let timeout: number | undefined | null

        return (...callbackArgs: any[]) => {
            const context = this
            // const args = arguments

            function later() {
                timeout = null
                if (!immediate) {
                    func.apply(context, callbackArgs)
                }
            }
            
            const callNow = immediate && !timeout
            
            clearTimeout(timeout)
            timeout = setTimeout(later, wait)
            
            if (callNow) {
                func.apply(context, callbackArgs)
            }
        }
    }

    return {
        debounce
    }
}

export function useLimitOffeset () {
    const paginationUrl = ref<URL>()

    function parser(url: string | null | undefined, limit = 100, offset = 100) {
        let defaultLimit: string | number = 100
        let defaultOffset: string | number = 0

        if (url) {
            paginationUrl.value = new URL(url)

            const potentialLimit = paginationUrl.value.searchParams.get('limit')
            const potentialOffset = paginationUrl.value.searchParams.get('offset')

            defaultLimit = potentialLimit || limit
            defaultOffset = potentialOffset || offset
        }

        const query = new URLSearchParams({ limit: defaultLimit.toString(), offset: defaultOffset.toString() }).toString()

        return {
            query,
            limit: defaultLimit,
            offset: defaultOffset
        }
    }

    return {
        parser
    }
}
