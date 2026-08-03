# Mesh（ComplyAdvantage）接入分析

> 来源：https://docs.mesh.complyadvantage.com/v2.1/docs/getting-started
> 整理日期：2026-08-03 ｜ 整理者：AI（产品视角）

## 一、Mesh 是什么

ComplyAdvantage Mesh 是一个 **AML（反洗钱）客户风险持续评估平台**：

- 客户入驻（onboarding）时可创建客户、算初始风险分、做 AML 筛查
- 持续监控（ongoing monitoring）阶段可 24 小时循环重筛查
- 案件管理（case management）用于优先级排序和人工评审风险告警

**关键概念（产品必须懂）**：

| 概念 | 含义 | 产品含义 |
|---|---|---|
| Customer 客户 | 与你有直接业务关系的人/公司 | 对应我们平台的开户对象 |
| Screening Configuration 筛查配置 | 决定查什么：制裁名单/警告名单/合规与适格名单/PEP 政要名单/负面媒体，可建多个 | 需要合规团队参与制定 |
| Risk Score 风险分 | 可配置公式算出的数值（选类别+选属性+加权） | 映射到低/中/高/禁止 4 档风险级别 |
| Case 案件 | 筛查命中时自动创建 | 等于"待人工评审工单" |
| Alert 告警 | 案件内的一条可疑信号 | 一个案件可含多个告警 |
| Profile 匹配档案 | 告警内命中的对象信息（姓名/DOB/关联关系/命中名单） | 人工判断是否真是本人 |

**风险级别（onboarding 阶段即返回）**：LOW-RISK / MEDIUM-RISK / HIGH-RISK / PROHIBITED（禁止）

**筛查结果（screening_result）**：`NO_PROFILES`（未命中）/ `HAS_PROFILES`（命中 1+ 档案）

**AML 类型**（命中的类型）：SANCTION（制裁）、PEP_CLASS_1~4（政要分级）、ADVERSE_MEDIA（负面媒体，细分为金融/欺诈/毒品/恐怖/网络犯罪/监管等 12+ 子类）、WARNINGS、FITNESS-PROBITY。

## 二、业务流程图（标准客户入驻 + 监控工作流）

```
┌─────────────────────────────────────────────────────────────┐
│ 接入前准备（一次性）                                          │
│ ① 开通账号 → 拿 API 凭据（realm 组织名 + API邮箱 + 密码）      │
│ ② 创建筛查配置（查哪些名单）→ 记下 configuration_identifier   │
│    ⚠ 需合规/风控团队共同制定，可随时改                        │
│ ③ 决定集成模式（二选一或混合）：                              │
│    A. 同步筛查：开户实时等待结果（1-3 秒返回）                │
│    B. 异步筛查：不等待，结果由 webhook 推送（适合大批量）      │
└───────────────────────┬─────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 客户入驻（每个新客户触发）                                    │
│ ④ 调「创建并筛查客户」API                                    │
│    入参：客户信息 + external_identifier（我方客户ID，必填且唯一）│
│    返回：customer_identifier（必须存库）+ 风险级别 + 筛查结果  │
└───────────────────────┬─────────────────────────────────────┘
                        ▼
              ┌─────────┴──────────┐
              ▼                    ▼
      未命中 NO_PROFILES      命中 HAS_PROFILES
      自动放行（STP）           ⏸ 暂停开户 → 生成案件
      继续开户流程              │
              │                ▼
              │        案件评审（两条路二选一）：
              │        ├─ Mesh 网页版人工评审（不深度集成）
              │        └─ API 拉取告警/风险 → 导入自有案件系统
              │                │
              │                ▼
              │        人工决策（case 决策）：
              │        无风险 / 有风险-接受 / 有风险-离船(offboard)
              │                │
              │                ▼
              │        ┌───────┴────────┐
              │        ▼                ▼
              │   POSITIVE（通过）   NEGATIVE（拒绝）
              │   放行继续开户       拦截客户/终止关系
              │        │
              ▼        ▼
┌─────────────────────────────────────────────────────────────┐
│ 持续监控（可选，按客户开启）                                  │
│ 每 24h 用最新名单重筛查 → 新命中自动生成新案件 → 同上评审      │
│ 客户信息变更 → 调 update-and-rescore（更新+重算风险分）       │
│ 客户关系结束/关户 → 关闭监控（停止计费、保留历史案件审计）      │
└─────────────────────────────────────────────────────────────┘
```

## 三、三个必须先定的产品决策

### 决策 1：客户入驻是实时还是异步？
- **同步**：注册/开户表单提交后卡住 1-3 秒等筛查结果 → 适合"实时决策"体验，可立即放行或拦截
- **异步**：先收单后筛查，webhook 通知结果 → 适合大批量/风控复审流程
- 文档推荐：实时开户场景用同步 + `last_sync_step=ALERTING`（一次调用拿全结果）

