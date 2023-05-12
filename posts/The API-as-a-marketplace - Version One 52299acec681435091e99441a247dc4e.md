# The API-as-a-marketplace - Version One

Created: May 28, 2020 10:17 AM
URL: https://versionone.vc/api-as-a-marketplace/

As we’ve been spending time on [B2B marketplaces](https://versionone.vc/b2b-marketplaces-revisited/) and dev tools/platforms, we’ve come to realize that there’s an interesting sub-category that combines elements of both: the API-as-a-marketplace.

**What is an API-as-a-marketplace?**

Just like a traditional marketplace, an API-as-a-marketplace has two sides: suppliers and buyers. But, the interface is different.

- In a traditional marketplace, discovery and purchase are done on the application layer. The transaction process is visible to the end user and is essentially a part of the platform’s identity and brand.
- In an API-as-a-marketplace, the API is the UX for the transaction; that is, the transaction occurs on the infrastructure layer and is abstracted away from the end user.

Here are two examples from e-commerce use cases – both are V1 portfolio companies:

- **[Shippo](https://goshippo.com/)**: developers can use this API to connect businesses to shipping carriers
- **[Patch](https://www.usepatch.com/)**: developers can use this API to connect businesses to carbon offset providers

Note that we aren’t talking about API marketplaces here. API marketplaces (like [RapidAPI](https://rapidapi.com/)) are traditional marketplaces that allow API providers to publish their APIs for developers to discover them. An API-as-a-marketplace is more of a dev tool that connects pools of suppliers and buyers and uses an API to connect the two sides.

**What makes the opportunity interesting? Choice, defensibility and simplicity**

APIs are the building blocks of today’s digital world: developers use them to quickly integrate features, data, services and functions into their own apps, removing the need to build and scale all those elements from scratch themselves. Given its DNA as a dev tool, an API-as-a-marketplace is a block in building a business just like Stripe (for payments), Twilio (for communication), Postmates (for on-demand delivery), etc.

But unlike Stripe, Twilio, and Postmates, the supply of an API-as-a-marketplace is not necessarily a commodity. That is, should they choose to, developers and businesses (or even their end users) can pick their suppliers based on whatever requirements they have.

For example, on Shippo, businesses may want to optimize the carrier (supplier) based on price, visibility on tracking, etc.. On Patch, businesses can choose a carbon offset provider based on the type of project (e.g. forestry) that most aligns with their business ethos.

In an API-as-a-marketplace, defensibility can result from two paths. First, you can aggregate the supply especially in antiquated industries where a lot of infrastructure needs to be built for the API-as-a-marketplace. For example, you need to build integrations for the supply side and make it accessible in one API call by the demand side. This direct integration is sticky: there’s instantaneous payment to the supplier whenever the API is called.

Next, network effects are a key driver of defensibility just as in traditional marketplace dynamics. When a new supplier or user joins, the value of the service or product that the marketplace is providing to users increases. In Shippo’s case, more carriers mean more options for platform users (better prices, faster delivery times, etc.). And the more businesses that use Shippo for their shipping needs drive added revenue and incentive for carriers to sign on.

And just like a regular API, the business model is simple. The API-as-a-marketplace can take a rake of each API call.

**What about data marketplaces?**

A data marketplace, which is an online store where people can buy data, is not necessarily an API-as-a-marketplace. This is because many of these platforms don’t broker data via API (but in the form of .csv for instance). They simply aggregate and resell data and don’t always give you a choice of data sources.

However, the trend is most likely such that more and more data marketplaces will move to API delivery for the efficiencies and economies of scale in connecting supply and demand. One example we’ve seen in healthcare is [Segmed](https://www.segmed.ai/), which helps clinics/hospitals monetize their medical image data by selling to healthcare AI startups that need data to train their models.

What are other API-as-a-marketplace examples? Are you building one? Where do you see other opportunities for devs? We would love to chat!