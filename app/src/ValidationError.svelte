<script>
    export let validationError = "";
</script>

{#if validationError != ""}
    <p class="validationError">
        {validationError}
    </p>
{/if}