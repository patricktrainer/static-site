# Binomial options pricing model - Wikipedia

Created: Dec 5, 2019 10:45 AM
Tags: Finance, Statistics
URL: https://en.wikipedia.org/wiki/Binomial_options_pricing_model

![Arbre_Binomial_Options_Reelles.png](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/Arbre_Binomial_Options_Reelles.png)

In [finance](https://en.wikipedia.org/wiki/Finance), the **binomial options pricing model** (**BOPM**) provides a generalizable [numerical method](https://en.wikipedia.org/wiki/Numerical_analysis) for the valuation of [options](https://en.wikipedia.org/wiki/Option_(finance)). Essentially, the model uses a "discrete-time" ([lattice based](https://en.wikipedia.org/wiki/Lattice_model_(finance))) model of the varying price over time of the [underlying](https://en.wikipedia.org/wiki/Underlying) financial instrument, addressing cases where the [closed-form](https://en.wikipedia.org/wiki/Closed-form_expression) [Black–Scholes formula](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_formula) is wanting.

The binomial model was first proposed by [William Sharpe](https://en.wikipedia.org/wiki/William_F._Sharpe) in the 1978 edition of Investments ([ISBN](https://en.wikipedia.org/wiki/International_Standard_Book_Number) [013504605X](https://en.wikipedia.org/wiki/Special:BookSources/013504605X)),[[1]](https://en.wikipedia.org/wiki/Binomial_options_pricing_model) and formalized by [Cox](https://en.wikipedia.org/wiki/John_Carrington_Cox), [Ross](https://en.wikipedia.org/wiki/Stephen_Ross_(economist)) and [Rubinstein](https://en.wikipedia.org/wiki/Mark_Rubinstein) in 1979[[2]](https://en.wikipedia.org/wiki/Binomial_options_pricing_model) and by Rendleman and Bartter in that same year.[[3]](https://en.wikipedia.org/wiki/Binomial_options_pricing_model)

## Use of the model[[edit](https://en.wikipedia.org/w/index.php?title=Binomial_options_pricing_model&action=edit&section=1)]

The Binomial options pricing model approach has been widely used since it is able to handle a variety of conditions for which other models cannot easily be applied. This is largely because the BOPM is based on the description of an [underlying instrument](https://en.wikipedia.org/wiki/Underlying_instrument) over a period of time rather than a single point. As a consequence, it is used to value [American options](https://en.wikipedia.org/wiki/American_option) that are exercisable at any time in a given interval as well as [Bermudan options](https://en.wikipedia.org/wiki/Bermudan_option) that are exercisable at specific instances of time. Being relatively simple, the model is readily implementable in computer [software](https://en.wikipedia.org/wiki/Software) (including a [spreadsheet](https://en.wikipedia.org/wiki/Spreadsheet)).

Although computationally slower than the [Black–Scholes formula](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model), it is more accurate, particularly for longer-dated options on securities with [dividend](https://en.wikipedia.org/wiki/Dividend) payments. For these reasons, various versions of the binomial model are widely used by practitioners in the options markets.[[citation needed](https://en.wikipedia.org/wiki/Wikipedia:Citation_needed)]

For options with several sources of uncertainty (e.g., [real options](https://en.wikipedia.org/wiki/Real_option)) and for options with complicated features (e.g., [Asian options](https://en.wikipedia.org/wiki/Asian_option)), binomial methods are less practical due to several difficulties, and [Monte Carlo option models](https://en.wikipedia.org/wiki/Monte_Carlo_option_model) are commonly used instead. When simulating a small number of time steps [Monte Carlo simulation](https://en.wikipedia.org/wiki/Monte_Carlo_simulation) will be more computationally time-consuming than BOPM (cf. [Monte Carlo methods in finance](https://en.wikipedia.org/wiki/Monte_Carlo_methods_in_finance)). However, the worst-case runtime of BOPM will be [O(2n)](https://en.wikipedia.org/wiki/Exponential_time), where n is the number of time steps in the simulation. Monte Carlo simulations will generally have a [polynomial time complexity](https://en.wikipedia.org/wiki/Polynomial_time), and will be faster for large numbers of simulation steps. [Monte Carlo simulations](https://en.wikipedia.org/wiki/Monte_Carlo_simulation) are also less susceptible to sampling errors, since binomial techniques use discrete time units. This becomes more true the smaller the discrete units become.

## Method[[edit](https://en.wikipedia.org/w/index.php?title=Binomial_options_pricing_model&action=edit&section=2)]

![Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/500px-Arbre_Binomial_Options_Reelles.png](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/500px-Arbre_Binomial_Options_Reelles.png)

[Untitled](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/Untitled%20Database%20b6eb1d50a16d41d9b7acd71ea5d00381.csv)

The binomial pricing model traces the evolution of the option's key underlying variables in discrete-time. This is done by means of a binomial lattice (tree), for a number of time steps between the valuation and expiration dates. Each node in the lattice represents a possible price of the underlying at a given point in time.

Valuation is performed iteratively, starting at each of the final nodes (those that may be reached at the time of expiration), and then [working backwards](https://en.wikipedia.org/wiki/Backward_induction) through the tree towards the first node (valuation date). The value computed at each stage is the value of the option at that point in time.

Option valuation using this method is, as described, a three-step process:

1. price tree generation,
2. calculation of option value at each final node,
3. sequential calculation of the option value at each preceding node.

### Step 1: Create the binomial price tree[[edit](https://en.wikipedia.org/w/index.php?title=Binomial_options_pricing_model&action=edit&section=3)]

The tree of prices is produced by working forward from valuation date to expiration.

At each step, it is assumed that the [underlying instrument](https://en.wikipedia.org/wiki/Underlying_instrument) will move up or down by a specific factor (

[Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/c3e6bb763d22c20916ed4f0bb6bd49d7470cffd8](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/c3e6bb763d22c20916ed4f0bb6bd49d7470cffd8)

or

[Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/e85ff03cbe0c7341af6b982e47e9f90d235c66ab](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/e85ff03cbe0c7341af6b982e47e9f90d235c66ab)

) per step of the tree (where, by definition,

[Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/9418b55d44983bad84c6530b9368538a9892b9ef](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/9418b55d44983bad84c6530b9368538a9892b9ef)

and

[Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/5f15d45850d0fb6f9b86b6ff899f71e679e67374](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/5f15d45850d0fb6f9b86b6ff899f71e679e67374)

). So, if

[Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/4611d85173cd3b508e67077d4a1252c9c05abca2](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/4611d85173cd3b508e67077d4a1252c9c05abca2)

is the current price, then in the next period the price will either be

[Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/d2d300295bbe9a42f6778c122702ea649aa6deb8](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/d2d300295bbe9a42f6778c122702ea649aa6deb8)

or

[Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/8eda62013c246ced6f1cba53b03e546e3aaa1e12](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/8eda62013c246ced6f1cba53b03e546e3aaa1e12)

.

The up and down factors are calculated using the underlying [volatility](https://en.wikipedia.org/wiki/Volatility_(finance)),

[Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/59f59b7c3e6fdb1d0365a494b81fb9a696138c36](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/59f59b7c3e6fdb1d0365a494b81fb9a696138c36)

, and the time duration of a step,

[Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/65658b7b223af9e1acc877d848888ecdb4466560](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/65658b7b223af9e1acc877d848888ecdb4466560)

, measured in years (using the [day count convention](https://en.wikipedia.org/wiki/Day_count_convention) of the underlying instrument). From the condition that the [variance](https://en.wikipedia.org/wiki/Variance) of the log of the price is

[Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/b0e1c37781b3dc7893867cccbc045477dacaf2f0](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/b0e1c37781b3dc7893867cccbc045477dacaf2f0)

, we have:

[Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/85bfc1738db1939b56899f171150474d163b6364](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/85bfc1738db1939b56899f171150474d163b6364)

[Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/c3033d03393e1aaf762ffe28d1c979aedf3b236e](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/c3033d03393e1aaf762ffe28d1c979aedf3b236e)

Above is the original Cox, Ross, & Rubinstein (CRR) method; there are various other techniques for generating the lattice, such as "the equal probabilities" tree, see.[[4][5]](https://en.wikipedia.org/wiki/Binomial_options_pricing_model)

The CRR method ensures that the tree is recombinant, i.e. if the underlying asset moves up and then down (u,d), the price will be the same as if it had moved down and then up (d,u)—here the two paths merge or recombine. This property reduces the number of tree nodes, and thus accelerates the computation of the option price.

This property also allows that the value of the underlying asset at each node can be calculated directly via formula, and does not require that the tree be built first. The node-value will be:

[Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/7a987c3b255bd6672f2ac4f5a46592004575067c](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/7a987c3b255bd6672f2ac4f5a46592004575067c)

Where

[Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/d73a2c58c0ef96f8d3052f27c743edbda96ae7d6](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/d73a2c58c0ef96f8d3052f27c743edbda96ae7d6)

is the number of up ticks and

[Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/0b86cf1e41ad94827d86efab7fbc998502df0ecf](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/0b86cf1e41ad94827d86efab7fbc998502df0ecf)

is the number of down ticks.

### Step 2: Find Option value at each final node[[edit](https://en.wikipedia.org/w/index.php?title=Binomial_options_pricing_model&action=edit&section=4)]

At each final node of the tree—i.e. at expiration of the option—the option value is simply its [intrinsic](https://en.wikipedia.org/wiki/Option_time_value), or exercise, value.

[Max](https://en.wikipedia.org/wiki/Extreme_value) [ (Sn − K), 0 ], for a [call option](https://en.wikipedia.org/wiki/Call_option) Max [ (K − Sn), 0 ], for a [put option](https://en.wikipedia.org/wiki/Put_option):

Where K is the [strike price](https://en.wikipedia.org/wiki/Strike_price) and

[Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/9f049ac28d4ac8097b625f9d71c1f22b2ebd1bc4](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/9f049ac28d4ac8097b625f9d71c1f22b2ebd1bc4)

is the spot price of the underlying asset at the nth period.

### Step 3: Find Option value at earlier nodes[[edit](https://en.wikipedia.org/w/index.php?title=Binomial_options_pricing_model&action=edit&section=5)]

Once the above step is complete, the option value is then found for each node, starting at the penultimate time step, and working back to the first node of the tree (the valuation date) where the calculated result is the value of the option.

In overview: the "binomial value" is found at each node, using the [risk neutrality](https://en.wikipedia.org/wiki/Risk-neutral_measure) assumption; see [Risk neutral valuation](https://en.wikipedia.org/wiki/Rational_pricing). If exercise is permitted at the node, then the model takes the greater of binomial and exercise value at the node.

The steps are as follows:

1. Under the risk neutrality assumption, today's [fair price](https://en.wikipedia.org/wiki/Fair_value) of a [derivative](https://en.wikipedia.org/wiki/Derivative_(finance)) is equal to the [expected value](https://en.wikipedia.org/wiki/Expected_value) of its future payoff discounted by the [risk free rate](https://en.wikipedia.org/wiki/Risk-free_interest_rate). Therefore, expected value is calculated using the option values from the later two nodes ( and ) weighted by their respective probabilities—"probability" **p** of an up move in the underlying, and "probability" **(1−p)** of a down move. The expected value is then discounted at **r**, the [risk free rate](https://en.wikipedia.org/wiki/Risk-free_interest_rate) corresponding to the life of the option.        

    Option up

    Option down

    The following formula to compute the [expectation value](https://en.wikipedia.org/wiki/Expectation_value) is applied at each node:

    , or

    [Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/b75e23dc7ad848aee9b22bb4cef7cb97ae667b83](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/b75e23dc7ad848aee9b22bb4cef7cb97ae667b83)

    [Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/00282af864f696abbe09d86960fe7d10ed44f0f4](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/00282af864f696abbe09d86960fe7d10ed44f0f4)

    where  is the option's value for the  node at time t,

    [Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/6586a79a20630949cb9f3809b10bc9ba637166cb](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/6586a79a20630949cb9f3809b10bc9ba637166cb)

    [Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/b20367c858b407ee650081aad55d73bc9bfb1850](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/b20367c858b407ee650081aad55d73bc9bfb1850)

    is chosen such that the related [binomial distribution](https://en.wikipedia.org/wiki/Binomial_distribution) simulates the [geometric Brownian motion](https://en.wikipedia.org/wiki/Geometric_Brownian_motion) of the underlying stock with parameters **r** and **σ**,

    [Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/30baa98e7511726459fb5f5fd0de92a05366b7a5](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/30baa98e7511726459fb5f5fd0de92a05366b7a5)

    q is the [dividend yield](https://en.wikipedia.org/wiki/Dividend_yield) of the underlying corresponding to the life of the option. It follows that in a risk-neutral world futures price should have an expected growth rate of zero and therefore we can consider  for futures.

    [Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/9e6bb6ede6621aa135f419f86549cffc92479e38](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/9e6bb6ede6621aa135f419f86549cffc92479e38)

    Note that for p to be in the interval  the following condition on  has to be satisfied .

    [Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/c79c6838e423c1ed3c7ea532a56dc9f9dae8290b](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/c79c6838e423c1ed3c7ea532a56dc9f9dae8290b)

    [Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/8c28867ecd34e2caed12cf38feadf6a81a7ee542](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/8c28867ecd34e2caed12cf38feadf6a81a7ee542)

    [Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/4fe08220c8b2f64274902355b60d96d5963b2143](Binomial%20options%20pricing%20model%20-%20Wikipedia%20aad15f50e3744cf0aed55b7aa8320dea/4fe08220c8b2f64274902355b60d96d5963b2143)

    (Note that the alternative valuation approach, [arbitrage-free](https://en.wikipedia.org/wiki/Arbitrage-free) pricing, yields identical results; see “[delta-hedging](https://en.wikipedia.org/wiki/Rational_pricing)”.)

2. This result is the "Binomial Value". It represents the fair price of the derivative at a particular point in time (i.e. at each node), given the evolution in the price of the underlying to that point. It is the value of the option if it were to be held—as opposed to exercised at that point.
3. Depending on the style of the option, evaluate the possibility of early exercise at each node: if (1) the option can be exercised, and (2) the exercise value exceeds the Binomial Value, then (3) the value at the node is the exercise value.
    - For a [European option](https://en.wikipedia.org/wiki/European_option), there is no option of early exercise, and the binomial value applies at all nodes.
    - For an [American option](https://en.wikipedia.org/wiki/American_option), since the option may either be held or exercised prior to expiry, the value at each node is: Max (Binomial Value, Exercise Value).
    - For a [Bermudan option](https://en.wikipedia.org/wiki/Bermudan_option), the value at nodes where early exercise is allowed is: Max (Binomial Value, Exercise Value); at nodes where early exercise is not allowed, only the binomial value applies.

In calculating the value at the next time step calculated—i.e. one step closer to valuation—the model must use the value selected here, for “Option up”/“Option down” as appropriate, in the formula at the node. The aside [algorithm](https://en.wikipedia.org/wiki/Algorithm) demonstrates the approach computing the price of an American put option, although is easily generalized for calls and for European and Bermudan options:

## Relationship with Black–Scholes[[edit](https://en.wikipedia.org/w/index.php?title=Binomial_options_pricing_model&action=edit&section=6)]

Similar [assumptions](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes) underpin both the binomial model and the [Black–Scholes model](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes), and the binomial model thus provides a [discrete time](https://en.wikipedia.org/wiki/Discrete_time_and_continuous_time) [approximation](https://en.wikipedia.org/wiki/Approximation) to the continuous process underlying the Black–Scholes model. The binomial model assumes that movements in the price follow a [binomial distribution](https://en.wikipedia.org/wiki/Binomial_distribution); for many trials, this binomial distribution approaches the [lognormal distribution](https://en.wikipedia.org/wiki/Lognormal_distribution) assumed by Black–Scholes. In this case then, for [European options](https://en.wikipedia.org/wiki/European_option) without dividends, the binomial model value converges on the Black–Scholes formula value as the number of time steps increases. [[5]](https://en.wikipedia.org/wiki/Binomial_options_pricing_model) [[4]](https://en.wikipedia.org/wiki/Binomial_options_pricing_model)

In addition, when analyzed as a numerical procedure, the CRR binomial method can be viewed as a [special case](https://en.wikipedia.org/wiki/Special_case) of the [explicit finite difference method](https://en.wikipedia.org/wiki/Finite_difference_method) for the Black–Scholes [PDE](https://en.wikipedia.org/wiki/Partial_differential_equation); see [finite difference methods for option pricing](https://en.wikipedia.org/wiki/Finite_difference_methods_for_option_pricing).[[citation needed](https://en.wikipedia.org/wiki/Wikipedia:Citation_needed)]

In 2011, [Georgiadis](https://en.wikipedia.org/w/index.php?title=Evangelos_Georgiadis_(mathematician)&action=edit&redlink=1) showed that the binomial options pricing model has a lower bound on complexity that rules out a [closed-form solution](https://en.wikipedia.org/wiki/Closed-form_expression).[[6]](https://en.wikipedia.org/wiki/Binomial_options_pricing_model)

## See also[[edit](https://en.wikipedia.org/w/index.php?title=Binomial_options_pricing_model&action=edit&section=7)]

- [Trinomial tree](https://en.wikipedia.org/wiki/Trinomial_tree), a similar model with three possible paths per node.
- [Tree (data structure)](https://en.wikipedia.org/wiki/Tree_(data_structure))
- [Black–Scholes](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model): binomial lattices are able to handle a variety of conditions for which Black–Scholes cannot be applied.
- [Monte Carlo option model](https://en.wikipedia.org/wiki/Monte_Carlo_option_model), used in the valuation of options with complicated features that make them difficult to value through other methods.
- [Real options analysis](https://en.wikipedia.org/wiki/Real_options_analysis), where the BOPM is widely used.
- [Quantum finance](https://en.wikipedia.org/wiki/Quantum_finance), quantum binomial pricing model.
- [Mathematical finance](https://en.wikipedia.org/wiki/Mathematical_finance), which has a list of related articles.
- [Employee stock option#Valuation](https://en.wikipedia.org/wiki/Employee_stock_option), where the BOPM is widely used.
- [Implied binomial tree](https://en.wikipedia.org/wiki/Implied_binomial_tree)
- [Edgeworth binomial tree](https://en.wikipedia.org/wiki/Edgeworth_binomial_tree)

## [[edit](https://en.wikipedia.org/w/index.php?title=Binomial_options_pricing_model&action=edit&section=8)]

## External links[[edit](https://en.wikipedia.org/w/index.php?title=Binomial_options_pricing_model&action=edit&section=9)]

- [The Binomial Model for Pricing Options](http://www.sjsu.edu/faculty/watkins/binomial.htm), Prof. Thayer Watkins
- [Binomial Option Pricing](http://faculty.darden.virginia.edu/conroyb/derivatives/Binomial%20Option%20Pricing%20_f-0943_.pdf) ([PDF](https://en.wikipedia.org/wiki/PDF)), Prof. Robert M. Conroy
- [Binomial Option Pricing Model](http://demonstrations.wolfram.com/BinomialOptionPricingModel/) by Fiona Maclachlan, [The Wolfram Demonstrations Project](https://en.wikipedia.org/wiki/The_Wolfram_Demonstrations_Project)
- [On the Irrelevance of Expected Stock Returns in the Pricing of Options in the Binomial Model: A Pedagogical Note](http://ssrn.com/abstract=844104) by Valeri Zakamouline
- [A Simple Derivation of Risk-Neutral Probability in the Binomial Option Pricing Model](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2428763) by Greg Orosi