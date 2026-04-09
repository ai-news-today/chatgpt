# 文章生成后评估（`article_seo_eval.py`）

用于 **Hugo / Markdown 正文**在生成或改写后的**可量化质检**，并与**基线快照**做**回归对比**。  
与 `seo_skill_threshold_check.py`（校验 `SKILL.md` 技能文档）**职责不同**，请勿混用。

---

## 1. 何时使用

- 新文章定稿前：是否满足站点默认的**结构 / 可读性 / 信息密度代理指标**。
- 改版或重生成后：与上一版通过的**基线 JSON**对比，发现「变差」的维度（回归）。

---

## 2. 快速命令

```bash
# 单篇评估（人类可读摘要 + 退出码）
python3 .agents/skills/scripts/article_seo_eval.py \
  --file content/articles/chatgpt-plus-deep-usage-2026.en.md

# JSON 完整报告（CI / 脚本解析）
python3 .agents/skills/scripts/article_seo_eval.py \
  --file content/articles/your-article.en.md \
  --json

# 自定义阈值（复制 article_eval_defaults.json 后修改路径）
python3 .agents/skills/scripts/article_seo_eval.py \
  --file content/articles/your-article.en.md \
  --defaults path/to/your_article_eval_defaults.json
```

### 2.1 基线（回归）

```bash
# 首次：把当前指标存成基线（Golden 版本或上一版已上线文）
python3 .agents/skills/scripts/article_seo_eval.py \
  --file content/articles/chatgpt-plus-deep-usage-2026.en.md \
  --save-baseline baselines/chatgpt-plus-deep-usage-2026.en.json

# 之后每次改写同一主题文章后对比
python3 .agents/skills/scripts/article_seo_eval.py \
  --file content/articles/chatgpt-plus-deep-usage-2026.en.md \
  --baseline baselines/chatgpt-plus-deep-usage-2026.en.json \
  --json
```

- **`regression_checks`** 非空：相对基线出现**显著变差**（幅度见 `article_eval_defaults.json` 的 `regression`）。
- **`relative_fail`**：相对下降超过该比例 → 记为 **fail** 级回归。
- **`relative_warn`**：超过该比例 → **warn**。

**越大越好**的指标（如 `intro_word_count`、`token_count`、`list_line_ratio` 等）：当前值**明显低于**基线为劣化。  
**越小越好**的指标（`long_paragraph_count`、`max_paragraph_words`）：当前值**明显高于**基线为劣化。

### 2.2 退出码

| `status` | 默认退出码 | `--fail-on-warn` |
|----------|------------|------------------|
| `PASS`   | 0          | 0                |
| `WARN`   | 0          | 1                |
| `FAIL`   | 1          | 1                |

---

## 3. 指标说明（`metrics`）

| 字段 | 含义 |
|------|------|
| `structure_parser` | `markdown-it-py`：已安装 `requirements-seo-check.txt` 中的解析器，用 **CommonMark token 流**抽标题；`builtin-atx`：无依赖时的行解析回退（与 `seo_skill_threshold_check.py` 一致） |
| `language` | `zh` 或 `en`（CJK vs 拉丁字母启发式） |
| `heading_count` | `##`～`######` 标题数量（正文内；Hugo 常无 `#`） |
| `intro_word_count` | 第一个 `##` **之前**的正文词数（首屏/开篇代理） |
| `list_line_ratio` | 列表行数 / 非空行数 |
| `max_paragraph_words` / `avg_paragraph_words` | 按空行分段后的词数（中文为 jieba 词或字片） |
| `long_paragraph_count` | 超过 `long_paragraph_word_threshold`（默认 120）的段数 |
| `eval_signal_weighted_total` | 与技能脚本一致的**评估型**加权（`%`、`(0-3)`、小分制比率） |
| `unique_token_ratio` | 唯一词元 / 总词元 |
| `link_count` | `[text](url)` 形式链接数量 |

---

## 4. 默认阈值（`article_eval_defaults.json`）

可在副本中修改 `thresholds`，例如：

- 提高 `intro_word_count_min`：强制更充实的开篇。
- 提高 `eval_signal_weighted_min`：强制更多可量化表述（报价类、对比类文章常用）。
- 调整 `regression.relative_warn` / `relative_fail`：收紧或放宽回归敏感度。

默认文件中 `eval_signal_weighted_min` 为 **0**，避免叙事类文章被误伤；若你的体裁要求数据与比例，请将该 `min` 改为 `1.0` 或更高。

---

## 5. 可选依赖（`requirements-seo-check.txt`）

**为何默认不强制安装**：许多环境（如 PEP 668 系统 Python）不便全局装包，脚本须 **零依赖可跑**；装上后校验**更准**。

| 包 | 作用 |
|----|------|
| **markdown-it-py** | 标题 **AST 级**解析（内联加粗、链接等与源码行解析不一致时，与 `builtin-atx` 结果可能不同） |
| **jieba** | 中文 **词级**分词；未装时为 CJK 字片，词数类指标仅作粗参考 |

```bash
python3 -m pip install -r .agents/skills/scripts/requirements-seo-check.txt
```

文章评估脚本 **`article_seo_eval.py` 已与技能校验脚本共用上述逻辑**：装包后 `metrics.structure_parser` 会显示 `markdown-it-py`，否则为 `builtin-atx`。

---

## 6. 如何根据结果优化

| 现象 | 建议 |
|------|------|
| `intro_word_count` 低于阈值 | 开篇先给结论或范围，再展开；避免空洞铺垫 |
| `list_line_ratio` 过低 | 步骤、对比、清单改为列表 |
| `long_paragraph_count` 高 | 拆段、加 `###` 小标题 |
| `eval_signal_weighted_total` 低（且你提高了 min） | 补充价格、比例、步骤序号、明确对比 |
| 回归：关键指标相对基线下降 | 对比 Git diff，优先恢复被删的列表、链接与数据段 |

---

## 7. 与技能校验脚本的关系

| 脚本 | 对象 | 目的 |
|------|------|------|
| `seo_skill_threshold_check.py` | `SKILL.md` | 技能文档结构是否合规 |
| `article_seo_eval.py` | 文章 `.md` | 生成物质量与回归 |
