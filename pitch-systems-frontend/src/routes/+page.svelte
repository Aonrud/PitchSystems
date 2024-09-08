<script lang="ts">
import { enhance } from "$app/forms";
import Melody from "$lib/Melody";
import PSClient from "$lib/PSClient";
import Saved from "./Saved.svelte";
import { MelodyLocalStorage } from "$lib/MelodyLocalStorage";
import Frequencies from "./Frequencies.svelte";
import Analysis from "./Analysis.svelte";
import { browser } from "$app/environment";
import { PUBLIC_PARSER_SOCKET } from "$env/static/public";
import * as utils from "$lib/MelodyUtils";
import { Upload, Save, OctagonX } from "lucide-svelte";
import colours from "tailwindcss/colors";

export let form;

let melody: Melody;
let psclient = new PSClient();
let saved_list: Melody[] = [];
let messages: string[] = [];
let description: string;

const formSubmit = () => {
  // @ts-ignore Object and Function for the Svelte enhance callback
  return ({ result, update }) => {
    if (result.type === "success") {
      queue_message(`Analysing frequencies in "${result.data.file.name}"`);
      melody = new Melody(
        result.data.file.uuid,
        result.data.file.name,
        result.data.file.path,
      );
      getFrequencies();
    }
    update();
  };
};

const queue_message = (message: string) => {
  messages.push(message);
  messages = messages;
  console.log(`Queued message: ${message}`);
  setTimeout(() => {
    messages.shift();
    messages = messages;
    console.log(`Removed message: ${message}`);
  }, 5000);
};

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
      melody.root = melody.frequencies[melody.frequencies.length - 1].frequency;
      melody.pending = false;
      socket.close();
      utils.getAnalysis(melody, psclient).then((m) => (melody = m));
    }
  });

  //Send the url when the socket is ready
  socket.addEventListener("open", () => {
    const url = `${window.location.protocol}//${window.location.host}/${melody.path}`;
    socket.send(JSON.stringify({ url: url }));
  });
};

const save = (melody: Melody) => {
  MelodyLocalStorage.save(melody);
  saved_list = MelodyLocalStorage.getAll();
  queue_message(`Saved "${melody.name}"`);
  console.log(melody);
};

const discard = (id: string) => {
  const name = saved_list.find((m) => m.id == id)?.name;
  MelodyLocalStorage.remove(melody.id);
  saved_list = saved_list.filter((m) => m.id !== melody.id);
  //@ts-ignore Melody will be defined in contexts where needed
  melody = undefined;
  queue_message(`Discarded "${name}"`);
};
</script>

<svelte:head>
  <title>Pitch Systems: Analyse Musical Tunings</title>
</svelte:head>

{#if !melody}
  <div class="mb-4 border border-emerald-100 bg-emerald-50 p-2 text-center">
    <p class="mb-4 text-lg text-emerald-800">
      Analyse the frequencies in a monophonic audio recording and identify the
      intervals and scales it uses.
    </p>
    <p class="mb-4 text-stone-800">
      Upload a file from your device or select an example from the "Saved
      Analyses" menu.
    </p>
  </div>
{/if}

<details id="upload-form" open>
  <summary
    class="flex cursor-pointer list-none justify-center text-lg text-stone-800"
    >Analyse a new audio file <span class="pl-4"
      ><Upload color={colours.stone["600"]} /></span
    ></summary
  >
  <form
    method="post"
    action="?/upload"
    use:enhance={formSubmit}
    enctype="multipart/form-data"
    class="m-4 mx-auto max-w-sm bg-white p-4 text-center shadow"
  >
    {#if form?.error}<p class="error">Error uploading file.</p>{/if}
    <div>
      <label class="block" for="file">Select a file on your device.</label>
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
    rounded-md border border-emerald-900
    bg-emerald-700 p-2 text-emerald-50
    hover:border-emerald-900 hover:bg-emerald-600
    focus:border-emerald-900 focus:bg-emerald-600"
      type="submit"
      >Analyze Audio
    </button>
  </form>
</details>

{#if melody}
  <article>
    <header class="my-4 flex justify-between">
      <h2 class="text-2xl font-bold">{melody.name}</h2>
      <div class="flex gap-2">
        <button
          on:click={() => save(melody)}
          class="flex rounded-md border border-emerald-200 bg-emerald-50 p-2
        hover:bg-emerald-100 focus:bg-emerald-100"
          title="Save this analysis to local storage."
        >
          <Save color={colours.emerald["400"]} />
          <span class="pl-2">Save</span>
        </button>
        <button
          on:click={() => discard(melody.id)}
          class="flex rounded-md border border-red-200 bg-red-50 p-2
        hover:bg-red-100 focus:bg-red-100"
          title="Remove this analysis from local storage."
        >
          <OctagonX color={colours.red["400"]} />
          <span class="pl-2">Discard</span>
        </button>
      </div>
    </header>
    {#if description}
      <h3 class="my-4 text-xl">About This Example</h3>
      <p class="text-lg">{description}</p>
    {/if}
    <div class="my-4 w-full">
      <audio class="mx-auto" src={melody.path} controls>
        <p>
          The audio recording analysed. If playback is unavailable, <a
            href={melody.path}>download here</a
          >.
        </p>
      </audio>
    </div>
    <Frequencies list={melody.frequencies} />
    <Analysis bind:melody={melody} psclient={psclient} />
  </article>
{/if}

{#if browser}
  <Saved
    bind:melody={melody}
    bind:saved_list={saved_list}
    bind:description={description}
  />
{/if}

<!--User Messages display-->
<div id="messages" class="absolute right-10 top-10 max-w-80">
  {#each messages as message}
    <p class="m-4 border border-emerald-200 bg-emerald-50 p-4">{message}</p>
  {/each}
</div>
