import { useEffect, useRef, useState } from 'react'
import { Thread } from '@/components/assistant-ui/elements/thread.aui'
import { useAui } from '@assistant-ui/react'
import TopBar from './TopBar'
import Welcome from './Welcome'
import SettingsDialog from './SettingsDialog'
import SaveNoteDialog from './SaveNoteDialog'
import HistoryPanel from './HistoryPanel'
import { shell } from '../lib/shell'
import { fetchStatus, type CopilotStatus } from '../lib/api'
import { upsertThread, type StoredMessage, type StoredPart } from '../lib/threads'

/** 把 thread state 的消息映射为可存储结构(保留文本与工具调用块)。 */
function toStoredMessages(messages: readonly any[]): StoredMessage[] {
  return messages
    .filter((m) => m.role === 'user' || m.role === 'assistant')
    .map((m) => {
      const content: StoredPart[] = []
      for (const p of m.content ?? []) {
        if (p.type === 'text' && p.text) {
          content.push({ type: 'text', text: p.text })
        } else if (p.type === 'tool-call') {
          content.push({
            type: 'tool-call',
            toolCallId: p.toolCallId,
            toolName: p.toolName,
            args: p.args,
            argsText: p.argsText,
            result: p.result,
            isError: p.isError,
          })
        }
      }
      return { role: m.role, content }
    })
    .filter((m) => m.content.length > 0)
}

function deriveTitle(messages: StoredMessage[]): string {
  const first = messages.find((m) => m.role === 'user')
  const text = first?.content.find((p) => p.type === 'text')
  const t = text && text.type === 'text' ? text.text.trim() : ''
  return t ? (t.length > 24 ? t.slice(0, 24) + '…' : t) : '(无标题)'
}

/** 主面板:顶栏 + 官方 Thread + 设置/历史;对话自动保存到后端。 */
export default function ChatPanel({
  onNewChat,
  onOpenThread,
  threadId,
}: {
  onNewChat: () => void
  onOpenThread: (id: string) => void
  threadId: string | null
}) {
  const [status, setStatus] = useState<CopilotStatus | null>(null)
  const [showHistory, setShowHistory] = useState(false)
  const aui = useAui()

  // 状态轮询(3 秒)
  useEffect(() => {
    let alive = true
    const tick = () =>
      fetchStatus()
        .then((s) => alive && setStatus(s))
        .catch(() => {})
    tick()
    const timer = setInterval(tick, 3000)
    return () => {
      alive = false
      clearInterval(timer)
    }
  }, [])

  // Esc:历史面板开着先关面板,否则收起窗口(pywebview 壳)
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== 'Escape') return
      if (showHistory) {
        setShowHistory(false)
      } else {
        shell.hide()
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [showHistory])

  // 自动保存:runtime 状态变化 → 防抖 800ms → 空闲且有消息时 upsert
  const threadIdRef = useRef<string | null>(threadId)
  const lastSavedRef = useRef<string>('')
  useEffect(() => {
    let timer: ReturnType<typeof setTimeout> | null = null
    const save = async () => {
      try {
        const s = aui.thread.getState()
        if (s.isRunning || s.messages.length === 0) return
        const stored = toStoredMessages(s.messages as any[])
        if (stored.length === 0) return
        const payload = JSON.stringify(stored)
        if (payload === lastSavedRef.current) return
        lastSavedRef.current = payload
        const id =
          threadIdRef.current ??
          (threadIdRef.current = crypto.randomUUID())
        await upsertThread({
          id,
          title: deriveTitle(stored),
          messages: stored,
        })
      } catch {
        /* 保存失败不打扰对话,下次变更再试 */
      }
    }
    const unsubscribe = aui.subscribe(() => {
      if (timer) clearTimeout(timer)
      timer = setTimeout(save, 800)
    })
    return () => {
      unsubscribe()
      if (timer) clearTimeout(timer)
    }
  }, [aui])

  return (
    <div className="app-root">
      <TopBar
        onNewChat={onNewChat}
        status={status}
        onHistory={() => setShowHistory(true)}
      />
      <div className="thread-wrap">
        <Thread components={{ Welcome }} />
      </div>
      <SettingsDialog />
      <SaveNoteDialog />
      {showHistory && (
        <HistoryPanel
          onClose={() => setShowHistory(false)}
          onOpenThread={(id) => {
            setShowHistory(false)
            onOpenThread(id)
          }}
        />
      )}
    </div>
  )
}
