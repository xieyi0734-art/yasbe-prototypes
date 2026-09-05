# PRD — YASBe 法币账户（欧元 / 英镑 · OpenPayd 通道）

| 项 | 内容 |
| --- | --- |
| 产品 | YASBe · 法币账户（EUR / GBP）开户、入金、出金与同名外部账户管理 |
| 底层 | OpenPayd（Linked Client 模式，平台后端直连 OpenPayd API） |
| 本文档状态 | Draft v0.1，待评审（产品 + 研发，逐句验收） |
| 日期 | 2026-09-05 |
| 对齐原型 | `03-法币账户-欧元英镑-多渠道多账户.html`（开户向导 / 收款账户信息 / 提现 / 外部同名账户 / 交易记录 / 演示控制） |
| API 基准 | 本地权威副本 `opd_full_spec.json`（OpenPayd OpenAPI）；与 apidocs.openpayd.com 在线文档冲突时以在线文档为准，并回写本 PRD |
| 字段纪律 | 本 PRD 所有 OpenPayd 字段名、必填约束、枚举均直接取自上述 spec，未经验证的字段/逻辑一律标注 ❓ 待确认，不臆造 |

---

## 1. 背景与目标

### 1.1 背景
YASBe 通过 OpenPayd 为用户提供一条**欧元 / 英镑法币账户通道**：平台为已完成 KYB 建档的主体（个人 / 企业）开立 OpenPayd 法币账户（Account），账户 ACTIVE 后系统获得该账户专属的**收款账户信息（Payment Account）**；用户从**本人（同名）的外部银行账户**向收款账户转账完成入金，平台凭 OpenPayd 的 Pay In 到账通知在自有账本为用户入账；出金时用户只能选择**已添加且通过同名核验的外部同名账户（EA）**作为收款目的地，平台调用 OpenPayd 发款。

> 一句话：**法币账户是"入金收款管道"，外部同名账户是"出金收款目的地"，平台余额是"用户可支配记账"；同名（户主=本人/本企业）是本产品在出入金两端的强约束。**
>
> 与 OpenPayd 的关系：OpenPayd 的 API 本身**不强制要求**入金来源或出金目的地与账户持有人同名（出金仅要求指向已创建的 Beneficiary 对象）；**"同名"是 YASBe 产品层强加的合规约束**（见 M3 / M4 / §12 未决）。

### 1.2 要解决的用户问题
1. 海外 / 跨境用户需要欧元、英镑本地收款能力（IBAN / 本地账号 / Sort Code），用于把法币安全地转入平台并形成可用余额。
2. 用户需要"像给自己的银行账户转账一样"的入金体验，以及"只能回到自己同名银行账户"的可信出金闭环。
3. 平台需要合规外壳：资金经由 OpenPayd 持牌机构收款账户进出，出金目标必须是本人同名账户，杜绝向任意第三方账户代付。

### 1.3 产品目标
- G1 开户 → 入金 → 出金 → 记录全链路对用户可理解、可操作、低摩擦；收款字段与到账/费用规则清楚。
- G2 合规对齐：主体 KYB 建档先行（个人 / 企业双主体）；同名强约束产品化——入金来源同名核验（到账环节）、出金目的地同名（创建环节锁定 + 核验）。
- G3 与 OpenPayd API 的字段 / 必填 / 状态逻辑**完全一致**，评审可对照 OpenPayd API 文档逐字段核对（本 PRD 附录 A 为逐字段映射）。

### 1.4 非目标（本阶段不做）
- 非同名出金（向任意第三方银行账户收款）——设计为**不可行路径**而非默认开放。
- 非同名入金的自动入账或留存——不设计为默认放行（处置见 M3-5 / §8 / §12 F1）。
- 币种兑换（Exchange / FX）——本版业务流程不含兑换入口；交易类型词表预留 `exchange` 展示位。
- EUR / GBP 之外的法币账户（USD 等由其他通道承接，见同目录 USD 版 PRD）。
- 出金支付类型超出 SEPA / Faster Payments 的范围（CHAPS / SWIFT 出金是否开放 → §12 F5）。
- 后台运营系统（真实后端角色 / 审批流）；原型用"演示控制"面板模拟异步状态（§7 / §11）。
- 多语言超出 zh / en。

---

## 2. 名词与术语

| 术语 | 英文 | 说明 |
| --- | --- | --- |
| 法币账户 | Fiat Account / Account | 平台在 OpenPayd 为客户主体开立的指定币种（EUR / GBP）账户；账户登记在平台（Linked Client）名下，用户享有平台记账权益。对应 OpenPayd `POST /accounts` 返回的 Account Object |
| 收款账户信息 | Payment Account / Bank Account | 法币账户 ACTIVE 后，OpenPayd 为该账户分配的专属收款账号（iban / bic / accountNumber / routingCodeEntries / payInReference 等），用户照此从自己的银行转账。对应 `GET /bank-accounts` 返回的 Payment Account Object |
| 入金通道 / 支付类型 | Rail / Payment Type | 收款账户可接收与出金可使用的支付类型：GBP：Faster Payments / CHAPS / SWIFT；EUR：SEPA / SEPA Instant / SWIFT（原型 rails 常量，§6 M2） |
| 附言 | Reference / payInReference | 入金时用户须在转账附言填写的参考号（`payInReference`），用于平台 / OpenPayd 匹配到账归属（收款账户字段、到账通知中的 `transactionReference`） |
| 外部同名账户 | External Account（EA） | 用户添加的、户名与其本人（个人全名 / 企业注册名）**一致**的外部银行账户；OpenPayd 侧对应 **Beneficiary（收款人档案）+ Bank Beneficiary（银行收款账户）** 两层对象 |
| 收款人档案 | Beneficiary | `POST /beneficiaries` 创建的对象；`beneficiaryType` = RETAIL（个人）/ CORPORATE（企业），`tag` = SELF 表示"受益人即账户持有人本人" |
| 银行收款账户 | Bank Beneficiary | `POST /beneficiaries/{parentBeneficiaryId}/bank-beneficiaries` 创建的对象；持有 iban / bic（欧洲）或 accountNumber + sort code（英国），是出金交易的目的地 |
| 同名核验 / 持有人核验 | CoP（Confirmation of Payee） | 平台对 EA 持有人姓名与主体实名一致性的核验：英国账户走 OpenPayd `POST /beneficiaries/verify`（CoP，返回 MATCH 等）；欧洲 IBAN 账户无 CoP 端点，核验方式见 §12 F3。核验通过（原型 `verified`）前 EA **不可用于出金** |
| 平台余额 | Platform balance | 平台账本上用户可支配金额：入金上账增加，出金提交时扣减；不等同于 OpenPayd 单笔账户余额（需呈现可用 / 在途口径） |
| KYB 建档 | KYB / Account Holder | 开户前置：主体（个人实名 / 企业注册资料）提交平台并完成合规审核，形成 OpenPayd 环境内可开户的客户档案（原型预设：个人 XIAOMING LI；企业 ABC LTD） |
| 主体 | Subject | 当前操作所代表的主体：INDIVIDUAL（个人）/ BUSINESS（企业）；决定开户字段组、出金可用 EA 范围、入金收款户主名（§6 M0） |

---

## 3. 范围（In / Out of scope）

