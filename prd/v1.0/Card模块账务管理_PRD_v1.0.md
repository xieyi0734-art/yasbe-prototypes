# YASBee Card Module — 账务管理 PRD v1.0

> 版本：v1.0 | 日期：2026-06-03
> 平台：admin.beeznis.com | 渠道：Interlace MoR | 卡片类型：Prepaid Virtual Card

---

## 1. 产品概述

### 1.1 背景

YASBee 管理后台（admin.beeznis.com）已上线 Card management 页面（卡片列表），但缺少对卡片账户级资金的财务管理能力。当前 Fiat/Crypto Transaction Management 仅覆盖充提通道，未涵盖卡片内部的资金流转（充值到卡、消费扣款、手续费、退款等）。

运营/财务人员目前无法在线上完成以下工作：
- 查看某卡片账户的余额、累计充值/消费/手续费
- 查询卡片交易流水
- 手动为卡片充值或扣款
- 查看费用明细和汇总
- 发起退款及审批

### 1.2 目标

本期目标是为运营和财务团队提供 **2 个账务管理页面**，覆盖卡片账户的资金查询与操作能力。

### 1.3 范围

本 PRD 覆盖以下 2 个核心模块：

| 模块 | 菜单入口 | 核心功能 |
|------|---------|---------|
| **交易与结算** | Channel Management → 💰 Transaction & Settlement | 交易流水查询 / 费用明细 / 按周期结算 / 账单查看 |
| **充值/扣款与退款** | Channel Management → ⚡ Recharge / Deduct / Refund | 手动充值 / 手动扣款 / 余额调整 / 退款申请 + 审批 |

**本期不覆盖**：
- 争议工单（Dispute Tickets）— 后放
- 卡产品费率配置（由 Card Service Management 负责）
- 用户端卡账单展示（由用户端产品线负责）

### 1.4 用户角色

| 角色 | 职责范围 |
|------|---------|
| **运营专员** | 查看交易流水、费用明细、结算报表；发起 ≤ $100 充值/扣款/退款 |
| **运营主管** | 全部运营专员权限 + 审批 ≥ $100 且 ≤ $1,000 的充值/扣款/退款操作 |
| **财务人员** | 查看结算报表、月度账单、费用汇总分析 |
| **管理员** | 全部权限；审批 ≥ $1,000 的高风险操作 |

---

## 2. 侧边栏导航调整

### 2.1 新增入口

```
Channel Management
├── Upstream Management          ← 已有
├── Card Service Management     ← 已有（卡产品配置入口）
├── Card management             ← 已有（已发行卡片列表）
├── ─────────────────────────
├── 💰 Transaction & Settlement  ← 新增
├── ⚡ Recharge / Deduct / Refund ← 新增
├── ─────────────────────────
├── Investment management       ← 已有
└── Rebate Management           ← 已有
```

### 2.2 页面之间跳转关系

- **Card management（卡片列表）**：每行提供一个「交易」按钮 → 跳转到该卡片的 Transaction & Settlement（带 card_id 筛选）
- **Transaction & Settlement**：交易详情中显示卡片信息 → 可跳回 Card management 该卡片详情
- **Recharge / Deduct / Refund**：操作时需搜索/选择目标卡片 → 操作记录可关联回 Transaction & Settlement 对应交易

---

## 3. 功能需求

### 3.1 模块一：交易与结算（Transaction & Settlement）

> 一个页面，顶部 Tab 切换三个视图：**Transactions / Settlement / Bills**

#### 3.1.1 Transactions Tab（交易流水）

**功能描述**：运营/财务查看所有卡片交易的流水记录，多维筛选定位问题。

**查询筛选区**（顶部折叠式面板）：

| 筛选条件 | 控件类型 | 选项 |
|---------|---------|------|
| Transaction ID | 文本输入 | 精确搜索 |
| Card ID / Card Number | 文本输入 | 模糊搜索 |
| User ID / Email | 文本输入 | 模糊搜索 |
| 交易类型 | 多选下拉 | ⚡Recharge / 🛒Consumption / ↩️Refund / 💰Fee / ⚖️Chargeback / ⚙️Adjustment |
| 交易状态 | 多选下拉 | Success / Pending / Failed / Reversed / Flagged |
| 渠道 | 多选下拉 | Visa / Mastercard / Interlace（由卡产品配置决定） |
| 时间范围 | 日期选择器 | 预设：Today / Last 7 Days / This Month / Custom |
| 金额范围 | 数字区间 Min ~ Max | — |
| 操作人 | 文本输入 | 精确搜索（筛选后台操作记录） |

