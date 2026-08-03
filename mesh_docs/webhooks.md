---
updatedAt: 2026-05-13T09:01:50.000Z
---

Fetch the complete documentation index at: https://docs.mesh.complyadvantage.com/v2.1/llms.txt. Use this file to discover all available pages before exploring further.

# Webhooks

Webhooks in ComplyAdvantage Mesh

ComplyAdvantage Mesh has a comprehensive webhook infrastructure. Setting up, viewing and changing the status of webhooks can be achieved through our [webhook endpoints](https://docs.mesh.complyadvantage.com/reference/notificationcreatewebhookconfiguration#/).

## Source IP addresses

Webhooks will be delivered from the following IP addresses, depending on the region you are hosted in. If you are unsure of the region you are hosted in, please reach out to our support team who will be able to confirm.

| Server                                      | IP addresses                                 |
| :------------------------------------------ | :------------------------------------------- |
| <https://api.eu.mesh.complyadvantage.com/>  | 99.81.100.211, 99.81.116.122, 99.81.123.126  |
| <https://api.eu3.mesh.complyadvantage.com/> | 34.159.166.146, 34.159.147.62, 34.89.250.171 |
| <https://api.us.mesh.complyadvantage.com/>  | 34.67.184.6, 35.225.126.158, 34.70.66.162    |
| <https://api.us2.mesh.complyadvantage.com/> | 3.129.172.188, 3.134.73.120, 52.14.135.67    |
| <https://api.ca.mesh.complyadvantage.com/>  | 34.47.8.155, 34.47.17.48, 34.95.18.164       |
| <https://api.au.mesh.complyadvantage.com/>  | 34.151.112.133, 35.201.15.175, 35.201.23.82  |

## Delivery Guarantees

Our webhooks operate on an "at least once" delivery guarantee. This means that when an event occurs that triggers a webhook, we ensure that the webhook is sent to your specified endpoint at least one time.

In practice, this guarantee implies that for each webhook, you will receive one or more requests from our systems. While we strive to send each webhook only once, there are scenarios where you may receive the same webhook more than once. This can happen due to various factors such as network issues, server redundancy, or our retry mechanisms.

It's important to note that receiving duplicate webhooks is a normal, though infrequent occurrence in an "at least once" delivery system. We prioritize ensuring that you don't miss webhooks over preventing occasional duplicates. Therefore, we recommend that your webhook handling logic be idempotent - capable of processing the same event multiple times without adverse effects.

## Webhooks retry mechanism

If a webhook is sent from our side and the endpoint on the other end is not available to receive it, there will be three retries with an exponential back-off between them:

* 1st retry after 1 second
* 2nd retry after 5 seconds
* 3rd retry after 10 seconds

For signed webhooks, each retry attempt carries the same `webhook-id` as the original send, but a fresh `webhook-timestamp` and `webhook-signature`. Use `webhook-id` for idempotency.

## Webhook signature verification

If your account has webhook signing enabled, every webhook we send carries three additional headers (`webhook-id`, `webhook-timestamp`, `webhook-signature`) that let you verify the payload was sent by us and has not been altered in transit. We sign using HMAC-SHA256 over a canonical string that includes the message id, timestamp, and body. See below for the exact format.

### Enabling webhook signatures

Webhook signing is opt-in per account. To enable it, please reach out to our support team. We generate a 256-bit signing secret on your behalf and share it with you securely.

If you ever need to rotate the secret, contact us. We support zero-downtime rotation: while both the old and new secret are active, every webhook is signed with both, and you can verify against whichever one you currently hold.

### Headers we send

| Header              | Format                                   | Description                                                                                                         |
| :------------------ | :--------------------------------------- | :------------------------------------------------------------------------------------------------------------------ |
| `webhook-id`        | UUID                                     | Stable identifier for this webhook. Useful for deduplication.                                                       |
| `webhook-timestamp` | Unix epoch in seconds (not milliseconds) | When we sent the webhook.                                                                                           |
| `webhook-signature` | `v1,<base64-sig>`                        | The signature(s) over the message contents. May contain multiple entries separated by spaces during a key rotation. |

Example:

```
webhook-signature: v1,K5oZfzN95Z9UVu1EsfQmfVNQhnkZ2pj9o9NDN/H/pI4=
```

During a key rotation you may temporarily see two signatures:

```
webhook-signature: v1,K5oZfzN95Z9UVu1EsfQmfVNQhnkZ2pj9o9NDN/H/pI4= v1,p4yUrAEPP7n9TG8K3+ZxLyhKK6Lyw9k8oDZ4qf73wHQ=
```

A signature verifier should treat the header value as a list and accept the message if **any** entry matches.

### The signature scheme

We compute the signature as:

```
signature = base64( HMAC-SHA256( secret, "{webhook-id}.{webhook-timestamp}.{body}" ) )
```

Where:

* `secret` is the 32 raw bytes obtained by **base64-decoding** the secret value we shared with you.
* `{webhook-id}` and `{webhook-timestamp}` are the exact strings from the corresponding headers. Don't reformat them or strip whitespace.
* `{body}` is the **raw bytes** of the request body, exactly as delivered. Don't parse and re-serialize the JSON. Whitespace and key ordering matter.
* The three components are joined by literal `.` characters.

### Secret format

The secret we share with you is a raw base64 string. For example:

```
CDed2VbFJcUjH4HxmPBkHTmWozoGgZrjAnWkrcKVKVE=
```

It uses the **standard base64 alphabet** (`+`, `/`, `=`), not URL-safe base64. Decoding it with a URL-safe decoder will give you garbled bytes and signatures will mismatch. After decoding you should have 32 bytes of raw key material.

We use the secret value as-is, without `whsec_` or any other prefix.

### Timestamp tolerance

A common practice is to reject messages whose `webhook-timestamp` is outside a **±5 minute window** of the current time. This protects against replay attacks.

### How to verify

1. Capture the **raw request body** before any JSON parsing or middleware. Most web frameworks parse the body before your handler sees it, so you need to hook in earlier.
2. Read the `webhook-id`, `webhook-timestamp`, and `webhook-signature` headers.
3. Reject the request if `webhook-timestamp` is outside ±5 minutes of "now".
4. Base64-decode the signing secret to get 32 raw bytes.
5. Build the canonical string: `{webhook-id}.{webhook-timestamp}.{body}` joined by literal dots.
6. Compute `HMAC-SHA256` over the canonical string with the decoded secret as the key, and base64-encode the result.
7. Strip the `v1,` prefix from each space-separated entry in the `webhook-signature` header and compare your computed signature against each. Use a **constant-time comparison** to avoid timing attacks. Accept the message if any entry matches.

### Common verification failures

Things that commonly cause verification failures:

* **Hashing the parsed JSON instead of the raw body.** Frameworks like Express, Spring, and FastAPI parse and re-serialize the JSON before your handler sees it. The re-serialized form differs in whitespace and key order, so the signature won't match. Always feed the verifier the raw bytes from the wire.
* **Forgetting to base64-decode the secret.** The secret value we share is base64-encoded. Use it as the HMAC key only after decoding to raw bytes.
* **Signing only the body.** The canonical string is `{webhook-id}.{webhook-timestamp}.{body}`, joined by literal dots. Hashing just the body, or `timestamp.body`, will not match.
* **Including the `v1,` prefix in the signature you compare against.** Strip it and compare only the base64 portion.
* **Using URL-safe base64 to decode the secret.** Use the standard alphabet (`+`, `/`, `=`).

### Pre-built libraries

Our signing format is compatible with the [Standard Webhooks v1 specification](https://www.standardwebhooks.com/), so any [Standard Webhooks library](https://github.com/standard-webhooks/standard-webhooks/tree/main/libraries) will work out of the box. They handle the signing scheme, multi-signature header parsing, and timestamp-window enforcement for you, in Python, JavaScript / TypeScript, Java / Kotlin, Go, Ruby, C# / .NET, PHP, Rust, and Elixir.