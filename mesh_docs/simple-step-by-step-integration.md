---
updatedAt: 2026-06-08T11:17:05.000Z
---

Fetch the complete documentation index at: https://docs.mesh.complyadvantage.com/v2.1/llms.txt. Use this file to discover all available pages before exploring further.

# Simple step-by-step integration

Step-by-step guide for integrating customer onboarding and screening workflow

# 6 Step Integration Guide: Standard Customer Onboarding Screening and Monitoring Workflow

## Overview

This guide provides a streamlined, step-by-step approach to integrating with the ComplyAdvantage Mesh API for the standard customer onboarding screening and monitoring workflow.

**What you'll accomplish:**

* Authenticate and connect to the API
* Create and screen customers synchronously
* Set up a webhook to track case resolution
* Enable and disable ongoing monitoring
* Set up a webhook to be notified of new monitoring cases
* Update customer information when needed

## Prerequisites

Before starting your integration, ensure you have:

* **API Credentials**: Organisation name, API user email, and password (provided during onboarding)
* **API Base URL:** api.mesh.complyadvantage.com
* **Dedicated API User**:
  * Recommended to use a dedicated email (e.g. <api@yourcompany.com>)
  * To avoid needing to invoke an endpoint to switch operations between sandbox and production, we also recommend using a separate email for production and sandbox accounts
* **Screening Configuration**: Already created in the Mesh web application UI or via the create screening configuration endpoint

## Step 1: Authentication

### Generate an Access Token

ComplyAdvantage Mesh uses OAuth2 authentication. You'll need to obtain a bearer token.

**Endpoint:** `POST /v2/token`

**Required fields:**

* `realm`: The identifier for your organisation in Mesh. This can be found in your welcome email.
* `username`: API user email address
* `password`: API user password

**Response includes:**

* `access_token`: Use in the Authorization header as `Bearer {access_token}`
* `expires_in`: 86400 (24 hours)

**Important Notes:**

* Access tokens expire after **24 hours**
* Store the token securely in your application
* Implement automatic token refresh logic

*See Appendix A for code examples*

## Step 2: Create and Screen a Customer

This endpoint initiates the complete 'create and screen' workflow synchronously. The workflow consists of five steps:

1. **Customer Record Creation**: The Customer Record is created in Mesh
2. **Risk Scoring**: An initial Risk Score is calculated for the Customer
3. **Customer Screening**: The Customer is screened using your configured settings
4. **Alerts**: Alerts are generated based on the risk analysis
5. **Case Creation**: Cases are created for analyst review if matches are found

**Endpoint:** `POST /v2/workflows/sync/create-and-screen`

### Get Your Screening Configuration ID

Before making the API call, you'll need your screening configuration identifier:

