// Divyasree 'Whispers of the Wind' — Voice Agent Interactive Controller
document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initSimulator();
  initRecordedFlows();
});

// ================= TAB CONTROLLER =================
function initTabs() {
  const tabs = document.querySelectorAll(".nav-tab");
  const panels = document.querySelectorAll(".tab-panel");

  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      panels.forEach(p => p.classList.remove("active"));

      tab.classList.add("active");
      const targetPanel = document.getElementById(tab.dataset.tab);
      if (targetPanel) {
        targetPanel.classList.add("active");
      }
    });
  });
}

// ================= SIMULATOR CONTROLLER =================
let isCallActive = false;
let callTimer = null;
let callSeconds = 0;
let recognition = null;
let isRecognizing = false;

function initSimulator() {
  const btnStartCall = document.getElementById("btnStartCall");
  const btnEndCall = document.getElementById("btnEndCall");
  const btnMicToggle = document.getElementById("btnMicToggle");
  const btnSendText = document.getElementById("btnSendText");
  const userTextInput = document.getElementById("userTextInput");
  const btnResetSession = document.getElementById("btnResetSession");
  const quickChips = document.querySelectorAll(".quick-chip");

  // Speech Recognition Setup (Web Speech API)
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-IN";

    recognition.onstart = () => {
      isRecognizing = true;
      btnMicToggle.classList.add("listening");
      setWaveformState("listening", "Listening to user microphone...");
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      if (transcript.trim()) {
        sendUserMessage(transcript.trim());
      }
    };

    recognition.onerror = (e) => {
      console.warn("Speech recognition error:", e);
      btnMicToggle.classList.remove("listening");
      isRecognizing = false;
      setWaveformState("standby", "Aarav (Divyasree AI Consultant) • Connected");
    };

    recognition.onend = () => {
      btnMicToggle.classList.remove("listening");
      isRecognizing = false;
      if (isCallActive) {
        setWaveformState("standby", "Aarav (Divyasree AI Consultant) • Connected");
      }
    };
  } else {
    btnMicToggle.title = "Web Speech API not supported in this browser. Please use text input.";
  }

  // Start Call
  btnStartCall.addEventListener("click", () => {
    startOutboundCall();
  });

  // End Call
  btnEndCall.addEventListener("click", () => {
    endOutboundCall();
  });

  // Reset Session
  btnResetSession.addEventListener("click", () => {
    resetSession();
  });

  // Mic Toggle
  btnMicToggle.addEventListener("click", () => {
    if (!recognition) {
      alert("Speech recognition is not supported in this browser. You can type in the text box.");
      return;
    }
    if (isRecognizing) {
      recognition.stop();
    } else {
      try {
        recognition.start();
      } catch (err) {
        console.error("Mic start failed", err);
      }
    }
  });

  // Send Text Button
  btnSendText.addEventListener("click", () => {
    submitTextInput();
  });

  // Enter Key on input
  userTextInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      submitTextInput();
    }
  });

  // Quick Chips
  quickChips.forEach(chip => {
    chip.addEventListener("click", () => {
      if (!isCallActive) {
        startOutboundCall(() => {
          setTimeout(() => {
            sendUserMessage(chip.dataset.text);
          }, 1200);
        });
      } else {
        sendUserMessage(chip.dataset.text);
      }
    });
  });
}

function submitTextInput() {
  const input = document.getElementById("userTextInput");
  const text = input.value.trim();
  if (text) {
    sendUserMessage(text);
    input.value = "";
  }
}

function startOutboundCall(onConnected) {
  if (isCallActive) return;

  const statusIndicator = document.getElementById("callStatusIndicator");
  const statusText = document.getElementById("callStatusText");
  const btnStartCall = document.getElementById("btnStartCall");
  const btnEndCall = document.getElementById("btnEndCall");
  const btnMicToggle = document.getElementById("btnMicToggle");
  const userTextInput = document.getElementById("userTextInput");
  const btnSendText = document.getElementById("btnSendText");

  // Ringing phase
  statusIndicator.className = "call-status-indicator ringing";
  statusText.textContent = "Dialing Outbound Lead...";
  btnStartCall.style.display = "none";
  btnEndCall.style.display = "inline-flex";

  setTimeout(() => {
    isCallActive = true;
    statusIndicator.className = "call-status-indicator active";
    statusText.textContent = "Call Connected • Qualifying Lead";

    btnMicToggle.disabled = false;
    userTextInput.disabled = false;
    btnSendText.disabled = false;

    // Start timer
    callSeconds = 0;
    startTimer();

    // Trigger Initial Agent Greeting (Phase 0)
    const initialGreeting = "Hello, good afternoon! This is Aarav from Divyasree Developers. I am reaching out regarding our new private valley development, Whispers of the Wind, nestled right at the foothills of Nandi Hills. I hope I am not catching you at an inconvenient time—do you have two quick minutes to speak?";
    appendMessage("Agent", initialGreeting);
    playAgentSpeech(initialGreeting);

    if (onConnected) onConnected();
  }, 1000);
}

