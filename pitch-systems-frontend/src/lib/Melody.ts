import type { Cents, Frequency, Interval, Scale } from './APITypes';

/**
 * Represents an analysed file and its results
 * @param id: string
 * @param name: string
 * @param path: string
 */
export default class Melody {
    readonly id: string;
    readonly path: string;

    pending: boolean = true;
    name: string;
    frequencies: Frequency[] = [];
    root?: number;
    cents: Cents[] = [];
    intervals: { cents: number, match: Interval}[] = [];
    scales: Scale[] = [];

    constructor(id: string, name: string, path: string) {
        this.id = id;
        this.name = name;
        this.path = path;
    }

    /**
     * Get a list of cents values for stored intervals.
     * 
     * @returns number[]
     */
    getCentsValues() {
        return this.intervals?.map((c) => c.cents)
    }

    /**
     * Get a list of interval objects selected for this melody.
     * 
     * @returns Interval[]
     */
    getSelectedIntervals() {
        return this.intervals.map((i) => i.match)
    }
}