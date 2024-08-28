<script lang="ts">
export let freqs: number[];

//Graph scale
//Set inverted so contents will expand (saves checking for first case)
let min = 1000;
let max = 0;

//Scale padding
const p_top = 10;
const p_bottom = 20;

const setMax = (num: number) => {
  max = Math.ceil(num);
};

const setMin = (num: number) => {
  min = Math.floor(num);
};
</script>

<div id="frequencies" class="flex h-60 border-b border-stone-700 bg-white">
  <div
    class="z-50 flex w-3 flex-col justify-between border-l border-stone-700 text-xs text-stone-500"
  >
    <div>{max}</div>
    <div class="-rotate-90">Hertz</div>
    <div>{min}</div>
  </div>
  {#each freqs as freq}
    {#if freq > max - p_top}
      {setMax(freq + p_top)}
    {/if}
    {#if freq < min + p_bottom}
      {setMin(freq -p_bottom)}
    {/if}
    <div class="flex grow flex-col justify-end overflow-hidden">
      <div
        title="{freq.toString()}Hz"
        class="w-full border-t border-stone-700 bg-stone-100"
        style="height: {Math.floor(((freq-min)/(max-min))*100)}%"
      >
        <div class="text-center text-xs text-stone-500">{freq.toFixed(2)}</div>
      </div>
    </div>
  {/each}
</div>
