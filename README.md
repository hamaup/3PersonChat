# 3PersonChat

This repository contains documentation for a hybrid AI and human chat system. See `spec_design.md` for the specification and design outline in Japanese.

## Running the demo

The repository includes a simple command line demo of the hybrid chat flow.
Run it with:

```bash
python chat.py
```

Type messages in Japanese. When the bot detects low confidence or keywords,
it prompts for a human operator response.
