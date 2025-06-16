# 3PersonChat

This repository contains documentation for a hybrid AI and human chat system. See `spec_design.md` for the specification and design outline in Japanese.

## Running the demo

The repository includes a simple command line demo of the hybrid chat flow.
Run it with:

```bash
python chat.py
```

## LangGraph demo


An alternative implementation using [LangGraph](https://github.com/langchain-ai/langgraph) is provided. Install the package with:

```bash
pip install langgraph
```

Run the demo with:


```bash
python langgraph_chat.py
```


Type messages in Japanese. If you include keywords such as `OP` or `オペレーター`,
the conversation is handed off to a human operator. Otherwise the AI responds.

To visualize the workflow, install `pygraphviz` and run:

```bash
pip install pygraphviz
python langgraph_chat.py --draw-graph
```

This writes `workflow.png` showing the conversation graph.

