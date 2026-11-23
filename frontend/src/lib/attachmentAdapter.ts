import type {
  AttachmentAdapter,
  CompleteAttachment,
  PendingAttachment,
} from '@assistant-ui/react'

/** 纯文本类(直接读)与文档类(提取后读)的大小上限 */
const TEXT_LIMIT = 2 * 1024 * 1024
const DOC_LIMIT = 20 * 1024 * 1024
/** 提取产物塞进对话的最大字符数(防撑爆上下文) */
const MAX_CHARS = 120_000
const PDF_MAX_PAGES = 200
const XLSX_MAX_SHEETS = 5
const XLSX_MAX_ROWS = 300

const TEXT_EXT =
  /\.(txt|md|markdown|log|trn|jou|py|pyw|c|cc|cpp|h|hpp|cs|java|js|jsx|ts|tsx|json|xml|yml|yaml|toml|ini|cfg|conf|csv|tsv|scm|inp|sh|bat|cmd|ps1|m|f|for|html|css|sql|rst|tex)$/i

const extOf = (name: string) => {
  const i = name.lastIndexOf('.')
  return i >= 0 ? name.slice(i).toLowerCase() : ''
}

/** 文件名转义,防 </attachment> 注入 */
const safeName = (name: string) => name.replace(/[<>"\n]/g, '_')

const truncatedNote = (note: string) => `\n\n[注意:${note}]`

async function extractPdf(file: File): Promise<string> {
  const pdfjs = await import('pdfjs-dist')
  const workerUrl = (
    (await import('pdfjs-dist/build/pdf.worker.min.mjs?url')) as {
      default: string
    }
  ).default
  pdfjs.GlobalWorkerOptions.workerSrc = workerUrl

  const data = new Uint8Array(await file.arrayBuffer())
  const doc = await pdfjs.getDocument({ data }).promise
  const pages = Math.min(doc.numPages, PDF_MAX_PAGES)
  let out = `PDF 文档,共 ${doc.numPages} 页${pages < doc.numPages ? `(仅提取前 ${pages} 页)` : ''}\n`
  for (let i = 1; i <= pages; i++) {
    const page = await doc.getPage(i)
    const tc = await page.getTextContent()
    out +=
      tc.items
        .map((it) => ('str' in it ? it.str + ((it as { hasEOL?: boolean }).hasEOL ? '\n' : '') : ''))
        .join('')
        .trimEnd() + '\n\n'
    if (out.length > MAX_CHARS) {
      out = out.slice(0, MAX_CHARS)
      out += truncatedNote(`内容超过 ${MAX_CHARS} 字符已截断`)
      break
    }
  }
  await doc.cleanup()
  return out
}

async function extractDocx(file: File): Promise<string> {
  const mammoth = await import('mammoth')
  const { value } = await mammoth.extractRawText({
    arrayBuffer: await file.arrayBuffer(),
  })
  return value.length > MAX_CHARS
    ? value.slice(0, MAX_CHARS) + truncatedNote(`内容超过 ${MAX_CHARS} 字符已截断`)
    : value
}

async function extractXlsx(file: File): Promise<string> {
  const XLSX = await import('xlsx')
  const wb = XLSX.read(await file.arrayBuffer(), { type: 'array' })
  const sheetNames = wb.SheetNames.slice(0, XLSX_MAX_SHEETS)
  let out = `Excel 工作簿,工作表:${sheetNames.join('、')}${wb.SheetNames.length > sheetNames.length ? `(仅提取前 ${XLSX_MAX_SHEETS} 个)` : ''}\n`
  for (const name of sheetNames) {
    const ws = wb.Sheets[name]
    const csv = XLSX.utils.sheet_to_csv(ws, { FS: '\t', blankrows: false })
    const lines = csv.split('\n')
    out += `\n## Sheet: ${name}\n`
    out += lines.slice(0, XLSX_MAX_ROWS).join('\n')
    if (lines.length > XLSX_MAX_ROWS) {
      out += truncatedNote(`Sheet「${name}」共 ${lines.length} 行,仅取前 ${XLSX_MAX_ROWS} 行`)
    }
    if (out.length > MAX_CHARS) {
      out = out.slice(0, MAX_CHARS) + truncatedNote(`内容超过 ${MAX_CHARS} 字符已截断`)
      break
    }
  }
  return out
}

/**
 * 附件适配器:面向 Fluent 工作流。
 * - 文本类(.trn/.jou/.py/.log/.csv/.md/.json 等)直接读,≤2MB
 * - PDF(≤20MB,提取文字层,扫描版无文字层时结果为空会提示)
 * - Word .docx(≤20MB,mammoth 提取纯文本;旧版 .doc 请另存为 .docx)
 * - Excel .xlsx/.xls(≤20MB,每表前 300 行转制表符文本)
 * - 图片/其它二进制:明确报错(视觉模型接入后再放开)
 */
export class FluentTextAttachmentAdapter implements AttachmentAdapter {
  accept = '*'

  async add({ file }: { file: File }): Promise<PendingAttachment> {
    const ext = extOf(file.name)
    const isDoc = ext === '.pdf' || ext === '.docx' || ext === '.xlsx' || ext === '.xls'
    const limit = isDoc ? DOC_LIMIT : TEXT_LIMIT
    if (file.size > limit) {
      throw new Error(
        `「${file.name}」过大（${(file.size / 1024 / 1024).toFixed(1)}MB），${isDoc ? '文档类' : '文本类'}附件上限 ${limit / 1024 / 1024}MB`,
      )
    }
    return {
      id: crypto.randomUUID(),
      type: 'document',
      name: file.name,
      contentType: file.type || 'text/plain',
      file,
      status: { type: 'requires-action', reason: 'composer-send' },
    }
  }

  async remove(): Promise<void> {}

  async send(
    attachment: PendingAttachment,
    options?: { signal?: AbortSignal },
  ): Promise<CompleteAttachment> {
    options?.signal?.throwIfAborted()
    const file = attachment.file
    const name = attachment.name
    const ext = extOf(name)

    let text: string
    let kind = 'text'
    if (ext === '.pdf') {
      kind = 'pdf'
      text = await extractPdf(file)
      if (text.replace(/[\s\w\W]/g, '').length < 20 && text.trim().split('\n').length <= 2) {
        // 文字层几乎为空 → 大概率扫描版
        text += truncatedNote('该 PDF 几乎没有文字层,可能是扫描版/图片型 PDF,无法提取文本')
      }
    } else if (ext === '.docx') {
      kind = 'docx'
      text = await extractDocx(file)
    } else if (ext === '.xlsx' || ext === '.xls') {
      kind = 'xlsx'
      text = await extractXlsx(file)
    } else if (ext === '.doc') {
      throw new Error('「' + name + '」是旧版 .doc 格式,请先用 Word 另存为 .docx 再拖入')
    } else if (file.type.startsWith('image/')) {
      throw new Error(`「${name}」是图片,目前暂不支持(视觉模型接入后开放),可拖入 .trn/.log/.pdf/.docx/.xlsx 等文件`)
    } else if (TEXT_EXT.test(name) || file.type.startsWith('text/')) {
      text = await file.text()
      if (text.slice(0, 2000).includes('\0')) {
        throw new Error(`「${name}」是二进制文件,无法按文本读取`)
      }
      if (text.length > MAX_CHARS) {
        text = text.slice(0, MAX_CHARS) + truncatedNote(`内容超过 ${MAX_CHARS} 字符已截断`)
      }
    } else {
      throw new Error(`「${name}」暂不支持的文件类型,可拖入文本类 / .pdf / .docx / .xlsx`)
    }

    options?.signal?.throwIfAborted()
    return {
      ...attachment,
      status: { type: 'complete' },
      content: [
        {
          type: 'text',
          text: `<attachment name="${safeName(name)}" type="${kind}">\n${text}\n</attachment>`,
        },
      ],
    }
  }
}
