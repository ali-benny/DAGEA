class Header extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    this.innerHTML = `
      <header>
        <div class="navbar navbar-expand-sm navbar-dark text-light">
            <div class="container">
                <a href="./index.html" class="navbar-brand">
                    <img src="../static/img/logo/favicon-transparent.ico" alt="" style="width: 100px;">
                </a>
                <div class="navbar-collapse justify-content-end">
                    <ul class="navbar-nav">
                        <li class="nav-item mx-1">
                            <a href="./index.html" class="nav-link">Home</a>
                        </li>
                        <li class="nav-item mx-1">
                            <a href="./howItWorks.html" class="nav-link">How it works </a>
                        </li>
                        <li class="nav-item mx-1">
                            <a href="./credits.html" class="nav-link">Credits</a>
                        </li>
                    </ul>
                    <form class="d-flex ms-2" role="search">
                        <input type="search" class="form-control border-dark" placeholder="SEARCH">
                    </form>
                </div>
            </div>
        </div>
    </header>
  `;
  }
}

customElements.define("header-component", Header);
