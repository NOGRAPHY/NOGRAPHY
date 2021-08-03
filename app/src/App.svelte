<script>
	let secret =
		"Aragorn broke two of his toes while kicking an Uruk Hai helmet";
	let placeholder =
		"In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, nor yet a dry, bare, sandy hole with nothing in it to sit down on or to eat: it was a hobbit-hole, and that means comfort. It had a perfectly round door like a porthole, painted green, with a shiny yellow brass knob in the exact middle. The door opened on to a tube-shaped hall like a tunnel: a very comfortable tunnel without smoke, with panelled walls, and floors tiled and carpeted, provided with polished chairs, and lots and lots of pegs for hats and coats - the hobbit was fond of visitors.";
	let loading = false;
	let exposeResult = "";
	const headers = new Headers();
	headers.append("Content-Type", "application/json");

	fetch(
		"https://vk6c7sl3d6.execute-api.eu-central-1.amazonaws.com/prod/hide",
		{
			method: "POST",
			headers: headers,
			body: '{"wake-up": true}',
			redirect: "follow",
		}
	).catch((error) => console.log("error", error));;

	fetch(
		"https://vk6c7sl3d6.execute-api.eu-central-1.amazonaws.com/prod/expose",
		{
			method: "POST",
			headers: headers,
			body: '{"wake-up": true}',
			redirect: "follow",
		}
	).catch((error) => console.log("error", error));;

	const hide = () => {
		if (!validateInput(secret, placeholder)) {
			return;
		}
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
				var a = document.createElement("a");
				a.href = "data:image/png;base64," + result;
				a.download = "Secret.png";
				a.click();
				loading = false;
			})
			.catch((error) => console.log("error", error));
	};

	const validateInput = (secret, placeholder) => {
		let valid = true;
		if (secret.length == 0) {
			valid = false;
			alert("Provide a secret.");
		}
		if (placeholder.length == 0) {
			valid = false;
			alert("Provide a placeholder.");
		}
		if (!secret.match("^[a-zA-Z ]*$")) {
			valid = false;
			alert("Use only A-Z for your secret.");
		}
		if (!placeholder.match("^[a-zA-Z-()`',.?!;: ]*$")) {
			valid = false;
			alert(
				"Use only letters and punctuation marks for your placeholder."
			);
		}
		if (secret.length * 5 > placeholder.length) {
			valid = false;
			alert("Use a longer placeholder or a shorter secret.");
		}
		return valid;
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
		document.querySelector("input[type=file]").click();
	};

	const expose = (image) => {
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
				console.log("expose result is: ");
				console.log(parsedResult);
			})
			.catch((error) => console.log("error", error));
	};
</script>

<main>
	<h1>nography</h1>
	{#if !loading}
		<br />
		<form>
			<label for="secret">Secret :</label>
			<input type="text" id="secret" bind:value={secret} />
			<label for="placeholder">Placeholder :</label>
			<textarea
				style="height: 20em; width: 30em;"
				name="placeholder"
				id="placeholder"
				maxlength="2000"
				bind:value={placeholder}
			/>
			<br />
			<button type="button" on:click={hide}> Hide </button>
			<button type="button" on:click={exposeButtonPressed}>
				Expose
			</button>
			{#if exposeResult.length > 0}
				<br />
				<p>Exposed secret :</p>
				<h2>{exposeResult}</h2>
			{/if}
			<!--invisible:-->
			<input type="file" id="fileId" on:change={imageUploaded} />
		</form>
	{/if}
	{#if loading}
		<div class="lds-ellipsis">
			<div />
			<div />
			<div />
			<div />
		</div>
	{/if}
</main>
