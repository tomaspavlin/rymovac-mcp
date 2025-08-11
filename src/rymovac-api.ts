import axios from "axios";
import { RymovacResponse, FindRhymesArgs } from "./types.js";

export class RymovacAPI {
  private static readonly BASE_URL = "https://rymovac.cz/api/v1";
  
  static async findRhymes(args: FindRhymesArgs): Promise<RymovacResponse> {
    const { word, count, from } = args;
    
    const url = `${this.BASE_URL}/rhymes/${encodeURIComponent(word)}`;
    const params = {
      precision: 0,
      source: 3,
      from,
      count
    };

    try {
      const response = await axios.get<RymovacResponse>(url, { params });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(`API request failed: ${error.response?.status} - ${error.response?.statusText}`);
      }
      throw new Error(`Unexpected error: ${error}`);
    }
  }
}