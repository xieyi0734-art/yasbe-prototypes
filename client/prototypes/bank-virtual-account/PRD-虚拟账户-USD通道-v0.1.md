# PRD — YASBe 法币虚拟账户（Bridge USD 通道）

| 项 | 内容 |
| --- | --- |
| 产品 | YASBe · 用户美元（法币）入金通道 |
| 底层 | Bridge.xyz（Customers / Endorsement / Virtual Account / Wallet / External Account） |
| 本文档状态 | Draft v0.8，待需求评审（v0.8 修订：**全量审计修订**——PRD ↔ Bridge OpenAPI 逐字段机器核对，修正常量 / 枚举 / 状态词 / 出处类不一致 **20 处**，清单见 §13.0 修订记录。v0.7 修订：S1–S3 判定范围拍板 D13——只在 EEA / 风险 / 标注客户内判定、**不做常显**） |
| 日期 | 2026-09-20（v0.1：2026-09-04） |
| 对齐原型 | `01-用户开通虚拟账户.html`（实名 + 开户门禁）、`02-法币账户-多渠道多账户.html`（四步开户向导：① 选币种 → ② 签署服务条款 → ③ 填写账户信息 → ④ 确认开通；账户/入金/归集/出金/流水） |
| 合规基准 | **以 Bridge 在线 API 文档为准**（apidocs.bridge.xyz），本地留存文档仅作参考 |
| 字段权威来源 | 附录 A–G 字段表逐字取自 Bridge OpenAPI（`latest.json`，2026-09-20 拉取，100 paths）；实现前须按后端锁定的 spec 版本复核 |

---

## 1. 背景与目标

### 1.1 背景
YASBe 通过 Bridge.xyz 为用户提供一条**美元法币入金通道**：平台为用户开立 Bridge 客户与法币虚拟账户（Virtual Account，收款专用），用户从**本人同名的外部银行账户**入金；到账后平台让 Bridge 把 VA 内法币**归集到平台官方托管钱包**（兑换为稳定币 USDC / 网络 Base），平台在自有账本上为用户**增加可用余额**；出金时用户选择/填写**同名外部账户**，平台出金。

> 一句话：**VA 是"收款专用管道"，托管钱包是"资金蓄水池"，平台余额是"用户可支配记账"，出金只走同名外部账户。**

### 1.2 要解决的用户问题
1. 海外/跨境用户难以直接获得美元收款与稳定币出入金通道。
2. 用户希望"像给一个自己的美国银行账户转账一样"完成入金，无个人钱包操作门槛。
3. 用户需要一个可信的托管与合规外壳：资金最终落在平台托管钱包 + 平台记账，用户不接触任何个人钱包地址。

### 1.3 产品目标
- G1 让"同名银行转账 → 美元到账 → 平台余额增加"的路径对普通用户**可理解、可复制、低摩擦**。
- G2 全链路合规可达：实名（KYC）、服务条款签署、base 收款 endorsement、反洗钱筛查、国别准入，均与 Bridge 对齐，**不在平台侧"假装"通过**。
- G3 出金闭环闭环到**同名外部账户**，可解释、可审计、防洗钱/代付。

### 1.4 非目标（本阶段不做）
- 企业客户 / KYB（后续版本）。
- 平台把法币/稳定币直接派发到**任意第三方**钱包地址（资金只进平台托管钱包）。
- 与银行账户体系外的出金（非同名）设计为不可行路径而非默认开放。
- EUR/GBP 通道的合规承诺未经验证前，仅作 UI 占位展示（见 §12 未决）。
- restricted（受限）美国低门槛档位及「提升限额」升档引导——**不做**；美国相关客户一律走标准档完整 KYC（产品决策 2026-09-04）。

---

## 2. 名词与术语

| 术语 | 英文 | 说明 |
| --- | --- | --- |
| 实名认证 | KYC | 个人客户身份核验；本阶段为 individual-first |
| 客户 | Customer | Bridge 客户主体；先建客户，endorsement 通过后才可开 VA |
| base 收款通道 | Endorsement (base/USD) | 允许该客户使用 USD 收款能力的产品级授权；含 requirements / issues / future_requirements |
| 收款账户 / 虚拟账户 | Virtual Account (VA) | Bridge 生成的专属法币收款账号（入金专用） |
| 收款通道 / 资金通道 | Rail | 收款账户的清算通道：USD(base)、EUR(SEPA)、GBP |
| 同名账户 | Same-name account | 户名与本人实名一致的外部银行账户 |
| 外部账户 | External Account | 用户保存的出金目标（同名），按币种/国家/通道核验 |
| 托管钱包 | Custody wallet | YASBe 平台官方 Bridge Wallet（稳定币 USDC / 网络 Base），VA 资金归集终点 |
| 平台余额 | Platform balance | 平台账本上用户可支配金额（入金上账 / 出金扣减） |
| 处理中 | Pending | 资金在途/审核中的状态（上账前、出金中） |
| 归集 | Sweep / Settlement | 平台指令将 VA 法币兑换并转至托管钱包 |

---

## 3. 范围（In / Out of scope）

**In scope**
- 个人用户：国别准入 → 选择币种 → **ToS 托管签署（Bridge 托管页，美元首次开户必签，向导第 2 步）** → 实名（KYC，含 EEA/受控地区差异化）→ 客户创建 → base endorsement 审核 → 开立 VA（多币种、可多账户）。
- VA 收款信息展示与入金（打款说明书），到账时效/限额/附言规则。
- 到账后资金归集（VA → 平台托管钱包）与平台余额上账（pending → 可用）。
- 出金：外部同名账户管理（添加/核验/列表）、出金发起与状态、流水。
- 账户/客户生命周期：审核中（under_review）、已开通（ACTIVE）、被拒（rejected，含理由）、PENDING 复核占位。
- 合规状态呈现：endorsement 状态、资金用途/来源、风控标注（flagged）、未来合规要求（future_requirements）。

**Out of scope**
- 企业 KYB；面向任意钱包地址的自动派发；restricted（受限）美国档位及升档引导（产品决策不做，见 §12）；EUR/GBP 真实可开通性验证；多语言 > zh/en。

---

## 4. 用户与角色

| 角色 | 说明 | 核心诉求 |
| --- | --- | --- |
| 个人用户 | 拥有同名外部银行账户，需要美元/稳定币通道 | 快速完成 KYC→开户；打款不被卡；清楚看得到余额与到账；能安全出金回自己 |
| 平台运营/审核员 | 复核被标注/风险客户、处理被拒重提 | 看清拒绝原因、要求补齐、状态可推进 |
| 平台合规/风控 | 维护国别名单、资金用途策略、同名校验 | 全程可审计、与 Bridge 对齐、未来要求（EEA TIN）可控 |
| 平台技术/Dev | 调 Bridge Customers/VA/Wallet/External/Webhook | 幂等、可重试、密钥不落前端 |

---

## 5. 核心业务流程（主路径）

### 5.1 总览
```
[1  准入] 国别/受控判定(US restricted等)
[2  选币种] 向导① 选择法币账户类型（USD / EUR / GBP；多账户可多次开通）
[3  ToS]   向导② 签署合作机构服务条款（仅美元首次开户）：
           跳转 Bridge 托管 ToS 页 → 用户签署 → redirect_uri 回跳携 signed_agreement_id
[4  KYC]   向导③ 填写账户信息 → 向导④ 确认开通（提交即触发实名核验）
           →(即时/审核)→ approved
[5  客户]  平台 POST /v0/customers（携 signed_agreement_id；直接 API，
           非托管 KYC Link，除 EEA 自拍=Persona 托管）
[6  endorsement] 等待 base(USD) endorsement 审核通过（webhook）
           → requirements 满足 / issues 补齐 / future 生效日提示
[7  开 VA]  开立 USD 收款账户（可多币种 EUR/GBP、可多账户）
[8  入金]   用户从本人同名银行账户 → 向 VA 转账（VA 收款信息=打款说明书）
[9  归集]   到账后平台指令 Bridge：VA 法币 → 兑换 USDC/Base → 平台托管钱包
           到账/归集完成 → 平台余额 +N（pending → 可用）
[10 出金]   用户选择同名外部账户 → 平台余额 -N → Bridge offramp / 法币出金
```

### 5.2 关键不变量
- **先合规后开户**：VA 只能在客户 + base endorsement 均 approved 后开立（第一次开通非即时）。
- **入金只进 VA**：用户不打款给任何个人钱包；VA 收款方户名=本人。
- **资金只进托管**：VA 资金终点=平台官方托管钱包，不派发到用户或第三方地址。
- **出金只到同名**：可出金目标必须与本人实名同名。
- **平台余额 = 记账，不直接等于任何单个 Bridge 账户余额**：需要清晰呈现"处理中/可用"以免用户误读。
- **先签署后建档**：美元首次开户（KYC 未 approved）必须先经 Bridge 托管页取得 `signed_agreement_id`，`POST /v0/customers` 必带该字段；**平台不得以本页勾选代替托管签署**，未取得前向导不得进入下一步。
- **步骤数随通道与客户态变化**：美元首次开户 4 步（含签署步骤）；EUR/GBP（OpenPayd）3 步；KYC 已 approved 的老客户美元开户 3 步（视为已签署过，跳过签署步骤）。

---

## 6. 功能需求（按模块）

> 每条含验收要点；**对齐**列指向 Bridge 文档/原型出处；**演示**列说明原型 demo 对应（原型用 demo 面板模拟真实网关状态）。

### M0 国别准入与账户限制
| ID | 需求 | 验收要点 | 对齐 |
| --- | --- | --- | --- |
| M0-1 | 开户前先判定用户国别可服务性 | 不可服务国家/地区（示例：CN/JPN/DZA/BDI/TUN 等 UNSERVED_CODES）在填写/开户前即拦截并给出明确原因，**不进 KYC 流程** | Bridge country servicability；原型 EA/演示默认 S.country='CHN' 使评审需切国家 |
| M0-2 | 演示/评审默认可服务国家应明确 | 原型默认国家为可服务地区（评审需人工切换，避免误把拦截当 bug） | 原型 02 |
| M0-3 | US 进件档位 | **仅标准档（完整 KYC）**；不做 restricted 低门槛档（无 $10k/笔、$100k/30 日受限额度建模），不设「提升限额」升档引导（决策 2026-09-04）；标准档下 NATIONS.USA 的证件/身份字段与 usNotice 文案需自洽（见 §12 已决策清单） | —（决策已关闭 restricted） |
| M0-4 | **账户数量口径（每人 / 每通道）** | **已决策 D10（2026-09-20）：支持多账户，不设数量上限** —— 同一币种可开多个账户，账户名自动递增（`…收款账户 2` / `… Account 2`）；**用户已开通多个美元账户时，仍可继续申请开通新的美元账户**，开户入口不得因「已有同币种账户」而拦截。**现网依据（2026-09-20 实读）**：C 端 `GET /api/bank/openpayd/accounts` 返回**数组**（支持多账户）；`open-form` 与 `POST /api/bank/openpayd/accounts` 未见唯一性 / 409 / duplicate 语义；Bridge `POST /v0/customers/{customerID}/virtual_accounts` 亦无「每客户仅一个 VA」表述。唯一「一人仅一个有效账户」的约束出现在**卡片 KYC 拒绝原因**（`duplicate`："Only one active account is allowed per person"），与法币账户无关 | 见 §12 已决策记录 D10；原型 02 `defaultAccName()` 保留递增命名 |

