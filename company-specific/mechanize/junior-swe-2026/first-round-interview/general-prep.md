# Mechanize First-Round Interview Study Guide

## 0. What You Need to Be Able to Do

The goal is **not** to become a probability expert in two days.

You want to be able to:

1. Turn a vague problem into a mathematical model.
2. State assumptions clearly.
3. Recognize common probability structures.
4. Compute simple quantities without getting lost.
5. Estimate unfamiliar quantities using first principles.
6. Sanity-check your result.
7. Explain your reasoning continuously.
8. Recover gracefully if your first approach is wrong.

For most questions, **reasoning quality matters more than getting an exact numerical answer immediately**.

---

# Part I — Core Probability

## 1. Probability Basics

A probability is a number between 0 and 1 representing how likely an event is.

\[
0 \leq P(A) \leq 1
\]

Certain event:

\[
P(A)=1
\]

Impossible event:

\[
P(A)=0
\]

### Complement Rule

If \(A^c\) means "A does not happen":

\[
P(A^c)=1-P(A)
\]

This is one of the most useful techniques in interview problems.

### Example

What is the probability of getting **at least one 6** in four dice rolls?

Directly counting 1, 2, 3, or 4 sixes is annoying.

Instead calculate the complement:

\[
P(\text{no six})=\left(\frac{5}{6}\right)^4
\]

Therefore:

\[
P(\text{at least one six})
=
1-\left(\frac{5}{6}\right)^4
\]

### Recognition rule

Whenever you see:

- "at least one"
- "one or more"
- "ever happens"

ask:

> Would the complement be easier?

---

# 2. AND vs OR

## AND

For independent events:

\[
P(A\cap B)=P(A)P(B)
\]

Example: two consecutive heads:

\[
\frac12\times\frac12=\frac14
\]

## OR

If events are mutually exclusive:

\[
P(A\cup B)=P(A)+P(B)
\]

In general:

\[
P(A\cup B)
=
P(A)+P(B)-P(A\cap B)
\]

You subtract the intersection because otherwise it gets counted twice.

---

# 3. Independence

Two events \(A\) and \(B\) are independent if learning that one happened gives you no information about the other.

Mathematically:

\[
P(A\cap B)=P(A)P(B)
\]

Equivalent:

\[
P(A|B)=P(A)
\]

### Example

Two separate fair coin flips are independent.

Knowing the first flip was heads tells you nothing about the second.

### Important trap

**Mutually exclusive does NOT mean independent.**

Suppose one die is rolled.

- \(A\): result is 2
- \(B\): result is 5

They cannot both happen.

Therefore knowing \(A\) happened tells you \(B\) definitely didn't happen.

They are maximally dependent.

---

# 4. Conditional Probability

Conditional probability asks:

> Given that I know \(B\) occurred, how likely is \(A\)?

Formula:

\[
P(A|B)=\frac{P(A\cap B)}{P(B)}
\]

The critical idea is that **conditioning changes your sample space**.

### Classic example

Two dice are rolled.

You are told **at least one is a 6**.

What is the probability both are 6?

Possible ordered outcomes involving at least one six:

\[
(6,1),(6,2),...,(6,6),...,(1,6),(2,6),...,(5,6)
\]

There are:

\[
6+5=11
\]

possible outcomes.

Only one is:

\[
(6,6)
\]

So:

\[
P(\text{both 6}|\text{at least one 6})
=
\frac1{11}
\]

### Trap

This is different from:

> The first die is a 6. What's the probability the second is a 6?

That answer is simply:

\[
\frac16
\]

The information you're given matters.

---

# 5. Bayes' Theorem

Bayes' theorem reverses conditioning.

You know:

\[
P(B|A)
\]

but want:

\[
P(A|B)
\]

Formula:

\[
P(A|B)
=
\frac{P(B|A)P(A)}
{P(B)}
\]

Usually expand the denominator:

\[
P(B)
=
P(B|A)P(A)
+
P(B|A^c)P(A^c)
\]

## Intuitive version

Think:

> posterior = likelihood × prior / evidence

Where:

- **Prior:** what you believed before seeing evidence.
- **Likelihood:** how likely that evidence is under a hypothesis.
- **Posterior:** what you should believe after observing evidence.

---

# 6. Bayes Example: Double-Headed Coin

There are three coins:

- Fair coin
- Fair coin
- Double-headed coin

You choose one uniformly and flip it.

You see heads.

What's the probability you chose the double-headed coin?

Before seeing anything:

\[
P(D)=\frac13
\]

Probability of heads if double-headed:

\[
P(H|D)=1
\]

Probability of heads overall:

\[
P(H)
=
\frac13(1)
+
\frac23\left(\frac12\right)
\]

\[
=\frac13+\frac13
=\frac23
\]

