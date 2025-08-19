chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "sendToAgent",
    title: "Send this job to Job Agent",
    contexts: ["page"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "sendToAgent" && tab?.url) {
    fetch("http://localhost:3000/api/scrape", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ url: tab.url })
    });
  }
});
