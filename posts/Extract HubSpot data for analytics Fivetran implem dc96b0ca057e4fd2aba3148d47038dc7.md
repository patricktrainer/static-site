# Extract HubSpot data for analytics | Fivetran implementation

Created: Apr 18, 2020 6:11 PM
URL: https://fivetran.com/docs/applications/hubspot

[HubSpot](http://www.hubspot.com/) is an inbound marketing and sales software that helps companies attract visitors, convert leads, and close customers.

## Features

[Untitled](Extract%20HubSpot%20data%20for%20analytics%20Fivetran%20implem%20dc96b0ca057e4fd2aba3148d47038dc7/Untitled%20Database%207be40f436c274368ad68374244c8515b.csv)

## Setup guide

Follow our [step-by-step HubSpot setup guide](https://fivetran.com/docs/applications/hubspot/setup-guide) to connect HubSpot with your destination using Fivetran connectors.

## Schema information

This schemas applies to all HubSpot connections.

### HubSpot Marketing Schema

### HubSpot Sales/CRM Schema

## Deleted Rows

The HubSpot API doesn't make deleted records available so Fivetran can't mark deleted records in the destination warehouse. Deleted records will remain marked `false` where `is_deleted` or `_fivetran_deleted` columns exist except for the tables listed in the Update Frequency section below.

## Update Frequency

Because the HubSpot API does not offer a mechanism to capture deletes, Fivetran infers deletes for the tables listed below. We perform a full import of these tables once a day, compare them to the previous version, and mark deletes using the `_fivetran_deleted` system column:

- `CONTACT_LIST`
- `CONTACT_LIST_MEMBER`
- `DEAL_PIPELINE`
- `DEAL_PIPELINE_STAGE`
- `FORM`

## HubSpot Developer Preview API

We maintain the following tables using the HubSpot developer preview API, so there are sometimes structural changes in these tables. Fivetran automatically handles structural changes, which might lead to some schema breaking changes. If that happens, we need to re-sync the affected tables. You can read more in the [HubSpot Developer Preview API documentation](https://developers.hubspot.com/docs/preview/preview-overview).

- `LINE_ITEM`
- `LINE_ITEM_PROPERTY_HISTORY`
- `PRODUCT`
- `PRODUCT_PROPERTY_HISTORY`

## Negative Timestamps from HubSpot

We automatically convert negative timestamps received from HubSpot to EPOCH, for example, 1st January 1970 00:00:00 UTC.

## Questions?

We're always happy to help with any other questions you might have! [Send us an email.](mailto:sales@fivetran.com?Subject=Questions)