<script lang="ts">
import type { Frequency } from "$lib/APITypes";

export let list: Frequency[];

//Graph scale
//Set inverted so contents will expand (saves checking for first case)
let min = 200;
let max = 200;

//Scale padding
const p_top = 10;
const p_bottom = 20;

const setMax = (num: number) => {
  max = Math.ceil(num);
};

const setMin = (num: number) => {
  min = Math.floor(num);
};

const getWidth = (freq: Frequency) => {
  const total = list.reduce((sum, frequency) => {
    return { "slices": sum.slices + frequency.slices}
  }, {"slices": 0}).slices;
  return (freq.slices/total) * 100;
}
</script>
<div id="frequencies" class="flex h-60 border-b border-stone-700 bg-white" >
  <div
    class="z-50 flex w-3 flex-col justify-between border-l border-stone-700 text-xs text-stone-500"
  >
    <div>{max}</div>
    <div class="-rotate-90">Hertz</div>
    <div>{min}</div>
  </div>
  {#each list as freq}
    {#if freq.frequency > max - p_top}
      {setMax(freq.frequency + p_top)}
    {/if}
    {#if freq.frequency < min + p_bottom}
      {setMin(freq.frequency -p_bottom)}
    {/if}
    <div class="flex grow flex-col justify-end overflow-hidden" style="width: {getWidth(freq)}%" data-slices="{freq.slices}" data-start="{freq.start}">
      <div
        title="{freq.frequency.toString()}Hz"
        class="w-full border-t border-stone-700 bg-stone-100"
        style="height: {Math.floor(((freq.frequency-min)/(max-min))*100)}%"
      >
        <div class="text-center text-xs text-stone-500">{freq.frequency.toFixed(2)}</div>
      </div>
    </div>
  {/each}
</div>
