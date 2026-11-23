/** 后端 API 客户端：SSE 聊天流 + 状态轮询。 */

export interface OpenAIMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
}

export type ChatEvent =
  | { type: 'text_delta'; content: string }
  | { type: 'tool_call'; id: string; name: string; arguments: string }
  | { type: 'tool_result'; id: string; name: string; result: string; ok: boolean }
  | { type: 'final'; content: string }
  | { type: 'cancelled' }
  | { type: 'error'; message: string }
  | { type: 'done' }

export interface CopilotStatus {
  fluent_ready: boolean
  sifile: string | null
  model: string
  models: string[]
  busy: boolean
  configured?: boolean
}

export async function fetchStatus(): Promise<CopilotStatus> {
  const resp = await fetch('/api/status')
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
  return resp.json()
}

/** POST /api/chat 并解析 SSE 事件流。abortSignal 断开时 fetch 抛 AbortError。 */
export async function* sseChat(
  messages: OpenAIMessage[],
  signal: AbortSignal,
): AsyncGenerator<ChatEvent> {
  const resp = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages }),
    signal,
  })
  if (!resp.ok || !resp.body) {
    throw new Error(`HTTP ${resp.status}`)
  }
  const reader = resp.body.getReader()
  const decoder = new TextDecoder()
  let buf = ''
  for (;;) {
    const { done, value } = await reader.read()
    if (done) break
    buf += decoder.decode(value, { stream: true })
    let idx: number
    while ((idx = buf.indexOf('\n\n')) >= 0) {
      const frame = buf.slice(0, idx)
      buf = buf.slice(idx + 2)
      const line = frame
        .split('\n')
        .find((l) => l.startsWith('data:'))
      if (!line) continue
      yield JSON.parse(line.slice(5).trim())
    }
  }
}
