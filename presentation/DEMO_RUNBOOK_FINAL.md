# 60–90 秒 Demo Runbook

## 主路线（约 75 秒）

| 时间 | 操作 | 口播锚点 |
|---:|---|---|
| 0–15s | 打开首页，停在 `#rq` | 我们研究的是观察结果能否被可靠解释，不是直接证明 AI 增量。 |
| 15–32s | 点击/滚动至 `#model` | 固定链路是 Observed Evidence → Raw Signal → Reliability → Adjusted Evaluation → Support/Coverage → 决策状态。 |
| 32–50s | 进入 `#result`，展示 70/16/54、3.5625/0.375/1.125、coverage 变化 | 分数可以稳定，但有效证据支持会下降；54 是 NO_EFFECTIVE_EVIDENCE，不是 54 个零分。 |
| 50–72s | 进入 `#failure`，选择 P108，切换 prompt 影响或展示结果 | P108 从 Raw=L6 变成 R=0.375、Adjusted=2.25，系统给 LOW_SUPPORT/ABSTAIN，而不是强行接受。 |
| 72–90s | 回到结论或进入 `#limitations` | 结论是 Score Stability ≠ Evidence Support Stability；Human Gate 尚未运行，结论保持 DEVELOPMENT_ONLY。 |

## 交互细节

- P108 固定参数：`C=0.75`、`LP=0.5`、`LC=0.5`、`RAW=6`。
- prompt=true、context=false 时 `w=0.375`，Adjusted=2.25。
- 不现场修改任何论文、Demo 文件或参数源文件。
- 不展示 Demo 中可能引起 M0/M1 口径混淆的“raw”标签作为论文主数字；论文主数字以 `PAPER_NUMBER_LOCK.md` 的 M0/M3 口径为准。

## 离线 Fallback

1. 直接打开 `reports/demo/index.html`；若浏览器策略限制本地文件，则使用项目现有静态服务。
2. 若交互异常，按顺序展示冻结图：F1 → F3 → F4 → F5 → F6。
3. 口播不依赖网络、外部字体或后端状态。
4. 若页面完全不可用，使用本 PPT 第 3、4、5、7、8 页替代 Demo，保持四个口播锚点。

## 现场禁忌

- 不说“AI 提高了学习效果”。
- 不说“RF 赢了”或“手工模型击败 ML”。
- 不说“BTC 证明了交易优势”。
- 不把 54 条 `NO_EFFECTIVE_EVIDENCE` 说成 54 个 0 分。
- 不把 `ABSTAIN` 说成失败。
