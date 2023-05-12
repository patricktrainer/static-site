# Optimal stopping - Wikipedia

Created: Dec 4, 2019 9:25 PM
Tags: Finance
URL: https://en.wikipedia.org/wiki/Optimal_stopping#Option_trading

Not to be confused with [Optional stopping theorem](https://en.wikipedia.org/wiki/Optional_stopping_theorem).

In [mathematics](https://en.wikipedia.org/wiki/Mathematics), the theory of **optimal stopping**[[1][2]](https://en.wikipedia.org/wiki/Optimal_stopping) or **early stopping**[[3]](https://en.wikipedia.org/wiki/Optimal_stopping) is concerned with the problem of choosing a time to take a particular action, in order to [maximise](https://en.wikipedia.org/wiki/Optimization_(mathematics)) an expected reward or minimise an expected cost. Optimal stopping problems can be found in areas of [statistics](https://en.wikipedia.org/wiki/Statistics), [economics](https://en.wikipedia.org/wiki/Economics), and [mathematical finance](https://en.wikipedia.org/wiki/Mathematical_finance) (related to the pricing of [American options](https://en.wikipedia.org/wiki/American_options)). A key example of an optimal stopping problem is the [secretary problem](https://en.wikipedia.org/wiki/Secretary_problem). Optimal stopping problems can often be written in the form of a [Bellman equation](https://en.wikipedia.org/wiki/Bellman_equation), and are therefore often solved using [dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming).

## Definition[[edit](https://en.wikipedia.org/w/index.php?title=Optimal_stopping&action=edit&section=1)]

### Discrete time case[[edit](https://en.wikipedia.org/w/index.php?title=Optimal_stopping&action=edit&section=2)]

Stopping rule problems are associated with two objects:

1. A sequence of random variables , whose joint distribution is something assumed to be known

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/869cccabc3ea7b90d40e40158d740fc88e07889a](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/869cccabc3ea7b90d40e40158d740fc88e07889a)

2. A sequence of 'reward' functions  which depend on the observed values of the random variables in 1.:

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/c347dcdade06ab59406dacf0d929e03855856ee8](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/c347dcdade06ab59406dacf0d929e03855856ee8)

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/4f93e8400461ac4d620680baee52030fa89911db](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/4f93e8400461ac4d620680baee52030fa89911db)

Given those objects, the problem is as follows:

- You are observing the sequence of random variables, and at each step , you can choose to either stop observing or continue

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/add78d8608ad86e54951b8c8bd6c8d8416533d20](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/add78d8608ad86e54951b8c8bd6c8d8416533d20)

- If you stop observing at step , you will receive reward

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/67d30d30b6c2dbe4d6f150d699de040937ecc95f](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/67d30d30b6c2dbe4d6f150d699de040937ecc95f)

- You want to choose a [stopping rule](https://en.wikipedia.org/wiki/Stopping_rule) to maximize your expected reward (or equivalently, minimize your expected loss)

### Continuous time case[[edit](https://en.wikipedia.org/w/index.php?title=Optimal_stopping&action=edit&section=3)]

Consider a gain processes

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/3145251bd7dcd62f06889457914d47d54447646a](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/3145251bd7dcd62f06889457914d47d54447646a)

defined on a [filtered probability space](https://en.wikipedia.org/wiki/Filtered_probability_space)

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/5e3f1b6d200f2bc4fd12f17fcd4b9547da96ce09](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/5e3f1b6d200f2bc4fd12f17fcd4b9547da96ce09)

and assume that

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/f5f3c8921a3b352de45446a6789b104458c9f90b](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/f5f3c8921a3b352de45446a6789b104458c9f90b)

is [adapted](https://en.wikipedia.org/wiki/Adapted_process) to the filtration. The optimal stopping problem is to find the [stopping time](https://en.wikipedia.org/wiki/Stopping_time)

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/0b4ac981f3c6efc49fbcb3ecd24f7bf152dad0a7](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/0b4ac981f3c6efc49fbcb3ecd24f7bf152dad0a7)

which maximizes the expected gain

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/c4da65227df8165056ee82f640793d8e4b37908f](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/c4da65227df8165056ee82f640793d8e4b37908f)

