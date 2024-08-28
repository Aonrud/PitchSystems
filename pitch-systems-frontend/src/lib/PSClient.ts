import type { Interval, Scale } from './APITypes'

export default class PSClient {
    API_URL = 'http://127.0.0.1:8000/api/v1'

    constructor() {

    }

    async getIntervals(cents: number[]) : Promise<Interval[]> {
        const endpoint = "/intervals/?cents="
        return await this.query(endpoint, cents)
    }

    async getScales(intervals: Interval[]) : Promise<Scale[]> {
        const endpoint = "/scales/"

        const data = intervals.map(i => i.id)
        return await this.query(endpoint, data)
    }

    async getCents(freqs: number[]): Promise<number[]> {
        const endpoint = "/frequencies/"
        return await this.query(endpoint, freqs)
    }

    protected async query(endpoint: string, data: number[]) : Promise<any> {
        const query = data.join(',')
        const result = await fetch(this.API_URL+endpoint+query)
        return result.json()
    }
}