**In scope**
- 主体与准入：个人 / 企业双主体；开户前国别可服务性拦截；KYB 建档信息采集（开户向导第 2 步）。
- 开户：币种选择（EUR / GBP，可多账户）→ 建档信息确认 / 补齐 → 预览收款账户 → 提交（OpenPayd Create Account）→ PENDING → ACTIVE。
- 收款账户信息展示与入金：按通道展示 Payment Account 字段、到账时效 / 截止 / 限额、附言 Reference 规则、同名引导。
- 入金到账与上账：Pay In 到账通知 → 同名核验 → 平台入账；**非同名入金的处置流程（❓ 退款机制 OpenPayd 未确认，§12 F1）**。
- 外部同名账户（EA）：添加（= 新建 Beneficiaries + bank Beneficiaries 两层）、持有人字段锁定、同名核验（pending → verified）、列表与出金可用性。
- 出金：选择已核验同名 EA（币种 + 主体一致）→ 金额 / 附言 → 提交（OpenPayd Create Payout）→ 状态推进与失败回滚展示。
- 交易记录与账户生命周期展示。

**Out of scope**
- 非同名出金 / 任意第三方银行账户出金；非同名入金默认放行。
- Exchange / FX 兑换流程；USD 及其他币种（由 USD 通道 PRD 承接）。
- 运营后台的真实审核 / 审批系统（评审用演示面板模拟，见 §7 / §11）。
- 多语言 > zh / en。

---

## 4. 用户与角色

| 角色 | 说明 | 核心诉求 |
| --- | --- | --- |
| 个人用户 | 已完成个人实名（KYB）的自然人，拥有本人同名外部银行账户 | 快速开户；清楚看到收款账户怎么用、到账时效、手续费；能安全出金回自己同名账户 |
| 企业用户 | 已完成企业 KYB 的主体（示例 ABC LTD），拥有企业对公银行账户 | 对公账户开户 / 收款 / 出金到企业对公同名账户；主体切换后所有弹窗默认字段随之切换 |
| 平台运营 / 审核员 | 复核 EA 同名核验人工兜底、处置非同名入金、被拒重提 | 看清核验状态与入金来源，能标记 / 推进状态（真实后台本期不做，评审用 demo 面板） |
| 平台合规 / 风控 | 维护国别名单、同名规则口径、退款处置策略 | 同名规则可解释、可审计；退款路径清晰（待 OpenPayd 确认，§12 F1） |
| 平台研发 | 对接 OpenPayd Account / Beneficiary / Bank-Beneficiary / Payout / webhook | 幂等、可重试、密钥不落前端；本 PRD 中 ❓ 项的最终判断方 |

---

## 5. 核心业务流程（主路径）

### 5.1 总览
```
[0 主体]  个人 / 企业 KYB 建档完成（原型预设：个人 XIAOMING LI；企业 ABC LTD）
[1 开户]  向导：选币种(EUR/GBP) → 建档信息确认补齐(KYB) → 预览收款账户
          → 提交 POST /accounts → PENDING →(OpenPayd 推进)→ ACTIVE
          → 收款账户信息生效（GET /bank-accounts）
[2 入金]  打开「收款账户信息」→ 选通道 → 展示收款账号/户主/附言 Reference/时效
          → 用户从本人(同名)银行账户转账(附言填 payInReference)
          → OpenPayd 收款 → Pay In 到账通知(含 senderName 等)
          → 平台同名核验: 同名 → 入账; 非同名 → 挂账/退款 ❓(§12 F1)
[3 EA]    添加外部同名账户: 选地区(欧洲IBAN / 英国) → 填银行信息
          （账户名称/持有人锁定=主体名,不可改）
          → 创建 Beneficiary(tag=SELF) → 创建 Bank Beneficiary
          → 同名核验(英国 CoP MATCH / 欧洲按平台规则) pending → verified
[4 出金]  选法币账户 → 选已核验同名 EA(币种+主体一致) → 金额+附言
          → POST /transactions/bank-payouts(beneficiaryId=该 EA 的 bankBeneficiaryId)
          → INITIATED → PROCESSING → RELEASED → COMPLETED / FAILED(资金回滚)
[5 记录]  交易流水（payin / payout）+ 账户生命周期展示
```

### 5.2 关键不变量
- **I1 先建档后开户**：仅已完成 KYB 建档的主体可开户；开户提交 = OpenPayd Create Account（返回 status=PENDING），账户 ACTIVE 后收款账户信息才生效、才可接收入金。
- **I2 入金只进本人名下的收款账户**：收款账户户主（holder）= 主体实名；平台引导用户"仅从本人（同名）银行账户转入"；**同名来源是平台强制核验项**（OpenPayd 到账通知含 senderName，供平台比对），非同名资金不默认入账（处置 ❓）。
- **I3 出金只到同名 EA**：可出金目标必须是与主体同名、且通过同名核验（verified）的外部账户；EA 的持有人字段（bankAccountHolderName）由系统锁定为主体实名，用户不可修改。
- **I4 EA = Beneficiary 两层对象**：每个 EA 在 OpenPayd 侧必须先创建 Parent Beneficiary（tag=SELF），再在其下创建 Bank Beneficiary；出金请求携带的是 Bank Beneficiary 的 id。
- **I5 平台余额 = 记账**：可用余额与在途需清晰区分；交易状态以 OpenPayd 返回为准，平台做展示映射，不虚构中间态。
- **I6 币种与主体约束贯穿出金**：出金账户（法币账户）与 EA 须同币种，且两者主体一致（个人账户 → 个人 EA；企业账户 → 企业 EA）。

---

## 6. 功能需求（按模块）

> 每条含验收要点；**对齐**列指向 OpenPayd spec 端点 / 原型出处；**❓** = 需研发 / 产品判断的开放项（集中汇总于 §12）。
> 主体词说明：原型内部用 INDIVIDUAL / BUSINESS，OpenPayd 侧对应词为 beneficiaryType 的 RETAIL / CORPORATE（附录 B 有词表）；本 PRD 正文"主体"沿用产品词，送参映射在附录 B 标明。

### M0 主体与准入

| ID | 需求 | 验收要点 | 对齐 |
| --- | --- | --- | --- |
| M0-1 | 双主体（个人 / 企业）贯穿全页面 | 页面存在**当前主体**（原型 `#dSubject` = INDIVIDUAL / BUSINESS），并**全局驱动**所有弹窗默认字段：开户向导第 2 步字段组（个人 vs 企业）、添加外部同名账户的锁定持有人名、出金可用 EA 范围、入金收款户主名。弹窗内不再出现主体单选（2026-09-05 已重构） | 原型 03：`dSubject` + `flow.subject` / `eaf.subject`；见 §12 已决策 D1 |
| M0-2 | 开户前国别可服务性拦截 | 不可服务国家 / 地区（原型示例 UNSERVED_CODES：CHN / JPN / DZA / BDI / TUN）在开户第 2 步即拦截并给出明确原因，不可继续提交；可服务国家正常放行 | 原型 03：`renderCompliancePanels` / `unservedText`；非 OpenPayd 字段，平台合规名单 |
| M0-3 | 开户前置 KYB 建档 | 开户向导第 2 步采集的持有人资料（个人：姓名 / 证件 / 地址；企业：注册名 / 注册号 / 公司类型 / 注册地址）属于**平台 KYB 建档信息**，用于主体在 OpenPayd 环境的合规档案（Account Holder），**不是** `POST /accounts` 的请求字段 | 原型 03 step2（opIndivFields / opBizFields）｜❓ F7：Account Holder 建档与 KYB 文档上传在 OpenPayd 的接口形态不在本 spec 范围（spec 仅有 `/linkedClient`），需研发确认与 OpenPayd 的实际建档 / 审核方式 |
| M0-4 | 建档信息校验规则 | 个人：名 / 姓 / 邮箱 / 地址 / 城市 / 国家必填且格式校验（邮箱格式、地址 3–35 字符、禁 PO Box / PMB）；企业：公司名 / 注册号 / 公司类型 / 公司邮箱 / 注册地址必填；行业选 OTHER 时须补充行业描述。证件（个人）为选填组 | 原型 03：VALIDATORS（opFname…opRCountry / opIndVal）；errIban / errBic / errStreet / errPobox |

