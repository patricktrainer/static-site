# Design Patterns in Python

Created: Jun 21, 2020 6:25 PM
URL: https://stackabuse.com/design-patterns-in-python/

### Introduction

Design Patterns are reusable models for solving known and common problems in software architecture.

They're best described as templates for dealing with a certain usual situation. An architect might have a template for designing certain kinds of door-frames which he fits into many of his projects, and a software engineer, or software architect, should know templates for solving frequent programming challenges.

A good presentation of a design pattern should include:

- Name
- Motivating problem
- Solution
- Consequences

### Equivalent Problems

If you were thinking that that's a pretty [fuzzy](https://en.wikipedia.org/wiki/Fuzzy_logic) concept, you'd be right. For instance, we could say that the following "pattern" solves all of your problems:

1. Fetch and prepare the necessary data and other resources
2. Do the calculations needed and perform the necessary work
3. Make logs of what you're doing
4. Release all resources
5. ???
6. Profit

This is an example of thinking *too abstract*. You can't really call this a pattern because it's not really a good model for solving any problem, despite being technically applicable to any of them (including making dinner).

On the other extreme, you can have solutions that are just too concrete to be called a pattern. For instance, you could wonder whether [QuickSort](https://stackabuse.com/quicksort-in-python/) is a pattern for solving the sorting problem.

It certainly is a common programming problem, and QuickSort is a good solution for it. However, it can be applied to any sorting problem with little to no modification.

Once you have it in a library and you can call it, your only real job is to make your object comparable somehow, you don't really have to deal with the essence of it yourself to modify it to fit your particular problem.

Equivalent problems are somewhere between these concepts. These are different problems that are sufficiently similar that you can apply a same model to them, but sufficiently different that this model has to be customized considerably to be applicable in each case.

Patterns that could be applied to these sorts of problems are what we can meaningfully dub *design patterns*.

### Why use Design Patterns?

You're probably familiar with some design patterns already through practice of writing code. A lot of good programmers eventually gravitate towards them even without being explicitly taught or they just pick them up from seniors along the way.

Motivations for making, learning, and utilizing design patterns are manyfold. They're a way to give names to complex abstract concepts to enable discussion and teaching.

They make communication within teams faster, because someone can just use the pattern's name instead of whipping out a whiteboard. They enable you to learn from the experiences of people who came before you, rather than having to reinvent the wheel by going through the whole crucible of gradually improving practices yourself (and having to constantly cringe at your old code).

Bad solutions that tend to be commonly invented because they seem logical on the first glance are often called [anti-patterns](https://en.wikipedia.org/wiki/Anti-pattern). In order for something to justly be called an anti-pattern it needs to be commonly reinvented and there needs to be a pattern for the same problem which solves it better.

Despite the obvious utility in practice, design patterns are also useful for learning. They introduce you to many problems that you may not have considered and allow you to think about scenarios that you may not have had hands-on experience with in-depth.

They're a must-learn for all, and they're an exceptionally good learning resource for all aspiring architects and developers who may be at the beginning of their careers and lacking the first-hand experience of grappling with various problems the industry provides.

### Design Patterns in Python

Traditionally, design patterns have been classified into three main categories: [Creational](https://stackabuse.com/design-patterns-in-python/), [Structural](https://stackabuse.com/design-patterns-in-python/), and [Behavioral](https://stackabuse.com/design-patterns-in-python/). There are other categories, like [architectural](https://en.wikipedia.org/wiki/Architectural_pattern) or [concurrency](https://en.wikipedia.org/wiki/Concurrency_pattern) patterns, but they're beyond the scope of this article.

There are also Python-specific design patterns that are created specifically around the problems that the structure of the language itself provides or that deal with problems in special ways that are only allowed because of the structure of the language.

**Creational Design Patterns** deal with creation of classes or objects. They serve to abstract away the specifics of classes so that we'd be less dependent on their exact implementation, or so that we wouldn't have to deal with complex construction whenever we need them, or so we'd ensure some special instantiation properties. They're very useful for lowering levels of dependency and controlling how the user interacts with our classes.

**Structural Design Patterns** deal with assembling objects and classes into larger structures, while keeping those structures flexible and efficient. They tend to be really useful for improving readability and maintainability of the code, ensure functionalities are properly separated, encapsulated, and that there are effective minimal interfaces between interdependent things.

**Behavioral Design Patterns** deal with algorithms in general, and assignment of responsibility between interacting objects. For example, they're good practices in cases where you may be tempted to implement a naive solution, like [busy waiting](https://en.wikipedia.org/wiki/Busy_waiting), or load your classes with unnecessary code for one specific purpose that isn't the core of their functionality.

### Creational Design Patterns

### Structural Design Patterns

### Behavioral Design Patterns

***Coming soon!***

- Chain of Responsibility
- Command
- Iterator
- Mediator
- Memento
- Observer
- State
- Strategy
- Visitor

### Python-Specific Design Patterns

***Coming soon!***

- Global Object Pattern
- Prebound Method Pattern
- Sentinel Object Pattern

### See Also