function endOutboundCall() {
  isCallActive = false;
  clearInterval(callTimer);
  if (recognition && isRecognizing) {
    recognition.stop();
  }
  const globalAudio = document.getElementById("globalAudioPlayer");
  globalAudio.pause();

  const statusIndicator = document.getElementById("callStatusIndicator");
  const statusText = document.getElementById("callStatusText");
  const btnStartCall = document.getElementById("btnStartCall");
  const btnEndCall = document.getElementById("btnEndCall");
  const btnMicToggle = document.getElementById("btnMicToggle");
  const userTextInput = document.getElementById("userTextInput");
  const btnSendText = document.getElementById("btnSendText");

  statusIndicator.className = "call-status-indicator";
  statusText.textContent = "Call Ended • Summary Logged";
  btnStartCall.style.display = "inline-flex";
  btnEndCall.style.display = "none";

  btnMicToggle.disabled = true;
  userTextInput.disabled = true;
  btnSendText.disabled = true;
  setWaveformState("standby", "Call Disconnected");
}

function startTimer() {
  clearInterval(callTimer);
  const durElem = document.getElementById("callDuration");
  callTimer = setInterval(() => {
    callSeconds++;
    const mins = String(Math.floor(callSeconds / 60)).padStart(2, "0");
    const secs = String(callSeconds % 60).padStart(2, "0");
    durElem.textContent = `${mins}:${secs}`;
  }, 1000);
}

async function sendUserMessage(text) {
  if (!isCallActive) return;

  appendMessage("User", text);

  try {
    setWaveformState("speaking", "Aarav is thinking...");
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();

    // Append Agent response
    appendMessage("Agent", data.reply);
    updateHUD(data.state);
    playAgentSpeech(data.reply);

    // If call was closed by state engine, gracefully end call after audio finishes
    if (data.state.call_stage === "CLOSED") {
      setTimeout(() => {
        // give time for speech to complete
      }, 5000);
    }
  } catch (err) {
    console.error("Chat turn error:", err);
    setWaveformState("standby", "Aarav (Divyasree AI Consultant) • Connected");
  }
}

function appendMessage(speaker, text) {
  const feed = document.getElementById("transcriptFeed");
  const placeholder = document.getElementById("transcriptPlaceholder");
  if (placeholder) {
    placeholder.style.display = "none";
  }

  const row = document.createElement("div");
  row.className = `chat-bubble-row ${speaker.toLowerCase()}`;

  const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  row.innerHTML = `
    <div class="bubble-meta">
      <span class="speaker-tag ${speaker.toLowerCase()}">${speaker === 'Agent' ? 'Aarav (Divyasree Consultant)' : 'Lead (Prospect)'}</span>
      <span>${timeStr}</span>
    </div>
    <div class="chat-bubble">${text}</div>
  `;

  feed.appendChild(row);
  feed.scrollTop = feed.scrollHeight;
}

function playAgentSpeech(text) {
  const globalAudio = document.getElementById("globalAudioPlayer");
  setWaveformState("speaking", "Aarav is speaking...");

  const ttsUrl = `/api/tts?text=${encodeURIComponent(text)}`;
  globalAudio.src = ttsUrl;
  globalAudio.play().catch(e => {
    console.warn("Audio autoplay blocked by browser policy. User can click or interact.", e);
  });

  globalAudio.onended = () => {
    setWaveformState("standby", "Aarav (Divyasree AI Consultant) • Listening");
  };
}

function setWaveformState(state, labelText) {
  const waveform = document.getElementById("waveformBox");
  const label = document.getElementById("waveStatusLabel");

  if (state === "speaking") {
    waveform.classList.add("speaking");
  } else {
    waveform.classList.remove("speaking");
  }
  if (labelText) {
    label.textContent = labelText;
  }
}

