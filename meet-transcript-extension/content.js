// meet-transcript-extension/content.js
console.log("✅ Agentic Meet Streaming Transcript Capture - Fixed 2026");

// Suppress Google's noisy feedback 429 errors in console (dev helper)
const originalConsoleError = console.error;
console.error = function (...args) {
  if (typeof args[0] === 'string' && args[0].includes('feedback-pa.clients6.google.com')) {
    return; // silently ignore
  }
  originalConsoleError.apply(console, args);
};

// ────────────────────────────────────────────────
// CONFIG
// ────────────────────────────────────────────────
const APPEND_API  = "http://localhost:8000/api/transcript/append";
const FINALIZE_API = "http://localhost:8000/api/transcript/finalize";
const SESSION_ID  = new Date().toISOString().replace(/[:.]/g, "-");

// ────────────────────────────────────────────────
// STATE
// ────────────────────────────────────────────────
const seenLines       = new Set();
let meetingFinalized  = false;
let meetingStarted    = false;
let lastCaptionAt     = null;
let hasSentAnyLine    = false;
let lastUrl           = location.href;

// ────────────────────────────────────────────────
// UTILITIES
// ────────────────────────────────────────────────
function nowISO() {
  return new Date().toISOString();
}

function sendAppendLine(speaker, text) {
  hasSentAnyLine = true;
  // Use sendBeacon for better reliability during unload/redirect
  const blob = new Blob([JSON.stringify({
    session_id: SESSION_ID,
    speaker,
    text,
    timestamp: nowISO()
  })], { type: "application/json" });

  if (!navigator.sendBeacon(APPEND_API, blob)) {
    // Fallback if beacon not supported / queue full
    fetch(APPEND_API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      keepalive: true,           // very important for unload
      body: JSON.stringify({
        session_id: SESSION_ID,
        speaker,
        text,
        timestamp: nowISO()
      })
    }).catch(err => console.error("❌ Append failed:", err));
  }
}

// ────────────────────────────────────────────────
// CAPTION EXTRACTION
// ────────────────────────────────────────────────
function extractAndSendCaptions() {
  if (meetingFinalized) return;

  const containerSelectors = [
    'div[role="region"][aria-label="Captions"]',
    'div[jsname="dsyhDe"]',
    'div.vNKgIf.UDinHf',
    '[aria-live="polite"]',
    'div[jsname="tZSHBe"]',
    'div[class*="caption"]'
  ];

  let container = null;
  for (const sel of containerSelectors) {
    container = document.querySelector(sel);
    if (container) {
      console.log(`✅ Captions container: ${sel}`);
      break;
    }
  }

  if (!container) return;

  const captionBlocks = container.querySelectorAll(
    'div.nMcdL, div.adE6rb + div, div.ygicle, .ygicle.VbkSUe, ' +
    'div > div.ygicle, [role="listitem"], div[jsname][data-self-name]'
  );

  captionBlocks.forEach(block => {
    const speakerEl = block.querySelector(
      '.NWpY1d, span[jsname][dir="ltr"]:first-child, ' +
      '[data-self-name], span[aria-hidden="true"] ~ span, ' +
      'span[class*="name"]'
    );
    let speaker = speakerEl?.textContent?.trim() || "Unknown";

    const textEl = block.querySelector(
      '.a4cQT, .ygicle, .ygicle.VbkSUe, ' +
      'div[jsname="tZSHBe"] > div:last-child, ' +
      'div:not([class*="name"]):last-child'
    );
    let text = textEl?.textContent?.trim() || "";

    if (!text && block.textContent) {
      text = block.textContent.trim();
      if (speaker !== "Unknown") {
        text = text.replace(speaker, "").replace(/^[\s:•–-–]+/, "").trim();
      }
    }

    if (!text || text.length < 4) return;

    const isRealSpeech = text.length > 3 && !/^\s*$/.test(text);

    if (!meetingStarted && isRealSpeech) {
      meetingStarted = true;
      console.log("🚀 Meeting started – first real caption");
    }

    if (!meetingStarted) return;

    const dedupeKey = `${speaker}:${text}`;
    if (seenLines.has(dedupeKey)) return;
    seenLines.add(dedupeKey);

    console.log("📝 Streaming:", speaker, "→", text);
    lastCaptionAt = Date.now();
    sendAppendLine(speaker, text);
  });
}

