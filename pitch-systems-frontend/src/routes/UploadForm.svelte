<script lang="ts">
  import { enhance } from "$app/forms";
  import Melody from "$lib/Melody";
  export let form;
  export let melody: Melody;

  const formSubmit = () => {
    return ({ result, update }) => {
        if (result.type === "success") {
            melody = new Melody(result.data.file.id, result.data.file.name, result.data.file.path);
        }
        else {
            update();
        }
    }
}

</script>

<form
  method="post"
  action="?/upload"
  use:enhance
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