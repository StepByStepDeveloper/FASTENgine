# Skill: surf

Perform deep research on a given topic, problem, or task using web search tools, synthesize the gathered information, and then use that knowledge to complete the user's objective.

## Process

### Phase 1: Information Gathering (The Search)
1. **Formulate Queries**: Create multiple queries to cover different angles.
2. **Execute Searches**: Use `searxng_web_search` or `webfetch`.
3. **Deep Dive**: Use `web_url_read` for promising but insufficient snippets.

### Phase 2: Synthesis & Analysis (The Intelligence)
1. **Filter Noise**: Discard irrelevant/outdated info.
2. **Identify Key Facts**: Extract API signatures, version numbers, or error solutions.
3. **Cross-Reference**: Resolve conflicts between sources.
4. **Create a Summary**: Organize findings into logical groups.

### Phase 3: Task Execution (The Action)
1. **Map Findings to Task**: Determine how new information changes the approach.
2. **Execute**: Perform requested action (write code, fix bug, etc.) using researched facts.
3. **Verify**: Ensure implementation aligns with latest documentation.

## Anti-Patterns
- "Surface-level searching" (missing details).
- Relying on outdated training data.
- Skipping synthesis (dumping raw URLs).
