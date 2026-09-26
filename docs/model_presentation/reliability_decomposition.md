# Reliability decomposition

| 组件 | 定义 | 人话 | 示例 |
|---|---|---|---|
| Observable gate | `I(y_i∈L1..L6)` | 有没有可判读的学生证据？ | P072 为 0，因此不评分 |
| Confidence | `c_i∈{1,.75,.5}` | 标注者对这一判断有多确定？ | medium → 0.75 |
| Prompt risk | `(1−λ_prompt p_i)` | 证据是否可能由 AI 提示诱发？ | `p_i=1, λ=.5`，乘 0.5 |
| Context risk | `(1−λ_context t_i)` | 上下文是否被截断？ | `t_i=1, λ=.5`，乘 0.5 |

例：P033 为 L6、medium、prompt-induced、未截断：`w=.75×(1−.5)=.375`。因此 raw evidence 仍为 L6，但只有 0.375 的有效支持。

**边界：** 当前 16 条可判读证据全部 `prompt_induced=true` 且 `context_truncated=false`；prompt/context 独立惩罚尚未被数据识别，只能作开发版敏感性分析。
