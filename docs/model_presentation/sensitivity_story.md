# Sensitivity story

主图使用最终视觉证据 `reports/visual_evidence/final/F4_parameter_perturbation.svg`，辅以三句话：

1. 在当前有限参数网格内，ABL=3.5625、HOT=0.375、Gap=1.125 基本不变；这只是当前公共缩放开发切片的结构现象。
2. 支持度更敏感：有效权重可从 16 降到 6，假设范围下为 0.4–16；有效覆盖率为 0.005714–0.228571。
3. context 惩罚无法由当前切片单独识别，因为可判读记录没有 `context_truncated=true` 变异；这部分必须标为 sensitivity-only。

这不是统计置信区间，也不证明参数已校准。
