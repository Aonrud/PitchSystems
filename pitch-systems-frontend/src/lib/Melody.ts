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
    intervals: Partial<Record<string, Interval|null>> = {};
    scales: Scale[] = [];

    constructor(id: string, name: string, path: string) {
        this.id = id;
        this.name = name;
        this.path = path;
    }

    /**
     * Set the cents values and add corresponding empty interval matches.
     * @param cents
     */
    setCents(cents: Cents[]) {
        //Remove the unison interval
        cents = cents.filter((c) => c.cents !== 0);
        this.cents = cents;
        const intervals: Partial<Record<string, Interval|null>> = {}
        for (const c of cents) {
            if (c.cents !== 0) {
                intervals[c.cents.toString()] = null;
            }
        }
        this.intervals = intervals;
    }

    /**
     * Get the interval set as a match for the given cents value, if it is set.
     * 
     * @param cents 
     * 
     * @returns Interval|null
     */
    getCentsMatch(cents: number): Interval|null {
       if (this.intervals[cents]) {
        return this.intervals[cents.toString()]!
       }
       return null;
    }

    /**
     * Set the interval selected to match the given cents value.
     * 
     * If the interval is already set, it will be replaced.
     * 
     * @param cents 
     * @param interval
     */
    setInterval(cents: number, interval: Interval): void {
        this.intervals[cents] = interval;
    }

    /**
     * Get a list of interval objects selected for this melody.
     * 
     * @returns Interval[]
     */
    getSelectedIntervals(): Array<Interval> {
        const intervals = [];
        for (const c of this.cents) {
            if (this.intervals[c.cents]) {
                intervals.push(this.intervals[c.cents]!)
            }
        }
        return intervals;
    }

    /**
     * Get a list of unique frequency values from the melody.
     * @returns number[]
     */
    getUniqueFrequencies(): number[] {
        return [...new Set(this.frequencies.map((f) => f.frequency))];
    }
}