function updateHUD(state) {
  // Score
  const scoreVal = document.getElementById("hudScoreValue");
  const progressBar = document.getElementById("hudScoreProgressBar");
  const badge = document.getElementById("hudLeadStatusBadge");

  scoreVal.textContent = state.lead_score;
  progressBar.style.width = `${state.lead_score}%`;
  badge.textContent = state.lead_status;

  if (state.lead_status === "DISQUALIFIED") {
    badge.className = "hud-badge disqualified";
  } else {
    badge.className = "hud-badge";
  }

  // Sentiment, Language, Stage
  document.getElementById("hudSentimentVal").textContent = state.sentiment;
  document.getElementById("hudLanguageVal").textContent = state.language === "hinglish" ? "Hinglish (Hindi)" : "English (IN)";
  document.getElementById("hudStageVal").textContent = state.call_stage;

  // Checkpoint 1: Intent
  const cp1 = document.getElementById("cpItem1");
  const cpStatus1 = document.getElementById("cpStatus1");
  const cpVal1 = document.getElementById("cpVal1");
  if (state.checkpoint_1_intent) {
    cp1.classList.add("completed");
    cpStatus1.textContent = "Qualified";
    cpVal1.textContent = `Intent: ${state.checkpoint_1_intent}`;
  }

  // Checkpoint 2: Geography
  const cp2 = document.getElementById("cpItem2");
  const cpStatus2 = document.getElementById("cpStatus2");
  const cpVal2 = document.getElementById("cpVal2");
  if (state.checkpoint_2_geography) {
    cp2.classList.add("completed");
    cpStatus2.textContent = state.checkpoint_2_geography === "Comfortable" || state.checkpoint_2_geography === "Convinced" ? "Qualified" : "Reluctant";
    cpVal2.textContent = `Location Fit: ${state.checkpoint_2_geography}`;
  }

  // Checkpoint 3: Budget
  const cp3 = document.getElementById("cpItem3");
  const cpStatus3 = document.getElementById("cpStatus3");
  const cpVal3 = document.getElementById("cpVal3");
  if (state.checkpoint_3_budget) {
    if (state.checkpoint_3_budget === "Qualified") {
      cp3.classList.add("completed");
      cpStatus3.textContent = "Qualified";
      cpVal3.textContent = "Budget: ≥ ₹92.4 Lakhs (Qualified)";
    } else {
      cp3.classList.add("disqualified");
      cpStatus3.textContent = "Out of Range";
      cpVal3.textContent = "Budget: Under ₹80 Lakhs (Disqualified)";
    }
  }

  // Checkpoint 4: Timeline
  const cp4 = document.getElementById("cpItem4");
  const cpStatus4 = document.getElementById("cpStatus4");
  const cpVal4 = document.getElementById("cpVal4");
  if (state.checkpoint_4_timeline) {
    cp4.classList.add("completed");
    cpStatus4.textContent = "Qualified";
    cpVal4.textContent = `Delivery: Handover Dec 2029 (${state.checkpoint_4_timeline})`;
  }
}

async function resetSession() {
  endOutboundCall();
  try {
    const res = await fetch("/api/reset", { method: "POST" });
    const data = await res.json();

    // Clear transcript
    const feed = document.getElementById("transcriptFeed");
    feed.innerHTML = `
      <div class="transcript-placeholder" id="transcriptPlaceholder">
        <div class="placeholder-icon">📞</div>
        <h3>Start an Outbound Call Simulation</h3>
        <p>Click "Start Outbound Call" below. The agent will greet you with executive courtesy, ask for permission to speak, qualify across 4 checkpoints, and transition to a Property Expert CTA.</p>
        <div class="placeholder-features">
          <span>&bull; Real-time Speech-to-Speech</span>
          <span>&bull; Indian English & Hinglish Code-Switching</span>
          <span>&bull; Auto Checkpoint Extraction</span>
        </div>
      </div>
    `;

    // Reset HUD
    document.querySelectorAll(".checkpoint-item").forEach(item => {
      item.classList.remove("completed", "disqualified");
    });
    document.getElementById("cpStatus1").textContent = "Pending";
    document.getElementById("cpVal1").textContent = "—";
    document.getElementById("cpStatus2").textContent = "Pending";
    document.getElementById("cpVal2").textContent = "—";
    document.getElementById("cpStatus3").textContent = "Pending";
    document.getElementById("cpVal3").textContent = "—";
    document.getElementById("cpStatus4").textContent = "Pending";
    document.getElementById("cpVal4").textContent = "—";

    updateHUD(data.state);
    document.getElementById("callDuration").textContent = "00:00";
  } catch (err) {
    console.error("Reset failed", err);
  }
}

// ================= RECORDED FLOWS CONTROLLER =================
let activeFlowAudio = null;
let activePlayBtn = null;

