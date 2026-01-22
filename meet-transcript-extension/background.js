// background.js
console.log("🟢 Agentic Meet background service worker loaded");

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "downloadTranscript") {
    chrome.downloads.download(
      {
        url: message.url,
        filename: message.filename,
        saveAs: false
      },
      (downloadId) => {
        if (chrome.runtime.lastError) {
          sendResponse({
            success: false,
            error: chrome.runtime.lastError.message
          });
        } else {
          sendResponse({
            success: true,
            filename: message.filename,
            downloadId
          });
        }
      }
    );
    return true; // keep channel open
  }
});
