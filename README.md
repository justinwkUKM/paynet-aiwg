# PayNet AI Working Group

This repository hosts materials and resources for the PayNet AI Working Group (AIWG). The AIWG brings together teams across PayNet to present and share knowledge on the latest artificial intelligence concepts, tools, and practices.

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Explore the Jupyter notebooks and supporting source files for each session to follow along with demonstrations and examples.
3. Session-specific projects may include their own `requirements.txt` files. Install them in an isolated environment when you are ready to experiment with that session's code.

## Session 1: Building a Security Deep Research Agent

The notebook [`AIWorkingGroup_01_AIAgents.ipynb`](AIWorkingGroup_01_AIAgents.ipynb) demonstrates how to assemble a simple research agent using tools from the [LangGraph](https://langchain-ai.github.io/langgraph/) ecosystem and the [LiteLLM](https://docs.litellm.ai/) proxy. It walks through:

* Initialising an OpenAI-compatible client pointing at a LiteLLM proxy.
* Generating both streaming and non-streaming responses from a selected model.
* Creating a reactive agent via `create_react_agent`, wiring in custom tools (`get_weather`, `scan_port`, and `lookup_cve`), and storing conversation history with an `InMemorySaver` checkpointer.
* Maintaining context across turns by supplying a thread ID and invoking the agent to recall earlier details (e.g. a user's city) when answering follow-up questions.

To run the notebook locally or in Google&nbsp;Colab:

1. Install the dependencies listed in `requirements.txt`.
2. Provide values for the environment variables `LITELLM_API_KEY`, `LITELLM_URL`, and `LITELLM_MODEL` (Colab users can store these as secrets).
3. Launch Jupyter or open the notebook in Colab and execute the cells sequentially.

The resulting agent showcases how lightweight tools and memory can be combined to build a security-focused deep research assistant.

## Session 2: What is Model Context Protocol (MCP)?

The materials for Session&nbsp;2 live in [`AIWorkingGroup_02_MCP/`](AIWorkingGroup_02_MCP/). This session introduces the [Model Context Protocol](https://modelcontextprotocol.io) and demonstrates how to build, secure, and interact with a simple MCP server.

### Key Components

* [`mcp_server.py`](AIWorkingGroup_02_MCP/mcp_server.py) – a weather-themed MCP server powered by [`FastMCP`](https://github.com/modelcontextprotocol/fastmcp). It exposes tools such as `get_temperature` and `get_windspeed` that call the Open-Meteo APIs, and includes commented code illustrating how to enable token-based authentication.
* [`src/auth.py`](AIWorkingGroup_02_MCP/src/auth.py) – includes a `SimpleTokenVerifier` class demonstrating optional bearer-token validation when running the server in authenticated mode.
* [`mcp_client.ipynb`](AIWorkingGroup_02_MCP/mcp_client.ipynb) – walks through connecting to the MCP server, invoking its tools, and observing the responses.

### Running the server

1. Install the session-specific dependencies:
   ```bash
   cd AIWorkingGroup_02_MCP
   pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   python mcp_server.py
   ```
   The default configuration runs without authentication using the streamable HTTP transport. Uncomment the provided `FastMCP` configuration and supply a valid token (for example, `sk-1234`) to explore the optional authentication flow.
3. Open the accompanying notebook or your preferred MCP-compatible client to connect to the running server and exercise the tools.

The project folder also contains an example `output.log` showcasing sample server interactions.

## Session Schedule

| Session | Title | Team | Date | Location |
|--------:|-------|------|------|----------|
| 01 | Building a Security Deep Research Agent | R&D | 12 September 2025 | Bangsar South |
| 02 | What is Model Context Protocol (MCP)? Build and Secure your MCP servers | R&D | 23 September 2025 | Bangsar South |
| 03 | Automated Red-teaming of AI models & endpoints | R&D | 7 October 2025 | MURUD |
| 04 | Vibe Coding is the future | App Engineering | 21 October 2025 | Bangsar South |
| 05 | Using Uncensored Models for Cybersecurity Tasks | R&D | 4 November 2025 | Bangsar South |
| 06 | AI Driven Code Review & Security Testing | ITS | 18 November 2025 | Bangsar South |

## Contributing

Contributions in the form of session materials, notebooks, or improvements are welcome. Please fork the repository and open a pull request with your changes.

## License

This project is licensed under the terms of the [LICENSE](LICENSE) file.

