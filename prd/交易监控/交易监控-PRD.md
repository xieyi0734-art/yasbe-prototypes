# 交易监控 PRD

版本：v0.7 · MVP
日期：2026-11-23
端别：管理端 · 风控管理
状态：需求评审稿；Excel/API 文档核对已完成，生产配置、平台字段映射与真实接口待联调。

## 1. 范围

成功交易事后监控：平台负责交易上送核对及 CA 案件同步查看，案件调查与处理统一在 CA 完成。

| 业务 | 纳入 | 排除／约束 |
| --- | --- | --- |
| Crypto Wallet | 成功链上入金、出金；监控金额与笔数异常 | 失败、处理中及内部划转不计入 |
| VA | OpenPayd EUR／GBP 成功入金、出金；监控金额与笔数异常 | 不含 USD／Bridge |
| Card | 充值、Card 转 Crypto Wallet；关注充值后快速转出 | 不含开卡、消费、拒付、ATM；消费沿用 Interlace 监控。成功节点及规则待确认 |

Card 转 Wallet 只算一次内部转移，不重复计为链上入金。本期不开发规则编辑器、本地案件处理或人工补录；不展示平台操作日志。监控结论不触发放行、拒绝、冻结、退款或冲正，地址筛查独立于本模块。

依据：[CA Scoping Sheet](https://docs.google.com/spreadsheets/d/1v-cyQqa2HzML41J86wssPyUMF9cIAkopHmKNVMBJITA/edit?gid=1002527305#gid=1002527305)；优先本地 Excel，缺项补 Mesh API，详见第 6 节。资料快照不代表生产配置。

[原型目录](../../prototypes/交易监控/index.html)：仅虚构演示，不连接 CA。Card 快速转出样例只展示证据时间线，尚无真实案件，不开放同步；演示控制区不进入正式产品。

## 2. 规则口径

| 表内规则 | 来源 | 本次需求表达 |
| --- | --- | --- |
| RL_0013 / RL_0014 单笔出／入金额 | 第 8–9 行 | 保留方向、原币金额、折算金额与币种、阈值。表内为 `> 100,000`，不能擅自解释成 USD 或 USDT |
| RL_0015 入金笔数 | 第 10–12 行 | 分别按 BANK_PAYMENT、CARD_PAYMENT、CRYPTO 过滤，按 `{customer_identifier.id, type}` 统计入金。表内 7 calendar_days、`> 3` |
| RL_0016 出金笔数 | 第 13–15 行 | 同上，方向 OUTBOUND；入／出不可混计 |
| RL_0017 入金累计金额 | 第 16–18 行 | 按客户＋type 统计 `base_value.amount`；表内 7 calendar_days、`> 100,000` |
| RL_0018 出金累计金额 | 第 19–21 行 | 同上，方向 OUTBOUND |
| 余额比例、余额上限、首次交易等其他规则 | 第 7、22–25 行等 | 仅作为供应商规则资料，不自动新增本期需求 |


- 按 `{customer_identifier.id, type}` 区分客户与业务类型，入／出分别统计；不同规则实例不得仅按 RL 编号合并。
- 展示业务、统计对象、方向、窗口、阈值、实际值。命中实际值与窗口使用上游当时证据，缺失显示“暂未获取”。
- `7 calendar_days` 不擅自改为滚动 168 小时；时区、窗口边界、当前交易是否计入及生产阈值待确认。
- 原币、折算币种／金额、汇率及汇率时间分别保留；不混加 USD／USDT、EUR／GBP。100,000 的币种待确认。
- Allow 不触发平台放行；P7 - Low 不映射为地址风险等级。Card 金额／笔数配置不自动扩展本期范围；快速转出需确认组合规则能力。
- 非本期 RL_0020 存在 730／30 天资料冲突，不自行采用。

## 3. 主流程

1. 成功交易 → 创建上送任务 → CA 受理与评估。业务成功、上送成功、评估完成、形成案件为独立状态。
2. 接收 CASE_CREATED → 按稳定标识查询并入库案件、规则与关联交易；多规则／多交易不得仅按客户拼案。
3. 人员在 CA 调查处理 → CASE_TRANSITIONED 触发详情及记录查询；定时查询、手动同步补齐遗漏和单独新增的备注。
4. 同步成功更新快照；失败保留上次内容与成功时间，允许重试；无法取回的信息显示“暂未获取”。

## 4. 页面需求

### 4.1 [案件列表](../../prototypes/交易监控/2026-11-19_案件列表_管理端.html)

- 统计：全部案件、CA 调查中、CA 已结案、同步失败。按最近成功快照及真实账户阶段映射统计，生产不计入拟议样例。
- 筛选：案件号／客户 UID、业务、CA 阶段、同步情况、规则、创建日期；支持重置、分页、空结果。信息缺失标记独立于同步状态。
- 列：Case ID、客户 UID、业务、规则、关联交易数、CA 阶段、同步情况／最近成功同步时间、创建时间、查看。

### 4.2 [案件详情](../../prototypes/交易监控/2026-11-19_案件详情_管理端.html?id=CASE-DEMO-001)

- 展示：概况、CA 阶段／负责人／更新时间、同步情况／成功时间、处理结果、命中原因、关联交易、CA 处理记录。
- 案件信息只读；无领取、我的待办、调查、结案、升级、分配、补录入口及平台操作日志模块。
- 阶段显示 `stage.display_name`，保留标识、类型、决策类型。无处理结果显示“尚无处理结果”，无法获取显示“暂未获取”；不凭 POSITIVE/NEGATIVE 推导结论或监管报送结果。
- “同步 CA 信息”只读查询；执行中禁止重复点击，失败可重试，刷新／中断后可恢复，不永久停留同步中。

### 4.3 [监控交易记录](../../prototypes/交易监控/2026-11-19_监控交易记录_管理端.html)

- 覆盖全部纳入监控的交易，包括未产生案件者。统计：纳入监控、已上送、待上送（含上送中）、上送失败。
- 筛选：客户 UID／平台交易号、业务、事件、上送状态、成功日期；支持重置、分页。
- 列：成功时间、平台交易号、客户 UID、业务／事件、原始金额与币种、业务状态、上送状态、关联 Case、详情／补送。
- 详情：原币及折算字段、网络、真实 CA 受理编号、补送记录；Bank／Card 网络显示“不适用”。
- 状态：待上送 → 上送中 → 已上送／上送失败。“已上送”仅代表确认受理。
- 补送前用原交易标识核查：已受理仅修正状态；确认未受理才复用原标识补送；未知则保持失败并记录核查。执行中禁止重复补送，演示结果选择框不进入正式流程。

## 5. 权限与异常

- 查看、手动同步、交易补送分别授权；后端校验权限及租户／客户隔离。不接 CA 分配、阶段写入或备注写入接口。
- 查询读取全部分页，按稳定标识去重；通知重复／乱序及并发查询不得重复建案或回退新快照，以 CA 更新时间控制更新。
- 同步失败不改变交易状态、不清空快照、不写成功时间；正常空记录不等于信息缺失或已结案。案件不存在／无权访问按系统规范提示。
- 后端审计保留同步、核查、补送的触发方式、结果、错误、时间及操作者；不记录敏感凭据或完整鉴权头。
- 取舍：案件统一在 CA 处理，平台存在同步延迟；真实账号权限、通知投递、完整字段与失败恢复须联调。

## 6. 字段核对：Excel 优先，API 补缺

优先依据 `Apex Markets Inc _ Mesh TM Scoping Sheet.xlsx`；交易字段读取 `3.1 Bank_Payments_Schema`（B）、`3.2 Card_Payments_Schema`（C）、`3.4 Crypto_Payments_Schema`（X）列 D（API Field Name），规则读取 `4. Scenarios`。不混用标记 OLD 的工作表，不把 F 列 Protobuf 简写直接当 JSON 路径。下表行号均为 Excel 实际行号。

| 页面／业务字段 | Excel 中的 API 路径或口径 | 来源行 B / C / X | 展示与使用 |
| --- | --- | --- | --- |
| CA 交易标识 | `-` | 3 / 3 / 3 | H 列说明为 CA assigned tx_ID；只读保存真实返回，不生成伪编号。 |
| CA 客户内部标识 | `transaction.customer_identifier` | 4 / 4 / 4 | CA 生成、只读；不能直接填平台 UID。 |
| 资金方向 | `transaction.details.direction` | 5 / 5 / 5 | CA 计算、只读；Bank/Crypto 根据客户作为 debtor/creditor 推导，Card 根据 payment_stage 推导。 |
| 业务类型 | `transaction.details.type` | 10 / 11 / 8 | BANK_PAYMENT / CARD_PAYMENT / CRYPTO；平台业务名只作展示映射。 |
| 平台交易号 | `transaction.external_identifier` | 11 / 12 / 9 | 使用稳定外部交易标识，重试复用；平台原始字段名仍需开发映射。 |
| 客户 UID 关联 | `transaction.customer_external_identifier` | 12 / 13 / 10 | 使用与 CA 客户创建一致的外部标识映射，保留平台 UID 与 CA 内部标识关系。 |
| 交易发生时间 | `transaction.occurred_at` | 13 / 14 / 11 | 平台保留成功时间；上送发生时间按事件定义，不能把两者未经确认直接视为相同。 |
| 折算金额 | `transaction.details.base_value.amount` | 16 / 17 / 14 | Excel 标 Yes；基准币和折算来源未确认时不填零，不默认用原币代替。 |
| 折算法币币种 | `transaction.details.base_value.currency` | 20 / 21 / 18 | Conditional；加密资产另用 crypto_asset，不能把 USDT 当 ISO 法币。 |
| 原币金额 | `transaction.details.local_value.amount` | 21 / 22 / 19 | Conditional；按 Excel local_value 保留，页面原业务金额不得丢失。 |
| 原币法币币种 | `transaction.details.local_value.currency` | 25 / 26 / 23 | Conditional；加密币保留 local_value.crypto_asset 标识与 symbol，不假造法币代码。 |
| 链网络 | `transaction.details.chain.network_name`、`network_type` | — / — / 113–114 | X113 可选名称，X114 必填类型；Bank/Card 显示不适用。 |
| 原币加密资产 | `transaction.details.local_value.crypto_asset.identifier.namespace`、`reference`、`symbol` | 22–24 / 23–25 / 20–22 | 标识按条件提供，symbol 仅展示，不能取代资产唯一标识。 |
| 折算加密资产 | `transaction.details.base_value.crypto_asset.identifier.namespace`、`reference`、`symbol` | 17–19 / 18–20 / 15–17 | 与法币 currency 按资产口径选用，不把 USD 与 USDT 混同。 |
| 规则编号、名称、方向、阈值、优先级 | `4. Scenarios` 第 8–21 行 | 规则表 | RL_0013–0018；7 calendar_days、>3、>100,000、Allow、P7 - Low 依表保留；未确认生产启用。 |
| 统计对象 | `{customer_identifier.id, type}` | 规则表第 10–21 行 | 这是规则引擎表达式；不能用平台 UID 直接替代 CA 内部客户标识，也不跨类型汇总。 |

规则阈值来自 Excel 配置；命中实际值、准确窗口起止应来自命中当时的上游证据。不能用当前关联交易条数或自行减 7 天替代真实命中快照。原型数值明确为虚构样例，未提供真实值时显示“暂未获取”。

Excel 未定义案件操作与风险查询返回，以下补充依据 Mesh API OpenAPI v2.0（服务地址 `https://api.mesh.complyadvantage.com`，本次核对本地保存的 `ca-openapi.json`，未验证在线最新版本）。

| 页面字段／动作 | 补充 API 来源 | 映射与缺失处理 |
| --- | --- | --- |
| 案件号、创建／更新时间、阶段、负责人 | GET `/v2/cases/{case_identifier}`：`identifier`、`created_at`、`updated_at`、`stage`、`assignee` | 阶段显示 `stage.display_name`，保留阶段标识／类型／决策类型；负责人只读，未解析 CA 用户名时保留标识，不编造姓名。 |
| 阶段变更通知 | POST `/v2/notifications/configurations/webhook`，订阅 `CASE_TRANSITIONED` | CA 阶段变化通知后查询详情与记录；`CASE_STATE_UPDATED` 已弃用。配置权限和实际投递待联调，不承诺实时送达。 |
| 新案件通知 | 同一 Webhook 配置接口，订阅 `CASE_CREATED` | 根据稳定案件标识查询及入库，重复通知不重复建案；生产权限与重试机制待联调。 |
| CA 处理记录 | GET `/v2/cases/{case_identifier}/notes`：`identifier`、`contents`、`created_at`、`created_by`、`type` | 分页读取，按 identifier 去重；type 包含 CASE / CASE_ASSIGNMENT / CASE_TRANSITION。时间是记录创建时间，不直接当结案时间；本平台不 POST 备注。 |
| 告警与风险关联 | GET `/v2/cases/{case_identifier}/alerts`；GET `/v2/alerts/{alert_identifier}/risks` | 从案件关联告警再取风险，不能只按客户拼案，不能用 RL 编号冒充风险标识。 |
| 命中说明 | GET `/v2/transaction-monitoring/risks/{risk_identifier}`；`transaction_ScenarioObservationResponse.configuration/observation` | 按实际返回解释风险；不假造统一 actual/threshold/window 响应字段，缺值展示暂未获取。 |
| 关联交易、关联类型、证据状态 | GET `/v2/transaction-monitoring/alerts/{alert_identifier}/related-transactions`：`related_transactions[].identifier/type/status/version/occurred_at` | type 为 ALERTING / CONTEXTUAL；status 为 UP_TO_DATE / UPDATED / OUTDATED，不是业务成功状态。取回所有分页后统计去重交易数。 |
| 评估结果 | `ol_EvaluationResultDTO.outcome`、`scenario_evaluations` | 受理成功不代表评估完成；ALLOW 不证明没有案件，不能触发资金放行。 |
| 按外部交易标识核查 | GET `/v3/transactions/external/{identifier}` | 用原外部交易标识核查，返回未完成或未知时不盲补；生产幂等及一致性窗口仍需联调。 |
| 工作流映射 | GET `/v2/cases/workflows` 及 workflow/version 详情 | 读取实际配置确定阶段展示和统计映射，不设置本地目标阶段，不硬编码演示中文状态。 |

平台自有字段：业务事件、成功状态／成功时间、CA 上送任务状态、补送次数、案件同步状态、最近成功同步时间、处理信息缺失标记／原因、客户 UID。上述字段不声称由 CA 提供；CA 处理结果按真实阶段和记录展示，不假造统一 result 字段。

核对边界：Excel 的类型、路径、方向和规则已逐项核对；平台数据源到 Excel 空白 Inbound/Outbound 栏的具体字段名、基准币、实际账户阶段及 Card 充值／转 Wallet 的 payment_stage 尚需联调确认。未确认项不填推测值。

## 7. 验收标准

| 编号 | 验收场景 | 预期 |
| --- | --- | --- |
| A1 | Crypto 失败或处理中交易、USD／Bridge VA、Card 消费进入事件源 | 不被本期成功交易监控误纳入 |
| A2 | 同一客户同时有 Bank 与 Crypto 入金 | 各 type 独立统计，不跨业务拼成笔数／金额告警 |
| A3 | 存在不同原币交易 | 原币分别展示；没有确认的折算依据不直接合计 |
| A4 | 按业务、CA 阶段、同步情况、客户和日期查案件／交易 | 查询、分页、重置、空结果正确，日期错误提示修正 |
| A5 | 打开案件列表及详情 | 不存在领取、我的待办、开始调查、结案、升级和人员分配操作 |
| A6 | CA 阶段变更并同步 | 更新 CA 阶段、更新时间及处理记录，不执行本平台阶段写入 |
| A7 | 无法获取处理信息 | 显示暂未获取，保留同步入口 |
| A8 | 查看案件详情 | 不展示人工补录记录和平台操作日志模块，无补录入口 |
| A9 | 上送超时，CA 实际已受理 | 核查后修正状态，不重复上送或重复统计 |
| A10 | 确认 CA 未受理后补送 | 原标识复用，交易记录总数不增加；未知结果不盲补 |
| A11 | Card 转 Wallet | 不重复产生链上入金；时间线保留原始币种，不伪造资金配对；拟议样例无同步入口 |
| A12 | CA 正常返回空记录或尚未处理 | 显示暂无记录，不显示已结案 |
| A13 | 暂时同步失败 | 保留上次阶段、记录及成功同步时间，提供重试 |
| A14 | 同步恢复且信息完整 | 展示最新 CA 信息，解除信息缺失标记 |
| A15 | 同步中刷新或断网 | 不永久停留同步中，恢复后允许重试；未完成时不写成功时间 |
| A16 | 重复／乱序通知、重复手动同步与分页 | 不重复建案、不重复记录、不回退新快照 |
| A17 | 无同步权限或跨租户访问 | 后端拒绝越权，不靠按钮隐藏保证安全 |
| A18 | Excel/API 来源核对 | 保留字段标明来源，平台字段与 CA 字段分开，未确认值不伪造 |


原型验证页面与模拟交互；Webhook、真实权限、并发防重和 CA 数据同步须通过服务联调。

## 8. 待确认项

| 编号 | 状态 | 问题 | 影响 |
| --- | --- | --- | --- |
| N1 | 待确认 | 7 自然日与阈值 3／100,000 是否用于生产；各类型是否不同 | CA 配置和验收用例 |
| N2 | 待确认 | 基准币、折算来源、汇率时间、统计窗口时区与边界 | 金额可比性与命中解释 |
| N3 | 待确认 | Card 充值来源、入／出方向与成功节点 | 事件映射与纳入时机 |
| N4 | 待确认 | Card 快速转出时间窗、金额／比例、配对方法及 CA 实现能力 | 规则实现；不采用样例的 8 分钟作为阈值 |
| N5 | 读取／通知能力有文档依据，接入待验证；结论回写已作废 | CA 上送幂等、受理查询、案件详情／记录读取、CASE_CREATED／CASE_TRANSITIONED 投递 | 核实实际账号权限、完整字段及失败恢复；不接案件写接口 |
| N6 | 旧本地人员处理流程已作废；展示映射待验证 | CA 负责调查与处理，本平台只读阶段及负责人 | 核实实际阶段／用户展示映射和信息缺失判定 |
| N7 | 待确认 | 多规则聚案、多交易关联、租户和客户映射 | 去重、统计隔离与案件解释 |
| N8 | 待确认 | 重试策略、保留期限、SLA 与异常通知 | 生产运营保障 |

已确认：D1 本期范围见第 1 节；D2 按客户＋业务类型统计；D3 案件在 CA 处理，平台只读同步，移除人工补录及平台操作日志展示。

## 修订历史

| 版本 | 日期 | 修改内容 |
| --- | --- | --- |
| v0.7 | 2026-11-23 | 精简重复说明，合并页面、流程与异常要求；保留字段映射、验收及待确认项 |
| v0.6 | 2026-11-23 | 删除人工补录记录、补录入口及平台操作日志展示 |
| v0.5 | 2026-11-23 | 改为 CA 处理、平台只读同步；删除领取／本地结案升级及草稿；新增独立人工补录、同步失败恢复；同步更新接口来源、权限、验收和 D3/N5/N6 |
| v0.4 | 2026-11-23 | 收敛 MVP 单角色流程；取消本地多级复核与转派；按 Excel 优先、API 补缺添加字段映射；补刷新中断及核查恢复 |
| v0.3 | 2026-11-23 | 补齐初审、升级接收、合规复核、退回补充、最终结案和同角色转派；统一负责人、权限、失败恢复及验收；关闭 N6 业务流程缺口，保留 CA 接入验证 |
| v0.1 | 2026-11-19 | 建立范围、规则依据、三页交互、字段要求、案件与上送状态、验收和待确认项；区分表内配置与生产决策 |
