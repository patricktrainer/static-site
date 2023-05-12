# Consistency Models

Created: Jun 18, 2020 3:07 PM
URL: https://jepsen.io/consistency

This clickable map (adapted from [Bailis, Davidson, Fekete et al](http://www.vldb.org/pvldb/vol7/p181-bailis.pdf) and [Viotti & Vukolic](https://arxiv.org/pdf/1512.00168.pdf)) shows the relationships between common consistency models for concurrent systems. Arrows show the relationship between consistency models. For instance, strict serializable implies both serializability and linearizability, linearizability implies sequential consistency, and so on. Colors show how available each model is, for a distributed system on an asynchronous network.

Jepsen analyses the safety properties of distributed systems–most notably, identifying violations of consistency models. But what are consistency models? What phenomena do they allow? What kind of consistency does a given program really need?

In this reference guide, we provide basic definitions, intuitive explanations, and theoretical underpinnings of various consistency models for engineers and academics alike.

*Distributed* systems are a type of *concurrent* system, and much of the literature on concurrency control applies directly to distributed systems. Indeed, most of the concepts we’re going to discuss were originally formulated for single-node concurrent systems. There are, however, some important differences in *availability* and *performance*.

Systems have a logical *state* which changes over time. For instance, a simple system could be a single integer variable, with states like `0`, `3`, and `42`. A mutex has only two states: locked or unlocked. The states of a key-value store might be maps of keys to values, for instance: `{cat: 1, dog: 1}`, or `{cat: 4}`.

A *process*[1](https://jepsen.io/consistency) is a logically single-threaded program which performs computation and runs operations. Processes are never asynchronous—we model asynchronous computation via independent processes. We say “logically single-threaded” to emphasize that while a process can only do one thing at a time, its implementation may be spread across multiple threads, operating system processes, or even physical nodes—just so long as those components provide the illusion of a coherent singlethreaded program.

An operation is a transition from state to state. For instance, a single-variable system might have operations like `read` and `write`, which get and set the value of that variable, respectively. A counter might have operations like *increments*, *decrements*, and *reads*. An SQL store might have operations like *selects* and *updates*.

In theory, we could give every state transition a unique name. A lock has exactly two transition: `lock` and `unlock`. An integer register has an infinite number of reads and writes: `read-the-value-1`, `read-the-value-2`, …, and `write-1`, `write-2`, ….

To make this more tractable, we break up these transitions into *functions* like `read`, `write`, `cas`, `increment`, etc., and *values* that parameterize those functions. In a single register system, a write of 1 could be written:

```
{:f :write, :value 1}

```

Given a key-value store, we might increment the value of key “a” by 3 like so:

```
{:f :increment, :value ["a" 3]}

```

In a transactional store, the value could be a complex transaction. Here we read the current value of `a`, finding 2, and set `b` to `3`, in a single state transition:

```
{:f :txn, :value [[:read "a" 2] [:write "b" 3]]}

```

Operations, in general, take time. In a multithreaded program, an operation might be a function call. In distributed systems, an operation might mean sending a request to a server, and receiving a response.

To model this, we say that each operation has an *invocation time* and, should it complete, a strictly greater *completion time*, both given by an imaginary[2](https://jepsen.io/consistency), perfectly synchronized, globally accessible clock.[3](https://jepsen.io/consistency) We refer to these clocks as providing a *real-time* order, as opposed to clocks that only track causal ordering.[4](https://jepsen.io/consistency)

Since operations take time, two operations might overlap in time. For instance, given two operations A and B, A could begin, B could begin, A could complete, and then B could complete. We say that two operations A and B are *concurrent* if there is some time during which A and B are both executing.

Processes are single-threaded, which implies that no two operations executed by the same process are ever concurrent.

If an operation does not complete for some reason (perhaps because it timed out or a critical component crashed) that operation *has no completion time*, and must, in general, be considered concurrent with every operation after its invocation. It may or may not execute.

A process with an operation is in this state is effectively stuck, and can never invoke another operation again. If it *were* to invoke another operation, it would violate our single-threaded constraint: processes only do one thing at a time.

A *history* is a collection of operations, including their concurrent structure.

Some papers represent this as a set of operations, where each operation includes two numbers, representing their invocation and completion time; concurrent structure is inferred by comparing the time windows between processes.

Jepsen represents a history as an ordered list of invocation and completion operations, effectively splitting each operation in two. This representation is more convenient for algorithms which iterate over the history, keeping a representation of concurrent operations and possible states.

A *consistency model* is a set of histories. We use consistency models to define which histories are “good”, or “legal” in a system. When we say a history “violates serializability” or “is not serializable”, we mean that the history is not in the set of serializable histories.

We say that consistency model A implies model B if A is a subset of B. For example, linearizability implies sequential consistency because every history which is linearizable is also sequentially consistent. This allows us to relate consistency models in a hierarchy.

Speaking informally, we refer to smaller, more restrictive consistency models as “stronger”, and larger, more permissive consistency models as “weaker”.

Not all consistency models are directly comparable. Often, two models allow different behavior, but neither contains the other.

1.  [↩](https://jepsen.io/consistency) 

    Different texts may refer to processes as nodes, hosts, actors, agents, sites, or threads, often with subtle distinctions depending on context.

2.  [↩](https://jepsen.io/consistency) 

    This magical synchronized clock doesn’t actually need to exist, but some consistency models imply that *if such a clock were to exist*, some operations would happen before others.

3.  [↩](https://jepsen.io/consistency) 

    You may have heard “relativity means there is no such thing as simultaneity” used as an argument that synchronized clocks cannot exist. This is a misunderstanding: the equations of special and general relativity provide exact equations for time transformations, and it is possible to define any number of sensible, globally-synchronized time clocks. Consistency constraints that refer to these clocks will depend on the *choice* of clock, e.g. depending on one’s reference frame, a system might or might not provide linearizability. The good news is that a.) for all intents and purposes, clocks on earth are so close to each other’s velocities and accelerations that errors are much smaller than side-channel latencies, and b.) many of the algorithms for ensuring real-time bounds in asynchronous networks use causal messages to enforce a real-time order, and the resulting order is therefore invariant across *all* reference frames.

4.  [↩](https://jepsen.io/consistency) 

    “Real-time” also refers to programs that guarantee execution in a certain time duration, but we’re using the term to refer to time in the real world, as opposed to possibly unsynchronized local clocks, or some kind of logical temporal relationship.

Copyright © 2016–2020 Jepsen, LLC.

We do our best to provide accurate information, but if you see a mistake, please [let us know](mailto:errata@jepsen.io).