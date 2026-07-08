# YASBee Card Module — 账务管理端 PRD v1.0

> 版本：v1.0 | 日期：2026-06-03  
> 对应环境：admin.beeznis.com | 渠道：Interlace MoR | 卡片类型：Prepaid Virtual Card

---

## 1. 产品概述

### 1.1 背景

YASBee 管理后台（admin.beeznis.com）已有 **Card Service Management** 模块管理卡产品配置（费率、渠道、钱包支持等），但缺少对 **已发行卡片** 的账户级财务管理。当前 Fiat/Crypto 交易管理仅覆盖充提通道，未涵盖卡片内部的资金流转（充值到卡、消费扣款、手续费、退款等）。

### 1.2 目标

为运营团队提供一套完整的卡片账户财务管理工具，覆盖单卡账户总览、交易流水、手动资金操作、费用明细和异常处理。

### 1.3 范围

本期涉及 5 个子模块，均在 **Channel Management** 侧边栏下新增二级菜单，入口与现有 Card Service Management / Card management 平级：

```
Channel Management
├── Card Service Management    ← 已有（卡产品配置）
├── Card management            ← 已有（占位，404）
├── ??? 卡片账户管理 ???       ← 本期新增入口
└── Rebate Management          ← 已有（占位，404）
```

---

## 2. 用户角色

| 角色 | 权限范围 |
|------|---------|
| **运营专员** | 查看账户总览、交易流水、手续费明细；发起充值/扣款/退款操作 |
| **运营主管** | 全部运营专员权限 + 审核异常标记、审批大额退款 |
| **风控专员** | 查看异常交易、标记交易、审批争议处理 |

---

## 3. 功能模块

### F-001 卡片账户总览

> 侧边栏入口：「Card Account Overview」或作为 Card management 的子页面

**用户故事**：运营人员搜索某张卡片后，一眼看清该卡的资金状态。

**字段展示（只读信息卡片）**：

```
┌─ 卡片基本信息 ──────────────────────────┐
│  Card Number: 5274 83XX XXXX XXXX       │
│  User ID: USR-20260601-XXXXX            │
│  User Name: John Doe                    │
│  Card Product: Premium Card             │
│  Status: Active │ Issued: 2026-06-02    │
├─ 资金概览 ───────────────────────────────┤
│  💰 Balance:       $1,250.00            │
│  🧊 Frozen:        $200.00              │
│  📥 Total Recharge: $5,000.00           │
│  📤 Total Spent:   $3,550.00            │
│  💸 Total Fees:    $12.50               │
│  🔄 Available:     $1,050.00            │
└──────────────────────────────────────────┘
```

| 维度 | 内容 |
|------|------|
| **优先级** | P0 |
| **前置条件** | 卡片状态为 Issued/Active |
| **搜索方式** | 顶部搜索框：Card Number / User ID / User Name 模糊搜索 |
| **数据来源** | Interlace API 账户余额 + YASBee 本地资金流水聚合 |
| **可用额度** | Available = Balance − Frozen |
| **异常提示** | 当 Frozen > 0 时，显示红色提示「存在冻结资金」 |

---

### F-002 交易流水查询

> Tab 或子页面，与账户总览联动

**用户故事**：运营查看某卡片的全部资金变动记录，按类型和状态筛选定位问题。

**查询筛选区**：

| 筛选条件 | 控件类型 | 选项 |
|---------|---------|------|
| 交易类型 | 多选下拉 | 充值 / 消费 / 退款 / 手续费 / 余额调整 |
| 交易状态 | 单选下拉 | 成功 / 处理中 / 失败 / 已撤销 |
| 时间范围 | 日期选择器 | 预设：今天 / 本周 / 本月 / 自定义 |
| 金额范围 | 数字区间 | Min ~ Max |
| 交易ID | 文本输入 | 精确搜索 |

**列表列定义**：

| 列 | 说明 | 格式 |
|----|------|------|
| Transaction ID | 系统唯一流水号 | TXN-20260603-XXXXX |
| Type | 交易类型 | 标签样式（绿=充值 / 橙=消费 / 红=退款 / 灰=手续费 / 蓝=调整） |
| Amount | 交易金额 | +$100.00 / −$50.00（正负色） |
| Currency | 币种 | USD / USDT / USDC |
| Balance After | 交易后余额 | $1,200.00 |
| Status | 状态 | Badge（成功 / 处理中 / 失败 / 已撤销） |
| Time | 交易时间 | 2026-06-03 14:30:22 |
| Remark | 备注 | 如「Manual recharge by admin」 |
| Operator | 操作人 | 如果是后台操作，显示管理员名称 |
| Action | 操作 | 详情 / 标记异常 |

