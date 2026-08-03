---
updatedAt: 2025-12-17T11:03:58.000Z
---

Fetch the complete documentation index at: https://docs.mesh.complyadvantage.com/v2.1/llms.txt. Use this file to discover all available pages before exploring further.

# Key integration use cases

The choice of APIs to integrate with will depend on the specific outcomes you want to achieve

# Key integration use cases

<br />

The choice of APIs to integrate with will depend on the specific outcomes you want to achieve.

The main considerations include:

* **Case remediation** - Is this done using ComplyAdvantage Mesh?
* **Customer journey** - Are your customers onboarded and screened in real-time, or retrospectively?

### Remediation using ComplyAdvantage Mesh web application

**If you are creating and screening customers without the requirement of an immediate response, follow these steps:**

1. [Create and screen customers (asynchronously)](https://docs.mesh.complyadvantage.com/docs/creating-and-screening-customers#create-and-screen-a-single-customer).
2. View customers and remediate cases in the ComplyAdvantage Mesh web application.

**If you are creating customers in real-time and blocking them based on AML types, follow these steps:**

1. [Create and screen customers (synchronously)](https://docs.mesh.complyadvantage.com/docs/creating-and-screening-customers#creating-and-screening-a-single-customer)
2. [Check for screening hits and AML types.](https://docs.mesh.complyadvantage.com/docs/checking-for-screening-hits#checking-for-hits-and-aml-types-after-synchronous-screening)
3. View customer records and remediate cases in the ComplyAdvantage Mesh web application.

### Remediation using a case management system outside ComplyAdvantage Mesh

**If you are creating and screening customers without the requirement of an immediate response, follow these steps:**

1. [Create and screen customers (asynchronously)](https://docs.mesh.complyadvantage.com/docs/creating-and-screening-customers#create-and-screen-a-single-customer).
2. [Retrieve alerts and extract returned profile details.](https://docs.mesh.complyadvantage.com/docs/viewing-screening-results)
3. Import risk details into an external case management system.

**If you are creating customers in real-time and blocking them based on AML types, follow these steps:**

1. [Create and screen customers (synchronously).](https://docs.mesh.complyadvantage.com/docs/creating-and-screening-customers#create-and-screen-a-single-customer)
2. [Check for screening hits.](https://docs.mesh.complyadvantage.com/docs/checking-for-screening-hits)
3. [Retrieve alerts and extract returned profile details.](https://docs.mesh.complyadvantage.com/docs/viewing-screening-results)
4. Import risk details into your case management system.