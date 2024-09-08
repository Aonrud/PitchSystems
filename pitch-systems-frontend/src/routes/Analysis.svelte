<script lang="ts">
import Melody from "$lib/Melody";
import type PSClient from "$lib/PSClient";
import * as utils from "$lib/MelodyUtils";
import type { Cents, Interval } from "$lib/APITypes";
import { SquareChevronDown, SquareChevronUp, ChevronDown } from "lucide-svelte";
import colours from "tailwindcss/colors";

export let melody: Melody;
export let psclient: PSClient;
let interval_list: Promise<Interval[]> = new Promise((resolve, reject) => {}); //Set to a dummy promise to prevent immediate resolution
let cents_active: Cents;

/**
 * Parse a fixed digit number for display so that trailing 0s are dropped.
 * @param num
 * @param max_dec
 * @return number
 */
const formatNumber = (num: number, max_dec: number = 4) => {
  return parseFloat(num.toFixed(max_dec));
};

/**
 * Open the interval selector and show alternative matches.
 * @param e
 * @param cents
 */
const intervalSelection = (e: Event, cents: Cents) => {
  cents_active = cents;
  interval_list = psclient.getIntervalsNear(cents.cents, 10);

  const display = document.getElementById("interval-selection");
  if (e.currentTarget instanceof Element) {
    e.currentTarget.parentElement?.appendChild(display!);
  }
};

const showMatch = (cents: Cents): string => {  
  const match = melody.getCentsMatch(cents.cents);

  if (match) {
    return `<span>${match.name} <span class="text-stone-500 ml-4">${match.cents} cents</span></span>`  
  }
  return `<span class="text-stone-500">No exact match.</span>`
};

/**
 * Apply an interval selection and close the selector.
 * @param e
 * @param interval
 */
const selectionHandler = async (e: Event, interval: Interval) => {
  console.log(`Setting match: ${cents_active.cents} is ${interval.name}`);
  melody = await utils.updateInterval(
    cents_active.cents,
    interval,
    melody,
    psclient,
  );
  melody = melody;
  melody.cents = melody.cents;
  melody.intervals = melody.intervals;

  interval_list = new Promise((resolve, reject) => {});
  document.body.append(document.getElementById("interval-selection")!); //Put the container back at the end of the document
  if (e.currentTarget instanceof HTMLElement) {
    const fragment = showMatch(cents_active);
    console.log(fragment);
    e.currentTarget.append(fragment);
  }
};

const removeHandler = async (item: Cents) => {
  melody = await utils.removeCents(item, melody, psclient)
}
</script>

{#if melody.pending}
  <p>Analysing frequencies…</p>
{:else if melody.cents.length > 0}
  <div id="intervals" class="my-4">
    <h3 class="text-lg font-bold">Intervals</h3>
    <div class="my-4 flex gap-2">
      <p>
        The audio file contains the following intervals in cents from the root
        frequency.
      </p>
      <div>
        <label for="root-select">Selected root:</label>
        <select class="p-2 bg-white border border-stone-200 hover:bg-stone-200 focus:bg-stone-200 cursor-pointer"
          id="root-select"
          bind:value={melody.root}
          on:change={() => {
            //@ts-ignore Root is defined
            utils.updateRoot(melody.root, melody, psclient).then((m) => melody = m)
          }}
        >
          {#each melody.getUniqueFrequencies().sort() as f}
            <option value={f} selected={melody.root == f}
              >{f.toFixed(2)} Hz</option
            >
          {/each}
        </select>
      </div>
    </div>
    <ul class="w-full">
      {#each melody.cents as item}
        <li
          class="my-4 flex min-w-full gap-2 bg-white px-2"
          data-item={JSON.stringify(item)}
        >
          <div class="w-36 py-4">{formatNumber(item.cents)} cents</div>
          <div class="relative mx-8 flex-grow py-4">
            <button
              title="Select an alternative match"
              class="flex w-full justify-between p-4 -m-4 group"
              on:click={(e) => {
                        intervalSelection(e, item);
                    }}
            >
              {@html showMatch(item)}
              <span class="text-stone-400 group-hover:text-stone-700">
              <SquareChevronDown />
            </span>
            </button>
          </div>
          <div class="py-4">
            <button
              on:click={() => removeHandler(item)}
              title="Remove this interval from the analysis."
              class="hover:text-red-900 focus:text-red-900 -m-4 p-4"
              >Remove
            </button>
          </div>
        </li>
      {/each}
    </ul>

    <div class="scales">
      <h3 class="my-4 text-lg font-bold">Scales</h3>
      <p class="my-4">Scales that include the selected intervals.</p>
      {#each melody.scales as scale}
        <details class="my-4 bg-white px-2 py-4 [&_svg]:open:-rotate-180">
          <summary class="flex cursor-pointer list-none gap-2 justify-between group">
            <h4 class="text-lg font-semibold" title="Expand scale details.">
              {scale.name}
            </h4>
            <span class="text-stone-400 group-hover:text-stone-700"><ChevronDown /></span>
          </summary>
          {#if scale.description}
            <p class="my-4">{scale.description}</p>
          {/if}
          <h5 class="my-4 font-semibold">Intervals</h5>
          <ul class="px-4">
            {#each scale.intervals.sort((a, b) => a.cents - b.cents) as interval}
              <li class="my-2">
                {interval.name}
                <span class="ml-3 text-stone-600"
                  >({interval.ratio ? interval.ratio :   interval.cents})</span
                >
              </li>
            {/each}
          </ul>
          {#if scale.system}
            <h5 class="my-4 font-semibold">
              Musical System: {scale.system.name}
            </h5>
            <p class="my-4">{scale.system.description}</p>
          {/if}
        </details>
      {/each}
    </div>
  </div>

  <div id="interval-selection" class="absolute top-0 z-50 bg-white">
    <ul class="border border-stone-100 shadow">
      {#await interval_list then data}
        {#each data as interval}
          <li>
            <button
              class="flex w-full p-4 hover:bg-stone-200"
              on:click={(e) => selectionHandler(e, interval)}
            >
              <span class="flex-grow text-left">{interval.name}</span>
              <em class="text-right">{interval.cents} cents</em>
            </button>
          </li>
        {/each}
      {/await}
    </ul>
  </div>
{/if}
