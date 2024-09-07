//STUBS

export type Frequency = {
    slices: number,
    start: number,
    frequency: number
}

export type Cents = {
    cents: number,
    f1: number,
    f2: number
}

export type Interval = {
    id: number,
    name: string,
    cents: number,
    ratio: string|null,
    description: string|null,
    additional_names?: string[]
}

export type Scale = {
    id: number,
    name: string,
    description: string|null,
    intervals: Interval[],
    system: BaseApiItem
}

export type BaseApiItem = {
    id: number,
    name: string,
    description: string
}