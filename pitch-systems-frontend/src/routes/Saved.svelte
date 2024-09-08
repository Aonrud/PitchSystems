<script lang="ts">
    import { MelodyLocalStorage } from "$lib/MelodyLocalStorage";
    import Melody from "$lib/Melody";
    import {examples} from "$lib/examples"
    import { Menu, ArrowBigRightDash, X } from "lucide-svelte";
    import colours from "tailwindcss/colors";

    export let melody: Melody;
    export let saved_list: Melody[];
    export let description: string;

    const loadList = () => {
        console.log("Loading saved list")
        saved_list = MelodyLocalStorage.getAll();
    }

    const loadMelody = (id: string) => {
        const result = MelodyLocalStorage.get(id);
        if (result) {
            melody = result;
            description = "";
        }
        //Close the drawer
        document.getElementById("drawer")?.removeAttribute("open")
    }

    const loadExample = (example: { "description": string, "melody": object}) => {
        description = example.description;
        const obj = example.melody;
        //@ts-ignore The object is manually defined in examples
        const reformat = new Melody(obj.id, obj.name, obj.path);
        for (const [k, v] of Object.entries(obj)) {
            // @ts-ignore 
            if (reformat.hasOwnProperty(k)) reformat[k] = v
        }
        melody = reformat;

        //Close the drawer
        document.getElementById("drawer")?.removeAttribute("open")
    }

    loadList();
</script>

<details id="drawer" class="absolute top-8 left-8 bg-white border open:shadow group">
    <summary class="p-4 cursor-pointer list-none flex justify-start text-stone-800" aria-label="Saved analyses"><Menu color="{colours.stone["600"]}" aria-hidden="true" /><span class="hidden md:inline md:ml-4 flex-grow">Saved Analyses</span><span class="hidden group-open:inline"><X color={colours.stone["400"]} /></span></summary>
    <div class="px-4">
        {#if saved_list.length > 0}
            <nav aria-labelledby="nav-saved">
                <h2 id="nav-saved" class="text-lg font-bold my-6">Saved Analyses</h2>
                <div class="flex flex-col gap-1">
                    {#each saved_list as melody}
                        <button class="text-left hover:bg-stone-50 -mx-4 p-4 group/btn relative" on:click={() => { loadMelody(melody.id) }}>{melody.name} <span class="hidden absolute right-2 top-4 group-hover/btn:block bg-stone-50 px-1" aria-hidden="true"><ArrowBigRightDash color={colours.stone["400"]} /></span></button>
                    {/each}
                </div>
            </nav>
        {/if}
        <nav aria-labelledby="nav-examples">
            <h2 id="nav-examples" class="text-lg font-bold my-6">Examples</h2>
            <div class="flex flex-col gap-1">
                {#each examples as example}
                    <button class="text-left hover:bg-stone-50 -mx-4 p-4 group/btn relative" on:click={() => { loadExample(example) }}>{example.melody.name} <span class="hidden absolute right-2 top-4 group-hover/btn:block bg-stone-50 px-1" aria-hidden="true"><ArrowBigRightDash color={colours.stone["400"]} /></span></button>
                {/each}
            </div>
        </nav>
    </div>
</details>