# YASBe 原型链接总览

> 部署根：`https://xieyi0734-art.github.io/yasbe-prototypes/`
> **最后更新** = 该文件最后一次 git 提交日期（未提交/未入库的文件取文件修改时间）
> **维护规则**：新增原型后必须在此登记（原型名称 / 功能 / 最后更新 / 链接）
> **流程规范**：[`prototypes/README.md`](prototypes/README.md) —— 命名 / 存放 / 确认闸门 / 归档口径的唯一权威文件
> **每轮 push 前自检**：`python tools/check_registry.py --online`（命名 · 覆盖 · 一致性三闸，退出码非 0 不要 push）
> **本版（2026-10-15）**：租户业务台「工作台首页」新增平台服务开通状态区块（法币账户 / 加密货币 / 卡片）与各自统计；本租户法币已开通，加密货币与卡片未开通；首页顶部新增对外价值主张文案（加密货币 & 法币出入金解决方案 · 实时购买/持有/出售稳定币与主流币 · 企业级 MPC 加密钱包 · web3 企业一站式金融服务）；三条业务线（法币账户 / 加密货币 / 卡片）服务卡各自补卖点文案（全球账户 · 实时买卖 + MPC 钱包 · 开卡即用）；新增「通知」模块（最近通知 5 条 · 未读 3 · 深链到本模块页面）；左侧菜单底部新增 DOCS（跳白标开发者门户 API 文档首页）与 登出（二次确认弹窗）；新增「账号设置」页（修改密码 / 修改邮箱 / 身份验证器绑定与解绑 / 登录设备；卡片式——每个功能一张卡，卡片只做只读汇总，改值走弹窗），侧栏底部三项（账号设置 / DOCS / 登出）已同步到本模块全部页面；随后侧栏在新增的「设置」分组下并排 账户管理 与 账号设置、底部只留 DOCS / 登出，并新增「账户管理」页（本租户成员与角色：邀请 / 改角色 / 停用 / 移除，按 RBAC 仅管理员可见），本模块 11 个页面全部同步
> **上一版（2026-10-14）**：新增 `租户业务台` 端别与 §3 专题（9 条：MVP 8 页 + 目录页）—— BaaS 白标系统租户侧控制台首版
> **上一版（2026-09-18）**：返佣与奖励专题按新口径重铺 7 页（电子签名存证 / 自动审核 / 兜底值），该专题按排序规则升为 §5；2026-09-17 旧口径一套移入 §4-C 追溯
> **上一版（2026-09-17）**：按「端别 · 业务模块」重新整理分组，并逐条核对线上状态
> **排序规则**：业务分组按「组内最新更新时间」倒序；组内各条按更新时间倒序。命名规范与「入口与导航」两节置顶；「未部署 / 失效清单」与登记模板置底

**线上核对（2026-09-17 实测）**：登记 123 条 —— 可访问 106 条 / 失效 17 条（失效均为 `.gitignore` 排除、从未部署，清单见 §16-A）；另有本地存在但未部署 11 条（§16-B）
**二次核对（2026-09-17 · `tools/check_registry.py --online` 自动跑）**：106 条线上链接全部 HTTP 200，其中 104 条与本地字节完全一致（线上为 LF 版）；2 条不符为本地已改未推
**三次核对（2026-09-18 · 代理体系 15 页 push 后）**：登记 122 条 —— 一致 118 条 / 非 200 共 0 条 / 字节不符 3 条（均为「本地已改未推」的其他模块存量：`admin/prototypes/channel/07-Channel-Management.html`、`prototypes/加密出入金风险扫描/2026-09-11_加密出入金风险扫描_客户端.html`、`client/prototypes/card-management/21-B端-卡片管理.html`）；本次新增 15 条（§3-A 7 条 + §3-C 8 条）全部 HTTP 200 且与本地字节完全一致
**四次核对（2026-09-20 · 加密出入金风险扫描 push 后· `tools/check_registry.py --online`）**：登记 122 条 —— 一致 120 条 / 非 200 共 0 条 / 字节不符 2 条（均为其他模块「本地已改未推」存量：`admin/prototypes/channel/07-Channel-Management.html`、`client/prototypes/card-management/21-B端-卡片管理.html`）；本次新登记 1 条（§7 管理端 2026-09-14 版首次入库）、`2026-09-11_…_客户端.html` 字节不符已消除；另同步 3 份 PRD（PRD v1.4 / 需求梳理 / 验收审计 v1.3）
**五次核对（2026-09-20 · 法币虚拟账户 push 后 · `tools/check_registry.py --online`）**：登记 124 条 —— 一致 115 条 / 非 200 共 0 条 / 字节不符 9 条（全部为其他模块「本地已改未推」存量：`prototypes/返佣和奖励/` 7 页（2026-09-20 13:50 本地修改，未 push）、`admin/prototypes/channel/07-Channel-Management.html`、`client/prototypes/card-management/21-B端-卡片管理.html`）；本次新登记 2 条（§8 `01-用户开通虚拟账户.html`、`02-法币账户-多渠道多账户.html`）全部 HTTP 200 且与本地字节完全一致；另同步 2 份 PRD（虚拟账户-USD通道 v0.8 / 法币账户-欧元英镑-OpenPayd通道 v0.3）
**七次核对（2026-10-10 · VA 代理双端首次登记）**：登记 124 → 136 条 —— 本次新增 12 条（§3 `prototypes/VA代理/`：管理端 6 页 + 代理端 6 页），均为本地新增、尚未 push；本模块不新增独立客户登录端
**六次核对（2026-09-20 · 法币虚拟账户「开户最后一步」修订 push 后 · `tools/check_registry.py --online`）**：登记 124 条 —— 一致 115 条 / 非 200 共 0 条 / 字节不符 9 条（全部为其他模块「本地已改未推」存量：`prototypes/返佣和奖励/` 7 页、`admin/prototypes/channel/07-Channel-Management.html`、`client/prototypes/card-management/21-B端-卡片管理.html`）；本次修订 2 页（§8 `02-法币账户-多渠道多账户.html`：删「资金归集（平台托管）」块 + 确认页不再展示开户后才生成的收款信息 + 修 `holderAddr` 双语渲染；`03-法币账户-欧元英镑-多渠道多账户.html`：修 `holderAddr` 双语渲染）push 后线上字节与本地完全一致

本次整理动作：① 分组由「存储目录」改为「端别 · 业务模块」；② 逐条实测线上 HTTP 状态，失效链接移入 §14 不再散落各表；③ 按 git 提交记录刷新 11 条「最后更新」；④ 补登记 3 条此前遗漏的线上页面；⑤ 修复原 §13 因空行导致断层的表格；⑥ 新增 `prototypes/README.md` 流程规范与 `tools/check_registry.py` 三闸自检

---

## 1. 原型命名与存放规范（2026-09-10 起）

> 新建原型必须遵守。**2026-09-10 已按本规范把「返佣与奖励」相关 8 个原型从 `admin/prototypes/distribution`、`admin/prototypes/card-type`、`client/prototypes/card-apply`、`client/prototypes/card-management` 统一归集到 `prototypes/返佣和奖励/`**（详见 §5）；**其余存量文件不动**。

