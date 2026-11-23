/** ChatModelAdapter：assistant-ui ↔ /api/chat SSE 的翻译层。

后端事件流 → 累计 content parts（assistant-ui 语义：每次 yield 全量 parts）。
- text_delta：续接最后一个 text 段；若已有 tool-call 段则新开一段
- tool_call / tool_result：映射为 tool-call part（result 回填到对应 part）
- error 事件：以 ⚠ 文本段呈现给用户
- 用户取消（AbortError）：静默结束
*/
import type { ChatModelAdapter, ThreadMessage } from '@assistant-ui/react'
import { sseChat, type OpenAIMessage } from '../lib/api'

type Part = {
  type: 'text'
  text: string
} | {
  type: 'tool-call'
  toolCallId: string
  toolName: string
  argsText: string
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  args: Record<string, any>
  result?: string
  isError?: boolean
}

function parseArgs(text: string): Record<string, unknown> {
  try {
    const v = JSON.parse(text || '{}')
    return typeof v === 'object' && v !== null ? v : {}
  } catch {
    return {}
  }
}

function toOpenAIMessages(messages: readonly ThreadMessage[]): OpenAIMessage[] {
  const out: OpenAIMessage[] = []
  for (const m of messages) {
    if (m.role !== 'user' && m.role !== 'assistant') continue
    const text = m.content
      .filter((p): p is { type: 'text'; text: string } => p.type === 'text')
      .map((p) => p.text)
      .join('')
    // 附件内容(文本适配器已把文件文本放进 attachment.content)拼到用户消息后
    const attachmentText = (m.attachments ?? [])
      .flatMap((a) => a.content)
      .filter((p): p is { type: 'text'; text: string } => p.type === 'text')
      .map((p) => p.text)
      .join('\n\n')
    const content = attachmentText
      ? `${text}${text ? '\n\n' : ''}${attachmentText}`
      : text
    if (!content) continue
    out.push({ role: m.role, content })
  }
  return out
}

function pushText(parts: Part[], delta: string) {
  const last = parts[parts.length - 1]
  if (last && last.type === 'text') {
    parts[parts.length - 1] = { type: 'text', text: last.text + delta }
  } else {
    parts.push({ type: 'text', text: delta })
  }
}

export const copilotAdapter: ChatModelAdapter = {
  async *run({ messages, abortSignal }) {
    const parts: Part[] = []

    const snapshot = () => ({
      content: parts
        .filter((p) => p.type !== 'text' || p.text.length > 0)
        .map((p) => ({ ...p })),
    })

    let stream: AsyncGenerator<import('../lib/api').ChatEvent>
    try {
      stream = sseChat(toOpenAIMessages(messages), abortSignal)
    } catch (err) {
      if (abortSignal.aborted) return
      throw err
    }

    try {
      for await (const ev of stream) {
        switch (ev.type) {
          case 'text_delta':
            pushText(parts, ev.content)
            break
          case 'tool_call':
            parts.push({
              type: 'tool-call',
              toolCallId: ev.id,
              toolName: ev.name,
              argsText: ev.arguments,
              args: parseArgs(ev.arguments),
            })
            break
          case 'tool_result': {
            const part = parts.find(
              (p) => p.type === 'tool-call' && p.toolCallId === ev.id,
            )
            if (part && part.type === 'tool-call') {
              part.result = ev.result
              part.isError = !ev.ok
            }
            break
          }
          case 'error':
            pushText(parts, `\n\n⚠ ${ev.message}`)
            break
          case 'final':
          case 'cancelled':
          case 'done':
            break
        }
        if (ev.type !== 'final' && ev.type !== 'cancelled' && ev.type !== 'done') {
          yield snapshot()
        }
      }
    } catch (err) {
      if (abortSignal.aborted) return
      pushText(parts, `\n\n⚠ 连接失败：${String(err)}`)
    }
    yield snapshot()
  },
}