**汇总统计条**（筛选区下方）：

```
┌──────────┬────────────┬────────────┬────────────┬────────────┐
│   总笔数   │  收入总计    │  支出总计    │ 手续费总计   │  净结算额    │
│    248    │  +$45,280   │  -$38,195   │   $2,845   │   $4,240    │
└──────────┴────────────┴────────────┴────────────┴────────────┘
```

**数据表格**：

| 列 | 说明 | 格式 |
|----|------|------|
| TXN ID | 唯一流水号 | TXN-20260603-XXXXX |
| Time | 交易时间 | 2026-06-03 14:30 |
| Type | 交易类型 | 标签样式：⚡Recharge(绿) / 🛒Consumption(蓝) / ↩️Refund(黄) / 💰Fee(紫) / ⚖️Chargeback(红) / ⚙️Adjustment(灰) |
| Card | 卡片标识 | CRD-8A3F |
| Customer | 客户标识 | email 或 user ID |
| Channel | 渠道 | Visa / MC / IL |
| Amount | 交易金额 | +$500.00 / −$89.99（正负色） |
| Fee | 手续费 | $2.50（如果该笔有手续费） |
| Status | 状态 | ✅ Success / ⏳ Pending / ❌ Failed / ↩️ Reversed / ⚠️ Flagged |
| Action | 操作 | 详情 / 标记异常 |

**排序**：默认按时间倒序；支持点击列头排序

**详情弹窗/侧边栏**（点击详情打开）：

```
┌─ Transaction Details ────────────────────────────────────┐
│ TXN-20260603-001                                          │
│ ├─ 交易信息 ────────────┬─ 金额信息 ──────────────────── │
│ │  时间: 06-03 09:24     │  金额: +$500.00               │
│ │  类型: Recharge        │  手续费: $2.50                │
│ │  状态: ✅ Success      │  结算金额: $497.50            │
│ │  卡片: CRD-8A3F        │                               │
│ │  客户: john@...        ├─ 引用信息 ──────────────────── │
│ │  渠道: Interlace       │  上游引用 ID: INT-REF-A3F2...  │
│ │  操作人: —（系统）      │  关联卡产品: Premium Card       │
│ │  备注: —               │                               │
│ └────────────────────────┴────────────────────────────────┘
│                                    [Close]                 │
└───────────────────────────────────────────────────────────┘
```

**交易类型标签配色**：

| 类型 | 标签色 | Emoji |
|------|--------|-------|
| Recharge | 绿色 #52c41a | ⚡ |
| Consumption | 蓝色 #1890ff | 🛒 |
| Refund | 黄色 #faad14 | ↩️ |
| Fee | 紫色 #722ed1 | 💰 |
| Chargeback | 红色 #ff4d4f | ⚖️ |
| Balance Adjustment | 灰色 #8c8c8c | ⚙️ |

**数据导出**：
- 点击「📥 Export CSV」导出当前筛选结果
- 记录数 > 1,000 条时异步导出，后台处理完成后通知下载

---

#### 3.1.2 Settlement Tab（结算汇总）

**功能描述**：按周期（日/月）查看费用结算的汇总数据。

**筛选区**：
- 周期类型：Daily / Monthly
- 时间范围：日期选择器
- 状态筛选：All / Pending / Settled

**结算列表（按月）**：

| 结算编号 | 周期 | 日期 | 活跃卡片数 | 开卡费 | 充值费 | 消费费 | 月费 | 优惠减免 | 费用总计 | 状态 |
|---------|------|------|-----------|--------|--------|--------|------|---------|---------|------|
| SET-202606 | 月 | 06-30 | 156 | $1,250.00 | $845.30 | $2,150.50 | $18.60 | -$200.00 | $4,064.40 | ✅ SETTLED |
| SET-202605 | 月 | 05-31 | 142 | $980.00 | $720.00 | $1,850.00 | $15.40 | -$150.00 | $3,415.40 | ✅ SETTLED |
| SET-202604 | 月 | 04-30 | 128 | $750.00 | $680.00 | $1,620.00 | $12.80 | -$100.00 | $2,962.80 | ✅ SETTLED |

