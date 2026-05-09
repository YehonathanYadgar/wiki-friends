(function () {
  const menuButton = document.querySelector(".menu-button");
  const search = document.querySelector("#search");
  const results = document.querySelector("#searchResults");
  const index = window.SEARCH_INDEX || [];

  if (menuButton) {
    menuButton.addEventListener("click", () => {
      document.body.classList.toggle("nav-open");
    });
  }

  document.addEventListener("click", (event) => {
    if (!event.target.closest(".sidebar") && !event.target.closest(".menu-button")) {
      document.body.classList.remove("nav-open");
    }
  });

  function renderResults(query) {
    const q = query.trim().toLowerCase();
    if (!q) {
      results.hidden = true;
      results.innerHTML = "";
      return;
    }

    const matches = index
      .filter((page) => `${page.title} ${page.section} ${page.summary}`.toLowerCase().includes(q))
      .slice(0, 12);

    if (!matches.length) {
      results.hidden = false;
      results.innerHTML = '<a><strong>No results</strong><span>Try a different word.</span></a>';
      return;
    }

    results.hidden = false;
    results.innerHTML = matches
      .map((page) => `<a href="${page.url}"><strong>${escapeHtml(page.title)}</strong><span>${escapeHtml(page.summary || page.section)}</span></a>`)
      .join("");
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }

  if (search) {
    search.addEventListener("input", () => renderResults(search.value));
    search.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        search.value = "";
        renderResults("");
      }
    });
  }
})();
