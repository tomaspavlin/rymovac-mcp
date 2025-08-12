export interface RhymeResult {
  word: string;
  count: number;
  positive: number;
  negative: number;
  rating: number;
  highlight: boolean;
}

export interface RymovacResponse {
  word: string;
  precision: number;
  source: number;
  total_min: number;
  is_more_rhymes: boolean;
  arr: RhymeResult[];
}

export interface FindRhymesArgs {
  word: string;
  count: number;
  from: number;
}

export interface IsRhymeResponse {
  precision: number;
  is_rhyme: boolean;
  log: {
    full_time: number;
  };
}

export interface CheckRhymeArgs {
  word1: string;
  word2: string;
}