**点击行展开** → 该周期下各卡片费用明细表：

| 卡片 ID | 客户 | 开卡费 | 充值费 | 消费费 | 月费 | 优惠减免 | 小计 |
|---------|------|--------|--------|--------|------|---------|------|
| CRD-8A3F | john@... | $0.00 | $15.00 | $42.50 | $0.25 | $0.00 | $57.75 |
| CRD-7B2E | alice@... | $10.00 | $0.00 | $0.00 | $0.00 | -$10.00 | $0.00 |

**结算状态说明**：

| 状态 | 含义 |
|------|------|
| PENDING | 周期未结束，数据为预估 |
| SETTLED | 周期已结束，数据已确认不可更改 |

**导出**：支持导出当前结算周期明细 CSV

---

#### 3.1.3 Bills Tab（月度账单）

**功能描述**：按月出具面向 YASBee 财务的正式账单。

**账单列表**：

| 账单编号 | 月份 | 开账日期 | 开卡费收入 | 充值费收入 | 消费费收入 | 月费收入 | 优惠支出 | 净收入 | 状态 |
|---------|------|---------|-----------|-----------|-----------|---------|---------|-------|------|
| INV-202606 | 2026-06 | 07-01 | $1,250.00 | $845.30 | $2,150.50 | $18.60 | -$200.00 | $4,064.40 | ✅ CONFIRMED |
| INV-202605 | 2026-05 | 06-01 | $980.00 | $720.00 | $1,850.00 | $15.40 | -$150.00 | $3,415.40 | ✅ CONFIRMED |
| INV-202604 | 2026-04 | 05-01 | $750.00 | $680.00 | $1,620.00 | $12.80 | -$100.00 | $2,962.80 | ✅ CONFIRMED |

**功能操作**：
- 筛选：月份范围 / 状态
- 查看详情：点击账单行 → 弹出完整账单明细（含每卡费用分解）
- 确认标记：财务人员确认后标记「CONFIRMED」
- 导出：CSV / PDF（P1 功能）

---

### 3.2 模块二：充值/扣款与退款（Recharge / Deduct / Refund）

> 一个页面分上下两部分：上半部操作区 + 下半部历史记录

#### 3.2.1 手动操作区（上半部）

**单笔充值/扣款/余额调整表单**：

```
┌─ Manual Operation ─────────────────────────────────────────┐
│ Operation Type:  [Recharge ▾]                               │
│   ┌──────────────┬────────────────────────────────────────┐│
│   │ Recharge     │ 向卡片增加余额                           ││
│   │ Deduct       │ 从卡片扣除余额                           ││
│   │ Adjust       │ 余额调整（可正可负）                     ││
│   └──────────────┴────────────────────────────────────────┘│
│ Target Card:     [CRD-8A3F (john.doe@...) 🔍]              │
│ Amount:          [__________] USD                           │
│ Reason:          [Testing ▾]                                │
│ Remark:          [_______________________________] (必填)   │
│ Operator:        admin@yasbe.com (自动获取当前登录用户)       │
│                                                        │
│                    [Cancel]            [🚀 Submit]         │
└────────────────────────────────────────────────────────────┘
```

**操作类型说明**：

| 类型 | 金额方向 | 说明 | 余额校验 |
|------|---------|------|---------|
| Recharge | 正数 | 向卡片增加余额 | 不校验 |
| Deduct | 正数 | 从卡片扣除余额 | 扣款金额 + 冻结 ≤ 可用余额 |
| Adjust | 正数/负数 | 余额调整（正=增加，负=减少） | 负数时：abs(金额) + 冻结 ≤ 可用余额 |

**金额限制与审批路由**：

| 金额范围 | 审批要求 |
|---------|---------|
| ≤ $100 | 运营专员直接提交执行 |
| $100 < x ≤ $1,000 | 需运营主管审批 |
| > $1,000 | 需运营主管 + 管理员二级审批 |

