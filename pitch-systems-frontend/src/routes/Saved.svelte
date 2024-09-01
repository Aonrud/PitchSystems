<script lang="ts">
    import { MelodyLocalStorage } from "$lib/MelodyStore";
    import Melody from "$lib/Melody";

    export let melody: Melody;
    export let store: MelodyLocalStorage;

    let list = store.list()

    const loadMelody = (id: string) => {
        melody = store.get(id)!;
    }
</script>

<div id="drawer" class="absolute top-8 left-16">
    {#if list.length > 0}
        <h3 class="text-lg font-bold my-6">Saved Analyses</h3>
        <div class="flex flex-col gap-1">
            {#each list as id}
                <button on:click={() => { loadMelody(id) }}>{store.get(id).name}</button>
            {/each}
        </div>
    {/if}

    <h3 class="text-lg font-bold my-6">Examples</h3>
</div>