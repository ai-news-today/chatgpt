# ChatGPT News Today

一个基于 Hugo + Blowfish 的中英双语站点，聚焦 ChatGPT 信息与新闻。

## 技术栈

- Hugo (Extended)
- Blowfish（Hugo Module）
- GitHub Pages（GitHub Actions）

## 本地开发

```bash
cd /Users/zhangjane/home_work_space/chatgpt
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
cd /Users/zhangjane/home_work_space/chatgpt
hugo server --source "/Users/zhangjane/home_work_space/chatgpt"
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
cd /Users/zhangjane/home_work_space/chatgpt
go version
hugo version
hugo mod graph
hugo server
```

## 部署

推送到 `main` 后，GitHub Actions 会自动构建并发布到 GitHub Pages。