1. Log in to the ComplyAdvantage Mesh web application
2. Navigate to **Settings > Screening Configurations**
3. Click into the relevant screening configuration
4. Copy the **configuration identifier** (you'll need this for the API request)

### Important: External Identifier

**Each customer within your account must have a unique `external_identifier`:**

* This identifier is **required** for creating and screening a customer
* Ideally, it should match the customer identifier used in your system (e.g., CRM customer ID)
* This allows you to link ComplyAdvantage records back to your internal systems
* The API will reject duplicate `external_identifier` values

### Required Request Fields

**For Individual Customers:**

* `customer.external_identifier`: Your unique customer ID
* Send either one of the following:
  * `customer.person.last_name`: Last name
  * `customer.person.full_name`: Full name
* `configuration.screening_configuration_identifier`: Your screening config ID
* `monitoring.entity_screening.enabled`: true or false\*

**For Company Customers:**

* `customer.external_identifier`: Your unique customer ID
* `customer.company.legal_name`: Company name
* `configuration.screening_configuration_identifier`: Your screening config ID
* `monitoring.entity_screening.enabled`: true or false\*

\*If ongoing monitoring is enabled:

* The customer will be rescreened every 24 hours against the latest version of the screening configuration
* New matches and updated profiles that have not been muted will generate cases automatically

You can find a full list of fields and their accepted formats: [Create and Screen Customer API documentation](/reference/createcustomerandscreensync)

**Optional but Important Fields**:

* The country and date of birth fields are optional, but they are useful in filtering out false positives.
* `last_sync_step` query parameter: By default, an API response will be generated at the 'SCREENING' stage, which will mean the process isn't complete and the results might not be immediately retrievable. To avoid this, set the `last_sync_step` query parameter to `'ALERTING'` in order to ensure an API response is only received once all the information is ready.

### Critical Response Fields to Store

**1. `customer_identifier`** (from `customer-creation.step_output`)

* A unique identifier generated by ComplyAdvantage for the customer
* **You MUST store this field** as part of the customer record in your internal systems
* Required to interact with many API endpoints (monitoring, case retrieval, etc.)

**2. `overall_level`** (from `initial-risk-scoring.step_output`)

* The API response will return a risk level based on your configured risk model
* Possible values: **LOW-RISK**, **MEDIUM-RISK**, **HIGH-RISK**, or **PROHIBITED**
* **Action**: Depending on your risk-based approach, you can decide to automatically offboard customers with a "Prohibited" risk level
* This risk level is calculated before screening and helps determine the screening profile applied

**3. `screening_result`** (from `customer-screening.step_output`)

* **`HAS_PROFILES`**: Customer has matched with one or more profiles in the database
  * **Action**: Pause the customer's onboarding until their matches have been remediated
  * Review the associated cases to determine if matches are genuine or false positives
* **`NO_PROFILES`**: Customer has no matches
  * **Action**: You can straight-through process (STP) the customer and proceed with onboarding

### Customer Data Format Reference

For a complete list of customer fields and their accepted formats, see the [Create and Screen Customer API documentation](/reference/createcustomerandscreensync).

*See Appendix B for request and response examples*

## Step 3: Set Up Webhook for Case Resolution

Webhooks provide real-time notifications when cases are updated, allowing you to automatically progress customers through onboarding once their cases are resolved.

**Endpoint:** `POST /v2/notifications/configurations/webhook`

### Register a CASE\_STATE\_UPDATED Webhook

This webhook notifies you whenever a case changes stage, such as when it moves from "Not Started" to "In Progress" to "False Positive" (resolved).

**Required fields:**

* `url`: Your webhook endpoint URL (must be HTTPS)
* `type`: "CASE\_STATE\_UPDATED"
* `name`: A name for this webhook configuration
* `is_active`: true

### Key Fields in Webhook Payload

**`customer.external_identifier`**

* Your unique customer identifier that links back to your system
* Use this to identify which customer the case update relates to

**`case_stage.decision_type`** (recommended)

The v2 webhook payload includes a `case_stage` object with a `decision_type` field. This is the recommended way to determine case outcomes:

* **`POSITIVE`**: Case resolved favourably (e.g., "False Positive", "Approved")
  * **Action**: Customer can progress in their onboarding
* **`NEGATIVE`**: Case resolved unfavourably (e.g., "True Match", "Rejected")
  * **Action**: Block or reject the customer
* **`null`** (no decision\_type): Case is still in progress or awaiting review
  * **Action**: Keep customer onboarding paused

**`case_state`** (deprecated)

The `case_state` field is deprecated. If you are still using it, the possible values include:

* **`CASE_STATE_POSITIVE_END_STATE`**: Case resolved favourably
* **`CASE_STATE_NEGATIVE_END_STATE`**: Case resolved unfavourably
* **`CASE_STATE_IN_PROGRESS`**: Case is still in progress
* **`CASE_STATE_NOT_STARTED`**: Case is awaiting review

Please migrate to using `case_stage.decision_type` instead.

*See Appendix C for webhook setup and implementation examples*

## Step 4: Disable Ongoing Monitoring

When you no longer need to monitor a customer (e.g., customer relationship ended, account closed), you can disable ongoing monitoring to stop generating new alerts and optimise costs.

**Endpoint:** `PATCH /v2/customers/{customer_identifier}/monitor`

**Request body:**

```json
{
  "entity_screening": {
    "enabled": false
  }
}
```

**Important**: Disabling monitoring means:

* The customer will no longer be rescreened against updated databases
* No new monitoring alerts will be generated
* Existing cases remain accessible for historical audit purposes
* You can re-enable monitoring at any time if needed

### Re-Enable Monitoring

To re-enable monitoring, use the same endpoint with `enabled: true`

*See Appendix D for request and response examples*

## Step 5: Update Customer Information (Optional)

If a customer's information changes after onboarding (e.g., address update, name change, new products), you can update their record and recalculate their risk score.

**Endpoint:** `PATCH /v2/customers/{customer_identifier}/workflows/sync/update-and-rescore`

This endpoint initiates the synchronous 'update and re-score' workflow, which consists of two steps:

1. **Customer Record Update**: The customer record is updated
2. **Risk Scoring**: The risk score is recalculated for the updated customer

### When to Update Customer Information

Consider updating customer records when:

* Customer provides updated contact details
* Address changes (particularly to higher/lower risk jurisdictions)
* New products or services are added to the relationship
* Nationality or citizenship status changes
* Business structure changes (for company customers)

### Important Notes

* Updates trigger a risk score recalculation automatically
* If the new risk level crosses configured thresholds, it may trigger additional screening or case creation
* Customer monitoring settings remain unchanged unless explicitly updated
* The endpoint is idempotent - you can safely retry the same request if errors occur

*See Appendix E for request and response examples*

## Step 6: Set Up Webhook Notification for a New Ongoing Monitoring Case (Optional)

### Register a CASE\_CREATED Webhook

This webhook notifies you whenever a case is created. You can use this webhook to be notified when your customer has a new ongoing monitoring case awaiting review.

**Required fields:**

* `url`: Your webhook endpoint URL (must be HTTPS)
* `type`: "CASE\_CREATED"
* `name`: A name for this webhook configuration
* `is_active`: true

### Key Fields in Webhook Payload

**`customer.external_identifier`**

* Your unique customer identifier that links back to your system
* Use this to identify which customer the case update relates to

**`case_type: CUSTOMER_MONITORING`**

* This field-value combination identifies that the webhook is relevant to an ongoing monitoring case

## Error Handling Best Practices

### Common Error Codes

| Status Code | Meaning      | Action                                                   |
| ----------- | ------------ | -------------------------------------------------------- |
| 400         | Bad Request  | Check request format, required fields, and field formats |
| 401         | Unauthorised | Refresh your access token                                |
| 403         | Forbidden    | Verify API user has required permissions                 |
| 404         | Not Found    | Verify customer\_identifier or case\_identifier exists   |
| 409         | Conflict     | Duplicate external\_identifier - use unique values       |
| 429         | Rate Limit   | Implement exponential backoff and request queuing        |
| 500         | Server Error | Retry with exponential backoff (max 3 attempts)          |

### Handling Duplicate External Identifiers

If you receive a 409 Conflict error, the response will include the existing `customer_identifier`. Check if this is a legitimate duplicate (e.g., resubmission) and either retrieve the existing customer or use a different `external_identifier` for a new customer.

*See Appendix F for retry logic implementation*

## Performance Optimisation

### Caching Strategy

* **Configuration Management:** Store your screening configuration ID as an application constant or environment variable - it rarely changes and doesn't need to be retrieved via API
* **Don't cache access tokens beyond expiry** - Refresh proactively at 23 hours

### Rate Limit Management

* The default rate limit is **300 requests per minute**
* This limit can be changed upon request - contact your support team
* Monitor your API usage and stay within rate limits
* Implement request queuing for high-volume scenarios
* Use batch operations where available
* Spread requests across time to avoid bursts

### Response Time Optimisation

* The synchronous create and screen endpoint (/sync) typically responds in 1-3 seconds
* For slower responses, implement timeout handling (suggest 10 second timeout)
  * For applications that cannot wait for API responses, use the asynchronous create-and-screen endpoint (/async) which returns immediately and delivers results via webhook notification, eliminating timeout risks and improving user experience
* Use webhooks for asynchronous processing of long-running operations

## Testing Your Integration

### Test in your Sandbox Account

### Sample Test Cases

**1. Clean Customer (No Matches)**

* Use a test name like "Test CleanUser"
* Date of birth: 1990-01-01
* Expected: `screening_result: "NO_PROFILES"`

**2. Potential Match**

* Use a test name like "Victor Bout"
* Date of birth: 1967-01-13
* Expected: `screening_result: "HAS_PROFILES"` with alerts

### Webhook Testing

Use tools like [webhook.site](https://webhook.site/) to test webhook delivery during development:

1. Generate a webhook URL
2. Register it with ComplyAdvantage
3. Trigger events (create customers, close cases)
4. Inspect the webhook payloads
5. Validate your signature verification logic

## Getting Help

* **Documentation**: <https://docs.mesh.complyadvantage.com>
* **Knowledge Base**: <https://support.complyadvantage.com/hc/en-gb>
* **API Reference**: [Interactive API documentation with request examples](https://docs.mesh.complyadvantage.com/reference/)
* **Support**: Contact your support team at <support@complyadvantage.com>

## Quick Reference: Standard Workflow

```
┌─────────────────────────────────────────────────────────┐
│ STEP 1: Authenticate                                    │
│    POST /v2/token                                       │
│    → Store access_token (valid 24 hours)                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 2: Create and Screen Customer                      │
│    POST /v2/workflows/sync/create-and-screen            │
│    → Store customer_identifier                          │
│    → Check risk level (LOW-RISK/MEDIUM-RISK/HIGH-RISK)   │
│    → Check screening_result:                            │
│       • NO_PROFILES: STP customer                       │
│       • HAS_PROFILES: Queue for review                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 3: Set Up Webhook (one-time setup)                │
│    POST /v2/notifications/configurations/webhook        │
│    type: CASE_STATE_UPDATED                             │
│    → Receive notifications when cases resolved          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Webhook Notification Received                           │
│    case_stage.decision_type: POSITIVE                   │
│      → Progress onboarding                              │
│    case_stage.decision_type: NEGATIVE                   │
│      → Reject customer                                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 4: Disable Monitoring                              │
│    PATCH /v2/customers/{id}/monitor                     │
│    enabled: false                                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 5: Update Customer (optional)                      │
│    PATCH /v2/customers/{id}/workflows/sync/update...    │
│    → Updates info and recalculates risk score           │
└─────────────────────────────────────────────────────────┘
```

## Implementation Checklist

### Initial Setup

* [ ] Obtain API credentials (organisation, email, password)
* [ ] Identify your API base URL
* [ ] Create screening configuration in Mesh UI
* [ ] Note the screening configuration identifier
* [ ] Set up secure storage for API credentials

### Development

* [ ] Implement authentication with automatic token refresh
* [ ] Build create and screen customer integration
* [ ] Implement risk level and screening\_result decision logic
* [ ] Set up webhook endpoint for CASE\_STATE\_UPDATED
* [ ] Implement webhook signature validation
* [ ] Add webhook processing logic (case\_state handling)
* [ ] Implement error handling and retry logic

### Testing

* [ ] Test authentication and token refresh
* [ ] Test customer creation with NO\_PROFILES result (STP)
* [ ] Test customer creation with HAS\_PROFILES result
* [ ] Test webhook delivery and signature validation
* [ ] Test webhook processing for POSITIVE decision
* [ ] Test webhook processing for NEGATIVE decision
* [ ] Test disabling monitoring
* [ ] Test updating customer information
* [ ] Test error scenarios (duplicates, invalid data, etc.)

### Production Readiness

* [ ] Set up monitoring and alerting
* [ ] Implement logging (sanitised)
* [ ] Configure rate limiting and request queuing
* [ ] Set up webhook retry mechanism

### Go Live

* [ ] Deploy to production
* [ ] Monitor initial transactions closely
* [ ] Verify webhook delivery

*Last Updated: February 2026 | API Version: v2*

***

# APPENDIX

## Appendix A: Authentication Code Examples

<details>
<summary>Click to expand authentication examples</summary>

### Request Example

```bash
curl -X POST {BASE_URL}/v2/token \
  -H "Content-Type: application/json" \
  -d '{
    "realm": "your-organization-name",
    "username": "api@yourcompany.com",
    "password": "your-secure-password"
  }'
```

### Response Example

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 86400
}
```

</details>

## Appendix B: Create and Screen Customer Examples

<details>
<summary>Click to expand customer creation examples</summary>

### Individual Customer Request

```bash
curl -X POST {BASE_URL}/v2/workflows/sync/create-and-screen \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": {
      "external_identifier": "CUST-12345",
      "person": {
        "first_name": "John",
        "last_name": "Smith"
      },
      "date_of_birth": {
        "day": 21,
        "month": 10,
        "year": 2000
      },
      "nationality": ["US"],
      "email_address": "john.smith@example.com",
      "address": {
        "address_line_1": "123 Main Street",
        "country_subdivision": "New York",
        "postal_code": "10001",
        "country": "US"
      }
    },
    "configuration": {
      "screening_configuration_identifier": "your-screening-config-id"
    },
    "monitoring": {
      "entity_screening": {
        "enabled": true
      }
    }
  }'
