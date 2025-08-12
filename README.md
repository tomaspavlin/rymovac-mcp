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

### Prompts

#### `czech-poem-guide` (experimental)

A comprehensive guide for writing Czech poems using the rhyme finder.

**Parameters:**
- `theme` (optional): Theme or topic for the poem
- `verses` (optional): Number of verses/stanzas (default: 4)

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
