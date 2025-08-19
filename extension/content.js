function isJobPosting(doc = document) {
  const urlOk = /linkedin\.com\/jobs\/|boards\.greenhouse\.io|jobs\.lever\.co|myworkdayjobs\.com/i.test(location.href);
  const blocks = [...doc.querySelectorAll('script[type="application/ld+json"]')];
  const hasSchema = blocks.some(b => {
    try {
      const j = JSON.parse(b.textContent || "{}");
      const type = Array.isArray(j["@type"]) ? j["@type"] : [j["@type"]];
      return type && type.includes && type.includes("JobPosting");
    } catch { return false; }
  });
  return urlOk || hasSchema;
}

function injectButton() {
  if (document.getElementById("__job_agent_btn__")) return; // dedupe

  const host = document.createElement("div");
  host.id = "__job_agent_btn__";
  host.style.all = "initial"; // reduce style interference
  host.style.position = "fixed";
  host.style.right = "16px";
  host.style.bottom = "16px";
  host.style.zIndex = "2147483647"; // top-most

  const shadow = host.attachShadow({ mode: "open" });
  const btn = document.createElement("button");
  btn.textContent = "Send to Job Agent";
  btn.style.cssText = `
    all: initial; font-family: system-ui, sans-serif; font-size: 14px;
    padding: 10px 14px; border-radius: 8px; background:#111; color:#fff; border:none; cursor:pointer;
    box-shadow: 0 2px 10px rgba(0,0,0,.2)
  `;
  btn.onclick = async () => {
    try {
      const res = await fetch("http://localhost:3000/api/scrape", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ url: location.href })
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      btn.textContent = "Sent ✓";
      setTimeout(() => (btn.textContent = "Send to Job Agent"), 1400);
    } catch (e) {
      console.error(e);
      btn.textContent = "Error";
    }
  };
  shadow.appendChild(btn);
  document.body.appendChild(host);
}

function maybeInject() {
  if (isJobPosting()) injectButton();
}

// initial + DOM ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", maybeInject);
} else {
  maybeInject();
}

// watch for SPA navigations (LinkedIn/Workday)
let lastUrl = location.href;
new MutationObserver(() => {
  if (location.href !== lastUrl) {
    lastUrl = location.href;
    // remove any prior button so we can re-add
    const prior = document.getElementById("__job_agent_btn__");
    if (prior) prior.remove();
    maybeInject();
  }
}).observe(document.documentElement, { childList: true, subtree: true });
