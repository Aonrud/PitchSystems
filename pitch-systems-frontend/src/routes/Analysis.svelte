<script lang="ts">
import Melody from "$lib/Melody";
import type PSClient from "$lib/PSClient";
import * as utils from "$lib/MelodyUtils";
import type { Cents, Interval } from "$lib/APITypes";
import { SquareChevronDown, SquareChevronUp } from "lucide-svelte";
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
  const match = melody.getCentsMatch(cents.cents)
  if (match) {
    return match.name;
  }
  return "No exact match";
}

/**
 * Apply an interval selection and close the selector.
 * @param e
 * @param interval
 */
const selectionHandler = async (e: Event, interval: Interval) => {
  console.log(`Setting match: ${cents_active.cents} is ${interval.name}`)
  melody = await utils.updateInterval(cents_active.cents, interval, melody, psclient);
  melody = melody;
  melody.cents = melody.cents;
  melody.intervals = melody.intervals;

  interval_list = new Promise((resolve, reject) => {});
  document.body.append(document.getElementById("interval-selection")!); //Put the container back at the end of the document
  if (e.currentTarget instanceof HTMLElement) {
    e.currentTarget.innerText = showMatch(cents_active);
  }
};
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
        <select
          name="root-select"
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
          class="my-4 flex min-w-full bg-white gap-2 px-2"
          data-item={JSON.stringify(item)}
        >
          <div class="w-36 py-4">{formatNumber(item.cents)} cents</div>
          <div class="relative mx-8 flex-grow py-4">
            <button
              title="Select an alternative match"
              class="flex w-full justify-between"
              on:click={(e) => {
                        intervalSelection(e, item);
                    }}
            >
              { showMatch(item) }
              <SquareChevronDown color={colours.stone["400"]} />
            
            </button>
          </div>
          <div class="py-4">
            <button on:click={() => melody = utils.removeCents(item, melody)} title="Remove this interval from the analysis."
              >Remove
            </button>
          </div>
        </li>
      {/each}
    </ul>

    <div class="scales">
      <ul>
        {#each melody.scales as scale}
          <li>{scale.name}</li>
        {/each}
      </ul>
    </div>
  </div>

  <div id="interval-selection" class="absolute top-0 bg-white z-50">
    <ul class="border border-stone-100">
      {#await interval_list then data}
        {#each data as interval}
          <li>
            <button
              class="w-full p-4 flex hover:bg-stone-200"
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
