# Merkle Science 加密出入金钱包风险扫描 — API 需求梳理与注意点

> 日期：2026-09-10
> 目的：为「出入金扫描对方钱包 → 风险警报 → 人工审核」能力梳理 Merkle Science Compass API 的对接需求与工程注意点。
> 业务硬约束：风险命中 = 不自动入账 / 不自动出金，订单一律进入 pending，由运营人工审核；入金拒绝 → 退款，出金拒绝 → 出金失败。

---

## 一、API 概览

| 项目 | 值 |
|---|---|
| 产品 | Merkle Science Compass（企业级实时加密交易监控 / 钱包监控 / 客户监控） |
| 认证方式 | HTTP 请求头 `X-API-KEY`，仅 HTTPS，密钥在 Workspace 后台管理 |
| Base URL (demo) | `https://demo.api.merklescience.com/api/v4/` |
| Base URL (生产) | `https://api.merklescience.com/api/v4/` |
| 限流 | 100 次 / 分钟，1,000 次 / 小时，10,000 次 / 天 |
| 重试策略 | 指数退避：30s → 300s → 3,000s → 30,000s |
| 结果返回 | 同步返回风险评估；告警详情可同步返回（`show_alerts=true`，top 10）或异步回调（Webhook） |

**核心结论**：Merkle Science 提供的是「地址 / 交易 / 客户」三类风险决策能力，通过 `risk_level`（0–5）输出风险评分，并附带命中告警明细。本业务只需用到「地址筛查」和「交易筛查」两类。

---

## 二、风险等级模型（核心枚举）

`risk_level` 为数值 0–5，同时返回 `risk_level_verbose` 文本：

| risk_level | verbose | 含义 | 本业务默认处置 |
|---|---|---|---|
| 0 | No Risk Detected | 无风险 | 自动放行（不入队） |
| 1 | Info | 信息级 | 待确认（建议自动放行，仅记录） |
| 2 | Caution | 谨慎 | 待确认（建议进 pending） |
| 3 | Medium | 中风险 | **进 pending 人工审核** |
| 4 | High | 高风险 | **进 pending 人工审核** |
| 5 | Critical | 严重风险 | **进 pending 人工审核（优先）** |

告警等级（`level` / `level_verbose`）同样为 Info / Caution / Medium / High / Critical 五档。

> ⚠️ **风险阈值需确认**：用户需求表述为「出现风险警报」。Merkle 的 `risk_level ≥ 1` 即可能产生告警。建议阈值做成**可配置**，默认 `risk_level ≥ 3（Medium）拦截进 pending`，`2（Caution）` 可配置是否拦截，`0–1` 自动放行。此阈值是本需求的关键决策点，需产品确认。

---

## 三、两种集成模型（重要取舍）

Merkle 官方提供两套集成思路：

| 维度 | Simple 模型 | Advanced 模型（推荐） |
|---|---|---|
| 筛查对象 | 交易 + 钱包地址（双侧全部筛查） | 客户 + 入金/出金对象 + 钱包（单侧按需筛查） |
| 误报率 | **高**（会把平台自己的归集/中转地址一并扫入） | **低**（通过 `type` 参数只筛「对方」一侧） |
| 合规可读性 | 差（告警堆叠，运营难判断） | 好（告警按入金/出金事件归类，聚合客户级风险） |
| 适配本业务 | 不推荐 | **必须采用** |

**本业务必须走 Advanced 模型**，关键参数：
- `type=1`（Deposit，入金）：只筛查**发送方钱包**（即「对方钱包」= 打款进来的地址）。
- `type=2`（Withdrawal，出金）：只筛查**接收方钱包**（即「对方钱包」= 用户提现的目的地址）。

---

## 四、核心端点与业务映射

### 4.1 钱包地址筛查（KYA — Know Your Address）
- `POST /api/v4/addresses/`
- 入参：`identifier`（钱包地址）、`blockchain`（链代码）、`customer_id`（关联平台客户，可选）、`type`（1/2，与 customer_id 成对出现）、`show_alerts`（返回 top 10 告警）、`custom_tags`（可选自定义标签）。
- 出参（关键字段）：`risk_level` / `risk_level_verbose`、`total_incoming/outgoing_value`、`balance`、`originator[]`（直接/间接风险来源）、`beneficiary[]`、`digital_assets[]`、`tags`。

### 4.2 交易筛查（KYT — Know Your Transaction）
- `POST /api/v4/transactions/`
- 入参：`identifier`（交易哈希）、`blockchain`、`currency`、`customer_id`、`address`、`type`（1/2/3，须三者齐全或都不传）、`show_alerts`。
- 出参：`risk_level` / `risk_level_verbose`、`value` / `value_usd`、`fee`、`block_timestamp`（未确认时返回 `Unconfirmed`）、`originator[]`、`beneficiary[]`、`digital_assets[]`。

### 4.3 告警查询与处理
- `GET /api/v4/alerts/` — 按 `identifier` / `blockchain` / `customer_id` / `type` / `status` / `level` 过滤告警。
- `POST /api/v4/alerts/resolve/` — 处理告警（运营审核后回写 Merkle，保持合规留痕）。

### 4.4 事件回调（Webhook）
- 风险等级在首次筛查后**可能发生变化**（地址后续被标记）。需订阅 Webhook 实现持续监控；回调用 `X-WEBHOOK-KEY` 校验来源。