### M1 开通法币账户（开户）

| ID | 需求 | 验收要点 | 对齐 |
| --- | --- | --- | --- |
| M1-1 | 开户向导 = 三步 | ① 选币种（EUR / GBP，可多账户，同币种可重复开通并自动命名"…收款账户 2"）；② 建档信息（见 M0-3）；③ 预览与协议确认 | 原型 03：obModal step1/2/3；`defaultAccName` |
| M1-2 | 提交 = OpenPayd Create Account | 平台后端调 `POST /accounts`，请求体仅需映射：`currency`（必填，ISO 4217）；`friendlyName`（= 用户自定义账户名）；多币种关联 / `ibanCountry` / `endToEndReference` 本期不使用（EUR 在 UK 平台开立时 `ibanCountry` 按 OpenPayd 要求需评估，❓ F7 一并确认）。**建档资料不回传本接口** | spec：POST /accounts（required: [`currency`]） |
| M1-3 | 开户响应即 PENDING | 提交成功后进入 PENDING：原型弹窗提示"审核通过后将生成专属收款账户号码"；PENDING 状态下账户卡不展示 rails 收款字段、不可发起收款 / 提现（无操作按钮） | spec：POST /accounts 201 → `status` 示例 `PENDING`；原型：`statusChip` / `pendAccNote` / accCard |
| M1-4 | PENDING → ACTIVE | 账户被 OpenPayd 激活（ACTIVE）后收款账户信息生效：账户卡展示币种尾号 / IBAN（EUR）/ Sort Code（GBP）+ 通道标签 + 入金 / 提现按钮。原型用演示按钮 `dActivate` 模拟推进（评审工具）；生产靠轮询 `GET /accounts/{id}` 或 OpenPayd 通知 | spec：GET /accounts/{id}（status 推进）；原型：`dActivate` |
| M1-5 | 多账户与默认账户 | 每币种可开多个账户，支持 primary 标识（原型种子含 a-eur-01 / a-eur-02 等）；账户命名不重复 | 原型 03：ACCOUNTS 种子 / `defaultAccName` |

### M2 收款账户信息与入金（打款说明书）

| ID | 需求 | 验收要点 | 对齐 |
| --- | --- | --- | --- |
| M2-1 | 入金弹窗主体 = Payment Account 收款字段 | 「收款账户信息」弹窗展示该法币账户的收款账号字段（按所选通道过滤）：银行名称 / 银行地址 / **账户持有人名称（= 主体实名）** / 账号 / IBAN / BIC / Sort Code / 附言 Reference | spec：GET /bank-accounts（Payment Account Object，字段映射见附录 A2）；原型：`renderAmBody` |
| M2-2 | 按通道展示字段 | EUR 收款账户通道 SEPA / SEPA Instant / SWIFT → 展示 bankName / bankAddress / holder / iban / bic（SEPA 系 + payInRef）；GBP 收款账户通道 Faster Payments / CHAPS / SWIFT → 展示 bankName / holder / sortCode / accountNumber（+ payInRef）；字段缺省不展示 | 原型 03：RAIL_FIELDS；与 Payment Account 的 `iban` / `bic` / `accountNumber` / `routingCodeEntries`（SORT_CODE）/ `payInReference` 对应 |
| M2-3 | 到账时效 / 截止 / 限额 | 展示所选通道的 arrive（预计到账）、cutoff（当日截止）、limit（单笔限额）。数值为平台维护的通道元数据（非 OpenPayd 账户字段）：SEPA 2–3 小时（工作日）；SEPA Instant 实时（€100,000）；SWIFT 2–5 个工作日；FPS 实时（£1,000,000）；CHAPS 1–2 小时（工作日） | 原型 03：RAILS 常量（zh/en）｜费率 / 时效以平台费率表为准（❓ 需与 OpenPayd 对账） |
| M2-4 | 附言 Reference 规则 | 有 `payInReference` 的账户提示"转账附言须填 Reference 用于入账匹配，未填将延迟入账"；收款字段逐项可复制 + 一键复制全部 | 原型 03：refNote / copy；spec：Payment Account 的 `payInReference` |
| M2-5 | 同名引导 | 弹窗顶部引导语："这是您本人名下的入金账户：请仅从您本人（同名）的银行账户向本账户转账入金"——**同名入金是平台规则，非 OpenPayd 强制**（OpenPayd 只负责收款与通知，同名判定在平台，见 M3） | 原型 03：`amDepLead`；用户指定业务规则（2026-09-05） |

### M3 入金到账与同名核验（核心承诺）

| ID | 需求 | 验收要点 | 对齐 |
| --- | --- | --- | --- |
| M3-1 | 到账通知 | 用户从外部银行向收款账户转账后，OpenPayd 收款并向平台推送 Pay In 到账通知（生产 webhook；沙箱以 `POST /webhooks/payin/{accountId}` 模拟），通知携带 senderName / senderIban / senderBic / senderAccountNumber / transactionReference 等（字段集依据沙箱 simulate 请求体与 `GET /transactions/payin/{id}` 详情） | spec：POST /webhooks/payin/{accountId}（Simulate Pay In Complete Webhook）；GET /transactions/payin/{id}；❓ F9：生产 Pay In webhook 推送的完整字段以 OpenPayd 实际配置为准 |
| M3-2 | 到账归属匹配 | 平台凭收款账户 + 金额 / `transactionReference`（= 用户在转账附言填的 `payInReference`）把到账归属到具体法币账户；匹配成功进入同名核验，匹配异常（Reference 缺失 / 不匹配）标记待人工（与 M2-4 呼应，延迟入账） | 原型 03：`page-sub`"入金到账自动匹配并计入余额"；流水 payin 示例（ref = YASBE-GBP-2194 等） |
| M3-3 | **同名入金核验（平台规则）** | 平台比对到账通知中的 senderName（打款人户名）与收款账户户主（= 主体实名，个人全名 / 企业注册名）是否**同名**：一致 → 正常入账（平台余额 +N，流水 payin completed）；**不一致（非同名 / 第三方代付 / 错付）→ 不默认入账，进入处置流程（M3-5）**。OpenPayd 本身不校验 sender 与户主同名，此规则为平台强制 | 用户指定业务规则（2026-09-05）；原型：`amDepLead` + 交易记录口径；判定口径（大小写 / 空格 / 企业后缀等）❓ F2 |
| M3-4 | 入账口径 | 入账增加平台余额（可用）；流水类型 payin、状态 completed、fee 为 0（入金无平台手续费，费率另见费率表） | 原型 03：TX payin 示例（fee:0） |
| M3-5 | **非同名入金处置与退款** | 非同名 / 无法判定同名的入金：先**挂账（不入可用余额）并提示用户**，由平台运营人工核实来源；核实为错付 / 第三方代付的，平台发起**原路退回（退款）**。⚠️ **退款的具体执行机制 OpenPayd 尚未确认**（spec 无 Payout 退款 / 冲正端点；`direct-debit/reverse` 与出金无关），候选路径见 §12 F1，需研发与 OpenPayd 确认后定稿 | ❓ F1（核心未决）：退款动作由谁触发、走 OpenPayd 哪个能力（候选：A 反向 bank-payout；B OpenPayd 运营人工原路退回；C 冻结挂账等待官方退款能力）；本 PRD 不定稿为 OpenPayd 已支持 |
| M3-6 | 非同名资金不被误用 | 挂账资金不计入可用余额、不可用于出金 / 兑换；流水 / 提示清晰可解释（用户可见的处置状态） | 与 M3-5 同源；原型当前未实现挂账 UI，❓ F1 结论后补 |

