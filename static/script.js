/* ==========================================================================
   Meeting Notes Summarizer — Frontend logic
   Pure vanilla JS. No frameworks, no build step.
   ========================================================================== */

(() => {
  "use strict";

  const MAX_CHARACTERS = 10000;
  const MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024; // 5MB

  // ---- Element references -------------------------------------------------
  const tabButtons = document.querySelectorAll(".tab-btn");
  const panelPaste = document.getElementById("panel-paste");
  const panelUpload = document.getElementById("panel-upload");

  const notesInput = document.getElementById("notesInput");
  const charCounter = document.getElementById("charCounter");

  const dropzone = document.getElementById("dropzone");
  const browseBtn = document.getElementById("browseBtn");
  const fileInput = document.getElementById("fileInput");
  const fileSelected = document.getElementById("fileSelected");
  const fileSelectedName = document.getElementById("fileSelectedName");
  const fileRemoveBtn = document.getElementById("fileRemoveBtn");

  const errorBanner = document.getElementById("errorBanner");

  const generateBtn = document.getElementById("generateBtn");
  const btnContent = generateBtn.querySelector(".btn-content");
  const btnLoading = generateBtn.querySelector(".btn-loading");

  const clearAllBtn = document.getElementById("clearAllBtn");
  const copyAllBtn = document.getElementById("copyAllBtn");

  const summaryOutput = document.getElementById("summaryOutput");
  const actionItemsOutput = document.getElementById("actionItemsOutput");
  const keyDecisionsOutput = document.getElementById("keyDecisionsOutput");
  const openQuestionsOutput = document.getElementById("openQuestionsOutput");
  const tokenInput = document.getElementById("tokenInput");
  const tokenOutput = document.getElementById("tokenOutput");
  const tokenTotal = document.getElementById("tokenTotal");

  const toast = document.getElementById("toast");

  // ---- State ---------------------------------------------------------------
  let activeTab = "paste";
  let selectedFile = null;
  let lastResult = null;

  const EMPTY_TEXT = {
    summary: "Your summary will appear here...",
    action_items: ["Your action items will appear here..."],
    key_decisions: ["Your key decisions will appear here..."],
    open_questions: ["Your open questions will appear here..."],
  };

  // Reset initial UI states
  setLoading(false);
  resetFileSelection();

  // ==========================================================================
  // Tabs
  // ==========================================================================
  tabButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      activeTab = btn.dataset.tab;
      tabButtons.forEach((b) => b.classList.toggle("active", b === btn));
      panelPaste.classList.toggle("active", activeTab === "paste");
      panelUpload.classList.toggle("active", activeTab === "upload");
      hideError();
    });
  });

  // ==========================================================================
  // Character counter
  // ==========================================================================
  notesInput.addEventListener("input", () => {
    const len = notesInput.value.length;
    charCounter.textContent = `${len} / ${MAX_CHARACTERS} characters`;
    charCounter.classList.toggle("limit-reached", len >= MAX_CHARACTERS);
  });

  // ==========================================================================
  // File upload: browse, drag & drop, remove
  // ==========================================================================
  browseBtn.addEventListener("click", () => fileInput.click());

  fileInput.addEventListener("change", () => {
    if (fileInput.files && fileInput.files[0]) {
      handleFileSelection(fileInput.files[0]);
    }
  });

  ["dragenter", "dragover"].forEach((evt) => {
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.add("dragover");
    });
  });

  ["dragleave", "drop"].forEach((evt) => {
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.remove("dragover");
    });
  });

  dropzone.addEventListener("drop", (e) => {
    const files = e.dataTransfer.files;
    if (files && files[0]) {
      handleFileSelection(files[0]);
    }
  });

  fileRemoveBtn.addEventListener("click", () => {
    resetFileSelection();
    hideError();
  });

  function handleFileSelection(file) {
    hideError();

    if (!file.name.toLowerCase().endsWith(".txt")) {
      showError("Only .txt files are supported.");
      return;
    }

    if (file.size > MAX_FILE_SIZE_BYTES) {
      showError("File exceeds the maximum size of 5MB.");
      return;
    }

    selectedFile = file;
    fileSelectedName.textContent = file.name;
    fileSelected.hidden = false;
    fileSelected.style.display = "flex";
  }

  function resetFileSelection() {
    selectedFile = null;
    fileInput.value = "";
    fileSelected.hidden = true;
    fileSelected.style.display = "none";
  }

  // ==========================================================================
  // Error banner
  // ==========================================================================
  function showError(message) {
    errorBanner.textContent = message;
    errorBanner.hidden = false;
  }

  function hideError() {
    errorBanner.hidden = true;
    errorBanner.textContent = "";
  }

  // ==========================================================================
  // Generate Summary
  // ==========================================================================
  generateBtn.addEventListener("click", async () => {
    hideError();

    const notesText = notesInput.value.trim();
    const hasText = activeTab === "paste" && notesText.length > 0;
    const hasFile = activeTab === "upload" && selectedFile !== null;

    if (!hasText && !hasFile) {
      showError(
        activeTab === "paste"
          ? "Please paste some meeting notes first."
          : "Please select a .txt file to upload."
      );
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      if (hasText) {
        formData.append("notes", notesText);
      }
      if (hasFile) {
        formData.append("file", selectedFile);
      }

      const response = await fetch("/generate", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        showError(data.error || "Something went wrong. Please try again.");
        return;
      }

      lastResult = data;
      renderResults(data);
    } catch (err) {
      showError("Could not reach the server. Please check your connection and try again.");
    } finally {
      setLoading(false);
    }
  });

  function setLoading(isLoading) {
    generateBtn.disabled = isLoading;
    if (isLoading) {
      btnContent.style.display = "none";
      btnLoading.style.display = "inline-flex";
      btnLoading.removeAttribute("hidden");
    } else {
      btnContent.style.display = "inline-flex";
      btnLoading.style.display = "none";
      btnLoading.setAttribute("hidden", "true");
    }
  }

  // ==========================================================================
  // Render results into cards
  // ==========================================================================
  function renderResults(data) {
  summaryOutput.textContent = data.summary || "No summary generated.";
  summaryOutput.classList.add("filled");

  fillList("action_items", actionItemsOutput, data.action_items, "No action items identified.");
  fillList("key_decisions", keyDecisionsOutput, data.key_decisions, "No key decisions recorded.");
  fillList("open_questions", openQuestionsOutput, data.open_questions, "No open questions identified.");

  const usage = data.token_usage || {};
  tokenInput.textContent = usage.input ?? "--";
  tokenOutput.textContent = usage.output ?? "--";
  tokenTotal.textContent = usage.total ?? "--";
}

  function fillList(cardKey, listEl, items, emptyMessage) {
  listEl.innerHTML = "";
  const hasItems = Array.isArray(items) && items.length > 0;
  
  // Get copy button corresponding to this card
  const copyBtn = document.querySelector(`.copy-btn[data-copy-target="${cardKey}"]`);

  if (hasItems) {
    items.forEach((text) => {
      const li = document.createElement("li");
      li.textContent = text;
      listEl.appendChild(li);
    });
    listEl.classList.add("filled");
    
    // Enable copy button when items exist
    if (copyBtn) {
      copyBtn.disabled = false;
      copyBtn.style.opacity = "1";
      copyBtn.style.cursor = "pointer";
    }
  } else {
    const li = document.createElement("li");
    li.textContent = emptyMessage;
    li.style.listStyleType = "none"; // Clean look for empty state
    li.style.color = "var(--text-muted)";
    listEl.appendChild(li);
    listEl.classList.remove("filled");

    // Disable copy button so it's not copyable!
    if (copyBtn) {
      copyBtn.disabled = true;
      copyBtn.style.opacity = "0.3";
      copyBtn.style.cursor = "not-allowed";
    }
  }
}

  // ==========================================================================
  // Clear All
  // ==========================================================================
  clearAllBtn.addEventListener("click", () => {
    notesInput.value = "";
    charCounter.textContent = `0 / ${MAX_CHARACTERS} characters`;
    charCounter.classList.remove("limit-reached");

    resetFileSelection();
    hideError();

    summaryOutput.textContent = EMPTY_TEXT.summary;
    summaryOutput.classList.remove("filled");

    // Reset all list outputs properly matching fillList parameters!
    fillList("action_items", actionItemsOutput, null, EMPTY_TEXT.action_items[0]);
    fillList("key_decisions", keyDecisionsOutput, null, EMPTY_TEXT.key_decisions[0]);
    fillList("open_questions", openQuestionsOutput, null, EMPTY_TEXT.open_questions[0]);

    tokenInput.textContent = "--";
    tokenOutput.textContent = "--";
    tokenTotal.textContent = "--";

    lastResult = null;

    showToast("Cleared");
  });

  // ==========================================================================
  // Copy individual card
  // ==========================================================================
  document.querySelectorAll(".copy-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (btn.disabled) return;
      const target = btn.dataset.copyTarget;
      const text = getCardText(target);
      if (text) {
      copyToClipboard(text);
      showToast("Copied to clipboard");
    }
  });
});

  function getCardText(target) {
    if (!lastResult) return "";
    switch (target) {
      case "summary":
        return lastResult.summary || "";
      case "action_items":
        return (lastResult.action_items || []).map((i) => `- ${i}`).join("\n");
      case "key_decisions":
        return (lastResult.key_decisions || []).map((i) => `- ${i}`).join("\n");
      case "open_questions":
        return (lastResult.open_questions || []).map((i) => `- ${i}`).join("\n");
      default:
        return "";
    }
  }

  // ==========================================================================
  // Copy All Results
  // ==========================================================================
  copyAllBtn.addEventListener("click", () => {
    if (!lastResult) {
      showToast("Nothing to copy yet");
      return;
    }

    const usage = lastResult.token_usage || {};
    const parts = [
      "Summary:",
      lastResult.summary || "",
      "",
      "Action Items:",
      ...(lastResult.action_items || []).map((i) => `- ${i}`),
      "",
      "Key Decisions:",
      ...(lastResult.key_decisions || []).map((i) => `- ${i}`),
      "",
      "Open Questions:",
      ...(lastResult.open_questions || []).map((i) => `- ${i}`),
      "",
      `Token Usage — Input: ${usage.input ?? "--"}, Output: ${usage.output ?? "--"}, Total: ${usage.total ?? "--"}`,
    ];

    copyToClipboard(parts.join("\n"));
    showToast("All results copied");
  });

  function copyToClipboard(text) {
    if (!text) return;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).catch(() => fallbackCopy(text));
    } else {
      fallbackCopy(text);
    }
  }

  function fallbackCopy(text) {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand("copy");
    } catch (e) {
      /* no-op */
    }
    document.body.removeChild(textarea);
  }

  // ==========================================================================
  // Toast
  // ==========================================================================
  let toastTimer = null;
  function showToast(message) {
    toast.textContent = message;
    toast.hidden = false;
    void toast.offsetWidth;
    toast.classList.add("show");

    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toast.classList.remove("show");
      setTimeout(() => { toast.hidden = true; }, 150);
    }, 1800);
  }
})();