// ────────────────────────────────────────────────
// MEETING END DETECTION – no :contains anywhere
// ────────────────────────────────────────────────
function isMeetingEnded() {
  if (!meetingStarted) return false;

  const now = Date.now();

  const captionsGone = !document.querySelector(
    'div[role="region"][aria-label="Captions"], div[jsname="dsyhDe"], ' +
    '[aria-live="polite"], div[jsname="tZSHBe"], .a4cQT'
  );

  const bodyText = document.body.innerText.toLowerCase();

  const rejoinButton = document.querySelector(
    'button[aria-label*="Rejoin" i], ' +
    'button[jsname][aria-label*="Rejoin" i], ' +
    'button[aria-label*="return to home" i], ' +
    'button[aria-label*="Return to home" i], ' +
    'button[aria-label*="home screen" i]'
  );

  const postMeetingPhrases = [
    "you've left the meeting",
    "you left the meeting",
    "meeting has ended",
    "returning to home",
    "back to home",
    "rejoin"
  ];

  const hasPostMeetingText = postMeetingPhrases.some(p => bodyText.includes(p));

  const postMeetingIndicators =
    hasPostMeetingText ||
    !!rejoinButton ||
    !!document.querySelector('div[role="alertdialog"], div[jsname="srlkmc"]');

  const lobbyIndicators =
    bodyText.includes("ready to join") ||
    bodyText.includes("join now") ||
    !!document.querySelector('button[aria-label*="Join now" i]');

  const leftOrRedirect =
    !location.href.includes("meet.google.com") ||
    bodyText.includes("you left the meeting");

  const noRecentActivity = lastCaptionAt && (now - lastCaptionAt > 60000);

  const shouldEnd =
    leftOrRedirect ||
    (captionsGone && noRecentActivity && postMeetingIndicators) ||
    (captionsGone && noRecentActivity && !lobbyIndicators);

  if (shouldEnd) {
    console.log("🏁 End conditions met:", {
      captionsGone,
      postMeetingIndicators,
      hasPostMeetingText,
      rejoinButton: !!rejoinButton,
      noRecentActivity,
      leftOrRedirect
    });
  }

  return shouldEnd;
}

// ────────────────────────────────────────────────
// FINALIZATION
// ────────────────────────────────────────────────
function finalizeMeeting() {
  if (meetingFinalized) return;

  if (!hasSentAnyLine || !meetingStarted) {
    console.warn("Finalize skipped: no transcript data");
    return;
  }

  meetingFinalized = true;
  console.log("🏁 Finalizing session:", SESSION_ID);

  const blob = new Blob([JSON.stringify({
    session_id: SESSION_ID,
    ended_at: nowISO()
  })], { type: "application/json" });

  if (!navigator.sendBeacon(FINALIZE_API, blob)) {
    fetch(FINALIZE_API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      keepalive: true,
      body: JSON.stringify({
        session_id: SESSION_ID,
        ended_at: nowISO()
      })
    }).catch(err => console.error("❌ Finalize failed:", err));
  }
}

// ────────────────────────────────────────────────
// URL CHANGE WATCH
// ────────────────────────────────────────────────
setInterval(() => {
  if (location.href !== lastUrl) {
    lastUrl = location.href;
    if (!location.href.includes("meet.google.com")) {
      console.log("🔗 URL changed → likely left meeting");
      finalizeMeeting();
    }
  }
}, 3000);

// ────────────────────────────────────────────────
// OBSERVER + POLLING
// ────────────────────────────────────────────────
const observer = new MutationObserver(() => {
  extractAndSendCaptions();
  if (isMeetingEnded()) finalizeMeeting();
});

observer.observe(document.body, {
  childList: true,
  subtree: true,
  characterData: true
});

setInterval(extractAndSendCaptions, 1800);   // slightly faster
setInterval(() => {
  if (isMeetingEnded()) finalizeMeeting();
}, 6000);

// ────────────────────────────────────────────────
// UNLOAD SAFETY – already using beacon
// ────────────────────────────────────────────────
window.addEventListener("beforeunload", () => {
  if (meetingFinalized || !meetingStarted) return;
  console.warn("Page unload → sending beacon finalize");
  finalizeMeeting();  // call it directly here too
});