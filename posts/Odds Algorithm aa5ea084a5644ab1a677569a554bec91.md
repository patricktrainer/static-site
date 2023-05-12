# Odds Algorithm

Created: Dec 7, 2019 10:57 PM
Tags: Data, Statistics
URL: https://en.m.wikipedia.org/wiki/Odds_algorithm

The **odds-algorithm** is a mathematical method for computing optimal strategies for a class of problems that belong to the domain of [optimal stopping](https://en.m.wikipedia.org/wiki/Optimal_stopping) problems. Their solution follows from the odds-strategy, and the importance of the odds-strategy lies in its optimality, as explained below.

The odds-algorithm applies to a class of problems called last-success-problems. Formally, the objective in these problems is to maximize the probability of identifying in a sequence of sequentially observed independent events the last event satisfying a specific criterion (a "specific event"). This identification must be done at the time of observation. No revisiting of preceding observations is permitted. Usually, a specific event is defined by the decision maker as an event that is of true interest in the view of "stopping" to take a well-defined action. Such problems are encountered in several situations.

Two different situations exemplify the interest in maximizing the probability to stop on a last specific event.

1. Suppose a car is advertised for sale to the highest bidder (best "offer"). Let n potential buyers respond and ask to see the car. Each insists upon an immediate decision from the seller to accept the bid, or not. Define a bid as , and coded 1 if it is better than all preceding bids, and coded 0 otherwise. The bids will form a [random sequence](https://en.m.wikipedia.org/wiki/Random_sequence) of 0s and 1s. Only 1s interest the seller, who may fear that each successive 1 might be the last. It follows from the definition that the very last 1 is the highest bid. Maximizing the probability of selling on the last 1 therefore means maximizing the probability of selling .

    interesting

    best

2. A physician, using a special treatment, may use the code 1 for a successful treatment, 0 otherwise. The physician treats a sequence of n patients the same way, and wants to minimize any suffering, and to treat every responsive patient in the sequence. Stopping on the last 1 in such a random sequence of 0s and 1s would achieve this objective. Since the physician is no prophet, the objective is to maximize the probability of stopping on the last 1. (See [Compassionate use](https://en.m.wikipedia.org/wiki/Compassionate_use).)

The odds-algorithm sums up the odds in reverse order

until this sum reaches or exceeds the value 1 for the first time. If this happens at index s, it saves s and the corresponding sum

If the sum of the odds does not reach 1, it sets s = 1. At the same time it computes

The output is

The odds-strategy is the rule to observe the events one after the other and to stop on the first interesting event from index s onwards (if any), where s is the stopping threshold of output a.

The importance of the odds-strategy, and hence of the odds-algorithm, lies in the following odds-theorem.

The odds-algorithm computes the optimal strategy and the optimal win probability at the same time. Also, the number of operations of the odds-algorithm is (sub)linear in n. Hence no quicker algorithm can possibly exist for all sequences, so that the odds-algorithm is, at the same time, optimal as an algorithm.

[Bruss 2000](https://en.m.wikipedia.org/wiki/Odds_algorithm) devised the odd-algorithm, and coined its name. It is also known as Bruss-algorithm (strategy). Free implementations can be found on the web.

Applications reach from medical questions in [clinical trials](https://en.m.wikipedia.org/wiki/Clinical_trial) over sales problems, [secretary problems](https://en.m.wikipedia.org/wiki/Secretary_problems), [portfolio](https://en.m.wikipedia.org/wiki/Portfolio_(finance)) selection, (one-way) search strategies, trajectory problems and the [parking problem](https://en.m.wikipedia.org/wiki/Parking_problem) to problems in on-line maintenance and others.

There exists, in the same spirit, an Odds-Theorem for continuous-time arrival processes with [independent increments](https://en.m.wikipedia.org/wiki/Independent_increments) such as the [Poisson process](https://en.m.wikipedia.org/wiki/Poisson_process)Bruss. In some cases, the odds are not necessarily known in advance (as in Example 2 above) so that the application of the odds-algorithm is not directly possible. In this case each step can use [sequential estimates](https://en.m.wikipedia.org/w/index.php?title=Sequential_estimate&action=edit&redlink=1) of the odds. This is meaningful, if the number of unknown parameters is not large compared with the number n of observations. The question of optimality is then more complicated, however, and requires additional studies. Generalizations of the odds-algorithm allow for different rewards for failing to stop and wrong stops as well as replacing independence assumptions by weaker ones (Ferguson (2008)).

[Tamaki 2010](https://en.m.wikipedia.org/wiki/Odds_algorithm) proved a multiplicative odds theorem which deals with a problem of stopping at any of the last successes. A tight lower bound of win probability is obtained by [Matsui & Ano 2014](https://en.m.wikipedia.org/wiki/Odds_algorithm).

[Matsui & Ano 2017](https://en.m.wikipedia.org/wiki/Odds_algorithm) discussed a problem of selecting out of the last successes and obtained a tight lower bound of win probability. When the problem is equivalent to Bruss' odds problem. If the problem is equivalent to that in [Bruss & Paindaveine 2000](https://en.m.wikipedia.org/wiki/Odds_algorithm). A problem discussed by [Tamaki 2010](https://en.m.wikipedia.org/wiki/Odds_algorithm) is obtained by setting

**multiple choice problem**: A player is allowed choices, and he wins if any choice is the last success. For classical secretary problem, [Gilbert & Mosteller 1966](https://en.m.wikipedia.org/wiki/Odds_algorithm) discussed the cases . The odds problem with is discussed by [Ano, Kakinuma & Miyoshi 2010](https://en.m.wikipedia.org/wiki/Odds_algorithm). For further cases of odds problem, see [Matsui & Ano 2016](https://en.m.wikipedia.org/wiki/Odds_algorithm).

An optimal strategy belongs to the class of strategies defined by a set of threshold numbers , where . The first choice is to be used on the first candidates starting with th applicant, and once the first choice is used, second choice is to be used on the first candidate starting with th applicant, and so on.

When , [Ano, Kakinuma & Miyoshi 2010](https://en.m.wikipedia.org/wiki/Odds_algorithm) showed that the tight lower bound of win probability is equal to For general positive integer , [Matsui & Ano 2016](https://en.m.wikipedia.org/wiki/Odds_algorithm) discussed the tight lower bound of win probability. When , tight lower bounds of win probabilities are equal to , and respectively. For further cases that , see [Matsui & Ano 2016](https://en.m.wikipedia.org/wiki/Odds_algorithm).

- —: "The art of a right decision", , Issue 62, 14–20, (2005).

    Newsletter of the [European Mathematical Society](https://en.m.wikipedia.org/wiki/European_Mathematical_Society)

- T.S. Ferguson: (2008, unpublished)