**审批流程**（触发时）：
1. 运营专员提交 → 状态变为 Pending Approval
2. 审批人收到 My Tasks 通知
3. 审批人在 My Tasks 或操作记录列表中点击审批
4. 审批人 Approve / Reject + 备注
5. 审批通过 → 系统执行操作；审批拒绝 → 操作取消

**CSV 批量操作**（P1 功能）：

```
┌─ CSV Batch Operation ──────────────────────────────────────┐
│ [📎 Download Template] 【Card ID, Amount, Type, Remark】    │
│ [📤 Upload CSV]                                            │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ Preview: (上传后展示前 5 行数据供确认)                   │ │
│ │ Card ID      | Amount | Type     | Remark              │ │
│ │ CRD-8A3F     | 500    | Recharge | Batch test #1       │ │
│ │ CRD-7B2E     | -200   | Deduct   | Fee recovery        │ │
│ └────────────────────────────────────────────────────────┘ │
│                                               [🚀 Execute] │
└────────────────────────────────────────────────────────────┘
```

#### 3.2.2 操作与退款记录区（下半部）

**筛选区**：

| 筛选条件 | 控件 |
|---------|------|
| 操作类型 | 多选下拉：Recharge / Deduct / Refund / Adjustment |
| 状态 | 多选下拉：Completed / Pending Approval / Rejected / Failed |
| 时间范围 | 日期选择器 |
| 卡片 | 文本输入 |
| 操作人 | 文本输入 |

**记录列表**：

| 编号 | 类型 | 卡片 | 客户 | 金额 | 状态 | 操作人 | 审批人 | 时间 | 操作 |
|------|------|------|------|------|------|--------|--------|------|------|
| OP-001 | ⚡Recharge | CRD-8A3F | john@... | +$500.00 | ✅ Completed | admin | — | 06-03 09:24 | 详情 |
| OP-002 | ➖Deduct | CRD-7B2E | alice@... | -$200.00 | ✅ Completed | admin | — | 06-02 14:30 | 详情 |
| OP-003 | ↩️Refund | CRD-4D17 | carol@... | -$120.00 | ⏳ Pending Approval | operator1 | — | 06-03 10:00 | 审批 |
| OP-004 | ⚙️Adjust | CRD-5F2B | dave@... | +$50.00 | ❌ Rejected | operator2 | admin | 06-01 08:00 | 详情 |
| OP-005 | ↩️Refund | CRD-8A3F | john@... | -$500.00 | ⏳ Pending Approval | operator1 | admin | 06-03 11:00 | 审批 |

**状态标签**：

| 状态 | 标签色 |
|------|--------|
| Completed | 绿色 ✅ |
| Pending Approval | 橙色 ⏳ |
| Rejected | 红色 ❌ |
| Failed | 红色 ❌ |

**详情弹窗**（点击详情/审批打开）：

```
┌─ Operation Details ────────────────────────────────────────┐
│ OP-20260603-003                                             │
│ ├─ 操作信息 ────────────┬─ 审批信息 ──────────────────── │
│ │  类型: Refund          │  审批状态: ⏳ Pending Approval│
│ │  卡片: CRD-4D17        │  当前审批人: admin            │
│ │  客户: carol@...       │  审批层级: 一级（运营主管）    │
│ │  金额: -$120.00        │                               │
│ │  余额变更前: $250.00   ├─ 审计记录 ──────────────────── │
│ │  余额变更后: $370.00   │  创建: 06-03 10:00 by op1     │
│ │  原因: User Request    │  审批: —                       │
│ │  备注: 用户多扣退款     │  执行: —                       │
│ └────────────────────────┴────────────────────────────────┘
│                       [Approve] [Reject] [Close]            │
└───────────────────────────────────────────────────────────┘
```

**审批操作**（当状态为 Pending Approval 时显示）：
- 审批人点击「Approve」→ 系统执行该操作（充值/扣款/退款）
- 审批人点击「Reject」→ 填写拒绝原因 → 操作取消
- 审批人在 My Tasks 中也会收到待审批通知

---

## 4. 权限矩阵