Therefore:

\[
P(D|H)
=
\frac{1\cdot(1/3)}{2/3}
=
\frac12
\]

### Easier interview technique: weighted possibilities

Think of the probability mass producing heads:

Fair coin 1:

\[
\frac13\times\frac12=\frac16
\]

Fair coin 2:

\[
\frac16
\]

Double-headed:

\[
\frac13
\]

Total:

\[
\frac16+\frac16+\frac13
=
\frac23
\]

The double-headed coin contributes:

\[
\frac13
\]

so:

\[
\frac{1/3}{2/3}
=
\frac12
\]

Sometimes enumeration is easier than formally invoking Bayes.

---

# Part II — Counting

## 7. Permutations vs Combinations

### Permutations

Order matters.

Number of ways to arrange \(r\) objects from \(n\):

\[
P(n,r)=\frac{n!}{(n-r)!}
\]

### Combinations

Order does not matter.

\[
{n\choose r}
=
\frac{n!}{r!(n-r)!}
\]

### Example

How many 5-card hands can be drawn from a 52-card deck?

Order doesn't matter:

\[
{52\choose5}
\]

### Recognition

Ask:

> Would ABC and BAC count as different outcomes?

If yes → permutations.

If no → combinations.

---

# 8. Factorials

\[
n! = n(n-1)(n-2)\cdots1
\]

Know small values:

\[
0!=1
\]

\[
3!=6
\]

\[
4!=24
\]

\[
5!=120
\]

\[
6!=720
\]

You probably don't need anything huge.

---

# Part III — Random Variables and Expectation

## 9. Random Variables

A random variable assigns a numerical value to an uncertain outcome.

Example:

Let \(X\) be the number shown on a fair six-sided die.

Then:

\[
X\in\{1,2,3,4,5,6\}
\]

with each probability \(1/6\).

---

# 10. Expected Value

Expected value is the probability-weighted average outcome.

\[
E[X]
=
\sum_x xP(X=x)
\]

### Fair die

\[
E[X]
=
\frac{1+2+3+4+5+6}{6}
=
3.5
\]

This does **not** mean you'll ever roll 3.5.

Expectation is a long-run average.

---

# 11. Expected Value of a Bet

Suppose:

- 20% chance you win \$100.
- 80% chance you lose \$10.

Then:

\[
EV
=
0.2(100)+0.8(-10)
\]

\[
=20-8
\]

\[
=\$12
\]

Positive expected value.

### Interview framework

For any bet:

1. Enumerate outcomes.
2. Assign probability to each.
3. Multiply outcome × probability.
4. Sum.
5. Compare EV against cost.

---

# 12. Linearity of Expectation

Extremely important.

\[
E[X+Y]
=
E[X]+E[Y]
\]

More generally:

\[
E\left[\sum_i X_i\right]
=
\sum_i E[X_i]
\]

**Independence is not required.**

That last sentence is worth remembering.

### Example

You flip 100 fair coins.

Expected number of heads:

Define:

\[
X_i =
\begin{cases}
1 & \text{coin }i\text{ is heads}\\
0 & \text{otherwise}
\end{cases}
\]

Then:

\[
E[X_i]=\frac12
\]

Total heads:

\[
X=X_1+\cdots+X_{100}
\]

Therefore:

\[
E[X]=100\times\frac12=50
\]

---

# 13. Indicator Variables

An indicator variable equals either 0 or 1.

\[
I_A =
\begin{cases}
1 & A\text{ occurs}\\
0 & A\text{ does not}
\end{cases}
\]

Then:

\[
E[I_A]=P(A)
\]

This turns many complicated counting questions into easy expectation problems.

### Useful pattern

If asked:

> What's the expected number of things satisfying condition X?

Define one indicator for each thing and sum their probabilities.

---

# Part IV — Variance

## 14. What Variance Means

Expectation tells you the center.

Variance tells you how spread out outcomes are around that center.

\[
Var(X)
=
E[(X-E[X])^2]
\]

Equivalent formula:

\[
Var(X)
=
E[X^2]-E[X]^2
\]

Standard deviation:

\[
\sigma=\sqrt{Var(X)}
\]

### Intuition

Two investments can both have EV = \$100 while having dramatically different risk.

One always pays \$100.

Another pays:

- \$0 half the time
- \$200 half the time

Same expectation.

Different variance.

For a SWE interview, understanding the intuition is much more important than deriving variance formulas.

---

# Part V — Important Distributions

You should recognize these, not perform advanced derivations.

---

# 15. Bernoulli Distribution

One binary trial.

Examples:

- heads/tails
- success/failure
- user converts/doesn't convert

Let:

\[
X =
\begin{cases}
1 & \text{success}\\
0 & \text{failure}
\end{cases}
\]