```

### Company Customer Request

```bash
curl -X POST {BASE_URL}/v2/workflows/sync/create-and-screen \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": {
      "external_identifier": "COMP-98765",
      "company": {
        "legal_name": "Example Corp Inc"
      },
      "registration_number": "12345678",
      "address": {
        "address_line_1": "123 Main Street",
        "country_subdivision": "New York",
        "postal_code": "10001",
        "country": "US"
      }
    },
    "configuration": {
      "screening_configuration_identifier": "your-screening-config-id"
    },
    "monitoring": {
      "entity_screening": {
        "enabled": true
      }
    }
  }'
```

### Response Example

```json
{
  "workflow_instance_identifier": "wf_abc123def456",
  "status": "COMPLETED",
  "step_details": {
    "customer-creation": {
      "identifier": "step_001",
      "status": "COMPLETED",
      "step_output": {
        "customer_identifier": "cust_xyz789abc"
      }
    },
    "initial-risk-scoring": {
      "identifier": "step_002",
      "status": "COMPLETED",
      "step_output": {
        "overall_level": "MEDIUM-RISK",
        "overall_value": 45
      }
    },
    "customer-screening": {
      "identifier": "step_003",
      "status": "COMPLETED",
      "step_output": {
        "screening_result": "HAS_PROFILES",
        "aml_types": [
          "SANCTION",
          "PEP_CLASS_2"
        ]
      }
    },
    "alerting": {
      "identifier": "step_004",
      "status": "COMPLETED",
      "step_output": {
        "alerts": [
          {
            "identifier": "alert_abc123"
          }
        ]
      }
    }
  }
}
```

</details>

## Appendix C: Webhook Configuration Examples

<details>
<summary>Click to expand webhook examples</summary>

### Webhook Registration Request

```bash
curl -X POST {BASE_URL}/v2/notifications/configurations/webhook \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://yourapi.com/webhooks/case-state-updated",
    "type": "CASE_STATE_UPDATED",
    "name": "Case state updates",
    "is_active": true
  }'
