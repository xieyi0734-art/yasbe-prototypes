---
updatedAt: 2025-12-17T10:33:29.000Z
---

Fetch the complete documentation index at: https://docs.mesh.complyadvantage.com/v2.1/llms.txt. Use this file to discover all available pages before exploring further.

# Rate Limiting

How the ComplyAdvantage Mesh API handles rate limiting

## Rate limit

The ComplyAdvantage Mesh API has rate limiting to manage sudden surges in traffic to help maximise its stability. Please contact your account manager to confirm the rate limits you have in place for your account.

## Rate limit status code

Exceeding the limit will trigger a HTTP 429 response as below

```json 429
{
  "message": "API rate limit exceeded"
}
```

## Rate limit headers

The API response headers will include up-to-date information on the rate limit usage:

| Header              | Description                                              |
| :------------------ | :------------------------------------------------------- |
| Ratelimit-Limit     | The total allowed number of requests in the time window  |
| Ratelimit-Remaining | The number of requests remaining in the time window      |
| Ratelimit-Reset     | The time remaining (in seconds) until the quota is reset |