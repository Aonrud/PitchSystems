export const examples = [
    { "description": "This piano tune is identified as using a minor scale. Note that because no note on the sixth degree is played,it is ambiguous as to whether it employs a harmonic or melodic minor scale. Both are matched by the intervals detected. Note also that erroneous intervals are present but excluded from scale matches unless a match is selected.",
        "melody": {
            "id": "5d2fa746-cbd7-4f8e-b068-717b7e5a23fb",
            "path": "examples/piano.wav",
            "pending": false,
            "name": "Short Piano Tune",
            "frequencies": [
              {
                "start": 103,
                "slices": 9,
                "frequency": 294.5134116201051
              },
              {
                "slices": 30,
                "start": 126,
                "frequency": 233.75544971224912
              },
              {
                "slices": 14,
                "start": 183,
                "frequency": 233.75544971224912
              },
              {
                "slices": 10,
                "start": 203,
                "frequency": 233.75544971224912
              },
              {
                "slices": 14,
                "start": 231,
                "frequency": 233.5631165235804
              },
              {
                "slices": 15,
                "start": 264,
                "frequency": 220.72097309813725
              },
              {
                "start": 309,
                "slices": 10,
                "frequency": 233.75544971224912
              },
              {
                "start": 323,
                "slices": 8,
                "frequency": 233.75544971224912
              },
              {
                "start": 364,
                "slices": 13,
                "frequency": 220.63576443274928
              },
              {
                "slices": 16,
                "start": 465,
                "frequency": 184.86395796884062
              },
              {
                "slices": 14,
                "start": 562,
                "frequency": 196.56411970905023
              },
              {
                "slices": 8,
                "start": 649,
                "frequency": 195.43199368684918
              },
              {
                "slices": 13,
                "start": 664,
                "frequency": 195.43199368684918
              },
              {
                "slices": 10,
                "start": 695,
                "frequency": 195.43199368684918
              },
              {
                "slices": 11,
                "start": 722,
                "frequency": 195.43199368684918
              }
            ],
            "root": 196.56411970905023,
            "cents": [
              {
                "cents": -106.2432,
                "f1": 196.5641,
                "f2": 184.864
              },
              {
                "cents": -10,
                "f1": 196.5641,
                "f2": 195.432
              },
              {
                "cents": 0,
                "f1": 196.5641,
                "f2": 196.5641
              },
              {
                "cents": 200,
                "f1": 196.5641,
                "f2": 220.6358
              },
              {
                "cents": 200.6685,
                "f1": 196.5641,
                "f2": 220.721
              },
              {
                "cents": 298.575,
                "f1": 196.5641,
                "f2": 233.5631
              },
              {
                "cents": 300,
                "f1": 196.5641,
                "f2": 233.7554
              },
              {
                "cents": 700,
                "f1": 196.5641,
                "f2": 294.5134
              }
            ],
            "intervals": {
              "0": {
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
              "200": {
                "id": 597,
                "name": "12-ET Major Second",
                "description": null,
                "cents": 200,
                "ratio": null,
                "additional_names": []
              },
              "300": {
                "id": 598,
                "name": "12-ET Minor Third",
                "description": null,
                "cents": 300,
                "ratio": null,
                "additional_names": [
                  {
                    "id": 1,
                    "name": "12-ET Augmented Second",
                    "description": null,
                    "system": "12 Tone Equal Temperament"
                  }
                ]
              },
              "700": {
                "id": 602,
                "name": "12-ET Fifth",
                "description": null,
                "cents": 700,
                "ratio": null,
                "additional_names": []
              },
              "-106.2432": {
                "id": 606,
                "name": "12-ET Major Seventh",
                "description": null,
                "cents": 1100,
                "ratio": null,
                "additional_names": []
              }
            },
            "scales": [
              {
                "id": 73,
                "name": "12-ET Harmonic Minor Scale",
                "description": "",
                "system": {
                  "id": 1,
                  "name": "12 Tone Equal Temperament",
                  "description": "The standard contemporary tuning system in Western music. Divides an octave into twelve semitones of equal size."
                },
                "intervals": [
                  {
                    "id": 597,
                    "name": "12-ET Major Second",
                    "description": null,
                    "cents": 200,
                    "ratio": null,
                    "additional_names": []
                  },
                  {
                    "id": 598,
                    "name": "12-ET Minor Third",
                    "description": null,
                    "cents": 300,
                    "ratio": null,
                    "additional_names": [
                      {
                        "id": 1,
                        "name": "12-ET Augmented Second",
                        "description": null,
                        "system": "12 Tone Equal Temperament"
                      }
                    ]
                  },
                  {
                    "id": 600,
                    "name": "12-ET Fourth",
                    "description": null,
                    "cents": 500,
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
                  },
                  {
                    "id": 603,
                    "name": "12-ET Minor Sixth",
                    "description": null,
                    "cents": 800,
                    "ratio": null,
                    "additional_names": [
                      {
                        "id": 4,
                        "name": "12-ET Augmented Fifth",
                        "description": null,
                        "system": "12 Tone Equal Temperament"
                      }
                    ]
                  },
                  {
                    "id": 606,
                    "name": "12-ET Major Seventh",
                    "description": null,
                    "cents": 1100,
                    "ratio": null,
                    "additional_names": []
                  },
                  {
                    "id": 582,
                    "name": "Octave",
                    "description": null,
                    "cents": 1200,
                    "ratio": "2:1",
                    "additional_names": []
                  }
                ]
              },
              {
                "id": 107,
                "name": "12-ET Melodic Minor",
                "description": "The melodic minor scale uses the major form of the 6th and 7th degrees when asccending, and the minor form when descending.",
                "system": {
                  "id": 1,
                  "name": "12 Tone Equal Temperament",
                  "description": "The standard contemporary tuning system in Western music. Divides an octave into twelve semitones of equal size."
                },
                "intervals": [
                  {
                    "id": 597,
                    "name": "12-ET Major Second",
                    "description": null,
                    "cents": 200,
                    "ratio": null,
                    "additional_names": []
                  },
                  {
                    "id": 598,
                    "name": "12-ET Minor Third",
                    "description": null,
                    "cents": 300,
                    "ratio": null,
                    "additional_names": [
                      {
                        "id": 1,
                        "name": "12-ET Augmented Second",
                        "description": null,
                        "system": "12 Tone Equal Temperament"
                      }
                    ]
                  },
                  {
                    "id": 600,
                    "name": "12-ET Fourth",
                    "description": null,
                    "cents": 500,
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
                  },
                  {
                    "id": 603,
                    "name": "12-ET Minor Sixth",
                    "description": null,
                    "cents": 800,
                    "ratio": null,
                    "additional_names": [
                      {
                        "id": 4,
                        "name": "12-ET Augmented Fifth",
                        "description": null,
                        "system": "12 Tone Equal Temperament"
                      }
                    ]
                  },
                  {
                    "id": 604,
                    "name": "12-ET Major Sixth",
                    "description": null,
                    "cents": 900,
                    "ratio": null,
                    "additional_names": [
                      {
                        "id": 6,
                        "name": "12-ET Diminished Seventh",
                        "description": null,
                        "system": "12 Tone Equal Temperament"
                      }
                    ]
                  },
                  {
                    "id": 605,
                    "name": "12-ET Minor Seventh",
                    "description": null,
                    "cents": 1000,
                    "ratio": null,
                    "additional_names": [
                      {
                        "id": 5,
                        "name": "12-ET Augmented Sixth",
                        "description": null,
                        "system": "12 Tone Equal Temperament"
                      }
                    ]
                  },
                  {
                    "id": 606,
                    "name": "12-ET Major Seventh",
                    "description": null,
                    "cents": 1100,
                    "ratio": null,
                    "additional_names": []
                  },
                  {
                    "id": 582,
                    "name": "Octave",
                    "description": null,
                    "cents": 1200,
                    "ratio": "2:1",
                    "additional_names": []
                  }
                ]
              }
            ]
          }
    },
    {
      "description": "This is a traditional tune from Breizh (Brittany). It is played here on an Appalachian Dulcimer. This example illustrates the selection and clean up of detected intervals to identify the scale used in a recording. The saved data excludes erroneously detected intervals, but resetting the information by changing the root frequency shows the initial analysis and additional informational noise.",
    "melody": {
    "id": "8c8e9401-ca26-4cb3-a3ac-09ce2c10d497",
    "path": "examples/blackbird.mp3",
    "pending": false,
    "name": "Blackbird Dulcimer",
    "frequencies": [
      {
        "slices": 11,
        "start": 21,
        "frequency": 294.51341162010516
      },
      {
        "start": 61,
        "slices": 10,
        "frequency": 292.81713918912504
      },
      {
        "slices": 8,
        "start": 112,
        "frequency": 371.0636467765238
      },
      {
        "slices": 8,
        "start": 143,
        "frequency": 368.92647743437567
      },
      {
        "slices": 9,
        "start": 172,
        "frequency": 388.6127764614423
      },
      {
        "start": 241,
        "slices": 17,
        "frequency": 390.8639873736984
      },
      {
        "start": 281,
        "slices": 8,
        "frequency": 390.8639873736984
      },
      {
        "slices": 16,
        "start": 381,
        "frequency": 522.1186296398199
      },
      {
        "start": 441,
        "slices": 11,
        "frequency": 495.3105441509761
      },
      {
        "start": 483,
        "slices": 16,
        "frequency": 438.72999187785035
      },
      {
        "start": 509,
        "slices": 9,
        "frequency": 438.72999187785035
      },
      {
        "slices": 18,
        "start": 582,
        "frequency": 438.7299918778504
      },
      {
        "start": 641,
        "slices": 11,
        "frequency": 441.27152886549857
      },
      {
        "start": 681,
        "slices": 9,
        "frequency": 495.3105441509761
      },
      {
        "slices": 14,
        "start": 741,
        "frequency": 524.7632417749795
      },
      {
        "start": 922,
        "slices": 14,
        "frequency": 589.0268232402102
      },
      {
        "slices": 14,
        "start": 945,
        "frequency": 589.0268232402102
      },
      {
        "start": 981,
        "slices": 8,
        "frequency": 661.1602545233694
      },
      {
        "start": 1041,
        "slices": 16,
        "frequency": 525.9032127252963
      },
      {
        "slices": 8,
        "start": 1115,
        "frequency": 371.0636467765238
      },
      {
        "slices": 9,
        "start": 1164,
        "frequency": 393.38128038732907
      },
      {
        "start": 1181,
        "slices": 14,
        "frequency": 390.8639873736984
      },
      {
        "start": 1246,
        "slices": 8,
        "frequency": 393.12823941810046
      },
      {
        "start": 1261,
        "slices": 12,
        "frequency": 390.8639873736984
      },
      {
        "start": 1283,
        "slices": 9,
        "frequency": 390.8639873736984
      },
      {
        "slices": 27,
        "start": 1301,
        "frequency": 392.5412111102924
      },
      {
        "slices": 11,
        "start": 1374,
        "frequency": 438.7299918778504
      },
      {
        "start": 1522,
        "slices": 13,
        "frequency": 393.12823941810046
      },
      {
        "slices": 15,
        "start": 1546,
        "frequency": 371.0636467765238
      },
      {
        "start": 1621,
        "slices": 16,
        "frequency": 441.27152886549857
      },
      {
        "start": 1701,
        "slices": 13,
        "frequency": 393.12823941810046
      },
      {
        "start": 1761,
        "slices": 12,
        "frequency": 393.12823941810046
      },
      {
        "slices": 8,
        "start": 1774,
        "frequency": 390.8639873736984
      },
      {
        "slices": 12,
        "start": 1792,
        "frequency": 390.8639873736984
      },
      {
        "start": 1807,
        "slices": 10,
        "frequency": 393.12823941810046
      },
      {
        "slices": 19,
        "start": 1827,
        "frequency": 392.174870136247
      },
      {
        "slices": 20,
        "start": 1924,
        "frequency": 438.72999187785035
      },
      {
        "slices": 9,
        "start": 1971,
        "frequency": 441.27152886549857
      },
      {
        "start": 2082,
        "slices": 10,
        "frequency": 393.12823941810046
      },
      {
        "start": 2104,
        "slices": 13,
        "frequency": 371.0636467765238
      },
      {
        "start": 2141,
        "slices": 12,
        "frequency": 441.27152886549857
      },
      {
        "slices": 20,
        "start": 2181,
        "frequency": 441.27152886549857
      },
      {
        "slices": 24,
        "start": 2361,
        "frequency": 292.81713918912504
      }
    ],
    "root": 294.51341162010516,
    "cents": [
      {
        "cents": 0,
        "f1": 294.5134,
        "f2": 294.5134
      },
      {
        "cents": 400,
        "f1": 294.5134,
        "f2": 371.0636
      },
      {
        "cents": 500,
        "f1": 294.5134,
        "f2": 393.1282
      },
      {
        "cents": 700,
        "f1": 294.5134,
        "f2": 441.2715
      },
      {
        "cents": 900,
        "f1": 294.5134,
        "f2": 495.3105
      },
      {
        "cents": 1000,
        "f1": 294.5134,
        "f2": 524.7632
      },
      {
        "cents": 1200,
        "f1": 294.5134,
        "f2": 589.0268
      },
      {
        "cents": 1400,
        "f1": 294.5134,
        "f2": 661.1603
      }
    ],
    "intervals": {
      "0": {
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
      "400": {
        "id": 599,
        "name": "12-ET Major Third",
        "description": null,
        "cents": 400,
        "ratio": null,
        "additional_names": []
      },
      "500": {
        "id": 600,
        "name": "12-ET Fourth",
        "description": null,
        "cents": 500,
        "ratio": null,
        "additional_names": []
      },
      "700": {
        "id": 602,
        "name": "12-ET Fifth",
        "description": null,
        "cents": 700,
        "ratio": null,
        "additional_names": []
      },
      "900": {
        "id": 604,
        "name": "12-ET Major Sixth",
        "description": null,
        "cents": 900,
        "ratio": null,
        "additional_names": [
          {
            "id": 6,
            "name": "12-ET Diminished Seventh",
            "description": null,
            "system": "12 Tone Equal Temperament"
          }
        ]
      },
      "1000": {
        "id": 605,
        "name": "12-ET Minor Seventh",
        "description": null,
        "cents": 1000,
        "ratio": null,
        "additional_names": [
          {
            "id": 5,
            "name": "12-ET Augmented Sixth",
            "description": null,
            "system": "12 Tone Equal Temperament"
          }
        ]
      },
      "1200": {
        "id": 582,
        "name": "Octave",
        "description": null,
        "cents": 1200,
        "ratio": "2:1",
        "additional_names": []
      },
      "1400": {
        "id": 597,
        "name": "12-ET Major Second",
        "description": null,
        "cents": 200,
        "ratio": null,
        "additional_names": []
      }
    },
    "scales": [
      {
        "id": 90,
        "name": "12-ET Mixolydian Mode",
        "description": "The diatonic Mixolydian mode.",
        "system": {
          "id": 1,
          "name": "12 Tone Equal Temperament",
          "description": "The standard contemporary tuning system in Western music. Divides an octave into twelve semitones of equal size."
        },
        "intervals": [
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
            "id": 599,
            "name": "12-ET Major Third",
            "description": null,
            "cents": 400,
            "ratio": null,
            "additional_names": []
          },
          {
            "id": 600,
            "name": "12-ET Fourth",
            "description": null,
            "cents": 500,
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
          },
          {
            "id": 604,
            "name": "12-ET Major Sixth",
            "description": null,
            "cents": 900,
            "ratio": null,
            "additional_names": [
              {
                "id": 6,
                "name": "12-ET Diminished Seventh",
                "description": null,
                "system": "12 Tone Equal Temperament"
              }
            ]
          },
          {
            "id": 605,
            "name": "12-ET Minor Seventh",
            "description": null,
            "cents": 1000,
            "ratio": null,
            "additional_names": [
              {
                "id": 5,
                "name": "12-ET Augmented Sixth",
                "description": null,
                "system": "12 Tone Equal Temperament"
              }
            ]
          },
          {
            "id": 582,
            "name": "Octave",
            "description": null,
            "cents": 1200,
            "ratio": "2:1",
            "additional_names": []
          }
        ]
      }
    ]
  }
    }
]