async function initRecordedFlows() {
  const container = document.getElementById("flowsContainer");
  try {
    const res = await fetch("/api/flows");
    const data = await res.json();

    const audioFilenameMap = {
      "flow_1": "/static/audio/Flow_1_HNI_Investor_Happy_Path.mp3",
      "flow_2": "/static/audio/Flow_2_Luxury_Weekend_Home_Buyer.mp3",
      "flow_3": "/static/audio/Flow_3_Budget_Constraint_Handling.mp3",
      "flow_4": "/static/audio/Flow_4_Location_Objection_Handling.mp3",
      "flow_5": "/static/audio/Flow_5_Irritated_User_Multilingual_Hinglish.mp3"
    };

    container.innerHTML = data.flows.map((flow, index) => {
      const audioUrl = audioFilenameMap[flow.id] || "";
      let badgeClass = "";
      if (flow.lead_score.includes("HOT")) badgeClass = "";
      else if (flow.lead_score.includes("DISQUALIFIED")) badgeClass = "red";
      else badgeClass = "orange";

      const dialogueHtml = flow.dialogue.map(d => `
        <div class="dialogue-turn-row">
          <span class="d-speaker ${d.speaker.toLowerCase()}">${d.speaker === 'Agent' ? 'Aarav (Divyasree)' : 'Lead'}:</span>
          <span>${d.text}</span>
        </div>
      `).join("");

      return `
        <div class="flow-card" data-flow-id="${flow.id}">
          <div class="flow-card-top">
            <div class="flow-title-block">
              <h3>${flow.title}</h3>
              <p class="flow-persona">${flow.persona}</p>
            </div>
            <div class="flow-outcome-badge ${badgeClass}">${flow.lead_score} &bull; ${flow.outcome}</div>
          </div>

          <!-- Audio Player Bar -->
          <div class="flow-audio-row">
            <button class="flow-play-btn" data-audio-url="${audioUrl}" title="Play Audio Simulation">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
            </button>
            <div class="flow-audio-track">
              <input type="range" class="flow-timeline-slider" value="0" min="0" max="100" step="0.1">
              <div class="flow-audio-time">
                <span class="curr-time">0:00</span>
                <span class="total-time">--:--</span>
              </div>
            </div>
          </div>

          <!-- Transcript Accordion -->
          <button class="flow-transcript-toggle" onclick="toggleTranscript('${flow.id}')">
            <span>View Full Synchronized Transcript (${flow.dialogue.length} Turns)</span>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
          </button>
          <div class="flow-transcript-body" id="transcript_${flow.id}">
            ${dialogueHtml}
          </div>
        </div>
      `;
    }).join("");

    attachFlowAudioEvents();
  } catch (err) {
    console.error("Failed to load conversation flows", err);
  }
}

function attachFlowAudioEvents() {
  const cards = document.querySelectorAll(".flow-card");

  cards.forEach(card => {
    const playBtn = card.querySelector(".flow-play-btn");
    const audioUrl = playBtn.dataset.audioUrl;
    const slider = card.querySelector(".flow-timeline-slider");
    const currTimeElem = card.querySelector(".curr-time");
    const totalTimeElem = card.querySelector(".total-time");

    const audio = new Audio(audioUrl);

    audio.addEventListener("loadedmetadata", () => {
      totalTimeElem.textContent = formatTime(audio.duration);
    });

    audio.addEventListener("timeupdate", () => {
      if (audio.duration) {
        slider.value = (audio.currentTime / audio.duration) * 100;
        currTimeElem.textContent = formatTime(audio.currentTime);
      }
    });

    audio.addEventListener("ended", () => {
      playBtn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>`;
      slider.value = 0;
      currTimeElem.textContent = "0:00";
    });

    slider.addEventListener("input", () => {
      if (audio.duration) {
        audio.currentTime = (slider.value / 100) * audio.duration;
      }
    });

    playBtn.addEventListener("click", () => {
      if (activeFlowAudio && activeFlowAudio !== audio) {
        activeFlowAudio.pause();
        if (activePlayBtn) {
          activePlayBtn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>`;
        }
      }

      if (audio.paused) {
        audio.play();
        activeFlowAudio = audio;
        activePlayBtn = playBtn;
        playBtn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>`;
      } else {
        audio.pause();
        playBtn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>`;
      }
    });
  });
}

function toggleTranscript(flowId) {
  const elem = document.getElementById(`transcript_${flowId}`);
  if (elem) {
    elem.classList.toggle("open");
  }
}

function formatTime(sec) {
  if (isNaN(sec)) return "0:00";
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${m}:${s < 10 ? '0' : ''}${s}`;
}

// Global Clipboard helper
window.copyToClipboard = function(elementId) {
  const text = document.getElementById(elementId).innerText;
  navigator.clipboard.writeText(text).then(() => {
    alert("Configuration JSON copied to clipboard!");
  }).catch(err => {
    console.error("Clipboard copy failed", err);
  });
};

window.toggleTranscript = toggleTranscript;