### M1 实名认证（KYC，个人）
> 字段全量清单见 **附录 A**（按字段）；**按向导步骤的可见项清单见附录 H**；**画像条件字段（EEA / 高风险 / 标注 / 不可服务）见 M11**。
| ID | 需求 | 验收要点 | 对齐 |
| --- | --- | --- | --- |
| M1-1 | individual-first，平台自采信息直传 Customers API | 平台收集字段→POST /v0/customers，**非**使用托管 KYC Link 全流程 | Customers API 直传（已确认） |
| M1-2 | ToS 托管签署在前 | 勾选/自签不足；须先调 `POST /v0/customers/tos_links` 取得 Bridge 托管 URL，用户在该页签署（新窗外链 + `redirect_uri` 回跳；`postMessage` / `signedAgreementId` **spec 未声明、未证实**）取得 `signed_agreement_id` 再提交客户；存量客户新 ToS 走 `GET /v0/customers/{customerID}/tos_acceptance_link`。**向导落位见 M10，接口与字段见附录 B** | 附录 B / §12 H1 |
| M1-3 | EEA 个体自拍走 Persona 托管 | 直接 API 自拍被拒；EEA 进入 hosted Persona 流程（平台不自行采集人脸） | Bridge EEA 要求；见 §12 fork2 |
| M1-4 | 状态机与门禁 | KYC 状态：未提交 not_submitted → 审核中 under_review → 已通过 approved（被拒见 M1-6）；KYC 未通过时**不能**走到 VA 开通 | 原型 01 KYC gate |
| M1-5 | 高风险画像增强字段 | 命中风险/标注（flagged）时，资金用途/来源等为**必填且系统锁定**（用户不可自行关闭），提交审核 | 原型 02 flagged/risk |
| M1-6 | 被拒与重提 | 建模被拒：展示（可分享的）拒绝原因；`developer_reason` 不直接展示给用户；TIN/证件类填错可即时拒；支持修正后重提 | Bridge rejection_reasons / developer_reason |
| M1-7 | 字段枚举对齐 Bridge | 资金来源/用途/月频/职业等枚举与 Bridge 一致（来源：SOURCE_OF_FUNDS、PURPOSES、expected_monthly 档位等）；职业码建议改从 `GET /lists/occupation_codes` 拉取而非硬编码（P2） | §附录枚举 |
| M1-8 | 地址与身份合规 | 地址 `street_line_1` ≥ 4 字符、**外部账户地址 4–35**（`ExternalAccountAddress.street_line_1` = 4–35、`street_line_2` ≤ 35）、禁 PO Box；美国必须提供 `subdivision`（ISO 3166-2，`Address.state` 1–3 位）；`postal_code` **不在 `Address.required` 内**（描述：*Must be supplied for countries that use postal codes*）→ 实现为按「使用邮编的国家」**条件必填**（国家名单待补）；`country` 一律 ISO 3166-1 **alpha-3** | 附录 A #10 |
| M1-9 | 证件数组与签发国 | `identifying_information[]` 每项：`type`（145 类，含 passport / national_id / drivers_license / 各国税号）、`issuing_country`（alpha-3，**必填**）、`number`（作税号用时必填）、`description`（type=other 时必填）、`expiration`（yyyy-mm-dd）、`image_front`（政府证件必填、税号选填）、`image_back`；多国籍/多证件时**逐条采集签发国**，不可用居住国替代 | 附录 A #27 |
| M1-10 | 文档数组多用途 | `documents[]`：`purposes`（个人 8 类：proof_of_address / proof_of_source_of_funds / proof_of_source_of_wealth / proof_of_tax_identification / proof_of_account_purpose / proof_of_individual_name_change / proof_of_relationship / other）、`file`（base64 data-uri，≥200×200，≤24MB）、`description`（purpose=other 时必填）；原型当前覆盖 `proof_of_address` 单文档 + 情形自动追加的 `proof_of_source_of_funds`（M11-10） | 附录 A #28（待拍板 H6） |
| M1-11 | EEA reliance 时间戳 | EEA in-scope 走 reliance（`TWO_FORMS_OF_ID_RELIANCE`）时需提交 `verified_govid_at` / `verified_selfie_at` / `verified_database_at`（write-only ISO 8601）；原型未建模，须与合规确认采集方（平台 or Persona 托管）与组合规则 | 附录 A #25（待拍板 H5） |
| M1-12 | 自拍字段的平台边界 | `liveness_check_selfies[].image` 仅用于**代 Bridge 采集**（base64 data-uri，≥200×200、≤15MB、jpeg 等）；**EEA in-scope 客户不可用此字段**，必须走 Persona 托管自拍 | 附录 A #26（已落地 02 selfieHost） |
| M1-13 | 平台注入字段（非用户填写） | `type=individual`；`endorsements` **建议显式传 `['base']`**（不传时 Bridge 默认尝试授予 base + sepa，会造成非预期授权）；`client_reference_id`（1–256）用于平台侧关联申请单 | 附录 A #1/#14/#29 |

### M2 客户 → base endorsement 两阶段
| ID | 需求 | 验收要点 | 对齐 |
| --- | --- | --- | --- |
| M2-1 | 分阶段建模 | 建客户 →（等待）base(USD) endorsement approved → 再开 VA；**首次开通非即时**，需呈现进度/状态而非假"秒开" | 两阶段开户（已确认） |
| M2-2 | endorsement 级状态 | 展示 endorsement 状态（开通/审核中/缺失资料/issues）与其 `requirements{missing{all_of}}`；缺失项要给到用户可执行清单 | H7 审计项（已落地 02） |
| M2-3 | future_requirements | 未来生效的新要求需展示生效日（例：EEA TIN 截止 2026-12-31），在生效日前引导补齐 | future_requirements+effective_date（已落地 02） |
| M2-4 | 审核推进 | 复核中客户 VA 可先占位 PENDING，审核通过 → ACTIVE；被拒 → rejected + 原因 | 原型 02 demo dKyc |

### M3 开立虚拟账户（收款账户）
| ID | 需求 | 验收要点 | 对齐 |
| --- | --- | --- | --- |
| M3-1 | 多币种 / 多账户 | USD 主通道；EUR/GBP Tab 存在；**每币种可开多个账户、可设主账户，不设数量上限**（D10）；同币种重复开户允许，账户名自动递增 | 原型 02：`defaultAccName()` |
| M3-2 | 开通向导 | 选币种+收款通道 → 展示收款账户；**到账配置为只读"资金归集（平台托管）"**：稳定币 USDC/网络 Base/地址=平台官方钱包固定，用户不可填写钱包地址 | 平台托管（已落地 02） |
| M3-3 | VA 收款字段完整 | 开户成功后展示：银行名称/地址、户主（本人）、账号、路由/IBAN/BIC/SortCode、附言(payInRef，如通道要求) | 原型 02 accModal |
| M3-4 | 账户状态 | ACTIVE（可收款）/ PENDING（复核占位，不可收款）/ SUSPENDED / CLOSED 的可视化与禁用逻辑（PENDING 不展示 rails 收款字段、不能发起收款） | 原型 02 statusChip |
| M3-5 | 生命周期与创建信息 | 展示账户生命周期（status/holder/createdOn），与"平台余额"解耦 | 原型 02 详情 |
| M3-6 | 归集目标模式（destination） | `destination` 三选一（spec 中 `address` / `bridge_wallet_id` / `prefunded_account_id` **均为选填**、无 `oneOf` 约束；「三选一」为 Bridge 文档散文口径）：`address`（外部钱包地址，本期=平台托管钱包）/ `bridge_wallet_id`（Bridge 钱包）/ `prefunded_account_id`；`currency` 枚举 [usdb, usdc, usdt, pyusd, eurc]，`payment_rail` 枚举 12 链（本期 base）；`blockchain_memo` 仅 memo 链（如 stellar）需要、Base 不需要；**用户不可填任何钱包地址** | 附录 C（待拍板 H7） |
| M3-7 | 开发者费率字段 | `developer_fee_percent`（base-100 百分比；**spec 未声明上下限**，「0–100」为平台约定）与 `fee_config`（需向 Bridge 申请开通，二者**不可同传**）；若启用，须与平台结算与费用说明口径一致；`travel_rule_data` 本业务不适用（用户级资金往来非固定对手方） | 附录 C |

### M4 入金（打款说明书 / Deposit 弹窗）
| ID | 需求 | 验收要点 | 对齐 |
| --- | --- | --- | --- |
| M4-1 | **主体 = VA 收款账户内容** | 入金弹窗主要呈现 VA 收款字段（含户主），供用户照着去自己银行转账 | 2026-09-04 定稿（已落地 02） |
| M4-2 | 同名引导 | 顶部引导"仅从本人（同名）银行账户转账"；不同名打款可能被拒/退回 | 已落地 amDepLead |
| M4-3 | 一键复制 | 收款字段逐项复制 + 全选复制（copiedAll） | 已落地 |
| M4-4 | 时效与限额 | 展示到账时效 arrive / cutoff / limit；费率按通道 | 已落地 |
| M4-5 | 附言规则按通道 | 需要 Reference 的通道（SEPA 等）提示填写，非必填附言的通道**不展示"免附言"说明**（deposit 简化）；详情页保留完整说明 | 2026-09-04 定稿 |
| M4-6 | 不在入金弹窗堆杂项 | 托管归集说明、费用行、endorsement 合规块、未来要求提示**不放入入金弹窗**（避免干扰打款动作）；这些进"详情(view)" | 2026-09-04 定稿（已落地 02） |

### M5 到账归集与平台入账（核心承诺）
| ID | 需求 | 验收要点 | 对齐 |
| --- | --- | --- | --- |
| M5-1 | 入金到账 → 平台余额上账 | 平台识别 VA 到账（matching/附言）→ 触发归集 → 到账入账为处理中(pending) → 归集完成/兑换后转可用(available)；金额、币种、折算口径需在 UI 明示 | 业务流（用户确认） |
| M5-2 | 归集目标唯一 | 归集终点=平台官方托管钱包（USDC/Base `0x71C7…`）；不派发到用户/第三方地址 | 平台托管（已落地 02） |
| M5-3 | 展示口径 | 列表/详情区分"VA 内可用/在途"与"平台可用余额"，避免把 VA 收款账户余额误当可提现余额 | §12 平台账本呈现（未定） |
| M5-4 | 费用 | 入金/兑换/Gas 费等从入账额扣除的规则需产品明示（开发费+兑换费+Gas 示例），且不因入金弹窗移除而丢失可查性 | 原型 02 详情 fee |

### M6 出金到同名外部账户
| ID | 需求 | 验收要点 | 对齐 |
| --- | --- | --- | --- |
| M6-1 | 外部账户=同名账户 | 用户添加外部账户（同名字面提示贯穿：添加外部同名账户）；新增目标需与本人实名同名校验 | 已改名落地（外部同名账户） |
| M6-2 | 添加与核验 | 添加后按币种/国家核验：**US 即时可用**（spec 无 US 校验器）；**EU/UK 走 `match_level` `pending → match / close_match / no_match / error`**（平台「已核验」的定义待拍板）；**仅核验通过者可选作出金目标** | 原型 02（已验证） |
| M6-3 | 出金可用性 | 出金可用金额=平台可用余额；出金发起后状态机清晰（发起→处理中→成功/失败），失败可重试并给出原因 | 原型 02 TX/出金 |
| M6-4 | 出金口径对齐 Bridge | 出金=从平台余额扣减并发起（Bridge offramp：wallet→external_account；FedNow 等 beta）语义需产品拍板（见 §12 M3/I6）；不能让用户以为"VA 内法币可直接转出" | 未决 |
| M6-5 | 限额与同名强约束 | 出金限额、同名核验失败提示；不允许出金到第三方 | §12 同名策略 |
| M6-6 | 外部账户字段与类型 | `account_type` 枚举 [us / iban / gb / clabe / pix / bre_b / co_bank_transfer]；本期：`us`（USD：`account.account_number` + `routing_number` 9 位 + `last_4` + `checking_or_savings`）、`iban`（EUR：`iban.account_number`（spec **无 pattern**；结构 + mod97 校验位为**平台侧规则、由服务端实现**）+ `bic` 8–11 位正则）、`gb`（GBP：`account_number` 8 位 + `sort_code` 6 位）；`account_owner_name`（spec `minLength=1` / `maxLength=256`；description 对 ach / wire / iban 要求 **3–35**）且须与本人实名同名；`address`（`street_line_1` 4–35 / `street_line_2` ≤ 35）：**`us` 类型为 spec 必填**，`iban` / `gb` 请求体中为**选填**（平台仍要求填写，用于受益人地址核验）；顶层 `account_number` / `routing_number` **已弃用**，改用 `account.*` | 附录 D |
| M6-7 | 不可用原因可解释 | `deactivation_reason` 枚举 7 类（deactivated_due_to_bounceback / deleted_by_developer / invalid_account_number / invalid_bank_validation / rejected_by_bank_provider / requested_by_developer / plaid_item_error）+ `deactivation_details`，用于说明"该目标为何不可出金"，不得只显示"不可用" | 附录 D |

