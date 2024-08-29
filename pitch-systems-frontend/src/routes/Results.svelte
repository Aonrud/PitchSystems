<script lang="ts">
import Frequencies from "./Frequencies.svelte";

import AudioParser from "$lib/AudioParser";
import Melody from "$lib/Melody";
import { MelodyLocalStorage } from "$lib/MelodyStore";
import PSClient from "$lib/PSClient";
import type { AudioAnalysis, Interval, Scale } from "$lib/APITypes";

export let form;
export let melody: Melody;
export let store: MelodyLocalStorage;

//Messages shown to the user
let message: string = "";

//Instantiate each dataset as an unresolved promise.
//Otherwise the initial 'undefined' value means await blocks will trigger immmediately.
let freqs: Promise<AudioAnalysis>,
  cents: Promise<object>,
  intervals: Promise<Interval[]>,
  scales: Promise<Scale[]>;
freqs = new Promise((resolve, reject) => {});
cents = new Promise((resolve, reject) => {});
intervals = new Promise((resolve, reject) => {}); 
scales = new Promise((resolve, reject) => {});

const psclient = new PSClient();

let intervals_shown: Promise<Interval[]>
intervals_shown = new Promise((resolve, reject) => {});

const intervalData = (cents: number) => {
  intervals_shown = psclient.getIntervalsNear(cents);

}

//If form is present, this is a new analysis
if (form) {
  melody = new Melody(form.file.uuid, form.file.name, form.file.path);
  //TMP file for localhost testing
  const test =
    "https://cloud.aonghus.org/s/2L7T75zXagj7KBM/download?path=%2F&files=piano-BbMajor-Scale.wav";

  const parser = new AudioParser(`${test}`);

  freqs = parser.parse();

  freqs
    .then((data) => {
      melody.frequencies = data.freqs;
      cents = psclient.getCents(data.freqs);
      return cents;
    })
    .then((data) => {
      melody.cents = Object.values(data);
      intervals = psclient.getIntervals(Object.values(data));
      return intervals;
    })
    .then((data) => {
      melody.intervals = data;
      scales = psclient.getScales(data);
      return scales;
    })
    .then((data) => {
      melody.scales = data;
      try {
        store.add(melody);
      } catch (e) {
        message =
          "Can't save to local storage. Check that it is enabled in your browser.";
      }
    });
  } else {
    if (melody != undefined) {
      freqs = Promise.resolve({ "freqs": melody.frequencies! })
      cents = Promise.resolve(melody.cents!)
      intervals = Promise.resolve(melody.intervals!)
      scales = Promise.resolve(melody.scales!)
    } else {
      //STUB - no melody loaded
    }

  }
</script>

{#if message.length > 0}
  <div id="message">{message}</div>
{/if}

<h2 class="text-3xl font-semibold text-stone-500">{melody.name}</h2>

<div class="my-4">
  <audio src="/{melody.path}" controls class="mx-auto" />
</div>

{#await freqs}
  <p>Getting frequencies…</p>
{:then result}
  <Frequencies freqs={result.freqs} />
  {#await cents}
    <p>Getting intervals…</p>
  {:then result}
    <div id="intervals" class="bg-white my-4">
      <h3 class="text-lg font-bold">Intervals</h3>
      <p class="my-4">Intervals in cents from the root frequency.</p>
      <div class="my-4">Root: </div>
      <ul class="flex flex-row">
          {#each Object.values(result) as item}
              <li><button class="" on:click={() => intervalData(item)}>{item}</button></li>
          {/each}
      </ul>
    </div>

    <div id="intervals_shown" class="my-4 border-stone-400 border p-4">
      {#await intervals_shown then data}
        <ul class="list-none">
          {#each data as interval}
            <li><span class="cents">{interval.cents}</span>: {interval.name}</li>
          {/each}
        </ul>
      {/await}
    </div>
    {#await scales}
      <p>Getting scales…</p>
    {:then scales}
      <div id="scales">
        <ul>
            {#each scales as scale}
                <li>{scale.name}</li>
            {/each}
        </ul>
    </div>
    {/await}
  {/await}
{/await}