where

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/57a433d75842b2d6a28cd5f8ca9cf7dba459084f](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/57a433d75842b2d6a28cd5f8ca9cf7dba459084f)

is called the [value function](https://en.wikipedia.org/wiki/Value_function). Here

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/ec7200acd984a1d3a3d7dc455e262fbe54f7f6e0](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/ec7200acd984a1d3a3d7dc455e262fbe54f7f6e0)

can take value

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/c26c105004f30c27aa7c2a9c601550a4183b1f21](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/c26c105004f30c27aa7c2a9c601550a4183b1f21)

.

A more specific formulation is as follows. We consider an adapted strong [Markov process](https://en.wikipedia.org/wiki/Markov_process)

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/478bcaa73ef8daeb8bd07701b59c6384b689f131](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/478bcaa73ef8daeb8bd07701b59c6384b689f131)

defined on a filtered probability space

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/becca0fa5b0e6527db1e25d78299511b5320edbb](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/becca0fa5b0e6527db1e25d78299511b5320edbb)

where

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/03c8fe9e48980d22020c362b11762a216f8bee58](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/03c8fe9e48980d22020c362b11762a216f8bee58)

denotes the [probability measure](https://en.wikipedia.org/wiki/Probability_measure) where the [stochastic process](https://en.wikipedia.org/wiki/Stochastic_process) starts at

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/87f9e315fd7e2ba406057a97300593c4802b53e4](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/87f9e315fd7e2ba406057a97300593c4802b53e4)

. Given continuous functions

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/6cda8890e3537220b4086150dad4d2083e9e309f](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/6cda8890e3537220b4086150dad4d2083e9e309f)

, and

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/2b76fce82a62ed5461908f0dc8f037de4e3686b0](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/2b76fce82a62ed5461908f0dc8f037de4e3686b0)

, the optimal stopping problem is

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/1bc9b95ddda4fb83aaeec166d832384ecfed6db8](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/1bc9b95ddda4fb83aaeec166d832384ecfed6db8)

This is sometimes called the MLS (which stand for Mayer, Lagrange, and supremum, respectively) formulation.[[4]](https://en.wikipedia.org/wiki/Optimal_stopping)

## Solution methods[[edit](https://en.wikipedia.org/w/index.php?title=Optimal_stopping&action=edit&section=4)]

There are generally two approaches to solving optimal stopping problems.[[4]](https://en.wikipedia.org/wiki/Optimal_stopping) When the underlying process (or the gain process) is described by its unconditional [finite-dimensional distributions](https://en.wikipedia.org/wiki/Finite-dimensional_distribution), the appropriate solution technique is the martingale approach, so called because it uses [martingale](https://en.wikipedia.org/wiki/Martingale_(probability_theory)) theory, the most important concept being the [Snell envelope](https://en.wikipedia.org/wiki/Snell_envelope). In the discrete time case, if the planning horizon

is finite, the problem can also be easily solved by [dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming).

When the underlying process is determined by a family of (conditional) transition functions leading to a Markov family of transition probabilities, powerful analytical tools provided by the theory of [Markov processes](https://en.wikipedia.org/wiki/Markov_process) can often be utilized and this approach is referred to as the Markov method. The solution is usually obtained by solving the associated [free-boundary problems](https://en.wikipedia.org/wiki/Free_boundary_problem) ([Stefan problems](https://en.wikipedia.org/wiki/Stefan_problem)).

## A jump diffusion result[[edit](https://en.wikipedia.org/w/index.php?title=Optimal_stopping&action=edit&section=5)]

Let

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/95734a78eb8407939c3496cbfd92763ced1e41e1](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/95734a78eb8407939c3496cbfd92763ced1e41e1)

be a [Lévy](https://en.wikipedia.org/wiki/L%C3%A9vy_process) diffusion in

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/1bcd8908c9fa46eb979ef7b67d1bb65eb3692cbb](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/1bcd8908c9fa46eb979ef7b67d1bb65eb3692cbb)

given by the [SDE](https://en.wikipedia.org/wiki/Stochastic_differential_equation)

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/264bc8d76ca788b3eff6e45fa24b76c3201aba60](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/264bc8d76ca788b3eff6e45fa24b76c3201aba60)

where

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/47136aad860d145f75f3eed3022df827cee94d7a](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/47136aad860d145f75f3eed3022df827cee94d7a)

is an

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/0a07d98bb302f3856cbabc47b2b9016692e3f7bc](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/0a07d98bb302f3856cbabc47b2b9016692e3f7bc)

