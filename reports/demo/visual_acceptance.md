# Demo Visual Acceptance

日期：2026-09-26  
目标：答辩级真实浏览器视觉验收，限制为必要 P0/P1 修复。

## 结论

`DEMO_VISUAL_GATE = PASS`

本次发现并修复一个 P0 启动路径问题和一个 P1 移动端裁切问题：补充只读 Demo 服务器映射数据源，并修复 390px 视口的文字/状态栏溢出。修复后未发现数据错误、JavaScript 运行阻断、场景无响应或投影尺寸不可用问题。

## 浏览器与启动

- 启动命令：`python serve_demo.py 4173`（兼容用户要求的 4173 端口，并把 `/experiments/` 映射到项目根目录）
- 访问地址：http://127.0.0.1:4173/
- 验收浏览器：本机 Google Chrome Headless (`C:\Program Files\Google\Chrome\Application\chrome.exe`)
- 页面数据源：`/experiments/transfer_finance/information_missing_validation.json`（由 `serve_demo.py` 只读映射项目根目录文件）
- 浏览器内置 CUA 本轮因 Codex auth token unavailable 无法连接，因此使用本机 Chrome 截图完成验收。

## 分辨率验收

| 分辨率 | 结果 | 观察 |
|---|---|---|
| 1366×768 | PASS | 首屏显示研究主题、Raw→Reliability→Adjusted→Decision 路径和 DEVELOPMENT_ONLY；底部可见管线起始区域，无横向溢出。 |
| 1440×900 | PASS | Hero、指标摘要、场景控制与模型管线层级清晰，信息密度可控。 |
| 1920×1080 | PASS | 页面保持居中，内容没有异常放大或空洞，验证区可自然向下阅读。 |
| 390×844 | PASS | 修复标题/正文/状态标签的横向裁切后，页面无横向滚动；场景卡片按单列堆叠。 |

## 逐项检查

1. **首屏回答研究问题**：PASS。标题说明 evidence 与 score 的关系；副文案说明 raw signal、information completeness、evidence quality；右侧说明明确给出 Raw → Reliability → Adjusted → Decision。
2. **信息过载**：PASS。首屏只保留四个摘要指标和一条结果阅读顺序，详细案例下沉到后续区块。
3. **字号**：PASS。正文保持可读字号；移动端标题和说明做了响应式收缩。
4. **视觉层级**：PASS。四步管线采用统一 node 卡片和箭头，Decision 单独作为最后节点。
5. **四种场景交互**：静态代码检查确认 `normal`、`delayed`、`conflicting`、`low_trust` 均改变 `factor`、`agreement`、`quality` 或 `fresh`，并重新渲染 reliability、adjusted、decision、breakdown；不是只变按钮颜色。
6. **边界声明**：PASS。顶部 DEVELOPMENT_ONLY 可见但不覆盖核心结果；Gate 3 NOT SUPPORTED 与失败边界位于验证区和末尾 callout。
7. **叙事一致性**：PASS。Controlled parameter variants、Validation Gates、Historical Cases 保持既有 development-only / mechanism-check 口径。
8. **响应式**：PASS。移动端控制区和结果区单列堆叠，未发现水平滚动。

## 发现的问题

### P0（已修复）\n\n- 按 `cd reports/demo && python -m http.server 4173` 直接启动时，JSON 路径返回 404，导致交互数据无法加载。\n- 修复：新增 `reports/demo/serve_demo.py`，仅做本地只读路径映射，不改变 JSON、模型或计算逻辑。\n\n### P1（已修复）

- 390×844 下 Hero 标题、正文和顶部 DEVELOPMENT_ONLY 标签存在超出视口的横向裁切风险。
- 原因：移动端长文本和顶部状态标签没有明确的宽度约束。
- 修复：限制移动端文本宽度为 `calc(100vw - 32px)`，启用断行，收缩标题字号，并隐藏多余横向溢出。

## 已修复问题

- `reports/demo/serve_demo.py`：本地只读静态路径映射。\n- `reports/demo/index.html`：仅修改移动端 CSS，不改变任何数据、计算、阈值或状态文案。

## 未修复问题

- 无 P0/P1 未修复项。
- 页面仍然是较长的单页阅读结构，但在本轮规则下不属于真实阻断；已通过顶部导航锚点缓解。

## JS / 网络错误

- 页面 HTML 服务：HTTP 200。
- 主 JSON 数据源存在并可被页面引用。
- 数据 JSON：HTTP 200。\n- 页面依赖的 JSON 为 HTTP 200；Chrome 请求的 `/favicon.ico` 返回 404，但该资源不被页面引用，不影响 Demo。
- 未发现 JSON load failure 的代码路径改变。
- 静态检查未发现 `NaN`、`undefined` 作为固定输出文本。
- 本机截图加载成功，生成四张 PNG。
- 由于当前环境没有 Playwright Python/Node 包，且 Codex 内置浏览器认证令牌不可用，未取得 DevTools console 事件流；因此控制台错误项按静态代码和 Headless Chrome 成功加载结果判定为未见阻断。

## 关键截图路径

- [1366×768](C:\Users\lin\Documents\Codex\2026-09-25\yu\reports\demo\visual_acceptance\1366x768.png)
- [1440×900](C:\Users\lin\Documents\Codex\2026-09-25\yu\reports\demo\visual_acceptance\1440x900.png)
- [1920×1080](C:\Users\lin\Documents\Codex\2026-09-25\yu\reports\demo\visual_acceptance\1920x1080.png)
- [390×844](C:\Users\lin\Documents\Codex\2026-09-25\yu\reports\demo\visual_acceptance\390x844.png)

## 变更边界

本轮未修改数学模型、数据、Gate、阈值、R1/R2 或论文正式结论。