| 功能/操作 | 运营专员 | 运营主管 | 财务人员 | 管理员 |
|-----------|:--------:|:--------:|:--------:|:------:|
| 查看交易流水 | ✅ | ✅ | ✅ | ✅ |
| 查看结算报表 | ✅ | ✅ | ✅ | ✅ |
| 查看月度账单 | ❌ | ✅ | ✅ | ✅ |
| 确认账单 | ❌ | ❌ | ✅ | ✅ |
| 导出 CSV | ✅ | ✅ | ✅ | ✅ |
| 手动充值 ≤ $100 | ✅ | ✅ | ❌ | ✅ |
| 手动充值 > $100 | ❌ | ✅ | ❌ | ✅ |
| 手动扣款 ≤ $100 | ✅ | ✅ | ❌ | ✅ |
| 手动扣款 > $100 | ❌ | ✅ | ❌ | ✅ |
| 余额调整 | ❌ | ✅ | ❌ | ✅ |
| 发起退款 ≤ $100 | ✅ | ✅ | ❌ | ✅ |
| 发起退款 > $100 | ❌ | ✅ | ❌ | ✅ |
| 审批（一级） | ❌ | ✅ | ❌ | ✅ |
| 审批（二级） | ❌ | ❌ | ❌ | ✅ |
| 查看操作审计日志 | ❌ | ✅ | ✅ | ✅ |

---

## 5. 操作审计规范

所有写操作（充值/扣款/退款/余额调整/账单确认）必须记录以下审计信息：

| 审计字段 | 说明 |
|---------|------|
| 操作 ID | 唯一标识 OPR-YYYYMMDD-XXXXX |
| 操作人 | 操作员用户名 / 用户 ID |
| 操作时间 | 服务器时间，精确到毫秒 |
| 客户端 IP | 操作来源 IP |
| 操作类型 | Recharge / Deduct / Refund / Adjustment / BillConfirm |
| 目标对象 | 操作的卡片 ID / 账单 ID |
| 变更前值 | JSON 格式（如操作前余额） |
| 变更后值 | JSON 格式（如操作后余额） |
| 审批记录 | 审批人 / 审批时间 / 审批意见（如需审批） |
| 备注 | 操作备注内容 |

审计日志在 Admin Management → Operation Log 中可查询。

---

## 6. 数据模型

### 6.1 Card Account（卡片账户）

每张已发行卡片对应一个账户：

| 字段 | 类型 | 说明 |
|------|------|------|
| card_id | string | YASBee 内部卡 ID |
| card_number | string | 脱敏卡号（仅后 4 位明文） |
| user_id | string | 关联用户 ID |
| card_product_id | string | 关联 Card Product（卡产品配置） |
| balance | decimal(18,2) | 当前余额（USD） |
| frozen_amount | decimal(18,2) | 冻结金额（USD） |
| total_recharge | decimal(18,2) | 累计充值总额 |
| total_spent | decimal(18,2) | 累计消费总额 |
| total_fees | decimal(18,2) | 累计手续费总额 |
| currency | string | 账户币种（固定 USD） |
| status | enum | Active / Frozen / Closed |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 最后更新时间 |

### 6.2 Card Transaction（交易流水）

| 字段 | 类型 | 说明 |
|------|------|------|
| txn_id | string | 唯一流水号 TXN-YYYYMMDD-XXXXX |
| card_id | string | 关联卡片 ID |
| user_id | string | 关联用户 ID |
| type | enum | Recharge / Consumption / Refund / Fee / Chargeback / BalanceAdjustment |
| amount | decimal(18,2) | 金额（正=入账，负=出账） |
| currency | string | USD |
| fee | decimal(18,2) | 该笔交易产生的手续费 |
| balance_before | decimal(18,2) | 交易前余额 |
| balance_after | decimal(18,2) | 交易后余额 |
| status | enum | Success / Pending / Failed / Reversed / Flagged |
| channel | string | Visa / Mastercard / Interlace |
| operator | string | 操作人（系统操作时为 null） |
| approval_status | enum | null / Pending / Approved / Rejected（需要审批时） |
| approver | string | 审批人用户名 |
| remark | string | 备注 |
| upstream_txn_id | string | Interlace 上游交易 ID |
| created_at | datetime | 交易时间 |