### 决策 2：案件评审在哪里做？
- **方案 A：用 Mesh 网页版**（零开发，运营在对方后台点）—— 只需一个 `CASE_STATE_UPDATED` webhook 把结果推回我们系统
- **方案 B：自建/接入自有案件系统** —— 需要实现告警拉取、风险详情、决策回写等 API
- 影响集成工作量 3-5 倍差异，产品上影响运营团队的工作习惯

### 决策 3：持续监控开不开？
- 开启后客户每 24h 重筛查，新命中自动生成案件（合规价值高，但**按筛查量计费，成本随客户数线性增长**）
- 建议：高风险客户开、低风险关，或全开但配合静音(mute)规则减少噪音

## 四、需要了解的内容清单（对接前向 Mesh 方确认）

### 商务 / 合同类
1. **计费模型**：按筛查次数？按月订阅？批量折扣？（文档未公开，需 account manager）
2. **区域/数据驻留**：EU / EU3 / US / US2 / CA / AU 六个区域实例，选哪个影响 webhook 来源 IP 和数据合规
3. **费率调整**：默认限流 300 次/分钟，可申请调整
4. **webhook 签名**：按账号开启（opt-in），密钥轮换走人工支持

### 合规 / 配置类
5. **筛查配置内容**：用哪些名单组合？不同客户群体（个人/公司/不同国家）是否要不同配置？
6. **风险分公式**：选哪些类别/属性、各占多少权重、阈值映射到低/中/高/禁止 —— 必须合规团队参与
7. **PEP 分级策略**：PEP_CLASS_1~4 各自怎么处理（一票否决 or 加权计分）
8. **负面媒体子类**：12+ 子类（欺诈/毒品/恐怖/网络犯罪…）哪些该直接拒、哪些进人工
9. **PROHIBITED 自动处理**：是否见到 PROHIBITED 就自动离船（文档建议考虑）

### 技术 / 集成类
10. **external_identifier 映射**：我方客户 ID 必须唯一且映射回 CRM，重复会 409
11. **customer_identifier 存储**：创建后必须存库，后续监控/更新/查案件都靠它
12. **token 生命周期**：access token 24h 过期，需要自动刷新（文档建议 23h 刷新）
13. **webhook 幂等**：at-least-once 投递会重复，必须按 webhook-id 去重；签名校验用 Standard Webhooks v1 库
14. **错误处理**：400/401/403/404/409/429/500 的处置（429 退避重试、500 最多 3 次）
15. **沙盒测试**：用沙盒账号，测试用例（干净客户 "Test CleanUser" → NO_PROFILES；潜在命中 "Victor Bout" → HAS_PROFILES）
16. **API 用户最佳实践**：专用邮箱、沙盒/生产分离（避免切账号）

### 产品 / 体验类
17. **开户流程 UX**：同步模式要设计"筛查中"等待态（1-3 秒）；命中客户如何给前台提示（"审核中"而非直接拒）
18. **风控复审工作流**：谁负责看案件？SLA 多久？是否设自动超时策略
19. **客户变更流程**：地址/国籍/产品变更触发 update-and-rescore，重新计分可能升档触发再筛查
20. **关闭监控流程**：关户即停监控（省钱），历史案件保留供审计

## 五、关键 API 速查（给研发对照）

| 步骤 | 端点 |
|---|---|
| 鉴权 | `POST /v2/token`（realm + username + password → Bearer token，24h） |
| 同步创建+筛查 | `POST /v2/workflows/sync/create-and-screen` |
| 异步创建+筛查 | `POST /v2/workflows/async/create-and-screen`（返回 workflow_instance_identifier） |
| 查工作流状态（轮询） | `GET .../workflows/{workflow_instance_identifier}` |
| 批量上传 | `POST /v2/batch-processing`（CSV 批量建客户/批量交易监控） |
| 注册 webhook | `POST /v2/notifications/configurations/webhook`（CASE_STATE_UPDATED / CASE_CREATED / WORKFLOW_COMPLETED） |
| 查案件列表/详情 | `GET /v2/cases`、`GET /v2/cases/{id}` |
| 查告警内风险 | `GET .../alerts/{alert_identifier}/risks` |
| 更新客户+重算分 | `PATCH /v2/customers/{id}/workflows/sync/update-and-rescore` |
| 开关监控 | `PATCH /v2/customers/{id}/monitor` |

## 六、术语对照表（产品 ↔ Mesh）

| 我们（产品语言） | Mesh 术语 |
|---|---|
| 开户/注册 | Create and Screen Customer |
| 风控名单 | Screening Configuration |
| 客户风险分 | Risk Score → Level（低/中/高/禁止） |
| 待审核工单 | Case |
| 工单里的可疑点 | Alert |
| 命中的那个人 | Profile |
| 审批通过/拒绝 | case_stage.decision_type = POSITIVE / NEGATIVE |
| 拉黑/终止 | Offboard / PROHIBITED |
| 定期复查 | Ongoing Monitoring（24h rescreen） |
