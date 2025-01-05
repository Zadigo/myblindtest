/* eslint-disable  @typescript-eslint/no-this-alias */
/* eslint-disable  @typescript-eslint/no-explicit-any */

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
