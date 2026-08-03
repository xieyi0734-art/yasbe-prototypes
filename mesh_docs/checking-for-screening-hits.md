---
updatedAt: 2025-12-17T10:33:08.000Z
---

Fetch the complete documentation index at: https://docs.mesh.complyadvantage.com/v2.1/llms.txt. Use this file to discover all available pages before exploring further.

# Checking for screening hits

Checking for hits after screening a customer

# Checking for screening hits

Checking for hits after screening a customer

You can determine whether a customer has any hits after screening using different approaches, depending on whether the screening was conducted asynchronously or synchronously.

### Checking for hits after asynchronous screening

#### Webhooks (recommended)

* Set up a webhook of type `WORKFLOW_COMPLETED` using the [Create a Webhook](https://docs.mesh.complyadvantage.com/reference/createwebhook#workflow_completed) API.
* Once the screening workflow completes, an update will be sent to the configured webhook URL.
* Refer to the `customer-screening.step_output.screening_result` field in the webhook payload to determine if any hits were found (`HAS_PROFILES`).

#### Polling

* After using the Create and Screen (Asynchronous) API, you’ll receive a `workflow_instance_identifier` in the response.
* Use this identifier to poll the [Get Status and Result of Onboarding](https://docs.mesh.complyadvantage.com/reference/getworkflowstate)  API.
* When the customer-screening step is complete, the `customer-screening.step_output.screening_result` field in the response will indicate whether any hits were found (`HAS_PROFILES`).

### Checking for hits and AML types after synchronous screening

* For Create and Screen (Synchronous) requests, the screening result is included directly in the API response.
* Refer to the `customer-screening.step_output.screening_result` field to see if any hits were found (`HAS_PROFILES`).
* Refer to the `customer-screening.step_output.aml_types` to see the AML types of the hits. AML types includes:
  * `SANCTION`
  * `FITNESS-PROBITY`
  * `WARNINGS`
  * `PEP_CLASS_1`
  * `PEP_CLASS_2`
  * `PEP_CLASS_3`
  * `PEP_CLASS_4`
  * `ADVERSE_MEDIA`
  * `ADVERSE-MEDIA-V2-PROPERTY`
  * `ADVERSE-MEDIA-V2-FINANCIAL-AML-CFT`
  * `ADVERSE-MEDIA-V2-FRAUD-LINKED`
  * `ADVERSE-MEDIA-V2-NARCOTICS-AML-CFTADVERSE-MEDIA-V2-VIOLENCE-AML-CFT`
  * `ADVERSE-MEDIA-V2-TERRORISM`
  * `ADVERSE-MEDIA-V2-CYBERCRIME`
  * `ADVERSE-MEDIA-V2-GENERAL-AML-CFT`
  * `ADVERSE-MEDIA-V2-REGULATORY`
  * `ADVERSE-MEDIA-V2-FINANCIAL-DIFFICULTY`
  * `ADVERSE-MEDIA-V2-VIOLENCE-NON-AML-CFT`
  * `ADVERSE-MEDIA-V2-OTHER-FINANCIAL`
  * `ADVERSE-MEDIA-V2-OTHER-SERIOUS`
  * `ADVERSE-MEDIA-V2-OTHER-MINOR`\ <br />