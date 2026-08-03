---
updatedAt: 2025-12-18T10:40:00.000Z
---

Fetch the complete documentation index at: https://docs.mesh.complyadvantage.com/v2.1/llms.txt. Use this file to discover all available pages before exploring further.

# Onboarding

What is customer screening and risk scoring in ComplyAdvantage Mesh?

## Screening

To ensure a customer is safe to do business with or if they continue to be safe to do business with, you can check your customers against a global database of Sanctions, Warning, Fitness and Probity and Watchlists, Politically Exposed Persons registers (PEPs) and Adverse Media.

You can tailor your screening process by creating different screening configurations; a solution that enables you to specify exactly what you want to screen a customer against. You can create as many different screening configurations as you want and name them what you want. For example, you could create a screening configuration called ‘Small businesses in the USA’ and choose to include all sources except Adverse Media.

## Risk scores

A risk score is a number that quantifies the risk level of a customer. You have the ability to configure the equation that calculates the risk score of your customers by:

**Choosing categories**\
Pick categories such as ‘basic information’ which includes attributes such as age, profession, source of wealth, salary details and identity document information.

**Selecting specific attributes within each category**\
Decide exactly what to include. For example, in the 'country' category, you might care about 'country of residence' but not 'country of nationality.'

**Deciding how much each category matters**\
We call this a weight factor. When we calculate the risk score, each group you picked is multiplied by how important you said it was. Then, we add up all those multiplied numbers to get the final risk score for each customer.

The risk score is a number that quantifies the risk level. The risk level is a way to represent the score in an easy to understand way. The risk level categories are 'Unknown', 'Low', 'Medium', 'High', and 'Prohibited'. You get to choose which risk scores correspond to the risk level categories.

You can edit your risk scoring formula and risk level thresholds at any time. Additionally, if information about your customer changes, we will automatically update your customers’ risk score and level accordingly.