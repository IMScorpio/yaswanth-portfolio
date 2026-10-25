(() => {
  const nodes = [...document.querySelectorAll("#viewCount")];
  if (!nodes.length || typeof fetch !== "function") return;
  fetch("/.netlify/functions/views", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: "{}",
    cache: "no-store",
    credentials: "omit",
    referrerPolicy: "no-referrer"
  })
    .then((response) => {
      if (!response.ok) throw new Error("Visit count unavailable");
      return response.json();
    })
    .then((data) => {
      const total = Number(data.total);
      if (!Number.isFinite(total)) throw new Error("Invalid visit count");
      nodes.forEach((node) => { node.textContent = total.toLocaleString(); });
      document.querySelectorAll("#counterNote").forEach((node) => {
        node.textContent = "Anonymous aggregate count; details in the privacy notice.";
      });
    })
    .catch(() => {
      nodes.forEach((node) => { node.textContent = "—"; });
      document.querySelectorAll("#counterNote").forEach((node) => { node.textContent = ""; });
    });
})();