```

### Webhook Registration Response

```json
{
  "identifier": "webhook_abc123",
  "url": "https://yourapi.com/webhooks/case-state-updated",
  "type": "CASE_STATE_UPDATED",
  "is_active": true
}
```

### Webhook Payload Example

```json
{
  "api_version": "v2",
  "webhook_type": "CASE_STAGE_UPDATED",
  "case_identifier": "case_xyz123",
  "case_state": "CASE_STATE_POSITIVE_END_STATE",
  "case_type": "CUSTOMER_ONBOARDING",
  "customer": {
    "identifier": "cust_abc789",
    "external_identifier": "CUST-12345",
    "version": 1
  },
  "note": {
    "contents": "Confirmed false positive - different individual with same name"
  },
  "case_stage": {
    "identifier": "stage_def456",
    "display_name": "False Positive",
    "display_order": 4,
    "stage_type": "DECISION",
    "decision_type": "POSITIVE"
  },
  "subjects": [
    {
      "type": "CUSTOMER",
      "identifier": "cust_abc789",
      "external_identifier": "CUST-12345",
      "version": "1"
    }
  ]
}
```

### Webhook Handler Implementation Example

```javascript
// Webhook handler endpoint
app.post('/webhooks/case-stage-updated', async (req, res) => {
  const payload = req.body;
  
  // 1. Validate webhook signature (recommended)
  if (!validateWebhookSignature(req, YOUR_WEBHOOK_SECRET)) {
    return res.status(401).send('Invalid signature');
  }
  
  // 2. Extract key information
  const externalId = payload.customer.external_identifier;
  const decisionType = payload.case_stage.decision_type;

  // 3. Only act on final decisions
  if (decisionType === 'POSITIVE') {
    // Case resolved favourably - progress customer onboarding
    await progressCustomerOnboarding(externalId);
    await notifyCustomer(externalId, 'approved');
  } else if (decisionType === 'NEGATIVE') {
    // Case resolved unfavourably - reject customer
    await rejectCustomerOnboarding(externalId);
    await notifyCustomer(externalId, 'rejected');
  }
  
  // 4. Acknowledge receipt
  res.status(200).send('Webhook processed');
});
```

### Webhook Signature Validation Example

```javascript
const crypto = require('crypto');

