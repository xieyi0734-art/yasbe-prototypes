# YASBe 原型链接总览

> 所有原型统一部署在 GitHub Pages：`https://xieyi0734-art.github.io/yasbe-prototypes/`
> 更新时间 = 该文件最后一次 git 提交时间（未提交文件取文件修改时间）
> 维护规则：**新增原型后必须在此登记**（名称 / 功能 / 更新时间 / 链接）

---

## 0. 原型命名与存放规范（2026-09-10 起）

> 新建原型必须遵守。**2026-09-10 已按本规范把「返佣与奖励」相关 8 个原型从 `admin/prototypes/distribution`、`admin/prototypes/card-type`、`client/prototypes/card-apply`、`client/prototypes/card-management` 统一归集到 `prototypes/返佣和奖励/`**（详见第 8 节）；**其余存量文件不动**。

- **命名格式**：`YYYY-MM-DD_<业务>_<端别>.html`
  - 例：`2026-09-10_卡种维度奖励配置_管理端.html`
  - 例：`2026-09-10_开卡返佣记录_客户端.html`
  - 端别取值：`管理端` / `客户端` / `B端` / `代币官网`
- **存放位置**：全部统一收在**仓库根 `prototypes/`** 一个目录下 ——
  - **文件夹按「需求」划分，文件夹名不含端别**（例：`prototypes/返佣和奖励/`）；同需求的管理端 / 客户端 / B 端原型放同一文件夹，不再按端别拆目录
  - **原型文件名区分端别**（`管理端` / `客户端` / `B端` / `代币官网`）
  - 时间维度由文件名的 `YYYY-MM-DD` 前缀承载，同文件夹内按文件名排序即为时间序
- **登记**：新增后在本文件对应业务分组登记（原型名称 / 功能 / 最后更新 / 链接）
- **存量为何不动**：改名会打断大量内部 `.html` 互链，且 GitHub Pages 上已部署的旧路径会 404。除本次「返佣与奖励」8 个原型外，旧文件继续留在 `admin/prototypes/*`、`client/prototypes/*`
- **本次迁移的内链处理**：移动文件的相对链接已按新位置重新相对化（含指向未移动文件 `08-Card-Type-Management.html` 的链接）；反向引用 `admin/prototypes/index.html`、根 `index.html` 已同步更新

---