### M4 外部同名账户（EA）创建 = 新建 Beneficiaries + bank Beneficiaries

> EA 是用户出金收款目的地。**产品语义**：EA 必须是主体同名账户（个人本人 / 企业公司名），持有人字段由系统锁定。**OpenPayd 语义**：EA 落库 = 两层对象——① Parent Beneficiary（收款人档案，tag=SELF）；② 其下的 Bank Beneficiary（银行收款账户，承载收款账号信息与出金目的地 id）。**OpenPayd 不校验"同名"**（tag=SELF 仅为声明式字段），同名由平台在产品层执行。

| ID | 需求 | 验收要点 | 对齐 |
| --- | --- | --- | --- |
| M4-1 | 添加向导 = 两步 | ① 选银行所在地区类型：欧洲（EUR，IBAN，SEPA · SWIFT）/ 英国（GBP，Sort Code + 账号，Faster Payments · CHAPS）；② 填写账户信息 | 原型 03：eaModal step1（eaGrid，EA_TYPES：iban / gb）；文案"添加您本人（同名）名下的银行账户，用于同名入金与出金收款" |
| M4-2 | **持有人字段锁定（同名落点）** | 第 2 步中"账户名称 / 账户持有人"为**只读**，自动取自主体实名（个人：实名全名；企业：注册公司名），用户不可修改——这是"同名"在产品 UI 层的强制表达 | 原型 03：`eaSameOnly`（"仅支持添加您本人（同名）的银行账户。账户名称与持有人由系统自动取自您的实名认证信息，不可修改"）、`eaRoName` / `eaRoHolder` 只读、`eaLocked` |
| M4-3 | 银行信息字段（按地区） | 欧洲：bankName / iban / bic / 受益人地址（街道 / 城市 / 邮编 / 国家）；英国：bankName / sortCode / accountNumber。字段格式校验（IBAN 校验位、BIC 8/11 位等），提交前逐项校验 | 原型 03：EA_TYPE_FIELDS（iban / gb 两组）+ EA_FIELDS + 校验（errIban / errBic 等）｜字段与 OpenPayd Bank Beneficiary 请求字段对应见附录 A4 |
| M4-4 | 提交 = 创建 Beneficiary 两层 | 平台后端依次调用：① `POST /beneficiaries` 创建 Parent Beneficiary——个人：`beneficiaryType=RETAIL` + firstName / lastName + `tag=SELF`；企业：`beneficiaryType=CORPORATE` + companyName + `tag=SELF`；`friendlyName` = 用户自定义账户名。② `POST /beneficiaries/{parentBeneficiaryId}/bank-beneficiaries` 创建 Bank Beneficiary——`bankAccountCurrency` / `bankAccountCountry` / `beneficiaryType`（RETAIL / CORPORATE）/ `beneficiaryCountry` / `paymentTypes`（欧洲 SEPA / SWIFT；英国 FASTER_PAYMENTS / CHAPS）/ **`bankAccountHolderName` = 主体实名（锁定值）** + iban / bic 或 accountNumber + `bankRoutingCodes`（SORT_CODE） | spec：POST /beneficiaries（required: beneficiaryType, friendlyName）；POST /beneficiaries/{parentBeneficiaryId}/bank-beneficiaries（required: bankAccountCurrency, paymentTypes, beneficiaryType, beneficiaryCountry, bankAccountCountry, bankAccountHolderName）｜原型：`eaAdded` 文案"已创建收款人档案与银行收款账户"、EA 对象携带 beneficiaryId + bankBeneficiaryId |
| M4-5 | 提交前通道 / 参数校验（建议） | 创建前可调 `POST /beneficiaries/validate` 校验（币种 / 国家 / 支付类型组合）是否合法，避免创建后无法用于对应支付类型 | spec：POST /beneficiaries/validate → beneficiaryValidationResultSet[{paymentType, valid, messages}]｜❓ F10：是否在每次创建前强制调用，研发判断（建议必调，失败则拦截） |
| M4-6 | **同名核验（pending → verified）** | EA 创建后进入持有人核验：**核验通过前不可用于出金**（出金列表置灰 / 提示"核验中 · 通过前不可用"）。英国（FPS 通道，sortCode + accountNumber）可调 `POST /beneficiaries/verify`（Confirmation of Payee）→ status = MATCH 即通过；欧洲 IBAN 账户无 CoP 类端点 → 平台规则核验（❓ F3）。原型演示：创建后 toast "持有人核验进行中…核验通过后方可用于出金"，约数秒后自动 verified（演示简化，生产由真实核验结果驱动） | spec：POST /beneficiaries/verify（required: accountNumber, sortCode, beneficiaryType, bankAccountHolderName）｜原型：`eaVerifyNote` / verified chip / `eaVerified`；❓ F3 / F4 |
| M4-7 | EA 列表与出金可用性 | EA 卡片展示：地区旗标 / 名称 / 持有人（+ 企业同名 chip，企业主体）/ 银行名 / 币种尾号 / 核验状态（已核验 green / 核验中 amber）；仅 verified 的 EA 可被出金选中 | 原型 03：renderEa / renderWdList |
| M4-8 | 核验失败路径 | CoP 返回非 MATCH（如 NO_MATCH）或平台核验不通过：EA 维持不可出金，向用户展示原因与重试 / 删除入口；**不允许强制绕过** | ❓ F4：verify 非 MATCH 状态枚举与 UX 策略，研发 / 产品判断 |

### M5 出金（提现）

