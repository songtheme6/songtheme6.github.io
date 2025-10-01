# PDF Library Starter (GitHub Pages + Actions)

这是一个可直接 Fork 使用的 GitHub 仓库模板：
- 使用 `pdfs/` 目录维护你的 PDF 文件与子目录
- 通过 GitHub Actions 自动生成 `docs/meta.json`（PDF 元数据）与封面图
- 自动将 `pdfs/` 同步复制到 `docs/pdfs/`，供 GitHub Pages 在线访问
- 前端 `docs/index.html` 提供：目录树折叠、搜索、封面卡片、内嵌 PDF.js 阅读
- 内嵌阅读器位于 `docs/pdf-viewer/`，支持翻页与缩放（基于 PDF.js CDN）

## 一键使用步骤

1. Fork 本仓库到你的账户。
2. 在仓库 Settings → Pages：
   - Build and deployment → Source 选择 "Deploy from a branch"
   - 分支选择 `main`，文件夹选择 `/docs`，保存。
3. `pdfs/` 目录中放入你的 PDF（支持子目录）。
4. 提交并 push 到 `main` 分支。
5. GitHub Actions 将自动：
   - 安装环境（poppler、python）
   - 扫描 `pdfs/`
   - 生成封面 PNG 到 `docs/covers/`
   - 复制 PDF 到 `docs/pdfs/`
   - 生成 `docs/meta.json`
6. 几分钟后打开你的 GitHub Pages 网址（仓库主页 "Environments" 或 Pages 设置里有链接），即可在线浏览 PDF 目录与阅读。

> 注意：首次运行需要几分钟时间生成封面与元数据。后续仅对变更过的文件再生成。

## 目录结构

```
your-repo/
├── pdfs/
│   └── (你的 PDF 与子目录)
├── docs/
│   ├── index.html        # 首页（目录树 + 搜索 + 封面 + 内嵌阅读器）
│   ├── meta.json         # 由 Action 自动生成（初始为空对象）
│   ├── pdf-viewer/
│   │   └── index.html    # PDF.js 内嵌阅读器（CDN）
│   ├── covers/           # 由 Action 生成的封面图
│   └── pdfs/             # 由 Action 复制的 PDF（与 pdfs/ 同结构）
└── .github/
    ├── workflows/
    │   └── pdf-meta.yml
    └── scripts/
        └── build_meta.py
```

## 功能说明

- 目录树：自动根据 `docs/meta.json` 构建，支持折叠/展开
- 搜索：检索文件名与相对路径
- 封面：从 PDF 第 1 页生成 PNG 作为卡片封面
- 阅读：点击文件在右侧内嵌 PDF.js 阅读，支持翻页/缩放

## 本地预览（可选）

你可以在本地直接打开 `docs/index.html` 进行预览（部分功能如封面取决于 `docs/meta.json` 是否已生成）。

## 自定义

- 样式：可在 `docs/index.html` 中修改 CSS 变量与样式。
- 行为：可在 `docs/index.html` 中调整目录树和搜索逻辑。

## 常见问题

- 看不到文件或封面：
  - 确认 `pdfs/` 下已提交 PDF 文件
  - 等待 Actions 完成（仓库 "Actions" 标签页）后刷新 Pages
- 部分 PDF 生成封面失败：
  - 尝试在本地检查是否可以用 `pdftoppm` 转换；或者将该 PDF 重新导出

## 许可证

MIT
