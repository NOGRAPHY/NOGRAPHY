<script>
	let secret = "LOTR is better than GOT";
	let placeholder =
		"In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, nor yet a dry, bare, sandy hole with nothing in it to sit down on or to eat: it was a hobbit-hole, and that means comfort.";
	let loading = false;
	let exposeResult = "";

	const hide = () => {
		loading = true;
		var myHeaders = new Headers();
		myHeaders.append("Content-Type", "application/json");
		var raw = JSON.stringify({ secret: secret, placeholder: placeholder });
		var requestOptions = {
			method: "POST",
			headers: myHeaders,
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
		var myHeaders = new Headers();
		myHeaders.append("Content-Type", "application/json");
		var raw = JSON.stringify({ image: image });
		var requestOptions = {
			method: "POST",
			headers: myHeaders,
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
				bind:value={placeholder}
			/>
			<br />
			<button type="button" on:click={hide}> Hide </button>
			<button type="button" on:click={exposeButtonPressed}>
				Expose
			</button>
			{#if exposeResult.length > 0}
				<br>
				<label>Exposed secret :</label>
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