| ID | 需求 | 验收要点 | 对齐 |
| --- | --- | --- | --- |
| M5-1 | 入口与前置 | 仅 ACTIVE 法币账户可发起提现；出金引导语按主体动态文案（个人："从所选法币账户提现至您的同名银行账户"；企业："至您企业同名的对公银行账户"） | 原型 03：openWithdraw / wdSubTxt |
| M5-2 | 第 1 步：选择收款 EA | 候选 EA = **币种与法币账户一致 + 主体一致（个人账户只列个人 EA，企业账户只列企业 EA）+ 已核验（verified）**；空态提示先添加（"暂无外部账户，请先添加您的同名银行账户" / 企业对应文案）；可就地从出金跳转添加 EA，添加后返回出金流程 | 原型 03：renderWdList（filter currency + eaSubj==accSubj + verified）；`wdNoEa` / `wdNoEaBiz`；wdAddBtn / fromWithdraw |
| M5-3 | 第 2 步：金额与附言 | 提现金额 ≤ 可用余额且 > 0；附言（Reference）必填（将显示在收款银行对账单，建议填发票号 / 订单号）；展示：提现账户 / 收款账户（EA）/ **Bank Beneficiary id** / 可用余额 / 预估手续费 / 预计到账金额（= 金额 − 手续费）/ 预计到账时效 | 原型 03：renderWdSum / updateWdFee；spec：payout 的 reference 必填（"will appear on the beneficiary bank statement"） |
| M5-4 | 手续费与到账 | 预估手续费 = max(固定费, 金额 × 0.5%)，EUR / GBP 固定费 1.0（平台费率表，❓ 与 OpenPayd 实际费用结构核对后以费率表为准）；预计到账时效按出金通道（欧洲 IBAN → SEPA；英国 → Faster Payments） | 原型 03：wdFeeFor / RAILS[rail].arrive；❓ F5 出金 rails 本期限定 SEPA / FPS 之外是否开放 CHAPS / SWIFT |
| M5-5 | 提交 = OpenPayd Create Payout | 平台后端调 `POST /transactions/bank-payouts`：`accountId`（法币账户 id）、`beneficiaryId`（所选 EA 的 **bankBeneficiaryId**）、`amount{currency, value}`（币种 = 账户币种）、`reference`（附言）；`paymentType` 按 EA 类型（欧洲 SEPA / 英国 FASTER_PAYMENTS）——spec 中 paymentType 非必填，❓ F5 确认是否显式传参 | spec：POST /transactions/bank-payouts（required: accountId, beneficiaryId, amount, reference）|
| M5-6 | 扣减与流水 | 提交成功即扣减平台余额（available / actual），生成流水：类型 payout、状态 processing、金额、手续费、附言；提示"提现申请已提交" | 原型 03：confirmWithdraw（TX.unshift + toast wdSuccess） |
| M5-7 | 状态推进（对齐 OpenPayd 状态机） | payout 状态机：INITIATED → PROCESSING → RELEASED → COMPLETED / FAILED（原型注释对齐 OpenPayd；spec 的 status 仅有示例值 `INITIATED`、无完整 enum → 以 OpenPayd 实际返回为准，❓ F6 确认完整状态集与中文映射：已提交 / 处理中 / 已汇出 / 已完成 / 失败）。原型演示：提交 → 处理中 → 5 秒后自动 COMPLETED（"提现已到账"） | 原型 03：st_initiated / st_processing / st_released / st_completed / st_failed；TX processing→completed 定时推进 |
| M5-8 | 失败与回滚 | payout FAILED：余额回滚（可用 / 实际 + 金额），流水状态 failed，用户可重试；原型 `dWdFail` 演示"PROCESSING → FAILED + 资金已退回"（评审工具）。生产由 OpenPayd 状态 / webhook 驱动回滚，❓ 失败资金是否由 OpenPayd 自动退回原账户、平台如何对账（与 F1 同源，需 OpenPayd 确认） | 原型 03：dWdFail / failLatestWithdraw；❓ F1 / F11 |
| M5-9 | 币种一致性拦截 | 目标 EA 与法币账户币种不一致时不提供选择，提示"币种不一致，暂不支持提现，请添加对应币种的同名账户" | 原型 03：`wdMismatch`（筛选已保证，作为兜底文案） |

### M6 交易记录与账户生命周期

| ID | 需求 | 验收要点 | 对齐 |
| --- | --- | --- | --- |
| M6-1 | 交易列表 | 全部 / 入金（payin）/ 提现（payout）/ 兑换（exchange 预留）筛选；每行：类型、账户（容错：账户被重置删除时显示原账户标识兜底）、金额、手续费、状态、时间、附言 | 原型 03：renderTx（含账户缺失兜底修复 2026-09-05） |
| M6-2 | 交易状态与类型词表 | 状态：已提交（INITIATED）/ 处理中（PROCESSING）/ 已汇出（RELEASED）/ 已完成（COMPLETED）/ 失败（FAILED）；类型：入金 / 提现 / 兑换 / 手续费（词表预留） | 原型 03：st_* / ty_*（zh + en）；❓ F6 完整状态集确认 |
| M6-3 | 账户生命周期展示 | 账户状态：ACTIVE（正常，可收款 / 提现）/ PENDING（开通中，收款信息未生效）/ SUSPENDED（已冻结）/ CLOSED（已关闭）/ FAILED（开户失败）；PENDING / 非 ACTIVE 账户禁用收款与提现操作 | 原型 03：statusChip / accCard；spec：POST /accounts → status PENDING 示例（其余状态为展示预留，❓ 以 OpenPayd 实际状态枚举为准） |

### M7 演示面板（评审工具）

> 演示控制面板用于把 OpenPayd 的**异步状态推进**在评审 / 演示中可视化，**不是**最终前端功能；上线替换为真实 API + webhook 驱动。

| 按钮 | 作用 | 说明 |
| --- | --- | --- |
| `dOpen` | 打开「开通新账户」向导 | M1 |
| `dActivate` | 激活最新账户 PENDING → ACTIVE | 模拟 OpenPayd 账户激活（M1-4） |
| `dDeposit` | 打开「收款账户信息」（欧元） | M2 打款说明书 |
| `dWithdraw` | 打开「提现」（英镑） | M5 |
| `dWdFail` | 模拟提现失败（PROCESSING → FAILED，资金回滚） | M5-8 |
| `dEa` | 打开「添加外部同名账户」 | M4 |
| `dBiz` | 企业演示：创建 ABC LTD 公司账户（GBP £5,000 + 对公收款账户 + 企业 EA） | 注入企业主体数据（M0） |
| `dReset` | 重置演示数据 | 回到种子状态 |
| `dSubject` | 当前用户主体（个人 / 企业），决定所有弹窗默认字段 | M0-1（2026-09-05 全局主体重构） |

---

## 7. 状态与枚举汇总（实现模型参考）

**法币账户（OpenPayd Account）**
`创建(POST 201 → PENDING)` → `ACTIVE（收款信息生效，可收款 / 出金）`；展示预留：SUSPENDED（已冻结）/ CLOSED（已关闭）/ FAILED（开户失败）。状态来源：OpenPayd（spec 示例 PENDING / ACTIVE；其余 ❓ F12 以 OpenPayd 实际枚举为准）。

**外部同名账户 EA（平台业务态）**
`添加（= Beneficiary + Bank Beneficiary 创建成功）→ 核验中（pending）→ 已核验（verified）`（仅 verified 可作出金收款）。
- 英国：CoP `POST /beneficiaries/verify` → status=MATCH（spec 示例值）→ verified；非 MATCH → 不可出金（❓ F4）。
- 欧洲 IBAN：无 CoP → 平台规则核验（❓ F3）。
- verified 是**平台业务状态**（OpenPayd 的 Bank Beneficiary 对象本身无"核验中/已核验"状态字段；对应关系见附录 B）。

**交易（流水）**
- payin（入金）：`到账通知 → 同名核验通过 → 入账（completed）`；`同名核验失败 → 挂账待处置（❓ F1，退款）`。
- payout（提现）：`INITIATED（已提交）→ PROCESSING（处理中）→ RELEASED（已汇出）→ COMPLETED（已完成）/ FAILED（失败，余额回滚）`（原型注释对齐 OpenPayd；spec status 无完整 enum，❓ F6 确认）。

