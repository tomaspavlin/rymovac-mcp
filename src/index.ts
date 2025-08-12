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
      prompts: {},
    },
  }
);

server.registerTool(
  "find_rhymes",
  {
    title: "Find Czech Rhymes",
    description: "Find Czech rhymes for a given word or phrase using the rymovac.cz API.",
    inputSchema: {
      word: z.string().min(1, "Word cannot be empty").describe("The Czech word or phrase to find rhymes for. Can be a single word like 'slovo' or a phrase/verse/poem row like 'Tohle je krásné slovo'. The API will find words that rhyme with the ending."),
      count: z.number().min(1).max(50).default(10).describe("Maximum number of rhymes to return (1-50). Default is 10. Set to 10 if user does not tell otherwise."),
      from: z.number().min(0).default(0).describe("Starting index for pagination (0-based). Use 0 for first page, 10 for second page (if count=10), etc. Useful when there are many rhymes available and you want to see additional results.")
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

server.registerTool(
  "check_rhyme",
  {
    title: "Check if Words Rhyme",
    description: "Check if two Czech words, phrases, verses, or poem rows rhyme. It uses the rymovac.cz API.",
    inputSchema: {
      word1: z.string().min(1, "First word/phrase cannot be empty").describe("The first Czech word, phrase, verse, or poem row to compare. Can be a single word like 'kocka' or a whole verse/phrase like 'V noci temné'."),
      word2: z.string().min(1, "Second word/phrase cannot be empty").describe("The second Czech word, phrase, verse, or poem row to compare. Can be a single word like 'ocka' or a whole verse/phrase like 'pod hvězdami jemné'.")
    }
  },
  async ({ word1, word2 }) => {
    try {
      const result = await RymovacAPI.checkRhyme({ word1, word2 });
      
      const rhymeStatus = result.is_rhyme ? "✓ DO RHYME" : "✗ DO NOT RHYME";
      const output = `The following phrases ${rhymeStatus}:\n- "${word1}"\n- "${word2}"`;

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

server.registerPrompt(
  "czech-poem-guide",
  {
    title: "Czech Poetry Writing Guide",
    description: "Instructions for writing Czech poems using the Rymovac MCP server to find rhymes",
    argsSchema: {
      theme: z.string().optional().describe("Optional theme or topic for the poem"),
      verses: z.string().optional().describe("Number of verses/stanzas in the poem (2-20, default: 4)")
    }
  },
  ({ theme, verses = "4" }) => ({
    messages: [{
      role: "user", 
      content: {
        type: "text",
        text: `# Czech Poetry Writing Guide

You are helping to write Czech poems using the rymovac MCP server. Follow these guidelines:

## Poem Structure:
- Write ${verses} verses (stanzas)
- Each verse should have 4 lines
- Number each line: 1., 2., 3., 4., 5., etc.
- Each line should be on a separate line in your response

## Using the Rymovac Tool:
1. **Find rhymes for line endings**: Use the find_rhymes tool with the last word or phrase of each line
2. **Word parameter**: You can search for:
   - Single words: "slovo" 
   - Phrases/verse endings: "krásné slovo", "v noci temné"
   - The tool finds words that rhyme with the ending
3. **Rhyme schemes**: Common patterns are AABA, ABAB, or AABB

## Writing Process:
1. Start with your first line${theme ? ` about "${theme}"` : ""}
2. Use find_rhymes to find words that rhyme with the ending
3. Write the second line using a rhyming word
4. Continue building verses with consistent rhyme scheme
5. Ensure the poem flows naturally and makes sense

## Example workflow:
1. Write: "1. V zahradě roste krásné slovo"
2. Use find_rhymes with "slovo" 
3. Choose a rhyme like "olovo" for line 3
4. Write: "3. Těžké jako olovo"

## Tips:
- Czech poetry often uses metaphors and imagery
- Pay attention to syllable count for rhythm
- Use the rating from rhymes to pick the best matches
- Don't force rhymes - natural flow is important

${theme ? `\n## Your Task:\nWrite a Czech poem about "${theme}" following the guidelines above.` : "\n## Your Task:\nWrite a Czech poem following the guidelines above."}

Begin by writing your first line, then use the find_rhymes tool to help craft the rest of the poem.`
      }
    }]
  })
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