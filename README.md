# Rymovac MCP Server

A Model Context Protocol (MCP) server that provides access to Czech rhyme finding using the rymovac.cz API.

## Installation

```bash
npm install
npm run build
```

## MCP Tool

The server provides a single tool:

### `find_rhymes`

Find Czech rhymes for a given word or phrase.

**Parameters:**
- `word` (required): The word or phrase to find rhymes for
- `count` (optional): Number of rhymes to return (1-50, default: 10)
- `from` (optional): Starting index for pagination (default: 0)

## Development

### Scripts
- `npm run build` - Build TypeScript to JavaScript
- `npm run dev` - Development mode with auto-restart
- `npm run watch` - Watch mode for TypeScript compilation
- `npm start` - Start the production server

## License

MIT

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
