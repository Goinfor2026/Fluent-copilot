import { useEffect, useRef, useState } from 'react'
import { shell } from '../lib/shell'
import type { CopilotStatus } from '../lib/api'

function formatElapsed(ms: number): string {
  const total = Math.floor(ms / 1000)
  const h = Math.floor(total / 3600)
  const m = Math.floor((total % 3600) / 60)
  const s = total % 60
  if (h > 0) return `已工作 ${h} 时 ${m} 分 ${s} 秒`
  return `已工作 ${m} 分 ${s} 秒`
}

/** 顶栏:会话计时 + Fluent 状态 + 新对话/记录/收起;整栏可拖拽移动窗口。 */
export default function TopBar({
  onNewChat,
  status,
  onHistory,
}: {
  onNewChat: () => void
  status: CopilotStatus | null
  onHistory: () => void
}) {
  const [elapsed, setElapsed] = useState(0)
  const startRef = useRef(Date.now())

  useEffect(() => {
    const timer = setInterval(
      () => setElapsed(Date.now() - startRef.current),
      1000,
    )
    return () => clearInterval(timer)
  }, [])

  // 拖拽:按下顶栏空白处移动窗口(按钮上 data-nodrag 排除)
  const onPointerDown = (e: React.PointerEvent<HTMLElement>) => {
    if (!shell.available()) return
    if ((e.target as HTMLElement).closest('[data-nodrag]')) return
    let lastX = e.clientX
    let lastY = e.clientY
    const onMove = (ev: PointerEvent) => {
      shell.moveBy(ev.clientX - lastX, ev.clientY - lastY)
      lastX = ev.clientX
      lastY = ev.clientY
    }
    const onUp = () => {
      window.removeEventListener('pointermove', onMove)
      window.removeEventListener('pointerup', onUp)
    }
    window.addEventListener('pointermove', onMove)
    window.addEventListener('pointerup', onUp)
  }

  const busy = status?.busy ?? false
  const ready = status?.fluent_ready ?? false
  const dotClass = busy ? 'dot-busy' : ready ? 'dot-ready' : ''
  const dotLabel = busy ? '思考中' : ready ? 'Fluent 已就绪' : 'Fluent 未连接'

  return (
    <header className="topbar" onPointerDown={onPointerDown}>
      <span className="topbar-timer">{formatElapsed(elapsed)}</span>
      <div className="topbar-right">
        <span className={`status-chip ${dotClass}`} title={status?.sifile ?? ''}>
          <span className="status-dot" />
          {dotLabel}
        </span>
        <button className="ghost-btn" data-nodrag onClick={onNewChat}>
          ＋ 新对话
        </button>
        <button
          className="ghost-btn"
          data-nodrag
          onClick={onHistory}
          title="对话记录"
        >
          记录
        </button>
        <button
          className="ghost-btn"
          data-nodrag
          onClick={() => shell.hide()}
          title="收起（Esc）"
        >
          —
        </button>
      </div>
    </header>
  )
}
