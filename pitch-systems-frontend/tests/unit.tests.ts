import Melody from "$lib/Melody";
import * as data from "./test-data";
import { expect, test } from 'vitest'

const melody = data.melody;

const expected_match = {
    "id": 6,
    "name": "12-ET Major Second",
    "description": null,
    "cents": 200,
    "ratio": null,
    "additional_names": []
};

const cents_match = {
    "cents": 200,
    "f1": 100,
    "f2": 100
}

const new_interval = {
    "id": 7,
    "name": "Alternative",
    "description": null,
    "cents": 201,
    "ratio": null,
    "additional_names": []
}
//@ts-ignore undefined response
test("Test Melody.getCentsMatch()", expect(melody.getCentsMatch(200)).toEqual(expected_match)); 

//Update an interval
const old = data.intervals;

test("Test Melody.setInterval", expect(melody.setInterval(200, new_interval).t)


