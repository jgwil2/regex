# Regex

## Purpose

Regular expressions describe regular languages, which can be recognized by automata. Regular expression engines work by simulating these automata. Most academic descriptions of such automata treat them as graphs whose edges are associated with a character (TODO add citations). However, all regular expression implementations that I have seen actually represent automata as graphs whose *nodes* are associated with a character, which changes the algorithms used to construct and simulate them. This implementation is intended to follow the mathematical definition of automata more closely.

Following [Cox (and Thompson)](https://swtch.com/~rsc/regexp/regexp1.html), this implementation first converts a regular expression to a postfix form via [Dijkstra's shunting-yard algorithm](https://en.wikipedia.org/wiki/Shunting-yard_algorithm). This convenient format is then used to build an NFA corresponding to the given expression.

The implementation should use immutable data structures and rely on the fact that the class of regular languages is closed under the regular operations (union, concatenation, star). This means that more complex machines can be constructed from simple machines using simple algorithms.
