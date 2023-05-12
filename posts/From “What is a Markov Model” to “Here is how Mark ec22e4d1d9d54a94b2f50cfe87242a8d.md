# From “What is a Markov Model” to “Here is how Markov Models Work” - By

Created: Feb 21, 2020 12:22 PM
URL: https://hackernoon.com/from-what-is-a-markov-model-to-here-is-how-markov-models-work-1ac5f4629b71

To be honest, if you are just looking to answer the age old question of “what is a Markov Model” you should take a visit to Wikipedia (or just check the TLDR 😉), but if you are curious and looking to use some examples to aid in your understanding of *what* a Markov Model is, *why* Markov Models Matter, and *how to implement* a Markov Model stick around :) **Show > Tell**

> TLDR: “In probability theory, a Markov model is a stochastic model used to model randomly changing systems where it is assumed that future states depend only on the current state not on the events that occurred before it (that is, it assumes the Markov property). Source: https://en.wikipedia.org/wiki/Markov_model

Roadmaps are great! Check out this **table of contents** for this article’s roadmap 🚗

### Table of Contents

### A. Intro To Markov Models 👶

1. Starter Sentence
2. Weighted Distributions
3. Special Additions
4. *How* a Markov Model Works
5. Full Example Summary

### B. Further Markov Model Topics 😼

1. Larger Example
2. Distribution
3. Bigger Windows

### C. Implementation - Python 🐍

1. Dictogram Data Structure
2. Hash Table Data Structure
3. Markov Model Structure
4. Parse Markov Model

### D. Further Readings, Suggestions, Thoughts 💚

1. Applications
2. Further Reading
3. Final Thoughts

### Intro To Markov Models (☝️ 🐠 ✌️ 🐠 ⭕️ 🐠 🌀 🐠)