-dimensional [Brownian motion](https://en.wikipedia.org/wiki/Brownian_motion),

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/b49f9e15c90b97d6d95aaf6bd1a4f520d66c2bb7](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/b49f9e15c90b97d6d95aaf6bd1a4f520d66c2bb7)

is an

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/829091f745070b9eb97a80244129025440a1cfac](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/829091f745070b9eb97a80244129025440a1cfac)

-dimensional compensated [Poisson random measure](https://en.wikipedia.org/wiki/Poisson_random_measure),

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/aae4bec0dfe664f70a1b9cda15fd319fa1e454eb](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/aae4bec0dfe664f70a1b9cda15fd319fa1e454eb)

,

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/165b2ac51764fbee3ed5db71d915b53420333832](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/165b2ac51764fbee3ed5db71d915b53420333832)

, and

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/454e9f9964b0205f0e19d54a5e902038bc1e095f](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/454e9f9964b0205f0e19d54a5e902038bc1e095f)

are given functions such that a unique solution

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/5446d2e710df1848b39d3474304fa84dbdc60a05](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/5446d2e710df1848b39d3474304fa84dbdc60a05)

exists. Let

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/cf346ba43df3bcfeb8dce6640c9416328c3aebcf](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/cf346ba43df3bcfeb8dce6640c9416328c3aebcf)

be an open set (the solvency region) and

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/4e5b9402b8a17241a5c43ee27ce04f1ffab93579](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/4e5b9402b8a17241a5c43ee27ce04f1ffab93579)

be the bankruptcy time. The optimal stopping problem is:

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/96e90fc8d59f61857be4ba95aff689714bfc5761](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/96e90fc8d59f61857be4ba95aff689714bfc5761)

It turns out that under some regularity conditions,[[5]](https://en.wikipedia.org/wiki/Optimal_stopping) the following verification theorem holds:

If a function

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/7d9dd8e4893e28a7f6eabb88b72d49efc8ddeb39](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/7d9dd8e4893e28a7f6eabb88b72d49efc8ddeb39)

satisfies

- where the continuation region is ,

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/8a238ecdc084108386647a9f4928c99d54af39a4](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/8a238ecdc084108386647a9f4928c99d54af39a4)

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/9b3f5a2a4a0459b28eb40706f67ea48f83d35b78](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/9b3f5a2a4a0459b28eb40706f67ea48f83d35b78)

- on , and

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/3a8073395c6ee55e9f384471412c9d453ced655f](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/3a8073395c6ee55e9f384471412c9d453ced655f)

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/2302a18e269dbecc43c57c0c2aced3bfae15278d](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/2302a18e269dbecc43c57c0c2aced3bfae15278d)

- on , where  is the [infinitesimal generator](https://en.wikipedia.org/wiki/Infinitesimal_generator_(stochastic_processes)) of

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/b4b891a2ffc1861ecef13412bb7c69dd7e794891](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/b4b891a2ffc1861ecef13412bb7c69dd7e794891)

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/bc33a22fb3a9e91084b653ef5e58815ff05aba06](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/bc33a22fb3a9e91084b653ef5e58815ff05aba06)

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/280ae03440942ab348c2ca9b8db6b56ffa9618f8](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/280ae03440942ab348c2ca9b8db6b56ffa9618f8)

then

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/812e58cf6049240099f528ebf2c4b403f7a9ebc7](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/812e58cf6049240099f528ebf2c4b403f7a9ebc7)

for all

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/45c9dab32dcebce045fc69264dc531a98b9bc6c9](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/45c9dab32dcebce045fc69264dc531a98b9bc6c9)

. Moreover, if