with success probability \(p\).

Then:

\[
E[X]=p
\]

\[
Var(X)=p(1-p)
\]

---

# 16. Binomial Distribution

Counts successes in \(n\) independent Bernoulli trials.

\[
X\sim Binomial(n,p)
\]

Probability of exactly \(k\) successes:

\[
P(X=k)
=
{n\choose k}p^k(1-p)^{n-k}
\]

Expectation:

\[
E[X]=np
\]

Variance:

\[
Var(X)=np(1-p)
\]

### Example

Flip 10 fair coins.

Probability exactly 4 are heads:

\[
{10\choose4}
\left(\frac12\right)^4
\left(\frac12\right)^6
\]

or:

\[
{10\choose4}\left(\frac12\right)^{10}
\]

---

# 17. Geometric Distribution

Counts how many trials you need before the first success.

If success probability each trial is \(p\):

\[
E[X]=\frac1p
\]

### Example

Expected flips until first heads:

\[
p=\frac12
\]

Therefore:

\[
E[X]=2
\]

Expected die rolls until first six:

\[
p=\frac16
\]

Therefore:

\[
E[X]=6
\]

### Memoryless property

If you've failed repeatedly, your future waiting time doesn't change.

After rolling a die 100 times without a six, the chance of a six next roll is still:

\[
\frac16
\]

---

# 18. Poisson Distribution

Useful for counting events occurring independently at some average rate.

Examples:

- website requests per second
- defects per meter
- phone calls per minute
- accidents per day

Parameter:

\[
\lambda = \text{expected number of events}
\]

Probability of exactly \(k\):

\[
P(X=k)
=
\frac{e^{-\lambda}\lambda^k}{k!}
\]

Expectation:

\[
E[X]=\lambda
\]

Variance:

\[
Var(X)=\lambda
\]

You mainly need to recognize when Poisson is appropriate.

---

# 19. Normal Distribution

The classic bell curve.

Characterized by:

- mean \(\mu\)
- standard deviation \(\sigma\)

Useful approximation:

- ~68% within \(1\sigma\)
- ~95% within \(2\sigma\)
- ~99.7% within \(3\sigma\)

This is the **68-95-99.7 rule**.

No advanced normal-distribution calculations are necessary.

---

# Part VI — Classic Probability Patterns

# 20. Birthday Problem

Question:

> How many people are needed before there's roughly a 50% chance two share a birthday?

Surprisingly:

**23 people.**

The important method is the complement.

Probability everyone has different birthdays:

\[
P(\text{all unique})
=
\frac{365}{365}
\frac{364}{365}
\frac{363}{365}
\cdots
\]

Therefore:

\[
P(\text{collision})
=
1-P(\text{all unique})
\]

### General lesson

Collision problems are often easiest by calculating:

> probability of no collision.

---

# 21. Monty Hall

Three doors:

- one car
- two goats

You choose door 1.

Host knows where the car is and opens a different door containing a goat.

Should you switch?

Yes.

Initial probability your choice is correct:

\[
\frac13
\]

Initial probability car lies among other two doors:

\[
\frac23
\]

Host deliberately eliminates one losing door.

That entire \(\frac23\) probability effectively concentrates on the remaining unopened alternative.

So:

- stay: \(1/3\)
- switch: \(2/3\)

### Key lesson

The host's action contains information because it is **not random**.

---

# 22. Gambler's Fallacy

After:

HHHHHH

the probability the next fair coin flip is heads is still:

\[
\frac12
\]

Past independent outcomes don't make tails "due."

---

# 23. Base-Rate Neglect

Suppose:

- 1 in 1,000 people has a disease.
- Test detects it 99% of the time.
- False-positive rate is 1%.

A positive result does **not** mean a 99% probability of disease.

Why?

There are many more healthy people available to generate false positives.

When conditional-probability problems feel counterintuitive, simulate a population of:

**1,000 or 10,000 people.**

Natural frequencies often make Bayes dramatically easier.

---

# Part VII — Expected Waiting Time

# 24. Expected Flips Until Heads

Let \(E\) be expected remaining flips.

After one flip:

- heads with probability \(1/2\): you're done.
- tails with probability \(1/2\): you're back where you started.

Therefore:

\[
E
=
1+\frac12(0)+\frac12E
\]

So:

\[
\frac12E=1
\]

\[
E=2
\]

This is a very useful interview technique:

> Define the expected value recursively in terms of itself.

---

# 25. Expected Rolls Until Six

Likewise:

\[
E
=
1+\frac56E
\]

Therefore:

\[
\frac16E=1
\]

\[
E=6
\]

Generalizing:

\[
E=\frac1p
\]

---

# 26. Consecutive Patterns

Questions like:

