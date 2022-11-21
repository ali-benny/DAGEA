class location extends HTMLElement {
	constructor() {
		super();
	}

	connectedCallback() {
		this.innerHTML = `
		<button class="btn btn-secondary bi-map-fill" type="button" data-bs-toggle="collapse" data-bs-target="#locationId"
			aria-expanded="false" aria-controls="locationId">
		</button>
		<div class="collapse text-white" id="locationId">
			<h1>mi vedi?</h1>
		</div>
	`;
	}
}

customElements.define("location-col", location);
