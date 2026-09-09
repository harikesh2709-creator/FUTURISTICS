export function initAIAssistant() {
  const chatFeed = document.getElementById('ai-chat-feed');
  const input = document.getElementById('ai-prompt-input');
  const sendBtn = document.getElementById('ai-send-btn');
  const suggestions = document.getElementById('ai-suggested-prompts');

  if (!chatFeed || !input) return;

  function addMessage(text, isUser = false) {
    const msg = document.createElement('div');
    msg.style.display = 'flex';
    msg.style.gap = '16px';
    msg.style.alignItems = 'flex-start';
    msg.style.animation = 'fadeSlideUp 0.3s var(--ease-spring) both';
    
    if (isUser) {
      msg.innerHTML = `
        <div style="flex: 1;"></div>
        <div style="background: rgba(255,255,255,0.05); border: 1px solid var(--glass-border); padding: 12px 16px; border-radius: 12px 12px 0 12px; max-width: 80%; color: #fff; font-size: 14px; line-height: 1.5;">
          ${text}
        </div>
        <div style="width: 32px; height: 32px; border-radius: 50%; background: #3b82f6; display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0;">👤</div>
      `;
    } else {
      msg.innerHTML = `
        <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(99, 102, 241, 0.2); color: #818cf8; display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0; box-shadow: 0 0 10px rgba(99, 102, 241, 0.1);">🧠</div>
        <div style="background: rgba(99, 102, 241, 0.05); border: 1px solid rgba(99, 102, 241, 0.2); padding: 12px 16px; border-radius: 12px 12px 12px 0; max-width: 80%; color: #e5e5e5; font-size: 14px; line-height: 1.5;">
          ${text}
        </div>
        <div style="flex: 1;"></div>
      `;
    }
    
    chatFeed.appendChild(msg);
    chatFeed.scrollTop = chatFeed.scrollHeight;
  }

  function getAIResponse(prompt) {
    const p = prompt.toLowerCase();
    
    if (p.includes('cape') || p.includes('rate')) {
      return "Based on my analysis of the latest Baltic Dry Index and synthetic market data, Capesize rates are currently experiencing a slight upward trend. I recommend locking in short-term COAs if your shipment volume exceeds 150,000 MT this quarter to hedge against upcoming volatility.";
    } 
    
    if (p.includes('weather') || p.includes('risk') || p.includes('australia')) {
      return "I've detected elevated risk levels for Australian origins (Newcastle, Hay Point) due to historical cyclone patterns in the upcoming months. The current idle risk score for these routes is high. Consider diversifying origins or buffering transit times by 4-6 days.";
    }
    
    if (p.includes('contract') || p.includes('strategy')) {
      return "Looking at the 90-day forecast, the market shows a rising trend (magnitude > 3%). My predictive model suggests moving away from the Spot market. A Mid-Term (12 month) COA could yield approximately 7% savings annually compared to current spot rates.";
    }

    return "I am analyzing the global freight network... My current models indicate stable conditions across major East Coast India trade lanes. Is there a specific vessel class or route you would like me to evaluate?";
  }

  function handleSend(text) {
    if (!text.trim()) return;
    
    addMessage(text, true);
    input.value = '';
    
    // Simulate thinking delay
    setTimeout(() => {
      addMessage(getAIResponse(text), false);
    }, 600 + Math.random() * 800);
  }

  sendBtn.addEventListener('click', () => handleSend(input.value));
  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSend(input.value);
  });

  if (suggestions) {
    suggestions.addEventListener('click', (e) => {
      if (e.target.tagName === 'SPAN') {
        handleSend(e.target.innerText);
      }
    });
  }

  // Initial greeting
  if (chatFeed.children.length === 0) {
    setTimeout(() => {
      addMessage("Hello! I am the FreightForecast AI. I continuously monitor global charter rates, port congestion, and seasonal risks. How can I assist with your procurement strategy today?");
    }, 500);
  }
}
