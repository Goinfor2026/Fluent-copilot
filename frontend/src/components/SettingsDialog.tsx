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

interface Provider {
  id: string
  name: string
  base_url: string
  models: string[]
}

interface Settings {
  provider: string
  base_url: string
  api_key: string
  model: string
  models: string[]
}

/** API 设置对话框:API 地址 / Key / 模型列表管理,保存写回 config.toml 并热生效。

 * 无自带触发按钮;监听 window 事件 "copilot:open-settings" 打开
 * (入口在底部模型选择菜单的 "API 设置…" 项,事件避免了穿过官方 Thread 组件传 props)。
 */
export default function SettingsDialog() {
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const onOpen = () => setOpen(true)
    window.addEventListener('copilot:open-settings', onOpen)
    return () => window.removeEventListener('copilot:open-settings', onOpen)
  }, [])

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      {open && (
        <DialogContent className="max-w-sm">
          <SettingsForm onClose={() => setOpen(false)} />
        </DialogContent>
      )}
    </Dialog>
  )
}

function SettingsForm({ onClose }: { onClose: () => void }) {
  const [providers, setProviders] = useState<Provider[]>([])
  const [providerId, setProviderId] = useState('custom')
  const [baseUrl, setBaseUrl] = useState('')
  const [apiKey, setApiKey] = useState('')
  const [showKey, setShowKey] = useState(false)
  const [models, setModels] = useState<string[]>([])
  const [model, setModel] = useState('')
  const [newModel, setNewModel] = useState('')
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    Promise.all([
      fetch('/api/settings').then((r) => r.json()),
      fetch('/api/providers')
        .then((r) => r.json())
        .catch(() => []),
    ])
      .then(([s, ps]: [Settings, Provider[]]) => {
        setProviders(Array.isArray(ps) ? ps : [])
        setProviderId(s.provider || 'custom')
        setBaseUrl(s.base_url)
        setApiKey(s.api_key)
        setModels(s.models)
        setModel(s.model)
        setLoaded(true)
      })
      .catch(() => setError('读取设置失败'))
  }, [])

  /** 选供应商:自动填地址与默认模型列表(key 不动,模型可再增删)。 */
  const applyProvider = (id: string) => {
    setProviderId(id)
    const p = providers.find((x) => x.id === id)
    if (!p) return
    if (id !== 'custom') {
      setBaseUrl(p.base_url)
      if (p.models.length > 0) {
        setModels([...p.models])
        setModel(p.models[0])
      }
    }
  }

  /** 手动改地址后,若不再匹配所选预置,自动切到"自定义"。 */
  const onBaseUrlChange = (url: string) => {
    setBaseUrl(url)
    const norm = url.trim().replace(/\/+$/, '').toLowerCase()
    const cur = providers.find((x) => x.id === providerId)
    const matched =
      cur && cur.id !== 'custom'
        ? cur.base_url.replace(/\/+$/, '').toLowerCase() === norm
        : false
    if (!matched) {
      const hit = providers.find(
        (x) => x.id !== 'custom' && x.base_url.replace(/\/+$/, '').toLowerCase() === norm,
      )
      setProviderId(hit ? hit.id : 'custom')
    }
  }

  const addModel = () => {
    const m = newModel.trim()
    if (!m || models.includes(m)) {
      setNewModel('')
      return
    }
    setModels([...models, m])
    setNewModel('')
  }

  const removeModel = (m: string) => {
    const next = models.filter((x) => x !== m)
    if (next.length === 0) return
    setModels(next)
    if (model === m) setModel(next[0])
  }

  const save = async () => {
    setSaving(true)
    setError('')
    try {
      const resp = await fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          base_url: baseUrl,
          api_key: apiKey,
          models,
          model,
        }),
      })
      const data = await resp.json().catch(() => ({}))
      if (!resp.ok) {
        setError(data.error || `保存失败（HTTP ${resp.status}）`)
        return
      }
      onClose()
    } catch (e) {
      setError(`保存失败：${String(e)}`)
    } finally {
      setSaving(false)
    }
  }

  return (
    <>
      <DialogHeader>
        <DialogTitle>API 设置</DialogTitle>
        <DialogDescription>
          修改后保存即写回 config.toml,下一轮对话生效。
        </DialogDescription>
      </DialogHeader>

      <div className="settings-form">
        <label className="settings-label">
          供应商
          <select
            className="settings-input settings-select"
            value={providerId}
            onChange={(e) => applyProvider(e.target.value)}
          >
            {providers.length === 0 && <option value="custom">自定义</option>}
            {providers.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name}
              </option>
            ))}
          </select>
        </label>

        <label className="settings-label">
          API 地址
          <input
            className="settings-input"
            value={baseUrl}
            onChange={(e) => onBaseUrlChange(e.target.value)}
            placeholder="https://open.bigmodel.cn/api/paas/v4/"
            spellCheck={false}
          />
        </label>

        <label className="settings-label">
          API Key
          <div className="settings-key-row">
            <input
              className="settings-input"
              type={showKey ? 'text' : 'password'}
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="sk-…"
              spellCheck={false}
            />
            <button
              type="button"
              className="settings-key-toggle"
              onClick={() => setShowKey((v) => !v)}
            >
              {showKey ? '隐藏' : '显示'}
            </button>
          </div>
        </label>

        <div className="settings-label">
          模型列表
          <div className="chip-row">
            {models.map((m) => (
              <span key={m} className={`chip${m === model ? ' chip-active' : ''}`}>
                {m}
                <button
                  type="button"
                  className="chip-x"
                  title="移除"
                  onClick={() => removeModel(m)}
                >
                  ×
                </button>
              </span>
            ))}
          </div>
          <div className="settings-key-row">
            <input
              className="settings-input"
              value={newModel}
              onChange={(e) => setNewModel(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault()
                  addModel()
                }
              }}
              placeholder="添加模型名，如 glm-4.5"
              spellCheck={false}
            />
            <button type="button" className="settings-key-toggle" onClick={addModel}>
              添加
            </button>
          </div>
        </div>

        <label className="settings-label">
          当前模型
          <select
            className="settings-input settings-select"
            value={model}
            onChange={(e) => setModel(e.target.value)}
          >
            {models.map((m) => (
              <option key={m} value={m}>
                {m}
              </option>
            ))}
          </select>
        </label>

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
          disabled={saving || !loaded}
        >
          {saving ? '保存中…' : '保存'}
        </button>
      </DialogFooter>
    </>
  )
}
