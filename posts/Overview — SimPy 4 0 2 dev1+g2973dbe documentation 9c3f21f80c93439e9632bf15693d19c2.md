# Overview — SimPy 4.0.2.dev1+g2973dbe documentation

Created: Jun 19, 2020 11:21 AM
URL: https://simpy.readthedocs.io/en/latest/

learn the basics of SimPy in just a couple of minutes for a complete overview 

SimPy is a process-based discrete-event simulation framework based on standard Python.

Processes in SimPy are defined by Python [generator functions](http://docs.python.org/3/glossary.html#term-generator) and may, for example, be used to model active components like customers, vehicles or agents. SimPy also provides various types of [shared resources](https://simpy.readthedocs.io/en/latest/topical_guides/resources.html) to model limited capacity congestion points (like servers, checkout counters and tunnels).

Simulations can be performed [“as fast as possible”](https://simpy.readthedocs.io/en/latest/topical_guides/environments.html), in [real time](https://simpy.readthedocs.io/en/latest/topical_guides/real-time-simulations.html) (wall clock time) or by manually [stepping](https://simpy.readthedocs.io/en/latest/topical_guides/environments.html) through the events.

Though it is theoretically possible to do continuous simulations with SimPy, it has no features that help you with that. On the other hand, SimPy is overkill for simulations with a fixed step size where your processes don’t interact with each other or with shared resources.

A short example simulating two clocks ticking in different time intervals looks like this:

```
>>> import simpy
>>>
>>> def clock(env, name, tick):
...     while True:
...         print(name, env.now)
...         yield env.timeout(tick)
...
>>> env = simpy.Environment()
>>> env.process(clock(env, 'fast', 0.5))
<Process(clock) object at 0x...>
>>> env.process(clock(env, 'slow', 1))
<Process(clock) object at 0x...>
>>> env.run(until=2)
fast 0
slow 0
fast 0.5
slow 1
fast 1.0
fast 1.5

```

The documentation contains a [tutorial](https://simpy.readthedocs.io/en/latest/simpy_intro/index.html), [several guides](https://simpy.readthedocs.io/en/latest/topical_guides/index.html) explaining key concepts, a number of [examples](https://simpy.readthedocs.io/en/latest/examples/index.html) and the [API reference](https://simpy.readthedocs.io/en/latest/api_reference/index.html).

SimPy is released under the MIT License. Simulation model developers are encouraged to share their SimPy modeling techniques with the SimPy community. Please post a message to the [SimPy mailing list](https://groups.google.com/forum/#!forum/python-simpy).

There is an introductory talk that explains SimPy’s concepts and provides some examples: [watch the video](https://www.youtube.com/watch?v=Bk91DoAEcjY) or [get the slides](http://stefan.sofa-rockers.org/downloads/simpy-ep14.pdf).

SimPy has also been reimplemented in other programming languages. See the [list of ports](https://simpy.readthedocs.io/en/latest/about/ports.html) for more details.