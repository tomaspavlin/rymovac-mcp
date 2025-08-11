# Rymovac MCP Server

A Model Context Protocol (MCP) server that provides access to Czech rhyme finding using the rymovac.cz API.

## Installation

```bash
npm install
npm run build
npm run dev
# or for production: npm start
```

## MCP Tool

The server provides a single tool:

### `find_rhymes`

Find Czech rhymes for a given word or phrase.

**Parameters:**
- `word` (required): The word or phrase to find rhymes for
- `count` (optional): Number of rhymes to return (1-50, default: 10)
- `from` (optional): Starting index for pagination (default: 0)

**Example:**
```json
{
  "word": "slovo",
  "count": 5,
  "from": 0
}
```

**Response:**
```json
{
  "original_word": "slovo",
  "total_rhymes_available": 4,
  "has_more_rhymes": false,
  "returned_count": 2,
  "rhymes": [
    {
      "word": "olovo",
      "rating": 15,
      "count": 513,
      "highlighted": true
    },
    {
      "word": "hotovo",
      "rating": 12,
      "count": 1119,
      "highlighted": true
    }
  ]
}
```

## Testing

### Testing with Claude Desktop

this server to your Claude Desktop configuration:

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

You can test the MCP server using the official MCP Inspector:

```bash
npx @modelcontextprotocol/inspector node dist/index.js
```

For more information about the MCP Inspector, visit: https://modelcontextprotocol.io/legacy/tools/inspector

## Development

### Scripts
- `npm run build` - Build TypeScript to JavaScript
- `npm run dev` - Development mode with auto-restart
- `npm run watch` - Watch mode for TypeScript compilation
- `npm start` - Start the production server

## License

MIT