## 1. 🛠️ 管理端 · Card 模块（admin/prototypes/）

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| 卡务管理（卡类型） | 卡产品类型管理（08） | 2026-08-10 | [08-Card-Type-Management.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/card-type/08-Card-Type-Management.html) |
| 卡片管理 | 卡片列表管理（03） | 2026-07-08 | [03-Card-Management.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/card-management/03-Card-Management.html) |
| 卡片详情 | 单卡详情（02） | 2026-07-08 | [02-Card-Detail.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/card-management/02-Card-Detail.html) |
| 卡片介绍 | 卡片产品介绍页（12） | 2026-07-08 | [12-Card-Introduction.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/card-intro/12-Card-Introduction.html) |
| 卡片介绍（旧版） | 早期卡片介绍页 | 2026-07-08 | [CardIntroduction.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/card-intro/CardIntroduction.html) |
| 卡片介绍 v5 | 旧版卡片介绍（v5） | 2026-07-08 | [CardIntroduction_v5.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/card-intro/CardIntroduction_v5.html) |
| 渠道管理 | 发卡渠道管理（07） | 2026-07-08 | [07-Channel-Management.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/channel/07-Channel-Management.html) |
| 我的资料 | 客户资料弹窗（11） | 2026-07-08 | [11-Client-Profile-Modal.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/client-profile/11-Client-Profile-Modal.html) |
| 加密货币归集设置 | Crypto 归集配置（19） | 2026-07-08 | [19-Crypto-Collection-Settings.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/crypto/19-Crypto-Collection-Settings.html) |
| 客户详情 · 卡片 Tab | 客户卡片视图（01） | 2026-07-08 | [01-Customer-Detail-Cards-Tab.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/customer/01-Customer-Detail-Cards-Tab.html) |
| 客户详情 · 法币 Tab | 客户法币账户 + 出入金记录 | 2026-09-08 | [02-Customer-Detail-Fiat-Tab.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/customer/02-Customer-Detail-Fiat-Tab.html) |
| 客户详情 · 推荐 Tab | 客户推荐视图（10） | 2026-07-08 | [10-Customer-Detail-Referrals-Tab.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/customer/10-Customer-Detail-Referrals-Tab.html) |
| 客户详情 · 推荐 Tab v2 | 推荐视图（代理版） | 2026-08-03 | [10-Customer-Detail-Referrals-Tab-v2.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/customer/10-Customer-Detail-Referrals-Tab-v2.html) |
| 法币 · 交易审核 | 三队列:入金非同名挂账复核 / 出金同名已核验受益人终审 / EA 非同名添加审核(同意=创建成功·仅入金来源,驳回=失败) | 2026-09-08 | [01-Fiat-Review-Queue.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/fiat/01-Fiat-Review-Queue.html) |
| 法币 · 交易记录 | 出入金全量流水（10 列 + Review 入口） | 2026-09-08 | [02-Fiat-Transaction-List.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/fiat/02-Fiat-Transaction-List.html) |
| 法币 · 资金总览 | 平台级资金视图（逐币种对账闭环） | 2026-09-08 | [03-Fiat-Treasury-Overview.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/fiat/03-Fiat-Treasury-Overview.html) |
| 法币 · 收款账户 | 平台收款账户 + 上游 KYB | 2026-09-08 | [04-Fiat-Bank-Accounts.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/fiat/04-Fiat-Bank-Accounts.html) |
| 法币 · 币种设置 | 币种费率两档（≤50k / >50k） | 2026-09-08 | [05-Fiat-Currency-Settings.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/fiat/05-Fiat-Currency-Settings.html) |
| 风控规则管理 | 风控规则配置（01） | 2026-07-08 | [01-Risk-Rule-Management.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/risk-control/01-Risk-Rule-Management.html) |
| 风控事件列表 | 风控事件（02） | 2026-07-08 | [02-Risk-Event-List.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/risk-control/02-Risk-Event-List.html) |
| 卡片交易流水 | 交易流水列表（17） | 2026-07-08 | [17-Card-Transaction-List.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/transaction/17-Card-Transaction-List.html) |
| 交易审核 | 交易审核快照（18） | 2026-07-08 | [18-Card-Transaction-Review.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/transaction/18-Card-Transaction-Review.html) |
| KYC 审核详情 v1 | KYC 审核（旧版） | 2026-07-08 | [03-KYC-ReviewDetail-v1.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/verification/03-KYC-ReviewDetail-v1.html) |
| KYC 审核详情 (CA) | KYC 审核 + ComplyAdvantage 命中抽屉 | 2026-08-11 | [04-KYC-ReviewDetail-CA.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/verification/04-KYC-ReviewDetail-CA.html) |
| KYB 审核详情 (CA) | KYB 审核 + ComplyAdvantage 命中抽屉 | 2026-08-11 | [05-KYB-ReviewDetail-CA.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/verification/05-KYB-ReviewDetail-CA.html) |
| ComplyAdvantage 案件 | CA 风险案件列表（06） | 2026-08-11 | [06-ComplyAdvantage-Cases.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/verification/06-ComplyAdvantage-Cases.html) |
| 管理端原型总览 | Card 模块导航首页 | 2026-07-08 | [index.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/index.html) |

