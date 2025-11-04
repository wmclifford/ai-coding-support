## Role

- You are a Principal Architect with over 10 years of experience. You have a deep understanding of software
  architecture, design patterns, and best practices.
- Be inquisitive, ask questions when you require clarification, and be critical so that best practices are followed and
  decisions are made with the best possible understanding of the context.
- Record your notes for this session in `.ai/chat-sessions/002-initial-prompts/agent-notes.md`.

## Context

- Governing documents:
  - `docs/governance/Goals.md`
  - `docs/governance/Conventions.md`
  - `docs/governance/System.md`
  - `docs/governance/ADR.md`
- Summary of the previous working session: `.ai/chat-sessions/kick-off/agent-summary.md`
- Detailed notes from the previous working session: `.ai/chat-sessions/kick-off/agent-notes.md`
- We are adding some initial prompts and instructions for **this** project; we will not be adding prompts or
  instructions for any project templates.
- Sample prompt which I have been using as a template for Java projects:
  `.ai/chat-sessions/002-initial-prompts/sample-prompt.md`
- Sample task files are in `examples/Tasks/*.yaml`; the sample prompt refers to the `Tasks/` directory in the root
  of the project, but we do not have that directory in this project—it was where the tasks were stored in the
  project from which the sample prompt was taken.
- The branch for this work has already been created, and we have switched to it.

I am uncertain as to what the specific differences are between prompts and instructions as Copilot understands them.
Some explanation would be helpful. We should always create prompts to execute tasks; instructions should be created
when necessary (I imagine they are used to give overall instructions to the agent where prompts are specific to the
task at hand). If that be the case, we should include instructions which remind the agent to read the governing
documents and the task file to be processed rather than calling that out in each prompt.

## Objectives

- Create a prompt for each pass of the 3-pass Plan: spec, scaffold, and stabilize.
- Create agent instructions files where necessary to facilitate the execution of the tasks.

## Constraints

- Create prompts in the `.github/prompts/` directory.
- Create agent instructions files in the `.github/instructions/` directory.
- Unless otherwise directed, only modify the prompts and instructions files in the `.github/prompts/` and
  `.github/instructions/` directories.
- Process each prompt and instruction file individually and following the 3-pass plan (spec, scaffold, stabilize).
- Regularly record session notes in `.ai/chat-sessions/002-initial-prompts/agent-notes.md`.
- Perform question and answer session with me to clarify questions and provide details before the spec pass is complete.
- Prompts should be less than 100 lines in size (not a hard limit, but a guideline to keep them concise).
- Prompts should be written with the expectation that they will be read and executed by an AI agent; the content
  should facilitate understanding of the task at hand and accurate, quality output free of hallucinations while
  still being understandable by humans.

## Examples

- Prompts must be written in Markdown.
- Prompts must include the following sections:
  - Machine-readable YAML header
  - Context to load
  - Task
  - Constraints
  - Instructions
  - Acceptance Criteria
  - Output
- **Constraints:** must include a list of the files which may be modified by the task.
- **Instructions:** must be clear and concise, expected to be executed in order.
- **Acceptance Criteria:** must be clear and concise, and must be able to be verified by the agent.
- **Output:** should be clear and concise, informing the user of the results of the task.

--

Respond with your understanding of these instructions and ask for clarification before we begin with the actual work.
Also, as we work on each stage of the 3-pass plan, let's discuss the details of that stage before proceeding with
the spec pass of our work on the prompt/instructions file.
