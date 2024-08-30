<script lang="ts">
import Frequencies from "./Frequencies.svelte";

import AudioParser from "$lib/AudioParser";
import Melody from "$lib/Melody";
import { MelodyLocalStorage } from "$lib/MelodyStore";
import PSClient from "$lib/PSClient";
import type { Frequency, Interval, Scale } from "$lib/APITypes";

export let form;
export let melody: Melody;
export let store: MelodyLocalStorage;

//Messages shown to the user
let message: string = "";

//Instantiate each dataset as an unresolved promise.
//Otherwise the initial 'undefined' value means await blocks will trigger immmediately.
let freqs: Promise<Frequency[]>,
  cents: Promise<object>,
  intervals: Promise<Interval[]>,
  scales: Promise<Scale[]>;
freqs = new Promise((resolve, reject) => {});
cents = new Promise((resolve, reject) => {});
intervals = new Promise((resolve, reject) => {});
scales = new Promise((resolve, reject) => {});

let freq_list: Frequency[] = [];

const psclient = new PSClient();

let intervals_shown: Promise<Interval[]>;
intervals_shown = new Promise((resolve, reject) => {});

const intervalData = (cents: number) => {

  //If the interval is negative, get the octave equivalent
  if (cents < 0) {
    console.log(`cents was: ${cents}`)
    cents = +cents + +1200
    console.log(`Now: ${cents}`);
  }
  intervals_shown = psclient.getIntervalsNear(cents, 10);
};

const socketMessageListener = (e) => {
  const data = JSON.parse(e.data);
  
  if (data.status == "error") {
    message = data.message;
    return
  }


  if (data.frequency) {
    freq_list.push(data);
    freq_list = freq_list;
  }
}

const endOfAnalysis = () => {
  freqs = Promise.resolve(freq_list);
  cents = psclient.getCents(freq_list.map((f) => f.frequency));
}

//If form is present, this is a new analysis
if (form) {
  melody = new Melody(form.file.uuid, form.file.name, form.file.path);
  //TMP file for localhost testing
  const test =
    "https://cloud.aonghus.org/s/7CqCj6fZbYPxD4G/download?path=%2F&files=Piano_Gm_tune.wav";

  const socket = new WebSocket("ws://localhost:5678");
  socket.addEventListener("open", () => {
    console.log("Parser socket open");
    socket.send(JSON.stringify({ "url": test, "settings": { "cents_tolerance": 12, "duration_tolerance": 1 } }));
  });

  socket.addEventListener("message", socketMessageListener);

  //Listen for end of analysis message.
  //At end, resolve the frequency promise, convert to cents with psclient, and close the websocket.
  socket.addEventListener("message", (e) => {
    const data = JSON.parse(e.data);
    if (data.message == "End of analysis") {
      freqs = Promise.resolve(freq_list);
      cents = psclient.getCents(freq_list.map((f) => f.frequency));
      socket.close();
    }
  })

  form = null
} else if (melody) {
    freqs = Promise.resolve(melody.frequencies!);
    cents = Promise.resolve(melody.cents!);
    intervals = Promise.resolve(melody.intervals!);
    scales = Promise.resolve(melody.scales!);
} else {
  //STUB - no analysis to show
}
</script>

{#if message.length > 0}
  <div id="message">{message}</div>
{/if}

<h2 class="text-3xl font-semibold text-stone-500">{melody.name}</h2>

<div class="my-4">
  <audio src="/{melody.path}" controls class="mx-auto" />
</div>

<Frequencies {freq_list} />

{#await freqs}
Analysing frequencies…
{:then _}
  {#await cents}
  <p>Getting cent values…</p>
  {:then data}
    <div id="intervals" class="my-4 bg-white">
      <h3 class="text-lg font-bold">Intervals</h3>
      <p class="my-4">Intervals in cents from the root frequency.</p>
      <div class="my-4">Root:</div>
      <ul class="flex flex-row flex-wrap">
        {#each Object.values(data) as item}
          <li class="min-w-fit p-2 m-2">
            <button class="" on:click={() => intervalData(item)}>{item}</button>
          </li>
        {/each}
      </ul>
    </div>

    <div id="intervals_shown" class="my-4 border border-stone-400 p-4">
      {#await intervals_shown then data}
        <ul class="list-none">
          {#each data as interval}
            <li>
              <span class="cents">{interval.cents}</span>: {interval.name}
            </li>
          {/each}
        </ul>
      {/await}
    </div>
  {/await}
{/await}