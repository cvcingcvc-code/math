# S4 数据审计与队列重建报告

## 输入清点

已重新读取 `work/extracted/` 下全部 Excel 与 Word 文件：13 个数据文件（工作簿/Word），并读取全部非临时 xlsx 工作表。Excel 锁文件未作为数据源读取：2 个；路径记录于本报告。

| 文件 | 类型 | 内容/用途 |
|---|---|---|
| `2025秋-数学模型-课程反馈详情记录.docx` | .docx | Word text 179963 chars; 1 images |
| `2025秋-数学模型-课程智能体“探知侠”使用讨论.docx` | .docx | Word text 350765 chars; 532 images |
| `2025秋-数学模型-课程智能体“数模全才”使用讨论.docx` | .docx | Word text 474261 chars; 404 images |
| `2025秋-数学模型-问答记录导出20260502导出_已标注_已更新.xlsx` | .xlsx | 智能体使用次数 (298 rows x 6 cols); 问答记录 (846 rows x 5 cols) |
| `请大家对本学期线上线下融合授课-参与数据.xlsx` | .xlsx | 话题概览 (8 rows x 2 cols); 学生参与情况 (135 rows x 8 cols) |
| `请大家对本学期线上线下融合授课.docx` | .docx | Word text 91502 chars; 1 images |
| `课程智能体“探知侠的引导学习空间-参与数据.xlsx` | .xlsx | 话题概览 (8 rows x 2 cols); 学生参与情况 (135 rows x 8 cols) |
| `课程智能体“探知侠的引导学习空间.docx` | .docx | Word text 85949 chars; 5 images |
| `课程智能体“数学模型匹配专业知识点-参与数据.xlsx` | .xlsx | 话题概览 (8 rows x 2 cols); 学生参与情况 (135 rows x 8 cols) |
| `课程智能体“数学模型匹配专业知识点.docx` | .docx | Word text 130096 chars; 6 images |
| `课程智能体“逆行侠的探索空间”-参与数据.xlsx` | .xlsx | 话题概览 (8 rows x 2 cols); 学生参与情况 (134 rows x 6 cols) |
| `课程智能体“逆行侠的探索空间”.docx` | .docx | Word text 97029 chars; 1 images |
| `问答记录导出0919_已更新.xlsx` | .xlsx | 问答记录 (1926 rows x 6 cols) |

临时锁文件：
- `work\extracted\黑客松赛题-关老师\附件2-2025 年秋季学期脱敏数据\~$2025秋-数学模型-问答记录导出20260502导出_已标注.xlsx`
- `work\extracted\黑客松赛题-关老师\附件3-2026年春季学期脱敏数据\~$2026春-数学模型-智能体-探知侠-逆行侠-数模匹配知识点-问答记录20260502导出_已分类_已统计.xlsx`

## 队列定义与事实依据

- **2025 秋**：采用带“2025秋”标记的课程问答工作簿 `问答记录` sheet。课程讨论 Word 记录标示课程为数学模型，参与班级为九龙湖班、四牌楼班；个体班级没有与问答学号对应的交叉表，因此记录级 class 标为“班级未映射”。问答观察期按该工作簿实际时间确定。
- **2026 春**：从四份“参与数据”工作簿中只取 `是否参与=是` 的学号，按并集纳入；四名单的肯定参与人数分别为 115, 118, 124, 117，并集为 131 人。再在聚合问答记录中限定学号属于该并集，且时间落在这些已匹配记录的观测活动窗 2026-03-19 至 2026-07-27。此窗是数据观测边界，不声称是教务规定的完整学期窗。
- 春季记录保留 `问答来源` 原值；并集命中记录包含多个来源，来源不作为智能体身份的替代。春季没有可靠的逐学生班级字段映射时，使用 Word/名单所确认的“数学模型2026春季班”课程口径。
- Fall cohort has no complete class roster in the interaction workbook; Word discussion participant counts are not treated as a log roster because they are discussion exports and do not provide a validated one-to-one course roster join.

## 秋季原始到最终样本流

- 原始非空数据行：845。
- 纳入 cohort 且有文本内容的原始记录：824；覆盖学号 295 人。
- 排除：21 行。
- 拆分后 turn-level clean 行：5019；角色计数：{'student': 2512, 'ai': 2507}。
- 观察日期：2025-10-09 15:50:24 至 2026-02-05 22:07:58。

## 春季原始到最终样本流

- 聚合问答原始非空数据行：1925，学号去重 528 人；原表整体日期跨越 2024–2026，不整表纳入。
- 四份春季肯定参与名单并集：131 人；聚合日志命中 482 行，109 人。
- 限定观测活动窗且文本可用后纳入：401 行，覆盖 106 人；拆分后 clean turns 2009 行。
- 观测活动窗：2026-03-19 至 2026-07-27；纳入记录日期：2026-03-19 14:55:02 至 2026-07-27 14:25:54。
- 纳入来源分布：{'AI智能体': 324, 'AI学伴': 73, 'AI助教': 4}。