### M7 账户与记录
| ID | 需求 | 验收要点 | 对齐 |
| --- | --- | --- | --- |
| M7-1 | 账户卡片 | 每账户显示币种/主账户标识/状态/账户号；PENDING 占位与 ACTIVE 视觉区分 | 原型 02 |
| M7-2 | 资金流水 | 入金(payin)/出金(payout) 双 Tab；单笔含金额、币种、手续费、状态（平台态：completed / processing / rejected / failed；Bridge 侧为 VA 事件 / Transfer 状态，映射待补）、时间 | 原型 02 TX |
| M7-3 | 对账可审计 | 流水与 Bridge 侧（VA settlement、custody 钱包、offramp）能对得上；处理中单需可追溯 | NFR |

### M8 合规状态与运营
| ID | 需求 | 验收要点 | 对齐 |
| --- | --- | --- | --- |
| M8-1 | endorsement 状态面板 | 账户详情展示 base(USD) 通道合规状态与已满足项（实名/ToS/制裁筛查）、审核中说明、未来要求 | H7（已落地 02 详情） |
| M8-2 | 风险/标注 | flagged 客户：资金用途/来源字段锁定必填；审核提示"需配合完整身份与资金用途信息" | 原型 02 |
| M8-3 | 拒绝可解释 | rejected 提供可分享原因；重提入口 kfRetry 可用 | 原型 02（H6） |
| M8-4 | 审核后台 | 运营可推进状态（approve → ACTIVE）；与真实后端角色/审批流对齐（当前用 demo 面板模拟） | §12 后台未定 |

### M9 原型演示面板（评审工具）
> 用于把"真实网关异步状态"在评审/演示中可视化，**不是**最终前端功能；上线应替换为真实 webhook 驱动。
- dKyc：KYC 状态 approved / under_review / not_submitted。
- dRisk / dFlag：风控标注。
- dCountry：国别（默认 CHN 会触发不可服务拦截，评审需切换）。
- dDeposit：入金弹窗。
- dEa / dReset：外部账户与重置演示数据。

### M10 开户向导 · ToS 托管签署步骤（Bridge）
> 本轮（2026-09-20）新增：美元**首次**开户在「选择币种」之后、「填写账户信息」之前增加一个**独立步骤**承载 Bridge 托管 ToS 签署。依据：`POST /v0/customers/tos_links` 明确 "Signing this acceptance flow is a requirement for creating customers"。
| ID | 需求 | 验收要点 | 对齐 |
| --- | --- | --- | --- |
| M10-1 | 步骤位次与步骤数 | 美元首次开户向导 = 4 步：① 选择法币账户类型 → ② **签署合作机构服务条款** → ③ 填写账户信息 → ④ 确认开通；EUR/GBP（OpenPayd）保持 3 步、不出现该步骤；KYC 已 approved 的老客户美元开户为 3 步（跳过签署） | 附录 B |
| M10-2 | 先签署后建档（硬约束） | 未取得 `signed_agreement_id` 时「下一步」禁用并给出明确原因；**不得以本页勾选代替托管签署**；`POST /v0/customers` 必带 `signed_agreement_id` | M1-2 / 附录 B |
| M10-3 | 跳转外部托管页并回跳 | 「前往 Bridge 托管页签署」跳转 Bridge 托管页（生产：新窗或同窗外链；原型：模拟托管页并标注「外部页面」+ 托管 URL + `redirect_uri`）；签署完成经 `redirect_uri` 回跳并携 `signed_agreement_id`（`tos_links` 返回示例 URL 即含 `redirect_uri` 参数）；iFrame + `postMessage` 回传 `signedAgreementId` 在 spec **0 命中**，**未证实**，须与 Bridge 确认后方可采用 | 附录 B |
| M10-4 | 签署态与回执 | 步骤内展示：待签署/已签署状态、服务提供方、条款版本（USD/base 为 **Terms v1**）、协议名称、适用服务；签署后展示签署编号 + 签署时间；确认页展示**只读回执**（不可修改）；签署编号按 §9 留存可审计 | `has_accepted_terms_of_service` |
| M10-5 | 存量客户新版条款 | 存量客户接受新版 ToS 走 `GET /v0/customers/{customerID}/tos_acceptance_link`，在法币账户页提示「需接受新版条款」并跳转；endorsement `requirements.missing` 出现 `tos_v2_acceptance` 时须给出可执行引导 | 附录 B（**本轮原型未做，登记待办**） |
| M10-6 | 异常与取消 | 托管页取消/关闭 = 仍未签署，不得默认通过；签署链接过期或回跳失败 → 重新获取链接并提示重试；重复进入该步骤不得重复建档或覆盖既有签署记录 | §8 |

---

### M11 合规画像判定与增补字段（EEA / 高风险 / 标注 / 不可服务）

> **本轮补充（2026-09-20）**：开户字段**不是固定一套**。同一张「填写账户信息」表单，部分字段只在命中特定客户画像时才出现、或由选填转为必填且锁定。判定轴三条：**地域**（EEA / BBSA in-scope）与**风险**（高风险 / 标注客户）；**资金来源情形**（用户自填字段值命中三种业务情形 → 自动追加材料，见 M11-10 / M11.A）；判定均由平台与渠道侧完成，**用户不可自行开关**（原型复选框 `disabled`）。
>
> **字段依据（逐字取自 Bridge OpenAPI，2026-09-20）**：`account_purpose`、`employment_status`、`expected_monthly_payments_usd`、`acting_as_intermediary`、`most_recent_occupation`、`source_of_funds` 的 description 均含 *"Required for high risk customers"*；`place_of_birth`、`nationalities`、`account_purpose`、`employment_status` 的 description 含 *"EEA / BBSA in-scope ... required"*；**`identifying_information` 的 EEA 要求（国民身份号类 + TIN 类逐条）出自 EEA 政策页 `eea-updated-requirements`，该 schema 在 spec 中无 description**（政策文件 `eea_requirements.rb`）。原型实现见 `02` 的 `needEea()` / `needCond()` / `needMore()`。

| # | 画像 | 判定条件 | 命中后的字段后果 | 原型对应 |
| --- | --- | --- | --- | --- |
| M11-1 | **E1 EEA in-scope（个体）** | 客户与 EEA 相关：**居住国 / 国籍 / 出生地**任一落入名单即 in-scope（Bridge 以 *"EEA / BBSA in-scope"* 表述）。**名单口径（D11，2026-09-20）：EU27 + ISL / NOR / LIE + GBR = 31 国，英国（GBR）计入**；触发维度为三维**任一** | 增补或转必填：`place_of_birth{country, city}`、`nationalities[]`（**全部**国籍，非仅一个）、`account_purpose`、`employment_status`；`identifying_information[]` 须**同时**含「国民身份号类」一条 + 「TIN 类」一条，且 TIN 的 `issuing_country` **须等于居住国** | `eeaFields`（`kfBirthCountry` / `kfBirthCity` / `kfNations` / `kfNatId` / `kfTin`）；原型 02 `needEea()` 三维 + `kfNations` / `kfBirthCountry` 变更重算 |
| M11-2 | **E2 EEA 人脸核验不可自助** | EEA in-scope 个体 | `liveness_check_selfies[].image` **不适用**（Bridge 明文：经该字段提交的自拍不足），**必须走 Persona 托管核验**；页面直接上传自拍的入口须隐藏 | `selfieHost` 显示 + `kfSelfieCell` 隐藏 |
| M11-3 | **E3 EEA reliance 路径** | 走 `TWO_FORMS_OF_ID_RELIANCE` 依赖（不采证件实拍，改用核验时间戳） | 提交 `verified_govid_at` **加**（`verified_selfie_at` **或** `verified_database_at`）二选一组合；企业侧另有 `verified_business_formation_at` / `verified_business_registry_at` / `verified_evidence_of_good_standing_at` / `verified_ownership_at` / `verified_account_authorization_at`（business 非本期范围，登记备查） | 未建模（**H5**） |
| M11-4 | **E4 EEA 按国别的证件类型** | 每国国民身份号 / 税号类型不同（Bridge 按国家表） | 采集项**名称与类型随居住国切换**（FRA=NIR / Numéro fiscal、DEU=National ID / Steuer-ID、ESP=NIE / NIF、ITA=Codice Fiscale、NLD=BSN、ISL=kennitala、NOR=Fødselsnummer …）；未列入的国家回落默认（`national_id` / `tin`） | `EEA_NATID`（D11 已补齐至 **31 国**，含 SVK / LIE / GBR；**其中 SVK / LIE / GBR 的国别类型映射待合规回填**，取值取自 Bridge 证件类型枚举，暂 `national_id` / `tin`、GBR `nino` / `utr`）+ `kfNatIdHint` / `kfTinHint` |
| M11-5 | **R1 高风险客户（渠道判定）** | 渠道判定为 **high risk**（Bridge 仅给出「高风险客户必填」口径，**未公开阈值**） | 下列 **6 个字段**由选填转**必填且系统锁定**（`account_purpose` 选 `other` 时须补 `account_purpose_other`，故实现为 6 + 1 项）：`account_purpose`（+ `account_purpose_other`）、`employment_status`、`expected_monthly_payments_usd`、`acting_as_intermediary`、`most_recent_occupation`（职业码，取值应拉 `GET /lists/occupation_codes`）、`source_of_funds`（+ 资金来源说明） | `kfCondRow`（`kfEmp` / `kfPurpose` / `kfPurposeOther`）+ `kfMore`（`kfOccup` / `kfSof` / `kfMonthly` / `kfInter`）+ `kfMoreCb` 只读勾选 + `riskNotice` |
| M11-6 | **R2 标注客户（flagged）** | 平台 / 合规侧标注 | 同上增补字段；**提交后不秒开**：账户先置「开通中」，连同实名资料进人工复核，复核通过才转「已开通」 | `flagNotice` / `cfNoteReview` / `cfNoteInstant` 二选一 |
| M11-7 | **R3 平台风险信号（管理端现网）** | ComplyAdvantage CA 风险：`customerRiskCode ∈ {HIGH, PROHIBITED}`、或 `screeningResult=HAS_PROFILES`、或 `handlingStatus=PENDING`；或命中用户黑名单 / 邮箱域名黑名单 / 用户暂停（`source=SUSPEND`） | 平台侧处置：**拦截或转人工复核**；开户与入金按风控结论放行 / 拒绝（不表现为字段增补） | 管理端 `/apiAdmin/ca-user-risk/*`、`/apiAdmin/user-blacklist/*`、`/apiAdmin/email-domain-blacklist/*`（2026-09-20 实读）；**原型未建模，登记缺口** |
| M11-8 | **R4 不可服务国家 / 地区** | 居住国 ∈ 不可服务名单（原型 `UNSERVED_CODES` = CHN / JPN / DZA / BDI / TUN；US 走标准档，见 M0-3） | **在字段采集前直接拦截**，不进 KYC 流程（M0-1） | `noSvcNotice` / `isUnserved()` |
| M11-9 | **R5 美国居民证件照核验** | 居住国 = USA（标准档） | 政府证件照核验须走托管核验页（Persona）拍摄并完成人脸自拍，**不可仅提交 SSN 类号码** | `usPhotoHost`（另有 `usNotice`） |
| M11-10 | **S1–S3 三种资金来源情形（系统自动判定 → 自动追加材料）** | **不由人工接入**：平台系统按用户在步骤③**自填的字段值**判定，命中即在该步骤内**自动增加需上传的信息**（用户当场上传）。① `employment_status=unemployed` **且** `source_of_funds=salary`；② `source_of_funds=pension_retirement`；③ `expected_monthly_payments_usd=50000_plus` | 命中情形 → 表单内**自动出现**对应上传项并标必传，未上传不能进入下一步；未命中即不出现、用户无开关可关闭。落点 `documents[]{purposes:[proof_of_source_of_funds], file}` | 原型 02 `kfSofDocs`（`kfSofStatementDoc` / `kfSofSalaryDoc` / `kfSofPensionDoc` / `kfSofProofDoc`）；`sofCases()` / `renderSofDocs()`；细则见 **M11.A** |