> Expected flips until HH?

are harder because you need to track **state**.

Possible states:

- no useful previous flip
- one H already seen
- done

Let \(E_0\) = expectation from scratch.

Let \(E_H\) = expectation when the previous flip was H.

Then write equations for both states.

You should understand this technique, but you don't need to memorize every pattern's answer.

### Interview skill

Ask:

> What information about the past actually matters for predicting progress?

Those pieces of information become your states.

---

# Part VIII — Random Walks

# 27. Random Walk Basics

Imagine standing at 0.

Each step:

- +1 with probability 1/2
- -1 with probability 1/2

After \(n\) steps:

Expected position:

\[
E[X_n]=0
\]

But expected **distance from zero** is not zero.

Don't confuse:

\[
E[X]
\]

with:

\[
E[|X|]
\]

### Main intuition

A symmetric random walk has no directional drift, but uncertainty spreads over time.

---

# 28. Gambler's Ruin

Classic setup:

You have \(i\) dollars.

Game ends when you reach:

- \$0
- or \$N.

Each round you win or lose \$1 with equal probability.

For the fair game:

\[
P(\text{reach }N\text{ before }0)
=
\frac{i}{N}
\]

Example:

Start with \$4 and stop at either \$0 or \$10.

Probability of reaching \$10:

\[
\frac4{10}=40\%
\]

You don't need the advanced biased-walk formula unless you have spare time.

---

# Part IX — Expected Value and Decisions

# 29. Positive EV vs Good Decision

Expected value isn't always enough.

Suppose:

- 50% chance of \$2 million
- 50% chance of \$0

EV:

\[
\$1\text{ million}
\]

Would you pay \$900,000 to play?

EV says yes.

Most humans should probably not.

Why?

Because:

- risk matters
- utility isn't linear in money
- bankruptcy constraints matter
- opportunity cost matters

For interview questions, start with EV and then mention these considerations if appropriate.

---

# 30. St. Petersburg Paradox

Flip a fair coin until heads.

If first heads occurs on flip \(n\), payout is:

\[
2^n
\]

Probability first heads occurs on flip \(n\):

\[
\left(\frac12\right)^n
\]

Expected contribution of every possible \(n\):

\[
\left(\frac12\right)^n2^n=1
\]

Therefore:

\[
EV=1+1+1+\cdots=\infty
\]

Yet nobody would rationally pay an arbitrarily large amount to play.

Shows the difference between:

- mathematical expected value
- actual utility / risk / finite resources

Recognize it; don't spend hours studying it.

---

# 31. Value of Information

Sometimes a decision problem asks whether information is worth purchasing.

General structure:

\[
\text{Value of information}
=
EV(\text{best decision after information})
-
EV(\text{best decision without information})
\]

Information has value because it lets you condition future actions.

This is a useful general decision-theory concept.

---

# Part X — Fermi Estimation

This is one of the highest-value areas to practice.

A Fermi problem gives you something you probably don't know and asks you to **estimate it from quantities you can reason about**.

Example:

> How many piano tuners work in Chicago?

The interviewer usually cares more about your decomposition than your final answer.

---

# 32. The Fermi Framework

Always use:

## Step 1: Define the quantity

Clarify what you're counting.

> "I'll count full-time-equivalent piano tuners working within the Chicago metro area."

This prevents ambiguity.

## Step 2: Decompose

Find an equation.

For piano tuners:

\[
\text{tuners}
=
\frac{
\text{number of pianos}
\times
\text{tunings per piano/year}
}{
\text{tunings per tuner/year}
}
\]

## Step 3: Estimate inputs

Use round numbers.

Example:

- Chicago metro population ≈ 10M.
- Maybe 2.5 people/household → 4M households.
- Maybe 1 in 20 households has a piano → 200k pianos.
- Include schools/businesses → perhaps 250k total.
- Average piano tuned once every 2 years → 125k tunings/year.
- Tuner handles perhaps 4/day × 250 days = 1,000/year.

Then:

\[
125,000/1,000
\approx125
\]

So perhaps order of:

\[
10^2
\]

piano tuners.

## Step 4: Sanity-check

Ask:

- Is this plausible relative to population?
- Are units correct?
- Did I accidentally use daily demand against annual capacity?
- Could my estimate be off 10×?

Fermi questions usually care about getting the correct **order of magnitude**, not an exact number.

---

# 33. Top-Down vs Bottom-Up Estimates

There are two major approaches.

## Top-down

Start with a large population.

Example:

> Coffee cups consumed in San Francisco per day.

\[
\text{population}
\times
\text{cups/person/day}
\]

## Bottom-up

Start with production capacity.

\[
\text{coffee shops}
\times
\text{cups/shop/day}
\]

A strong sanity-check is to estimate using **both approaches** and see if they approximately agree.

