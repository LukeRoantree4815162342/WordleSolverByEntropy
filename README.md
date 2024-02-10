# WordleSolverByEntropy

### Small Python package to solve Wordle puzzles using Shannon entropy of the potential solutions

(dependencies: python3, numpy)

---

### Context

[Wordle](https://www.nytimes.com/games/wordle/index.html) is a word-based puzzle, where you attempt to guess a random 5 letter word in 6 or fewer guesses. 
After each guess, you are given clues about the word - each letter of your guess will be coloured to indicate how that letter relates to the hidden word;

* black: This letter is not in the word

* yellow: This letter is in the word, but not in the same location it was guessed

* green: This letter is in the word, in the same location it was guessed

---

### Overview

This repository contains a) a list of all acceptable 5 letter words for the Wordle game, and b) a minimalist Python library (WordleInfoTheory) to make educated guesses to solve Wordle puzzles

The 'educated guesses' are calculated by scoring every potential 5 letter word based on the sum of the [Shannon entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory)) associated with each letter in the word, based on the relative frequencies of the letters in the corpus of all potential words.

After each guess, the result (colours described above) is given, and the list of potential words is pruned, and the relative letter frequencies regenerated from the remaining words.

---

### Using the solver

The library contains a single class, WordleSolver, which has two methods; 'guess' and 'add_rule'.

An example is given in `WordleSolver_example.ipynb`

A solver object is created as 

`solver = WordleSolver()`

and an itial guess can immediately be generated as

`print(solver.guess())`,

or alternatively, the `n` (e.g. 10) most likely guesses may be generated as 

`print(solver.guess(10))`.

After entering a guess in Wordle, the result will be shown. The solver can then be updated to reflect the feedback given;

`solver.add_rule('guess', ['b','y','g','b','b'])`,

where `'guess'` is the word guessed (as a string), and the second argument is a list of the colours givin in the feedback (`'b'`: black, `'y'`: yellow, `'g'`: green).

The previous two steps can be repeated until the solution is reached, usually in around 3 guesses.

A custom strategy may be supplied when creating the solver object to be used in place of the default entropy-based solver. It must be a function which takes two inputs, the solver itself (to provide access to internal class attributes), and a given word which must be a 5 letter string. It must return a numerical score associated with the word, where the word the highest score corresponds to the most desirable guess.

```
def some_strategy(solver, word):
    ...
    return score

solver = WordleSolver(strategy = some_strategy)
````
