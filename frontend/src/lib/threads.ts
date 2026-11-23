/** 对话历史 API 客户端(后端存 data/threads/{id}.json)。 */

export type StoredPart =
  | {
      type: 'text'
      text: string
    }
  | {
      type: 'tool-call'
      toolCallId?: string
      toolName: string
      args?: Record<string, any>
      argsText?: string
      result?: unknown
      isError?: boolean
    }

export interface StoredMessage {
  role: 'user' | 'assistant'
  content: StoredPart[]
}

export interface ThreadMeta {
  id: string
  title: string
  updated_at: string
  message_count: number
}

export interface ThreadFull {
  id: string
  title: string
  created_at: string
  updated_at: string
  messages: StoredMessage[]
}

export async function listThreads(): Promise<ThreadMeta[]> {
  const resp = await fetch('/api/threads')
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
  return resp.json()
}

export async function getThread(id: string): Promise<ThreadFull> {
  const resp = await fetch(`/api/threads/${encodeURIComponent(id)}`)
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
  return resp.json()
}

export async function upsertThread(body: {
  id: string
  title: string
  messages: StoredMessage[]
}): Promise<void> {
  const resp = await fetch('/api/threads', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
}

export async function deleteThread(id: string): Promise<void> {
  const resp = await fetch(`/api/threads/${encodeURIComponent(id)}`, {
    method: 'DELETE',
  })
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
}

/** 相对时间显示:3 分钟前 / 昨天 / 10-24 */
export function relativeTime(iso: string): string {
  const t = new Date(iso.replace(' ', 'T'))
  if (isNaN(t.getTime())) return iso
  const diff = Date.now() - t.getTime()
  const min = Math.floor(diff / 60000)
  if (min < 1) return '刚刚'
  if (min < 60) return `${min} 分钟前`
  const h = Math.floor(min / 60)
  if (h < 24) return `${h} 小时前`
  const d = Math.floor(h / 24)
  if (d === 1) return '昨天'
  if (d < 7) return `${d} 天前`
  const m = t.getMonth() + 1
  const day = t.getDate()
  return `${m}-${day}`
}
