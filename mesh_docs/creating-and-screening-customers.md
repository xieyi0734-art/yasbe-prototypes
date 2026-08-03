---
updatedAt: 2025-12-17T10:33:11.000Z
---

Fetch the complete documentation index at: https://docs.mesh.complyadvantage.com/v2.1/llms.txt. Use this file to discover all available pages before exploring further.

# Creating and screening customers

How to create and screen individual or multiple customers

# Creating and screening customers

How to create and screen individual or multiple customers

<br />

Now that your [customer screening configuration](https://docs.mesh.complyadvantage.com/docs/getting-starte#creating-a-customer-screening-configuration) has been successfully set up, you can begin onboarding customers and screening them against the relevant configuration.

### Customer types

ComplyAdvantage Mesh supports screening for a variety of customer types, including:

* Persons
* Companies
* Undefined types: Includes entities such as vessels, aircraft, or other entities where the type is not specified.

### External identifiers

* Each customer within an account must have a unique `external_identifier`.
* This identifier is required for creating and screening a customer.
* Ideally, it should match the customer identifier used in your system such as a CRM.

### Creating and screening a single customer

Two different ways this can be done:

* Asynchronous screening: Use the [Create and Screen a Customer Asynchronously](https://docs.mesh.complyadvantage.com/reference/createcustomerandscreenasync) API.
* Synchronous screening: Use the [Create and Screen a Customer Synchronously](https://docs.mesh.complyadvantage.com/reference/createcustomerandscreensync) API.

> ℹ️ Asynchronous or synchronous screening
>
> Choose the screening method based on your use case.
>
> * Synchronous screening: Ideal for real-time onboarding workflows where low latency is critical.
> * Asynchronous screening: Suitable for high-volume screening scenarios, allowing processing of customers with remediation handled later.

> ❗️ Retrieving risks
>
> * To fetch detailed risks from the returned profiles, `alert_identifiers` must be retrieved.
> * For synchronous screening, you can include the `last_sync_step` parameter with a value of `ALERTING`.
>   * This triggers the alerting step during initial screening, eliminating the need for a separate call to retrieve alert identifiers.

For further details on constructing your screening request, refer to the step-by-step example below:

<Recipe slug="create-a-person" title="Create a person" />

### Batch create and screen customers

* For high-volume processing, use the [Batch Processing](https://docs.mesh.complyadvantage.com/reference/bulkuploaderpostv2batchprocessing#/) API.
* To prepare your batch file, refer to the instructions in [this article](https://support.complyadvantage.com/hc/en-gb/articles/24891341549073-Fields-used-when-batch-creating-customers).