### 6.3 Settlement Record（结算记录）

| 字段 | 类型 | 说明 |
|------|------|------|
| settlement_id | string | SET-YYYYMM 或 SET-YYYYMMDD |
| period_type | enum | Daily / Monthly |
| period_start | date | 周期开始日期 |
| period_end | date | 周期结束日期 |
| total_cards | int | 参与计费的卡片数 |
| opening_fee | decimal(18,2) | 开卡费收入 |
| recharge_fee | decimal(18,2) | 充值费收入 |
| consumption_fee | decimal(18,2) | 消费费收入 |
| monthly_fee | decimal(18,2) | 月费收入 |
| discount | decimal(18,2) | 优惠减免（负值） |
| total_fee | decimal(18,2) | 费用总计 |
| status | enum | Pending / Settled |
| created_at | datetime | 创建时间 |
| settled_at | datetime | 结算时间 |

### 6.4 Bill（月度账单）

| 字段 | 类型 | 说明 |
|------|------|------|
| bill_id | string | INV-YYYYMM |
| month | string | 账期月份 2026-06 |
| issue_date | date | 开账日期 |
| opening_fee_income | decimal(18,2) | 开卡费收入 |
| recharge_fee_income | decimal(18,2) | 充值费收入 |
| consumption_fee_income | decimal(18,2) | 消费费收入 |
| monthly_fee_income | decimal(18,2) | 月费收入 |
| discount_expense | decimal(18,2) | 优惠支出 |
| net_income | decimal(18,2) | 净收入（= 各项收入之和 − 优惠支出） |
| status | enum | Draft / Confirmed |
| confirmed_by | string | 确认人 |
| confirmed_at | datetime | 确认时间 |
| created_at | datetime | 创建时间 |

### 6.5 Operation Record（操作记录 — 审计用）

| 字段 | 类型 | 说明 |
|------|------|------|
| operation_id | string | OPR-YYYYMMDD-XXXXX |
| type | enum | Recharge / Deduct / Refund / Adjustment |
| card_id | string | 目标卡片 |
| user_id | string | 关联用户 |
| amount | decimal(18,2) | 操作金额 |
| balance_before | decimal(18,2) | 操作前余额 |
| balance_after | decimal(18,2) | 操作后余额 |
| operator | string | 操作人 |
| approval_status | enum | null / Pending / Approved / Rejected |
| approver | string | 审批人 |
| remark | string | 备注 |
| client_ip | string | 操作来源 IP |
| created_at | datetime | 操作时间 |

---

## 7. 非功能需求

| 编号 | 需求 | 说明 |
|------|------|------|
| N-01 | 权限控制 | 按角色控制菜单可见性和读写权限，操作记录可追溯 |
| N-02 | 操作审计 | 所有资金操作写入 Audit Log（操作人/时间/IP/变更前后值） |
| N-03 | 余额一致性 | 手动充值/扣款需保证 YASBee 本地记录与上游（Interlace）余额一致 |
| N-04 | 余额防负 | Deduct 和 Adjust（负数）操作需校验：金额 + 冻结 ≤ 当前余额 |
| N-05 | 金额精度 | 统一使用 decimal(18,2)，2 位小数 Cent 精度 |
| N-06 | 查询性能 | 交易流水查询响应 ≤ 2s（10 万条数据规模） |
| N-07 | 数据导出 | 所有列表页支持 CSV 导出；> 1,000 条异步导出 |
| N-08 | 幂等性 | 充值/扣款需有幂等键（Idempotency Key），防止重复提交 |
| N-09 | 审批超时 | 待审批操作超过 72 小时未处理 → 自动升级通知管理员 |

---

## 8. 费用约定规则（附录）

### 8.1 费用类型定义

YASBee Card 平台的费用来自用户开卡/充值/消费时产生的各项费用，按以下规则计算：