**排序**：默认按时间倒序；支持点击列头排序

**详情弹窗**：点击「详情」弹出 Drawer，显示：

- 完整字段（含上游 Interlace 交易 ID）
- 关联卡片信息（卡号脱敏、卡片产品名称）
- 费用分解（如有手续费，列出 Network Fee / Platform Fee）
- 操作时间线（审核记录、状态变更记录）

**汇总统计条**（列表顶部）：

```
📊 Summary: Total 45 records
  充值: +$5,000.00 (12笔) | 消费: −$3,550.00 (30笔)
  手续费: −$12.50 (3笔)   | 退款: +$200.00 (2笔)
```

---

### F-003 充值/扣款管理

> 操作型功能，与交易流水同页面或独立 Tab

**用户故事**：运营因测试/赔付/用户充值失败等场景需要手动操作卡片余额。

#### 3.1 手动充值

| 维度 | 内容 |
|------|------|
| **操作流程** | 1. 选择目标卡片（搜索卡号/用户）<br>2. 输入金额 + 币种<br>3. 选择资金来源（Platform / Channel）<br>4. 输入备注（必填，如「Testing funds」「User compensation」）<br>5. 提交 → 记录操作人和时间 |
| **金额限制** | 单笔 ≤ $10,000；日累计 ≤ $50,000 |
| **权限** | 运营专员可发起；≥ $1,000 需运营主管审批 |
| **数据记录** | 写入交易流水，Type=Recharge，Remark 含操作人信息 |

#### 3.2 手动扣款

| 维度 | 内容 |
|------|------|
| **操作流程** | 1. 选择目标卡片<br>2. 输入扣款金额 + 币种<br>3. 选择扣款原因（Adjustment / Fee Recovery / Other）<br>4. 输入备注（必填）<br>5. 验证余额充足 → 提交 |
| **余额校验** | 扣款金额 + 已冻结 ≤ 当前可用余额，否则报错提示 |
| **权限** | 运营专员可发起；单笔 > $1,000 需主管审批 |

#### 3.3 操作记录视图

所有手动操作均需记录审计日志，在当前页面下方展示历史记录表：

| 列 | 说明 |
|----|------|
| Operation ID | OPR-20260603-XXXXX |
| Type | Recharge / Deduct |
| Card Number | 脱敏显示 |
| Amount | 金额（正/负） |
| Operator | 管理员名称 |
| Remark | 备注内容 |
| Approval Status | Pending / Approved / Rejected |
| Time | 操作时间 |

#### 3.4 CSV 批量操作

> 支持 CSV 导入批量充值/扣款（P1 功能）

- 模板下载（含列：Card Number, Amount, Currency, Remark）
- 上传后预览确认 → 提交
- 处理结果下载（成功/失败明细）

---

### F-004 手续费管理

> 独立页面或交易流水中的一个筛选类型

**用户故事**：运营需要查看每张卡产生的所有费用，分析平台收入构成。

#### 4.1 费用类型定义

| 费用类型 | 说明 | 收费方 |
|---------|------|--------|
| Network Fee | 支付网络手续费（如 Visa/Mastercard 清算费） | Interlace |
| Bank Fee | 发卡行手续费 | Interlace |
| Platform Income | YASBee 平台收入（卡片费用 = 用户支付 − 渠道成本） | YASBee |
| Opening Fee | 开卡费（用户在办卡时支付） | YASBee → Interlace |
| Monthly Fee | 月费（如 $0.12~$0.25/月） | YASBee |
| Chargeback Fee | 退单费（$35/笔） | Interlace |

#### 4.2 费用列表

| 列 | 说明 |
|----|------|
| Fee ID | FEE-20260603-XXXXX |
| Card Number | 脱敏显示 |
| Fee Type | 标签分类（Network / Bank / Platform / Opening / Monthly / Chargeback） |
| Amount | 金额（正数=支出，负数=收入） |
| Currency | USD |
| Related TXN | 关联交易 ID |
| Status | Settled / Pending |
| Time | 产生时间 |

