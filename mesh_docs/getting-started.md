---
updatedAt: 2026-02-20T17:43:39.000Z
---

Fetch the complete documentation index at: https://docs.mesh.complyadvantage.com/v2.1/llms.txt. Use this file to discover all available pages before exploring further.

# Getting Started

Getting started with your ComplyAdvantage Mesh API integration

# Getting Started

Getting started with your ComplyAdvantage Mesh API integration

<br />

This guide offers step-by-step instructions for integrating with the ComplyAdvantage Mesh API and addresses common use cases, including creating and screening customers, checking for hits, and viewing cases, alerts, and risks.

### Setting up your environment

#### API authentication

To begin using the ComplyAdvantage Mesh API, you’ll need credentials provided during onboarding. Your nominated API user should have received a welcome email containing instructions for setting up their password and specifying their organization name. These credentials are used to [generate an access token](https://docs.mesh.complyadvantage.com/reference/createtoken):

* username: The email address of the API user.
* password: The password created by the API user.
* realm: The organization name as stated in the welcome email.

```json Sample API authentication request
{
  "username": "apiuser@company.com",
  "password": "password",
  "realm": "organization name"
}
```

> ℹ️ API user best practices
>
> It is recommended to have a dedicated email address for your API user (e.g. <apiuser@companyname.com>) and have one API user per account. This will enable you to create tokens for each account without having to switch accounts.

#### Creating a customer screening configuration

> ❗️ Setting up screening configurations
>
> Screening configurations should be set up in collaboration with a compliance or risk team to ensure the appropriate screening lists are selected. These configurations can be updated at any time.

Customers are screened against pre-configured settings. Before creating and screening your first customer, you must set up a customer screening configuration. This can be done via ComplyAdvantage Mesh web application or the API. You can create multiple configurations and select the appropriate one for each customer during the screening process.

##### Create a customer screening configuration via the web application

* Follow the steps outlined in this [article](https://support.complyadvantage.com/hc/en-gb/articles/23169593842321-Create-a-screening-configuration).

##### Create a customer screening configuration via API

* Use the [create screening configuration](https://docs.mesh.complyadvantage.com/reference/createscreeningconfiguration) API.

> ℹ️ Customer screening configuration identifier
>
> After creating a customer screening configuration, make sure to note the `configuration_identifier`. This identifier is required when creating and screening customers.
>
> <Image align="center" alt="Example of a screening configuration identifier " border={false} caption="Example of a screening configuration identifier" src="https://files.readme.io/576209218c4d5463ce5d11db4d32004c3493d268ac84d1274a4e71abc8b001a5-image.png" width="300px" />