- on

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/ab904cee10099523faefb28ada29590acb97c578](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/ab904cee10099523faefb28ada29590acb97c578)

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/f34a0c600395e5d4345287e21fb26efd386990e6](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/f34a0c600395e5d4345287e21fb26efd386990e6)

Then

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/76c271acf29d6893d8a17d35018cc7d8d840ac50](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/76c271acf29d6893d8a17d35018cc7d8d840ac50)

for all

and

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/72be0ff341a0ca9b991ed0249f29a229b223903f](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/72be0ff341a0ca9b991ed0249f29a229b223903f)

is an optimal stopping time.

These conditions can also be written is a more compact form (the [integro-variational inequality](https://en.wikipedia.org/wiki/Variational_inequality)):

- on

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/e277d5e516d0bdcaa7a1ea7896c0129a6297984b](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/e277d5e516d0bdcaa7a1ea7896c0129a6297984b)

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/e4ad885c8d55acb90903513494a78df58819a698](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/e4ad885c8d55acb90903513494a78df58819a698)

## Examples[[edit](https://en.wikipedia.org/w/index.php?title=Optimal_stopping&action=edit&section=6)]

### Coin tossing[[edit](https://en.wikipedia.org/w/index.php?title=Optimal_stopping&action=edit&section=7)]

(Example where

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/be348268d92ff805c0f7f57db483e8db945df843](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/be348268d92ff805c0f7f57db483e8db945df843)

converges)

You have a fair coin and are repeatedly tossing it. Each time, before it is tossed, you can choose to stop tossing it and get paid (in dollars, say) the average number of heads observed.

You wish to maximise the amount you get paid by choosing a stopping rule. If Xi (for i ≥ 1) forms a sequence of independent, identically distributed random variables with [Bernoulli distribution](https://en.wikipedia.org/wiki/Bernoulli_distribution)

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/102796cdd3229e1e12c9ff2983ae14a3e7afd0fa](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/102796cdd3229e1e12c9ff2983ae14a3e7afd0fa)

and if

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/2b6ab4cac758ec16219542d8f24ff54d00ae7fe5](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/2b6ab4cac758ec16219542d8f24ff54d00ae7fe5)

then the sequences

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/9b10d6e0110708f8a39731fa02059ac1a233e02b](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/9b10d6e0110708f8a39731fa02059ac1a233e02b)

, and

are the objects associated with this problem.

### House selling[[edit](https://en.wikipedia.org/w/index.php?title=Optimal_stopping&action=edit&section=8)]

(Example where

does not necessarily converge)

You have a house and wish to sell it. Each day you are offered

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/72a8564cedc659cf2f95ae68bc5de2f5207a3285](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/72a8564cedc659cf2f95ae68bc5de2f5207a3285)

for your house, and pay

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/c3c9a2c7b599b37105512c5d570edc034056dd40](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/c3c9a2c7b599b37105512c5d570edc034056dd40)

to continue advertising it. If you sell your house on day

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/a601995d55609f2d9f5e233e36fbe9ea26011b3b](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/a601995d55609f2d9f5e233e36fbe9ea26011b3b)

, you will earn

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/2c5fbb0c89590b028eba7239a8803fd0cd2e698e](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/2c5fbb0c89590b028eba7239a8803fd0cd2e698e)

, where

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/f792fe4acc394f169287f6cba9787c6615272a26](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/f792fe4acc394f169287f6cba9787c6615272a26)

.

You wish to maximise the amount you earn by choosing a stopping rule.

In this example, the sequence (

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/af4a0955af42beb5f85aa05fb8c07abedc13990d](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/af4a0955af42beb5f85aa05fb8c07abedc13990d)

) is the sequence of offers for your house, and the sequence of reward functions is how much you will earn.

### Secretary problem[[edit](https://en.wikipedia.org/w/index.php?title=Optimal_stopping&action=edit&section=9)]

Main article: [Secretary problem](https://en.wikipedia.org/wiki/Secretary_problem)

(Example where

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/67f488841364dd170c2f46faae8e2c3010f4cdb1](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/67f488841364dd170c2f46faae8e2c3010f4cdb1)

is a finite sequence)

