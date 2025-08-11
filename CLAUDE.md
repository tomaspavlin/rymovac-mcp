## Project description

This project creates MCP server rymovac-mcp.
The server uses api of rymovac.cz website for finding czech rhymes for a given word.

Use this doc of MCP: https://modelcontextprotocol.io/quickstart/server#implementing-tool-execution-2

## Rymovac API

The project uses this endpoint:
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
