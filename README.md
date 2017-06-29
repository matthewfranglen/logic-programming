Logic Programming
=================

This is a toy demonstration of logic programming implemented in python.

This currently supports searching a fact graph for expressions where the
expressions are defined as a graph of labelled edges. A solution is a subgraph
of the fact graph which has vertexes with matching edges.

Installation
------------

I recommend using pyenv for this:

```
pyenv install 3.6.1
pyenv virtualenv 3.6.1 logic
pyenv activate logic
pip install -r requirements.txt
```

Execution
---------

```
python logic.py
```

Currently this evaluates a fixed expression over a randomly generated fact graph.
This will print the generated graph, the expression, and the first 10 solutions found.

Performance
-----------

Currently terrible. I have not seen this complete an infinite expression yet.

Something to work on.