### 4.5 其它
- `POST /api/v4/customers/` — 客户级风险筛查（可选，用于聚合客户风险画像）。
- `GET /api/v4/health/` — 健康检查（服务可用性探针）。
- 报告下载 / 币种代码表 / 告警状态表 — 辅助能力。

---

## 五、出入金业务时序（Advanced 模型）

### 入金（Deposit）
```
链上交易确认
  → POST /transactions/ (type=1，只筛发送方钱包)
  → risk_level ≥ 阈值？
      ├─ 否 → 自动入账（completed）
      └─ 是 → 订单置为 pending，生成风险告警，通知运营
            → 运营审核
                ├─ 批准 → 入账（completed）
                └─ 拒绝 → 原路退款（refunded）+ 回写 Merkle resolve
```

### 出金（Withdrawal）
```
用户提交提现（含 2FA 校验）
  → POST /addresses/ (type=2，预筛查接收方钱包)
  → risk_level ≥ 阈值？
      ├─ 否 → 提交链上出金
      └─ 是 → 订单置为 pending，生成风险告警，通知运营
            → 运营审核
                ├─ 批准 → 放行出金（processing → completed）
                └─ 拒绝 → 出金失败（failed）+ 回写 Merkle resolve
（可选）出金链上确认后 → POST /transactions/ (type=2) 持续监控
```

---

## 六、需求注意点（工程 + 合规）

### A. 安全
1. **API Key 只允许服务端持有**，禁止出现在任何客户端代码、日志、前端请求中。
2. 记录密钥时一律脱敏（`[REDACTED]`），不写入 PRD / 文档 / 提交历史。

### B. 筛查正确性（最关键）
3. **必须用 Advanced 模型 + `type` 参数**，否则双侧筛查会把平台归集钱包/热钱包扫入，产生大量误报。
4. `customer_id` 与 `type` 必须**成对**关联，否则地址/交易无法正确归属到客户维度。
5. 地址格式需做**链级校验**（EVM 用 `0x` 前缀、BTC/Solana 等各自格式），格式非法直接拒绝，不送 Merkle。

### C. 性能与可用性
6. 限流 100 次/分钟，需设计**队列 + 背压**，避免批量入金/出金高峰期打满配额。
7. 筛查是**同步调用**，需定义超时（建议 ≤ 3s）；超时/5xx 的兜底策略需明确：
   - **fail-closed**（推荐，合规优先）：超时按「需人工审核」处理，进 pending，宁可人工多审不放过。
   - fail-open：超时放行（合规风险高，不推荐默认）。
8. Webhook 持续监控：已入账/已出金的交易后续风险等级变化，需触发**重审**（二次拦截 + 通知运营）。

### D. 审核闭环与留痕
9. 运营审核动作（批准/拒绝、理由、时间、操作人）必须**全量留痕**。
10. 审核结果需**回写 Merkle**（`POST /alerts/resolve/`），保持双方合规记录一致。
11. 告警状态需与平台订单状态做**映射与同步**（pending → 审核中 / resolved → 已处置）。

### E. 资金与订单状态机
12. 入金拒绝 = **原路退款**，需定义退款路径（回退到来源钱包 / 挂账待处理）。
13. 出金拒绝 = **出金失败**，资金解冻回用户可用余额，不可自动重试放行。
14. 用户可见状态文案需新增/复用：`pending review`（风控审核中）、`refunded`（已退款）、`failed`（出金失败），且需向用户说明「因合规风控审核」而非「技术故障」。

### F. 数据与合规
15. 平台资产（币种/链）需映射到 Merkle 的 `blockchain` / `currency` 代码表。
16. 高风险告警需支持导出合规报告（Merkle 报告下载能力）供审计。
17. 风险阈值、筛查开关、告警等级→处置策略建议做成**管理端可配置**（风控规则）。

---

## 七、待确认决策清单（供产品拍板）

1. **风险阈值**：默认 `risk_level ≥ 3（Medium）` 拦截进 pending；Caution（2）是否拦截？
2. **超时兜底**：筛查超时/服务不可用时，fail-closed（进 pending）还是 fail-open（放行）？
3. **持续监控**：已入账交易后续风险升级，是否二次拦截 + 冻结 + 重审？
4. **是否引入客户级筛查**（`POST /customers/`）做跨链客户风险聚合？
5. **退款路径**：入金拒绝的「原路退款」具体走哪条链上路径（回来源钱包？是否需要用户补目标地址？）。

---

## 八、与现网模块的关系（原型与 PRD 依据）

- **客户端**：现有 `Statement`（Billing）4-Tab 中的 Crypto 交易记录 + `Withdrawal Amount` 出金弹窗（深色主题、`#FFCA00` 金色、TOTP 6 位码）。风险扫描能力需在出金弹窗与入金/出金记录状态上体现（新增 `pending review` 等状态与提示）。
- **管理端**：现有「法币管理 → 交易审核」三队列（入金挂账复核 / 出金终审 / EA 添加审核）是**最直接可复用的审核模式**；管理端侧边栏「加密货币」目前为空节点（仅归集设置页）。本次需新增「加密货币 → 交易审核」风险审核队列 + 风险详情。
- **风控规则**：现有 `risk-control/01-Risk-Rule-Management`、`02-Risk-Event-List` 可承载「Merkle 风险阈值 / 告警等级处置」配置。
