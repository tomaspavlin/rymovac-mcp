# Rymovac MCP Server

A Model Context Protocol (MCP) server that provides access to Czech rhyme finding using the rymovac.cz API.

## Installation

```bash
npm install
npm run build
npm run start
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
- `npm start` - Start the production server
- `npm run inspect` - Start and testing with MCP Inspector
- `npm run watch` - Watch mode for TypeScript compilation only

## Testing

### Testing with Claude Desktop

Add this server to your Claude Desktop configuration:

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

## License

MIT
