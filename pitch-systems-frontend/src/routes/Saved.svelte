<script lang="ts">
    import { MelodyLocalStorage } from "$lib/MelodyLocalStorage";
    import Melody from "$lib/Melody";

    export let melody: Melody;
    export let saved_list: Melody[];

    const loadList = () => {
        console.log("Loading saved list")
        saved_list = MelodyLocalStorage.getAll();
    }

    const loadMelody = (id: string) => {
        const result = MelodyLocalStorage.get(id);
        if (result) {
            melody = result;
        }
    }

    loadList();
</script>

<div id="drawer" class="absolute top-8 left-16">
    {#if saved_list.length > 0}
        <h3 class="text-lg font-bold my-6">Saved Analyses</h3>
        <div class="flex flex-col gap-1">
            {#each saved_list as melody}
                <button on:click={() => { loadMelody(melody.id) }}>{melody.name}</button>
            {/each}
        </div>
    {/if}

    <h3 class="text-lg font-bold my-6">Examples</h3>
</div>