You are observing a sequence of objects which can be ranked from best to worst. You wish to choose a stopping rule which maximises your chance of picking the best object.

Here, if

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/d44badd5781f56fcefe502b90932c06c0b2cd14e](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/d44badd5781f56fcefe502b90932c06c0b2cd14e)

(n is some large number) are the ranks of the objects, and

is the chance you pick the best object if you stop intentionally rejecting objects at step i, then

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/90341931f91c1eacf5850a1f78054b83527ef5e1](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/90341931f91c1eacf5850a1f78054b83527ef5e1)

and

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/c11054157cb27ceec5584a202820ab82dd2d5791](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/c11054157cb27ceec5584a202820ab82dd2d5791)

are the sequences associated with this problem. This problem was solved in the early 1960s by several people. An elegant solution to the secretary problem and several modifications of this problem is provided by the more recent [odds algorithm](https://en.wikipedia.org/wiki/Odds_algorithm) of optimal stopping (Bruss algorithm).

### Search theory[[edit](https://en.wikipedia.org/w/index.php?title=Optimal_stopping&action=edit&section=10)]

Main article: [Search theory](https://en.wikipedia.org/wiki/Search_theory)

Economists have studied a number of optimal stopping problems similar to the 'secretary problem', and typically call this type of analysis 'search theory'. Search theory has especially focused on a worker's search for a high-wage job, or a consumer's search for a low-priced good.

### Parking problem[[edit](https://en.wikipedia.org/w/index.php?title=Optimal_stopping&action=edit&section=11)]

A special example of an application of search theory is the task of optimal selection of parking space by a driver going to the opera (theater, shopping, etc.). Approaching the destination, the driver goes down the street along which there are parking spaces - usually, only some places in the parking lot are free. The goal is clearly visible, so the distance from the target is easily assessed. The driver's task is to choose a free parking space as close to the destination as possible without turning around so that the distance from this place to the destination is the shortest.[[6]](https://en.wikipedia.org/wiki/Optimal_stopping)

### Option trading[[edit](https://en.wikipedia.org/w/index.php?title=Optimal_stopping&action=edit&section=12)]

In the trading of [options](https://en.wikipedia.org/wiki/Option_(finance)) on [financial markets](https://en.wikipedia.org/wiki/Financial_market), the holder of an [American option](https://en.wikipedia.org/wiki/Option_style) is allowed to exercise the right to buy (or sell) the underlying asset at a predetermined price at any time before or at the expiry date. Therefore, the valuation of American options is essentially an optimal stopping problem. Consider a classical [Black-Scholes](https://en.wikipedia.org/wiki/Black-Scholes) set-up and let

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/0d1ecb613aa2984f0576f70f86650b7c2a132538](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/0d1ecb613aa2984f0576f70f86650b7c2a132538)

be the [risk-free interest rate](https://en.wikipedia.org/wiki/Risk-free_interest_rate) and

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/c5321cfa797202b3e1f8620663ff43c4660ea03a](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/c5321cfa797202b3e1f8620663ff43c4660ea03a)

and

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/59f59b7c3e6fdb1d0365a494b81fb9a696138c36](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/59f59b7c3e6fdb1d0365a494b81fb9a696138c36)

be the dividend rate and volatility of the stock. The stock price

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/4611d85173cd3b508e67077d4a1252c9c05abca2](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/4611d85173cd3b508e67077d4a1252c9c05abca2)

follows geometric Brownian motion

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/c769dcec166530a578ddc45226c80165acc41d43](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/c769dcec166530a578ddc45226c80165acc41d43)

under the risk-neutral measure.

When the option is perpetual, the optimal stopping problem is

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/f46cc433dc29f009cbebcc35da0676e827477069](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/f46cc433dc29f009cbebcc35da0676e827477069)

where the payoff function is

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/cf89534865f96b8b4246520a77a5a09d05b25ad9](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/cf89534865f96b8b4246520a77a5a09d05b25ad9)

for a call option and

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/7315fc2b11cadc2070ab78858ee8be0c7b75a708](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/7315fc2b11cadc2070ab78858ee8be0c7b75a708)