**筛选**：按 Fee Type、时间范围、卡片搜索

**汇总统计**（页面顶部）：

```
📊 Fee Summary (本月)
  Network Fee: $5.20    Bank Fee: $3.00
  Platform Income: $12.50
  Opening Fee: $10.00   Monthly Fee: $0.85
  Chargeback Fee: $35.00
```

#### 4.3 数据来源

- Opening / Monthly / Chargeback Fee：来自用户端的卡费用收取记录
- Network / Bank Fee：来自 Interlace 结算对账单
- Platform Income = 用户支付总费用 − 渠道成本总费用

---

### F-005 异常与退款处理

> 独立 Tab 或页面

**用户故事**：运营发现某笔交易异常（双花、金额异常、风控拦截），需要标记、暂停、发起退款或余额调整。

#### 5.1 异常交易标记

在交易流水详情中增加「Mark as Abnormal」按钮：

| 维度 | 内容 |
|------|------|
| **触发** | 运营在交易详情页点击「Mark as Abnormal」 |
| **必填信息** | 异常原因分类（Fraud / Duplicate / Amount Mismatch / System Error / Other）+ 说明文字 |
| **状态变化** | 该笔交易状态变为 Flagged；卡片可用余额扣除该笔金额（临时冻结） |
| **通知** | 创建 My Tasks 工单，分配给风控专员 |

#### 5.2 退款发起

在交易详情页或异常处理页操作：

| 维度 | 内容 |
|------|------|
| **操作流程** | 1. 选择目标交易<br>2. 输入退款金额（支持部分退款）<br>3. 选择退款原因（Merchant Error / System Error / User Request / Fraud）<br>4. 提交 → 生成退款交易记录（Type=Refund） |
| **金额限制** | ≤ $100：运营专员直接处理<br>> $100 且 ≤ $1,000：运营主管审批<br>> $1,000：运营主管 + 风控二级审批 |
| **余额校验** | 退款金额 ≤ 该笔交易原始金额 |
| **结果** | 退款成功 → 卡片余额增加；退款失败 → 记录失败原因 |

#### 5.3 余额调整

用于无法通过标准退款处理的场景（如系统故障导致余额错乱）：

| 维度 | 内容 |
|------|------|
| **操作流程** | 1. 搜索目标卡片<br>2. 输入调整金额（正=增加，负=减少）<br>3. 选择调整原因 + 备注（必填）<br>4. 运营主管审批 → 执行<br>5. 生成余额调整记录（Type=BalanceAdjustment） |
| **日志** | 记录调整前余额、调整后余额、操作人、审批人、时间 |

#### 5.4 争议工单（Dispute Tickets）

> P1 功能

| 维度 | 内容 |
|------|------|
| **列表** | 工单 ID / 关联交易 / 卡片 / 用户 / 状态 / 创建时间 |
| **状态** | Open → Processing → Resolved → Closed |
| **详情** | 工单信息 + 处理记录时间线 + 结案结果（WIN / LOSS + 金额） |
| **操作** | 提交处理结果、更新状态 |

---

## 4. 非功能需求

| 编号 | 需求 | 说明 |
|------|------|------|
| N-01 | 权限控制 | 按角色控制读写权限，操作记录可追溯 |
| N-02 | 操作审计 | 所有手动资金操作写入 Audit Log（操作人、时间、IP、前后数据） |
| N-03 | 数据一致性 | 手动充值/扣款需保证 YASBee 本地记录与 Interlace 余额一致 |
| N-04 | 余额防负 | 扣款操作需校验余额 ≥ 扣款金额 + 冻结金额 |
| N-05 | 金额精度 | 统一使用 2 位小数（Cent 精度） |
| N-06 | 性能 | 交易流水列表查询响应 ≤ 2s（10 万条数据规模） |
| N-07 | 导出 | 支持 CSV 导出交易流水和费用明细 |

---

## 5. 侧边栏布局建议

