import { useEffect, useState } from 'react'
import {
  deleteThread,
  listThreads,
  relativeTime,
  type ThreadMeta,
} from '../lib/threads'

/** 对话历史面板:列表 / 加载 / 删除。 */
export default function HistoryPanel({
  onClose,
  onOpenThread,
}: {
  onClose: () => void
  onOpenThread: (id: string) => void
}) {
  const [threads, setThreads] = useState<ThreadMeta[] | null>(null)
  const [filter, setFilter] = useState('')

  const load = () =>
    listThreads()
      .then(setThreads)
      .catch(() => setThreads([]))

  useEffect(() => {
    load()
  }, [])

  const remove = async (id: string) => {
    setThreads((ts) => (ts ?? []).filter((t) => t.id !== id))
    try {
      await deleteThread(id)
    } catch {
      load()
    }
  }

  const visible = (threads ?? []).filter((t) =>
    filter ? t.title.includes(filter) : true,
  )

  return (
    <div className="history-overlay">
      <div className="history-header">
        <button className="ghost-btn" data-nodrag onClick={onClose} title="返回聊天">
          ← 返回
        </button>
        <span className="history-title">对话记录</span>
        <button className="ghost-btn" data-nodrag onClick={onClose} title="关闭">
          ✕
        </button>
      </div>
      <div className="history-search">
        <input
          className="settings-input"
          placeholder="搜索标题…"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          spellCheck={false}
        />
      </div>
      <div className="history-list">
        {threads === null ? (
          <div className="history-empty">加载中…</div>
        ) : visible.length === 0 ? (
          <div className="history-empty">
            {filter ? '没有匹配的对话' : '还没有历史对话,聊一句就有了'}
          </div>
        ) : (
          visible.map((t) => (
            <div key={t.id} className="history-item">
              <button
                className="history-item-main"
                onClick={() => onOpenThread(t.id)}
                title={t.title}
              >
                <span className="history-item-title">{t.title}</span>
                <span className="history-item-meta">
                  {relativeTime(t.updated_at)} · {t.message_count} 条
                </span>
              </button>
              <button
                className="history-item-del"
                title="删除"
                onClick={() => remove(t.id)}
              >
                🗑
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