function validateWebhookSignature(request, secret) {
  const signature = request.headers['x-complyadvantage-signature'];
  const payload = JSON.stringify(request.body);
  
  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');
  
  return signature === expectedSignature;
}
```

</details>

## Appendix D: Monitoring Management Examples

<details>
<summary>Click to expand monitoring examples</summary>

### Disable Monitoring Request

```bash
curl -X PATCH {BASE_URL}/v2/customers/cust_abc789/monitor \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_screening": {
      "enabled": false
    }
  }'
```

### Disable Monitoring Response

```json
{
  "customer_identifier": "cust_abc789",
  "external_identifier": "CUST-12345",
  "monitoring": {
    "entity_screening": {
      "enabled": false,
      "updated_at": "2025-11-04T15:30:00Z"
    }
  }
}
```

### Re-Enable Monitoring Request

```bash
curl -X PATCH {BASE_URL}/v2/customers/cust_abc789/monitor \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_screening": {
      "enabled": true
    }
  }'
```

</details>

## Appendix E: Update Customer Examples

<details>
<summary>Click to expand update customer examples</summary>

### Update Customer Request

```bash
curl -X PATCH {BASE_URL}/v2/customers/cust_abc789/workflows/sync/update-and-rescore \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": {
      "address": {
        "address_line_1": "789 New Street",
        "country_subdivision": "London",
        "postal_code": "SW1A 1AA",
        "country": "GB"
      },
      "email_address": "john.smith.new@example.com"
    }
  }'
