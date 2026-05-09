(function () {
  const form = document.getElementById("askForm");
  const input = document.getElementById("askInput");
  const messages = document.getElementById("askMessages");

  if (!form) return;

  function addMessage(role, text) {
    const div = document.createElement("div");
    div.className = "ask-message ask-message--" + role;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
    return div;
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    const q = input.value.trim();
    if (!q) return;

    input.value = "";
    input.disabled = true;
    const btn = form.querySelector("button");
    btn.disabled = true;

    addMessage("user", q);
    const thinking = addMessage("assistant", "thinking…");

    try {
      const res = await fetch("/.netlify/functions/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });
      const data = await res.json();
      thinking.textContent = data.answer || data.error || "Something went wrong.";

      if (data.sources && data.sources.length) {
        const sourcesEl = document.createElement("div");
        sourcesEl.className = "ask-sources";
        data.sources.forEach(function (s) {
          const a = document.createElement("a");
          a.href = s.url;
          a.textContent = s.title;
          sourcesEl.appendChild(a);
        });
        thinking.appendChild(sourcesEl);
      }
    } catch {
      thinking.textContent = "Could not reach the server. Try again.";
    } finally {
      input.disabled = false;
      btn.disabled = false;
      input.focus();
    }
  });
})();
