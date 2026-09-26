# WorkBuddy B 标注质量审计

- 文件：`data/annotations/workbuddy/pilot_worksheet_B_submitted.csv`
- 行数：70；record_id 唯一：是
- SHA-256：`089331175f37eb66b4baec311e2e40e7294421050b6240af6b6a98fc44551fc6`
- 编码：UTF-8 BOM
- 必填字段缺失：{"speaker_role_check": 0, "task_bloom": 0, "task_confidence": 0, "student_evidence_bloom": 0, "evidence_confidence": 0, "confidence": 0, "reason": 0, "ambiguity_type": 0, "needs_second_review": 0}
- 条件字段缺失：{"task_source": 0, "task_actor": 0, "evidence_span": 0, "content_relation": 0, "correctness": 0, "prompt_induced": 0}
- 受控值非法：无

## 边界

此审计只确认 B 表可读取性与字段质量，不把 B 表当作冻结 B010 的 R1/R2，不计算正式一致性系数，不产生 Formal AIV 或学生排名。