```
Channel Management
├── Card Service Management     ← 已有
├── Card Account Overview       ← 新增（本期 F-001）
│   ├── 🔍 Search Card
│   └── ├── 账户总览
│       ├── 交易流水（F-002）
│       ├── 充值/扣款（F-003）
│       └── 异常与退款（F-005）
├── Fee Management              ← 新增（本期 F-004）
├── Investment management       ← 已有（占位）
└── Rebate Management           ← 已有（占位）
```

---

## 6. 数据模型参考

### 6.1 现有 Card Product 字段（Card Service Management）

| 字段 | 类型 | 示例 |
|------|------|------|
| Card Name | string | Premium Card |
| Channel Card ID | string | Premium Card |
| Channel | string | interlace |
| Type | enum | Budget / Prepaid / Credit |
| Card Model | enum | Virtual Card / Physical Card |
| Google Wallet | bool | true |
| Apple Pay | bool | true |
| Opening Fee | decimal | $0 |
| Opening Rate | decimal | 0% |
| Recharge Rate | decimal | 0% |
| Recharge Fixed | decimal | $0 |
| Consumption Rate | decimal | 0% |
| Consumption Fixed | decimal | $0 |
| First Discount | decimal | $0 |
| Rebate Rate | decimal | 0% |
| Support Currency | string | USDT,USDC |
| Status | enum | Enabled / Disabled / Disabled by Channel |

### 6.2 本期新增核心实体

**Card Account**（每张已发行卡片一个账户）

| 字段 | 类型 | 说明 |
|------|------|------|
| card_id | string | YASBee 内部卡 ID |
| card_number | string | 脱敏卡号（后4位明文） |
| user_id | string | 用户 ID |
| card_product_id | string | 关联 Card Product |
| balance | decimal | 当前余额 |
| frozen_amount | decimal | 冻结金额 |
| total_recharge | decimal | 累计充值 |
| total_spent | decimal | 累计消费 |
| total_fees | decimal | 累计手续费 |
| currency | string | 账户币种（USD） |
| status | enum | Active / Frozen / Closed |
| created_at | datetime | 开卡时间 |
| updated_at | datetime | 最后更新时间 |

**Card Transaction**（交易流水）

| 字段 | 类型 | 说明 |
|------|------|------|
| txn_id | string | 唯一流水号 |
| card_id | string | 关联卡片 |
| user_id | string | 关联用户 |
| type | enum | Recharge / Consumption / Refund / Fee / BalanceAdjustment |
| amount | decimal | 金额（正=入，负=出） |
| currency | string | USD |
| balance_before | decimal | 交易前余额 |
| balance_after | decimal | 交易后余额 |
| status | enum | Success / Pending / Failed / Reversed / Flagged |
| operator | string | 操作人（手动操作时） |
| remark | string | 备注 |
| upstream_txn_id | string | Interlace 端交易 ID（如有） |
| created_at | datetime | 交易时间 |

**Fee Record**（费用记录）

| 字段 | 类型 | 说明 |
|------|------|------|
| fee_id | string | 费用 ID |
| card_id | string | 关联卡片 |
| fee_type | enum | NetworkFee / BankFee / PlatformIncome / OpeningFee / MonthlyFee / ChargebackFee |
| amount | decimal | 金额 |
| currency | string | USD |
| related_txn_id | string | 关联交易 |
| status | enum | Settled / Pending |
| created_at | datetime | 产生时间 |

---

## 7. 迭代计划

| Phase | 功能 | 周期 |
|:-----:|------|:----:|
| 1 | F-001 卡片账户总览 + F-002 交易流水查询 | 1.5 周 |
| 2 | F-003 充值/扣款管理 + F-004 手续费管理 | 1 周 |
| 3 | F-005 异常与退款处理（含审批流） | 1.5 周 |

---

## 8. 与现有系统的关系

| 现有页面 | 与本 PRD 关系 |
|---------|-------------|
| Card Service Management | 提供卡产品的费率配置，本期读取费率数据展示 |
| Fiat Transaction Management | 独立，本期为卡内资金流，非银行充提通道 |
| Dashboard / Overview | 独立，不重叠 |
| My Tasks | 异常标记后创建工单通知 |
管理端的加密模块下需要增加一个归集的表单页，可以选择对应的链和币种，设置自动归集的时间和间隔时间以及开关，也有手动归集触发按钮

还设计一个交易审核快照页，也是一个列表，每条数据是当日全部交易数据的快照，由财务任务进行复核，
