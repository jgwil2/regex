# Regex

## Purpose

Regular expressions describe regular languages, which can be recognized by automata. Regular expression engines work by simulating these automata. Most academic descriptions of such automata treat them as graphs whose edges are associated with a character (TODO add citations). However, all regular expression implementations that I have seen actually represent automata as graphs whose *nodes* are associated with a character, which changes the algorithms used to construct and simulate them. This implementation is intended to follow the mathematical definition of automata more closely.
