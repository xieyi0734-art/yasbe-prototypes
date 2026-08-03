---
updatedAt: 2025-12-17T10:33:13.000Z
---

Fetch the complete documentation index at: https://docs.mesh.complyadvantage.com/v2.1/llms.txt. Use this file to discover all available pages before exploring further.

# Viewing screening results

Viewing cases, alerts, and risks after screening customers

# Viewing screening results

When a customer is screened and hits are found, cases and alerts are automatically generated. Risks can then be reviewed within the alerts. Cases, alerts and risks can be reviewed and remediated either via the ComplyAdvantage Mesh web application or by integrating with the API for use in your own case management system.

### Viewing cases and alerts in the ComplyAdvantage Mesh web application

* To review cases directly in the web application, follow the steps outlined in this [article](https://support.complyadvantage.com/hc/en-gb/articles/22694088419601-Reviewing-cases).

### Retrieving alerts using the ComplyAdvantage Mesh API

#### Retrieving alerts after asynchronous screening

##### Using webhooks (Recommended)

* Retrieve the `alert_identifier` from the `WORKFLOW_COMPLETED` webhook payload.
* Use the `alert_identifier` to fetch detailed risks using the [Get Risks Within an Alert](https://docs.mesh.complyadvantage.com/reference/getrisks) API.

##### Using polling

* Poll the [Get Status and Result of Onboarding](https://docs.mesh.complyadvantage.com/reference/getworkflowstate) API using the `workflow_instance_identifier`.
* Retrieve the `alert_identifier` from the response.
* Use the `alert_identifier` to fetch detailed risks using the [Get Risks Within an Alert](https://docs.mesh.complyadvantage.com/reference/getrisks) API.

#### Retrieving alerts after synchronous screening

* If `last_sync_step` is set to `ALERTING` in the request:
  * Retrieve the `alerting.identifier` directly from the Create and Screen (Synchronous) API response.
  * Use the `alert_identifier` to fetch detailed risks using the [Get Risks Within an Alert](https://docs.mesh.complyadvantage.com/reference/getrisks) API.
* If `last_sync_step` is not set:
  * Follow the same process outlined in the Asynchronous Screening section above to retrieve and view the alert.