# How we scrape 300k prices per day from Google Flights

Created: Jun 13, 2020 2:23 PM
URL: https://medium.com/brisk-voyage/how-we-scrape-300k-flight-prices-per-day-from-google-flights-79f5ddbdc4c0

[0*ohKb6_EQ-Ck-aCuG](How%20we%20scrape%20300k%20prices%20per%20day%20from%20Google%20Flig%20bba4ece16f374661b4e5ada346103a51/0ohKb6_EQ-Ck-aCuG)

[Brisk Voyage](https://briskvoyage.com/) finds cheap, last-minute weekend trips for our members. The basic idea is that we continuously check a bunch of flight and hotel prices, and when we find a trip that’s a low-priced outlier, we send an email with booking instructions.

To find flight and hotel prices, we scrape Google Flights and Google Hotels. Hotels are relatively simple: to find the cheapest hotel at 100 destinations over 5 different dates each, we have to scrape 500 Google Hotels pages total.

Scraping flight prices is a larger challenge. To find the cheapest round-trip flight for 100 destinations over 5 different dates each, that’s 500 pages. Flights, however, don’t just have a destination airport — they also have an origin airport. Those 500 flights have to be checked from *each origin airport*. We have to check those flights to Aspen from every airport around NYC, every airport around Los Angeles, and every airport in between. We don’t have this extra origin airport “dimension” when scraping hotels. This means there are several orders of magnitude more flight prices than hotel prices relevant to our problem.

The goal is to find the cheapest flight between each origin/destination pair for a given set of dates. To do this, we fetch around 300,000 flight prices from 25,000 Google Flights pages every day. This isn’t an astronomical number, but it’s large enough that we (at least, as a bootstrapped company) have to care about cost efficiency. Over the past year or so, we’ve iterated on our scraping methodology to arrive at a fairly robust and flexible solution. Below, I’ll describe each tool we use in our scraping stack, roughly ordered by the flow of data.

## AWS Simple Queue Service (SQS)

We use [SQS](https://aws.amazon.com/sqs/) to serve a queue of URLs to crawl. Google Flights URLs look like this: [https://www.google.com/flights?hl=en#flt=BOS.JFK,LGA,EWR.2020-11-13*JFK,LGA,EWR.BOS.2020-11-16;c:USD;e:1;sd:1;t:f](https://www.google.com/flights?hl=en#flt=BOS.JFK,LGA,EWR.2020-11-13*JFK,LGA,EWR.BOS.2020-11-16;c:USD;e:1;sd:1;t:f).

The three-letter codes in the URL above are [IATA airport codes](https://en.wikipedia.org/wiki/IATA_airport_code). If you click that link, notice how there are multiple destination airports. This is one key to efficient Google Flights scraping! Since Google Flights allows for multiple trips to be searched at once, we can fetch the cheapest prices for multiple round-trips on one page. Google sometimes won’t show flights for all trips queried. To make sure we have all the data we need, we detect when an origin/destination isn’t displayed in the result, then re-queue the trip to be searched on its own. This ensures we collect the price of the cheapest flight available for each trip.

A single SQS queue stores all Google Flights URLs that need to be crawled. When the crawler runs, it will pick off a message from the queue. Order is not important, so a [standard queue](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues.html) (not a FIFO) is used. Here’s what the queue looks like when it’s full of messages:

## AWS Lambda (using Chalice)

[Lambda](https://aws.amazon.com/lambda/) is where the crawler actually runs. We use [Chalice](https://github.com/aws/chalice), which is an excellent Lambda microframework for Python, to deploy functions to Lambda. Although [Serverless](https://www.serverless.com/) is the most popular Lambda framework, it is written in NodeJS. This is a turn-off for us given that we’re most familiar with Python, and want to keep our stack uniform. We’ve been very happy with Chalice — it’s as simple as Flask to use, and it allows the entire Brisk Voyage backend to be Python on Lambda.

**The crawler consists of two Lambda functions:**

- The primary Lambda function ingests messages from the SQS queue, crawls Google Flights, and stores the output. When this function runs, it launches a Chrome browser on the Lambda instance and crawls the page. We define this as a pure Lambda function with Chalice, as this function will be separately triggered:
- The second Lambda function triggers multiple instances of the first function. This runs as many crawlers as we need in parallel. This function is defined to run at two minutes past the hour during UTC hours 15–22 every day. It starts 50 instances of the primary `crawl` function, for 50 parallel crawlers:

```
@app.schedule(“cron(2 15,16,17,18,19,20,21,22 ? * * *)”)
def start_crawlers(event):
    app.log.info(“Starting crawlers.”)    n_crawlers = 50
    client = boto3.client(“lambda”)    for n in range(n_crawlers):
        response = client.invoke(
            FunctionName=”collector-dev-crawl”,
            InvocationType=”Event”,
            Payload=’{“crawler_id”: ‘ + str(n) + “}”,
        )
```

An alternative would be to use the SQS queue as an event source for the `crawl` function, so that when the queue populates, the crawlers automatically scale up. We originally used this approach. There is one big drawback, however: the maximum number of messages that can be ingested by one invocation (batch size) is 10, meaning that the function has to be freshly invoked for every group of 10 messages. This not only causes compute inefficiency, but increases bandwidth drastically as the browser cache is destroyed every time the function restarts. There are ways around this, but in our experience, they have lead lots of extra complexity.

**A note on Lambda costs**Lambda costs $0.00001667/GB/second, while many EC2 instances cost [one-sixth of that](https://aws.amazon.com/ec2/pricing/on-demand/). We currently pay around $50/month for Lambda, so this would mean we could substantially reduce these costs. Lambda, however, has two big benefits: first, it scales up and down instantly with zero effort on our part, meaning we are not ever paying for an idling server. Second, it’s what the rest of our stack is built on. Less technology means less cognitive overhead. If the number of pages we crawl ramps up, it will make sense to reconsidering EC2 or a similar compute service. At this point, I think an extra $40 per month ($50 on Lambda vs ~$10 on EC2) is worth the simplicity for us.

## Pyppeteer

[Pyppeteer](https://github.com/pyppeteer/pyppeteer) is a Python library for interacting with [Puppeteer](https://github.com/puppeteer/puppeteer), a headless Chrome API. Since Google Flights requires Javascript to load prices, it is necessary to actually render the full page. Each of the 50 `crawl` functions launches its own copy of a headless Chrome browser, which is controlled with Pyppeteer.

Running headless Chrome on Lambda was a challenge. We had to pre-package the necessary libraries into Chalice that were not pre-installed on Amazon Linux, the OS that Lambda runs on top of. These libraries are added to the `vendor` directory inside our Chalice project which tells Chalice to install them on each Lambda `crawl` instance:

As the 50 `crawl` functions start up over ~5 seconds, Chrome instances are launched within each function. This is a powerful system; it can scale into thousands of concurrent Chrome instances by changing one line of code.

The `crawl` function reads a URL from the SQS queue, then Pyppeteer tells Chrome to navigate to that page behind a rotating residential proxy. The residential proxy is necessary to prevent Google from blocking the IP Lambda makes requests from. Once the page loads and renders, the rendered HTML can be extracted, and the flight prices, airlines, and times can be read from the page. There are 10–15 flight results per page that we want to extract (we mostly care about the cheapest, but the others can be useful too). This is currently done manually by traversing the page structure, but this is brittle. The crawler can break if Google changes one element on the page. In the future, I’d like to use something that’s less reliant on the page structure.

Once the prices are extracted, we delete the SQS message, and re-queue any origin/destinations that weren’t displayed within the flight results. We then move onto the next page — a new URL is pulled from the queue, and the process repeats. After the first page crawled in each `crawl` instance, pages require much less bandwidth to load (~100kb instead of 3 MB) due to Chrome’s caching. This means that we want to keep the instance alive as long as possible, and crawl as many trips as we can in order to preserve the cache. Because it’s advantageous to persist functions to retain the cache, `crawl`‘s timeout is 15 minutes, which is the maximum that AWS currently allows.

## DynamoDB

After it’s extracted from the page, we have to store the flight data. We chose [DynamoDB](https://aws.amazon.com/dynamodb/) for this because it has on-demand scaling. This was important for us, as we were uncertain about what kinds of loads we would need. It’s also cheap, and 25GB comes free under [AWS’s Free Tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc).

DynamoDB has taken some work to get right. Normally, tables can only have one primary index with one sort key. Adding secondary indices is possible, but is either limited or requires additional provisioning, which increases costs. Due to this limitation on indices, DynamoDB works best when the usage is fully thought-out beforehand. It took us a couple tries to get the table design right. In retrospect, DynamoDB is a little inflexible for the kind of product we’re building. Now that [Aurora Serverless offers PostgreSQL](https://aws.amazon.com/rds/aurora/serverless/), it may be wise for us to switch to that at some point.

Regardless, we store all of our flight data in a single table. The index has a primary key of the destination airport’s IATA code, and a secondary range key which is a [ULID](https://github.com/ulid/spec).

ULIDs are great for DyanmoDB because they are unique, have an embedded timestamp, and are lexicographically sortable by that timestamp. This allows the range key to both serve as a unique identifier and support queries such as “give me the cheapest trips to BED that we’ve crawled in the past 30 minutes”:

```
response = crawled_flights_table.query(
    KeyConditionExpression=Key("destination").eq(iata_code) & Key("id").gt(earliest_id),
    FilterExpression=Attr("cheapest_entry").eq(1),
)
```

## Monitoring and testing

We use [Dashbird](https://app.dashbird.io/) for monitoring the crawler and everything else that’s run under Lambda. Good monitoring is a requirement for scraping applications because page structure changes are a constant danger. At any time (even multiple times per day, as we’ve seen with Google Flights recently) the page structure can change, which breaks the crawler. We need to be alerted when this occurs. We have two separate mechanisms to track this:

1. A Dashbird alert that emails us when there is a crawl failure.
2. A [GitHub Action](https://github.com/features/actions) that runs every 3 hours that runs a test crawl and verifies the results make sense. Since that crawler isn’t always running, this alerts us when Google Flights changes their page structure outside of operating hours. This way, the crawler can be fixed prior to starting for the day.

The combination of SQS, Lambda, Chalice, Pyppeteer, DynamoDB, Dashbird, and GitHub Actions works well for us. It is a low-overhead solution that is entirely Python, requires no instance provisioning, and keeps costs relatively low.

While we’re satisfied with this at our current scale of roughly 300k prices and 25k pages per day, there is some room for improvement as our data needs grow:

- First, it may be wise to move the crawler to EC2 servers that are automatically provisioned when needed. As compute crawl requirements increase, the delta between Lambda and EC2 costs will increase to the point where it will make sense to run on EC2. EC2 will cost roughly 1/5th of Lambda in terms of compute, but will require more overhead and won’t reduce bandwidth costs.
- Second, we would move from DynamoDB to Serverless Aurora, which allows for more flexible data usage. This will be useful as our library of prices and the appetite for alternative data uses grow.

If you found this interesting, you might like [Brisk Voyage](https://briskvoyage.com/) — our free newsletter sends you a cheap weekend trip every few days from airports near you. If you like the service, we’ve also got a Premium version which will send you more trips and has a few more features.

There are, of course, ways this system can be improved. If you’ve got any ideas, please let us know!