import { getBaseUrl, getDomain } from "@/plugins/client";
import { describe, expect, it } from "vitest";

describe('AxiosClient', () => {
    it('can build url for client', async () => {
        const url = getBaseUrl('/api/v1/')
        expect(url).not.toBeNull()
        expect(url).toBe('http://127.0.0.1:8000/api/v1/')
        
        const webSocketUrl = getBaseUrl('/ws/test', null, true)
        expect(webSocketUrl).not.toBeNull()
        expect(webSocketUrl.startsWith('ws')).toBeTruthy()
    })

    it('can get domain', async () => {
        const domain = getDomain()
        expect(domain).toBe('127.0.0.1')
    })
})