> **实现提醒（避免只做显示切换）**：
> - E1 与 R1 **有字段重叠**（`account_purpose` / `employment_status` 两条画像都要求），原型用 `needCond()` = EEA ∪ 高风险 ∪ 标注统一控制这一组条件字段行；渲染前须**按画像分别计算「显示 / 必填 / 只读」**，不能只切 `display`。
> - 条件字段的**默认值**遵循「系统带出、用户可改」：`applyUserCountry()` 会按 `S.country` 自动带出国籍 / 居住国 / 出生国与证件类型提示（M11-4）。
> - **已决策（D12，2026-09-20）**：原型第 3 步的「其他国家/地区税务居民」行（`kfFtrCb` + `kfFtrCountries`）已**移除**——Bridge **individual** payload 无对应字段，该能力位于 business 的 `has_foreign_tax_registration`；个人侧不采集、不展示。如后续需承载境外税务居民，走 `documents[].purposes=proof_of_tax_identification` 或额外 TIN 条目。

#### M11.A 三种资金来源情形 · 自动追加材料（细则，2026-09-20 拍板）

> **口径**：三种情形的处理**不由人工接入**——由平台系统按用户在步骤③**自填的字段值**自动判定，命中即在该步骤内**自动增加需上传的信息**，由用户当场上传。用户无开关可关闭；命中项未上传时「下一步」不可用（与 M11-5 的锁定口径一致）。 **判定范围 ＝ EEA / BBSA in-scope、高风险、标注客户**（见下方「判定依据字段的采集口径」，D13）。

| # | 情形 | 判定条件（用户自填字段值，枚举逐字对齐 Bridge，见附录 E） | 自动追加的上传项（当场上传） | 接口落点 |
| --- | --- | --- | --- | --- |
| S1 | 无业但声明工资来源 | `employment_status = unemployed` **且** `source_of_funds = salary` | ① 资金来源说明 ② 工资入账凭证（近 3 个月银行流水 / 工资单） | `documents[]{purposes:[proof_of_source_of_funds], file}` |
| S2 | 养老金 / 退休金来源 | `source_of_funds = pension_retirement` | 养老金 / 退休金发放证明 | 同上 |
| S3 | 高月均资金往来 | `expected_monthly_payments_usd = 50000_plus` | 资金来源证明（银行流水 / 收入证明） | 同上 |

**判定与呈现规则**
- **判定时序**：在步骤③内**实时**判定——字段值变更即重判；命中立即出现上传项，不再命中立即收起**并清空该项已选文件**。
- **多情形叠加**：可同时命中，材料项**逐项列出**（同一 `purposes` 值可有多条 `documents[]`）；S1 的两项须**分别**上传。
- **必传与拦截**：命中项均为必传；未上传时「下一步」禁用（同 `complianceComplete()` 口径）。
- **文案（面向用户；不含内部实现口径）**：

| 位置 | 中文 | English |
| --- | --- | --- |
| 区块标题 | 资金来源材料 | Source of funds documents |
| 区块说明 | 以下材料由平台按您填写的信息自动判定，须在开户时一并上传。 | The items below are determined automatically from the information you provided and must be uploaded with this application. |
| 判定说明 | 系统判定：因{情形}，您需补充上传以下材料（必填，无法自行关闭） | Required: because of {reason}, please upload the items below (mandatory) |
| 情形 S1 描述 | 就业状态为「无业」且资金来源为「工资」 | employment status "unemployed" with salary as source of funds |
| 情形 S2 描述 | 资金来源为「养老金 / 退休金」 | pension / retirement as source of funds |
| 情形 S3 描述 | 预计每月资金往来为 5 万美元及以上 | expected monthly volume of USD 50,000 or more |
| 上传项 ①a | 资金来源说明 / 请上传说明资金来源的书面说明文件。 | Source of funds statement / Upload a written statement explaining the source of funds. |
| 上传项 ①b | 工资入账凭证 / 近 3 个月银行流水或工资单。 | Salary payment evidence / Bank statements or payslips for the last 3 months. |
| 上传项 ② | 养老金 / 退休金发放证明 / 发放机构出具的证明或近 3 个月入账记录。 | Pension / retirement benefit proof / Issuer letter or 3 months of benefit credits. |
| 上传项 ③ | 资金来源证明 / 银行流水、收入证明等可证明资金来源的材料。 | Proof of source of funds / Bank statements, income proof or other documents showing the source of funds. |
| 未上传提示 | 请上传所需材料 | Please upload the required document |

**口径边界（不可越界）**
- 三个触发器名称（`unemployed_using_salary` / `high_expected_monthly_payments` / `funds_sourced_pension_or_retirement`）在 Bridge OpenAPI 中 **0 命中**，属**渠道内部合规触发器**，**不得写成「接口可读字段」或「接口返回的判定结果」**。
- 情形 S3 的阈值真值是**枚举** `50000_plus`（个人 `expected_monthly_payments_usd` 为 string 四档枚举，**非金额**）；用户文案「5 万美元及以上」须与该枚举一致，**不得引入金额字段**。
- **高风险地区个人 20 万美元档在个人字段中无法表达**：`200000` / `100000` 类阈值在 Bridge spec 中 **0 命中**（**阈值属合规政策口径，非 API 字段**）；个人 `expected_monthly_payments_usd` 为 string 四档枚举，企业同名字段为 **integer** 金额（可表达任意数额）→ 见 §12 **H13**。

**判定依据字段的采集口径（已拍板 2026-09-20，见 §12 D13）**
- **判定范围 ＝ `E1 EEA / BBSA in-scope` ∪ `R1 高风险` ∪ `R2 标注` 客户**，即 `employment_status` / `source_of_funds` / `expected_monthly_payments_usd` 的**现有可见范围**；**不做常显**（不把这 3 项扩到全体开户用户），全量用户的步骤③表单保持精简。
- 为让 **EEA 客户也能被判出情形**，原型把 `source_of_funds` / `expected_monthly_payments_usd` 两项**随条件字段行（`needCond()`）一并展示**：EEA 客户亦可见、亦必填；`employment_status` 沿用原可见范围。三项统一作为「系统判定输入」处理，**不给用户关闭开关**。
- **边界**：非 EEA 且非风险 / 标注的客户**不采集**这 3 项 → **不参与** S1–S3 判定（无判定输入即无命中）。如后续要求覆盖全体开户用户，须先改「常显」——即本决策的**替换条件**。

**演示路径（原型 02）**——① **EEA**：演示面板「用户所在国家 / 地区」选「德国」（或任一 EEA 国）→ 第③步「就业状态」选「无业」（「资金来源」/「预计每月资金往来」随条件字段行一并展示，**EEA 客户亦可见**）→ 情形 S1 命中并出现两项上传位；② **风险 / 标注**：勾「高风险客户」或「标注客户（flag）」→ 同上；③ 再把「预计每月资金往来」选为「50,000 USD 以上」→ 叠加 S3；④ 关闭风险且切回非 EEA 国家 → 材料区收起并清空已选文件。

---


## 7. 状态与枚举汇总（实现模型参考）

**客户 KYC**
**平台态**：`not_submitted → under_review → approved | rejected`（rejected 可修正重提 → under_review）。**Bridge 值**：KYC 流 `KycStatus` = `not_started / incomplete / awaiting_questionnaire / awaiting_ubo / under_review / approved / rejected / paused / offboarded / deposits_restricted`（**无 `not_submitted`**）；直连 Customers API 的客户态取 `Customer.status`（`CustomerStatus`，**通过态 = `active`，无 `approved`**）→ 映射见附录 F
**资金来源情形（M11-10 / M11.A）**：命中 S1–S3 时平台在步骤③内**自动追加材料项**（`documents[].purposes=proof_of_source_of_funds`），命中项未上传不能进入下一步；判定与呈现细则见 M11.A。**判定范围**＝ EEA / BBSA in-scope、高风险、标注客户（即 3 个判定字段的现有可见范围），**不做常显**（D13）。

**ToS（Bridge 托管签署）**
`未签署 → 已签署（signed_agreement_id + 签署时间）`；客户侧布尔字段 `has_accepted_terms_of_service`；endorsement 维度以 `requirements.complete` / `requirements.missing` 中的 `tos_acceptance` / `tos_v2_acceptance` 表达。**平台不得以本页勾选替代托管签署。**

**base endorsement（USD）**
`incomplete/requirements{missing} → approved`（`Endorsement.status` enum = `incomplete / approved / revoked`，**无 `pending`**）；未来要求：`future_requirements + effective_date`（例 EEA TIN 2026-12-31）

**收款账户 VA**
`PENDING(复核占位，不可收款) | ACTIVE(可收款) | SUSPENDED | CLOSED`；VA 建成前置条件：customer + base endorsement 均 approved

**外部账户**
添加 → 核验：**US 无持有人姓名核验、添加即可用**（spec 无 US 校验器）；**EU/UK 走 `AccountVerification.*.match_level`**（enum `pending / match / close_match / no_match / error`）——平台「已核验」对应哪些 `match_level` 值**待拍板**；仅核验通过者可选作出金目标

**流水**
**平台态** payin：pending→completed / rejected；payout：processing→completed/failed（可重试）。**Bridge 真值（勿混用，映射待补）**：VA 事件 `VirtualAccountEvent.type` = `funds_scheduled / funds_received / payment_submitted / payment_processed / in_review / refund / refund_in_flight / refund_failed / microdeposit / account_update / deactivation / activation`；Transfer `TransactionStatus` = `awaiting_funds / in_review / funds_received / payment_submitted / payment_processed / canceled / error / undeliverable / returned / refund_in_flight / refund_failed / refunded`

**枚举（对齐 Bridge，避免硬编码漂移）**
来源 SOURCE_OF_FUNDS、用途 PURPOSES、月入档 expected_monthly_payments_usd、职业 occupation_codes（`GET /lists/occupation_codes`）、雇佣状态 EMPLOYMENTS、证件类型 `identifying_information.type`（145 类）、文档用途 `documents[].purposes`（个人 8 类）。**全量枚举见附录 E；平台 ↔ Bridge 状态映射见附录 F。**

---

## 8. 异常与边界场景
| 场景 | 期望行为 |
| --- | --- |
| 不可服务国别填写 | 开户前拦截，给出国家不可服务原因，不进 KYC |
| 未同名入金 | 通道上可能被拒/退回/延迟；产品需在入金说明中预警 |
| 需 Reference 未填 | 延迟入账/匹配失败，提示补 Reference |
| KYC 未通过点"开通" | 弹 KYC 门禁，引导前往认证（01 原型） |
| VA PENDING 尝试收款 | 无 rails 字段、提示待复核通过 |
| 证件/TIN 填错 | 可即时 rejected，展示可分享原因，支持重提 |
| 未来合规要求生效 | 生效日前提示补齐（EEA TIN 2026-12-31） |
| 出金目标未核验 | 不可选作出金目标 |
| 到账金额与申报偏差 | 入账 pending，人工/自动复核 |
| ToS 未签署点「下一步」 | 停留在签署步骤并明确提示，不放行；不得以勾选代替签署 |
| 在托管页取消 / 关闭 | 保持未签署，可再次进入；不产生半成品客户 |
| 签署链接过期 / 回跳失败 | 重新获取托管链接并提示重试；已签署以平台留存为准，不重复建档 |
| 已认证老客户开户 | 跳过签署步骤（Bridge 侧已签署）；若 `requirements.missing` 出现 `tos_v2_acceptance` 则引导新版签署 |

---

