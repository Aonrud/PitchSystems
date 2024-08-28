<script lang="ts">
    export let intervals;

</script>

<div id="intervals">
    <ul>
        {#each intervals as item}
            <li data-intervals="{JSON.stringify(item.intervals)}">{item.cents}</li>
        {/each}
    </ul>
</div>