import type { Frequency, Interval, Scale } from './APITypes';

export default class Melody {
    readonly id: string;
    readonly path: string;

    name: string;
    frequencies?: Frequency[];
    cents?: { value: number, selected: Interval}[]
    intervals?: Interval[];
    scales?: Scale[];

    constructor(id: string, name: string, path: string) {
        this.id = id;
        this.name = name;
        this.path = path;
    }
}