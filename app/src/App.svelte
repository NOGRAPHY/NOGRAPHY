<script>
	import Loading from "./Loading.svelte";
	import ValidationError from "./ValidationError.svelte";

	let secret =
		"Aragorn broke two of his toes while kicking an Uruk Hai helmet";
	let placeholder =
		"In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, nor yet a dry, bare, sandy hole with nothing in it to sit down on or to eat: it was a hobbit-hole, and that means comfort. It had a perfectly round door like a porthole, painted green, with a shiny yellow brass knob in the exact middle. The door opened on to a tube-shaped hall like a tunnel: a very comfortable tunnel without smoke, with panelled walls, and floors tiled and carpeted, provided with polished chairs, and lots and lots of pegs for hats and coats - the hobbit was fond of visitors.";
	let loading = false;
	let showHint = true;
	let imageWithSecret = "";
	let exposeResult = "";
	let secretValidationError = "";
	let placeholderValidationError = "";
	const allowedChars = "^[a-zA-Z-()`',.?!;: ]*$";
	const headers = new Headers();
	headers.append("Content-Type", "application/json");

	const wakeUpHide = () => {
		fetch(
			"https://vk6c7sl3d6.execute-api.eu-central-1.amazonaws.com/prod/hide",
			{
				method: "POST",
				headers: headers,
				body: '{"wake-up": true}',
				redirect: "follow",
			}
		).catch((error) => console.log("error", error));
	};

	const wakeUpExpose = () => {
		fetch(
			"https://vk6c7sl3d6.execute-api.eu-central-1.amazonaws.com/prod/expose",
			{
				method: "POST",
				headers: headers,
				body: '{"wake-up": true}',
				redirect: "follow",
			}
		).catch((error) => console.log("error", error));
	};
	wakeUpHide();
	wakeUpExpose();

	const hide = () => {
		loading = true;
		var raw = JSON.stringify({ secret: secret, placeholder: placeholder });
		var requestOptions = {
			method: "POST",
			headers: headers,
			body: raw,
			redirect: "follow",
		};
		fetch(
			"https://vk6c7sl3d6.execute-api.eu-central-1.amazonaws.com/prod/hide",
			requestOptions
		)
			.then((response) => response.text())
			.then((result) => {
				imageWithSecret = "data:image/png;base64," + result;
				loading = false;
			})
			.catch((error) => console.log("error", error));
	};

	const validateSecret = () => {
		if (!secret.match(allowedChars)) {
			secretValidationError =
				"Use only letters and punctuation marks for your secret.";
		} else if (secret.length * 5 > placeholder.length) {
			secretValidationError =
				"Use a shorter secret or a longer placeholder.";
		} else {
			secretValidationError = "";
		}
	};

	const validatePlaceholder = () => {
		if (!placeholder.match(allowedChars)) {
			placeholderValidationError =
				"Use only letters and punctuation marks for your placeholder.";
		} else if (secret.length * 5 > placeholder.length) {
			placeholderValidationError =
				"Use a longer placeholder or a shorter secret.";
		} else {
			placeholderValidationError = "";
		}
	};

	const imageUploaded = () => {
		loading = true;
		let file = document.querySelector("input[type=file]")["files"][0];
		let reader = new FileReader();

		reader.onload = function () {
			let base64String = reader.result
				.replace("data:", "")
				.replace(/^.+,/, "");
			expose(base64String);
		};
		reader.readAsDataURL(file);
	};

	const exposeButtonPressed = () => {
		wakeUpExpose();
		document.querySelector("input[type=file]").click();
	};

	const expose = (image) => {
		imageWithSecret = "";
		var raw = JSON.stringify({ image: image });
		var requestOptions = {
			method: "POST",
			headers: headers,
			body: raw,
			redirect: "follow",
		};
		fetch(
			"https://vk6c7sl3d6.execute-api.eu-central-1.amazonaws.com/prod/expose",
			requestOptions
		)
			.then((response) => response.text())
			.then((result) => {
				let parsedResult = JSON.parse(result);
				exposeResult = parsedResult.exposed_message;
				loading = false;
			})
			.catch((error) => console.log("error", error));
	};

	const resetExposeResult = () => {
		exposeResult = "";
	};

	const resetImageWithSecret = () => {
		imageWithSecret = "";
	};

	const closeHint = () => {
		showHint = false;
	};
</script>

<main>
	<h1>nography</h1>
	<br /><br />

	{#if !loading}
		{#if showHint}
			<div class="hint-box">
				<p>
					With NOGRAPHY you can hide a secret text within a
					placeholder text saved as PNG. You can download and share
					that PNG image, deceiving outsiders with the placeholder
					text. You, or any other insider, can expose the secret
					afterwards with NOGRAPHY by uploading the file. For details
					visit <a
						href="https://github.com/steganographie-HTWG/steganographie"
						target="_blank">our Github repo</a
					>.
				</p>
				<br />
				<button class="btn-secondary btn-hint" on:click={closeHint}
					>Got it!</button
				>
			</div>
			<br />
		{/if}

		{#if imageWithSecret != ""}
			<a href={imageWithSecret} download="secret.png">
				<img
					style="border: 1px solid black;"
					src={imageWithSecret}
					name="helloworld"
					alt="Secret"
				/>
			</a>
			<p style="text-align: center; font-size: large;">
				⬆️ Download and share this image (without compression) ⬆️
			</p>
			<br /><br />
			<button
				class="btn-primary"
				type="button"
				on:click={exposeButtonPressed}
			>
				Upload image to expose secret
			</button>
			<button
				class="btn-secondary"
				type="button"
				on:click={resetImageWithSecret}>Hide another secret</button
			>
		{:else if exposeResult != ""}
			<p>Exposed secret :</p>
			<h2>{exposeResult}</h2>
			<br /><br />

			<button
				class="btn-primary"
				type="button"
				on:click={resetExposeResult}>Hide secret in image</button
			>
			<button
				class="btn-secondary"
				type="button"
				on:click={exposeButtonPressed}
			>
				Expose another secret
			</button>
		{:else}
			<form>
				<label for="secret">Secret :</label>
				<input
					type="text"
					id="secret"
					maxlength="320"
					bind:value={secret}
					on:keyup={validateSecret}
				/>
				<ValidationError validationError={secretValidationError} />
				<label for="placeholder">Placeholder :</label>
				<textarea
					class="placeholder"
					name="placeholder"
					id="placeholder"
					maxlength="1600"
					bind:value={placeholder}
					on:keyup={validatePlaceholder}
				/>
				<ValidationError validationError={placeholderValidationError} />

				<br />
				<button class="btn-primary" type="button" on:click={hide}
					>Hide secret in image</button
				>
				<button
					class="btn-secondary"
					type="button"
					on:click={exposeButtonPressed}
				>
					Expose secret from image
				</button>
			</form>
		{/if}

		<!--invisible:-->
		<input type="file" id="fileId" on:change={imageUploaded} />
	{:else}
		<Loading />
	{/if}
</main>
