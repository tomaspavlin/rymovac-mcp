#!/usr/bin/env node

import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { RymovacAPI } from "./rymovac-api.js";
import { formatRhymesResult } from "./formatters.js";

const server = new McpServer(
  {
    name: "rymovac-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.registerTool(
  "find_rhymes",
  {
    title: "Find Czech Rhymes",
    description: "Find Czech rhymes for a given word or phrase using the rymovac.cz API",
    inputSchema: {
      word: z.string().min(1, "Word cannot be empty"),
      count: z.number().min(1).max(50).default(10),
      from: z.number().min(0).default(0)
    }
  },
  async ({ word, count = 10, from = 0 }) => {
    try {
      const result = await RymovacAPI.findRhymes({ word, count, from });
      const output = formatRhymesResult(result);

      return {
        content: [
          {
            type: "text",
            text: output
          }
        ]
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: error instanceof Error ? error.message : String(error)
          }
        ],
        isError: true
      };
    }
  }
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Rymovac MCP server running on stdio");
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});