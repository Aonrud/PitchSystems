import type { Cents, Interval, Scale } from './APITypes'
import { PUBLIC_API_URL } from '$env/static/public'

export default class PSClient {
    API_URL: string = PUBLIC_API_URL

    async getIntervals(cents: number[]): Promise<Interval[]> {
        //Normalise octaves for negative cents values
        cents = cents.map((c) => (c < 0 ? Math.round(+1200 + +c) : Math.round(c)))

        const endpoint = "/intervals/"
        const params = [{ "name": "cents", "value": cents.join(",") }]
        return await this.query(endpoint, [], params)
    }

    async getIntervalsNear(cents: number, tolerance: number = 0): Promise<Interval[]> {

        //Negative intervals are measured by interval upwards from root
        if (cents < 0) {
            cents = +cents + +1200;
        }

        let endpoint = `/intervals/near/`
        let params = [];
        if (tolerance > 0) {
            params.push({ "name": "tolerance", "value": tolerance.toString() })
        }
        return await this.query(endpoint, [Math.round(cents)], params)
    }

    async getScales(intervals: Interval[]): Promise<Scale[]> {
        const endpoint = "/scales/"

        const data = intervals.map(i => i.id)
        return await this.query(endpoint, data)
    }

    async getCents(freqs: number[], root: number = -1): Promise<Cents[]> {
        let params = [];
        if (root > 0) {
            params.push({ "name": "root", "value": root.toString() })
        }
        let endpoint = "/frequencies/"
        return await this.query(endpoint, freqs, params)
    }

    protected async query(endpoint: string, data: number[], params: { "name": string, "value": string }[] = []): Promise<any> {
        let query = data.join(',')
        if (params) {
            query += "?"
            for (let param of params) {
                query += `${param.name}=${param.value}&`
            }
        }
        const result = await fetch(this.API_URL + endpoint + query)
        return result.json()
    }
}