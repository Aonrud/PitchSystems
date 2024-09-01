<script lang="ts">
import UploadForm from "./UploadForm.svelte";
import Results from "./Results.svelte";
import Melody from "$lib/Melody";
import Saved from "./Saved.svelte";
import { MelodyLocalStorage } from "$lib/MelodyStore";

export let form;
let melody: Melody; 
let store = new MelodyLocalStorage();

if (form?.success) {
  melody = new Melody(form.file.uuid, form.file.name, form.file.path);
}

$: melody, store
</script>

<svelte:head>
  <title>Pitch Systems: Analyse Musical Tunings</title>
</svelte:head>

<UploadForm form={form} />
<Results bind:melody bind:store />
<Saved bind:melody bind:store />