- **命名格式**：`YYYY-MM-DD_<业务>_<端别>.html`
  - 例：`2026-09-10_卡种维度奖励配置_管理端.html`
  - 端别取值：`管理端` / `客户端` / `B端` / `代币官网` / `白标门户`（2026-09-15 新增 / `租户业务台`（2026-10-14 新增）
- **存放位置**：统一收在仓库根 `prototypes/` 下
  - **文件夹按「需求」划分，文件夹名不含端别**（例：`prototypes/返佣和奖励/`）
  - **端别由文件名承载**（`管理端` / `客户端` / `B端` / `代币官网`）
  - 时间维度由文件名 `YYYY-MM-DD` 前缀承载，同文件夹内按文件名排序即时间序
- **登记**：新增后在本文件对应业务分组登记（原型名称 / 功能 / 最后更新 / 链接）
- **存量为何不动**：改名会打断大量内部 `.html` 互链，已部署的旧路径会 404。除「返佣与奖励」8 个外，旧文件继续留在 `admin/prototypes/*`、`client/prototypes/*`

---

## 2. 🧭 入口与导航（3）

*仓库根 / 各端导航页 —— 原型总入口*

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| 管理端原型总览 | Card 模块导航首页 | 2026-09-10 | [index.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/index.html) |
| 项目文件导航 | 仓库导航首页 | 2026-09-10 | [index.html](https://xieyi0734-art.github.io/yasbe-prototypes/index.html) |
| C 端原型导航 | Card 模块导航首页 | 2026-07-08 | [index.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/index.html) |

---

## 3. 🖥️ 专题 · 租户业务台（BaaS 白标 · 租户侧控制台）（11）

*`prototypes/租户业务台/`（2026-10-14 首版 18 页，同日按 MVP 精简为 8 页 + 目录页）*

> **业务**：BaaS 白标系统的租户侧控制台（Tenant Dashboard）—— 仅法币（USD / EUR / GBP）虚拟账户的开户、入金与出金；把原先分开的业务管理与开发者门户合并为一个系统。
> **端别**：`租户业务台`（2026-10-14 新增端别取值；与平台侧管理端、白标门户并列为三个独立前端工程）。
> **计费**：外扣模式 —— 租户预存储备金，每笔出入金手续费从储备金扣减，不从终端用户本金中扣。
> **角色**：管理员 / 财务 / 研发三档固定权限；每页左下角可切换角色查看菜单与按钮的差异。
> **口径**：MVP 只留 8 页；挂账待认领 / 账单与发票 / 事件清单 / 团队与权限 / 安全 / 通知偏好 / 审计日志 属一期后补，充值并入储备金页弹窗、虚拟账户并入终端用户详情、待办并入工作台首页。**例外（2026-10-15）**：「账号设置」已按产品需求新增为第 10 页，只放本人的登录凭据与验证方式（修改密码 / 修改邮箱 / 身份验证器绑定与解绑 / 登录设备）；PRD 1.1 中「安全」面上的租户级策略仍属一期后补。
> **平台服务**：首页按「法币账户 / 加密货币 / 卡片」展示平台对外提供的服务与当前租户开通状态（本租户：法币已开通，加密货币与卡片未开通，用量位以「—」占位）；除首页外其余页面仍只覆盖法币（USD / EUR / GBP）。
> **PRD**：[`prd/租户业务台/租户业务台-页面结构与字段定义-v0.1.md`](../prd/租户业务台/租户业务台-页面结构与字段定义-v0.1.md)

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| 页面目录（入口） | 8 页总览 + 范围与口径 + 三份交付物落点 | 2026-10-14 | [index.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/租户业务台/index.html) |
| 工作台首页 | 平台服务开通状态（法币/加密货币/卡片）· 储备金三币种状态 · 待办 · 接入健康度 | 2026-10-15 | [2026-10-14_工作台首页_租户业务台.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/租户业务台/2026-10-14_工作台首页_租户业务台.html) |
| 账号设置 | 本人账号（卡片式）：修改密码 · 修改邮箱 · 身份验证器绑定与解绑 · 登录设备 | 2026-10-15 |
| 账户管理 | 本租户成员与角色：邀请成员 · 改角色 · 停用与移除（仅管理员） | 2026-10-15 | [2026-10-15_账户管理_租户业务台.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/租户业务台/2026-10-15_账户管理_租户业务台.html) | [2026-10-15_账号设置_租户业务台.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/租户业务台/2026-10-15_账号设置_租户业务台.html) |
| 终端用户列表 | 认证状态 · 持有账户 · 进入详情（需补件整行高亮） | 2026-10-14 | [2026-10-14_终端用户列表_租户业务台.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/租户业务台/2026-10-14_终端用户列表_租户业务台.html) |
| 终端用户详情 | 认证材料与缺件清单 · 名下虚拟账户与收款信息（列表下钻页） | 2026-10-14 | [2026-10-14_终端用户详情_租户业务台.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/租户业务台/2026-10-14_终端用户详情_租户业务台.html) |
| 交易流水 | 入金/出金筛选 · 抽屉拆出用户本金与手续费（外扣重点） | 2026-10-14 | [2026-10-14_交易流水_租户业务台.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/租户业务台/2026-10-14_交易流水_租户业务台.html) |
| 储备金与账单 | 三币种可用余额 · 三档告警 · 逐笔手续费扣减 · 充值弹窗 | 2026-10-14 | [2026-10-14_储备金与账单_租户业务台.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/租户业务台/2026-10-14_储备金与账单_租户业务台.html) |
| API Key 管理 | 生成（完整值只显示一次）· 掩码列表 · 轮换与吊销 | 2026-10-14 | [2026-10-14_API-Key管理_租户业务台.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/租户业务台/2026-10-14_API-Key管理_租户业务台.html) |
| Webhook 端点 | 接收地址与订阅事件 · 签名密钥 · 验证投递 · 暂停恢复 | 2026-10-14 | [2026-10-14_Webhook端点_租户业务台.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/租户业务台/2026-10-14_Webhook端点_租户业务台.html) |
| 投递日志 | 逐次投递记录 · 失败原因与自助排查 · 手动重投 | 2026-10-14 | [2026-10-14_投递日志_租户业务台.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/租户业务台/2026-10-14_投递日志_租户业务台.html) |

---

## 4. 🧑‍💼 专题 · VA 代理（双端）（12）

*`prototypes/VA代理/`（2026-10-09 首版 10 页 · 2026-10-10 代理端两页改版）*

> **业务**：平台以自有名义发展的独立代理 —— 代客开立法币虚拟账户（VA），代理独立登录门户、平台独立后台管理。
> **双端**：① 代理端门户（独立 URL · 独立账号体系，不与平台标准用户账号关联）② 平台管理端（独立后台，独立于 YASBe 主管理端）。**无独立客户登录端**。
> **口径**：仅用上游通道必填字段开户（USD 12 项 + 证件照片；EUR / GBP 名·姓·邮箱由客户资料带出 + 地址三项）；代理端不展示通道名与「入账通道」列；余额按客户 / 按 VA 逐个看，**不做跨客户汇总（无「总余额」）**；平台不提供出金，出金在上游通道后台完成；入账由上游通知驱动，先落「未结算」，运营承兑（结算）后代理端才可见；**结算不可逆**。
> **PRD**：[`prd/VA代理业务-需求梳理-v0.4.md`](../prd/VA代理业务-需求梳理-v0.4.md)

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| VA 列表 · 代理端 🆕 | 代理端 VA 列表：名下 VA 总数 / 已激活 / 余额合计（折 USD）/ 累计入账（折 USD）/ 开户处理中 + 逐 VA 当前余额 · 累计入账（折 USD）· 开立时间；不展示入账通道 | 2026-10-10 | [2026-10-10_VA列表_代理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/VA代理/2026-10-10_VA列表_代理端.html) |
| 入金记录 · 代理端 🆕 | 代理端入金记录：逐笔入账时间 / 币种 / 收款账号 / 入账金额 / 折 USD / 付款方附言 / 状态；仅显示已结算（运营承兑后）的入账 | 2026-10-10 | [2026-10-10_入金记录_代理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/VA代理/2026-10-10_入金记录_代理端.html) |
| 客户列表 · 代理端 | 代理端客户列表：名下客户 + 已开通 VA（含开户处理中）+ 累计入账（折 USD）+ 创建时间；新增客户弹窗（姓名 / 邮箱 / 初始密码） | 2026-10-09 | [2026-10-09_客户列表_代理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/VA代理/2026-10-09_客户列表_代理端.html) |
| 客户详情 · 代理端 | 客户详情 + 已开立虚拟账户卡片 + 开立法币 VA 弹窗（按币种只展示必填项：USD 12 项 + 证件照片；EUR / GBP 名·姓·邮箱带出 + 地址三项） | 2026-10-09 | [2026-10-09_客户详情_代理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/VA代理/2026-10-09_客户详情_代理端.html) |
| VA 详情 · 代理端 | 单 VA 收款信息（账号 / 路由号 / 银行 / 入金附言）+ 余额（已结算入账累计 − 已出金）+ 该 VA 入账记录 | 2026-10-09 | [2026-10-09_VA详情_代理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/VA代理/2026-10-09_VA详情_代理端.html) |
| 代理登录 · 代理端 | 独立门户登录：独立 URL + 独立账号体系；顶部标识取代理自配平台标识，未配置时显示平台标准标识 | 2026-10-09 | [2026-10-09_代理登录_代理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/VA代理/2026-10-09_代理登录_代理端.html) |
| VA 代理列表 · 管理端 | 平台管理端：4 个代理的客户数 / 已开通 VA / 累计入账（折 USD）/ 状态 + 新增·编辑代理弹窗（含平台标识配置） | 2026-10-09 | [2026-10-09_VA代理列表_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/VA代理/2026-10-09_VA代理列表_管理端.html) |
| 代理详情 · 管理端 | 代理详情：信息卡 + 通道维度账户数·累计 + 名下客户 + 开户失败待处理 | 2026-10-09 | [2026-10-09_代理详情_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/VA代理/2026-10-09_代理详情_管理端.html) |
| 客户与 VA 总览 · 管理端 | 全量客户 × VA 总览（VA 账号 / 余额 / 累计入账 / 开户时间 / 状态）+ 统计条；不做跨客户汇总 | 2026-10-09 | [2026-10-09_客户与VA总览_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/VA代理/2026-10-09_客户与VA总览_管理端.html) |
| 入账流水 · 管理端 | 上游入账通知流水 + 结算闸门（未结算 → 运营承兑结算 → 代理端可见）+ 未结算/已结算统计 + 批量结算弹窗 | 2026-10-09 | [2026-10-09_入账流水_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/VA代理/2026-10-09_入账流水_管理端.html) |
| 开户记录 · 管理端 | 开户提交记录（提交时间 / 开户申请号 / 客户 / 归属代理 / 币种 / 状态 / 说明） | 2026-10-09 | [2026-10-09_开户记录_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/VA代理/2026-10-09_开户记录_管理端.html) |
| 管理端登录 · 管理端 | VA 代理平台独立管理后台登录（独立于 YASBe 主管理端） | 2026-10-09 | [2026-10-09_管理端登录_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/VA代理/2026-10-09_管理端登录_管理端.html) |

---

## 5. 🎁 专题 · 返佣与奖励（23 = 现行 15 + 历史 8）

*`prototypes/返佣和奖励/`（2026-09-10 归集；2026-09-18 按「电子签名留存 + 自动审核 + 兜底值」新口径重铺 7 页）*

**A. 现行版 · 代理体系（2026-09-18）**

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| 代理申请入口 · 客户端 🆕 | 代理申请引导与返佣口径说明（兜底：开卡 $6.00/单 · 充值 0.25%） | 2026-09-18 | [2026-09-18_代理申请入口_客户端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-09-18_代理申请入口_客户端.html) |
| 代理协议签署 · 客户端 🆕 | 代理协议正文 + canvas 手写电子签名 + 同意勾选门禁（未勾选不可提交），提交即生成存证 | 2026-09-18 | [2026-09-18_代理协议签署_客户端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-09-18_代理协议签署_客户端.html) |
| 代理申请状态 · 客户端 🆕 | 提交后即时自动核验 → 即时开通（无人工等待）+ 自动核验明细；含电子签名存证卡（编号 ES-20260918-4F7A2C · 协议 v1.1 · SHA-256 摘要）；核验未通过转平台进一步核验 | 2026-09-18 | [2026-09-18_代理申请状态_客户端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-09-18_代理申请状态_客户端.html) |
| 代理中心 · 客户端 🆕 | 代理身份总览 + 专属推广链接 + 返佣记录 + 我的返佣比例（来源标签：标准返点 / 专属调整） | 2026-09-18 | [2026-09-18_代理中心_客户端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-09-18_代理中心_客户端.html) |
| 代理管理 · 管理端 🆕 | 代理申请列表（申请人 / 实名状态 / 电子签名存证 / 开通时间 / 下级数 / 返佣方案 / 状态）+ 统计条 + 代理详情与调佣入口 | 2026-09-18 | [2026-09-18_代理管理_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-09-18_代理管理_管理端.html) |
| 代理返佣调整 · 管理端 🆕 | 按代理二次调整返 U（卡产品维度：兜底值 vs 调整后双列）+ 电子签名存证渲染 + 调整历史留痕 | 2026-09-18 | [2026-09-18_代理返佣调整_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-09-18_代理返佣调整_管理端.html) |
| 代理兜底值规则 · 管理端 🆕 | 平台兜底返 U（开卡 $6.00/单 · 充值 0.25%）+ 兜底 Points（充值 0.02% · 开卡 10 yasbee+/单）+ 生效优先级与操作日志 | 2026-09-18 | [2026-09-18_代理兜底值规则_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-09-18_代理兜底值规则_管理端.html) |

**B. 现行版 · 奖励与结算配置（2026-07-08 ~ 2026-09-10）**

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| yasbee+ 用户奖励设置 | 卡种维度奖励比例（开卡/卡充值 × 实体/虚拟） | 2026-09-10 | [2026-09-10_yasbee+用户奖励设置_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-09-10_yasbee+用户奖励设置_管理端.html) |
| YASBee Points 奖励记录与规则设置 | 客户维度奖励场景（开卡/卡充值/币兑）+ 代理返佣设置（下级开卡/充值/币兑）+ 奖励记录 | 2026-09-10 | [2026-09-10_YASBee-Points奖励记录与规则设置_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-09-10_YASBee-Points奖励记录与规则设置_管理端.html) |
| 代理推广与收益看板（B 端） | B 端代理推广与收益看板 | 2026-09-10 | [2026-09-09_代理推广与收益看板_B端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-09-09_代理推广与收益看板_B端.html) |
| Rewards · YASBee Cash & Points（C 端） | 双表：YASBee Cash（购买 / 空投赠送）+ YASBee Points（开卡 / 卡充值 / 币兑奖励） | 2026-09-10 | [2026-09-09_yasbee+奖励记录_客户端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-09-09_yasbee+奖励记录_客户端.html) |
| 返佣记录 | 待结算返佣 + 发起结算操作 | 2026-09-10 | [2026-08-11_返佣记录_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-08-11_返佣记录_管理端.html) |
| 结算记录 | 已结算台账（无结算操作） | 2026-09-10 | [2026-08-10_结算记录_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-08-10_结算记录_管理端.html) |
| 卡片代理返佣配置 | 代理配置 + 卡片返佣比例（按卡产品） | 2026-09-10 | [2026-08-10_卡片代理返佣配置_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-08-10_卡片代理返佣配置_管理端.html) |
| 分销返佣配置 | 分销返点规则配置（一级分销） | 2026-09-10 | [2026-07-08_分销返佣配置_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/返佣和奖励/2026-07-08_分销返佣配置_管理端.html) |

**C. 历史版本 · 代理体系旧口径（2026-09-17；已被 A 块取代，仅留追溯，请勿对外引用）**

*已归档至 `archive/返佣和奖励-旧口径/`（8 个原型 + 2 个 `.bak` 备份），下表线上链接为归档后路径。*

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| 代理申请入口 · 客户端（旧口径） | 人工审核流程版：提交后等待商务对接与人工审核 | 2026-09-17 | [2026-09-17_代理申请入口_客户端.html](https://xieyi0734-art.github.io/yasbe-prototypes/archive/返佣和奖励-旧口径/2026-09-17_代理申请入口_客户端.html) |
| 代理协议签署 · 客户端（旧口径） | 协议签署版（无电子签名存证） | 2026-09-17 | [2026-09-17_代理协议签署_客户端.html](https://xieyi0734-art.github.io/yasbe-prototypes/archive/返佣和奖励-旧口径/2026-09-17_代理协议签署_客户端.html) |
| 代理申请状态 · 客户端（旧口径） | 审核中 / 待商务对接状态版 | 2026-09-17 | [2026-09-17_代理申请状态_客户端.html](https://xieyi0734-art.github.io/yasbe-prototypes/archive/返佣和奖励-旧口径/2026-09-17_代理申请状态_客户端.html) |
| 代理中心 · 客户端（旧口径） | 代理中心（旧返佣来源口径） | 2026-09-17 | [2026-09-17_代理中心_客户端.html](https://xieyi0734-art.github.io/yasbe-prototypes/archive/返佣和奖励-旧口径/2026-09-17_代理中心_客户端.html) |
| 代理管理 · 管理端（旧口径） | 代理列表（旧口径） | 2026-09-17 | [2026-09-17_代理管理_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/archive/返佣和奖励-旧口径/2026-09-17_代理管理_管理端.html) |
| 代理审核与返佣配置 · 管理端（旧口径） | 已由 A 块「代理返佣调整」取代 | 2026-09-17 | [2026-09-17_代理审核与返佣配置_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/archive/返佣和奖励-旧口径/2026-09-17_代理审核与返佣配置_管理端.html) |
| 代理返佣规则与日志 · 管理端（旧口径） | 已由 A 块「代理兜底值规则」取代 | 2026-09-17 | [2026-09-17_代理返佣规则与日志_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/archive/返佣和奖励-旧口径/2026-09-17_代理返佣规则与日志_管理端.html) |
| 代理推广与收益看板（B 端 · 旧口径） | B 端代理推广与收益看板（来源标签仍为旧口径，待同步） | 2026-09-17 | [2026-09-17_代理推广与收益看板_B端.html](https://xieyi0734-art.github.io/yasbe-prototypes/archive/返佣和奖励-旧口径/2026-09-17_代理推广与收益看板_B端.html) |

## 6. 🏦 管理端 · 法币渠道（6）

*`admin/prototypes/fiat/` —— 法币复核 / 交易 / 银行账户 / 币种设置 / 通道日志（6 页）*

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| 法币 · 渠道调用日志 | 法币通道调用轨迹: traceId / 接口 / 状态 / 耗时 / 重试 / 关联交易，按交易号反查（新增页） | 2026-09-17 | [06-Channel-Api-Logs.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/fiat/06-Channel-Api-Logs.html) |
| 法币 · 币种设置 | 费率挂「通道 × 币种 × rails」两档 + 退回费; 1 弹窗(费率编辑 · 金额档位可配置); 无编辑币种 · 无启停开关 · 无 FX 兑换费 · 无通道成本 · 无限额层级 | 2026-09-17 | [05-Fiat-Currency-Settings.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/fiat/05-Fiat-Currency-Settings.html) |
| 法币 · 收款账户 | **三 table 页签**：客户账户(逐户列表 8 列 + 客户账户明细弹窗) / 开户记录(申请单 10 列, 含驳回原因) / 平台通道账户(12 列, 余额·冻结·可用·净额·归集·对账, 已并入原资金总览) | 2026-09-17 | [04-Fiat-Bank-Accounts.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/fiat/04-Fiat-Bank-Accounts.html) |
| 法币 · 资金总览 | **已并入「收款账户」页 → 平台通道账户页签**（通道 × 币种矩阵 + 余额/冻结/可用/净额 + 归集 + 对账）；本页保留跳转存根 | 2026-09-17 | [03-Fiat-Treasury-Overview.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/fiat/03-Fiat-Treasury-Overview.html) |
| 法币 · 交易记录 | 出入金全量流水（12 列，通道 / 上游状态 / 渠道交易号）+ 平台侧·上游侧双栏详情（已终审行亦可打开，终审态隐藏审核动作）+ 通道筛选 | 2026-09-17 | [02-Fiat-Transaction-List.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/fiat/02-Fiat-Transaction-List.html) |
| 法币 · 交易审核 | **双通道（Bridge / OpenPayd）**待办队列: 入金(挂账复核 / Pay In 待确认) / 出金(合规终审 / Payout 待审) / EA 非同名添加; 通道列 + 通道筛选 + 判定方标注(平台/上游) | 2026-09-17 | [01-Fiat-Review-Queue.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/fiat/01-Fiat-Review-Queue.html) |

---

## 7. 💳 管理端 · 卡片 · 渠道 · 交易（10）

*`admin/prototypes/{card-type,card-management,card-intro,channel,client-profile,transaction}/`*

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| 渠道管理 | 发卡渠道管理（07） | 2026-09-16 | [07-Channel-Management.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/channel/07-Channel-Management.html) |
| 卡务管理（卡类型） | 卡产品类型管理（08） | 2026-09-10 | [08-Card-Type-Management.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/card-type/08-Card-Type-Management.html) |
| 卡片介绍 v5（旧版 · 请勿对外引用） | 早期卡片介绍（v5） | 2026-07-08 | [CardIntroduction_v5.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/card-intro/CardIntroduction_v5.html) |
| 卡片介绍（旧版 · 请勿对外引用） | 早期卡片介绍页 | 2026-07-08 | [CardIntroduction.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/card-intro/CardIntroduction.html) |
| 交易审核 | 交易审核快照（18） | 2026-07-08 | [18-Card-Transaction-Review.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/transaction/18-Card-Transaction-Review.html) |
| 卡片交易流水 | 交易流水列表（17） | 2026-07-08 | [17-Card-Transaction-List.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/transaction/17-Card-Transaction-List.html) |
| 卡片介绍（旧版 · 请勿对外引用） | 卡片产品介绍页（12） | 2026-07-08 | [12-Card-Introduction.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/card-intro/12-Card-Introduction.html) |
| 我的资料 | 客户资料弹窗（11） | 2026-07-08 | [11-Client-Profile-Modal.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/client-profile/11-Client-Profile-Modal.html) |
| 卡片管理 | 卡片列表管理（03） | 2026-07-08 | [03-Card-Management.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/card-management/03-Card-Management.html) |
| 卡片详情 | 单卡详情（02） | 2026-07-08 | [02-Card-Detail.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/card-management/02-Card-Detail.html) |

*`card-intro/` 下 3 版（CardIntroduction_v5 / CardIntroduction / 12-Card-Introduction）均为 2026-06 ~ 07 早期版本，同批登记、均标为旧版。*

---

## 8. 🧩 专题 · API 文档（白标开发者门户）（9）

*`prototypes/API文档-白标开发者门户/`（2026-09-15）*

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| 原型导航（入口） | 8 页总览 + 参考基准 + 占位说明 | 2026-09-15 | [index.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/API文档-白标开发者门户/index.html) |
| 错误码与限流 | 错误响应结构 + HTTP 语义 + 30+ 业务错误码 + 幂等语义 + 限流配额与重试 | 2026-09-15 | [2026-09-15_错误码与限流_白标门户.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/API文档-白标开发者门户/2026-09-15_错误码与限流_白标门户.html) |
| 沙盒环境 | 自助开通 · 密钥形态 · 11 个模拟端点 · 测试数据 · 与生产差异表 · 上线检查清单 | 2026-09-15 | [2026-09-15_沙盒环境_白标门户.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/API文档-白标开发者门户/2026-09-15_沙盒环境_白标门户.html) |
| 服务能力总览 | 白标可售能力矩阵（8 模块 × 端点 × 前置条件 × 沙盒可用）+ 集成模式对照 + 能力边界 | 2026-09-15 | [2026-09-15_服务能力总览_白标门户.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/API文档-白标开发者门户/2026-09-15_服务能力总览_白标门户.html) |
| 快速开始 · Quick Start | 四步跑通首次调用：开通主体 → 取密钥 → 环境与鉴权（API Key / OAuth）→ 创建首个客户；含请求约定与常见坑 | 2026-09-15 | [2026-09-15_快速开始_白标门户.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/API文档-白标开发者门户/2026-09-15_快速开始_白标门户.html) |
| 开发者设置（B端门户） | 门户内控制台：环境切换 · API 密钥 · Webhook 端点与签名密钥 · IP 白名单 · 沙盒工具 · 请求日志 | 2026-09-15 | [2026-09-15_开发者设置_白标门户.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/API文档-白标开发者门户/2026-09-15_开发者设置_白标门户.html) |
| 事件与通知 | 29 类事件清单 + 投递与重试 + 签名校验（Node/Python）+ 沙盒重投 | 2026-09-15 | [2026-09-15_事件与通知_白标门户.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/API文档-白标开发者门户/2026-09-15_事件与通知_白标门户.html) |
| 文档首页 · Welcome | 能构建什么（6 场景）+ 四大核心组件 + 三种集成模式 + 入口分流 | 2026-09-15 | [2026-09-15_API文档首页_白标门户.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/API文档-白标开发者门户/2026-09-15_API文档首页_白标门户.html) |
| API Reference | 36 端点清单 + 5 端点完整文档形态（字段表/多语言示例/响应/拒绝原因）+ 状态机枚举 | 2026-09-15 | [2026-09-15_API参考_白标门户.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/API文档-白标开发者门户/2026-09-15_API参考_白标门户.html) |

---

## 9. 🔎 专题 · 加密出入金风险扫描（4）

*`prototypes/加密出入金风险扫描/`（Merkle Science）*

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| 加密出入金风险扫描 · 管理端（最新） 🆕 | 加密货币 · 交易审核：risk_level 六等级映射（0–2 自动通过 / 3–5 转人工，阈值 3）+ 16 列含退款状态 + 拒绝理由落库 + 重新扫描 | 2026-09-20 | [2026-09-14_加密出入金风险扫描_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/加密出入金风险扫描/2026-09-14_加密出入金风险扫描_管理端.html) |
| 加密出入金风险扫描 · 客户端 | Crypto Wallet（资产总览 + 资产列表 + 交易记录，深色 #FFCA00）+ 充值/提现弹窗 + 钱包风险扫描（审核中/已拒绝） | 2026-09-20 | [2026-09-11_加密出入金风险扫描_客户端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/加密出入金风险扫描/2026-09-11_加密出入金风险扫描_客户端.html) |
| 加密出入金风险扫描 · 客户端（旧版 · 请勿对外引用） | Crypto Wallet 首版：资产总览 + 交易记录 + 钱包风险扫描 —— **已被 2026-09-11 版取代** | 2026-09-11 | [2026-09-10_加密出入金风险扫描_客户端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/加密出入金风险扫描/2026-09-10_加密出入金风险扫描_客户端.html) |
| 加密出入金风险扫描 · 管理端（旧版 · 请勿对外引用） | 加密货币 · 交易审核：入金/出金两条风控队列 + Merkle 风险明细 + 批准/拒绝处置 —— **已被 2026-09-14 版取代** | 2026-09-10 | [2026-09-10_加密出入金风险扫描_管理端.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/加密出入金风险扫描/2026-09-10_加密出入金风险扫描_管理端.html) |

---

## 10. 💱 客户端 · 法币虚拟账户（3）

*`client/prototypes/bank-virtual-account/`*

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| 法币账户（美元 · 多渠道多账户）（最新） 🆕 | C 端 USD 虚拟账户：美元账户开通 + 多账户视图 + 出入金；开通资料按三情形自动追加（无业但声明工资 / 养老金退休金 / 高月均资金往来），判定与展示范围＝EEA + 风险客户 | 2026-09-20 | [02-法币账户-多渠道多账户.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/bank-virtual-account/02-法币账户-多渠道多账户.html) |
| 用户开通虚拟账户 🆕 | C 端银行账户页：法币账户列表 + 最近的法币交易 + 开通入口 | 2026-09-20 | [01-用户开通虚拟账户.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/bank-virtual-account/01-用户开通虚拟账户.html) |
| 法币账户（欧元 / 英镑 · 多渠道多账户） | C 端法币账户开通 + 多账户视图（EUR/GBP，多渠道） | 2026-09-09 | [03-法币账户-欧元英镑-多渠道多账户.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/bank-virtual-account/03-法币账户-欧元英镑-多渠道多账户.html) |

**模块 PRD**：`PRD-虚拟账户-USD通道-v0.1.md`（美元通道 · 对标 Bridge OpenAPI · v0.8）· `PRD-法币账户-欧元英镑-OpenPayd通道-v0.1.md`（欧元英镑通道 · 对标 OpenPayd · v0.3）

---

## 11. 🛡️ 管理端 · 核验 · 风控 · 客户（10）

*`admin/prototypes/{verification,risk-control,customer,crypto}/`*

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| 客户详情 · 法币 Tab | 客户法币账户 + 出入金记录 | 2026-09-08 | [02-Customer-Detail-Fiat-Tab.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/customer/02-Customer-Detail-Fiat-Tab.html) |
| ComplyAdvantage 案件 | CA 风险案件列表（06） | 2026-08-11 | [06-ComplyAdvantage-Cases.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/verification/06-ComplyAdvantage-Cases.html) |
| KYB 审核详情 (CA) | KYB 审核 + ComplyAdvantage 命中抽屉 | 2026-08-11 | [05-KYB-ReviewDetail-CA.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/verification/05-KYB-ReviewDetail-CA.html) |
| KYC 审核详情 (CA) | KYC 审核 + ComplyAdvantage 命中抽屉 | 2026-08-11 | [04-KYC-ReviewDetail-CA.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/verification/04-KYC-ReviewDetail-CA.html) |
| 加密货币归集设置 | Crypto 归集配置（19） | 2026-07-08 | [19-Crypto-Collection-Settings.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/crypto/19-Crypto-Collection-Settings.html) |
| 客户详情 · 推荐 Tab | 客户推荐视图（10） | 2026-07-08 | [10-Customer-Detail-Referrals-Tab.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/customer/10-Customer-Detail-Referrals-Tab.html) |
| KYC 审核详情 v1 | KYC 审核（旧版） | 2026-07-08 | [03-KYC-ReviewDetail-v1.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/verification/03-KYC-ReviewDetail-v1.html) |
| 风控事件列表 | 风控事件（02） | 2026-07-08 | [02-Risk-Event-List.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/risk-control/02-Risk-Event-List.html) |
| 风控规则管理 | 风控规则配置（01） | 2026-07-08 | [01-Risk-Rule-Management.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/risk-control/01-Risk-Rule-Management.html) |
| 客户详情 · 卡片 Tab | 客户卡片视图（01） | 2026-07-08 | [01-Customer-Detail-Cards-Tab.html](https://xieyi0734-art.github.io/yasbe-prototypes/admin/prototypes/customer/01-Customer-Detail-Cards-Tab.html) |

---

## 12. 📱 客户端 · 卡片与账务（14）

*`client/prototypes/*`（卡管理 / 开卡 / 激活 / 账单 / KYC / 风控）*

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| B 端卡片管理 | B 端卡片管理（21） | 2026-08-26 | [21-B端-卡片管理.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/card-management/21-B端-卡片管理.html) |
| 卡片详情 | C 端单卡详情（33） | 2026-07-24 | [33-卡片详情.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/card-management/33-卡片详情.html) |
| 实体卡申请 · 收件信息 | 实体卡申请配送弹窗 | 2026-07-21 | [17-Card-Apply-Shipping-Modal.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/card-apply/17-Card-Apply-Shipping-Modal.html) |
| 卡片激活弹窗 | 激活流程弹窗 | 2026-07-21 | [01-Card-Activation-Modals.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/card-activation/01-Card-Activation-Modals.html) |
| 账务模块导航 | 账务原型导航 | 2026-07-08 | [index-账务管理.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/index-账务管理.html) |
| 交易快照 | 卡片交易快照 | 2026-07-08 | [card-transaction-snapshot.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/card-overview/card-transaction-snapshot.html) |
| 账单管理 | 账单页（22） | 2026-07-08 | [22-账单管理.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/fee-billing/22-账单管理.html) |
| 费用结算 | 结算页面（21） | 2026-07-08 | [21-费用结算.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/fee-billing/21-费用结算.html) |
| 卡片管理 v6 | C 端卡片管理（MoR PRD v3.1） | 2026-07-08 | [12-卡片管理-v6.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/card-management/12-卡片管理-v6.html) |
| KYC 信息更新 | 更新资料（Scenario B） | 2026-07-08 | [02-KYC-SelfUpdate-ScenarioB-v1.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/kyc/02-KYC-SelfUpdate-ScenarioB-v1.html) |
| 费用管理 v2 | 费用/费率管理 | 2026-07-08 | [02-Fee-Management-v2.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/fee-billing/02-Fee-Management-v2.html) |
| KYC 认证已暂停 | KYC 暂停状态页 | 2026-07-08 | [01-KYC-Suspended-v1.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/kyc/01-KYC-Suspended-v1.html) |
| 卡账交易列表 | 卡账交易流水 | 2026-07-08 | [01-Card-Accounting-Transaction-List.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/card-overview/01-Card-Accounting-Transaction-List.html) |
| 卡账户总览 v2 | 账户总览 + 交易列表 | 2026-07-08 | [01-Card-Account-Overview-v2.html](https://xieyi0734-art.github.io/yasbe-prototypes/client/prototypes/card-overview/01-Card-Account-Overview-v2.html) |

---

## 13. 🔀 流程图（16）

*`diagrams/`*

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| ComplyAdvantage 风控接入流程 | 筛查→评分→风险等级流程图 | 2026-08-05 | [comply-advantage-risk-flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/comply-advantage-risk-flow.html) |
| 实体卡开卡流程 | 开卡流程（版2） | 2026-07-24 | [card-issue-flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/card-issue-flow.html) |
| 实体卡开卡完整流程 | 开卡全流程 | 2026-07-24 | [card-full-flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/card-full-flow.html) |
| 卡片激活流程 | Region 4 激活流程 | 2026-07-24 | [card-activation-flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/card-activation-flow.html) |
| B 端用户操作流程 | B 端操作流程图 | 2026-07-24 | [b端用户操作流程.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/b端用户操作流程.html) |
| 代理返佣业务流程 | 代理返佣流程图 | 2026-07-24 | [agent-rebate-flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/agent-rebate-flow.html) |
| KYC/KYB Re-review 流程 | 平台重审流程图 | 2026-07-08 | [platform-kyc-kyb-review-flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/platform-kyc-kyb-review-flow.html) |
| 模块化 KYC 流程 | KYC 认证流程图 | 2026-07-08 | [module-based-kyc-flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/module-based-kyc-flow.html) |
| 分模块 KYB 流程 | KYB 认证流程图 | 2026-07-08 | [module-based-kyb-flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/module-based-kyb-flow.html) |
| 卡片账务功能架构 | 管理端卡片账务架构图 | 2026-07-08 | [card-accounting-architecture.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/card-accounting-architecture.html) |
| YASBee 账务功能架构 | 卡片账务架构图 | 2026-07-08 | [YASBee-账务功能架构图.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/YASBee-账务功能架构图.html) |
| Card 账务功能架构 v3.0 | 账务模块架构图 | 2026-07-08 | [Card模块账务_v3.0_功能架构图.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/Card模块账务_v3.0_功能架构图.html) |
| 白标系统 · 全局系统架构图 🆕 | 白标一期全局架构（Mermaid）：第 1 张分层集成视图 = flowchart TD + subgraph，6 个层色块 / 26 节点（L0 拆 参与方 ACTOR 与 界面层 UI；上游一期 4 家实线高亮、二期 BitGo 虚线 Phase 2）；第 2 张核心实体关系 = erDiagram，19 实体（含 TENANT_PRICING 租户定价、AUDIT_LOG 审计日志）/ 1:1 · 1:N · 1:0..1；含分层图例 + 缩写与 BaaS 业务含义表 | 2026-10-13 | [白标系统-全局系统架构图.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/白标系统-全局系统架构图.html) |
| 白标系统 · 二期 API 与状态机设计 🆕 | 二期设计稿三件套：① 终端用户身份合规与开户状态机（stateDiagram-v2，6 状态 / 10 条转移 / 6 处 Webhook 标注）② 核心 API 接口清单（20 个接口 / 5 组：合规身份 · 子账户开立 · 法币出金 · 历史流水 · Webhook 订阅，含幂等键构成）③ 法币入金时序图（sequenceDiagram，7 参与者 / 20 条消息 + 挂账分支）④ Webhook 事件清单（15 行 / 19 个事件名，含 fiat.deposit.settled） | 2026-10-13 | [白标系统-二期-API与状态机设计.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/白标系统-二期-API与状态机设计.html) |
| 白标系统 · 三期 路由与对账方案 🆕 | 三期三件套：① 多币种出金智能路由决策树（flowchart TD，28 节点 / 33 条边：幂等 → 准入 → 风控拦截 → 额度 → Master Account 余额 → 智能选路 USD→Bridge / EUR·GBP→OpenPayd → 健康度探活 → cut-off → 查单优先重试 → 熔断降级与排队）② 状态归一化与适配器防腐层（sequenceDiagram，7 参与者 / 16 条消息 + 13 行状态映射字典：Bridge COMPLETED 与 OpenPayd EXECUTED 均归一为 SETTLED，未知状态挂人工）③ T+1 全局对账与核平（5 类外部数据源 + 三层双向核对 + 9 类差错账处置表：单边账 / 金额错配 / 状态不一致 / 重复流水 / 跨日 / 链上重组 / 卡授权未清算） | 2026-10-13 | [白标系统-三期-路由与对账方案.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/白标系统-三期-路由与对账方案.html) |
| 白标系统 · 一期 业务抽象与数据建模 🆕 | 一期（MVP · 纯法币）三件套：① 核心实体关系 = erDiagram，8 实体 / 92 字段 / 11 条关系（TENANT 与 API_KEY 轮换、TENANT_PRICING 租户定价、USER_PROFILE 合规身份独立于资产、FIAT_ACCOUNT 虚拟账户 VA、TRANSACTION_LEDGER 全局账本、ROUTING_RULE 多通道路由、AUDIT_LOG 审计）② 全局分层架构 = flowchart TD + subgraph，6 层色块 / 26 节点 / 40 条边（L0_ACTOR → L0_UI → L1_GATEWAY → L2_SERVICE → L3_ADAPTER 防腐层 → L4_UPSTREAM：Bridge 三币种、OpenPayd 两币种，EUR 与 GBP 双腿冗余 Multi-Rail）③ 名词解释表 19 行（VA / Global Ledger / Multi-Rail Routing / Anti-Corruption Layer / Attribution 等） | 2026-10-14 | [白标系统-一期-业务抽象与数据建模.html](https://xieyi0734-art.github.io/yasbe-prototypes/diagrams/白标系统-一期-业务抽象与数据建模.html) |

---

## 14. 📄 早期原型（23）

*仓库根 `prototypes/*.html` —— 未按新规范归集，存量不动*

**Dashboard 系列注意**：本区含 5 个变体（`Dashboard.html` / `-New` / `-Chinese` / `-New_tables` / `-v5`），均为 2026-07 早期多方案探索，**非现行版，勿对外引用**。

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| Mesh 接入业务流程 v2 | ComplyAdvantage 接入流程图 | 2026-08-03 | [Mesh-Integration-Business-Flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Mesh-Integration-Business-Flow.html) |
| Dashboard v4 New | 仪表盘新版 | 2026-07-28 | [Dashboard-New.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Dashboard-New.html) |
| Dashboard v4 中文 | 仪表盘中文版 | 2026-07-28 | [Dashboard-Chinese.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Dashboard-Chinese.html) |
| 白标 MVP 流程 | 白标 MVP 流程图 | 2026-07-24 | [White-Label-MVP-Business-Flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/White-Label-MVP-Business-Flow.html) |
| 白标客户业务流程 | 白标业务流程图 | 2026-07-24 | [White-Label-Business-Flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/White-Label-Business-Flow.html) |
| 费用中心架构 | 费用中心架构图 | 2026-07-24 | [Fee-Center-Architecture.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Fee-Center-Architecture.html) |
| Dashboard v4 | 管理端仪表盘 | 2026-07-24 | [Dashboard.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Dashboard.html) |
| Dashboard v5 | 仪表盘 v5 | 2026-07-24 | [Dashboard-v5.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Dashboard-v5.html) |
| Dashboard 表格版 | 仪表盘表格布局版 | 2026-07-24 | [Dashboard-New_tables.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Dashboard-New_tables.html) |
| 加密对账流程 | Crypto 对账业务流 | 2026-07-08 | [crypto-reconciliation-flow.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/crypto-reconciliation-flow.html) |
| 出金 2FA · Fiat | 法币出金 Review + 2FA | 2026-07-08 | [Withdraw-2FA-Fiat.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Withdraw-2FA-Fiat.html) |
| 出金 2FA · Crypto | 提币 2FA 弹窗 | 2026-07-08 | [Withdraw-2FA-Crypto.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Withdraw-2FA-Crypto.html) |
| 对账单 | Statement 页面 | 2026-07-08 | [Statement-Client.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Statement-Client.html) |
| 安全设置 · 2FA 绑定 | 2FA 绑定页 | 2026-07-08 | [Security-2FA-Setup.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Security-2FA-Setup.html) |
| 风控规则管理 | 风控规则（早期版） | 2026-07-08 | [RiskRule-Management.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/RiskRule-Management.html) |
| 新闻管理 | News 后台 | 2026-07-08 | [News-Management.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/News-Management.html) |
| 客户端登录 | 登录页 | 2026-07-08 | [Login-Client.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Login-Client.html) |
| FAQ 官网 | 官网 FAQ 页 | 2026-07-08 | [FAQ-Website.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/FAQ-Website.html) |
| FAQ 管理 | FAQ 后台 | 2026-07-08 | [FAQ-Management.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/FAQ-Management.html) |
| 兑换确认 + 2FA | Exchange 确认弹窗 | 2026-07-08 | [Exchange-Confirm-2FA.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Exchange-Confirm-2FA.html) |
| 兑换确认 2FA 合并 | 兑换确认+2FA 合并版 | 2026-07-08 | [Confirm-Conversion-2FA.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Confirm-Conversion-2FA.html) |
| 博客管理 | Blog 后台 | 2026-07-08 | [Blog-Management.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Blog-Management.html) |
| 账单（C 端） | 对账单/Statement | 2026-07-08 | [Billing-Client.html](https://xieyi0734-art.github.io/yasbe-prototypes/prototypes/Billing-Client.html) |

---

## 15. 📦 其他（7）

*仓库根 / `mesh_docs/` / `prd/`*

| 原型名称 | 功能 | 最后更新 | 链接 |
|---|---|---|---|
| Mesh 对接文档 · Getting Started 🆕 | Mesh 集成对接入门文档页（英文） | 2026-08-03 | [mesh_getting_started.html](https://xieyi0734-art.github.io/yasbe-prototypes/mesh_docs/mesh_getting_started.html) |
| 仪表盘 v4（根） | 管理端仪表盘 | 2026-07-28 | [Dashboard-Chinese.html](https://xieyi0734-art.github.io/yasbe-prototypes/Dashboard-Chinese.html) |
| 仪表盘 New（根） | 管理端仪表盘新版 | 2026-07-27 | [Dashboard-New.html](https://xieyi0734-art.github.io/yasbe-prototypes/Dashboard-New.html) |
| 注册（根） | CYRO Sign Up | 2026-07-24 | [signup.html](https://xieyi0734-art.github.io/yasbe-prototypes/signup.html) |
| 登录（根） | CYRO Sign In | 2026-07-24 | [signin.html](https://xieyi0734-art.github.io/yasbe-prototypes/signin.html) |
| CYRO 代币官网 | 单文件版品牌页 | 2026-07-24 | [cyro-token-website.html](https://xieyi0734-art.github.io/yasbe-prototypes/cyro-token-website.html) |
| 出金 2FA 合并 | Withdraw 2FA 合并版 | 2026-07-08 | [Withdraw-2FA-Combined.html](https://xieyi0734-art.github.io/yasbe-prototypes/Withdraw-2FA-Combined.html) |

---

## 16. ⚠️ 未部署 / 失效清单（25 条）

*这些条目**不能通过 GitHub Pages 访问**，登记保留只为追溯。*

**定义边界（重要）**：本清单只收「线上不可访问」（404 / 目录未部署到 main）的条目。
「线上能打开、但内容已被更新版取代」的旧版**不属于本清单** —— 那类在各章节就地标注「请勿对外引用」：
§4C（返佣 8 条）· §6（卡片介绍）· §8（风险扫描）· §13（Dashboard）。
两类问题不要混：**404 = 打不开；被取代 = 打得开但别用。**

**A. 已登记但线上 404（17 条）**

| 原型名称 | 原链接 | 本地文件 | 状态 |
|---|---|---|---|
| 客户详情 · 推荐 Tab v2 | `admin/prototypes/customer/10-Customer-Detail-Referrals-Tab-v2.html` | 有 | 线上 404（本地存在，未部署到 main） |
| 激活卡片 | `card-prototypes/activate.html` | 有 | 目录被 `.gitignore` 排除，从未部署 |
| 卡片账单 | `card-prototypes/bills.html` | 有 | 目录被 `.gitignore` 排除，从未部署 |
| 卡片详情 | `card-prototypes/card-detail.html` | 有 | 目录被 `.gitignore` 排除，从未部署 |
| 卡片管理 | `card-prototypes/index.html` | 有 | 目录被 `.gitignore` 排除，从未部署 |
| 冻结/解冻/注销 | `card-prototypes/operations.html` | 有 | 目录被 `.gitignore` 排除，从未部署 |
| 管理端 · 网络 | `cyro-website/admin-chains.html` | 有 | 目录被 `.gitignore` 排除，从未部署 |
| 管理端 · 汇率 | `cyro-website/admin-rates.html` | 有 | 目录被 `.gitignore` 排除，从未部署 |
| 管理端 · 交易 | `cyro-website/admin-transactions.html` | 有 | 目录被 `.gitignore` 排除，从未部署 |
| 管理端 · 用户 | `cyro-website/admin-users.html` | 有 | 目录被 `.gitignore` 排除，从未部署 |
| 管理端 | `cyro-website/admin.html` | 有 | 目录被 `.gitignore` 排除，从未部署 |
| 充值 | `cyro-website/deposit.html` | 有 | 目录被 `.gitignore` 排除，从未部署 |
| 官网首页 | `cyro-website/index.html` | 有 | 目录被 `.gitignore` 排除，从未部署 |
| 登录 | `cyro-website/signin.html` | 有 | 目录被 `.gitignore` 排除，从未部署 |
| 注册 | `cyro-website/signup.html` | 有 | 目录被 `.gitignore` 排除，从未部署 |
| 交易记录 | `cyro-website/transactions.html` | 有 | 目录被 `.gitignore` 排除，从未部署 |
| 提现 | `cyro-website/withdraw.html` | 有 | 目录被 `.gitignore` 排除，从未部署 |

**B. 本地存在但从未登记、线上也 404（8 条）**

- `client/prototypes/bank-virtual-account/02-法币账户-多渠道多账户_存档_20260904.html`
- `client/prototypes/bank-virtual-account/02-法币账户-多渠道多账户_存档_20260904_证件照POA前.html`
- `client/prototypes/card-management/22-B端-批量充值.html`
- `client/prototypes/card-management/23-B端-卡片提现.html`
- `client/prototypes/card-management/24-C端-开卡记录.html`
- `client/prototypes/card-management/25-B端-开卡记录.html`
- `client/prototypes/risk-management/风险管理-CA风控Case.html`
- `prototypes/Notifications-Center.html`

**处理建议**：代币官网（`cyro-website/`）与卡片独立版（`card-prototypes/`）若仍需对外演示，请指定目标仓库/分支后重新部署；`10-Customer-Detail-Referrals-Tab-v2` 与 `bank-virtual-account` 系列旧版确认废弃的话，建议删除本地文件并从本文件移除登记。

---

## 📌 新增原型登记模板

| 原型名称 | 功能一句话 | YYYY-MM-DD | [文件名.html](https://xieyi0734-art.github.io/yasbe-prototypes/相对路径/文件名.html) |