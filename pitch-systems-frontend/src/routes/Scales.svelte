<script lang="ts">
    export let scales;
</script>

<div id="scales">
    <ul>
        {#each scales as scale}
            <li>{scale.name}</li>
        {/each}
    </ul>
</div>