---

# 34. Useful Fermi Numbers

You don't need exact figures.

Know rough orders of magnitude.

### Time

\[
1\text{ day}\approx10^5\text{ seconds}
\]

because:

\[
24\times60\times60=86,400
\]

\[
1\text{ year}\approx3\times10^7\text{ seconds}
\]

### US population

Order of magnitude:

\[
3\times10^8
\]

### World population

Order of magnitude:

\[
8\times10^9
\]

### Working days/year

Roughly:

\[
250
\]

### Hours/year

\[
365\times24\approx8760\approx10^4
\]

### People per household

Roughly:

\[
2-3
\]

The exact values are less important than being able to operate with reasonable approximations.

---

# 35. Scientific Notation

You should be comfortable manipulating:

\[
10^3=1,000
\]

\[
10^6=1,000,000
\]

\[
10^9=1,000,000,000
\]

Example:

\[
(3\times10^6)(2\times10^3)
=
6\times10^9
\]

Division:

\[
\frac{8\times10^9}{4\times10^3}
=
2\times10^6
\]

This is essential for Fermi questions.

---

# Part XI — Geometry and Physical Estimation

# 36. Distance to the Horizon

Suppose:

- Earth radius \(R\)
- observer height \(h\)
- horizon distance \(d\)

Geometry gives:

\[
(R+h)^2=R^2+d^2
\]

Expand:

\[
R^2+2Rh+h^2
=
R^2+d^2
\]

For \(h\ll R\), ignore \(h^2\):

\[
d^2\approx2Rh
\]

Therefore:

\[
d\approx\sqrt{2Rh}
\]

Use:

\[
R\approx6.4\times10^6m
\]

For eye height:

\[
h\approx2m
\]

Then:

\[
d
\approx
\sqrt{2(6.4\times10^6)(2)}
\]

\[
=\sqrt{25.6\times10^6}
\]

\[
\approx5\times10^3m
\]

About:

**5 km / 3 miles.**

### What this tests

Not whether you memorized Earth's radius perfectly.

It tests whether you can:

1. draw a diagram
2. identify the right geometry
3. simplify
4. approximate a square root

---

# 37. Dimensional Analysis

Units can reveal broken reasoning.

Suppose:

\[
\text{cars/day}
\times
\text{gallons/car}
\]

gives:

\[
\text{gallons/day}
\]

Great.

But:

\[
\text{cars/day}
+
\text{gallons/car}
\]

makes no physical sense.

For any estimation problem, say your units aloud.

This catches a surprising number of errors.

---

# Part XII — Mental Math

You do not need competition-math speed.

You do need comfortable approximation.

---

# 38. Fractions to Know Instantly

\[
\frac12=0.5=50\%
\]

\[
\frac13\approx0.333=33.3\%
\]

\[
\frac23\approx0.667=66.7\%
\]

\[
\frac14=0.25=25\%
\]

\[
\frac34=0.75=75\%
\]

\[
\frac15=0.2=20\%
\]

\[
\frac16\approx0.167
\]

\[
\frac18=0.125
\]

\[
\frac1{10}=0.1
\]

---

# 39. Powers of Two

Useful in software/CS reasoning:

\[
2^5=32
\]

\[
2^8=256
\]

\[
2^{10}=1024\approx10^3
\]

Therefore:

\[
2^{20}\approx10^6
\]

\[
2^{30}\approx10^9
\]

\[
2^{40}\approx10^{12}
\]

---

# 40. Approximate Multiplication

Instead of:

\[
48\times19
\]

think:

\[
48\times20-48
\]

\[
=960-48
\]

\[
=912
\]

For estimates:

\[
49\times21\approx50\times20=1000
\]

Use precision appropriate to the question.

---

# 41. Approximate Square Roots

Know:

\[
\sqrt{4}=2
\]

\[
\sqrt{9}=3
\]

\[
\sqrt{16}=4
\]

\[
\sqrt{25}=5
\]

\[
\sqrt{100}=10
\]

\[
\sqrt{1000}\approx32
\]

\[
\sqrt{10}\approx3.16
\]

For Fermi estimates, often the nearest factor of 2 is sufficient.

---

# 42. Percentage Changes

10% of \(x\):

\[
0.1x
\]

1%:

\[
0.01x
\]

5%:

Half of 10%.

15%:

10% + 5%.

Example:

15% of 80:

\[
8+4=12
\]

---

# Part XIII — Logic and Puzzle Techniques

Do **not** try to memorize hundreds of puzzles.

Learn the recurring tools.

---

# 43. Invariants

An invariant is something that remains unchanged as operations occur.

If a puzzle involves repeated transformations, ask:

> What property cannot change?

Possible invariants:

- parity
- total sum
- color
- modulo class
- number of connected components

---

# 44. Parity

Parity means whether something is:

- even
- odd

Useful facts:

- even + even = even
- odd + odd = even
- odd + even = odd

Many apparently complicated puzzles collapse once you track parity.

---

# 45. Pigeonhole Principle

If you place more than \(n\) objects into \(n\) containers, at least one container contains multiple objects.

Example:

With 13 people, at least two were born in the same month.

Why?

12 months.

13 people.

No probabilities required.

---

# 46. Extreme Cases

When unsure whether reasoning makes sense, test extreme inputs.

Suppose someone claims:

> As the probability of success increases, expected waiting time increases.

Test:

\[
p=1
\]

Success happens immediately.

Expected waiting time must be 1.

So the claim cannot be right.

Extreme cases are excellent sanity checks.

---

# 47. Work Backward

If a problem gives you a desired final configuration, sometimes reasoning backward is much easier than simulating forward.

Ask:

> What must have been true immediately before the goal?

Then repeat.

---

# 48. Two Eggs and a Building

Classic question:

You have two identical eggs and a 100-story building.

There is some highest safe floor \(F\).

An egg survives from floors \(\le F\) and breaks above \(F\).

Find \(F\) minimizing worst-case drops.

The important insight is not the exact answer.

With one egg remaining, you must test sequentially.

So with the first egg, use decreasing jump sizes:

\[
x,\ x-1,\ x-2,\ldots
\]

Choose \(x\) such that:

\[
x+(x-1)+\cdots+1\ge100
\]

Using:

\[
\frac{x(x+1)}2\ge100
\]

Try:

\[
x=14
\]

\[
\frac{14(15)}2=105
\]

So the worst case is **14 drops**.

### General lesson

Balance the worst-case cost across branches.

---

# Part XIV — Communication During Quant Questions

This may matter as much as the math.

---

# 49. How to Start

Don't immediately calculate.

Say something like:

> "Let me define the quantities first."

or:

> "I'll think out loud and break this into pieces."

That buys you structure without sounding evasive.

---

# 50. For Probability Problems

Use:

### 1. Define events

> Let \(A\) be choosing the special coin and \(H\) be observing heads.

### 2. Identify conditioning

> We're not asking \(P(A)\); we're asking \(P(A|H)\).

### 3. Choose method

Could use:

- enumeration
- complement
- Bayes
- expectation
- recursion

### 4. Calculate.

### 5. Sanity-check.

> The posterior should exceed the original \(1/3\), because heads is stronger evidence for the double-headed coin. My \(1/2\) answer satisfies that.

Excellent habit.

---

# 51. For Fermi Problems

Say:

> "I'll make a top-down estimate."

Then:

> "I'm going to assume..."

Then explicitly build:

\[
\text{answer}
=
A\times B\times C
\]

Finally:

> "So I'd call the answer order \(10^X\), perhaps between ___ and ___."

This is much stronger than pretending your assumptions are exact.

---

# 52. When You're Stuck

Don't go silent.

Say:

> "My first approach is getting messy, so I'm going to try the complement."

or:

> "I think I can reduce this by conditioning on the first event."

or:

> "Let me test a smaller version first."

Interviewers can evaluate productive recovery.

They cannot evaluate silent panic.

---

# 53. When You Make a Mistake

If you notice one:

> "Actually, I double-counted that case. Let me correct it."

Then continue.

That is better than defending a wrong answer.

---

# Part XV — Mechanize-Specific Non-Quant Preparation

Your first round may not be exclusively quantitative.

You should be ready for questions about:

- your background
- AI agents
- coding assistants
- why Mechanize
- technical projects
- how you verify AI-generated work

---

# 54. Your 60-Second Introduction

Have a clean structure:

## Present

What you're currently doing.

## Past

The 1–2 most relevant experiences/projects.

## Future

What kind of work you're trying to move toward and why Mechanize fits.

Avoid reciting your entire résumé chronologically.

---

# 55. Why Mechanize?

Understand the broad problem:

Modern coding agents can generate increasingly capable software, but making them robust requires:

- realistic environments
- difficult evaluations
- measuring long-horizon behavior
- detecting brittle solutions
- understanding when agents actually succeed
- giving agents access to tools and environments resembling real software engineering

Your answer should connect:

\[
\text{their problem}
+
\text{your interests}
+
\text{your relevant experience}
\]

Avoid generic AI enthusiasm.

---

# 56. How You Use AI for Programming

Be prepared to discuss:

- code generation
- debugging
- unfamiliar APIs
- codebase exploration
- test generation
- refactoring
- documentation
- brainstorming architecture

But especially:

> How do you determine whether the agent is correct?

Strong answers involve:

- reading the generated code
- running tests
- creating additional tests
- checking edge cases
- validating assumptions
- inspecting diffs
- reproducing bugs
- measuring behavior instead of trusting prose

---

# 57. Failure Modes of Coding Agents

Know several.

### Hallucinated APIs

Agent calls methods/packages that don't exist.

### Locally correct, globally broken

Patch solves the immediate symptom but violates assumptions elsewhere.

### Overfitting to tests

Solution makes visible tests pass without actually satisfying intended behavior.

### Incomplete refactor

Changes one path but misses duplicated or downstream logic.

### Silent assumptions

Agent assumes input types, filesystem layout, environment, API behavior, etc.

### Excessive complexity

Agent creates far more machinery than necessary.

### Security issues

Generated code can introduce:

- injection vulnerabilities
- unsafe deserialization
- auth mistakes
- leaked secrets
- excessive permissions

A strong engineer treats AI output as **untrusted code written very quickly by someone else**.

---

# Part XVI — Problems You Should Be Able to Solve

You should attempt every one of these aloud.

Do not memorize just the answers.

---

## Probability

### 1.

Flip two fair coins.

Probability of exactly one head?

Answer:

\[
\frac12
\]

because:

HT, TH out of HH, HT, TH, TT.

---

### 2.

Roll two dice.

Probability sum is 7?

Six outcomes:

\[
(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)
\]

out of 36.

\[
\frac6{36}=\frac16
\]

---

### 3.

Flip five fair coins.

Probability of at least one head?

\[
1-\left(\frac12\right)^5
=
\frac{31}{32}
\]

---

### 4.

Roll a die until getting a six.

Expected rolls?

\[
6
\]

---

### 5.

10 fair coin flips.

Expected heads?

\[
5
\]

---

### 6.

10 fair coin flips.

Probability exactly five heads?

\[
{10\choose5}\left(\frac12\right)^{10}
\]

---

### 7.

Two dice rolled.

Given at least one is six, probability both are six?

\[
\frac1{11}
\]

---

### 8.

Three coins: two fair, one double-headed.

Observe heads.

Probability you picked double-headed?

\[
\frac12
\]

---

# Fermi Problems

Do these without looking anything up.

## 9.

How many piano tuners are in Chicago?

## 10.

How many Git commits happen globally each day?

## 11.

How many Uber rides happen in Los Angeles each day?

## 12.

How many cups of coffee are consumed in the US each day?

## 13.

How many traffic lights exist in Manhattan?

## 14.

How many gallons of gasoline does the US consume per day?

## 15.

How many software engineers are currently typing code?

For each, force yourself to provide:

1. definition
2. decomposition
3. assumptions
4. arithmetic
5. answer
6. sanity-check

---

# Quantitative Reasoning

## 16.

Estimate how far away the horizon is for someone standing at sea level.

Derive:

\[
d\approx\sqrt{2Rh}
\]

---

## 17.

Estimate how many heartbeats occur during an 80-year lifetime.

Possible decomposition:

\[
80\text{ years}
\times365
\times24
\times60
\times70\text{ beats/min}
\]

Order of magnitude:

billions.

---

## 18.

How many people are flying in airplanes over the US at this instant?

Possible decomposition:

\[
\text{flights in air}
\times
\text{passengers/flight}
\]

or:

\[
\frac{
\text{passenger flights/day}
\times
\text{average flight duration}
}{
24\text{ hours}
}
\]

then multiply by passengers.

There isn't one correct method.

---

# EV Questions

## 19.

50% chance to win \$20.

50% chance to lose \$5.

EV:

\[
0.5(20)+0.5(-5)
=
\$7.50
\]

---

## 20.

You may pay \$4 to roll a die.

If you roll six, receive \$30.

Otherwise receive nothing.

EV of payout:

\[
\frac16(30)=5
\]

Net EV:

\[
5-4=1
\]

Positive EV.

---

# Part XVII — Concepts to Recognize Instantly

When you hear...

### "At least one"

Think:

**complement.**

### "Given that"

Think:

**conditional probability.**

### "Evidence changes probability"

Think:

**Bayes.**

### "Exactly k successes out of n"

Think:

**binomial.**

### "Trials until first success"

Think:

**geometric.**

### "Average number of events per interval"

Think:

**Poisson.**

### "Expected number of objects satisfying something"

Think:

**indicator variables + linearity of expectation.**

### "Repeated process whose future depends on current situation"

Think:

**states + recursion.**

### "Estimate something unknowable"

Think:

**Fermi decomposition.**

### "At least two objects must share..."

Think:

**pigeonhole principle.**

### "Repeated operations"

Think:

**invariants / parity.**

---

# Part XVIII — Common Interview Traps

## Trap 1: Assuming independence

Don't multiply probabilities unless independence is justified.

