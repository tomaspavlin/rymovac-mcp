# Rymovac MCP Server

MCP server that makes LLMs write poetry that actually rhymes. This Model Context Protocol server provides tools for Czech rhymes using the [rymovac.cz](https://rymovac.cz/) API.

## Usage

Add this server to your Claude Desktop/Cursor configuration:

```json
{
  "mcpServers": {
    "rymovac": {
      "command": "npx",
      "args": ["-y", "@rymovac/mcp"]
    }
  }
}
```

## Components

The server provides:

### Tools

#### `find_rhymes`

Find Czech rhymes for a given word or phrase.

**Parameters:**
- `word` (required): The word or phrase to find rhymes for
- `count` (optional): Number of rhymes to return (1-50, default: 10)
- `from` (optional): Starting index for pagination (default: 0)

#### `check_rhyme`

Check if two Czech words, phrases, verses, or poem rows rhyme.

**Parameters:**
- `word1` (required): The first Czech word, phrase, verse, or poem row to compare
- `word2` (required): The second Czech word, phrase, verse, or poem row to compare

### Prompts

#### `czech-poem-guide` (experimental)

A comprehensive guide for writing Czech poems using the rhyme finder.

**Parameters:**
- `theme` (optional): Theme or topic for the poem
- `verses` (optional): Number of verses/stanzas (default: 4)

## Prompt

For better results in poetry generating, use this LLM prompt:

```
When writing poetry, always follow the following.

Content:
- Plan a narrative arc that builds to a surprising conclusion
- Develop a surprising twist, punchline, or deeper message
- Consider unexpected angles or ironic perspectives on the topic
- Consider misdirection - lead readers one way, then reveal something unexpected

Format:
- If user not tell otherwise, use rhyme scheme AABB and write 1-2 stanzas.

Focus on Rhymes:
- BEFORE writing each stanza, find suitable rhyming pairs
- First look for rhymes for thematic words using the provided tool, search for words in multiple forms as "bratr", "bratře", "bratříček", ...
- Then use the found rhymes to write meaningful stanza
- Verify that the written lines actually rhyme using rhyme-checking tools. Do not compare only last words, but the whole lines
- Only then write complete verses around these rhymes

Grammar:
- Always check grammar. If incorrect or sound weird, rewrite

Before writing the poem, ALWAYS VERIFY:
- That grammar is flawless !!!
- That the line pairs actually rhymes using rhyme-checking tool !!!
- That it makes sense !!!
```

## Development

### Installation

```bash
npm install
npm run build
npm run start
```

### Scripts
- `npm run build` - Build TypeScript to JavaScript
- `npm start` - Start the production server
- `npm run inspect` - Start and testing with MCP Inspector
- `npm run watch` - Watch mode for TypeScript compilation only

## Testing

### Testing with Claude Desktop

Add this to configuration:

```json
{
  "mcpServers": {
    "rymovac": {
      "command": "node",
      "args": ["/path/to/rymovac-mcp/dist/index.js"]
    }
  }
}
```

### Testing with MCP Inspector

You can test the MCP server using the official MCP Inspector (https://modelcontextprotocol.io/legacy/tools/inspector):

```bash
npm run inspect
```

### Publishing as NPM package

1. Update version in package.json
2. `npm publish`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
