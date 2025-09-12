# PayNet AI Working Group

This repository hosts materials and resources for the PayNet AI Working Group (AIWG). The AIWG brings together teams across PayNet to present and share knowledge on the latest artificial intelligence concepts, tools, and practices.

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Explore the Jupyter notebooks for each session to follow along with demonstrations and examples.

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

