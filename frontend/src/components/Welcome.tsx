import { useEffect, useState } from 'react'
import { useAui } from '@assistant-ui/react'
import { fetchStatus } from '../lib/api'

const SAMPLES: { tag: string; question: string }[] = [
  { tag: '帮我看看', question: '会话里有没有警告或错误？' },
  { tag: '查知识库', question: 'GPU 求解器有什么限制？' },
  { tag: '读会话', question: '当前边界条件是什么？' },
]

/** Thread 的 Welcome 插槽:ZCode 风格空状态;未配置 API 时显示首次引导。 */
export default function Welcome() {
  const aui = useAui()
  const [configured, setConfigured] = useState<boolean | null>(null)

  useEffect(() => {
    fetchStatus()
      .then((s) => setConfigured(s.configured !== false))
      .catch(() => {})
  }, [])

  const fillQuestion = (q: string) => {
    aui.thread.composer().setText(q)
    document
      .querySelector<HTMLTextAreaElement>('[data-slot="aui_composer-shell"] textarea')
      ?.focus()
  }

  const openSettings = () => {
    window.dispatchEvent(new Event('copilot:open-settings'))
  }

  return (
    <div className="welcome">
      <div className="welcome-logo">F</div>
      <div className="welcome-title">有什么可以帮你？</div>
      {configured === false && (
        <button type="button" className="welcome-setup" onClick={openSettings}>
          ⚙ 首次使用:点此配置 API(选供应商 → 填 Key → 保存)
        </button>
      )}
      <div className="welcome-samples">
        {SAMPLES.map((s) => (
          <button
            key={s.question}
            className="welcome-sample"
            onClick={() => fillQuestion(s.question)}
          >
            <span className="welcome-sample-tag">{s.tag}</span>
            <span className="welcome-sample-text">{s.question}</span>
          </button>
        ))}
      </div>
      <div className="welcome-hint">
        Enter 发送 · Shift+Enter 换行 · Esc 收起
      </div>
    </div>
  )
}
