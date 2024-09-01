<script lang="ts">
import Frequencies from "./Frequencies.svelte";
import Melody from "$lib/Melody";
import { MelodyLocalStorage } from "$lib/MelodyStore";
import PSClient from "$lib/PSClient";
import type { Cents, Frequency, Interval, Scale } from "$lib/APITypes";

export let melody: Melody;
export let store: MelodyLocalStorage;

let status_shown: string;

//Instantiate each dataset as an unresolved promise.
//Otherwise the initial 'undefined' value means await blocks will trigger immmediately.
let freqs: Promise<Frequency[]>;
let cents: Promise<Cents[]>;
let intervals: Promise<Interval[]>;
let scales: Promise<Scale[]>;
let intervals_shown: Promise<Interval[]>;

freqs = new Promise((resolve, reject) => {});
cents = new Promise((resolve, reject) => {});
intervals = new Promise((resolve, reject) => {});
scales = new Promise((resolve, reject) => {});
intervals_shown = new Promise((resolve, reject) => {});

let freq_list: Frequency[] = [];
let freqs_unique: number[] = [];

const psclient = new PSClient();

const updateMelody = async () => {
  melody.frequencies = freq_list;
  cents = psclient.getCents(freqs_unique, melody.root);
  const cents_resp = await cents;

  intervals = psclient.getIntervals(cents_resp.map((c) => c.cents));
  const ints_val = await intervals;

  melody.cents = cents_resp;
  for (const interval of ints_val) {
    melody.intervals.push({ cents: interval.cents, match: interval });
  }

  scales = psclient.getScales(melody.getSelectedIntervals());
  const scales_resp = await scales;
  melody.scales = scales_resp;
  melody = melody;
  console.log(melody);
  store.save(melody);
  
};

//If form is present, this is a new analysis
if (melody?.pending) {
  //TMP file for localhost testing
  const test =
    "https://cloud.aonghus.org/s/7CqCj6fZbYPxD4G/download?path=%2F&files=Piano_Gm_tune.wav";

  //Set up the websocket and listener
  const socket = new WebSocket("ws://localhost:5678");
  socket.addEventListener("message", (e: MessageEvent) => {
    const data = JSON.parse(e.data);

    if (data.status == "error") {
      status_shown = data.message;
    }

    if (data.frequency) {
      freq_list.push(data);
      freq_list = freq_list; //Explicitly refresh for Svelte to see the change
    }

    if (data.message == "End of analysis") {
      freqs = Promise.resolve(freq_list);
      freqs_unique = [...new Set(freq_list.map((f) => f.frequency))];
      socket.close();
      updateMelody();
    }
  });

  //Send the url when the socket is ready
  socket.addEventListener("open", () => {
    socket.send(JSON.stringify({ url: test }));
  });
} else if (melody) {
  freqs = Promise.resolve(melody.frequencies); //Data isn't actually used from the promise, only from the list
  cents = Promise.resolve(melody.cents);
  intervals = Promise.resolve(melody.getSelectedIntervals());
  scales = Promise.resolve(melody.scales);
  freq_list = melody.frequencies;
  freqs_unique =  [...new Set(freq_list.map((f) => f.frequency))];
} else {
  //STUB - no analysis to show
}

$: melody
</script>

{#if melody}
<h2 class="text-3xl font-semibold text-stone-500">{melody.name}</h2>

<div class="my-4">
  <audio src="/{melody.path}" controls class="mx-auto" />
</div>

<Frequencies freq_list={freq_list} />

{#await freqs}
  Analysing frequencies…
{:then _}
  {#await cents}
    <p>Getting cent values…</p>
  {:then data}
    <div id="intervals" class="my-4 bg-white">
      <h3 class="text-lg font-bold">Intervals</h3>
      <p class="my-4">Intervals in cents from the root frequency.</p>
      <div class="my-4">
        <label for="">Root Note</label>
        <select
          bind:value={melody.root}
          on:change={() => cents = psclient.getCents(freqs_unique, melody.root)}
        >
          {#each freqs_unique as f}
            <option value={f}>{f.toFixed(2)} Hz</option>
          {/each}
        </select>
      </div>
      <ul class="flex flex-row flex-wrap">
        {#each data as item}
          <li class="m-2 min-w-fit p-2" data-item={JSON.stringify(item)}>
            <button
              class=""
              on:click={() => intervals_shown = psclient.getIntervalsNear(item.cents, 10)}
              >{item.cents}</button
            >
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
{/if}