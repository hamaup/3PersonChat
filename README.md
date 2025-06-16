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

Type messages in Japanese. After each message the bot asks whether you want to
talk to an operator. Answer `y` to chat with the operator or `n` to continue with
the bot.

To visualize the workflow, you need the optional `pygraphviz` package and the
Graphviz system libraries.

```bash
sudo apt-get install graphviz graphviz-dev  # Ubuntu/Debian
pip install pygraphviz
python langgraph_chat.py --draw-graph
```

If `pygraphviz` is not available, you can still run the demo without the
`--draw-graph` option. The graph will be skipped and the chatbot works as usual.

Running with `--draw-graph` writes `workflow.png` showing the conversation
workflow.
