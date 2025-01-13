// import { getBaseUrl } from "@/plugins/client"
// import { WebsocketMessage } from "@/types"
// import { useWebSocket } from "@vueuse/core"
// import { afterEach, beforeEach, describe, expect, it } from "vitest"


// function sendMessage(data: WebsocketMessage) {
//     return JSON.stringify(data)
// }

// async function waitForWebsocketState(ws: ReturnType<typeof useWebSocket>): Promise<void> {
//     return new Promise((resolve) => {
//         if (ws.status.value === 'OPEN') {
//             resolve()
//             return
//         }

//         const interval = setInterval(() => {
//             if (ws.status.value === 'CONNECTING') {
//                 clearInterval(interval)
//                 resolve()
//             }
//         }, 100)
//     })
// }

// describe('Score calculation', async () => {
//     let ws: ReturnType<typeof useWebSocket>
//     let messageReceived: Promise<void>

//     beforeEach(() => {
//         ws = useWebSocket(getBaseUrl('/ws/songs', null, true), {
//             immediate: false,
//             autoReconnect: {
//                 retries: 3,
//                 delay: 1000
//             },
//             heartbeat: {
//                 message: 'ping',
//                 interval: 1000
//             }
//         })
//     })

//     afterEach(async () => {
//         if (ws.status.value === 'OPEN') {
//             ws.close()
//             await waitForWebsocketState(ws)
//         }
//     })

//     it('should calculate correct score for valid guess', async () => {
//         messageReceived = new Promise((resolve) => {
//             ws.ws.value?.onmessage((event) => {
//                 try {
//                     const data = JSON.parse(event.data as string) as WebsocketMessage

//                     if (data.type === 'guess.correct') {
//                         expect(data.points).toBe(2)
//                         resolve()
//                     }
//                 } catch (error) {
//                     console.error('Failed to parse message')
//                 }
//             })
//         })

//         ws.open()
//         await waitForWebsocketState(ws)

//         ws.send(sendMessage({
//             type: 'guess.correct',
//             team: 1
//         }))

//         await Promise.race([
//             messageReceived,
//             new Promise((_, reject) => {
//                 setTimeout(() => reject(new Error('WebSocket timeout')), 5000)
//             })
//         ])
//     })

// })
