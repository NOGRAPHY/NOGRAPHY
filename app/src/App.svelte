<script>
	import Loading from "./Loading.svelte";
	import ValidationError from "./ValidationError.svelte";

	let secret =
		"Aragorn broke two of his toes while kicking an Uruk Hai helmet";
	let dummy =
		"In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, nor yet a dry, bare, sandy hole with nothing in it to sit down on or to eat: it was a hobbit-hole, and that means comfort. It had a perfectly round door like a porthole, painted green, with a shiny yellow brass knob in the exact middle. The door opened on to a tube-shaped hall like a tunnel: a very comfortable tunnel without smoke, with panelled walls, and floors tiled and carpeted, provided with polished chairs, and lots and lots of pegs for hats and coats - the hobbit was fond of visitors.";
	let loading = false;
	let showHint = true;
	let imageWithSecret = "";
	let exposeResult = "";
	let secretValidationError = "";
	let dummyValidationError = "";
	const allowedChars = "^[a-zA-Z-()`',.*+/?!$#%&;:@<>=_|{}~  \r\n\t]*$";
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
		var raw = JSON.stringify({ secret: secret, dummy: dummy });
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
			.then((response) => response.json())
			.then((result) => {
				if (result.error) {
					alert(result.error);
				} else {
					imageWithSecret = "data:image/png;base64," + result.image;
				}
				loading = false;
			})
			.catch((error) => {
				alert("Something went wrong!\n" + error);
				loading = false;
			});
	};

	const validateSecret = () => {
		if (!secret.match(allowedChars)) {
			secretValidationError =
				"Use only letters and punctuation marks for your secret.";
		} else if (secret.length * 5 > dummy.length) {
			secretValidationError = "Use a shorter secret or a longer dummy.";
		} else {
			secretValidationError = "";
		}
	};

	const validateDummy = () => {
		if (!dummy.match(allowedChars)) {
			dummyValidationError =
				"Use only letters and punctuation marks for your dummy.";
		} else if (secret.length * 5 > dummy.length) {
			dummyValidationError = "Use a longer dummy or a shorter secret.";
		} else {
			dummyValidationError = "";
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
			.then((response) => response.json())
			.then((result) => {
				if (result.error) {
					alert(result.error);
				} else {
					exposeResult = result.exposed_message;
				}
				loading = false;
			})
			.catch((error) => {
				alert("Something went wrong!\n" + error);
				loading = false;
			});
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
					With NOGRAPHY you can hide a secret text within a dummy text
					saved as PNG. You can download and share that PNG image,
					deceiving outsiders with the dummy text. You, or any other
					insider, can expose the secret afterwards with NOGRAPHY by
					uploading the file. For details visit <a
						href="https://github.com/NOGRAPHY/NOGRAPHY"
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
				<label for="dummy">Dummy :</label>
				<textarea
					class="dummy"
					name="dummy"
					id="dummy"
					maxlength="1600"
					bind:value={dummy}
					on:keyup={validateDummy}
				/>
				<ValidationError validationError={dummyValidationError} />

				<br />
				<button
					disabled={dummyValidationError != "" ||
						secretValidationError != ""}
					class="btn-primary"
					type="button"
					on:click={hide}>Hide secret in image</button
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
