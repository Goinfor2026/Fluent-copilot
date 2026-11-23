import { useEffect, useState } from 'react'
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'

export interface SaveNotePayload {
  title: string
  question: string
  answer: string
}

/** 把当前回答沉淀为知识库页面(window 事件 "copilot:save-note" 触发)。 */
export default function SaveNoteDialog() {
  const [open, setOpen] = useState(false)
  const [payload, setPayload] = useState<SaveNotePayload | null>(null)
  const [title, setTitle] = useState('')
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    const onOpen = (e: Event) => {
      const detail = (e as CustomEvent<SaveNotePayload>).detail
      if (!detail) return
      setPayload(detail)
      setTitle(detail.title)
      setError('')
      setOpen(true)
    }
    window.addEventListener('copilot:save-note', onOpen)
    return () => window.removeEventListener('copilot:save-note', onOpen)
  }, [])

  const save = async () => {
    if (!payload) return
    setSaving(true)
    setError('')
    try {
      const resp = await fetch('/api/knowledge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...payload, title }),
      })
      const data = await resp.json().catch(() => ({}))
      if (!resp.ok) {
        setError(data.error || `保存失败（HTTP ${resp.status}）`)
        return
      }
      setOpen(false)
    } catch (e) {
      setError(`保存失败：${String(e)}`)
    } finally {
      setSaving(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      {open && payload && (
        <DialogContent className="max-w-sm">
          <DialogHeader>
            <DialogTitle>存入知识库</DialogTitle>
            <DialogDescription>
              将作为 wiki/notes 页保存,之后 search_wiki 即可命中。
            </DialogDescription>
          </DialogHeader>
          <div className="settings-form">
            <label className="settings-label">
              页面标题
              <input
                className="settings-input"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                spellCheck={false}
                autoFocus
              />
            </label>
            <div className="settings-label">
              内容预览
              <pre className="tool-pre" style={{ maxHeight: 120 }}>
                {`问：${payload.question.slice(0, 100)}\n\n答：${payload.answer.slice(0, 200)}…`}
              </pre>
            </div>
            {error && <div className="settings-error">{error}</div>}
          </div>
          <DialogFooter>
            <DialogClose
              render={
                <button type="button" className="settings-btn ghost">
                  取消
                </button>
              }
            />
            <button
              type="button"
              className="settings-btn primary"
              onClick={save}
              disabled={saving || !title.trim()}
            >
              {saving ? '保存中…' : '保存'}
            </button>
          </DialogFooter>
        </DialogContent>
      )}
    </Dialog>
  )
}