**支付类型（Payment Type / Rail）**
- 收款（Payment Account 可接收）：GBP → Faster Payments / CHAPS / SWIFT；EUR → SEPA / SEPA Instant / SWIFT。
- 出金（本期）：欧洲 IBAN → SEPA；英国 → Faster Payments；CHAPS / SWIFT 出金是否开放 ❓ F5。
- 与 OpenPayd Supported Payment Types 的对齐在创建 EA 时可用 `POST /beneficiaries/validate` 校验（M4-5）。

**主体词映射（原型 ↔ OpenPayd）**
| 产品 / 原型 | OpenPayd（beneficiaryType） |
| --- | --- |
| 个人 INDIVIDUAL | RETAIL |
| 企业 BUSINESS | CORPORATE |

**同名核验状态（CoP verify）**
`status` spec 示例值：MATCH；完整枚举（PARTIAL_MATCH / NO_MATCH / UNKNOWN 等）spec 未枚举 → ❓ F4，以 OpenPayd 实际返回为准。

---

## 8. 异常与边界场景

| 场景 | 期望行为 |
| --- | --- |
| 不可服务国别填写 | 开户第 2 步即拦截，给出国家不可服务原因，不可继续（M0-2） |
| **非同名入金（第三方代付 / 错付）** | 不默认入账：挂账（不计可用余额）+ 提示 + 运营人工核实 → 原路退回（退款）；**退款执行机制 OpenPayd 未确认（❓ F1）** |
| 入金未填 / 填错 Reference | 归属匹配异常 → 延迟入账 / 人工匹配（M3-2，与 M2-4 一致） |
| 入金户名近似（大小写 / 空格 / 公司后缀） | 同名判定口径统一（❓ F2 定规则），无法判定走人工 |
| 账户 PENDING 尝试收款 | 无 rails 收款字段、无操作按钮（M1-3） |
| EA 未核验（核验中）选作出金目标 | 列表置灰不可选，提示"核验中 · 通过前不可用"（M4-6 / M5-2） |
| CoP 核验 NO_MATCH / 非 MATCH | EA 维持不可出金，展示原因与重试 / 删除入口，不可绕过（M4-8 / ❓ F4） |
| 出金 EA 币种 ≠ 法币账户币种 | 不提供选择，提示添加对应币种同名账户（M5-9） |
| 出金 EA 主体 ≠ 法币账户主体 | 企业账户不列个人 EA（反之亦然），须添加同主体对公 / 个人 EA（M5-2） |
| 提现金额 > 可用余额 / 金额 ≤ 0 / 附言为空 | 提交按钮禁用（M5-3） |
| payout FAILED | 余额回滚 + 流水 failed + 可重试（M5-8）；生产回滚 / 对账机制 ❓ F11 |
| EA 或账户在历史流水后被删除 / 重置 | 流水行账户栏兜底显示原账户标识，不崩溃（原型 renderTx 兜底修复） |
| 企业主体无任何 EA | 出金空态文案引导添加对公账户（wdNoEaBiz） |
| 从出金跳转添加 EA 后取消 | 返回出金流程原状态（fromWithdraw 恢复） |

---

## 9. 非功能需求
- **i18n**：zh / en 双语文案，键值双语字典齐全、切换即时生效（沿用 `data-i18n` + `t()` 机制；本 PRD 涉及文案均已给双语或在原型字典中）。
- **安全**：OpenPayd API Key / 敏感凭据只存在于服务端，绝不出现在前端 / 仓库；浏览器侧仅经平台后端代理调用 OpenPayd。webhook 需签名校验（❓ F13：OpenPayd webhook 签名机制确认后落地）。
- **幂等与重试**：开户、创建 Beneficiary / Bank Beneficiary、出金等指令需幂等处理，防重复创建 / 重复扣减；`POST /accounts` 支持 `endToEndReference`（对账 / 关联用），出金幂等键策略 ❓ 研发确认。
- **审计**：主体建档、开户、EA 创建 / 核验、出入金事件与状态流转可追溯；OpenPayd 返回的 `id` / `shortId` / `transactionId` 与平台流水一一对应留存。
- **合规留存**：KYB 建档资料、同名核验依据（senderName 比对 / CoP 结果）、非同名入金处置记录留存可查。
- **性能 / 可用性**：列表与详情感知流畅；OpenPayd 异步状态（账户激活、payout 推进、payin 通知）以轮询 / webhook 更新，不阻塞 UI。

---

## 10. 埋点 / 可观测（建议）
开户 PENDING→ACTIVE 时长；入金到账 → 上账时长与失败归因；同名核验通过 / 失败率（入金 + EA 两侧）；非同名入金笔数 / 金额 / 处置结果；EA 核验 pending→verified 时长与失败率；出金成功率 / 失败原因分布；退款需求笔数（❓ F1 落地后）。

---

## 11. 与原型 / 演示的对应

| 原型文件 | 页面 / 区域 | 覆盖 |
| --- | --- | --- |
| `03-法币账户-欧元英镑-多渠道多账户.html` | 账户列表 + 开通向导 + 收款账户信息弹窗 + 提现弹窗 + 外部同名账户区 + 交易记录 + 演示控制 | M0–M7 主体 |

演示面板（`demoPanel`）为评审工具，对应 §6 M7：`dOpen` / `dActivate` / `dDeposit` / `dWithdraw` / `dWdFail` / `dEa` / `dBiz` / `dReset` / `dSubject`（当前用户主体，全局驱动弹窗默认字段）。
生产实现替换关系：`dActivate` → `GET /accounts/{id}` 轮询 / OpenPayd 通知；出金 processing→completed 自动推进 → OpenPayd payout 状态 / webhook；EA 添加后自动核验通过 → `POST /beneficiaries/verify`（英国 CoP）/ 平台核验（欧洲）；非同名入金与退款 → ❓ F1 结论后的真实处置流。

---

## 12. 未决问题 / 评审待拍板（Open Forks）

