import { useState } from 'react'
import { AssistantRuntimeProvider, useLocalRuntime } from '@assistant-ui/react'
import type { ThreadMessageLike } from '@assistant-ui/react'
import { copilotAdapter } from './runtime/adapter'
import { FluentTextAttachmentAdapter } from './lib/attachmentAdapter'
import ChatPanel from './components/ChatPanel'
import { getThread, type StoredMessage } from './lib/threads'

export interface Session {
  key: number
  threadId: string | null
  initialMessages: ThreadMessageLike[]
}

function toMessageLike(stored: StoredMessage[]): ThreadMessageLike[] {
  return stored
    .filter((m) => m.role === 'user' || m.role === 'assistant')
    .map((m) => ({
      role: m.role,
      content: m.content.filter(
        (p) => p.type === 'text' || p.type === 'tool-call',
      ),
    }))
}

/** 新对话/加载历史 = 整体重挂 RuntimeShell(带 initialMessages 恢复)。 */
function RuntimeShell({
  session,
  onNewChat,
  onOpenThread,
}: {
  session: Session
  onNewChat: () => void
  onOpenThread: (id: string) => void
}) {
  const runtime = useLocalRuntime(copilotAdapter, {
    adapters: { attachments: new FluentTextAttachmentAdapter() },
    initialMessages: session.initialMessages,
  })
  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <ChatPanel
        onNewChat={onNewChat}
        onOpenThread={onOpenThread}
        threadId={session.threadId}
      />
    </AssistantRuntimeProvider>
  )
}

export default function App() {
  const [session, setSession] = useState<Session>({
    key: 0,
    threadId: null,
    initialMessages: [],
  })

  const newChat = () =>
    setSession((s) => ({ key: s.key + 1, threadId: null, initialMessages: [] }))

  const openThread = async (id: string) => {
    try {
      const t = await getThread(id)
      setSession((s) => ({
        key: s.key + 1,
        threadId: id,
        initialMessages: toMessageLike(t.messages),
      }))
    } catch {
      /* 列表已刷新,容错 */
    }
  }

  return (
    <RuntimeShell
      key={session.key}
      session={session}
      onNewChat={newChat}
      onOpenThread={openThread}
    />
  )
}
