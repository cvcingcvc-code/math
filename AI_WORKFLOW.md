# AI_WORKFLOW.md

> 本文件描述 yu 项目当前可用的 AI Coding 工作流。最后更新：2026-09-25。
> 本文件不包含任何 API Key。密钥只保存在用户目录（`.codex` / `.local/share/opencode`），不在本仓库内。

## 1. 当前主入口（已实测通过）

| 项 | 值 |
|---|---|
| 客户端 | Codex CLI `v0.155.0-alpha.16.4` |
| 可执行文件 | `C:\Users\lin\AppData\Local\OpenAI\Codex\bin\13995fba801849b0\codex.exe` |
| 启动脚本 | `start-ai.bat`（本项目根目录，双击即可） |
| Provider | `custom` → **DeepSeek Official** |
| Endpoint | `https://api.deepseek.com/responses`（OpenAI Responses API，SSE 实测 HTTP 200） |
| 模型 | `deepseek-flash`（DeepSeek-V4.1-Flash，1M 上下文，reasoning = high） |
| 备选模型 | `deepseek-v4-pro` |
| 配置文件 | `%USERPROFILE%\.codex\config.toml` |
| 配置守护 | `%USERPROFILE%\.codex\repair-deepseek.py`（被覆盖时自动恢复） |

实测结果（2026-09-25）：
- 在项目目录执行 `codex exec`，模型成功读取 `AGENTS.md` 与 `handoff/`，输出 5 行项目阶段摘要，未修改文件。
- 首字延迟约 1 秒级（SSE），无断流，`response.completed` 正常。

## 2. 每天怎么启动（最简单操作）

**双击 `C:\Users\lin\Documents\Codex\2026-09-25\yu\start-ai.bat`。**

脚本自动完成：
1. 进入项目根目录；
2. 调用 `repair-deepseek.py` 检查/修复 Codex 配置（幂等，正常时无输出）；
3. 启动 Codex CLI（deepseek-flash）。

## 3. 备选入口：OpenCode

- Desktop：`C:\Users\lin\AppData\Local\Programs\@opencode-aidesktop\OpenCode.exe`
- Provider：`deepseek`（key 已配置在 `%USERPROFILE%\.local\share\opencode\auth.json`）
- 模型：`deepseek/deepseek-flash`
- 当找不到 Codex CLI 时，`start-ai.bat` 会自动回退启动 OpenCode Desktop。
- 也可用 CC Switch 的本地代理统计用量。

## 4. 如何切换回 OpenAI 官方

- 方式 A：CC Switch 切换到 “OpenAI Official”，之后直接用 Codex Desktop 或 `codex.exe`，**不要运行 start-ai.bat**（它会切回 DeepSeek）。
- 方式 B：恢复现场备份后直接运行 `codex.exe`：
  ```
  copy "%USERPROFILE%\.codex\config.toml.bak-20260925-173212" "%USERPROFILE%\.codex\config.toml"
  ```
- 官方登录态始终保存在 `%USERPROFILE%\.codex\auth.json`（auth_mode=chatgpt），本项目从未改动它。

## 5. 故障排查

### 5.1 `stream disconnected before completion` / `stream closed`
1. 直接测 provider 连通性（PowerShell，不打印完整 key）：
   ```powershell
   $k=(Select-String "$env:USERPROFILE\.codex\config.toml" -Pattern 'experimental_bearer_token\s*=\s*"([^"]+)"').Matches[0].Groups[1].Value
   curl.exe -s -N -m 60 -o NUL -w "HTTP %{http_code} first %{time_starttransfer}s`n" -H "Authorization: Bearer $k" -H "Content-Type: application/json" --data-binary '{"model":"deepseek-flash","input":"只回复 123","stream":true}' https://api.deepseek.com/responses
   ```
2. HTTP 200 且 `response.completed` = 正常；若断流，重试一次或换 `deepseek-v4-pro`。
3. 重跑 `python %USERPROFILE%\.codex\repair-deepseek.py` 恢复配置。

### 5.2 aaccx relay（api.aaccx.pw）不可用（已知问题）
- 2026-09-25 实测：该 relay 仅提供 `claude-*` 模型，**不支持 `gpt-5.6-sol`**；且全部模型返回 `503 All available accounts exhausted`。
- 当前默认已切到 DeepSeek，不受该 relay 影响。
- 若仍想使用：把 config.toml 的 `model` 改为 `claude-opus-4-6`，`base_url` 改回 `https://api.aaccx.pw`，保持 `requires_openai_auth = false`，等 relay 恢复。

### 5.3 官方额度不足 / `You're out of Codex and Work usage`
- 该提示说明请求走了 OpenAI 官方账号额度。比赛期间不要用官方额度：
  **双击 `start-ai.bat`**，脚本会把 Codex 强制指回 DeepSeek 第三方（不消耗官方额度）。
- 如果 Desktop 在发送前就被 UI 额度拦截，直接改用 Codex CLI（start-ai.bat），不要再折腾 Desktop。

### 5.4 模型元数据警告
- `Model metadata for deepseek-flash not found. Defaulting to fallback metadata` 属于正常提示，不影响使用。

## 6. 上下文保持

- 每次启动 Codex 后，按 `AGENTS.md` 要求依次读取：
  `handoff/PROJECT_STATE.md` → `handoff/DECISIONS.md` → `handoff/NEXT_TASK.md` → `handoff/ARTIFACT_INDEX.md` → `handoff/BLOCKERS.md`。
- 当前阶段：**S4 Pilot Annotation Gate**，状态 `BLOCKED_BY_ANNOTATION`。
- 重大方向变更需过 Gate Review，不得由单个 AI 窗口自行修改。