## 9. 非功能需求
- **i18n**：zh/en 双语文案，键值双语字典齐全，切换即时生效（沿用 `data-i18n` + `t()` 机制）。
- **安全**：Bridge `Api-Key`/敏感凭据只存在于服务端，**绝不出现在前端/仓库**；前端永不回显密钥。浏览器侧仅经平台后端代理调用 Bridge。
- **幂等与重试**：开户、归集、出金等指令需幂等键，防重复扣减/重复建号；webhook 需签名校验。
- **审计**：客户状态、拒绝原因、归集/出金事件均可追溯；developer_reason 不进用户可见层。
- **合规留存**：ToS signed_agreement_id、KYC/Persona 结果、endorsement 时间线留存可查。
- **性能/可用性**：列表与详情为 P95 感知可接受；Bridge 异步状态（审核、归集）以轮询/webhook 更新，不阻塞 UI。

---

## 10. 埋点 / 可观测（建议）
KYC 转化漏斗、开户两阶段耗时、入金→上账时长与失败归因、同名入金拒绝率、出金失败率、PENDING→ACTIVE 时长、EEA TIN 补齐率。

---

## 11. 与原型/演示的对应
| 原型 | 页面 | 覆盖 |
| --- | --- | --- |
| 01-用户开通虚拟账户 | KYC 向导 + Lead Bank USD VA + KYC 门禁 | M1（部分）、M3（部分） |
| 02-法币账户-多渠道多账户 | 账户列表 + 开通向导（**4 步：选币种 → 签署服务条款 → 填写信息 → 确认**，含 Bridge 托管签署模拟页）+ 入金/详情弹窗 + 外部同名账户 + 出金 + 流水 + demo 面板 | M0–M11 主体（含资金来源情形自动追加材料） |

---

## 12. 未决问题 / 评审待拍板（Open Forks）
| # | 问题 | 现状/张力 | 建议评审结论方向 |
| --- | --- | --- | --- |
| H1 | ToS 签署（**2026-09-20 已确认并落地**） | 必须 Bridge 托管取得 `signed_agreement_id`（勾选不足）；存量客户新 ToS 走 `tos_acceptance_link` | 结论：采用托管签署 + `redirect_uri`/postMessage 回传，并在开户向导设**独立步骤**（M10，已落地 02 原型）；存量新版条款引导待补（M10-5） |
| H2 | PENDING 占位是否保留 | 复核中建 VA 占位是演示简化，与"VA 须 approved 后建"并存 | 确认生产用两阶段，PENDING 仅演示 |
| H3 | EEA TIN / 境外税务 | 仅托管(平台 custody)客户强制且 2026-12-31 生效；National ID 全 EEA 必填 | 确认托管模式下字段策略与生效日 |
| M3/I6 | 出金口径 | 平台余额扣减 vs Bridge offramp（wallet→external_account，FedNow beta）；VA 内"中间开户账单"所指未澄清 | 产品拍板出金语义与账单含义 |
| I3 | EUR/GBP | OpenPayd 表单显示 EEA 提示却无 EEA 字段，割裂；未验证可开通性 | 决定 EUR/GBP 去留或补 EEA 字段 |
| M4 | 入金同名策略 | 同名校验放行策略（严/宽）、非同名资金的处置流程未定 | 运营定义 |
| — | 平台余额/账本呈现 | "平台可用余额"与 VA/账户列表如何组织未定（单账本 vs 每账户） | 产品定义信息架构 |
| — | 中间开户账单 | 用户反馈原型未见"中间开户账单"；所指为入金凭据/VA 开户对账单/归集账单待确认 | 澄清后补 PRD 条目 |
| H5 | EEA reliance 时间戳字段 | EEA in-scope 走 reliance 需 `verified_govid_at` / `verified_selfie_at` / `verified_database_at`（write-only）；原型未建模 | 与合规确认采集方与组合规则（附录 A #25） |
| H6 | 文档数组多用途模型 | 原型仅覆盖 `proof_of_address` 单文档；Bridge `documents[].purposes` 支持个人 8 类用途 | 确认是否本期做多文档 UI 与全量 purposes（附录 A #28） |
| H7 | VA 归集目标模式 | `address` / `bridge_wallet_id` / `prefunded_account_id` 三选一；`blockchain_memo` 仅 memo 链 | 拍板归集模式（当前取 `address` = 平台托管钱包；附录 C） |
| H8 | 平台 ↔ Bridge 状态映射 | Bridge customer status 10 值（含 `paused` / `deposits_restricted` / `offboarded` / `awaiting_ubo` / `awaiting_questionnaire`）；VA 仅 `activated` / `deactivated`，平台用了 4 态 | 拍板映射表与「暂停 / 入金受限」是否需 UI（附录 F 给建议映射） |
| H10 | 开户字段清单的呈现位置 | 字段真值分散在附录 A（客户建档 31 字段）/ 附录 C（VA 开立），无「按向导步骤」的可见项清单，评审时找不到 | **已落地**：本 PRD 补 **附录 H**（按步骤的可见项 ↔ 接口字段 ↔ 出现条件）；**03 EUR/GBP PRD 已同步**（新增「开户字段真值（平台 C 端接口）」章 + 按步骤可见项附录）；后续字段变更须同步附录 A + H |
| H13 | 资金来源情形的阈值与判定方 | 三个触发器名称在 Bridge OpenAPI **0 命中**（属内部合规触发器）；个人 `expected_monthly_payments_usd` 为**四档枚举**，**高风险地区个人 20 万美元档在个人字段中无法表达**（20 万档仅企业侧 integer 金额） | 与 Bridge / 合规确认：20 万档是否需在个人侧新建档位；三触发器由平台自判还是渠道下发（判定口径来源） |
| H15 | 情形变化后的材料重判 | 用户在步骤③改字段导致情形消失时，已上传材料被清空；提交后字段变化是否需重交材料未定 | 产品拍板：**判一次**（提交时快照）vs **每次变更重判**；补件期是否复用 `awaiting_questionnaire` / `source_of_funds_questionnaire` |

### 已决策记录
| # | 决策 | 结论 | 影响 |
| --- | --- | --- | --- |
| H4 | US 进件档位 | **仅标准档完整 KYC；不做 restricted 低门槛档，不做「提升限额」升档引导**（2026-09-04 拍板） | PRD：M0-3/§1.4/§3 已改；实现待办：修正原型 `NATIONS.USA` 证件字段与 `usNotice` 文案自洽（按标准档口径，确认是否需补证件照采集与住址证明），使标准档不残留 restricted 痕迹 |
| H1 | ToS 签署落位 | **独立步骤**：选币种 → **签署合作机构服务条款** → 填写账户信息 → 确认开通（2026-09-20 拍板）；签署在信息采集之前，与「ToS 是创建客户的前置条件」一致 | PRD：§5.1 / M1-2 / M10 / §7 / §8 / 附录 B 已改；实现：02 原型已落地四步向导 + 模拟托管页回跳 |
| D10 | **账户数量口径：支持多账户（原 H9）** | **保留多账户、不设数量上限**（2026-09-20 拍板）：同一币种可开多个账户；用户已开通多个美元账户时仍可继续申请开通新的美元账户，开户入口不做唯一性拦截；账户名自动递增 | PRD：M0-4 / M3-1 已定稿；原型 02 `defaultAccName()` 无需改动 |
| D11 | **EEA / BBSA 名单与触发维度（原 H11）** | **全部采纳**（2026-09-20）：① 名单 = **EU27 + ISL / NOR / LIE + GBR = 31 国**；② **英国（GBR）in-scope**；③ 触发维度 = **居住国 / 国籍 / 出生地 任一**；④ `EEA_NATID` 由 28 → **31 国**（补 SVK / LIE / GBR）并加国籍 / 出生地变更重算 | PRD：M11-1 / M11-4；原型 02：`needEea()` 三维 + 31 国表 + 联动刷新；**SVK / LIE / GBR 国别类型待合规回填** |
| D12 | **个人开户「其他税务居民国家」行（原 H12）** | **移除**（2026-09-20 拍板）：Bridge **individual** payload 无对应字段（能力在 business `has_foreign_tax_registration`），个人侧不采集、不展示 | PRD：M11 缺口段 + 附录 H 该行已删；原型 02 已删 `kfFtrCb` / `kfFtrRow` / `kfFtrCountries` 及 i18n 键 `ftrCb` / `ftrCountriesL` / `ftrCountriesHint` / `errFtr` |
| D13 | **资金来源情形（S1–S3）判定依据的采集范围（原 H14）** | **不常显**（2026-09-20 拍板）：判定与展示**只在 EEA / BBSA in-scope、高风险、标注客户内生效**，即 `employment_status` / `source_of_funds` / `expected_monthly_payments_usd` 的现有可见范围；为让 EEA 客户可被判定，原型把后两项随条件字段行一并展示（EEA 亦可见、亦必填）；非 EEA 且非风险 / 标注客户不采集这 3 项，故不参与判定 | PRD：M11.A 口径段改写 + §7 补判定范围 + H14 关闭；原型 02：新增 `kfSofRow` 面板（资金来源 / 预计每月资金往来）并由 `needCond()` 控制，S1–S3 判定门控 `needMore()` → `needCond()`；**附修存量缺陷** `updateStateReq()` 空值保护（原写法抛 TypeError → 合规面板在正常路径不渲染） |

---

## 13. 附录

### 13.0 参考与修订记录
- Bridge 在线文档：apidocs.bridge.xyz（Customers / Endorsement / KYC Link / ToS / Virtual Account / Wallet / External Account / Proof of address / additional requirements）。
- Proof of address：政府证件来自受控/禁运地区却申报境外居住的个体，或地址信号冲突时需 90 天内住址证明（银行账单/水电/政府信函/90 天内政府证件/租房合同）——M1/POA 相关实现时引用。
- **字段出处**：以下字段表逐字取自 Bridge OpenAPI 描述文件（`https://withbridge-image1-sv-usw2-monorail-openapi.s3.amazonaws.com/latest.json`，2026-09-20 拉取，共 100 paths）；标注 `*` 者为该 schema 的必填项。**不写 spec 之外的字段**，实现前按后端锁定版本复核。
- **约束维度（2026-09-20 机器核对，非人工摘录）**：`类型 / 约束` 列取值逐字取自 spec 的 `type` / `format` / `minLength` / `maxLength` / `enum`。三条核对结论：
  - **本接口无 `number` / `integer` 字段** —— 31 个顶层字段全部为 string / array / object / boolean。金额一律 string 枚举区间（`expected_monthly_payments_usd` = `0_4999` / `5000_9999` / `10000_49999` / `50000_plus`）、日期一律 string 定长（`birth_date` 固定 10 位、`expiration` yyyy-mm-dd）、职业为 string 职业码。**前端不得按数字类型解析，也不得做千分位 / 小数处理**。
  - **`required` 真相**：spec 顶层仅 `type` 强制；嵌套强制项为 `residential_address{street_line_1, city, country}`、`transliterated_residential_address` 同、`identifying_information[]{type, issuing_country}`、`documents[]{purposes, file}`、`liveness_check_selfies[]{image}`。表中其余「必填」系 Bridge 建档 / 风控业务口径（**非 spec 强制**），实现前须与后端复核。
  - **`writeOnly` 13 个字段**（仅存在于请求体，接口不回返）：`residential_address`、`transliterated_residential_address`、`signed_agreement_id`、`endorsements`、`nationality`、`nationalities`、`place_of_birth`、`verified_database_at`、`verified_govid_at`、`verified_selfie_at`、`liveness_check_selfies`、`identifying_information`、`documents`。**实现影响**：`residential_address` / `transliterated_residential_address` / `place_of_birth` 同属 write-only → 居住地址与出生地**无法从 Bridge 回读**，平台侧须本地留存（附录 H 中「系统带出」的居住国 / 出生地即据此由平台自身数据带出，不从 Bridge 读）。
  - 长度下限的平凡约束（`minLength=1`）已在表中以 `(≥1)` 标出：`type`、`street_line_2`、`city`、`postal_code`、`place_of_birth.city`。