| 费用类型 | 收取方 | 计算方式 | 说明 |
|---------|--------|---------|------|
| Opening Fee（开卡费） | YASBee → Interlace | 固定金额 或 费率（互斥） | 用户开卡时支付，Opening Fee 和 Opening Fee Rate 互斥 |
| Recharge Fee（充值费） | YASBee | 固定金额 或 费率（互斥） | 用户充值时扣除，Recharge Fixed 和 Recharge Rate 互斥 |
| Consumption Fee（消费费） | YASBee | 固定金额 或 费率（互斥） | 用户消费时扣除，Consumption Fixed 和 Consumption Rate 互斥 |
| Monthly Fee（月费） | YASBee | $0.12~$0.25/月 | 仅正常状态（Active）卡片收取 |
| First Open Discount（新开优惠） | YASBee 支出 | 固定金额减免 | 首次开卡一次性优惠 |
| Chargeback Fee（退单费） | Interlace | $35/笔 | 发生退单争议时产生 |

### 8.2 关键规则

1. **费率与固定费互斥**：同一费用类型（如 Opening Fee），Rate 和 Fixed 不会同时存在。配置在 Card Product 中定义。
2. **Rebate（返佣）不是费用**：按 rebate_rate 计算的 YASBee 代币奖励，不计入任何 USD 费用总额或净收入计算。在 Settlement 和 Bill 中单独列出（单位 YB）。
3. **费用归属**：
   - Opening / Monthly / Chargeback Fee：用户端收取后，YASBee 侧需向 Interlace 结算
   - Recharge / Consumption Fee：YASBee 平台收入
   - Platform Income = 用户支付总费用 − 渠道成本总费用（渠道成本来自 Interlace）

### 8.3 与 Card Product 的关系

费用类型和具体费率在 **Card Service Management**（卡产品配置）中定义。本 PRD 的账务功能**读取**这些配置来展示和分析，不做配置修改。

---

## 9. 实施计划

| Phase | 内容 | 功能范围 | 周期 |
|:-----:|------|---------|:----:|
| **1** | 交易与结算页面（Transactions Tab + Settlement Tab） | F-001~F-005 | 1.5 周 |
| **2** | 交易与结算（Bills Tab）+ 充值/扣款与退款页面（操作区） | F-006~F-011 | 1 周 |
| **3** | 充值/扣款与退款页面（审批流 + CSV 批量） | F-012~F-015 | 1 周 |
| **4** | 权限矩阵 + 审计日志 + 联调测试 | — | 0.5 周 |

### 功能清单总表

| 编号 | 功能 | 模块 | Phase | 优先级 |
|:----:|------|------|:----:|:------:|
| F-001 | 交易流水列表 + 多维筛选 | 交易与结算 | 1 | P0 |
| F-002 | 交易详情弹窗 | 交易与结算 | 1 | P0 |
| F-003 | 交易汇总统计条 | 交易与结算 | 1 | P1 |
| F-004 | 导出交易记录 CSV | 交易与结算 | 1 | P1 |
| F-005 | 结算列表（日/月维度的费用汇总） | 交易与结算 | 1 | P1 |
| F-006 | 结算详情展开（周期下各卡片费用明细） | 交易与结算 | 1 | P1 |
| F-007 | 月度账单列表 + 筛选 | 交易与结算 | 2 | P1 |
| F-008 | 账单确认标记 + 导出 | 交易与结算 | 2 | P1 |
| F-009 | 手动充值/扣款/余额调整（单笔） | 充值/扣款与退款 | 2 | P0 |
| F-010 | 操作记录列表 | 充值/扣款与退款 | 2 | P1 |
| F-011 | 发起退款申请 + 余额校验 | 充值/扣款与退款 | 2 | P0 |
| F-012 | 退款审批流（金额路由 + 审批操作） | 充值/扣款与退款 | 3 | P1 |
| F-013 | 审批通知（My Tasks） | 充值/扣款与退款 | 3 | P1 |
| F-014 | CSV 批量充值/扣款 | 充值/扣款与退款 | 3 | P1 |
| F-015 | 操作审计日志 | 公共 | 4 | P1 |

---

## 10. 修订历史

| 版本 | 日期 | 修订内容 | 作者 |
|:----:|:----:|---------|:----:|
| v1.0 | 2026-06-03 | 初版 — 2 个模块（交易结算 + 充值退款），不含争议工单 | Hermes Agent |
