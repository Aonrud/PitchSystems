
import Melody from "$lib/Melody"
import Frequencies from "../src/routes/Frequencies.svelte";

//Set up a melody object with sample data
let melody = new Melody("id-1", "Testing melody", "/dev/null");

melody.root = 233.75544971224912;

export const frequencies = [
    {
        "start": 65,
        "slices": 12,
        "frequency": 262.50828432641384
    },
    {
        "slices": 13,
        "start": 81,
        "frequency": 294.5134116201051
    },
    {
        "slices": 9,
        "start": 143,
        "frequency": 350.237444562354
    },
    {
        "slices": 24,
        "start": 186,
        "frequency": 441.27152886549857
    },
    {
        "slices": 20,
        "start": 281,
        "frequency": 467.51089942449823
    },
    {
        "start": 361,
        "slices": 9,
        "frequency": 393.12823941810046
    },
    {
        "start": 384,
        "slices": 13,
        "frequency": 350.237444562354
    },
    {
        "start": 443,
        "slices": 13,
        "frequency": 294.5134116201051
    },
    {
        "slices": 12,
        "start": 481,
        "frequency": 262.38162088748976
    },
    {
        "start": 505,
        "slices": 14,
        "frequency": 233.75544971224912
    },
    {
        "start": 563,
        "slices": 16,
        "frequency": 233.75544971224912
    }
];

melody.frequencies = frequencies;

export const cents = [
    {
        "cents": 0.0000,
        "f1": 233.75544971224912,
        "f2": 233.75544971224912
    },
    {
        "cents": 200.0000,
        "f1": 233.75544971224912,
        "f2": 262.38162088748976
    },
    {
        "cents": 200.8355,
        "f1": 233.75544971224912,
        "f2": 262.50828432641384
    },
    {
        "cents": 400.0000,
        "f1": 233.75544971224912,
        "f2": 294.5134116201051
    },
    {
        "cents": 700.0000,
        "f1": 233.75544971224912,
        "f2": 350.237444562354
    },
    {
        "cents": 900.0000,
        "f1": 233.75544971224912,
        "f2": 393.12823941810046
    },
    {
        "cents": 1100.0000,
        "f1": 233.75544971224912,
        "f2": 441.27152886549857
    },
    {
        "cents": 1200.0000,
        "f1": 233.75544971224912,
        "f2": 467.51089942449823
    }
];
melody.cents = cents;

export const intervals = [
    {
        "cents": 0,
        "match": {
            "id": 1,
            "name": "Unison",
            "description": null,
            "cents": 0,
            "ratio": "1:1",
            "additional_names": []
        }
    },
    {
        "cents": 200,
        "match": {
            "id": 6,
            "name": "12-ET Major Second",
            "description": null,
            "cents": 200,
            "ratio": null,
            "additional_names": []
        }
    },
    {
        "cents": 400,
        "match": {
            "id": 13,
            "name": "12-ET Major Third",
            "description": null,
            "cents": 400,
            "ratio": null,
            "additional_names": []
        }
    },
    {
        "cents": 700,
        "match": {
            "id": 21,
            "name": "12-ET Fifth",
            "description": null,
            "cents": 700,
            "ratio": null,
            "additional_names": []
        }
    },
    {
        "cents": 900,
        "match": {
            "id": 27,
            "name": "12-ET Major Sixth",
            "description": null,
            "cents": 900,
            "ratio": null,
            "additional_names": []
        }
    },
    {
        "cents": 1100,
        "match": {
            "id": 33,
            "name": "12-ET Major Seventh",
            "description": null,
            "cents": 1100,
            "ratio": null,
            "additional_names": []
        }
    },
    {
        "cents": 1200,
        "match": {
            "id": 35,
            "name": "Octave",
            "description": null,
            "cents": 1200,
            "ratio": "2:1",
            "additional_names": []
        }
    },
];
melody.intervals = intervals;

export { melody }