- **字段约束的接口真值（2026-09-20 按 spec 逐字段机器比对；执行层＝服务端按本节实现，原型不承载接口级校验）**：
  - ① 姓名 `first_name` / `last_name` = **2–1024**（`UpdateIndividualCustomerPayload` minLength=2 / maxLength=1024；读取模型 `Customer.*` 为 minLength=1，**写入侧以 2 为准**）；
  - ② 转写名 `transliterated_first_name` / `_middle_name` / `_last_name` = **1–256**；
  - ③ 外部账户 `ExternalAccountAddress.street_line_1` = **4–35**、`street_line_2` ≤ 35、`account_owner_name` **3–35**；
  - ④ 邮编 `postal_code` **不在** `Address` / `ExternalAccountAddress` 的 `required`（仅 `{street_line_1, city, country}`），描述为 *Must be supplied for countries that use postal codes* → 按国家条件必填，**国家名单待补（开放项）**；
  - ⑤ `subdivision`（居住地址 `Address2025WinterRefresh`）= **1–3** 位、`Address.state` = **1–3** 位；**外部账户 `ExternalAccountAddress.state` 仅 `minLength=1`、无 `maxLength`**（勿按 1–3 实现）；三处均**仅美国地址必填**；
  - ⑥ 居住地址（`residential_address` → **`Address2025WinterRefresh`**，非 `Address`；`Address` 的对应字段名为 `state`）`street_line_1` ≥ 4、**无上限**；`country` 一律 ISO 3166-1 **alpha-3**；`birth_date` 固定 10 位 yyyy-mm-dd；
  - ⑦ 结构长度 `city` / `postal_code` / `street_line_2` / `place_of_birth.city` = **≥1**；
  - ⑧ **spec 正则分布** —— Bridge 全库 `pattern` 共 **8 处**：`Id` / `DepositId` / `Omad` / `Imad`（`[a-z0-9]*`）、`TraceNumber`（`[0-9]`）、`Clabe`（`^[0-9]+$`）、`IbanBankAccount.bic`（`^[A-Za-z]{4}[A-Za-z]{2}[A-Za-z0-9]{2}([A-Za-z0-9]{3})?$`）、`Webhook.id`（`^wep_[a-f0-9]+$`）；**客户建档链路（附录 A）无任何 `pattern`**；故 `email` 格式、`phone` E.164、`iban` 结构 + mod97 校验位属**平台侧规则**（服务端实现），**不得当作接口约束评审**；
  - ⑨ `IdentifyingInformation.required` 为空 —— 「证件号必填、政府证件须传正反面、税号类免传影像」来自 apidocs 散文口径，实现前须与后端复核。**原型侧口径**：原型 02 以演示为主、**不实现上述接口级校验**（原型上的必填标记与格式校验仅为演示需要），接口约束、字段异常与错误文案**一律以本节与附录 A 为准**；原型与本节不一致时**不视为缺陷**。

| 版本 | 日期 | 修订内容 |
| v0.8 | 2026-09-20 | ⑰ **全量审计修订（PRD ↔ Bridge OpenAPI 逐字段机器核对，非人工摘录）**：`writeOnly` 10 → **13**（补 `residential_address` / `transliterated_residential_address` / `place_of_birth`，并记 write-only 回读影响）；`pattern` 「仅 2 处」→ **8 处**（列全）；`ExternalAccountAddress.state` 无 `maxLength`（不再写 1–3）；居住地址 schema 更正为 `Address2025WinterRefresh`；`identifying_information` 的 EEA 要求出处改为 EEA 政策页（该 schema 无 description）；§7 endorsement 状态 `pending` → `incomplete`；§7 KYC 状态补 `KycStatus` / `CustomerStatus` 真值；附录 B / M1-2 / M10-3 的 `postMessage` + `signedAgreementId` 标注 spec 未声明（0 命中）；附录 H `kfSof` / `kfMonthly` 条件补 D13（EEA 亦采集）、`kfSofDocsHint` 标注为文案键；M6-6 `address` 区分必填（`us`）/ 选填（`iban` / `gb`）、`account_owner_name` 标注 1–256 与 3–35；§7 与 M6-2 外部账户核验改用 `match_level`（`verified` 非 Bridge 值）；§7 与 M7-2 流水状态标注平台态并列出 Bridge 真值；附录 F 标 `Customer.rejection_reasons` deprecated；附录 E 标 `requirements_due` deprecated + `future_requirements_due`、`missing` 出处；附录 C / M3-7「0–100」标注为平台约定；附录 D `account_type` 补响应侧 `BankAccountNumberType` 差异；附录 A #22 `nationality` 迁移后 deprecated、#27 补图片合计 24MB；M11-5「7 项」→ 6 字段 + 1 条件字段；H13 补「阈值非 spec 依据」 |

| v0.7 | 2026-09-20 | ⑯ **焦点 A 判定范围拍板落地（D13＝原 H14 关闭）**：S1–S3 的判定与展示**只在 EEA / BBSA in-scope、高风险、标注客户内生效**，**不做常显**；原型 02 新增 `kfSofRow`（资金来源 / 预计每月资金往来随条件字段行展示，**EEA 客户亦可见并必填**）、S1–S3 判定门控 `needMore()` → `needCond()`；**附修存量缺陷**：`updateStateReq()` 读 `kfStateReq`（该 span 位于 `data-i18n` 标签内，被 `applyI18n` 替换后消失）抛 TypeError，致 `applyUserCountry()` 中断、EEA / 风险合规面板与 EEA 字段组在正常路径下不渲染 → 已加空值保护 |
| v0.6 | 2026-09-20 | ⑮ **三种资金来源情形（S1–S3）落地**：判定**不由人工接入**，由平台按用户自填字段值**自动判定**、命中即在步骤③**自动追加需上传材料**；新增 **M11-10** 行 + **M11.A 细则**（判定矩阵 / 时序 / 多情形叠加 / 必传拦截 / 中英文案 / 口径边界）、§7 补充、附录 H 追加 5 行、§12 新增 H13–H15；原型 02 新增 `kfSofDocs` 区块 + `sofCases()` / `renderSofDocs()`（i18n 新增 15 键，中英对称） |
| v0.5 | 2026-09-20 | ⑭ **字段约束口径定稿**：接口级校验**不在原型承载**，约束真值与执行层声明集中写入 §13；M1-8 邮编改为「按国家条件必填（国家名单待补）」；M6-6 IBAN 校验位标注为平台侧规则；本轮原型为对齐 spec 所做的校验改动已**全部回退** |
| --- | --- | --- |
| v0.4 | 2026-09-20 | ⑫ **H9 / H11 / H12 拍板落地**：M0-4 定稿「支持多账户、不设数量上限」（D10）、M3-1 去待拍板；M11-1 / M11-4 改为 31 国名单 + GBR in-scope + 三维任一触发（D11）；个人侧「其他税务居民国家」行移除（D12）；⑬ 原型 02 同步：`needEea()` 三维判定、`EEA_NATID` 补齐 SVK / LIE / GBR（28 → 31）、`kfNations` / `kfBirthCountry` 变更重算、删除境外申报行及其 i18n 键 |
| v0.3 | 2026-09-20 | ⑧ 新增 **M11 合规画像判定与增补字段**（EEA / 高风险 / 标注 / 不可服务四类画像的判定条件与命中后字段后果，逐条对齐 Bridge description 原文）；⑨ 新增 **附录 H 开户向导可见字段清单（按步骤）** 与 M1 头部指引；⑩ M0 新增 **M0-4 账户数量口径**、M3-1 标注口径待拍板；⑪ §12 新增 H9–H12（账户数量口径 / 字段清单呈现 / EEA·BBSA 名单口径 / 个人其他税务居民字段归属），H3 见 M11 |
| v0.2 | 2026-09-20 | ① §5.1 流程新增「ToS 托管签署」独立步骤；② M1-2 改写、M1-9~13 / M3-6~7 / M6-6~7 新增、新增 **M10** 模块；③ §7 补 ToS 状态与枚举来源；④ §8 补 4 条 ToS 异常；⑤ 附录 A–G 全量字段对齐（客户建档 / ToS / VA / 外部账户 / 枚举 / 状态映射 / 请求字段边界）；⑥ §12 H1 转已确认、新增 H5–H8；⑦ 附录 A 增「约束维度」机器核对口径（类型分布 / `required` 真值 / `writeOnly` 集合），并修正枚举与长度：`account_purpose` 补 `operating_a_company`（10→**11 值**，附录 A + 附录 E 两处）、`birth_date` 固定 10 位、`subdivision` 1–3 位、`country`/`place_of_birth.country` 固定 3 位、`street_line_2`/`city`/`postal_code` ≥1 |
| v0.1 | 2026-09-04 | 初稿 |

### 附录 A. 客户建档 `POST /v0/customers`（`type=individual`）字段全量对齐
> 平台侧当前仅做 individual（企业 `type=business` 见 §1.4 非目标）。`覆盖` 列以 `02-法币账户-多渠道多账户.html` 向导第 3 步为基准。

