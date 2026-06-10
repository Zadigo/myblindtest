# Television Frontend

The television frontend is Nuxt application that allows the user to display the quiz on a television screen. It connects to the backend API to fetch quiz data and uses WebSockets to receive real-time updates during the quiz. The frontend is designed to be responsive and user-friendly, providing an engaging experience for players participating in the quiz.

## Global Architecture

```mermaid
sequenceDiagram
    participant F as Frontend
    participant B as Backend
    F->>B: Fetch quiz data (HTTP Requests)
    B->>F: Return quiz data (JSON)
    F->>B: Connect to WebSocket
    B->>F: Send real-time updates (e.g., quiz status, player scores)
    F->>B: Send player actions (e.g., answer submission)
    B->>F: Broadcast updates to all connected clients
```
