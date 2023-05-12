# Javascript tracker setup · snowplow/snowplow Wiki

Created: Apr 25, 2020 9:36 AM
URL: https://github.com/snowplow/snowplow/wiki/Javascript-tracker-setup

[1476001](Javascript%20tracker%20setup%20%C2%B7%20snowplow%20snowplow%20Wiki%202546ed2d246f498686d1cf3f4d2582f6/1476001)

[HOME](https://github.com/snowplow/snowplow/wiki/Home) » [SNOWPLOW SETUP GUIDE](https://github.com/snowplow/snowplow/wiki/Snowplow-setup-guide) » [Step 2: setup a Tracker](https://github.com/snowplow/snowplow/wiki/Setting-up-a-Tracker) » JavaScript Tracker

**Note:** Before beginning this tutorial, you will first need to host the Snowplow JavaScript tracker file `sp.js`. You can find instructions on how to host `sp.js` yourself [here](https://github.com/snowplow/snowplow/wiki/self-hosting-snowplow-js).

Before you integrate Snowplow's JavaScript Tracker, you need to decide whether you'll integrate it with a tag management system, or implement the Snowplow tags directly onto your site.

We strongly advise new Snowplow users who are not using a Tag Management solution to implement one before implementing Snowplow, and integrate Snowplow using it. We have documented [how to setup Google Tag Manager](https://github.com/snowplow/snowplow/wiki/Integrating-Javascript-tags-with-Google-Tag-Manager) and [how to setup QuBit's OpenTag](https://github.com/snowplow/snowplow/wiki/Integrating-Javascript-tags-with-QuBit-OpenTag), as well as how to integrate Snowplow using both these solutions, as part of this setup guide.

Select a setup option below based on your choice of Tag Management solution:

Once you have integrated tags on our site (either directly or via a tag manager) you should [test that the tags are firing correctly](https://github.com/snowplow/snowplow/wiki/Testing-the-Javascript-tracker-is-firing).

Once your tags are integrated and tested, there is an additional steps you may want to take:

1. [Setting up campaign tracking](https://github.com/snowplow/snowplow/wiki/tracking-your-marketing-campaigns) (optional but recommended). Snowplow identifiers the campaigns that drove users to your website using parameters appended to the landing page the ads push users into. (Exactly the same way that Google Analytics identifies traffic from campaigns). Instructions on how to track campaigns can be found [here](https://github.com/snowplow/snowplow/wiki/tracking-your-marketing-campaigns).

Finished setting up your tracker? Then proceed to setting up [EmrEtlRunner](https://github.com/snowplow/snowplow/wiki/Setting-up-EmrEtlRunner).

Back to [Tracker Setup](https://github.com/snowplow/snowplow/wiki/Setting-up-a-tracker).

Back to the [Setup Guide](https://github.com/snowplow/snowplow/wiki/Setting-up-Snowplow).