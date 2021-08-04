<script>
    let showHint = true;
    const closeHint = () => {
		showHint = false;
	}
</script>

{#if showHint}
    <div class="hint-box">
        <p>
            HINT: With NOGRAPHY you can hide a secret text within an image, by
            providing a non-secret placeholder text. You can download and share
            that image, deceiving outsiders with an image with the placeholder
            text. You (or any other insider) can expose the secret using
            NOGRAPHY.
        </p>
        <br />
        <button class="btn-secondary btn-hint" on:click={closeHint}
            >Got it!</button
        >
    </div>
    <br />
{/if}
