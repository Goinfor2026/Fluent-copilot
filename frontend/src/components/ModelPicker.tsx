import { useEffect, useRef, useState } from 'react'
import { fetchStatus, type CopilotStatus } from '../lib/api'

/** 底部输入区的模型选择器：⚙ model ▾，点击上弹菜单切换（下一轮对话生效）。 */
export default function ModelPicker() {
  const [status, setStatus] = useState<CopilotStatus | null>(null)
  const [open, setOpen] = useState(false)
  const rootRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    let alive = true
    const tick = () =>
      fetchStatus()
        .then((s) => alive && setStatus(s))
        .catch(() => {})
    tick()
    const timer = setInterval(tick, 5000)
    return () => {
      alive = false
      clearInterval(timer)
    }
  }, [])

  useEffect(() => {
    if (!open) return
    const onDown = (e: MouseEvent) => {
      if (!rootRef.current?.contains(e.target as Node)) setOpen(false)
    }
    window.addEventListener('mousedown', onDown)
    return () => window.removeEventListener('mousedown', onDown)
  }, [open])

  const models = status?.models ?? []
  const current = status?.model ?? '…'
  const selectable = models.length > 1

  const openSettings = () => {
    setOpen(false)
    window.dispatchEvent(new Event('copilot:open-settings'))
  }

  const pick = async (model: string) => {
    setOpen(false)
    if (model === current) return
    try {
      await fetch('/api/model', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model }),
      })
      setStatus((s) => (s ? { ...s, model } : s))
    } catch {
      /* 失败则等下一轮轮询纠正 */
    }
  }

  return (
    <div ref={rootRef} className="relative">
      <button
        type="button"
        className="model-picker-btn"
        title={selectable ? '切换模型' : '模型与 API 设置'}
        onClick={() => setOpen((v) => !v)}
      >
        ⚙ {current}
        <span className="model-picker-caret">▾</span>
      </button>
      {open && (
        <div className="model-picker-menu" role="listbox">
          {selectable &&
            models.map((m) => (
              <button
                key={m}
                type="button"
                role="option"
                aria-selected={m === current}
                className={`model-picker-item${m === current ? ' active' : ''}`}
                onClick={() => pick(m)}
              >
                {m === current && <span className="model-picker-check">✓</span>}
                <span>{m}</span>
              </button>
            ))}
          <div className="model-picker-divider" />
          <button type="button" className="model-picker-item footer" onClick={openSettings}>
            <span className="model-picker-check">⚙</span>
            <span>API 设置…</span>
          </button>
        </div>
      )}
    </div>
  )
}
