const chatEl = document.getElementById('chat');
const form = document.getElementById('chat-form');
const input = document.getElementById('user-input');
const sendButton = form.querySelector('button[type="submit"]');

let providerName = 'loading...';

// Fetch the current provider on page load
fetch('/health')
  .then(r => r.json())
  .then(data => {
    providerName = data.provider || 'unknown';
    console.log('Using provider:', providerName);
  })
  .catch(e => console.error('Failed to fetch provider info:', e));

const messages = [];

function appendMessage(who, text, cls = '') {
  const div = document.createElement('div');
  div.className = 'message ' + cls;
  const whoEl = document.createElement('strong');
  whoEl.textContent = who + ':';
  const textNode = document.createElement('span');
  textNode.textContent = ' ' + text;
  div.appendChild(whoEl);
  div.appendChild(textNode);
  chatEl.appendChild(div);
  chatEl.scrollTop = chatEl.scrollHeight;
}

function setBusy(b) {
  input.disabled = b;
  sendButton.disabled = b;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  appendMessage('You', text, 'user');
  messages.push({ role: 'user', content: text });
  input.value = '';
  setBusy(true);
  const typingId = 'typing';
  appendMessage('Bot', '…', 'bot');

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages })
    });
    const data = await res.json();
    // remove last bot typing placeholder
    const last = chatEl.lastChild;
    if (last && last.querySelector && last.querySelector('strong') && last.querySelector('strong').textContent.startsWith('Bot')) {
      chatEl.removeChild(last);
    }
    if (data.reply) {
      appendMessage('Bot', data.reply, 'bot');
      messages.push({ role: 'assistant', content: data.reply });
    } else {
      appendMessage('Bot', 'Error: ' + (data.error || 'Unknown'), 'bot');
    }
  } catch (err) {
    // remove typing placeholder
    const last = chatEl.lastChild;
    if (last && last.querySelector && last.querySelector('strong') && last.querySelector('strong').textContent.startsWith('Bot')) {
      chatEl.removeChild(last);
    }
    appendMessage('Bot', 'Network error: ' + err.message, 'bot');
  } finally {
    setBusy(false);
    input.focus();
  }
});

// focus on load
window.addEventListener('load', () => input.focus());