## 2. 📱 C 端 · Card 模块（client/prototypes/）

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| 卡片激活弹窗 | 激活流程弹窗 | 2026-07-21 | [01-Card-Activation-Modals.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/card-activation/01-Card-Activation-Modals.html) |
| 实体卡申请 · 收件信息 | 实体卡申请配送弹窗 | 2026-07-21 | [17-Card-Apply-Shipping-Modal.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/card-apply/17-Card-Apply-Shipping-Modal.html) |
| 卡片管理 v6 | C 端卡片管理（MoR PRD v3.1） | 2026-07-08 | [12-卡片管理-v6.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/card-management/12-卡片管理-v6.html) |
| B 端卡片管理 | B 端卡片管理（21） | 2026-07-24 | [21-B端-卡片管理.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/card-management/21-B端-卡片管理.html) |
| 卡片详情 | C 端单卡详情（33） | 2026-07-24 | [33-卡片详情.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/card-management/33-卡片详情.html) |
| 卡账户总览 v2 | 账户总览 + 交易列表 | 2026-07-08 | [01-Card-Account-Overview-v2.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/card-overview/01-Card-Account-Overview-v2.html) |
| 卡账交易列表 | 卡账交易流水 | 2026-07-08 | [01-Card-Accounting-Transaction-List.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/card-overview/01-Card-Accounting-Transaction-List.html) |
| 交易快照 | 卡片交易快照 | 2026-07-08 | [card-transaction-snapshot.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/card-overview/card-transaction-snapshot.html) |
| 费用管理 v2 | 费用/费率管理 | 2026-07-08 | [02-Fee-Management-v2.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/fee-billing/02-Fee-Management-v2.html) |
| 费用结算 | 结算页面（21） | 2026-07-08 | [21-费用结算.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/fee-billing/21-费用结算.html) |
| 账单管理 | 账单页（22） | 2026-07-08 | [22-账单管理.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/fee-billing/22-账单管理.html) |
| KYC 认证已暂停 | KYC 暂停状态页 | 2026-07-08 | [01-KYC-Suspended-v1.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/kyc/01-KYC-Suspended-v1.html) |
| KYC 信息更新 | 更新资料（Scenario B） | 2026-07-08 | [02-KYC-SelfUpdate-ScenarioB-v1.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/kyc/02-KYC-SelfUpdate-ScenarioB-v1.html) |
| C 端原型导航 | Card 模块导航首页 | 2026-07-08 | [index.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/index.html) |
| 账务模块导航 | 账务原型导航 | 2026-07-08 | [index-账务管理.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/index-账务管理.html) |

