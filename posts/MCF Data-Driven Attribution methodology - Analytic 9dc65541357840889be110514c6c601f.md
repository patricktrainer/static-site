# MCF Data-Driven Attribution methodology - Analytics Help

Created: Feb 21, 2020 12:08 PM
URL: https://support.google.com/analytics/answer/3191594?hl=en&ref_topic=3180362

There are two main parts to the Multi-Channel Funnels (MCF) Data-Driven Attribution methodology: (1) analyzing *all* of your available path data to develop custom conversion probability models, and (2) applying to that probabilistic data set a sophisticated algorithm that assigns partial conversion credit to your marketing touchpoints.

## Develop conversion probability models from *all* available path data

MCF Data-Driven Attribution uses all available path data—including data from both converting *and* non-converting users—to understand how the presence of particular marketing touchpoints impacts your users’ probability of conversion. The resulting probability models show how likely a user is to convert at any particular point in the path, given a particular sequence of events.

## Algorithmically assign conversion credit to marketing touchpoints

MCF Data-Driven Attribution then applies to this probabilistic data set an algorithm based on a concept from cooperative game theory called the *Shapley Value*. The *Shapley Value* was developed by the economics Nobel Laureate Lloyd S. Shapley as an approach to fairly distributing the output of a team among the constituent team members.

In the case of MCF Data-Driven Attribution, the “team” being analyzed has marketing touchpoints (e.g., *Organic Search*, *Display*, and *Email*) as “team members,” and the “output” of the team is conversions. The MCF Data-Driven Attribution algorithm computes the counterfactual gains of each marketing touchpoint—that is, it compares the conversion probability of similar users who were exposed to these touchpoints, to the probability when one of the touchpoints does not occur in the path.

The actual calculation of conversion credit for each touchpoint depends on comparing all of the different permutations of touchpoints and normalizing across them. This means that the MCF Data-Driven Attribution algorithm takes into account the order in which each touchpoint occurs and assigns different credit for different path positions. For example, *Display* preceding *Paid Search* is modeled separately than *Paid Search* preceding *Display*.

### Example

In the following high-level example, the combination of *Organic Search*, *Display*, and *Email* leads to a 3% probability of conversion. When *Display* is removed, the probability drops to 2%. The observed 50% increase when *Display* is present serves as the basis for attribution.

[MCF%20Data-Driven%20Attribution%20methodology%20-%20Analytic%209dc65541357840889be110514c6c601f/tMncmkROzRFPKDix5qqyoZ2VPUrOdSpS_Z1C5GOiMAFPorZQuGjt5rPv4zrN6-nOoRaFTxNtw520](MCF%20Data-Driven%20Attribution%20methodology%20-%20Analytic%209dc65541357840889be110514c6c601f/tMncmkROzRFPKDix5qqyoZ2VPUrOdSpS_Z1C5GOiMAFPorZQuGjt5rPv4zrN6-nOoRaFTxNtw520)

illustration of display increasing likelihood of purchase

## Explore your MCF Data-Driven model and analyze its ROI implications

You can use the MCF *[Model Explorer](https://support.google.com/analytics/answer/3264219)* report to explore the specific weights your *Data-Driven* model sets based on channel and position. (For a more detailed analysis, you can download the model as a CSV file.) Use the MCF*[Model Comparison Tool](https://support.google.com/analytics/answer/1662518)* to compare models, and to identify optimization opportunities. The *[ROI Analysis](https://support.google.com/analytics/answer/3264089)* report allows you to understand the ROI implications of your *Data-Driven* model.