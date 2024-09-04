<script lang="ts">
import { enhance } from "$app/forms";
import Melody from "$lib/Melody";
import PSClient from "$lib/PSClient"
import Saved from "./Saved.svelte";
import { MelodyLocalStorage } from "$lib/MelodyLocalStorage";
import Frequencies from "./Frequencies.svelte";
import Analysis from "./Analysis.svelte";
import { browser } from "$app/environment";
import { PUBLIC_PARSER_SOCKET } from '$env/static/public';
import * as utils from "$lib/MelodyUtils"

export let form;

let melody: Melody;
let psclient = new PSClient();
let saved_list: Melody[] = [];
let messages: string[] = [];

const formSubmit = () => {
  // @ts-ignore Object and Function for the Svelte enhance callback
    return ({ result, update }) => {
        if (result.type === "success") {
            queue_message(`Analysing frequencies in "${result.data.file.name}"`)
            melody = new Melody(result.data.file.uuid, result.data.file.name, result.data.file.path);
            getFrequencies();
        }
        update();
    }
}

const queue_message = (message: string) => {
  messages.push(message);
  messages = messages;
  console.log(`Queued message: ${message}`)
  setTimeout(() => {
    messages.shift();
    messages = messages;
    console.log(`Removed message: ${message}`)
  }, 5000)
}

const getFrequencies = () => {
  const socket = new WebSocket(PUBLIC_PARSER_SOCKET);
  socket.addEventListener("message", (e: MessageEvent) => {
    const data = JSON.parse(e.data);

    if (data.status == "error") {
      queue_message(data.message);
    }

    if (data.frequency) {
      melody.frequencies.push(data);
      melody.frequencies = melody.frequencies; //Explicitly refresh for Svelte to see the change
    }

    if (data.message == "End of analysis") {
      melody.root = melody.frequencies[melody.frequencies.length-1].frequency
      melody.pending = false;
      socket.close();
      utils.getAnalysis(melody, psclient).then((m) => melody = m);
    }
  });

  //Send the url when the socket is ready
  socket.addEventListener("open", () => {
    const url = `${window.location.protocol}//${window.location.host}/${melody.path}`
    socket.send(JSON.stringify({ "url": url }));
  });
}

const save = (melody: Melody) => {
  MelodyLocalStorage.save(melody);
  saved_list = MelodyLocalStorage.getAll();
  queue_message(`Saved "${melody.name}"`);
  console.log(melody);
}

const discard = (id: string) => {
  const name = saved_list.find((m) => m.id == id)?.name;
  MelodyLocalStorage.remove(melody.id);
  saved_list = saved_list.filter((m) => m.id !== melody.id);
  //@ts-ignore Melody will be defined in contexts where needed
  melody = undefined;
  queue_message(`Discarded "${name}"`);
}

</script>

<svelte:head>
  <title>Pitch Systems: Analyse Musical Tunings</title>
</svelte:head>

<form
  method="post"
  action="?/upload"
  use:enhance={formSubmit}
  enctype="multipart/form-data"
  class="m-4 mx-auto max-w-sm bg-white p-4 text-center shadow dark:bg-stone-800"
>
{#if form?.error}<p class="error">Error uploading file.</p>{/if}
  <div> 
    <label class="block" for="file">Upload an audio file</label>
    <input
      class="border-stone- m-4"
      id="file"
      type="file"
      name="audio_file"
      accept=".wav, .mp3, .aac"
      required
    />
  </div>
  <button
    class="
    p-2 rounded-md border
    border-emerald-900 bg-emerald-700 text-emerald-50
    hover:border-emerald-900 hover:bg-emerald-600
    dark:border-emerald-500 dark:bg-emerald-400 dark:text-emerald-900
    dark:hover:border-emerald-500 dark:hover:bg-emerald-200"
    type="submit"
    >Analyze Audio
  </button>   
</form>

{#if melody}
<article>
  <header class="my-4 flex justify-between">
    <h3 class="text-xl font-semibold">{melody.name}</h3>
    <div>
      <button on:click={() => save(melody)} title="Save this analysis to local storage.">Save</button>
      <button on:click={() => discard(melody.id)} title="Remove this analysis from local storage.">Discard</button>
    </div>
  </header>
  <Frequencies list={melody.frequencies} />
  <Analysis bind:melody {psclient} />
</article>
{/if}

{#if browser}
  <Saved bind:melody bind:saved_list />
{/if}

<!--User Messages display-->
<div id="messages" class="absolute top-10 max-w-80">
  {#each messages as message}
    <p class="m-4 p-4 bg-emerald-50 border border-emerald-200">{message}</p>
  {/each}
</div>
