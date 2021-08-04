<script>
    export let validationError = "";
</script>

{#if validationError != ""}
    <p class="validationError">
        {validationError}
    </p>
{/if}

<style>
    .validationError {
		color: red;
		margin-top: -1rem;
		text-align: center;
	}
</style>