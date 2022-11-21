class Header extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    this.innerHTML = `
      <header>
        <div class="navbar navbar-expand-sm navbar-dark text-light mb-3">
            <div class="container">
                <a href="/" class="navbar-brand">
                    <img src="../static/img/logo/favicon-transparent.ico" alt="" style="width: 100px;">
                </a>
                <div class="navbar-collapse justify-content-end">
                    <ul class="navbar-nav">
                        <li class="nav-item mx-1">
                            <a href="/" class="nav-link">Home</a>
                        </li>
                        <li class="nav-item mx-1">
                            <a href="/explain" class="nav-link">How it works </a>
                        </li>
                        <li class="nav-item mx-1">
                            <a href="/credits" class="nav-link">Credits</a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </header>
  `;
  }
}

customElements.define("header-component", Header);