| # | Bridge 字段 | 类型 / 约束 | 必填条件 | 平台 UI 映射（原型 02） | 覆盖 |
| --- | --- | --- | --- | --- | --- |
| 1 | `type` | string，enum [individual] | 必填 | 平台服务端固定注入 `individual` | 覆盖（服务端） |
| 2 | `first_name` | string，2–1024 | 必填 | 名 `kfFirst` | 覆盖 |
| 3 | `middle_name` | string，1–1024 | 选填 | 中间名 `kfMiddle` | 覆盖 |
| 4 | `last_name` | string，2–1024 | 必填 | 姓 `kfLast` | 覆盖 |
| 5 | `transliterated_first_name` | string，1–256 | 当 `first_name` 含非 Latin-1 字符时必填（可接受字符：Latin-1 À-ÖØ-ßà-öø-ÿ 与 `\x20-\x7E`） | 拼音/拉丁转写名 `kfFirstTr` | 覆盖 |
| 6 | `transliterated_middle_name` | string，1–256 | 同上 | `kfMiddleTr` | 覆盖 |
| 7 | `transliterated_last_name` | string，1–256 | 同上 | `kfLastTr` | 覆盖 |
| 8 | `email` | string，1–1024 | 必填 | 邮箱 `kfEmail` | 覆盖 |
| 9 | `phone` | string，1–1024，格式 `+122****4444`（E.164） | 必填 | 手机号 `kfPhone` | 覆盖 |
| 10 | `residential_address` | object：`street_line_1`(≥4)、`street_line_2`(≥1)、`city`(≥1)、`subdivision`（**1–3 位**，ISO 3166-2，美国必填）、`postal_code`(≥1)（有邮编国家必填）、`country`（ISO 3166-1 alpha-3，**固定 3 位**）；`street_line_1`/`city`/`country` 必填 | 必填 | 居住国 `kfRes` + 地址 `kfAddr`/`kfAddr2` + 城市 `kfCity` + 州/省 `kfState` + 邮编 `kfZip` | 覆盖 |
| 11 | `transliterated_residential_address` | 同 #10 结构 | 当住址含非 Latin-1 字符时必填 | 转写地址 `kfAddrTr` | 覆盖 |
| 12 | `birth_date` | string，**固定 10 位**（yyyy-mm-dd；须满 18 岁） | 必填 | 出生日期 `kfDob` | 覆盖 |
| 13 | `signed_agreement_id` | string，1–1024 | 必填（新客户须先完成 Bridge 托管 ToS 签署） | 不用户填写：向导第 2 步签署回跳取得，服务端随建档提交 | 覆盖（本轮新增） |
| 14 | `endorsements` | string[]，enum [base, cards, cop, faster_payments, pix, pix_onramp, pix_offramp, sepa, spei] | 选填；**不传时 Bridge 默认尝试授予 base + sepa** | 服务端显式注入 `['base']`（EUR 若开通另议） | 需确认（建议显式传，见 M1-13） |
| 15 | `account_purpose` | string，enum [charitable_donations, ecommerce_retail_payments, investment_purposes, operating_a_company, other, payments_to_friends_or_family_abroad, personal_or_living_expenses, protect_wealth, purchase_goods_and_services, receive_payment_for_freelancing, receive_salary] | 高风险客户必填；EEA / BBSA in-scope 亦必填 | 账户用途 `kfPurpose` | 覆盖 |
| 16 | `account_purpose_other` | string | 当 `account_purpose=other` | 用途补充说明 `kfPurposeOther` | 覆盖 |
| 17 | `employment_status` | string，enum [employed, homemaker, retired, self_employed, student, unemployed] | 高风险客户必填（EEA 亦要求） | 雇佣状态 `kfEmp` | 覆盖 |
| 18 | `expected_monthly_payments_usd` | string，enum [0_4999, 5000_9999, 10000_49999, 50000_plus] | 高风险客户必填 | 月收付规模 `kfMonthly` | 覆盖 |
| 19 | `acting_as_intermediary` | boolean | 高风险客户必填 | 是否代第三方持有 `kfInter` | 覆盖 |
| 20 | `most_recent_occupation` | string（职业码） | 高风险客户必填；取值建议来自 `GET /lists/occupation_codes` | 最近职业 `kfOccup` | 覆盖（取值改拉取，见 M1-7） |
| 21 | `source_of_funds` | string，enum [company_funds, ecommerce_reseller, gambling_proceeds, gifts, government_benefits, inheritance, investments_loans, pension_retirement, salary, sale_of_assets_real_estate, savings, someone_elses_funds] | 高风险客户必填 | 资金来源 `kfSof` | 覆盖 |
| 22 | `nationality` | string，ISO 3166-1 alpha-3 | 遗留单值字段（迁移期 Bridge 二者皆认，`nationalities` 优先；**迁移后 `nationality` 将 `deprecated`**） | 国籍 `kfNation` | 覆盖 |
| 23 | `nationalities` | string[]，ISO 3166-1 alpha-3 | EEA / BBSA in-scope 必填（须给全部国籍） | 多国籍 `kfNations` | 覆盖 |
| 24 | `place_of_birth` | object：`country`（alpha-3，**固定 3 位**）、`city`(≥1)；EEA / BBSA in-scope 提供 | EEA / BBSA in-scope | 出生国家 `kfBirthCountry` + 出生城市 `kfBirthCity` | 覆盖 |
| 25 | `verified_database_at` / `verified_govid_at` / `verified_selfie_at` | string，ISO 8601 date-time（write-only） | 仅 EEA in-scope 走 reliance（`TWO_FORMS_OF_ID_RELIANCE`）时按组合提交 | 原型未建模 | **缺口（H5）** |
| 26 | `liveness_check_selfies` | array of `{image}`：base64 data-uri，≥200×200，≤15MB，.jpeg 等 | 代 Bridge 采集自拍时使用；**EEA in-scope 不适用（须走 Persona 托管）** | 自拍 `kfSelfie`；EEA 走 `selfieHost` 托管跳转 | 覆盖 |
| 27 | `identifying_information` | array of `{type, issuing_country, number, description, expiration, image_front, image_back}`：`type` 145 类（passport / national_id / drivers_license / 各国税号…）、`issuing_country`（alpha-3，必填）、`number`（作税号用时必填）、`description`（`type=other` 时必填）、`expiration`（yyyy-mm-dd）、`image_front`（政府证件必填 / 税号选填，base64 200px x 200px 起、≤15MB；**`image_front` + `image_back` 合计 ≤24MB**）、`image_back` | 至少 1 项（按国别规则） | 证件类型 `kfIdType` + 证件号 `kfIdNo` + 有效期 `kfIdExp` + 正反面 `kfIdFront`/`kfIdBack`；EEA 追加 `kfNatId`/`kfTin` | **部分覆盖**：`issuing_country` 需逐证件采集 |
| 28 | `documents` | array of `{purposes, file, description}`：`purposes` enum [proof_of_account_purpose, proof_of_address, proof_of_individual_name_change, proof_of_relationship, proof_of_source_of_funds, proof_of_source_of_wealth, proof_of_tax_identification, other]、`file`（base64 data-uri，≥200×200，≤24MB）、`description`（`other` 时必填） | 按风控 / 合规触发（POA、SOF 佐证等） | 住址证明 `kfPoa`（仅 proof_of_address 单文档） | **部分覆盖（H6）** |
| 29 | `client_reference_id` | string，1–256 | 选填（平台自用） | 服务端注入（用户 ID / 申请单号） | 需确认 |

### 附录 B. ToS（Bridge 托管签署）接口与字段
| 接口 / 字段 | 用途与约束 | 平台落位 |
| --- | --- | --- |
| `POST /v0/customers/tos_links` | 为**新客户**取得托管签署 URL；**明确："Signing this acceptance flow is a requirement for creating customers"**；返回托管 `url`（含 session token），支持 `redirect_uri` 回跳 | 向导第 2 步「前往 Bridge 托管页签署」触发 |
| `GET /v0/customers/{customerID}/tos_acceptance_link` | 为**存量客户**取得接受新版 ToS 的托管 URL | 账户页「需接受新版条款」提示（M10-5，待办） |
| 回传 `signed_agreement_id` | 托管页签署完成后回传；随 `POST /v0/customers` 提交。**接口口径**：`POST /customers/tos_links` 仅声明 `Idempotency-Key` 参数，spec **未声明**回传机制（`postMessage` / `signedAgreementId` 在 spec **0 命中**）；返回示例 URL 带 `redirect_uri=...` 查询参数 → 以 `redirect_uri` 回跳为准，其余回传机制**须与 Bridge 确认**（未决，待登记） | 平台留存 + 建档必带 |
| `has_accepted_terms_of_service` | boolean，客户查询接口返回，表示客户是否已接受 ToS | 判断是否需再次引导签署 |
| `requirements.missing` 中的 `tos_acceptance` / `tos_v2_acceptance` | endorsement 维度表达 ToS 是否满足（新客户 / 新版条款） | 账户详情「合规状态」已满足项与待办项 |
| 条款版本 | USD / base 通道为 **Terms v1**；存量客户新版条款须以 `tos_acceptance_link` 返回为准 | 步骤与确认页展示版本号 |

### 附录 C. 开立收款账户 `POST /v0/customers/{customerID}/virtual_accounts` 字段
| Bridge 字段 | 类型 / 约束 | 平台取值与说明 |
| --- | --- | --- |
| `source.currency` | enum [usd, eur, mxn, brl, cop, gbp] | 本期 `usd`（EUR/GBP 走 OpenPayd 通道，不在本 PRD） |
| `destination.currency` | enum [usdb, usdc, usdt, pyusd, eurc] | `usdc` |
| `destination.payment_rail` | enum [arbitrum, avalanche_c_chain, base, celo, ethereum, optimism, polygon, solana, stellar, tempo, tron, xdc] | `base` |
| `destination.address` | string | 平台托管钱包地址（用户不可填，三选一之一） |
| `destination.blockchain_memo` | string | 仅 memo 链（如 stellar）需要；Base 不传 |
| `destination.bridge_wallet_id` | string（UUID，1–42，`[a-z0-9]*`） | 备选归集模式（若改用 Bridge Wallet） |
| `destination.prefunded_account_id` | string（UUID，1–42，`[a-z0-9]*`） | 备选归集模式 |
| `developer_fee_percent` | string，**base-100 百分比**（description 逐字：*The value is a base 100 percentage, i.e. 10.2% is 10.2 in the API*）；**spec 未声明 min/max，「0–100」为平台约定** | 平台费率决策项；与 `fee_config` 不可同传 |
| `fee_config` | object | 需向 Bridge 申请开通方可用；本期不传 |
| `travel_rule_data` | object | 仅当该 VA 的所有资金往来发起人/受益人固定时使用；**本业务不适用** |
| 出参 `status` | enum [activated, deactivated] | 与平台 4 态展示的映射见附录 F |
| 出参 `source_deposit_instructions`（USD） | `bank_account_number`*、`bank_routing_number`*、`bank_beneficiary_name`*、`bank_beneficiary_address`*、`bank_name`*、`bank_address`*、`currency=usd`*、`payment_rails`* ∈ [ach_push, fednow, wire] | 即入金弹窗「打款说明书」字段（账户号/路由号/户主/户主地址/银行名/银行地址/支持通道） |
| 出参 `id` / `created_at` / `customer_id` | string | 平台账户记录主键与开户时间 |

### 附录 D. 外部账户（出金目标）`POST /v0/customers/{customerID}/external_accounts` 字段
> 请求为 `oneOf` 多类型；本期用到 `us` / `iban` / `gb`，其余类型登记备查。

| Bridge 字段 | 类型 / 约束 | 平台取值与说明 |
| --- | --- | --- |
| `account_owner_name` | string，1–256；ach/wire/iban 要求 **3–35 字符 + 各类型正则**（出处：spec description 明列；原型为只读带出，不做输入校验） | 户名，须与本人实名**同名**（原型 `XIAOMING LI`） |
| `address` | object：`street_line_1`（4–35，必填）、`street_line_2`（≤35）、`city`*、`state`（ISO 3166-2，美国必填）、`postal_code`、`country`*（alpha-3） | 复用实名居住地址（US Beneficiary Address Validation 要求准确） |
| `account_type` | 请求侧 enum [us, iban, clabe, pix, gb, bre_b, co_bank_transfer]（共 7 值；BR Code 类型亦取 `pix`）| `us`（USD 出金）/ `iban`（EUR）/ `gb`（GBP）。**注意**：响应 / 通用枚举 `BankAccountNumberType` = [us, iban, bre_b, clabe, pix, gb, **unknown**]，**不含 `co_bank_transfer`**，二者不同源 |
| `currency` | enum [usd, eur, mxn, brl, gbp, cop] | 与 `account_type` 一一对应：us→usd、iban→eur、gb→gbp |
| `account`（US） | `account_number`*、`routing_number`*（9 位）、`last_4`*、`checking_or_savings` enum [checking, savings] | USD 外部账户：账号 + 路由号；默认按 checking 处理 |
| `iban` | `account_number`*、`bic`（8–11 位，正则 `^[A-Za-z]{4}[A-Za-z]{2}[A-Za-z0-9]{2}([A-Za-z0-9]{3})?$`）、`country`*、`last_4`* | EUR 外部账户（BIC 选填但建议给，可提升成功率） |
| `account`（GB/FPS） | `account_number`*（8 位）、`sort_code`*（6 位，不含连字符）、`last_4`* | GBP 外部账户 |
| `account_owner_type` / `first_name` / `last_name` / `business_name` | enum [individual, business]；individual 时 first/last 必填；business 时 business_name 必填 | 个人同名账户取 `individual` + 实名姓名 |
| `account_owner_country` | string，alpha-3 | 账户持有人居住国（与本人实名一致） |
| `deactivation_reason` | enum [plaid_item_error, deactivated_due_to_bounceback, deleted_by_developer, requested_by_developer, invalid_account_number, invalid_bank_validation, rejected_by_bank_provider] | 展示「为何不可出金」（M6-7） |
| `deactivation_details` | string | 不可用时的补充说明 |
| `active` | boolean | 是否可用（结合 verify 接口核验结果） |
| 已弃用 | 顶层 `account_number`（≥12）/ `routing_number`（≥9） | **不再使用**，一律走 `account.*` |