| # | 问题 | 现状 / 张力 | 建议评审结论方向 |
| --- | --- | --- | --- |
| F1 | **非同名入金退款机制（核心）** | OpenPayd **未确认**退款能力：spec 无 Payout 退款 / 冲正端点（`direct-debit/reverse` 仅针对 direct debit，与出金无关）。非同名入金必须退款，但"谁来退、怎么退"未定 | 候选：A 平台发起**反向 bank-payout**（原路退回，需同名银行收款支持）；B 提交 OpenPayd 运营**人工原路退回**；C 先**冻结挂账**，等 OpenPayd 官方退款能力 / 与 OpenPayd 确认后启用。建议：研发与 OpenPayd 商务 / 技术支持确认后定稿；结论落地前按 C 处置 |
| F2 | 同名入金判定口径 | senderName（到账通知）vs 户主实名比对的**规范化规则**未定：大小写 / 空格 / 企业后缀（Ltd / Inc）/ 拼音变体 | 建议：大小写不敏感 + 去空格；企业后缀差异走人工；无法自动判定一律人工（产品 + 合规拍板后定稿） |
| F3 | 欧洲 EA 同名核验手段 | CoP（`POST /beneficiaries/verify`）仅支持英国 sortCode + accountNumber；欧洲 IBAN 账户无对等端点 | 候选：A 声明式（bankAccountHolderName 锁定 = 主体名）+ 首次出金人工复核；B 微额验证（平台能力外，需银行通道支持）；C 引用 KYB 已有银行证明。建议：产品 + 合规拍板 |
| F4 | CoP 非 MATCH 状态与 UX | spec 仅示例 MATCH，完整枚举（PARTIAL_MATCH / NO_MATCH / UNKNOWN…）未在 spec | 研发对接时以 OpenPayd 实际返回为准并回写 PRD；UX：非 MATCH 不通过、可重试 / 删除、可人工（M4-8） |
| F5 | 出金 rails / paymentType 范围 | 原型出金 rail 仅欧洲→SEPA、英国→FPS；CHAPS / SWIFT 出金是否开放；`paymentType` 在 bank-payouts 中非必填，是否显式传参 | 本期维持 SEPA / FPS；CHAPS / SWIFT 出金按需求排期；paymentType 建议显式传参与 OpenPayd 对齐（研发判断） |
| F6 | payout 状态完整集 | 原型注释状态机 INITIATED→PROCESSING→RELEASED→COMPLETED/FAILED，但 spec 的 status 无 enum（示例 INITIATED） | 研发对接 OpenPayd 实际状态集后回写本 PRD（M5-7 / §7） |
| F7 | Account Holder 建档 / KYB 集成 | 开户前置"KYB 建档"在 OpenPayd 侧的真实接口不在本 spec 范围（spec 仅 `/linkedClient`）；EUR 在 UK 平台开户的 `ibanCountry`（MT）规则需确认 | 研发确认 OpenPayd Account Holder / KYB 建档方式（可能走 OpenPayd 门户 / 其他 API）后补 M0-3 / M1-2 |
| F8 | EN 账户自动命名 | 原型英文自动名 "Pound Sterling Account 3" 与中文"英镑收款账户 3"不一致（EN 缺本地化基名） | 对齐命名规则（en 基名 "GBP Account" 或保留 "Pound Sterling Account"），产品拍板后小改原型 |
| F9 | Pay In webhook 生产字段 | 沙箱 simulate 请求体 / payin 详情字段已知，生产 webhook 推送结构未确认 | 研发与 OpenPayd 确认 webhook 配置（URL / 签名 / payload）后回写 M3-1（含 F13 签名） |
| F10 | EA 创建前 validate 是否强制 | `POST /beneficiaries/validate` 可用于校验通道组合；原型未展示该调用 | 建议创建前强制调用，失败即拦截（M4-5） |
| F11 | payout 失败的资金处理 / 对账 | OpenPayd 失败后资金是否自动退回原法币账户、平台如何对账（回滚触发源）未确认 | 与 F1 一并与 OpenPayd 确认；平台侧先按"状态驱动回滚 + 人工对账"设计（M5-8） |
| F12 | 账户 SUSPENDED / CLOSED / FAILED | spec 仅见 PENDING / ACTIVE 示例；其余为展示预留 | 以 OpenPayd 实际状态枚举为准；本期仅展示 + 禁用操作（M6-3） |
| F13 | webhook 安全 | OpenPayd webhook 签名 / 鉴权机制未确认 | 研发确认后落地校验（§9） |

### 已决策记录
| # | 决策 | 结论 | 影响 |
| --- | --- | --- | --- |
| D1 | 全局主体（2026-09-05） | 页面单一"当前主体"（INDIVIDUAL / BUSINESS）由演示控制 `dSubject` 决定，**全局驱动**所有弹窗默认字段（开户字段组 / EA 锁定持有人 / 出金可用 EA / 入金户主）；移除弹窗内个人 / 企业选择项 | 原型 03 已重构（M0-1）；本 PRD 按此口径书写 |
| D2 | 同名 = 平台强制规则（2026-09-05） | OpenPayd 不要求同名（仅 tag=SELF 声明）；YASBe 产品层强制：入金来源须同名（到账核验），出金只到同名 EA（持有人字段锁定 + 核验）；非同名入金须退款（机制 ❓ F1） | M2-5 / M3-3 / M3-5 / M4-2 / M4-4 / M5-2；§12 F1–F3 |
| D3 | renderTx 容错（2026-09-05） | 历史流水引用的账户被删除时，流水行显示原账户标识兜底而非崩溃 | M6-1 |

---

## 13. 附录

### 附录 A：OpenPayd 端点字段映射（字段 / 必填 / 说明直接取自 opd_full_spec.json）

#### A1. `POST /accounts` — Create Account（开户，M1-2）
| 请求字段 | 必填 | spec 说明 | 平台用途 |
| --- | --- | --- | --- |
| `currency` | ✅ | 开户币种（ISO 4217），决定账户所有交易的计价币种 | EUR / GBP |
| `friendlyName` | — | 便于识别的标签，仅展示用途 | 用户自定义账户名（M1-2） |
| `accountId` | — | 仅 Multi Currency 账户：关联已有账户，同 IBAN 新币种 | 本期不使用 |
| `ibanCountry` | — | UK 平台开 EUR 账户时须为 `MT`；FR IBAN 另见文档 | ❓ F7 确认 |
| `endToEndReference` | — | 跨系统对账 / 审计关联参考 | 幂等 / 对账（§9） |
响应 201：`id` / `status`（示例 PENDING）/ `actualBalance` / `availableBalance`（{value, currency}）/ `friendlyName` / `master` / `primary` / `accountHolderId` / `transactionCategory` / `supportMccy` / `internalAccountId`。

#### A2. `GET /bank-accounts` — Payment Account Object（收款账户信息，M2-1/M2-2）
| 字段 | spec 示例 | 原型字段 / 用途 |
| --- | --- | --- |
| `currency` | GBP | 币种 |
| `status` | ACTIVE | 账户状态（与 Account 状态联动） |
| `internalAccountId` | GBP12790694918470 | 内部账户号（展示尾号依据） |
| `bankCountry` / `bankAddress` | GB / 133 Houndsditch… | 银行地址（f_bankAddress） |
| `iban` / `bic` | GB59CLRB… / CLRBGB22 | IBAN / SWIFT·BIC（EUR / SEPA 通道展示） |
| `accountNumber` | 11326194 | 账户号码（GBP 通道展示） |
| `bankName` | Clear Bank | 收款银行（f_bankName） |
| `bankAccountHolderName` | Company Name | **账户持有人名称（= 主体实名，同名核验基准，f_holder）** |
| `provider` | CLEARBANK | 服务行（不展示） |
| `paymentType` / `domestic` | — | 通道归属元数据（平台按 rails 展示） |
| `routingCodeEntries[]` | {routingCodeKey: SORT_CODE, routingCodeValue: 040510} | Sort Code（GBP 通道展示） |
| `payInReference` | A11638158-1PPWYKP020 | 附言 Reference（f_payInRef，入账匹配，M2-4/M3-2） |

#### A3. `POST /beneficiaries` — Create Beneficiary（收款人档案 = EA 第一层，M4-4）
| 请求字段 | 必填 | spec 说明 | 平台取值 |
| --- | --- | --- | --- |
| `beneficiaryType` | ✅ | RETAIL（个人）/ CORPORATE（企业），决定附加字段 | 主体映射：个人→RETAIL；企业→CORPORATE |
| `friendlyName` | ✅ | 便于识别的标签 | 用户自定义账户名 |
| `companyName` | CORPORATE 时必填 | 公司注册法定名，须与注册文件一致 | 企业主体实名 |
| `firstName` / `lastName` | RETAIL 时必填 | 个人名 / 姓 | 个人主体实名拆分 |
| `title` | — | 个人称谓（Mr./Ms. 等，展示用途） | 不采集（可不传） |
| `tag` | — | SELF（本人）/ THIRD_PARTY（他人 / 机构） | **恒为 SELF**（同名语义，D2） |
响应 200：`id` / `beneficiaryType` / `tag` / `accountHolderId` / `title` / `firstName` / `lastName` / `friendlyName`。

