# 平台 KYC/KYB 二次审核优化 PRD

**版本**：v1.0  
**日期**：2026-06-10  
**状态**：初稿  
**适用范围**：平台级 KYC（个人认证）/ KYB（企业认证）

---

## 1. 背景与问题

### 1.1 当前现状

目前管理端 Verification 功能已支持：
- **KYC（Personal）**：个人认证审核，支持 Level 1 review / Level 2 review / Approved / Rejected / Suspended 五个状态
- **KYB（Company）**：企业认证审核，同上状态体系
- 每行记录提供 **View**（查看详情）和 **Suspend**（暂停/冻结）两个操作按钮

当前存在核心问题：

> **Suspend 后状态不可回滚**

当管理员对用户执行 Suspend 操作后，用户的 KYC/KYB 状态变为 Suspended，但缺乏后续的处理流程：
- 用户无法提交更新后的材料来"复活"认证
- 管理员无法对 Suspended 状态的用户执行"重新审核并恢复"操作
- Suspended 状态成为死胡同状态，已认证（Approved）用户被误操作 Suspend 后无法恢复

### 1.2 需求触发场景

| 场景 | 触发方 | 典型原因 |
|------|--------|---------|
| 场景 A | 管理员主动 Suspend | 证件过期、信息异常、合规风险 |
| 场景 B | 用户自主更新 | 换发新护照、变更公司信息 |

两种场景的处理逻辑不同，需要差异化设计。

---

## 2. 核心方案

### 2.1 状态语义变更

| 当前语义 | 优化后语义 |
|----------|-----------|
| Suspend = 冻结（不可逆） | Suspend = "置为未认证（需重审）" |
| Suspended 为终态 | Suspended 为中间态，可恢复 |
| 被 Suspend 的用户无操作入口 | 被 Suspend 的用户可提交更新材料 |

### 2.2 状态机设计

```
                  ┌──────────────────────────────────────┐
                  │          已认证（Approved）            │
                  └──────────┬────────────┬─────────────┘
                             │            │
                             │ 场景A      │ 场景B
                             ▼            ▼
              ┌──────────────────┐   ┌──────────────────────┐
              │ 未认证（需重审）   │   │  审核中（信息更新）    │
              │ (Suspended)      │   │  (Level 1 review)    │
              │ 平台账号冻结      │   │  状态保持"已认证"     │
              │ 只允许提交材料    │   │  不影响正常使用       │
              └────────┬─────────┘   └──────────┬───────────┘
                       │                        │
                       ▼                        ▼
              ┌──────────────────┐   ┌──────────────────────┐
              │  审核中（重审）    │   │  Diff 审核           │
              │  (Level 1 review) │   │  仅审变更字段         │
              └────────┬─────────┘   └──────────┬───────────┘
                       │                        │
              ┌────────┴────────┐      ┌────────┴────────┐
              ▼                 ▼      ▼                 ▼
        ┌──────────┐    ┌──────────┐ ┌──────────┐  ┌──────────┐
        │ 已认证    │    │ 驳回     │ │ 信息生效  │  │ 驳回     │
        │ (Approved)│    │ (Rejected)│ │ (Approved)│  │ (Rejected)│
        │ 解冻      │    │ 通知重新  │ │ 无需冻结  │  │ 通知重新  │
        └──────────┘    └──────────┘ └──────────┘  └──────────┘
```

### 2.3 场景详细流程

#### 场景 A：管理员触发 → 需冻结用户

```
1. 管理员在 Verification 列表发现用户证件过期/信息异常
2. 管理员点击 Suspend 按钮
3. 系统弹出确认弹窗 + 必填原因（如：证件过期、信息不匹配等）
4. 确认后：
   a. 用户 KYC/KYB 状态从 Approved → Suspended（显示为"未认证（需重审）"）
   b. 平台账号冻结（用户无法进行交易、提现等操作）
   c. 系统自动通知用户：认证被暂停，请重新提交材料
5. 用户登录后看到提示，进入 KYC/KYB 页面重新提交更新材料
6. 用户提交后，状态变为 Level 1 review
7. 管理员在 Verification 列表中看到该记录，执行全量审核
8. 审核通过 → 状态恢复 Approved，账号解冻
   审核驳回 → 状态回到 Suspended，通知用户继续补充材料
```

