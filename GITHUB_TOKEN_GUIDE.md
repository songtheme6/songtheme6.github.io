# GitHub Token 使用指南

## 如何获取 GitHub Token

### 1. 登录 GitHub
访问 [GitHub.com](https://github.com) 并登录你的账户

### 2. 进入设置页面
- 点击右上角头像
- 选择 "Settings"

### 3. 创建 Personal Access Token
- 在左侧菜单中找到 "Developer settings"
- 点击 "Personal access tokens" → "Tokens (classic)"
- 点击 "Generate new token" → "Generate new token (classic)"

### 4. 配置 Token 权限
填写以下信息：
- **Note**: `PDF Library File Manager` (或任意描述)
- **Expiration**: 选择合适的时间（建议 90 days 或 No expiration）
- **Scopes**: 勾选以下权限：
  - ✅ `repo` (完整仓库访问权限)
    - ✅ `repo:status`
    - ✅ `repo_deployment`
    - ✅ `public_repo`
    - ✅ `repo:invite`
    - ✅ `security_events`

### 5. 生成并复制 Token
- 点击 "Generate token"
- **重要**: 立即复制生成的 token（以 `ghp_` 开头）
- 保存到安全的地方，页面刷新后将无法再次查看

## 如何使用

### 1. 在文件管理器中输入 Token
- 点击 "📁 文件管理" 按钮
- 在 "GitHub Token" 输入框中粘贴你的 token
- Token 会自动保存到浏览器本地存储

### 2. 功能说明

#### 📁 上传文件
- 拖拽 PDF 文件到上传区域，或点击选择文件
- 选择目标目录（可选）
- 文件会自动上传到 GitHub 仓库

#### 📁 创建目录
- 输入目录名称
- 点击 "📁 创建新目录"
- 新目录会出现在 pdfs/ 下

#### 🗑️ 删除文件
- 在文件列表中点击 "🗑️ 删除" 按钮
- 确认删除操作
- 文件会从 GitHub 仓库中删除

#### 🔄 刷新
- 点击 "🔄 刷新" 更新文件列表

#### 💾 保存
- 点击 "💾 保存" 触发 GitHub Actions
- Actions 会自动生成封面和更新 meta.json
- 等待几分钟后刷新页面查看更新

## 安全注意事项

1. **Token 安全**：
   - 不要将 token 分享给他人
   - 定期更换 token
   - 如果怀疑泄露，立即删除并重新生成

2. **权限最小化**：
   - 只给必要的权限
   - 定期检查 token 权限

3. **本地存储**：
   - Token 保存在浏览器本地存储中
   - 清除浏览器数据会删除保存的 token

## 故障排除

### 常见错误

1. **401 Unauthorized**
   - 检查 token 是否正确
   - 确认 token 有 repo 权限

2. **403 Forbidden**
   - 检查仓库权限
   - 确认 token 未过期

3. **404 Not Found**
   - 检查仓库名称是否正确
   - 确认仓库存在且可访问

### 获取帮助
如果遇到问题，可以：
1. 检查浏览器控制台错误信息
2. 确认 GitHub API 状态
3. 重新生成 token 并重试
