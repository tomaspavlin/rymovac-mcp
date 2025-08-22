Example of Rymovac MCP server using LangChain/LangGraph.

Followed:
- https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/#3-install-dependencies

# Install

System wide dependencies:
```sh
# 1. Installed python3.13 using pyenv

# 2. for ipynb
pip install jupyterlab
pip install langgraph-sdk # for calling the api

# 3. for cli / studio
pip install --upgrade "langgraph-cli[inmem]"
pip install langgraph
pip install "langchain[anthropic]"
```

# Run ipynb
```sh
jupyter lab
```

# Run studio (sample-project)
```sh
# or without template to choose from list
langgraph new sample-project --template new-langgraph-project-python

# In sample-project/ run:
# Run langgraph studio (in langsmith) for develpment, generates some api (langgraph server?)
langgraph dev
```