## 3. 💳 卡片 C 端独立版（card-prototypes/）

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| 卡片管理 | 卡片列表（独立版） | 2026-07-18 | [index.html](https://xieyi0734-art.github.io/yasbe-prototypes/card-prototypes/index.html) |
| 卡片详情 | 单卡详情 | 2026-07-15 | [card-detail.html](https://xieyi0734-art.github.io/yasbe-prototypes/card-prototypes/card-detail.html) |
| 激活卡片 | 激活流程 | 2026-07-15 | [activate.html](https://xieyi0734-art.github.io/yasbe-prototypes/card-prototypes/activate.html) |
| 冻结/解冻/注销 | 卡片操作 | 2026-07-15 | [operations.html](https://xieyi0734-art.github.io/yasbe-prototypes/card-prototypes/operations.html) |
| 卡片账单 | 账单列表 | 2026-07-15 | [bills.html](https://xieyi0734-art.github.io/yasbe-prototypes/card-prototypes/bills.html) |

## 4. 📄 早期原型（prototypes/）

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| Dashboard v4 | 管理端仪表盘 | 2026-07-24 | [Dashboard.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Dashboard.html) |
| Dashboard v4 中文 | 仪表盘中文版 | 2026-07-28 | [Dashboard-Chinese.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Dashboard-Chinese.html) |
| Dashboard v4 New | 仪表盘新版 | 2026-07-28 | [Dashboard-New.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Dashboard-New.html) |
| Dashboard v5 | 仪表盘 v5 | 2026-07-24 | [Dashboard-v5.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Dashboard-v5.html) |
| Dashboard 表格版 | 仪表盘表格布局版 | 2026-07-24 | [Dashboard-New_tables.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Dashboard-New_tables.html) |
| 客户端登录 | 登录页 | 2026-07-08 | [Login-Client.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Login-Client.html) |
| 账单（C 端） | 对账单/Statement | 2026-07-08 | [Billing-Client.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Billing-Client.html) |
| 对账单 | Statement 页面 | 2026-07-08 | [Statement-Client.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Statement-Client.html) |
| 兑换确认 + 2FA | Exchange 确认弹窗 | 2026-07-08 | [Exchange-Confirm-2FA.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Exchange-Confirm-2FA.html) |
| 兑换确认 2FA 合并 | 兑换确认+2FA 合并版 | 2026-07-08 | [Confirm-Conversion-2FA.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Confirm-Conversion-2FA.html) |
| 出金 2FA · Crypto | 提币 2FA 弹窗 | 2026-07-08 | [Withdraw-2FA-Crypto.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Withdraw-2FA-Crypto.html) |
| 出金 2FA · Fiat | 法币出金 Review + 2FA | 2026-07-08 | [Withdraw-2FA-Fiat.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Withdraw-2FA-Fiat.html) |
| 安全设置 · 2FA 绑定 | 2FA 绑定页 | 2026-07-08 | [Security-2FA-Setup.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Security-2FA-Setup.html) |
| 博客管理 | Blog 后台 | 2026-07-08 | [Blog-Management.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Blog-Management.html) |
| FAQ 管理 | FAQ 后台 | 2026-07-08 | [FAQ-Management.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/FAQ-Management.html) |
| 新闻管理 | News 后台 | 2026-07-08 | [News-Management.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/News-Management.html) |
| FAQ 官网 | 官网 FAQ 页 | 2026-07-08 | [FAQ-Website.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/FAQ-Website.html) |
| 风控规则管理 | 风控规则（早期版） | 2026-07-08 | [RiskRule-Management.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/RiskRule-Management.html) |
| 加密对账流程 | Crypto 对账业务流 | 2026-07-08 | [crypto-reconciliation-flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/crypto-reconciliation-flow.html) |
| 费用中心架构 | 费用中心架构图 | 2026-07-24 | [Fee-Center-Architecture.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Fee-Center-Architecture.html) |
| Mesh 接入业务流程 v2 | ComplyAdvantage 接入流程图 | 2026-08-03 | [Mesh-Integration-Business-Flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Mesh-Integration-Business-Flow.html) |
| 白标客户业务流程 | 白标业务流程图 | 2026-07-24 | [White-Label-Business-Flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/White-Label-Business-Flow.html) |
| 白标 MVP 流程 | 白标 MVP 流程图 | 2026-07-24 | [White-Label-MVP-Business-Flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/White-Label-MVP-Business-Flow.html) |

## 5. 🔀 流程图（diagrams/）

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| ComplyAdvantage 风控接入流程 | 筛查→评分→风险等级流程图 | 2026-08-05 | [comply-advantage-risk-flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/comply-advantage-risk-flow.html) |
| 代理返佣业务流程 | 代理返佣流程图 | 2026-07-24 | [agent-rebate-flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/agent-rebate-flow.html) |
| B 端用户操作流程 | B 端操作流程图 | 2026-07-24 | [b端用户操作流程.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/b端用户操作流程.html) |
| 卡片账务功能架构 | 管理端卡片账务架构图 | 2026-07-08 | [card-accounting-architecture.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/card-accounting-architecture.html) |
| 卡片激活流程 | Region 4 激活流程 | 2026-07-24 | [card-activation-flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/card-activation-flow.html) |
| 实体卡开卡完整流程 | 开卡全流程 | 2026-07-24 | [card-full-flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/card-full-flow.html) |
| 实体卡开卡流程 | 开卡流程（版2） | 2026-07-24 | [card-issue-flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/card-issue-flow.html) |
| Card 账务功能架构 v3.0 | 账务模块架构图 | 2026-07-08 | [Card模块账务_v3.0_功能架构图.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/Card模块账务_v3.0_功能架构图.html) |
| 分模块 KYB 流程 | KYB 认证流程图 | 2026-07-08 | [module-based-kyb-flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/module-based-kyb-flow.html) |
| 模块化 KYC 流程 | KYC 认证流程图 | 2026-07-08 | [module-based-kyc-flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/module-based-kyc-flow.html) |
| KYC/KYB Re-review 流程 | 平台重审流程图 | 2026-07-08 | [platform-kyc-kyb-review-flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/platform-kyc-kyb-review-flow.html) |
| YASBee 账务功能架构 | 卡片账务架构图 | 2026-07-08 | [YASBee-账务功能架构图.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/YASBee-账务功能架构图.html) |

## 6. 🪙 CYRO 代币官网（cyro-website/）

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| 官网首页 | CYRO PayFi Token 品牌页 | 2026-07-27 | [index.html](https://xieyi0734-art.github.io/yasbe-prototypes/cyro-website/index.html) |
| 登录 | Sign In | 2026-07-27 | [signin.html](https://xieyi0734-art.github.io/yasbe-prototypes/cyro-website/signin.html) |
| 注册 | Get Started | 2026-07-27 | [signup.html](https://xieyi0734-art.github.io/yasbe-prototypes/cyro-website/signup.html) |
| 充值 | Deposit | 2026-07-27 | [deposit.html](https://xieyi0734-art.github.io/yasbe-prototypes/cyro-website/deposit.html) |
| 提现 | Withdraw | 2026-07-27 | [withdraw.html](https://xieyi0734-art.github.io/yasbe-prototypes/cyro-website/withdraw.html) |
| 交易记录 | Transactions | 2026-07-27 | [transactions.html](https://xieyi0734-art.github.io/yasbe-prototypes/cyro-website/transactions.html) |
| 管理端 | CYRO Admin Dashboard | 2026-07-27 | [admin.html](https://xieyi0734-art.github.io/yasbe-prototypes/cyro-website/admin.html) |
| 管理端 · 网络 | Networks 配置 | 2026-07-27 | [admin-chains.html](https://xieyi0734-art.github.io/yasbe-prototypes/cyro-website/admin-chains.html) |
| 管理端 · 汇率 | Token Rates 配置 | 2026-07-27 | [admin-rates.html](https://xieyi0734-art.github.io/yasbe-prototypes/cyro-website/admin-rates.html) |
| 管理端 · 交易 | Transactions 管理 | 2026-07-27 | [admin-transactions.html](https://xieyi0734-art.github.io/yasbe-prototypes/cyro-website/admin-transactions.html) |
| 管理端 · 用户 | User Management | 2026-07-27 | [admin-users.html](https://xieyi0734-art.github.io/yasbe-prototypes/cyro-website/admin-users.html) |

## 7. 📁 根目录（导航 / 旧版）

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| 项目文件导航 | 仓库导航首页 | 2026-07-08 | [index.html](https://xieyi0734-art.github.io/yasbe-prototypes/index.html) |
| CYRO 代币官网 | 单文件版品牌页 | 2026-07-24 | [cyro-token-website.html](https://xieyi0734-art.github.io/yasbe-prototypes/cyro-token-website.html) |
| 仪表盘 v4（根） | 管理端仪表盘 | 2026-07-28 | [Dashboard-Chinese.html](https://xieyi0734-art.github.io/yasbe-prototypes/Dashboard-Chinese.html) |
| 仪表盘 New（根） | 管理端仪表盘新版 | 2026-07-27 | [Dashboard-New.html](https://xieyi0734-art.github.io/yasbe-prototypes/Dashboard-New.html) |
| 出金 2FA 合并 | Withdraw 2FA 合并版 | 2026-07-08 | [Withdraw-2FA-Combined.html](https://xieyi0734-art.github.io/yasbe-prototypes/Withdraw-2FA-Combined.html) |
| 登录（根） | CYRO Sign In | 2026-07-24 | [signin.html](https://xieyi0734-art.github.io/yasbe-prototypes/signin.html) |
| 注册（根） | CYRO Sign Up | 2026-07-24 | [signup.html](https://xieyi0734-art.github.io/yasbe-prototypes/signup.html) |

## 8. 🎁 返佣与奖励（`prototypes/返佣和奖励/` · 2026-09-10 归集）

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| 分销返佣配置 | 分销返点规则配置（一级分销） | 2026-07-08 | [2026-07-08_分销返佣配置_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-07-08_分销返佣配置_管理端.html) |
| YASBee Points 奖励记录与规则设置 | 客户维度奖励场景（开卡/卡充值/币兑）+ 代理返佣设置（下级开卡/充值/币兑）+ 奖励记录 | 2026-09-10 | [2026-09-10_YASBee-Points奖励记录与规则设置_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-09-10_YASBee-Points奖励记录与规则设置_管理端.html) |
| yasbee+ 用户奖励设置 | 卡种维度奖励比例（开卡/卡充值 × 实体/虚拟） | 2026-09-10 | [2026-09-10_yasbee+用户奖励设置_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-09-10_yasbee+用户奖励设置_管理端.html) |
| 卡片代理返佣配置 | 代理配置 + 卡片返佣比例（按卡产品） | 2026-08-10 | [2026-08-10_卡片代理返佣配置_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-08-10_卡片代理返佣配置_管理端.html) |
| 返佣记录 | 待结算返佣 + 发起结算操作 | 2026-08-11 | [2026-08-11_返佣记录_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-08-11_返佣记录_管理端.html) |
| 结算记录 | 已结算台账（无结算操作） | 2026-08-10 | [2026-08-10_结算记录_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-08-10_结算记录_管理端.html) |
| Rewards · YASBee Cash & Points（C 端） | 双表：YASBee Cash（购买 / 空投赠送）+ YASBee Points（开卡 / 卡充值 / 币兑奖励） | 2026-09-09 | [2026-09-09_yasbee+奖励记录_客户端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-09-09_yasbee+奖励记录_客户端.html) |
| 代理推广与收益看板（B 端） | B 端代理推广与收益看板 | 2026-09-09 | [2026-09-09_代理推广与收益看板_B端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-09-09_代理推广与收益看板_B端.html) |

## 9. 🛡️ 加密出入金风险扫描（`prototypes/加密出入金风险扫描/` · 2026-09-11）

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| 加密出入金风险扫描 · 客户端 | Crypto Wallet（资产总览 + 资产列表 + 交易记录，深色 #FFCA00）+ 充值/提现弹窗 + 钱包风险扫描（审核中/已拒绝） | 2026-09-11 | [2026-09-11_加密出入金风险扫描_客户端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/加密出入金风险扫描/2026-09-11_加密出入金风险扫描_客户端.html) |
| 加密出入金风险扫描 · 管理端 | 加密货币 · 交易审核：入金/出金两条风控队列 + Merkle 风险明细 + 批准/拒绝处置 | 2026-09-10 | [2026-09-10_加密出入金风险扫描_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/加密出入金风险扫描/2026-09-10_加密出入金风险扫描_管理端.html) |

---

## 📌 新增原型登记模板

```
| 原型名称 | 功能一句话 | YYYY-MM-DD | [文件名.html](https://xieyi0734-art.github.io/yasbe-prototypes/相对路径/文件名.html) |
```

新增后按模块插入对应表格，并更新顶部维护规则。若链接路径变化（如改文件名），同步修正旧条目。
