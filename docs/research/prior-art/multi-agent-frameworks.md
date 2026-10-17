# Multi-agent frameworks and evidence

Part of the [prior-art survey](../../plans/orchestra/prior-art.md). Researched 2026-10-18 to answer one question: does any framework outside the first ten keep agents focused with little ping-pong, work as a guideline rather than a prescription, and stay small? None does. The closest matches are published patterns and essays, not frameworks, and the evidence supports Orchestra's design.

Sources were fetched from primary pages unless marked "secondhand". Items marked (inference) are the researcher's reading, not a source's claim.

## Findings

1. **Multi-agent gains depend on parallelisable work; coupled coding loses.** Google Research's scaling study (https://arxiv.org/abs/2512.08296) reports results from +80.8% on decomposable financial reasoning to -70.0% on sequential planning, and finds that tasks where a single agent already scores above 45% see negative returns from added agents. On SWE-bench Verified every multi-agent design scored below the single agent (mean 0.522; hybrid -2.1%, centralized -3.1%, decentralized -5.4%, independent -14.9%). Anthropic says "most coding tasks involve fewer truly parallelizable tasks than research". A 2026 paper (https://arxiv.org/html/2609.19759v2) finds a single agent at 76.71 against 75.50 for its own multi-agent method on Terminal Bench 2.1.
2. **Independent checking is the cheapest reliable use of a second agent.** In the scaling study, trace-level error amplification is 17.2x for independent agents and 4.4x for centralized ones, against 1.0x for a single agent. MAST (https://arxiv.org/abs/2503.13657) attributes about 23.5% of failures to task verification (a sum of per-mode shares; versions differ). Cognition's reviewer shares no context with the coder.
3. **Most failures come from specification and termination.** MAST puts about 44% of failures in system design; the top modes are step repetition (15.7%), unawareness of termination conditions (12.4%) and disobeying the task spec (11.8%). Prompt-level fixes were "inconsistent".
4. **Overhead grows with agent count and conversation.** The scaling study measures +58% tokens (independent) to +515% (hybrid), and 44.3 turns for hybrid against 7.2 for a single agent. Anthropic's research system uses about 15x the tokens of chat. Adding agents from four to six lowered scores in the 2609.19759 paper.
5. **Long instructions cost more than they return.** An ETH Zurich/LogicStar study (https://arxiv.org/abs/2602.11988) found that context files "do not generally improve task success rates" and raise inference cost by over 20%. A smaller study (arXiv 2601.20404, secondhand) found the opposite, so the evidence is mixed.

Figures differ slightly between versions of the scaling paper (the researchers read different versions), so check the version before quoting a number.

## Closest matches to Orchestra's two criteria

| Rank | Source | Why it fits | Gap |
| --- | --- | --- | --- |
| 1 | Anthropic, [multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | Subagents get an explicit brief (objective, output format, tool guidance, boundaries), write results to files and return lightweight references. The lead saves its plan to external memory. It says when not to use multiple agents. | Research tasks, not coding; an essay, not a framework |
| 2 | Anthropic, [harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) (April 2026) | Planner, generator and a separate skeptical evaluator hand off through files; they agree a "sprint contract" that defines done before coding. Each part is an assumption to re-test with each new model. Solo run: 20 min and $9, broken result; harness: about $200 over 6 h, working. | One task type; the sprint construct was later dropped |
| 3 | Cognition, [Don't build multi-agents](https://cognition.com/blog/dont-build-multi-agents) (2025) and [Multi-agent systems in production](https://cognition.com/blog/multi-agents-working) (2026-04-22) | "Writes stay single-threaded"; a review agent sees only the diff and shares no context with the coder; unstructured swarms are "mostly a distraction". | A principle, not a kit; the 2026 post was read through a mirror in one of the two reports |
| 4 | Roo Code [Boomerang](https://roocodeinc.github.io/Roo-Code/features/boomerang-tasks) | Star topology: the orchestrator delegates with `new_task`, each subtask runs in isolation and only its `attempt_completion` summary returns. By default the orchestrator cannot read files or run commands. Subtasks never talk to each other. | Tied to Roo Code |
| 5 | Aider [architect/editor](https://aider.chat/2024/09/26/architect.html) | One handoff, a plan to edit instructions. o1-preview alone scored 79.7%; with DeepSeek as editor, 85.0%. The only controlled gain from role splitting found. | 2024 data on Aider's own benchmark |
| 6 | [Factory Missions](https://docs.factory.com/missions/overview) | Orchestrator, fresh worker session per feature, independent validators, a validation contract set before coding. Docs admit parallel execution is untested against sequential. | Closed product, medium prescription |
| 7 | [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) and [context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Pure guidance: use the simplest solution, aim for "the smallest set of high-signal tokens", prompt at the "right altitude", pass file paths and load them just in time. | Vocabulary, no mechanics |

## Frameworks checked and set aside

| Framework | Source | Why it does not fit |
| --- | --- | --- |
| Claude Code agent teams | https://code.claude.com/docs/en/agent-teams | Any teammate can message any other through mailbox files; that is the ping-pong Orchestra avoids. Docs recommend 3-5 teammates and say it suits parallel research and review, not same-file work. Mechanism only, low prescription. Hooks such as `TaskCompleted` are usable as quality gates. |
| ruflo / claude-flow | https://github.com/ruvnet/ruflo | About 100 agents, 314 MCP tools, 27 hooks; queen-led swarms with consensus topologies. Its README counts are inconsistent and its claims are self-reported. |
| oh-my-claudecode | https://github.com/Yeachan-Heo/oh-my-claudecode | 19 agents plus tiers; fixed pipeline (plan, prd, exec, verify, fix loop). Reviewer workers write verdict files that the lead reads, which resembles Orchestra's file contract, but the whole is moderately to highly prescriptive. |
| oh-my-opencode | https://github.com/code-yeongyu/oh-my-openagent | Marketing-level README; delegation design not verifiable. |
| CCPM | https://github.com/automazeio/ccpm | Five-phase discipline ("No Vibe Coding") on GitHub issues and worktrees. Its 100% against 27.7% benchmark is the author's own. |
| Task Master | https://github.com/eyaltoledano/claude-task-master | A task manager, not a team. 36 MCP tools by default (about 21k tokens of context), trimmable to 7; a warning about tool-surface bloat. |
| VoltAgent awesome-subagents | https://github.com/VoltAgent/awesome-claude-code-subagents | A catalogue of 100-161 role prompts; the opposite of few agents. |
| Gemini CLI Conductor | https://github.com/gemini-cli-extensions/conductor | Single agent, six commands, files as the contract (`product.md`, `tech-stack.md`, per-track `spec.md` and `plan.md`). Fairly prescriptive, no independent checker. |
| Agent OS | https://github.com/buildermethods/agent-os | Small standards system (discover, deploy, shape-spec). Not multi-agent. |
| LangGraph supervisor | https://github.com/langchain-ai/langgraph-supervisor-py | Archived; the README now recommends hand-rolling the pattern for context control. Its `last_message` output mode is the same idea as short reports. LangChain's benchmark (https://www.langchain.com/blog/benchmarking-multi-agent-architectures) found the supervisor loses accuracy when relaying worker output. |
| CrewAI, OpenAI Agents SDK, Microsoft Agent Framework (AutoGen successor), Agno, Google ADK | https://docs.crewai.com/en/concepts/crews, https://github.com/openai/openai-agents-python, https://docs.agno.com/basics/teams/overview | Runtime libraries with many concepts. The Microsoft and ADK claims are secondhand or from background knowledge. |
| MetaGPT, ChatDev 2.0, Magentic-One | https://github.com/FoundationAgents/MetaGPT, https://github.com/OpenBMB/ChatDev, https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/magentic-one.html | MetaGPT's role set (product manager, architect, project manager, engineer) is closest to Orchestra's, but all three are prescriptive runtimes. Magentic-One's task and progress ledgers are an idea worth knowing. |
| agents-concerto | https://github.com/moruno21/agents-concerto | Not opened. Its README, as summarised, separates the agent that writes code from the one that approves it, and uses isolated worktrees. Worth a read. |

## What this implies for Orchestra

- **The single-writer default holds.** Add a context when work is independent or needs a fresh view, which matches the plan's four cases. Do not fan out implementation by default (M3 risk).
- **Keep the checker's rule: artifact and exit criteria only.** It is the most consistently supported idea across Cognition, Google and MAST.
- **Put done criteria and a stop condition in every brief.** Specification and termination failures outweigh model limits in MAST (inference: these few lines matter more than extra roles).
- **Keep handoffs one-way and short.** Files plus references, not transcripts; no multi-turn negotiation between roles. This is why agent-teams-style peer messaging stays out of the idea, requirements and architecture flows.
- **Borrow the harness post's discipline of re-testing each role against the newest model.** It fits the coach's removal trials and the single-agent baseline.
- **Evidence gap.** No source shows a multi-agent loop beating a single agent on tightly coupled coding. The M1 baseline stays the defense.

## Not verified

Not opened: SWE-agent, Cline, Windsurf and Cursor internals, the agentskills.io specification, the Chroma context-rot report, the Silo-Bench paper (secondhand: teams lose 15-49% of single-agent performance at two agents), and the agents-concerto repo. Cursor and Codex multi-agent features were read through secondary sources only.
