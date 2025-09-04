## Project description

This project creates MCP server rymovac-mcp.
The server uses api of rymovac.cz website for finding czech rhymes for a given word.

Use this doc of MCP: https://modelcontextprotocol.io/quickstart/server#implementing-tool-execution-2

## Rymovac API

The project uses these endpoints:

### 1. Find rhymes endpoint:
- GET /api/v1/rhymes/<word>
- Example: https://rymovac.cz/api/v1/rhymes/slovo?precision=0&source=3&from=0&count=10
  - parameters:
    - precision - always use 0 for automatic precision
    - source - always use 3
    - from/count - paging throught rhymes, example: from=0,count=10 for first page, from=10,count=10 for second page etc.
    - <word> - word to find rhymes for. It can also be a whole sentence/verse. In that case it will find rhyme to that verse ending.
- Example endpoint output:
    ```json
    {"word":"Slovo","precision":3,"source":3,"total_min":4,"is_more_rhymes":true,"arr_stats":{"nonzero_rating_count":2,"positive_rating_count":2,"highlight_count":2},"arr":[{"word":"olovo","count":513,"positive":24,"negative":9,"rating":15,"highlight":true,"debug":{"thumb_up":24,"thumb_down":9,"add":0,"sum":15,"category":"promote"}},{"word":"hotovo","count":1119,"positive":18,"negative":6,"rating":12,"highlight":true,"debug":{"thumb_up":18,"thumb_down":6,"add":0,"sum":12,"category":"promote"}}],"log":{"full_time":2.032456874847412,"sql_time_promote":0.003512859344482422,"sql_time_other":2.0271120071411133}}
    ```

### 2. Check rhyme endpoint:
- GET /api/v1/is-rhyme?word1=<word1>&word2=<word2>
- Example: https://rymovac.cz/api/v1/is-rhyme?word1=kocka&word2=ocka
  - parameters:
    - word1 - first word/phrase/verse to compare
    - word2 - second word/phrase/verse to compare
    - Both parameters can be single words or whole sentences/verses
- Example endpoint output:
    ```json
    {"precision":4,"is_rhyme":true,"log":{"full_time":0.123}}
    ```

## Examples

### LangGraph Poetry System

Located in `examples/langgraph/poet/`, this is a poetry generation and evaluation system built with LangGraph that demonstrates usage of the rymovac MCP server.

**Workflow:**
1. **Ideator** (`src/agent/nodes/ideator.py`) - Creates story ideas/themes for poems in bullet points
2. **Writer** (`src/agent/nodes/writer.py`) - Writes 4-line poems based on the story, or improves them based on feedback
3. **Grammar Evaluator** (`src/agent/nodes/grammar_evaluator.py`) - Checks grammar correctness
4. **Rhymes Evaluator** (`src/agent/nodes/rhymes_evaluator.py`) - Verifies if the poem rhymes using rymovac tools
5. **Summarizer** (`src/agent/nodes/summarizer.py`) - Provides final summary

**Graph flow:**
- START → Ideator → Writer → Grammar Evaluator
- If rejected: loops back to Writer (max 5 iterations via `MAX_ITERATIONS`)
- If accepted: proceeds to Rhymes Evaluator
- If rhymes rejected: loops back to Writer
- If rhymes accepted: goes to Summarizer → END