```

### Update Customer Response

```json
{
  "workflow_instance_identifier": "wf_update_abc123",
  "status": "COMPLETED",
  "step_details": {
    "customer-update": {
      "identifier": "step_001",
      "status": "COMPLETED",
      "step_output": {
        "customer_identifier": "cust_abc789"
      }
    },
    "risk-scoring": {
      "identifier": "step_002",
      "status": "COMPLETED",
      "step_output": {
        "overall_level": "MEDIUM-RISK",
        "overall_value": 50
      }
    }
  }
}
```

</details>

## Appendix F: Error Handling and Retry Logic

<details>
<summary>Click to expand error handling examples</summary>

### Duplicate External Identifier Error Response

```json
{
  "error": "DUPLICATE_EXTERNAL_IDENTIFIER",
  "message": "A customer with external_identifier 'CUST-12345' already exists",
  "existing_customer_identifier": "cust_abc789"
}
```

### Retry Logic Implementation

```javascript
async function callApiWithRetry(apiCall, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await apiCall();
    } catch (error) {
      // Retry on rate limits and server errors
      if (error.status === 429 || error.status >= 500) {
        const delay = Math.pow(2, i) * 1000; // Exponential backoff
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        // Don't retry client errors (400, 403, 404, 409)
        throw error;
      }
    }
  }
  throw new Error('Max retries exceeded');
}
```

</details>