**1. Starter Sentence** | Definitely the best way to illustrate Markov models is through using an example. In this case we are going to use the same example that I was also presented when learning about Markov Models at [Make School](https://medium.com/@makeschool).

> “One fish two fish red fish blue fish.” -Dr. Seuss 🎩

**2. Weighted Distributions** | Before we jump into Markov models we need to make sure we have a strong understanding of the **given starter sentence, weighted distributions,** and **histograms**.

![From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1Q20t6KQDq0GhrF-NCyqxHg.png](From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1Q20t6KQDq0GhrF-NCyqxHg.png)

Starter Sentence

Cool, our starter sentence is a well known phrase and on the surface nothing may explicitly jump out. But we are going to break it down and look at what *composes* this exact sentence. Specifically, it consists of eight words (**tokens**) but only five unique words (**keys**).

![From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1GwzLn-9tMkRI4dRclS3now.png](From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1GwzLn-9tMkRI4dRclS3now.png)

Colored Starter Sentence

Here I gave each unique word (**key**) a different color and on the surface this is now just a colored sentence…but alas, there is more meaning behind coloring each **key** differently. By coloring each unique **key** differently we can see that certain **keys** appear much more often than others.

![From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1gnwXq22M3L3-bBXibqXqaw.png](From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1gnwXq22M3L3-bBXibqXqaw.png)

Distribution of keys

By looking at the above **distribution** of **keys** we could deduce that the **key** fish comes up 4x as much as any other **key.** This type of statement can led us to even further predictions such as if I randomly had to pick the next word at any point in the starter sentence my best guess would be saying “fish” because it occurs significantly more in the sentence than any other word. 💯
In our situation **weighted distributions** are the percentage that one key will appear is based on the total amount of times a key shows up divided by the total amount of tokens. For example, the weighted distribution for fish is 50% because it occurs 4 times out of the total 8 words. Then One, two, red, blue all have a 12.5% chance of occurring (1/8 each).

**Histograms** are a way to represent weighted distributions, often they are a plot that enables you to discover the underlying frequency distribution of a set of continuous data. In our case the continuous data is a *sentence* because a sentence consists of many words (continuous data).

![From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1sqA96Aytk6GG1IIMlPR_EA.png](From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1sqA96Aytk6GG1IIMlPR_EA.png)

Histogram for our starter sentence

By looking at the **histogram** of our starter sentence we can see the underlying distribution of words **visually 👀** Clearly, fish appears more than anything else in our data set 🐠🐟 🐡🐠

**3. Special Additions** | Great! At this point you should be comfortable with the concept that our *sentence* consists of many **tokens** and **keys.** Additionally, you should understand the relationship between a **histogram** and **weighted distributions**.

✅💯✅ **Extra Example** ✅💯✅

A **token** is any word in the sentence.
A **key** is a unique occurrence of a word.**Example: “***Fish Fish Fish Fish Cat”* there are two **keys** and five **tokens.** The keys are “Fish” and “Cat” (🐠 and 😺). Then any word is a token.
A **histogram** is related to **weighted distibutions** because a histogram visually shows the frequency of data in a continuous data set and in essence that is demonstrating the weighted distribution of the data.

✅💯✅ **End** ✅💯✅

Cool, so now we understand our sentence at the surface and how certain words occur more than others But before we continue we need to add some special additions to our sentence that are hidden on the surface but we can agree are there. The **Start** and **End** of the sentence…

![From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1U06RW22yqWz8tK9gMeQ3MA.png](From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1U06RW22yqWz8tK9gMeQ3MA.png)

Starter Sentence with Special Additions

Awesome! Take a moment and check out the above “additions” to the sentence that exist. This may seem unnecessary right now, but trust me, this will make exponentially more sense in the next part where we dive into Markov models 😌. In summary, every sentence proceeds by an invisible “*START*” symbol and it always concludes with an “*END*” symbol.

![From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1okyW8itkBNhiugBqZX3k0A.png](From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1okyW8itkBNhiugBqZX3k0A.png)

Distribution of Keys in Modified Example

Above, I went ahead and recreated the same distribution of keys from earlier but included our two additional keys (*START* and *END*).

**4. *How* a Markov Model Works** | Fantastic! You already may have learned a few things, but now here comes the meat of the article. Lets start from a high level definition of *What* a Markov Model is (according to [Wikipedia](https://en.wikipedia.org/wiki/Markov_model)):

> “A Markov model is a stochastic model used to model randomly changing systems where it is assumed that future states depend only on the current state not on the events that occurred before it (that is, it assumes the Markov property). Generally, this assumption enables reasoning and computation with the model that would otherwise be intractable.”-Wikipedia

Awesome! Sounds interesting…but what does that huge blob even mean? I bolded the **critical** portion of *what* a Markov Model is. In summary, a Markov Model is a model where the **next state** is solely chosen based on the **current state**.

One way to think about it is you have a window that only shows the current state (or in our case a single token) and then you have to determine what the next token is based on that small window!

![From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1xZwT88rLbYZhvAkx-XbOsw.png](From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1xZwT88rLbYZhvAkx-XbOsw.png)

Demonstrating the next word using a window

Above, I showed how each token leads to another token. Additionally, I colored the arrow leading to the next word based on the origin key. I recommend you spend some time on this diagram and the following ones because they build the foundation of *how* Markov Models work! 🤓

![From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/110vdH6xwkhX93ETi9ATsIw.png](From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/110vdH6xwkhX93ETi9ATsIw.png)

Pairs! Every Token leads to another Token!

You may have noticed that every token leads to another one (even the *END*, leads to another token — *none*). In this case it forms pairs of one token to another token!

![From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1UGdrm8lZmk1Lp3OxguaYWA.png](From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1UGdrm8lZmk1Lp3OxguaYWA.png)

Organized pairs by starting word

Above, I simply organized the pairs by their first token. At this point you may be recognizing something interesting 🤔 Each starting token is followed **only** by a possible key to follow it…

![From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1QEIDJPVBcct-Jld6cDdUKQ.png](From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1QEIDJPVBcct-Jld6cDdUKQ.png)

Possible tokens to follow each key

Ok, so hopefully you have followed along and understood that we are organizing pairs which we formed by using a **“window”** to look at what the next token is in a pair. Then above I trimmed the pairs down even further into something very interesting. Every **key** is matched with an array of possible tokens that could follow that key.

✨💡✨ **Thinking Break** ✨💡✨

Let’s take a moment to think about the above diagram. Every **key** has possible words that ***could*** follow it. If we were to give this structure from above to someone they could potentially recreate our original sentence!

### **Example:**

We give them ***Start*** to begin with, then we look at the potential options of words that ***could*** follow *START* → [One]. Being that there is only key that follows we have to pick it. Our sentence now looks like “One.” Let’s continue by looking at the potential words that ***could*** follow “One” → [fish]. Well again, that was easy only “fish” can follow One. Now our sentence is “One fish.” Now let’s see what ***could*** follow “fish” → [two, red, blue, *END*]. Here is where things get interesting any of these four options ***could*** be picked next 😳. Which means we ***could*** pick “two” and then continue and potentially get our original sentence…but there is a 25% (1/4) chance we just randomly pick “*END*”. If this was the case we would have used our original structure and randomly generated a sentence very different than our original → “One fish.” 1️⃣ 🐠

✨💡✨ **End** ✨💡✨

Congrats! 🎉🎉 You secretly just acted out a Markov Model in the above **Thinking Break** 😏. Nice! But seriously…think about it. We used the **current state** (current key) to determine our **next state**. Further our next state could only be a key that follows the current key. Sounds cool, but it gets even cooler! Let’s diagram a Markov Model for our starter sentence.

![From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1x4CnHyAqGkPa7ews_5f0sQ.png](From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1x4CnHyAqGkPa7ews_5f0sQ.png)

Markov Model for the Starter Sentence

Yikes 🙃 How does the above diagram represent what we just did? Look closely, each *oval* with a word inside it represents a **key** with the *arrows* pointing to potential **keys** that can follow it! But wait it gets even cooler:

![From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1UuD1-B7CFn3M2nUDy02sHg.png](From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1UuD1-B7CFn3M2nUDy02sHg.png)

Markov Model for the Starter Sentence with Probability

Yep! Each arrow has a probability that it will be selected to be the path that the current state will follow to the next state.

![From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1MbHRwYNA8F29hzes8EPHiQ.gif](From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1MbHRwYNA8F29hzes8EPHiQ.gif)

Full Gif of the Starter Sentence being Created Using A Markov Model.

Awesome! In summary, we now understand and have illustrated a Markov Model by using the Dr. Seuss starter sentence. As a **fun fact**, the data you use to create your model is often referred to as a **corpus 👻**

**5. Full Example Summary** | You made it! Congrats again 🏅 at this point you likely can describe what a Markov Model is and even possibly teach someone else how they work using this same basic example! You my friend are going places 🚀. But guess what! This was just the beginning of your fuller understanding of Markov Models in the following sections we will continue to grow and expand your understanding :) Remember distributions? Well we are going to use them in the next example to show how to use **weighted distributions** to *potentially* create a more accurate model; Further, we will talk about **bigger windows** 😲 (bigger is better, right? 🙄); and lastly we will implement a nifty Markov Model in Python 🐍. So buckle up and enjoy the ride 🔥🎢

### Further Markov Model Topics 😼

******Disclaimer****** 🦊 I am going to be following the same process as above for creating the Markov Model, but I am going to omit some steps. If something appears confusing refer back to the first section 🔥

**1. Larger Example** | Keeping in the spirit of Dr. Seuss quotes I went ahead and found four quotes that Theodor Seuss Geisel has **immortalized:**

> “Today you are you. That is truer than true. There is no one alive who is you-er than you.”

> “You have brains in your head. You have feet in your shoes. You can steer yourself any direction you choose. You’re on your own.”

> “The more that you read, the more things you will know. The more that you learn, the more places you’ll go.”

> “Think left and think right and think low and think high. Oh, the thinks you can think up if only you try.” -Dr. Seuss 🎩

The biggest difference between the original starter sentence and our new sentence is the fact that some **keys** follow different keys a **variable amount** of times. For example “more” follows “the” four times. So what will this additional complexity do to our Markov Model construction? 🤔 Well overall it **can improve** our logical outcome for our sentences. What I mean by that is: There are certain words in the english language (or any language for that matter 🇷🇴) that come up wayyyy more often than others. For example the word “a” comes up significantly more in day to day conversation than “wizard” 🎩. Just how the world works 🌎 With that in mind, knowing how often in comparison one key shows up vs a different key is **critical** to seeming more realistic 😊 This is known as taking the **weighted distribution** into account when deciding what the next **step** should be in the Markov Model.

One way to programmatically 💻 represent this would be for each **key** that follows a **window** you store the **keys** and the amount of **occurrences** of that key! This can be done via having a dictionary and the dictionary *key* would represent the **current window** and then have the *value* of that *dictionary key* be another dictionary that store the **unique tokens** that follow as *keys* and their *values* would be the **amount of occurrences…**Does this remind you of something we already talked about 📊? **Histograms**! Exactly! The *inner dictionary* is severing as a histogram - it is soley keeping track of **keys** and their **occurrences**! Wow, ok so many keys 🔑 were brought up and dictionaries too if you are curious about the code you should certainly check it out below👇 But otherwise, just recognize that in order to create a more advanced model we need to track what **keys** proceed other **keys** and the **amount of occurrences** of these keys.

**2. Distribution** | Awesome, quick tangent and then we will start tearing into this example 😋🍴 Cool so even this data set is ***very*** small to be a good corpus! Why? Well, we will get different distribution of words which is great and will impact the entire structure, but in the larger scope of generating **natural** **unique** generated sentences you should aim to have at **minimum 20,000** tokens. It would be better if you would have at least **100,000,** tokens. Then if you want to have a truly spectacular model you should aim for **500,000**+ tokens 🚀

But lets chat about how the distribution of words are in a **one key window** with this larger example.

![From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1e8mGc21E4cK5A-gixEoFoA.png](From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1e8mGc21E4cK5A-gixEoFoA.png)

Colored distribution of keys

Wow! Very cool 😎 Look at all that data - I went ahead and cleaned the data up and now you can see that each unique **key** in our corpus has an array of all of the **keys** and **occurrences** that follow the unique key. Very nice!

Want to know a little secret? 😏 There is very little difference between this and the previous Markov model because in both situations we make decisions on the next step **solely based on the current status** but storing the distribution of words allows us to weight the next step. Lets look at a real example from our data:

```
more : [things : 1, places : 1, that : 2]
```

Awesome! 👏 So if the Markov Model’s current status was “more” than we would randomly select one of the following words: “things”, “places”, and “that”. However, “that” appears twice as opposed to “things” and “places” which occur once. Therefore, there is a 50% chance “that” would be selected and a 25% that either “things” or “places” is selected! 😃

```
think : [high : 1, up : 1, right : 1, low : 1, left : 1]
```

☝️☝️☝️ Awesome, similar example as above, but in this case “high”, “up”, “right”, “low”, and “left” all have a 20% chance of being selected as the next state if “think” is the current state! Make sense? 💭

**3. Bigger Windows** | Currently, we have only been looking at markov models with *windows* of size one. We could increase the size of the window to get more **“accurate” sentences**. By more accurate I mean there will be less randomness in the generated sentences by the model because they will be closer and closer to the original corpus sentences. This can be good or bad 😇 😈 This is because if your purpose of the Markov Model is to generate some truly unqiue random sentences it would need to be a smaller window. A larger window is only a good idea if you have a ***significantly*** large corpus **100,000+ tokens.**

Increasing the size of the window is known as bringing the Markov Model to a **“higher order”**. The current examples we have worked with have been **first order markov models.** If we use a second order Markov Model our window size would be two! Similarly, for a third order → window size of three.

The window is the data in the current state of the Markov Model and is what is used for decision making. If there is a bigger window in a smaller data set it is unlikely that there will be large unique distributions for the possible outcomes from one window therefore it could **only recreate the same sentences.**

Let’s look at our original example with a **second order Markov Model** - window of size two! 2️⃣

![From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1PXimcZKB-1y82tQJNTZ94g.png](From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1PXimcZKB-1y82tQJNTZ94g.png)

2nd order Markov Model Data

Very interesting! Any observations? 🕵️ You may have noticed that every unique window of size two only has **one possible outcome**…therefore no matter where we start we will always get the same sentence because there is no possibility of deviating off the original path. There is a 100% chance we generate the same sentence 👎 Not great. This reveals a potential issue you can face with Markov Models…if you do not have a large enough corpus you will likely only generate sentences within the corpus which is not generating anything unique. Get a **huge data set - 500,000+ tokens** and then **play** **around** with using **different orders** of the Markov Model 👍

### Implementation — Python 🐍

**1. Dictogram Data Structure** |
The Dictogram purpose of the Dictogram is to act as a histogram but have incredibly fast 💨 and constant look up times regardless how large our data set gets. Basically it is a histogram built using a dictionary because dictionaries has the unique property of having constant lookup time O(1)!

The dictogram class can be created with an iterable data set, such as a list of words or entire books. I keep track of **token** and **key** count as I create it just so I can access those values without having to go through the entire data set 🤓

It is also good to note that I made two functions to return a random word. One just **picks a random key** and the other function takes into account the amount of occurrences for each word and then returns a **weighted random word!** **🏋️‍♀️**

**2. Markov Model Structure** |
Wow! It has been quite a journey to go from ***what*** is a Markov Model to now be talking about ***how to*** implement a Markov Model 🌄

[From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/13122645](From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/13122645)

In my implementation I have a **dictionary** that stores *windows* as the **key in the key-value pair** and then the *value* for each *key* is a **dictogram**. Basically I store a histogram of words for each window so I know what the next state can be based on a current state 😌 We increment the data in the dictogram for a key if it already exists in the current window!

**3. Nth Order Markov Model Structure |**Some of you are definitely curious about how to **implement higher order Markov Models** so I also included how I went about doing that 😏

☝️☝️☝️☝️☝️ Very similar to the first order Markov Model, but in this case we store a ***tuple*** as the **key** in the **key-value pair** in the **dictionary**. We do this because a ***tuple*** is a great way to represent a single list. And we use a tuple instead of a list because a key in a dictionary should not change and tuples are immutable sooo 🤷‍♂️

**4. Parse Markov Model** |
Yay!! 🎉👏 🎉 We now have implemented a dictogram, but how do we now do the thing where we generate content based on **current status** and **step** to a new state? 👇👇👇Here we will walk through our model 🚶

Great, so I *personally* wanted to be able to only use valid starting sentence words so I checked anything in the **END** key dictogram 🐶. Otherwise, you start the generated data with a **starting state** (which I generate from valid starts), then you just keep looking at the **possible keys** (by going into the dictogram for that key) that could **follow the current state** and **make a decision** based on *probability* and *randomness* (**weighted probability**). We keep repeating this until we do it ***length*** times! 💯

### Further Readings, Suggestions, Thoughts 💚

**1. Applications** | Some classic examples of Markov models include peoples actions based on weather, the stock market, and tweet generators! 🐣 Think about how you could use a **corpus** to create and ***generate new content*** based on a **Markov Model**. Think about what would change?
Hint: Not too much, if you have a solid understanding of what, why, and how Markov Models work and can be created the **only difference** will be *how you parse the Markov Model* and if you add any *unique restrictions.*

For example, in my dope **[silicon valley tweet generator](http://bit.ly/SVTweets)** I used a larger window, limited all my generated content to be less than 140 character, there could be a variable amount of sentences, and I used only existing sentence starting windows to “seed” the sentences. 🌱

**2. Further Reading** | Now that you have a good understanding of what a Markov Model is maybe you could explore how a Hidden Markov Model works. Or maybe if you are more inclined to build something using your new found knowledge you could read my artcile on building a HBO Silicon Valley Tweet Generator using a markov model (coming soon) !

**3. Final Thoughts** | I am always looking for feedback so please feel free to share your thoughts on how the article was structured, the content, examples, or anything else you want to share with me 😊 Markov Models are great tools and I encourage you to build something using one…maybe even your own tweet generator 😜 Cheers! 🤗

*If you liked this article, click the💚 below so other people will see it here on Medium.*

![From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1fKzgMQaOI_ox1w-PzkYvUQ.png](From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1fKzgMQaOI_ox1w-PzkYvUQ.png)

![From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1fSiuSUFIo6lGt2XKJWyqgg.png](From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1fSiuSUFIo6lGt2XKJWyqgg.png)

![From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1_1ZNPfn7_5dSLRg4Eu8Bcw.png](From%20%E2%80%9CWhat%20is%20a%20Markov%20Model%E2%80%9D%20to%20%E2%80%9CHere%20is%20how%20Mark%20ec22e4d1d9d54a94b2f50cfe87242a8d/1_1ZNPfn7_5dSLRg4Eu8Bcw.png)