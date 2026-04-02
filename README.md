# ChatGPT News Today

一个基于 Hugo + Blowfish 的中英双语站点，聚焦 ChatGPT 信息与新闻。

## 技术栈

- Hugo (Extended)
- Blowfish（Hugo Module）
- GitHub Pages（GitHub Actions）

## 本地开发

```bash
cd /Users/xxx/home_work_space/chatgpt
hugo server
```

## 常见报错与排查（重要）

### 1) `module "blowfish" not found in themes/blowfish`

原因：Hugo 在按本地主题目录查找，而不是按 Hugo Module 加载。  
正确配置：

- `config/_default/module.toml` 必须是：

```toml
[[imports]]
path = "github.com/nunocoracao/blowfish/v2"
```

- `hugo.toml` 不要再写 `theme = "blowfish"`（避免被当作本地主题目录）。

### 2) `no matching versions for query "upgrade"`

原因：模块路径用了 `github.com/nunocoracao/blowfish`（缺少 `/v2`），`go get ...@upgrade` 无法解析有效版本。  
修复：把模块路径改成 `github.com/nunocoracao/blowfish/v2`。

### 3) `Unable to locate config file or config directory`

原因：命令不是在项目根目录执行。  
修复：

```bash
cd /Users/xxx/home_work_space/chatgpt
hugo server --source "/Users/xxx/home_work_space/chatgpt"
```

### 4) Go 版本过低导致模块/工具失败

错误示例：`go command is too old (go1.20.x)`  
要求：Go >= 1.21（建议更高版本）。

```bash
brew upgrade go
go version
```

## 推荐启动顺序（首次）

```bash
cd /Users/xxx/home_work_space/chatgpt
go version
hugo version
hugo mod graph
hugo server
```

## 常见操作文档

### 1) 调整首页布局（page/profile/hero/card）

编辑 `config/_default/params.toml`：

```toml
[homepage]
layout = "card"
showRecent = true
showRecentItems = 6
cardView = true
cardViewScreenWidth = false
```

参考文档：[Blowfish 主页布局](https://blowfish.page/zh-cn/docs/homepage-layout/)

### 1.1) 切换主题配色（黑蓝新闻风）

编辑 `config/_default/params.toml`：

```toml
colorScheme = "chatgptnews"
```

当前已提供三套配色：

- `chatgptnews`：平衡版（默认）
- `chatgptnews-dark`：更强对比、科技感更明显
- `chatgptnews-soft`：更柔和、长时间阅读更舒适

配色文件位置：

- `assets/css/schemes/chatgptnews.css`
- `assets/css/schemes/chatgptnews-dark.css`
- `assets/css/schemes/chatgptnews-soft.css`

AI 背景光效在 `assets/css/custom.css`，如需关闭可清空该文件。

### 2) 配置导航栏与二级菜单

分别编辑：

- `config/_default/menus.zh-cn.toml`
- `config/_default/menus.en.toml`

一级菜单与二级菜单示例：

```toml
[[main]]
name = "时间线"
weight = 30

[[main]]
name = "模型发布"
parent = "时间线"
pageRef = "/timeline/model-releases"
weight = 31
```

参考文档：[Blowfish 配置（语言与菜单）](https://blowfish.page/zh-cn/docs/configuration/)

### 3) 新增文章并让首页卡片自动展示

1. 在 `content/articles/` 新建双语文章（如 `xxx.zh-cn.md` 和 `xxx.en.md`）。
2. Front matter 至少包含：`title`、`date`、`description`、`summary`。
3. 确认 `params.toml` 中包含：

```toml
mainSections = ["articles"]
```

这样首页 `showRecent` 区域会自动读取文章并显示卡片。

### 4) 新增时间线子栏目

按目录添加双语 `_index` 文件，例如：

- `content/timeline/model-releases/_index.zh-cn.md`
- `content/timeline/model-releases/_index.en.md`

然后在中英 `menus.*.toml` 中追加对应菜单项。

### 5) 本地验证清单

```bash
cd /Users/xxx/home_work_space/chatgpt
hugo mod graph
hugo
hugo server
```

检查项：

- 首页是否为 card 布局
- 首页是否展示最近文章卡片
- 导航与二级菜单是否可点击且无 404
- 中英页面切换是否正常

## 部署

推送到 `main` 后，GitHub Actions 会自动构建并发布到 GitHub Pages。

### GitHub Pages（GitHub Actions）操作流程

1. 打开仓库页：`Settings -> Pages`
2. 在 `Build and deployment` 里选择 `GitHub Actions`（而不是 `Deploy from a branch`）
3. 保存并开启 Pages
4. 等待 1-2 分钟后，再触发部署：
   - 推送一次到 `main`，或
   - 手动在 `Actions` 里运行本仓库的 `Deploy Hugo site to Pages`（`workflow_dispatch`）

部署失败排查（常见：404 Not Found）

- 如果看到类似 `Get Pages site failed / Not Found (pages#get-a-pag...`，通常是因为 Pages 站点还没在 `Settings -> Pages` 里被启用，或尚未切到 `GitHub Actions` 作为部署来源。
- 先确认第 1-3 步已完成，再重新触发 workflow。
- 若仍失败，可以检查 workflow 里 `actions/configure-pages@v5` 这一步是否配置了 `enablement`（有些场景需要显式开启 enablement）。