## 排除原因及数量

| 学期 | 原因 | 行数 |
|---|---|---:|
| 2025_fall | `url_only_unretrieved_content` | 21 |
| 2026_spring | `empty_interaction_text` | 13 |
| 2026_spring | `outside_affirmative_spring_rosters` | 1443 |
| 2026_spring | `url_only_unretrieved_content` | 68 |

完整逐行处置见 `data/processed/exclusion_log.csv`。其中所有原始 Excel 行号以 workbook、sheet、Excel row 组成 `source_row_id`，不静默删除。

## 主体与智能体识别

- Clean utterances 共 7,028 条；自动 `speaker_role=unknown` 为 0（0.0%），`system` 显式标记也为 0。另有 4 条（0.06%）因同一序列出现连续学生标记而降为低置信（0.65），均保留为 marker 指示的 student 并进入人工审计与 Pilot；自动角色尚未由人工审计验证。
- agent_type `unknown`：740/7,028 turns（10.5%）；按独立原始 session 计为 167/1,225（13.6%）。秋季优先使用原表显式智能体字段，春季优先使用对话中智能体自报名称；仅有泛化来源类别时不推断具体 agent。
- 明确 Q/A 标记的主体置信度设为 0.98，system marker 0.95，未解析文本 0.20；这些是解析规则置信度，不是经人工审计校准的概率。

## speaker 审计样本与 Pilot 构成

- `speaker_audit.csv`：120 条分层审计记录，覆盖学期、自动主体角色、低置信角色序列异常；人工判定列留空待审。
- `pilot_sample.csv`：140 条候选文本；按学期、智能体、长度、问题形式、表面线索和 speaker confidence 覆盖抽样。
- Pilot 学期分布：2025 秋 70，2026 春 70。
- Pilot speaker 分布：student 140；其中低置信 4 条。无未解析角色文本可抽入 Pilot。
- Pilot agent 分布：探知侠 65、逆行侠 18、数模全才 23、数模匹配 5、AI 学伴 6、unknown 23。
- Pilot 长度分层：<50 字 79、50–199 字 32、≥200 字 29；问题形式：含问号 39、请求/疑问句式 23、陈述/其他 78。表面线索：候选低阶 16、候选中阶 27、候选高阶 24、混合线索 24、无明显线索 49。
- `possible_bloom_surface_signal` 仅用于 Pilot 抽样覆盖；它不是 Bloom 标注，更不是 `Student Evidence` 标签。最终规则等待 annotation manual。

## 与 S3 假设冲突或形成限制的事实

- 春季聚合日志并非天然的 2026 春季队列：它混有其他时间、来源和非名单学生；按四份明确“参与=是”的名单和日志可观测窗过滤后，才形成可追溯子队列。
- 春季参与名单肯定参与学号并集为 131 人，日志仅匹配 109 人，仍有名单覆盖与日志覆盖缺口；不能将未匹配者当作零交互/零学习。
- 秋季问答导出每行可含多轮学生与智能体交替发言，按 Excel 行计数会低估交互轮次；但 session id 原始数据未提供，本处理用原始导出行作为保守 session proxy。
- 秋季有四种显式 agent 标签（含少量“思政点灯人”），不只 S3 举例的探知侠/逆行侠；跨学期 agent taxonomy 并不完全一致。
- 课程反馈/使用讨论 Word 文档包含自述性反馈和主题帖子，不能直接作为独立学习成效或标准答案；其中个体班级与日志学号无法完整映射。
- 时间戳和来源字段并不提供真实连续学习时长；同一学号、同一时间邻近记录是否属于同一 session 仍需平台定义确认。
- 智能体名称识别基于显式字段或文本自称；未自报名称的 spring 记录需保持 unknown，不能按文字风格硬分类。

## 可能改变研究方向的证据

- 目前最强的实证限制是：**没有独立于智能体对话的学习结果测量，且春季 roster 中约有 22 名肯定参与学生未在聚合问答日志匹配到记录**。因此目前可研究的是可观察交互与标注可信度，不能把对话层级变化解释为能力成长或 AI 因果增量。
- 如果后续人工主体审计发现 Q/A 前缀并不稳定地对应实际说话者，或 spring agent identity 大量无法核实，则需要进一步收窄到“记录文本的结构化描述”，而不是将其解释为学生/智能体真实分工。

## 输出文件

- `data/processed/cohort_flow.csv`：原始、纳入、排除、turn 数流转。
- `data/processed/clean_interactions.csv`：一行一个解析 utterance，含来源行 ID、角色、文本、学期、智能体和置信度。
- `data/processed/exclusion_log.csv`：每条原始问答数据行的纳入/排除处置及理由。
- `data/processed/speaker_audit.csv`：人工说话主体审计样本，含待填审计字段。
- `data/processed/pilot_sample.csv`：Bloom Pilot 候选样本，等待 annotation manual。