#### A4. `POST /beneficiaries/{parentBeneficiaryId}/bank-beneficiaries` — Create Bank Beneficiary（银行收款账户 = EA 第二层，M4-4）
必填 6 项 + 常用可选：
| 请求字段 | 必填 | 平台取值（原型字段） |
| --- | --- | --- |
| `bankAccountCurrency` | ✅ | 币种：EUR（欧洲）/ GBP（英国） |
| `paymentTypes` | ✅ | 欧洲：[SEPA, SWIFT]；英国：[FASTER_PAYMENTS, CHAPS] |
| `beneficiaryType` | ✅ | 同 A3（主体映射） |
| `beneficiaryCountry` | ✅ | 受益人居住 / 注册国（欧洲 EA 的受益人地址国家） |
| `bankAccountCountry` | ✅ | 账户所在国（欧洲区域 / GB） |
| `bankAccountHolderName` | ✅ | **= 主体实名（锁定值，不可改；同名落点，M4-2）** |
| `accountNumber` / `iban` / `bic` | 按通道 | 英国：accountNumber + `bankRoutingCodes`（SORT_CODE）；欧洲：iban + bic |
| `bankRoutingCodes[]` | — | {routingCodeKey: SORT_CODE, routingCodeValue}（英国） |
| `bankName` / `bankAddress` / `bankState` / `bankCity` / `bankPostalCode` | — | 银行名称 / 地址（原型填 bankName；地址字段可选） |
| `beneficiaryFirstName` / `beneficiaryLastName` / `beneficiaryBirthDate` / `beneficiaryAddressLine` / `beneficiaryCity` / `beneficiaryPostalCode` / `beneficiaryState` | RETAIL 时按需 | 个人受益人信息（原型 EA 地址组 addrStreet / addrCity / addrPostal / addrCountry） |
| `companyName` | CORPORATE 时 | 企业 EA 公司名（= 主体实名） |
| `friendlyName` / `taxId` / `phoneNumber` / `metadata` / 中间行字段（intermediary*） | — | 按需（本期不用） |
响应 200：`id`（= Bank Beneficiary id，出金 `beneficiaryId` 取值；原型 `bankBeneficiaryId`）。

#### A5. `POST /beneficiaries/verify` — CoP 核验（英国 EA，M4-6）
请求（必填）：`accountNumber`、`sortCode`、`beneficiaryType`（CORPORATE / RETAIL）、`bankAccountHolderName`（企业=公司名 / 个人=first+last name）；可选：`verificationReference`。
响应：`providerRegistrationId` / `status`（示例 MATCH，完整枚举 ❓ F4）/ `bankAccountHolderName` / `bankName`。
平台用途：英国 EA 创建后核验持有人是否同名且账户真实；MATCH → verified。

#### A6. `POST /beneficiaries/validate` — 创建前校验（M4-5，❓ F10）
请求必填：`bankAccountCurrency`、`bankAccountCountry`、`beneficiaryType`；可选：`paymentTypes`（空 = 全部）。
响应：`beneficiaryValidationResultSet[]`：{paymentType, valid, messages}。

#### A7. `POST /transactions/bank-payouts` — Create Payout（出金，M5-5）
| 请求字段 | 必填 | spec 说明 | 平台取值 |
| --- | --- | --- | --- |
| `accountId` | ✅ | 出金来源账户 id | 法币账户 id |
| `beneficiaryId` | ✅ | 收款 Bank Beneficiary 的 id（UUID） | 所选 EA 的 bankBeneficiaryId |
| `amount` | ✅ | {currency, value} | {账户币种, 提现金额} |
| `reference` | ✅ | 显示在收款方银行对账单的附言 | 用户填写的附言（M5-3） |
| `paymentType` | — | 收款方将收到的支付类型 | 按 EA 类型：SEPA / FASTER_PAYMENTS（❓ F5） |
| `paymentDate` | — | 未来执行日 YYYY-MM-DD | 本期不使用 |
| `reasonCode` / `purposeCode` | 按支付类型 | payout reason / purpose code | ❓ 按 OpenPayd 对所选 paymentType 的要求（研发确认） |
响应：`id` / `shortId` / `status`（示例 INITIATED）/ `type`（PAYOUT）/ `paymentType` / `sourceInfo` / `destinationInfo` / `amount` / `fee` / `runningBalance` / `transactionId` 等（状态推进 ❓ F6）。

#### A8. 交易查询与 Payin 详情
- `GET /transactions`（列表，分页 {content, pageable}）；`GET /transactions/{id}`：`transactionId` / `shortId` / `reference` / `paymentType` / `amount` / `status` 等。
- `GET /transactions/payin/{id}`（Payin 详情，M3-1 同名核验数据源）：`transactionId` / `senderBic` / `senderIban` / `senderName` / `senderAddress` / `senderInformation` / `paymentType` / `amount` / `transactionReference` / `senderAccountNumber` / `routingCodeEntries`。

#### A9. Pay In 到账通知（M3-1，❓ F9）
- 沙箱模拟：`POST /webhooks/payin/{accountId}`，请求体：`senderName` / `senderIban` / `senderBic` / `senderAddress` / `senderInformation` / `transactionReference`（均必填）。
- 生产：OpenPayd 向平台推送 Pay In webhook（payload 结构以 OpenPayd 实际配置为准，❓ F9 / F13）。

### 附录 B：原型 ↔ OpenPayd 词表
| 原型（产品） | OpenPayd |
| --- | --- |
| 主体 INDIVIDUAL / BUSINESS | beneficiaryType RETAIL / CORPORATE（§7 词表） |
| 外部同名账户 EA（id） | Beneficiary（parent，tag=SELF）+ Bank Beneficiary 两层 |
| EA 的 `bankBeneficiaryId` | Bank Beneficiary `id`（出金 `beneficiaryId`） |
| EA `verified`（平台业务态） | 英国：CoP status=MATCH；欧洲：平台核验结果（❓ F3）；OpenPayd 对象无该字段 |
| 收款账户信息（acc.bank 字段） | Payment Account Object（附录 A2） |
| `payInRef`（附言 Reference） | `payInReference`（收款账户）/ `transactionReference`（payin 附言） |
| rail（SEPA / SEPA_INSTANT / SWIFT / FPS / CHAPS） | Payment Type（FASTER_PAYMENTS 等）；本期出金 SEPA / FASTER_PAYMENTS |
| 入金 / 提现（payin / payout） | Pay In（webhook + `/transactions/payin/{id}`）/ Payout（`bank-payouts`） |
| 账户状态 ACTIVE / PENDING / SUSPENDED / CLOSED / FAILED | OpenPayd Account 状态（❓ F12 确认枚举） |
| 提现手续费 wdFeeFor = max(1.0, 0.5%×金额) | 平台费率表（❓ M5-4 与 OpenPayd 费用核对） |

### 附录 C：演示面板 ↔ 需求映射
见 §6 M7 表；生产替换关系见 §11。

---
*本 PRD v0.1 为 Draft；待产品 + 研发逐句评审后升 v0.2。所有 ❓ 项结论将回写本文档对应条目。*



