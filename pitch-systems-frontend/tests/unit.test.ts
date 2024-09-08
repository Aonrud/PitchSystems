import PSClient from '$lib/PSClient.js';
import { expect, test, vi, beforeEach, expectTypeOf } from 'vitest'
import type { Interval, Scale, } from "$lib/APITypes.js"

/**
 * Unit tests for classes in lib/.
 * NB: Requests involving PSClient require local dev server of the API to be running.
 */


beforeEach(() => {
    vi.resetModules()
  })

//@ts-ignore undefined response
test("Test Melody.getCentsMatch()", async () => {
    const data = await import('./test-data.js')
    const melody = data.melody;
    const expected_match = {
        "id": 597,
        "name": "12-ET Major Second",
        "description": null,
        "cents": 200,
        "ratio": null,
        "additional_names": []
    };

    expect(melody.getCentsMatch(200)).toEqual(expected_match);
})

test("Test Melody.setInterval", async () => {
    const data = await import('./test-data.js')
    const melody = data.melody;
    let intervals_new = data.intervals;
    const new_interval = {
        "id": 7,
        "name": "Alternative",
        "description": null,
        "cents": 201,
        "ratio": null,
        "additional_names": []
    }

    intervals_new["200"] = new_interval
    melody.setInterval(200, new_interval)
    expect(melody.intervals).toEqual(intervals_new)
})

test("Test Melody.setCents", async () => {
    const data = await import('./test-data.js')
    const melody = data.melody;
    const new_cents = [{
        "cents": 200.0000,
        "f1": 233.75544971224912,
        "f2": 262.38162088748976
    },
    {
        "cents": 200.8355,
        "f1": 233.75544971224912,
        "f2": 262.50828432641384
    }
    ]
    const new_cents_intervals = {
        "200": null,
        "200.8355": null
    }

    melody.setCents(new_cents)
    expect(melody.cents).toEqual(new_cents)
    expect(melody.intervals).toEqual(new_cents_intervals)

})

test("Test Melody.getSelectedIntervals", async () => {
    const data = await import('./test-data.js')
    const melody = data.melody;
    const expected_interval_list = [
        {
            "id": 1,
            "name": "Unison",
            "description": null,
            "cents": 0,
            "ratio": "1:1",
            "additional_names": [
                {
                    "id": 7,
                    "name": "Perfect prime",
                    "description": null,
                    "system": null
                }
            ]
        },
        {
            "id": 597,
            "name": "12-ET Major Second",
            "description": null,
            "cents": 200,
            "ratio": null,
            "additional_names": []
        },
        {
            "id": 602,
            "name": "12-ET Fifth",
            "description": null,
            "cents": 700,
            "ratio": null,
            "additional_names": []
        }
    
    ]
    
    expect(melody.getSelectedIntervals()).toEqual(expected_interval_list)
})

test("Test Melody.getUniqueFrequencies", async () => {
    const data = await import('./test-data.js')
    const melody = data.melody;

    const expected =  [ 262.50828432641384, 294.5134116201051, 350.237444562354, 441.27152886549857, 467.51089942449823, 393.12823941810046, 262.38162088748976, 233.75544971224912 ]

    expect(melody.getUniqueFrequencies()).toEqual(expected)
})


test("Test PSClient.getIntervals Matched", async () => {
    const ps = new PSClient();
    const result = await ps.getIntervals([0, 200, 700]);
    expectTypeOf(result).toMatchTypeOf<Interval[]>()
})