---

## Trap 2: Ignoring conditioning

After receiving information, your original sample space may no longer apply.

---

## Trap 3: Counting unordered objects as ordered

Check whether order actually matters.

---

## Trap 4: Solving "at least one" directly

Try the complement first.

---

## Trap 5: Excessive precision in estimates

Saying:

> "There are 12,843 piano tuners"

after making five rough assumptions looks worse than:

> "I'd estimate order \(10^4\), probably somewhere around 10–20 thousand."

Precision should match evidence.

---

## Trap 6: Forgetting units

Track:

- people
- people/day
- dollars/person
- miles/hour

etc.

---

## Trap 7: Giving an answer without explaining

Even a correct answer can be weak if the interviewer can't evaluate your thought process.

---

## Trap 8: Continuing broken reasoning

If something feels wrong, stop and restructure.

---

# Part XIX — What You Do NOT Need

Do not spend meaningful preparation time on:

- stochastic calculus
- Ito's lemma
- Black-Scholes
- options pricing
- measure-theoretic probability
- advanced Markov chains
- advanced statistical inference
- difficult integrals
- generating functions
- martingale theory
- continuous-time stochastic processes
- quant-trading strategy
- obscure competition math
- hard dynamic-programming probability problems

This is much more depth than your target interview calls for.

---

# Part XX — Your Formula Sheet

Memorize or deeply understand this page.

## Basic probability

\[
P(A^c)=1-P(A)
\]

\[
P(A\cap B)=P(A)P(B|A)
\]

For independent events:

\[
P(A\cap B)=P(A)P(B)
\]

\[
P(A\cup B)
=
P(A)+P(B)-P(A\cap B)
\]

---

## Conditional probability

\[
P(A|B)
=
\frac{P(A\cap B)}{P(B)}
\]

---

## Bayes

\[
P(A|B)
=
\frac{P(B|A)P(A)}
{P(B)}
\]

---

## Expectation

\[
E[X]
=
\sum_x xP(X=x)
\]

---

## Linearity

\[
E[X+Y]
=
E[X]+E[Y]
\]

No independence required.

---

## Variance

\[
Var(X)
=
E[X^2]-E[X]^2
\]

---

## Binomial

\[
P(X=k)
=
{n\choose k}p^k(1-p)^{n-k}
\]

\[
E[X]=np
\]

\[
Var(X)=np(1-p)
\]

---

## Geometric

\[
E[X]=\frac1p
\]

---

## Combinations

\[
{n\choose k}
=
\frac{n!}{k!(n-k)!}
\]

---

## Horizon approximation

\[
d\approx\sqrt{2Rh}
\]

---

# Part XXI — The Five Mental Models to Master

If you remember nothing else, remember these.

## 1. Change the sample space when given information.

This is conditional probability.

---

## 2. Solve "at least one" by finding "none."

This is the complement trick.

---

## 3. Break expected totals into contributions.

This is linearity of expectation.

---

## 4. Turn impossible-to-know quantities into products of estimable quantities.

This is Fermi estimation.

---

## 5. State assumptions and sanity-check everything.

This is good quantitative reasoning.

---

# Final Interview Checklist

Before the interview, you should be able to answer **yes** to these:

- [ ] I understand conditional probability.
- [ ] I can use Bayes' theorem.
- [ ] I understand independence.
- [ ] I instinctively use complements for "at least one."
- [ ] I know combinations vs permutations.
- [ ] I can calculate expected value.
- [ ] I understand linearity of expectation.
- [ ] I understand what variance represents.
- [ ] I recognize Bernoulli, binomial, geometric, Poisson, and normal distributions.
- [ ] I can solve expected-time-until-success questions.
- [ ] I understand basic random-walk intuition.
- [ ] I understand basic gambler's ruin.
- [ ] I can build a Fermi estimate from scratch.
- [ ] I can manipulate scientific notation mentally.
- [ ] I know common fractions and percentages.
- [ ] I can approximate square roots and large products.
- [ ] I check dimensional units.
- [ ] I know pigeonhole, parity, invariants, and complements.
- [ ] I can talk continuously while reasoning.
- [ ] I can admit and repair a mistake without panicking.
- [ ] I have a concise "Tell me about yourself."
- [ ] I have a specific answer to "Why Mechanize?"
- [ ] I can explain how I use AI coding agents.
- [ ] I can explain how I verify AI-generated code.
- [ ] I can discuss at least one failure mode I've seen from an AI coding tool.

If all of those are comfortable, you are covering the material at the right depth for this interview.

## The desired level

You don't want:

> "I memorized the formula for this exact puzzle."

You want:

> "I've never seen this exact question, but I recognize the structure and know how to reason my way through it."

That is the skill you're actually preparing.