### 附录 E. 枚举总表（来源：Bridge OpenAPI，2026-09-20）
| 枚举 | 取值 |
| --- | --- |
| 客户 `status` | active, awaiting_questionnaire, awaiting_ubo, deposits_restricted, incomplete, not_started, offboarded, paused, rejected, under_review |
| 客户 `capabilities.{payin_crypto, payout_crypto, payin_fiat, payout_fiat}` | pending, active, inactive, rejected |
| 客户 `requirements_due`（**spec 已标 `deprecated`**；客户侧另有 `future_requirements_due` 为新字段） | external_account, id_verification |
| endorsement `name` | base, cards, cop, faster_payments, pix, pix_onramp, pix_offramp, sepa, spei |
| endorsement `status` | incomplete, approved, revoked |
| endorsement `requirements`（`additional_requirements` 旧字段同值） | kyc_approval, tos_acceptance, kyc_with_proof_of_address, tos_v2_acceptance（**注意**：`missing` 在 spec 中为无 `properties` 的 object，`missing.all_of` 结构来自实调 / 文档口径，非 schema 声明） |
| `future_requirements[].verification_stage` | automatic_review, manual_review, post_review, complete, not_applicable |
| VA `status` | activated, deactivated |
| VA `source.currency` → 支持 rail | usd→[ach_push, fednow, wire]；eur→[sepa]；gbp→[faster_payments]；mxn→[spei]；brl→[pix]；cop→[bre_b] |
| VA `destination.currency` | usdb, usdc, usdt, pyusd, eurc |
| VA `destination.payment_rail` | arbitrum, avalanche_c_chain, base, celo, ethereum, optimism, polygon, solana, stellar, tempo, tron, xdc |
| 客户 `account_purpose`（个人） | charitable_donations, ecommerce_retail_payments, investment_purposes, operating_a_company, other, payments_to_friends_or_family_abroad, personal_or_living_expenses, protect_wealth, purchase_goods_and_services, receive_payment_for_freelancing, receive_salary |
| `source_of_funds`（个人） | company_funds, ecommerce_reseller, gambling_proceeds, gifts, government_benefits, inheritance, investments_loans, pension_retirement, salary, sale_of_assets_real_estate, savings, someone_elses_funds |
| `employment_status` | employed, homemaker, retired, self_employed, student, unemployed |
| `expected_monthly_payments_usd`（个人） | 0_4999, 5000_9999, 10000_49999, 50000_plus |
| `identifying_information[].type` | 145 类（政府证件：drivers_license, national_id, passport, permanent_residency_id, state_or_provincial_id, visa, military_id, matriculate_id 等 + 各国税号：ssn, itin, cpf, cnpj, nino, utr, rrn, sin, tfn, steuer_id, idnr 等）；完整列表由 Bridge 文档与 `identifying_information` schema 提供 |
| `documents[].purposes`（个人） | proof_of_account_purpose, proof_of_address, proof_of_individual_name_change, proof_of_relationship, proof_of_source_of_funds, proof_of_source_of_wealth, proof_of_tax_identification, other |

### 附录 F. 平台状态 ↔ Bridge 状态映射（建议，待拍板 H8）
| 平台展示（原型 02） | Bridge 真实值 | 说明 |
| --- | --- | --- |
| 未提交（notSubmitted，显示认证表单） | not_started / awaiting_questionnaire | 尚未提交或待补充问卷 |
| 复核中（underReview） | under_review / awaiting_ubo | 人工/系统审核中 |
| 已认证（approved） | active | 通过 |
| 已拒绝（rejected，可重提） | rejected（配 `rejection_reasons[].reason`，可分享） | `developer_reason` 仅内部，不得展示。**注意**：spec 中 `Customer.rejection_reasons` 已标 **`deprecated`**；在用取值处为 `IndividualKycLinkResponse.rejection_reasons` / `SimulateKycApprovalResponse` → 直连建档场景的拒绝原因来源**须与 Bridge 确认** |
| —（无对应展示位；须与「已拒绝」区分） | offboarded | 内部审查后关闭（可疑活动），用户可见口径须与「被拒」区分 |
| —（无对应展示位；须补） | paused / deposits_restricted | 账户暂停 / 入金受限，**平台当前无对应展示位**，须补 |
| VA 开通中（PENDING） | 无对应值（VA 仅在 endorsement approved 后创建） | 演示占位；生产改两阶段（H2） |
| VA 已开通（ACTIVE） | activated | — |
| VA 已停用（SUSPENDED / CLOSED） | deactivated | 平台叠加展示，非 Bridge 原值 |

### 附录 G. destination 与「用户不可填」边界
- `destination.address`、`destination.bridge_wallet_id`、`destination.prefunded_account_id` 三选一，**均由平台服务端注入**；前端只读展示「归集至平台托管钱包（USDC / Base）」。
- 入金侧收款信息（`source_deposit_instructions`）**全部来自 Bridge 返回值**，前端不得本地拼装或推测（含户主名与银行地址）。
- Bridge `Api-Key`、`session_token` 等敏感值仅存服务端（§9 安全）。



### 附录 H. 开户向导可见字段清单（按步骤，原型 02 ↔ Bridge 字段）

> 用途：把「开户时用户看到的每一项」与接口字段对上，并标出**出现条件**与**归属**。**类型 / 长度 / 枚举约束不在此重复**，一律以附录 A（客户建档）/ 附录 C（VA 开立）为准。
> 归属取值：**用户填** = 用户输入；**系统带出** = 由实名资料/登录态自动填充、用户可改；**只读** = 展示但不可编辑（提交值被忽略）；**平台注入** = 服务端写入且前端不出现。

**步骤 ① 选择法币账户类型**（币种卡 `buildPath()`）
| 可见项 | 接口字段 | 归属 | 出现条件 |
| --- | --- | --- | --- |
| 币种（USD / EUR / GBP） | `VA.source.currency` | 用户选 | 常显；不可服务国家在此之前拦截（M11-8 / `noSvcNotice`） |
| 该币种已有账户 / 已开通提示 | —（平台态） | 系统带出 | 有已开通账户时仍可继续开通，**不限数量、不拦截**（D10） |

**步骤 ② 签署合作机构服务条款**（仅美元首次开户；EUR/GBP 与老客户无此步，M10-1）
| 可见项 | 接口字段 | 归属 | 出现条件 |
| --- | --- | --- | --- |
| 签署状态（待签署 / 已签署） | `has_accepted_terms_of_service`（读） | 系统带出 | 常显 |
| 签署编号 / 签署时间 | `signed_agreement_id`（写，1–1024） | 托管页回跳带出 | 签署完成后 |
| 「前往签署」按钮 → 外部托管页 | `POST /v0/customers/tos_links` 返回的 `url` | 平台发起 | 常显（本步内） |

**步骤 ③ 填写账户信息（个人）** —— 表内前三段为常显，后三段按画像条件出现
| 可见项（原型 id） | 接口字段 | 归属 | 出现条件 |
| --- | --- | --- | --- |
| 名 / 中间名 / 姓（`kfFirst` / `kfMiddle` / `kfLast`） | `first_name` / `middle_name` / `last_name` | 用户填 | 常显 |
| 拼音（转写）名 / 中间名 / 姓（`kfNameTrRow`：`kfFirstTr` / `kfMiddleTr` / `kfLastTr`） | `transliterated_first_name` / `_middle_name` / `_last_name` | 用户填 | 姓名含非 Latin-1 字符时 |
| 出生日期（`kfDob`） | `birth_date`（固定 10 位 yyyy-mm-dd，须满 18 岁） | 用户填 | 常显 |
| 国籍（`kfNation`）→ 多国籍（`kfMultiCb` / `kfNationsRow` / `kfNations`） | `nationality`（遗留单值）/ `nationalities[]`（全部国籍） | 系统带出，用户可改 | 单国籍默认；勾选「多国籍」后出现多选 |
| 邮箱（`kfEmail`） | `email` | 用户填 | 常显 |
| 手机号（`kfPhone`） | `phone`（E.164，如 `+122****4444`） | 用户填 | 常显 |
| 证件类型 / 号码 / 有效期 / 正反面（`kfIdType` / `kfIdNo` / `kfIdExp` / `kfIdFront` / `kfIdBack`） | `identifying_information[0]{type, number, expiration, image_front, image_back}` | 用户填 | 常显；`type` 145 类随国家切换 |
| 人脸自拍（`kfSelfieCell` / `kfSelfie`） | `liveness_check_selfies[].image` | 用户填 | **非 EEA**；EEA 改走 `selfieHost`（M11-2） |
| 托管核验入口（`selfieHost`） | 经 KYC Link / Persona 托管流程回传 | 平台发起 | EEA in-scope（M11-2） |
| 美国证件照核验入口（`usPhotoHost`） | 同上（Persona 托管） | 平台发起 | 居住国 = USA（M11-9） |
| 居住国（`kfRes`） | `residential_address.country`（alpha-3） | 系统带出，用户可改 | 常显 |
| 地址 / 地址 2 / 城市 / 州省 / 邮编（`kfAddr` / `kfAddr2` / `kfCity` / `kfState` + `kfStateReq` / `kfZip`） | `residential_address{street_line_1, street_line_2, city, subdivision(1–3 位), postal_code}` | 用户填 | 常显；`subdivision` 美国必填、`Address.state` 1–3 位；`postal_code` 不硬性必填（提示：使用邮编的国家须填写） |
| 转写地址（`kfAddrTrRow` / `kfAddrTr`） | `transliterated_residential_address` | 用户填 | 住址含非 Latin-1 字符时 |
| 住址证明上传（`kfPoa` + `kfPoaReq` / `kfPoaWhy`） | `documents[]{purposes:[proof_of_address], file}` | 用户填 | 风控 / 地址信号冲突时必需 |
| — 出生国家 / 出生城市（`kfBirthCountry` / `kfBirthCity`） | `place_of_birth{country, city}` | 系统带出，用户可改 | **E1 EEA in-scope** |
| — 国民身份号 / 税号 TIN（`kfNatId` / `kfNatIdHint` / `kfTin` / `kfTinHint`） | `identifying_information[]` 追加：国民身份号类一条 + TIN 类一条（TIN `issuing_country` = 居住国） | 用户填（类型按国带出） | **E1 EEA in-scope**（M11-1 / M11-4） |
| — 就业状态（`kfEmp`） | `employment_status` | 用户填 | **E1 EEA** 或 **R1/R2 风险**（必填且锁定） |
| — 账户主要用途（`kfPurpose` → `kfPurposeOtherRow` / `kfPurposeOther`） | `account_purpose` → `account_purpose_other` | 用户填 | **E1 EEA** 或 **R1/R2 风险**；选 `other` 时出现补充说明 |
| — 职业（`kfOccup`） | `most_recent_occupation`（职业码，拉 `GET /lists/occupation_codes`） | 用户填 | **R1/R2 风险** |
| — 资金来源（`kfSof`） | `source_of_funds` | 用户填 | **E1 EEA** 或 **R1/R2 风险**（D13：EEA 亦采集，作为 S1–S3 判定输入） |
| — 预计每月资金往来（`kfMonthly`） | `expected_monthly_payments_usd` | 用户填 | **E1 EEA** 或 **R1/R2 风险**（D13：同上） |
| — 是否代第三方持有（`kfInter`） | `acting_as_intermediary` | 用户填 | **R1/R2 风险** |
| — 风险/标注提示条（`riskNotice` / `flagNotice` / `kfMoreToggle` + 只读 `kfMoreCb`） | —（平台态） | 系统判定 | R1/R2 命中时；勾选框**只读**，用户不可关闭 |
| — 资金来源材料区块（`kfSofDocs` / `kfSofDocsWhy` + 文案键 `kfSofDocsHint`） | —（平台态判定说明） | 系统判定 | **S1–S3 任一命中**（M11-10 / M11.A）；用户不可关闭 |
| — 资金来源说明（`kfSofStatementDoc`） | `documents[]{purposes:[proof_of_source_of_funds], file}` | 用户填 | **S1**：就业状态 = 无业 **且** 资金来源 = 工资 |
| — 工资入账凭证（`kfSofSalaryDoc`） | 同上 | 用户填 | **S1**（同上） |
| — 养老金 / 退休金发放证明（`kfSofPensionDoc`） | 同上 | 用户填 | **S2**：资金来源 = 养老金 / 退休金 |
| — 资金来源证明（`kfSofProofDoc`） | 同上 | 用户填 | **S3**：预计每月资金往来 = 5 万美元及以上 |

**步骤 ④ 确认开通**
| 可见项 | 接口字段 | 归属 | 出现条件 |
| --- | --- | --- | --- |
| 确认页只读回执（含步骤 ② 签署编号） | 同步骤 ② / ③ | 只读 | 常显 |
| 服务端注入项（前端不出现） | `type=individual`、`endorsements`（建议显式 `['base']`）、`client_reference_id` | 平台注入 | 提交时 |
| 开通结果与状态 | 建档 `POST /v0/customers` → endorsement approved → `POST /v0/customers/{customerID}/virtual_accounts` | 平台发起 | 见 M2 / M3 |
| 收款账户信息（账户号 / 路由号 / 户主 / 银行名与地址 / 支持通道） | VA 出参 `source_deposit_instructions`（附录 C） | 只读（来自 Bridge 返回） | 账户 `activated` 后 |
