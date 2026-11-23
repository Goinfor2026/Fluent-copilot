/** pywebview 壳桥接：收起窗口 / 拖拽移动。浏览器模式下全部安全降级为 no-op。 */

interface ShellApi {
  hide_window(): Promise<void>
  move_by(dx: number, dy: number): Promise<void>
}

declare global {
  interface Window {
    pywebview?: { api: ShellApi }
  }
}

export const shell = {
  available(): boolean {
    return typeof window !== 'undefined' && !!window.pywebview?.api
  },
  async hide(): Promise<void> {
    try {
      await window.pywebview?.api.hide_window()
    } catch {
      /* 浏览器模式：忽略 */
    }
  },
  async moveBy(dx: number, dy: number): Promise<void> {
    try {
      await window.pywebview?.api.move_by(dx, dy)
    } catch {
      /* 忽略 */
    }
  },
}
