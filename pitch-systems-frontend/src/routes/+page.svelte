<script lang="ts">
import UploadForm from "./UploadForm.svelte";
import Results from "./Results.svelte";
import type Melody from "$lib/Melody";
import Saved from "./Saved.svelte";
import { MelodyLocalStorage } from "$lib/MelodyStore";

export let form;
let melody: Melody;
let store = new MelodyLocalStorage();
</script>

<svelte:head>
  <title>Pitch Systems: Analyse Musical Tunings</title>
</svelte:head>

<UploadForm form={form} />

{#if form || melody}
  <Results form={form} bind:melody bind:store />
{/if}

<Saved bind:melody={melody} bind:store />
