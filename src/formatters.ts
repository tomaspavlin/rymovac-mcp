import { RymovacResponse } from "./types.js";

export function formatRhymesResult(result: RymovacResponse): string {
  let output = '';
  
  if (result.arr.length > 0) {
    output += `Rhymes for "${result.word}":\n`;
    output += result.arr.map(rhyme => `- ${rhyme.word}`).join('\n');
  } else {
    output += `No rhymes for "${result.word}" found.\n`;
  }
  
  if (result.is_more_rhymes) {
    output += `\n\nThere are more rhymes for "${result.word}" available.`;
  }
  
  return output;
}