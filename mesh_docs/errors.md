---
updatedAt: 2025-12-16T18:10:19.000Z
---

Fetch the complete documentation index at: https://docs.mesh.complyadvantage.com/v2.1/llms.txt. Use this file to discover all available pages before exploring further.

# Errors

How the ComplyAdvantage Mesh API handles error responses

# Errors

## How the ComplyAdvantage Mesh API handles error responses

Our APIs utilise HTTP status codes for error management. In the event of a failed API call, we will return a 4xx or 5xx status code.

## Error codes

These are the status codes returned from all endpoints. Some endpoints may have additional errors which are detailed within the respective endpoint documentation.

| Status | Description                                                                                                |
| :----- | :--------------------------------------------------------------------------------------------------------- |
| 401    | **Unauthorized** - Please ensure your authentication token is correct                                      |
| 403    | **Permissions error** - You do not have the correct permissions to access the resource                     |
| 404    | **Not found** - The requested resource could not be found                                                  |
| 409    | **Conflict** - The request conflicts with another request                                                  |
| 429    | **Too many requests** - Too many requests in a given amount of time (rate limiting).                       |
| 500    | **Internal server error** - The server has encountered an error. If this persists, please contact support. |

## Error structures

These are the typical error structures you will receive for each error code.

```json 401
{
    "title": "Unauthorized",
    "status": 401,
    "detail": "Invalid authentication for resource."
}
```
```json 403
{
    "type": "about:blank",
    "title": "Forbidden",
    "status": 403,
    "detail": "You do not have the permissions needed to access the resource.",
    "instance": "<attempted_path>",
    "properties": {},
    "identifier": "018d3157-0ec8-73ba-a684-865e5e2ff1ed",
    "timestamp": "2024-01-22T13:23:25.512206Z"
}
```
```json 404 - URL not found
{
    "title": "Not Found",
    "status": 404,
    "detail": "This resource could not be found",
    "instance": "<attempted_path>",
}
```
```json 404 - Resource not found
{
    "type": "about:blank",
    "title": "Not Found",
    "status": 404,
    "detail": "This resource could not be found",
    "instance": "<attempted_path>",
    "properties": {
        "identifier": "NOT_FOUND"
    },
    "identifier": "018d3157-0ec8-73ba-a684-865e5e2ff1ed",
    "timestamp": "2024-01-22T13:23:25.512206Z"
}
```
```json 409
{
    "type": "about:blank",
    "title": "Conflict",
    "status": 409,
    "detail": "<formatted SQL detailMessage>",
    "instance": "<attempted_path>",
    "properties": {
        "field_name" : "duplicated"
    },
    "identifier": "018d3157-0ec8-73ba-a684-865e5e2ff1ed",
    "timestamp": "2024-01-22T13:23:25.512206Z"
}
```
```json 500
{
    "type": "about:blank",
    "title": "Generic Error",
    "status": 500,
    "identifier": "018d3157-0ec8-73ba-a684-865e5e2ff1ed",
    "timestamp": "2024-01-22T13:23:25.512206Z"
}
```