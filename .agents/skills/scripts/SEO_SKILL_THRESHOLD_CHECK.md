# SEO Skill Threshold Check（`seo_skill_threshold_check.py`）说明

本文档说明检测脚本的**评估目标**、**指标含义**、**如何解读结果**、**如何根据结果优化**，以及 **AST / 分词**相关行为与依赖。

---

## 1. 工具定位

- **主要用途**：校验 `seo-audit` 技能的 `SKILL.md` 是否包含 2026 版要求的**章节结构**、**报告输出字段**、以及一定强度的**可量化评估信号**（百分比、分制等）。
- **次要用途**：对任意 Markdown 做**语言检测（中/英）**与**分词级统计**（用于观察信息密度、篇幅结构；**不等于**搜索引擎真实排名）。

若把本脚本用于**普通文章**（如 `content/articles/*.md`），会出现大量「规则未命中」，这是**预期现象**：文章不应复制技能文档里的固定标题与报告字段名。

---

## 2. 评估流程概览

1. **预处理**：剥离 YAML Front Matter（`---` 包裹），避免干扰正文解析。
2. **结构级校验（AST / 结构解析）**  
   - 优先使用 **CommonMark 解析器**（`markdown-it-py`，若已安装）从 token 流提取 **标题节点**（层级 + 纯文本）。  
   - 若未安装，则使用**内置 ATX 标题解析**（跳过 fenced code block），作为**无依赖回退**；语义与「从源码扫 `#` 行」一致，但对复杂内联标记的规范化略弱。
3. **规则匹配**  
   - **标题类规则**：在「提取到的标题文本」上匹配（支持 Emoji、加粗等出现在标题中的情况）。  
   - **正文类规则**：在全文中匹配（如 0–3 分级说明、报告字段模板行）。
4. **评估型数字信号（加权）**  
   - 仅统计更像**指标**的片段（如 `%`、`(0-3)`、小分制比率等），**不把**「2024 年」这类背景年份当作核心信号。
5. **中/英分词统计（辅助）**  
   - **中文**：优先 `jieba` 分词；未安装时对 CJK 做**字符级**回退（指标仍可看趋势，但词级会更粗）。  
   - **英文**：使用正则词元提取（与常见博客统计一致），无需 NLTK。

---

## 3. 指标说明

### 3.1 规则加权（`rule_weight_earned` / `rule_weight_max`）

- 每条规则有固定 **weight**（信息增益、IG 分数字段等权重更高）。
- **`weighted_ratio`** = 已命中规则的权重之和 / 满分权重。
- **默认（weighted 模式）**要求 `weighted_ratio >= --min-weighted-ratio`（默认 **0.85**）。

**含义**：技能文档是否**覆盖**了规定的章节与输出模板。

### 3.2 评估型数字信号（`eval_signal_weighted_total`）

对以下模式赋予权重并求加权和（详见脚本内 `EVAL_PATTERN_WEIGHTS`）：

| 类型 | 示例 | 说明 |
|------|------|------|
| 百分比 | `2.5%`、`95%` | 偏「可量化阈值」 |
| 分制 | `(0-3)`、`0-3 scale` | 与审计打分一致 |
| 小比率 | `3/5`、`80/100` | 排除四位年份内误切片 |

**默认**要求总分 ≥ `--min-eval-weighted`（默认 **6.0**）。

**含义**：文档里是否具备**可复核的量化表述**（弱化「泛泛而谈」）。

### 3.3 兼容计数（`legacy_numeric_signals`）

对任意数字与部分英文分级词的**粗计数**，**仅作参考**，默认**不参与** PASS/FAIL。

### 3.4 结构解析元数据（JSON 中的 `structure`）

| 字段 | 含义 |
|------|------|
| `parser` | `markdown-it-py`：已安装并使用 token 流；`builtin-atx`：内置 ATX 回退 |
| `heading_count` | 提取到的标题数量 |
| `headings_preview` | 前几级标题预览（便于人工核对） |

### 3.5 分词统计（JSON 中的 `token_analysis`）

| 字段 | 含义 |
|------|------|
| `language` | `zh` 或 `en`（由 CJK 与拉丁字母比例启发式判定） |
| `token_count` | 词/词元数量（中文为 jieba 词数或字符数） |
| `unique_token_ratio` | 唯一词元 / 总词元（过低可能暗示重复堆砌；过高需结合篇幅） |
| `avg_token_length` | 英文为平均词长；中文为「词」平均字符数（jieba）或 1（字符回退） |

**含义**：辅助观察**篇幅与词汇多样性**，不是排名因子本身。

---

## 4. 如何解读结果

### 4.1 `status: PASS`

- weighted 模式：`weighted_ratio` 与 `eval_signal_weighted_total` 均达到阈值，且（非 strict 下）允许少量规则按权重折算（由 `--min-weighted-ratio` 控制）。
- `strict` 模式：**每一条**规则都必须命中，且评估型信号仍 ≥ `--min-eval-weighted`。

### 4.2 `status: FAIL`

按优先级排查：

1. **`failed` 列表**：缺哪条模板（补章节或补报告字段说明）。
2. **`eval_signal_ok: false`**：补充显式分制、百分比或可比比率表述（避免堆砌年份）。
3. **`weighted_ratio_ok: false`**：整体覆盖不足，或需调高权重章节。
4. **对普通文章**：若 `failed` 几乎全满，通常说明**测错了对象**——应换用「文章质量」专用流程或人工按 `SKILL.md` 清单评审。

---

## 5. 如何根据结果优化（技能文档）

| 现象 | 建议 |
|------|------|
| 缺「2026 Ranking Focus」等标题 | 在 `SKILL.md` 增加对应 `##` / `###` 标题，措辞可微调，但核心短语建议保留以便检索与校验 |
| `eval_signal` 偏低 | 在技能中写明**可操作的量化口径**（如分制、阈值区间） |
| `structure.parser` 为 `builtin-atx` | 安装 `markdown-it-py` 以获得更稳的标题与内联解析（见 `requirements-seo-check.txt`） |
| 中文 `token_count` 异常低 | 安装 `jieba`；或检查是否大量内容在代码块/HTML 中被排除 |

---

## 6. 依赖安装

```bash
cd .agents/skills/scripts
python3 -m pip install -r requirements-seo-check.txt
```

建议在项目或本机独立 venv 中安装，避免与系统 Python 冲突（PEP 668）。

---

## 7. 常用命令

```bash
# 默认校验 seo-audit SKILL.md
python3 .agents/skills/scripts/seo_skill_threshold_check.py

# JSON 输出（含 structure / token_analysis）
python3 .agents/skills/scripts/seo_skill_threshold_check.py --json

# 全规则必过
python3 .agents/skills/scripts/seo_skill_threshold_check.py --strict

# 指定文件
python3 .agents/skills/scripts/seo_skill_threshold_check.py --file path/to/file.md --json
```

---

## 8. 与「文章 SEO 评估」的边界

本脚本**不**替代：Search Console、抓取日志、外链分析、或整站技术审计。

对**单篇 Markdown 文章**的「信息增益 / 首屏答案密度」等，应以 `SKILL.md` 中的编辑准则做**人工或专用文章脚本**评审；本工具聚焦**技能文件是否齐备、可量化、可自动化校验**。