for a put option. The variational inequality is

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/92b7e05cd99f79e615c9536ba8f4019e0bc00363](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/92b7e05cd99f79e615c9536ba8f4019e0bc00363)

for all

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/0c8c0fb29e87d4c3f3ba7aba8bc6e7a0c6b606a6](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/0c8c0fb29e87d4c3f3ba7aba8bc6e7a0c6b606a6)

where

[Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/f11423fbb2e967f986e36804a8ae4271734917c3](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/f11423fbb2e967f986e36804a8ae4271734917c3)

is the exercise boundary. The solution is known to be[[7]](https://en.wikipedia.org/wiki/Optimal_stopping)

- (Perpetual call)  where  and

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/62363453bd2df75ecda55d5ef3dba9d954f679a5](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/62363453bd2df75ecda55d5ef3dba9d954f679a5)

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/0b5c45a5b03cdca86ea8deb1ec6e2c10ed35d099](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/0b5c45a5b03cdca86ea8deb1ec6e2c10ed35d099)

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/fe2ccc20c0bf5cf1d671556648d75d76656fca3d](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/fe2ccc20c0bf5cf1d671556648d75d76656fca3d)

- (Perpetual put)  where  and

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/e77d9317d3a58cf30457e68bf232480b6afc4a4f](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/e77d9317d3a58cf30457e68bf232480b6afc4a4f)

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/fb8e5648b16dcd2cd97fdd295d5ea25ee2224d52](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/fb8e5648b16dcd2cd97fdd295d5ea25ee2224d52)

    [Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/10134e66db0d440076b296492c842f996f485e14](Optimal%20stopping%20-%20Wikipedia%201562c6df1bb44a33bce40d08f97f5a15/10134e66db0d440076b296492c842f996f485e14)

On the other hand, when the expiry date is finite, the problem is associated with a 2-dimensional free-boundary problem with no known closed-form solution. Various numerical methods can, however, be used. See [Black–Scholes model #American options](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model) for various valuation methods here, as well as [Fugit](https://en.wikipedia.org/wiki/Fugit) for a discrete, [tree based](https://en.wikipedia.org/wiki/Lattice_model_(finance)), calculation of the optimal time to exercise.

## See also[[edit](https://en.wikipedia.org/w/index.php?title=Optimal_stopping&action=edit&section=13)]

- [Halting problem](https://en.wikipedia.org/wiki/Halting_problem)
- [Markov decision process](https://en.wikipedia.org/wiki/Markov_decision_process)
- [Optional stopping theorem](https://en.wikipedia.org/wiki/Optional_stopping_theorem)
- [Stochastic control](https://en.wikipedia.org/wiki/Stochastic_control)

## [[edit](https://en.wikipedia.org/w/index.php?title=Optimal_stopping&action=edit&section=14)]

- Thomas S. Ferguson. [UCLA Department of Mathematics: Thomas Ferguson](https://www.math.ucla.edu/people/ladder/tom)[Optimal Stopping and Applications](https://www.math.ucla.edu/~tom/Stopping/Contents.html), retrieved on 21 June 2007
- Thomas S. Ferguson. "[Who solved the secretary problem?](https://projecteuclid.org/download/pdf_1/euclid.ss/1177012493)" , Vol. 4.,282-296, (1989)

    Statistical Science

- [F. Thomas Bruss](https://en.wikipedia.org/wiki/F._Thomas_Bruss). "Sum the odds to one and stop." , Vol. 28, 1384–1391,(2000)

    Annals of Probability

- F. Thomas Bruss. "The art of a right decision: Why decision makers want to know the odds-algorithm." , Issue 62, 14-20, (2006)

    [Newsletter of the European Mathematical Society](https://en.wikipedia.org/wiki/Newsletter_of_the_European_Mathematical_Society)

- Rogerson, R.; Shimer, R.; Wright, R. (2005). "Search-theoretic models of the labor market: a survey". . **43** (4): 959–88. [JSTOR](https://en.wikipedia.org/wiki/JSTOR) [4129380](https://www.jstor.org/stable/4129380).

    [Journal of Economic Literature](https://en.wikipedia.org/wiki/Journal_of_Economic_Literature)