#### 场景 B：用户自主更新 → 不需冻结

```
1. 用户登录后自行发起 KYC/KYB 信息更新
2. 无需管理员介入，用户直接上传新证件/新信息
3. 状态保持 Approved（不变），不影响使用
4. 系统自动创建审核任务，管理员在 Verification 列表中出现一条"Level 1 review"记录
5. 管理员点击 View 查看变更内容的 Diff（新旧对比）
6. 仅审核变更字段
7. 审核通过 → 新信息生效，状态保持 Approved
   审核驳回 → 新信息驳回，保留旧信息，状态保持 Approved
```

---

## 3. 功能需求

### F-01：Suspend 弹窗优化

**优先级**：P0  
**用户故事**：管理员点击 Suspend 时，需要明确原因和影响范围

**业务规则**：
- 点击 Suspend 后弹出确认弹窗
- 弹窗包含：
  - 原因选择（单选或下拉）：证件过期 / 信息不匹配 / 合规风险 / 其他（自定义填写）
  - 原因说明文本框（必填）
  - 影响提示文案：该操作将暂停用户的平台访问权限，用户需重新提交认证材料
  - 确认按钮 + 取消按钮
- 确认后，系统记录管理员 ID、操作时间、原因

**字段定义**：

| 字段 | 类型 | 说明 |
|------|------|------|
| suspend_reason | enum | 证件过期 / 信息不匹配 / 合规风险 / 其他 |
| suspend_reason_detail | text | 自定义补充说明 |
| suspended_by | string | 操作管理员 ID |
| suspended_at | datetime | 操作时间戳 |

### F-02：Suspended 状态的恢复流程

**优先级**：P0  
**用户故事**：被 Suspend 的用户可以重新提交 KYC/KYB 材料，管理员可以重新审核恢复

**业务规则**：
- Suspended 用户登录后可查看 Suspend 原因
- 用户可在此状态下重新上传认证材料（重新 KYC/KYB 全流程）
- 用户提交后状态变为 Level 1 review
- 管理员审核通过 → Approved + 解冻
- 管理员审核驳回 → 回到 Suspended（非 Rejected，保留继续提交能力）

**状态流转**：

| 当前状态 | 操作 | 目标状态 |
|----------|------|---------|
| Suspended | 用户提交材料 | Level 1 review |
| Level 1 review | 管理员通过 | Approved（解冻） |
| Level 1 review | 管理员驳回 | Suspended（回到冻结，可重提） |

### F-03：审核详情页优化（View 页面）

**优先级**：P1  
**用户故事**：管理员查看审核详情时，能区分"全量审核"和"Diff 审核"两种模式

**场景 A 全量审核页面**：
- 显示用户所有认证信息字段（与新建审核时一致）
- 历史认证材料归档（可查看历史提交记录）
- Suspend 原因展示
- 审核操作：Approve / Reject

**场景 B Diff 审核页面**：
- 显示变更字段的新旧对比（左右对照）
- 未变更字段折叠，只展示变更部分
- 变更摘要：共修改了 N 个字段
- 审核操作：Approve Changes / Reject Changes

### F-04：用户端通知

**优先级**：P1  
**用户故事**：用户在不同审核状态变化时收到通知

**通知规则**：

| 触发事件 | 通知方式 | 通知内容 |
|----------|---------|---------|
| 管理员 Suspend | 邮件 / App 推送 | 您的 KYC/KYB 认证已被暂停，原因：{原因}，请重新提交认证材料 |
| 审核通过（场景 A） | 邮件 / App 推送 | 您的认证已通过，平台权限已恢复 |
| 审核驳回（场景 A） | 邮件 / App 推送 | 您提交的材料未通过审核，原因：{原因}，请修改后重新提交 |
| 审核通过（场景 B） | 邮件 / App 推送 | 您的认证信息已更新成功 |
| 审核驳回（场景 B） | 邮件 / App 推送 | 您提交的信息变更未通过审核，原有信息保持不变 |

