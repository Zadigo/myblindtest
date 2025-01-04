import { getBaseUrl } from "@/plugins/client";
import { describe, expect, it } from "vitest";

describe('AxiosClient', () => {
    it('can build url', async () => {
        const url = getBaseUrl('/api/v1/')
        expect(url).toBe('http://127.0.0.1:8000/api/v1/')
    })
})
