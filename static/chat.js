const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const jsonOutput = document.getElementById('json-output');
const statusBadge = document.getElementById('status-badge');
const confidenceDisplay = document.getElementById('confidence-display');

// Summary elements
const summaryIntent = document.getElementById('summary-intent');
const summaryTemplate = document.getElementById('summary-template');
const summaryMode = document.getElementById('summary-mode');
const summaryColors = document.getElementById('summary-colors');
const summaryStyle = document.getElementById('summary-style');

let messages = [];
let lastParams = null;

// Handle Enter key
userInput.addEventListener('keypress', function (e) {
  if (e.key === 'Enter') {
    sendMessage();
  }
});

function appendMessage(text, cls) {
  const div = document.createElement('div');
  div.className = `message ${cls}`;

  const content = document.createElement('div');
  content.className = 'message-content';
  content.innerHTML = text;

  div.appendChild(content);
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function updateStatus(status, type = '') {
  statusBadge.textContent = status;
  statusBadge.className = `status-badge ${type}`;
}

function updateConfidence(value) {
  if (value !== null && value !== undefined) {
    const percent = Math.round(value * 100);
    confidenceDisplay.textContent = `Confidence: ${percent}%`;
  } else {
    confidenceDisplay.textContent = '—';
  }
}

function updateSummary(data) {
  if (!data) {
    summaryIntent.textContent = '—';
    summaryTemplate.textContent = '—';
    summaryMode.textContent = '—';
    summaryColors.textContent = '—';
    summaryStyle.textContent = '—';
    return;
  }

  summaryIntent.textContent = data.intent || '—';
  summaryTemplate.textContent = data.template || '—';

  if (data.parameters) {
    const p = data.parameters;
    summaryMode.textContent = p.generate_mode || '—';
    summaryColors.textContent = p.colors ? `${p.colors} colors` : '—';
    summaryStyle.textContent = p.design_style || '—';
  }
}

function updateParameters(data) {
  if (!data) return;

  lastParams = data;

  // Format JSON with syntax highlighting
  const formatted = JSON.stringify(data, null, 2);
  jsonOutput.textContent = formatted;

  // Update summary
  updateSummary(data);

  // Update confidence
  updateConfidence(data.confidence);

  // Flash effect
  jsonOutput.style.backgroundColor = '#1a2744';
  setTimeout(() => {
    jsonOutput.style.backgroundColor = '#0d1117';
  }, 200);
}

function copyJSON() {
  if (!lastParams) return;

  navigator.clipboard.writeText(JSON.stringify(lastParams, null, 2)).then(() => {
    const btn = document.querySelector('.copy-btn');
    const originalText = btn.textContent;
    btn.textContent = '✓ Copied!';
    setTimeout(() => {
      btn.textContent = originalText;
    }, 1500);
  });
}

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  // UI Updates
  appendMessage(text, 'user');
  userInput.value = '';
  userInput.disabled = true;
  updateStatus('Processing...', 'processing');

  messages.push({ role: 'user', content: text });

  // Add loading placeholder
  const loadingDiv = document.createElement('div');
  loadingDiv.className = 'message bot';
  loadingDiv.innerHTML = '<div class="message-content">Analyzing your request...</div>';
  chatBox.appendChild(loadingDiv);
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages })
    });

    const data = await res.json();

    // Remove loading placeholder
    if (loadingDiv.parentNode) chatBox.removeChild(loadingDiv);

    if (data.error) {
      appendMessage(`<strong>Error:</strong> ${data.error}`, 'bot');
      updateStatus('Error', 'error');
    } else {
      // Handle structured response
      if (data.structured) {
        updateParameters(data.structured);

        if (data.structured.clarification_required) {
          appendMessage(data.structured.question || "Could you provide more details?", 'bot');
          updateStatus('Waiting for input', 'processing');
        } else {
          const template = data.structured.template || 'custom';
          const intent = data.structured.intent || 'pattern';
          appendMessage(
            `<strong>Generated!</strong> Using template: <code>${template}</code> for <em>${intent}</em> pattern.`,
            'bot'
          );
          updateStatus('Ready', 'ready');
        }
      } else {
        // Fallback for non-JSON response
        appendMessage(data.reply, 'bot');
        updateStatus('Ready', 'ready');
      }

      messages.push({ role: 'assistant', content: data.reply });
    }
  } catch (err) {
    if (loadingDiv.parentNode) chatBox.removeChild(loadingDiv);
    appendMessage(`<strong>Network Error:</strong> ${err.message}`, 'bot');
    updateStatus('Error', 'error');
  } finally {
    userInput.disabled = false;
    userInput.focus();
  }
}

// Focus on load
window.addEventListener('load', () => userInput.focus());
