# YASBe Card模块PRD v1.4

> **文档版本**: v1.4

> **状态**: 待评审   **编写人**: 谢翼（Driven）

> **日期**: 2026-05-25

> **评审参与方**: YASBe 团队

> 用户端原型：

[请至钉钉文档查看附件《12-卡片管理-v3.html》。](https://alidocs.dingtalk.com/i/nodes/3NwLYZXWynyObXnefZX9X4nbVkyEqBQm?doc_type=wiki_doc&iframeQuery=anchorId%3DX02mpgi4frv0ry8ludalcf&rnd=0.08852992050236175)

> 管理端原型：

[请至钉钉文档查看附件《01-Customer-Detail-Cards-Tab.html》。](https://alidocs.dingtalk.com/i/nodes/3NwLYZXWynyObXnefZX9X4nbVkyEqBQm?doc_type=wiki_doc&iframeQuery=anchorId%3DX02mpgi4yjad8c1fth9njv&rnd=0.08852992050236175)

[请至钉钉文档查看附件《02-Card-Detail.html》。](https://alidocs.dingtalk.com/i/nodes/3NwLYZXWynyObXnefZX9X4nbVkyEqBQm?doc_type=wiki_doc&iframeQuery=anchorId%3DX02mpgi5ek9pzuetowoxy&rnd=0.08852992050236175)

[请至钉钉文档查看附件《03-Card-Management.html》。](https://alidocs.dingtalk.com/i/nodes/3NwLYZXWynyObXnefZX9X4nbVkyEqBQm?doc_type=wiki_doc&iframeQuery=anchorId%3DX02mpgi5tz8dufx24w9xd&rnd=0.08852992050236175)

[请至钉钉文档查看附件《07-Channel-Management.html》。](https://alidocs.dingtalk.com/i/nodes/3NwLYZXWynyObXnefZX9X4nbVkyEqBQm?doc_type=wiki_doc&iframeQuery=anchorId%3DX02mpgi65t1usxoaz02ngl&rnd=0.08852992050236175)

[请至钉钉文档查看附件《08-Card-Type-Management.html》。](https://alidocs.dingtalk.com/i/nodes/3NwLYZXWynyObXnefZX9X4nbVkyEqBQm?doc_type=wiki_doc&iframeQuery=anchorId%3DX02mpgi6foafiyqh50uc6&rnd=0.08852992050236175)

---

## 1. 产品概述

### 1.1 背景

YASBe作为跨境金融科技平台，现有 Crypto 和 Fiat 资产管理服务。为进一步拓展业务场景，计划通过 **Interlace MoR（Master on Record）** 模式推出虚拟卡产品，满足用户在线上消费、跨境支付场景中的需求。

**模式**：选项 B — 主商户模式（Master-Merchant），Interlace 作为卡处理方（发卡行），YASBee 作为主商户，双方通过 API 对接实现开卡、充值、消费、风控管理全流程。

**卡片类型**：

*   **预付卡**→ 资金直接来自钱包或账户余额。持卡人只能消费卡内已充值的金额。
    

*   **个人** → 走 KYC（个人身份认证）
    
*   **企业** → 走 KYB（企业身份认证，类似国内公司户概念）
    

### 1.2 产品定位

YASBee 虚拟卡是一款面向个人和企业用户的 **预付费虚拟卡产品**，支持 Crypto 和 Fiat 双通道充值，USD 结算，多币种消费，实时余额更新。

### 1.3 目标用户

| 用户类型 | 认证方式 | 典型场景 |
| --- | --- | --- |
| 个人用户 | KYC（个人身份认证） | 线上购物、跨境支付、日常消费 |
| 企业用户 | KYB（企业身份认证） | 公司采购、员工费用管理、跨境业务 |

### 1.4 核心数据指标

| 指标 | 目标值 | 说明 |
| --- | --- | --- |
| KYC 审核通过率 | ≥ 90% | 字段齐全的情况下 |
| KYC /KYB审核时长 | ≤ 1 分钟 | 正常通过情况 |
| 开卡成功率 | ≥ 95% | KYC/KYB 通过后 |
| 充值到账成功率 | ≥ 99% | Crypto + Fiat |
| 拒付率控制 | < 5% | 月度维度，超出触发惩罚 |

---

## 2. 业务流程总览

### 2.1 核心业务流程

```plaintext
用户注册 YASBe→ 选择卡片类型（BB/BZ，卡片信息）
  → 提交 KYC/KYB 认证（回显KYC/KYB）
  → Interlace 审核（正常 1 分钟内）
  → 创建持卡人 → 创建卡片 → 开卡成功
  → 充值（Crypto/Fiat）→ 消费 → 管理

```

### 2.2 用户角色

| 角色 | 描述 |
| --- | --- |
| **终端用户** | 使用 YASBee App/H5 开卡、充值、消费、管理卡片 |
| **运营人员** | 处理审核超时、争议、客服工单、对账 |
| **风控人员** | 监控交易风险、配置风控规则 |
| **管理员** | 费用配置、等级配置、BIN 管理 |

---

## 3. 功能需求

### 3.1 卡片管理模块

#### 3.1.1 卡片管理主页

| 功能编号 | F-101 |
| --- | --- |
| **功能名称** | 卡片管理主页 |
| **优先级** | P0 |
| **用户故事** | 作为用户，我希望在一个页面看到我所有卡片的总览，包括总余额、卡片列表、最近交易，以便快速了解资产状况 |
| **功能描述** | 展示用户所有虚拟卡的概览信息，支持多卡切换和管理 |
| **界面元素** | ① 顶部总余额（Card Balance）展示<br>② 多张卡片并列展示（卡面设计），每张展示：卡面颜色、卡号后4位、余额、状态标签、有效期<br>③ 快捷操作按钮组：开新卡、充值、冻结/解冻、限额管理、注销<br>④ 最近交易记录列表<br>⑤ 卡片数量统计、等级信息 |
| **前置条件** | 用户已完成登录 |
| **验收标准** | [AC-101](#81-%E5%8A%9F%E8%83%BD%E9%AA%8C%E6%94%B6) |

#### 3.1.2 卡片详情

| 功能编号 | F-102 |
| --- | --- |
| **功能名称** | 卡片详情页 |
| **优先级** | P1 |
| **用户故事** | 作为用户，我希望查看单张卡片的完整信息，包括限额、交易记录、卡片信息，以便管理该卡片 |
| **功能描述** | 展示单张卡片的详细信息，支持操作按钮 |
| **界面元素** | ① 卡片展示（卡面，可显隐卡号/CVV）<br>② 状态标签（使用中/已冻结）<br>③ 操作按钮：充值、冻结/解冻、、改限额、注销<br>④ 限额进度条（单笔/日/月）<br>⑤ 卡片信息：类型、BIN、等级、发卡日、到期日、月费、FX 费率<br>⑥ 该卡片的交易记录表格 |
| **验收标准** | [AC-113](#81-%E5%8A%9F%E8%83%BD%E9%AA%8C%E6%94%B6) |

### 3.1.3 KYC/KYB 认证与开卡

| 功能编号 | F-103 |
| --- | --- |
| **功能名称** | KYC/KYB 认证与开卡 |
| **优先级** | P0 |
| **用户故事** | 作为用户，我希望按步骤完成身份认证后开通虚拟卡，并能看到开卡需要的所有信息 |
| **功能描述** | 用户选择卡片类型后，进入回显 KYC/KYB 数据模块完成字段确认，审核通过后自动开卡 |

> **字段归属策略**：Interlace MoR 对接中，KYC/KYB 字段按业务属性拆分成两类：
> - ✅ **KYC/KYB 模块收集**：通用身份信息，一次采集终身可用
> - 🟢 **开卡申请补充**：业务属性、场景相关字段，仅在开卡时选填

##### 核心流程

```plaintext
用户注册 YASBee 账户
    ↓
选择卡片类型（BB/BZ）
    ↓
┌─ 个人卡 → KYC 模块 ──┐
│ ① 填写个人信息         │
│ ② 上传证件+自拍        │
│ ③ 填写地址+联系方式    │
│    ↕（必填 19 字段一次收齐）
└── ↓ ────────────────┘
┌─ 企业卡 → KYB 模块 ──┐
│ ① 填写公司信息         │
│ ② 法人+UBO信息        │
│    ↕（必填 + 补充字段一次收齐）
└── ↓ ────────────────┘
    ↓
系统预校验（必填字段完整性 + 格式校验）
    ↓
KYC/KYB 审核通过（审核结果处理见下方）
    ↓
┌─ 进入「开卡申请」步骤 ──┐
│ 补充开卡选填字段：       │
│ · 个人卡：occupation    │
│           annualSalary │
│           accountPurpose│
│           expectedMonthlyVolume│
│ · 企业卡：企业文档（按需上传）│
└── ↓ ────────────────┘
    ↓
选择 BIN / 等级 → 提交 Interlace 开卡
    ↓
┌─ PASSED → 创建持卡人 → 创建卡片 → 开卡成功
├─ REQUEST → 邮件通知具体修正建议 → 用户修正KYC/KYB重新提交开卡申请
├─ CANCELED → 清除记录 → 引导重新申请
└─ 超时（>1 分钟）→ 标记异常 → 运营告警 → 人工介入
```
```

##### 审核结果处理

| 审核结果 | 用户端提示 | 系统动作 |
| --- | --- | --- |
| **PASSED** | "认证成功，卡片即将开通" | 立即创建持卡人 + 创建卡片 |
| **REQUEST** | "部分信息需要修正：\[具体字段\]，请重新提交" | 展示 Interlace 返回的修正建议 |
| **CANCELED** | "认证未通过，请重新提交完整信息" | 清除该次提交记录，允许重新提交 |
| **超时（>1 分钟）** | "正在审核中，预计很快完成" | 后台告警，运营联系 Interlace |

> **连续失败策略**：用户连续失败 3 次后，触发人工客服介入流程（工单系统）。

##### Interlace KYC 必填字段（含归属标注）

```plaintext
POST /v3/cdd/submit-account-kyc

```

**必填字段（归属：KYC模块收集）：**

| # | Interlace 字段 | 类型 | 归属 | 格式/约束 |
| --- | --- | --- | :--: | --- |
| 1 | `accountId` | string (path) | ⚙️ **系统传递** | 注册后获取的账户 UUID |
| 2 | `firstName` | string | ✅ **KYC 模块** | 用户名字 |
| 3 | `lastName` | string | ✅ **KYC 模块** | 用户姓氏 |
| 4 | `dateOfBirth` | string (date) | ✅ **KYC 模块** | YYYY-MM-DD |
| 5 | `nationality` | string | ✅ **KYC 模块** | ISO 3166-1 alpha-2 二字码 |
| 6 | `nationalId` | string | ✅ **KYC 模块** | 证件号码 |
| 7 | `issueDate` | string (date) | ✅ **KYC 模块** | 证件签发日 YYYY-MM-DD |
| 8 | `expiryDate` | string (date) | ✅ **KYC 模块** | 证件到期日 YYYY-MM-DD |
| 9 | `idFrontId` | string | ✅ **KYC 模块** | 证件正面 fileId（需先上传） |
| 10 | `selfie` | string | ✅ **KYC 模块** | 自拍照片 fileId（需先上传） |
| 11 | `phoneNumber` | string | ✅ **KYC 模块** | 手机号含国家码 |
| 12 | `phoneCountryCode` | string | ✅ **KYC 模块** | 区号数字 |
| 13 | `sourceType` | string | ⚙️ **系统常量** | 固定值 "api" |
| 14 | `idType` | string | ✅ **KYC 模块** | 证件类型枚举 |
| 15 | `gender` | enum | ✅ **KYC 模块** | M / F |
| 16 | `address.addressLine1` | string | ✅ **KYC 模块** | 地址行1 |
| 17 | `address.city` | string | ✅ **KYC 模块** | 城市 |
| 18 | `address.country` | string | ✅ **KYC 模块** | ISO 3166-1 alpha-2 |
| 19 | `address.state` | string | ✅ **KYC 模块** | US/CA 二字码 |
| 20 | `address.postalCode` | string | ✅ **KYC 模块** | 邮编 |

**可选字段（含归属标注）：**

| # | Interlace 字段 | 类型 | 归属 | 格式/约束 |
| --- | --- | --- | :--: | --- |
| 1 | `middleName` | string | ✅ **KYC 模块选填** | 中间名 |
| 2 | `idBackId` | string | ✅ **KYC 模块建议** | 证件背面 fileId（建议 KYC 时一并收） |
| 3 | `address.addressLine2` | string | ✅ **KYC 模块选填** | 地址行2 |
| 4 | `occupation` | string | 🟢 **开卡申请选填** | 6 位 NAICS 职业代码 |
| 5 | `annualSalary` | string | 🟢 **开卡申请选填** | "金额 币种" |
| 6 | `accountPurpose` | string | 🟢 **开卡申请选填** | 例 "Living Expense" |
| 7 | `expectedMonthlyVolume` | string | 🟢 **开卡申请选填** | "金额 币种" |
| 8 | `ssn` | string | 🔵 **开卡申请（仅 US）** | 仅 US 用户需要 |

##### KYC 字段对照表（YASBee → Interlace，含归属）

| Interlace 字段 | 必填 | YASBee 对应 | 归属 | 处理说明 |
| --- | --- | --- | :--: | --- |
| `accountId` | ✅ | 注册后获取 | ⚙️ 系统传递 | 路径参数 |
| `firstName` | ✅ | First Name | ✅ **KYC 模块** | 直接映射 |
| `lastName` | ✅ | Last Name | ✅ **KYC 模块** | 直接映射 |
| `dateOfBirth` | ✅ | Date of Birth | ✅ **KYC 模块** | 格式化 YYYY-MM-DD |
| `nationality` | ✅ | Nationality | ✅ **KYC 模块** | 文本国名→ISO 二字码 |
| `nationalId` | ✅ | Passport/ID Number | ✅ **KYC 模块** | 直接映射 |
| `issueDate` | ✅ | — | ✅ **KYC 模块（新增）** | 证件签发日期 |
| `expiryDate` | ✅ | — | ✅ **KYC 模块（新增）** | 证件到期日期 |
| `idFrontId` | ✅ | Passport/ID Upload | ✅ **KYC 模块** | 文件→Upload API→fileId |
| `selfie` | ✅ | — | ✅ **KYC 模块（新增）** | 自拍照片，先上传→fileId |
| `phoneNumber` | ✅ | — | ✅ **KYC 模块（新增）** | 含国家码 |
| `phoneCountryCode` | ✅ | — | ✅ **KYC 模块（新增）** | 区号数字 |
| `sourceType` | ✅ | 固定值 "api" | ⚙️ 系统常量 | 后端写死 |
| `idType` | ✅ | — | ✅ **KYC 模块（新增）** | 证件类型枚举（6 种） |
| `gender` | ✅ | — | ✅ **KYC 模块（新增）** | M / F 枚举 |
| `address.addressLine1` | ✅ | Block + Street | ✅ **KYC 模块** | 拼接 Unit/Block/Street |
| `address.city` | ✅ | City | ✅ **KYC 模块** | 直接映射 |
| `address.country` | ✅ | Country | ✅ **KYC 模块** | 文本国名→ISO |
| `address.state` | ✅ | State/Province | ✅ **KYC 模块** | US/CA 二字码映射 |
| `address.postalCode` | ✅ | Postal Code | ✅ **KYC 模块** | 直接映射 |
| `middleName` | ⬜ | Middle Name | ✅ **KYC 模块选填** | 直接映射 |
| `idBackId` | ⬜ | — | ✅ **KYC 模块建议** | 建议 KYC 时一并收 |
| `address.addressLine2` | ⬜ | Unit Number | ✅ **KYC 模块选填** | 直接映射 |
| `occupation` | ⬜ | Occupation Description | 🟢 **开卡申请选填** | 文本→NAICS 映射 |
| `annualSalary` | ⬜ | — | 🟢 **开卡申请选填** | 可传默认值 |
| `accountPurpose` | ⬜ | Purpose of Account | 🟢 **开卡申请选填** | 直接映射 |
| `expectedMonthlyVolume` | ⬜ | Expected Monthly Trading Volume | 🟢 **开卡申请选填** | 格式化拼接 |
| `ssn` | ⬜ 条件 | — | 🔵 **开卡申请（仅 US）** | 仅 US 用户需要 |

##### 必须改造的字段（含归属标注）

**需新增的必填字段（全部归入 KYC 模块）：**

| 新增字段 | 归属 | 建议 UI 位置 | 说明 |
| --- | :--: | --- | --- |
| `issueDate`（证件签发日） | ✅ **KYC 模块** | 证件采集区 | 日期选择器 YYYY-MM-DD |
| `expiryDate`（证件到期日） | ✅ **KYC 模块** | 证件采集区 | 日期选择器 YYYY-MM-DD |
| `selfie`（自拍照） | ✅ **KYC 模块** | 证件采集区新增 | 用户自拍上传 → Upload API → fileId |
| `phoneNumber` + `phoneCountryCode` | ✅ **KYC 模块** | 联系方式区 | 手机号输入 + 区号下拉 |
| `idType`（证件类型枚举） | ✅ **KYC 模块** | 证件采集区 | 6 种枚举 |
| `gender`（性别） | ✅ **KYC 模块** | 个人信息区 | M / F 枚举选择 |
| `address` 对象（addressLine1/city/country/state/postalCode） | ✅ **KYC 模块** | 地址信息区 | 完整地址录入 |

**需改造的已有字段（4 项）：**

| 改造项 | 说明 |
| --- | --- |
| 国家名→ISO 二字码 | 建立映射表（~200 条），涉及 nationality、address.country |
| 文件上传流程 | 上传→Upload API→fileId 中间层，涉及 idFrontId、selfie |
| 地址字段状态调整 | address 子字段从可选改为必填，addressLine1/city/country/state/postalCode 全要 |
| gender 从无到有 | KYC 表单新增性别选择 |

**字段归属汇总：**

| 模块 | 归属 | 字段 |
| --- | :--: | --- |
| KYC 模块（必填） | ✅ | firstName / lastName / dateOfBirth / nationality / nationalId / gender / idType / issueDate / expiryDate / idFrontId / selfie / phoneNumber / phoneCountryCode / address 对象 / accountPurpose |
| KYC 模块（选填） | ✅ | middleName / idBackId / addressLine2 |
| 开卡申请（选填） | 🟢 | occupation / annualSalary / expectedMonthlyVolume |
| 开卡申请（仅 US） | 🔵 | ssn |

> **字段变更说明（相比 v2 版本）：**
> * `accountPurpose` 从「可选放至开卡」改为「KYC 模块必填」— 此字段为新 KYC 必填
> * `occupation` / `annualSalary` / `expectedMonthlyVolume` → 开卡时补充，不进 KYC
> * `ssn` → 仅 US 用户在开卡时补充
    


##### KYC 特殊处理字段说明

| 字段 | 特殊需求 | 处理方式 |
| --- | --- | --- |
| `nationality` | ISO 二字码 | 国家名→ISO 映射表（~200 条） |
| `idFrontId` / `selfie` | 需先上传文件 | 后端流程：用户上传 → 调 Upload API → 拿 fileId → 代入 KYC 请求 |
| `idType` 枚举值 | 需对齐 Interlace | 前端显示可用选项，后端不做额外映射 |

##### KYB 模块字段说明（企业认证）

##### Interlace KYB 必填字段（含归属标注）

```plaintext
POST /v3/cdd/submit-account-kyb

```

**必填字段（归属：KYB 模块收集）：**

| # | Interlace 字段 | 类型 | 归属 | 格式/约束 |
| --- | --- | --- | :--: | --- |
| 1 | `companyName` | string | ✅ **KYB 模块** | 公司法定全称 |
| 2 | `registrationNumber` | string | ✅ **KYB 模块** | 注册号（全局唯一） |
| 3 | `countryCode` | string | ✅ **KYB 模块** | ISO 3166-1 alpha-2 国家代码 |
| 4 | `industry` | string | ✅ **KYB 模块** | 6 位 NAICS 行业代码 |
| 5 | `website` | string | ✅ **KYB 模块** | 官网 URL，http(s)://，无则填 "N/A" |
| 6 | `companyNameEn` | string | ✅ **KYB 模块选填** | 公司英文名 |
| 7 | `registeredAddress` | string | ✅ **KYB 模块** | 注册地址 |
| 8 | `businessAddress` | string | ✅ **KYB 模块** | 营业地址 |
| 9 | `phoneNumber` | string | ✅ **KYB 模块** | 公司电话 |
| 10 | `email` | string | ✅ **KYB 模块** | 公司邮箱 |
| 11 | `sourceType` | string | ⚙️ **系统常量** | 固定值 "api" |
| 12 | `accountId` | string | ⚙️ **系统传递** | 注册后获取的账户 UUID |
| 13 | `uboList[].uboFirstName` | string | ✅ **KYB 模块** | 受益人名字 |
| 14 | `uboList[].uboLastName` | string | ✅ **KYB 模块** | 受益人姓氏 |
| 15 | `uboList[].uboGender` | enum | ✅ **KYB 模块** | M / F |
| 16 | `uboList[].uboCountryCode` | string | ✅ **KYB 模块** | ISO 3166-1 alpha-2 |
| 17 | `uboList[].uboIdType` | enum | ✅ **KYB 模块** | PASSPORT / CN-RIC / HK-HKID / DLN / Government-Issued ID Card |
| 18 | `uboList[].uboIdNumber` | string | ✅ **KYB 模块** | 证件号码 |
| 19 | `uboList[].uboDob` | string (date) | ✅ **KYB 模块** | YYYY-MM-DD |
| 20 | `fileIds[]` | array | 🟢 **开卡申请补充** | 企业文档 fileId 列表（按需上传） |

##### KYB 字段对照表（YASBee → Interlace，含归属）

#### 公司级别字段

| Interlace 字段 | YASBee 对应 | 归属 | 处理说明 |
| --- | --- | :--: | --- |
| `companyName` | Company Name | ✅ **KYB 模块** | 直接映射 |
| `companyNameEn` | — | ✅ **KYB 模块选填** | Interlace 可选，需确认是否存储英文名 |
| `registrationNumber` | Registration Number | ✅ **KYB 模块** | 每个 API Client 唯一，不可重复提交 |
| `countryCode` | Incorporate Jurisdiction | ✅ **KYB 模块** | 司法管辖区→ISO 二字码 |
| `industry` | Industry | ✅ **KYB 模块** | YASBee 行业文本→NAICS 6 位码 |
| `website` | Website | ✅ **KYB 模块** | 直接映射 |
| `registeredAddress` | Registered Address | ✅ **KYB 模块** | 直接映射 |
| `businessAddress` | Business Address | ✅ **KYB 模块** | 直接映射 |
| `phoneNumber` | — | ✅ **KYB 模块（新增）** | 公司联系电话 |
| `email` | Company Email | ✅ **KYB 模块** | 直接映射 |
| `sourceType` | 固定值 "api" | ⚙️ 系统常量 | 后端写死 |
| `accountId` | 注册后获取 | ⚙️ 系统传递 | 注册子账户后获得 |

#### UBO（最终受益人）字段

| Interlace 字段 | YASBee 对应 | 归属 | 处理说明 |
| --- | --- | :--: | --- |
| `uboFirstName` | 股东 First Name | ✅ **KYB 模块** | 直接映射 |
| `uboLastName` | 股东 Last Name | ✅ **KYB 模块** | 直接映射 |
| `uboGender` | — | ✅ **KYB 模块（新增）** | 股东信息新增 M/F 枚举 |
| `uboCountryCode` | 股东 Nationality | ✅ **KYB 模块** | 文本国名→ISO 二字码 |
| `uboIdType` | 股东证件类型 | ✅ **KYB 模块** | 需枚举对齐（5 种） |
| `uboIdNumber` | 股东证件号码 | ✅ **KYB 模块** | 直接映射 |
| `uboDob` | — | ✅ **KYB 模块（新增）** | 股东新增出生日期 YYYY-MM-DD |

#### 文件上传

| Interlace 字段 | YASBee 对应 | 归属 | 处理说明 |
| --- | --- | :--: | --- |
| `fileIds[]` | 企业文档上传（8 种） | 🟢 **开卡申请补充** | 开卡时按需上传，先调 Upload API 获取 fileId |

#####  KYB 缺失字段（已全部纳入 KYB 模块 + 开卡补充）

| # | 缺失字段 | 归属 | 说明 |
| --- | --- | :--: | --- |
| 1 | `companyPhoneNumber` | ✅ **KYB 模块（新增）** | 公司信息区新增联系电话输入框 |
| 2 | `uboGender`（受益人性别） | ✅ **KYB 模块（新增）** | 股东信息区新增 M/F 选择器 |
| 3 | `uboDob`（受益人出生日期） | ✅ **KYB 模块（新增）** | 股东信息区新增日期选择器 YYYY-MM-DD |
| 4 | `uboIdType`（受益人证件类型对齐） | ✅ **KYB 模块（新增）** | 股东证件区新增下拉枚举选择器，5 种类型 |
| 5 | `fileIds[]`（企业文档） | 🟢 **开卡申请补充** | 开卡时根据 BIN/等级要求按需上传 |

##### KYB 特殊处理字段

| 字段 | 特殊需求 | 处理方式 |
| --- | --- | --- |
| `registrationNumber` | **全局唯一** | 同一个 API Client 下不能重复提交，需要后端做幂等处理 |
| `countryCode` | ISO 二字码 | 建立司法管辖区→ISO 映射表 |
| `industry` | NAICS 6 位码 | 建立 YASBee 行业→NAICS 映射表 |
| `uboList` | 至少 1 人 | 确保表单至少有一个股东信息填写完整 |
| `uboCountryCode` | ISO 二字码 | 复用国家映射表 |

| `fileIds[ ]` | 先传后提 | 8 种企业文档逐个调 Upload API，收集 fileId 数组 |

#### 3.1.4 卡片操作系列

| 功能编号 | 操作 | 优先级 | 验收标准 |
| --- | --- | --- | --- |
| F-150 | 充值 | P0 | [AC-201](#81-%E5%8A%9F%E8%83%BD%E9%AA%8C%E6%94%B6) |
| F-151 | 冻结/解冻 | P0 | [AC-202](#81-%E5%8A%9F%E8%83%BD%E9%AA%8C%E6%94%B6) |
| F-153 | 修改限额 | P1 | [AC-203](#81-%E5%8A%9F%E8%83%BD%E9%AA%8C%E6%94%B6) |
| F-154 | 注销卡片 | P0 | [AC-204](#81-%E5%8A%9F%E8%83%BD%E9%AA%8C%E6%94%B6) |
| F-155 | 自助解冻 | P0 | [AC-205](#81-%E5%8A%9F%E8%83%BD%E9%AA%8C%E6%94%B6) |

**冻结/解冻规则**：

*   用户主动冻结 → 无验证要求，可随时解冻
    
*   风控冻结 → 需身份验证（生物识别/OTP）
    
*   卡片过期 → 不可自助解冻，引导补发新卡(后续版本迭代)
    

---

### 3.2 充值模块

#### 3.2.1 充值功能（F-201）

| 字段 | 值 |
| --- | --- |
| **优先级** | P0 |
| **用户故事** | 作为用户，我希望通过 Crypto 或 Fiat 方式为卡片充值，且实时到账 |
| **充值方式** | Crypto（USDT/USDC）、Fiat（银行转账/线上支付）、内部互转 |
| **到账速度** | Crypto ≤ 10 秒；Fiat 即时；内部互转 实时 |
| **手续费** | 0%（免费） |
| **前置条件** | 用户至少持有一张活跃卡片 |

**充值路由**：

| 充值方式 | 底层逻辑 |
| --- | --- |
| Crypto | USDT/USDC → 实时汇率换汇 USD → 到账 |
| Fiat 线上支付 | 银行转账 → 即时到账 |
| Fiat 银行转账 | T+1 ~ T+3（视地区） |
| 内部互转 | 卡片间余额划转，实时 |

#### 3.2.2 费用结算方式

| 费用类型 | 结算周期 | 备注 |
| --- | --- | --- |
| 返点（Rebate） | **月结** | 按月度消费量计算返佣 |
| KYC 复核费用 | **按次扣费** | $0.75/次（仅需 Interlace 重审时） |
| 月卡管理费 | **月结** | — |
| 交易失败/拒付率惩罚 | **月结** | 拒付率 ≥ 5% 时额外扣 $0.50/笔 |

---

### 3.3 交易与对账模块

#### 3.3.1 交易记录（F-301）

| 字段 | 值 |
| --- | --- |
| **优先级** | P0 |
| **展示字段** | 交易时间、商户名称、卡号后4位、交易金额（USD）、手续费、交易状态、失败原因 |
| **数据来源** | Interlace Webhook 实时推送 |

#### 3.3.2 对账（F-302）

| 字段 | 值 |
| --- | --- |
| **优先级** | P1 |
| **触发方式** | 每日自动对账，差异标记告警 |
| **对账内容** | YASBee 内部记录 vs Interlace 对账文件 |

---

### 3.4 费用与返佣模块

#### 3.4.1 费用结构（F-401）

**发卡方费用（Interlace → YASBee）：**

| 费用项 | 费率 | 结算方式 |
| --- | --- | --- |
| 虚拟卡发卡费 | $0.30/张 | 月结 |
| 月费 | $0.12~$0.25/卡/月 | 月结（卡片正常状态） |
| 交易费（国内） | $0.1 | 逐笔(BB/BZ) |
| 交易费（国际） | $0.2 | 逐笔(BB/BZ) |
| FX Fee（BB-BIN 加拿大） | 1.5% | 逐笔 |
| FX Fee（BZ-BIN 美国） | Pass through + 5bps | 逐笔 |
| Apple Pay 授权费 | 0.20% | 月结（开通后） |
| 充值手续费 | 0%（免费） | — |

**惩罚类费用****：**

| 费用项 | 费率 | 触发条件 |
| --- | --- | --- |
| 退款手续费 | 2% | 用户发起退款 |
| Chargeback（争议） | $35/笔 | 线下运营处理 |
| 失败交易费 | $0.50/笔 | 月度拒付率 ≥ 5% |

**拒付率计算逻辑**：

```plaintext
拒付率 = 当月拒付交易数 ÷ 当月总交易数

阈值：5%
  - < 5% → 不收失败交易费
  - ≥ 5% → 所有失败交易按 $0.50/笔 收费

失败原因包括：余额不足、风控拒绝、卡状态异常（冻结/过期/注销）

```

**返佣阶梯：**

| 月消费量 | 返佣比例 |
| --- | --- |
| $300K ~ $1M | 0.1% |
| $1M ~ $5M | 0.3% ~ 0.5% |
| $5M ~ $10M | 0.5% ~ 1% |
| \> $10M | 待协商 |

> **返佣方式待确认**：直接减免费用 / 现金返还 / 抵扣下月账单

#### 3.4.2 Chargeback 业务场景（F-402）

**Chargeback  完整处理流程：**

| 阶段 | 时间窗口 | 操作 |
| --- | --- | --- |
| 用户发起争议 | D0 | 客服受理，创建工单 |
| YASBee 初步判断 | D0 ~ D1 | 场景分类 + 证据收集 |
| 提交 Interlace（如需） | D1 ~ D3 | 打包证据提交仲裁 |
| Interlace 处理 | D3 ~ D93 | 90个工作日（按 Visa/MC 规则） |
| 结果通知用户 | D93~ D100 | 胜负判定 + 资金处理 |

**Chargeback 费用责任矩阵**：

| 场景 | $35 由谁承担 | YASBee 是否代付 | 备注 |
| --- | --- | --- | --- |
| 未授权交易（用户属实） | Interlace 豁免或商户承担 | 否 | YASBee 不垫付 |
| 未授权交易（误报） | 用户承担 | 是 | 建议展示费用说明 |
| 重复扣款 | 商户/Interlace | 否 | 服务端操作退款 |
| 欺诈交易（属实） | Interlace 豁免 | 否 | 风控拦截成功 |
| 欺诈交易（误报） | 用户/商户 | 是 | 需人工审核 |

---

### 3.5 风控与安全模块

#### 3.5.1 风控功能总览（F-501 ~ F-506）

| 功能编号 | 功能 | 优先级 |
| --- | --- | --- |
| F-501 | 交易风控检查（Interlace 侧执行） | P0 |
| F-502 | 错误码映射（6 种场景 → 用户端友好提示） | P0 |
| F-503 | Soft Decline / 3DS 验证流程 | P1 |
| F-504 | 自助解冻（按冻结原因执行不同策略） | P0 |
| F-505 | 拒付率监控（月度 ≥ 5% 预警） | P0 |
| F-506 | 限额管控（YASBee 自控等级额度体系） | P1 |

#### 3.5.2 错误码映射（F-502）

| Interlace 返回码 | 含义 | 用户端显示 | 建议动作 |
| --- | --- | --- | --- |
| INSUFFICIENT\_BALANCE | 余额不足 | "卡片余额不足，请充值" | 引导充值 |
| CARD\_FROZEN | 卡片已冻结 | "卡片已被冻结，请在 App 中解冻" | 引导自助解冻 |
| RISK\_DECLINED | 风控拒绝 | "交易存在风险，请验证身份" | 弹 3DS 验证 |
| CARD\_EXPIRED | 卡片已过期 | "卡片已过期，请申请新卡" | 引导补发新卡 |
| CARD\_CLOSED | 卡片已注销 | "卡片已注销" | 引导重新开卡 |
| INVALID\_AMOUNT | 超出限额 | "该笔交易超出限额" | 显示限额信息 |

#### 3.5.3 自助解冻流程（F-504）

```plaintext
用户收到"卡片已冻结"通知
    ↓
进入 YASBee App → 卡片详情 → 解冻
    ↓
系统识别冻结原因
    ↓
┌─ 用户主动冻结 → 直接解冻（无验证要求）
├─ 风控冻结 → 身份验证（3DS）→ 解冻
└─ 卡片过期 → 不可自助解冻 → 引导补发新卡

```

**解冻策略详细说明**：

#### 3.5.4 Apple Pay/Google Pay 3DS 验证流程（F-503）

**触发条件**：用户绑定Apple Pay/Google Pay，interlace发送验证码给YASBe，YASBe发送邮件携带验证码给用户，用户回填到Apple/Goole内。有效期5分钟。

---

### 3.6 等级与限额模块（F-601）

**YASBee 自行控制用户卡片等级，不依赖 Interlace 端。**

| 等级 | 单笔限额 | 日限额 | 月限额 | 升级条件 |
| --- | --- | --- | --- | --- |
| Lv1 新用户 | $500 | $1,000 | $5,000 | 完成 KYC |
| Lv2 标准 | $2,000 | $5,000 | $20,000 | 使用 30 天 + 10 笔以上 |
| Lv3 高级 | $5,000 | $15,000 | $50,000 | 月消费 > $5K，风控评分高 |
| Lv4 VIP | $10,000 | $30,000 | $100,000 | 人工审核 + 补充资料 |

> 具体额度数值需结合 YASBee 产品定价和风控策略进一步确认。

**晋升机制**：满足条件后 24 小时内自动晋升或触发人工审核。

---

### 3.7 BIN 管理（F-701）

| BIN | 地区 | Apple Pay/GPay | 支付宝 | 实体卡 | FX 费率 |
| --- | --- | --- | --- | --- | --- |
| BB-BIN | 🇨🇦 加拿大 | ✔支持 | ❌ | ❌ | 1.5% |
| BZ-BIN | 🇺🇸 美国 | ❌ 暂不支持 | ❌ | ❌ | Pass through + 5bps |

## 4. 用户余额与结算

| 项目 | 说明 |
| --- | --- |
| **Card Balance（卡余额）** | 卡片当前可用额度，用户在 App 中看到的就是这个 |
| **Ledger Balance** | YASBee 内部记账用，不对外展示 |
| **结算货币** | USD |
| **多币种支付** | Interlace 底层处理换汇 |
| **余额更新** | 实时更新（Webhook 触发 ≤ 3 秒） |

---

## 5. 非功能需求

### 5.1 性能指标

| 指标 | 目标值 |
| --- | --- |
| KYC 提交 → 审核通过 | ≤ 1 分钟（正常情况） |
| 充值到账延迟（Crypto） | 链上确认后 ≤ 10 秒 |
| 充值到账延迟（Fiat） | Real-time |
| 余额实时更新延迟 | ≤ 3 秒（Webhook 触发） |
| 系统可用性 | 99.9% |
| 对账完成时间 | 每日 T+1 08:00 前 |

### 5.2 安全要求

| 要求 | 说明 |
| --- | --- |
| 证件文件加密 | TLS 1.3 + 服务端加密存储 |
| API 凭证加密 | Interlace 凭证加密存储 |
| 敏感数据脱敏 | 卡号/CVV 前端掩码展示 |
| 数据传输安全 | 全链路 HTTPS |

### 5.3 合规要求

| 要求 | 说明 |
| --- | --- |
| KYC/KYB 数据保留 | 按当地法规（建议 5 年） |
| 用户数据跨境 | 征得用户同意，签署 DPA |
| 可疑交易上报 | 按当地监管要求 |

---

## 6. 依赖关系与里程碑

### 6.1 外部依赖

| 依赖方 | 依赖项 | 计划完成 | 备注 |
| --- | --- | --- | --- |
| Interlace | 完整 API 文档（含所有字段定义） | 接入前 | 需获取正式文档 |
| Interlace | Sandbox 环境开通 | 开发前 | 用于联调 |
| Interlace | Webhook 回调地址配置 | 测试前 | 需公网可达 |
| Interlace | 生产环境 API Key | 验收前 | 隔离测试与生产 |

### 6.2 内部依赖

| 模块 | 依赖项 | 说明 |
| --- | --- | --- |
| KYC/KYB | 文件上传服务（支持图片压缩） | 自拍/证件图片处理 |
| 充值 | Crypto Connect 通道 | USDT/USDC 充值 |
| 充值 | Fiat 支付通道（银行合作） | 法币充值 |
| 风控 | 短信/邮件服务（OTP） | 身份验证 |
| 对账 | 定时任务调度系统 | 每日自动对账 |

### 6.3 里程碑

| 阶段 | 内容 | 目标时间 |
| --- | --- | --- |
| M1 | PRD 评审通过，确认字段映射 | 第 1 周 |
| M2 | Interlace Sandbox 联调完成 | 第 3 周 |
| M3 | KYC/KYB 全流程功能开发完成 | 第 5 周 |
| M4 | 充值、消费、交易记录全流程联调 | 第 7 周 |
| M5 | 风控流程（3DS、解冻、错误码）验证 | 第 8 周 |
| M6 | 对账功能 + UAT 测试 | 第 9 周 |
| M7 | 生产环境部署 + 灰度发布 | 第 10 周 |
| M8 | 全量上线 | 第 11 周 |

---

## 7. 风险矩阵

| 风险 | 等级 | 影响 | 缓解措施 |
| --- | --- | --- | --- |
| Interlace API 字段变更 | 中 | 开发返工 | 提前锁定文档版本，接口加版本控制 |
| KYC 审核超时导致用户体验差 | 高 | 转化率下降 | 增加状态提示 + 运营告警 + 人工兜底 |
| 拒付率超过 5% 触发惩罚 | 高 | 额外成本 | 风控阈值提前预警（第 4% 触发告警） |
| Webhook 延迟导致余额更新不及时 | 中 | 用户投诉 | 定时轮询兜底 + 监控告警 |
| 合规政策变更 | 低 | 需调整功能 | 法务定期 review |

---

## 8. 验收标准

### 8.1 功能验收

| ID | 验收项 | 验收条件 |
| --- | --- | --- |
| AC-101 | 多卡展示 | 用户持有 3 张卡时可正常并列展示，余额正确累加 |
| AC-102 | KYC 提交到开卡 | 端到端 ≤ 1 分钟（审核通过情况下） |
|| AC-103 | KYC 必填字段覆盖 | 全部 19 个 Interlace 必填字段正确映射，字段校验通过 |
| AC-104 | 自拍上传 | selfie 字段上传 → 系统处理流程可跑通 |
| AC-105 | 充值流程 | Crypto + Fiat 双通道充值均可正常到账，余额实时更新 |
| AC-106 | 交易失败提示 | 6 种错误码均映射为友好中文提示 |
| AC-107 | 自助解冻 | 用户主动冻结可直接解冻；风控冻结需身份验证 |
| AC-108 | 等级晋升 | 满足条件后 24 小时内自动晋升 |
| AC-109 | Apple Pay 绑定 | 卡片信息传到 YASBee → 展示给用户 → 跳转钱包流程正常 |
| AC-110 | Soft Decline / 3DS | 高风险交易触发 3DS，验证通过后继续交易，失败则取消 |
| AC-111 | Webhook 稳定性 | 对账差异率 < 0.01% |
| AC-112 | 对账自动化 | 每日 T+1 08:00 前完成，无人工介入 |
| AC-113 | 卡片详情页 | 卡片信息完整展示，卡号/CVV 可切换显隐，限额进度条数据正确 |
| AC-201 | 充值功能 | Crypto + Fiat 双通道充值到账正常，余额实时更新 |
| AC-202 | 冻结/解冻 | 主动冻结可直接解冻；风控冻结需身份验证；过期卡片不可解冻 |
| AC-203 | Apple Pay / Google Pay 绑定 | 卡片信息传到 YASBee → 展示给用户 → 跳转钱包绑定流程正常 |
| AC-204 | 修改限额 | 用户可修改卡片限额，新限额对下一笔交易生效 |
| AC-205 | 注销卡片 | 注销后卡片不可再用，余额原路退回 |
| AC-206 | 自助解冻 | 按冻结原因执行对应解冻策略，临时解锁机制生效 |

### 8.2 上线检查清单

*   [ ] KYC/KYB 端到端流程测试通过（覆盖全部字段映射）
    
*   [ ] 充值与消费全流程通过
    
*   [ ] 卡片冻结/解冻/注销功能完整
    
*   [ ] 6 种交易错误码映射验证通过
    
*   [ ] 费用计算准确无误
    
*   [ ] 日对账自动完成无差异
    
*   [ ] 3DS 验证流程全场景测试通过
    
*   [ ] 连续 3 次 3DS 失败锁定逻辑验证
    
*   [ ] 拒付率告警阈值测试（4% 预警）
    
*   [ ] 合规文档（DPA）签署完成
    

---

## 9. 附录

### 9.1 关键映射表清单

开发前需建立以下映射表，用于前端表单字段在提交至 Interlace 前的自动转换：

| 映射表 | 源数据 | 目标格式 | 预计条目数 | 备注 |
| --- | --- | --- | --- | --- |
| 国家 → ISO 二字码 | 用户选择的国家名 | ISO 3166-1 alpha-2 | ~200 | Interlace 要求的标准格式 |
| 州/省 → 二字码 | 用户选择的州名 | USPS/CA 标准码 | ~60 | 仅 US/CA 用户 |
| 证件类型枚举映射 | 中文证件类型名 | Interlace 枚举值 | 6 | PASSPORT/CN-RIC/HK-HKID/DLN/Government-Issued ID Card/EU Residency Permit |
| 职业 → NAICS 码 | 用户输入的职业文本 | NAICS 6位行业码 | ~1,000+ | 建议前端做模糊搜索，后端映射 |
| 行业 → NAICS 码 | 用户输入的行业文本 | NAICS 6位行业码 | ~1,000+ | 同上，仅 KYB |
| 电话号码区号 | 用户选择的地区 | 国际电话区号（如+86） | ~200 | 与 Country Code 联动 |

> **开发建议**：以上映射表建议使用静态 JSON 文件维护，前端预加载公共表（国家/区号），后端维护复杂映射（NAICS）。定期从 Interlace 最新文档同步枚举值。

### 9.2术语表

| 术语 | 中文 | 说明 |
| --- | --- | --- |
| MoR | 主商户（Master on Record） | Interlace 的发卡合作模式，YASBee 作为 Master-Merchant |
| Master-Merchant | 主商户 | 在 Interlace 体系下管理子商户/持卡人的顶层商户 |
| Infinity Account | 对公充值账户 | 用于 YASBee 向 Interlace 充值的公司级账户 |
| KYC | 个人身份认证 | Know Your Customer，个人用户认证流程 |
| KYB | 企业身份认证 | Know Your Business，企业用户认证流程 |
| UBO | 最终受益人 | Ultimate Beneficial Owner，持股 ≥ 25% 的自然人 |
| Soft Decline | 软拒绝 | 交易被风控暂缓，需 3DS 验证后重新提交 |
| Chargeback | 退单/争议 | 持卡人向发卡行发起的交易争议 |
| BIN | 银行卡识别码 | Bank Identification Number，卡号前 6 位 |
| NAICS | 北美行业分类系统 | North American Industry Classification System |