### F-05：审核记录与审计日志

**优先级**：P2  
**用户故事**：所有审核操作可追溯

**业务规则**：
- 每次 Suspend 操作记录完整审计日志（操作人、时间、原因）
- 每次审核（Approve / Reject）记录审核人、审核时间、备注
- 显示用户的审核历史时间线

**审计日志字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| customer_id | string | 用户/企业 ID |
| action | enum | suspend / unsuspend / approve / reject / resubmit |
| operator_id | string | 操作人（管理员或用户本人） |
| operator_type | enum | admin / user / system |
| reason | text | 操作原因 |
| old_status | enum | 操作前状态 |
| new_status | enum | 操作后状态 |
| created_at | datetime | 操作时间 |

### F-06：Dashboard 统计面板

**优先级**：P2  
**用户故事**：管理员在 Dashboard 能看清审核工作量和趋势

**当前已有**：Total Cases / In Progress / Approved / Rejected / Suspended（全局统计）

**需补充**：
- 场景 A vs 场景 B 的审核量区分
- 平均审核处理时间（Suspend → Approved）
- 今日新增 Suspend 数、今日审核完数
- 待分配审核任务数

---

## 4. 非功能需求

### 4.1 权限控制

- 只有拥有"审核员"角色的管理员才能 Suspend / Approve / Reject
- Suspend 操作应开启二级确认（弹窗 + 原因必填）
- 同一条认证记录不能同时被多位管理员审核（锁定机制）

### 4.2 数据安全

- 所有审核操作写审计日志，不可删除
- 用户提交的认证材料加密存储
- Diff 审核时，新旧材料对比不泄露未变更的敏感信息

### 4.3 性能

- Verification 列表支持 10 万+ 条记录的分页查询
- Suspend → 通知用户的延迟不超过 5 分钟

---

## 5. 数据模型变更

### 5.1 现有表扩展

在 `customer_kyc`（或 `customer_kyb`）表中增加字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| status_history | JSON[] | [{status, changed_by, reason, timestamp}] |
| review_mode | enum | full / diff - 区分审核模式 |
| latest_update_request_at | datetime | 用户最近一次提交更新请求时间 |
| update_request_fields | JSON | 场景 B 下变更的字段清单 |

### 5.2 新表：审核审计表

```
audit_review_log
├── id
├── customer_id
├── customer_type: personal / company
├── action: suspend / unsuspend / approve / reject / resubmit
├── operator_id
├── operator_type: admin / user
├── reason
├── old_status
├── new_status
├── reviewer_notes (审核备注)
├── created_at
└── metadata (JSON, 扩展信息)
```

---

## 6. UI 改动摘要

| 页面 | 改动项 |
|------|--------|
| Verification 列表 | Suspended 状态下增加"可重新提交"标识 |
| Suspend 弹窗 | 新增原因选择 + 影响提示 |
| View 详情页 | 区分"全量审核"和"Diff 审核"两种视图模式 |
| Dashboard Overview | 增加审核细分统计 |
| 用户端 KYC/KYB 页面 | Suspended 状态下显示原因 + 重新提交入口 |

---

## 7. 附录

### 7.1 术语表

| 术语 | 说明 |
|------|------|
| KYC | Know Your Customer，个人实名认证 |
| KYB | Know Your Business，企业实名认证 |
| Suspend | 暂停认证状态，冻结平台账号权限 |
| Level 1 review | 一级审核（待初审） |
| Level 2 review | 二级审核（待复审） |
| Approved | 审核通过 |
| Rejected | 审核驳回 |
| Diff 审核 | 仅对比变更字段的审核模式 |

### 7.2 开放问题

1. **用户自主更新 KYC/KYB 是否有频率限制？**（如 30 天内最多 3 次）
2. **场景 B Diff 审核驳回后，是否允许用户立即重新提交？**（建议与新申请相同冷却期）
3. **Suspended 是否需要在客户端的 Card 模块同步冻结？**（当前管理端与 Card 产品是否共享用户体系？）
