# Regex

## Purpose

Regular expressions describe regular languages, which can be recognized by automata. Regular expression engines work by simulating these automata. Most academic descriptions of such automata treat them as graphs whose edges are associated with a character (see Sipser, _Introduction to the Theory of Computation_, for example). However, all regular expression implementations that I have seen actually represent automata as graphs whose _nodes_ are associated with a character, which changes the algorithms used to construct and simulate them. This implementation is intended to follow the mathematical definition of automata more closely.

Following [Cox (and Thompson)](https://swtch.com/~rsc/regexp/regexp1.html), this implementation first converts a regular expression to a postfix form via [Dijkstra's shunting-yard algorithm](https://en.wikipedia.org/wiki/Shunting-yard_algorithm). This convenient format is then used to build an NFA corresponding to the given expression.

## Classes

### Token

A token represents a set of characters or an operation in the language of regular expressions. Using token objects instead of literal characters makes it easier to support ranges (e.g. `[A-Z]` or `[0-9]`).

### Regex

Regex objects are the interface exposed by this library. Under the hood they are a wrapper for the NFA class. They are initialized with a string given in the language of regular expressions and provide a `test` method to check whether strings match the regular language described by the initial string.

### NFA

A [nondeterministic finite automaton](https://en.wikipedia.org/wiki/Nondeterministic_finite_automaton) is a state machine that can recognize a regular language. It can be thought of as a directed graph whose nodes represent states that the machine can possibly be in and whose edges represent transitions between those states. Each edge is associated with a set of characters: as the machine reads input a character at a time, it follows any edges that correspond to the current character and transitions to a new state. A state that has just been transitioned to is called an active state. Each state is an accept state or not. When the machine has consumed all input characters, if any active states are accept states, the machine is said to recognize the input string; that is to say, the string is a valid sentence in the regular language that the machine recognizes.

### State

A state is a node in a graph. An NFA always has one start state, and one or more accept states. As it consumes input characters, the active states are updated; after consuming each character, the states that have been most recently transitioned to are the active states.

### Edge

An edge represents a connection between states. States are connected by a character. When the NFA processes a character, it follows any edges with that character, as well as any edges with the empty string.
