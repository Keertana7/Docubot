/**
 * Docubot Frontend - JavaScript Logic
 * Handles chat interaction, API calls, and UI updates
 */

// DOM Elements
const chatHistory = document.getElementById("chat-history");
const queryInput = document.getElementById("query-input");
const sendBtn = document.getElementById("send-btn");
const spinner = document.getElementById("spinner");
const levelSelect = document.getElementById("level-select");
const topKSlider = document.getElementById("top-k-slider");
const topKValue = document.getElementById("top-k-value");
const statusSpan = document.getElementById("status");

// State
let isLoading = false;
let messageCount = 0;

/**
 * Update Top K display value
 */
topKSlider.addEventListener("input", (e) => {
    topKValue.textContent = e.target.value;
});

/**
 * Handle key press in input (Send on Enter)
 */
function handleKeyPress(event) {
    if (event.key === "Enter" && !isLoading) {
        sendQuery();
    }
}

/**
 * Send query to backend
 */
async function sendQuery() {
    const query = queryInput.value.trim();

    if (!query) {
        alert("Please enter a question.");
        return;
    }

    if (isLoading) {
        return;
    }

    // Get settings
    const level = levelSelect.value;
    const topK = parseInt(topKSlider.value);

    // Add user message to chat
    addMessage("user", query);

    // Clear input
    queryInput.value = "";
    queryInput.focus();

    // Show loading spinner
    setLoading(true);

    try {
        // Call backend API
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                query: query,
                level: level,
                top_k: topK,
            }),
        });

        const data = await response.json();

        // Check if response was successful (both 200 with response field or error field)
        if (response.ok && data.response) {
            addMessage("bot", data.response);
            statusSpan.textContent = "Ready";
        } else if (data.error) {
            addMessage("bot", `Error: ${data.error}`);
            statusSpan.textContent = "Error";
        } else if (data.response) {
            // Response may contain error info even in 200 status
            addMessage("bot", data.response);
            statusSpan.textContent = "Ready";
        } else {
            addMessage("bot", "Unexpected response from server");
            statusSpan.textContent = "Error";
        }
    } catch (error) {
        console.error("Error:", error);
        addMessage("bot", `❌ Connection error: ${error.message}`);
        statusSpan.textContent = "Error";
    } finally {
        setLoading(false);
    }
}

/**
 * Add message to chat history
 */
function addMessage(role, content) {
    messageCount++;

    // Remove welcome message if first message
    if (messageCount === 1) {
        const welcome = chatHistory.querySelector(".welcome-message");
        if (welcome) {
            welcome.remove();
        }
    }

    // Create message element
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${role}`;

    const contentDiv = document.createElement("div");
    contentDiv.className = "message-content";

    // Format content (add line breaks for readability)
    contentDiv.innerHTML = formatMessage(content);

    messageDiv.appendChild(contentDiv);

    // Add metadata
    const metaDiv = document.createElement("div");
    metaDiv.className = "message-meta";
    metaDiv.textContent = new Date().toLocaleTimeString();
    messageDiv.appendChild(metaDiv);

    chatHistory.appendChild(messageDiv);

    // Scroll to bottom
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

/**
 * Format message content (basic markdown-like formatting)
 */
function formatMessage(content) {
    // If marked and DOMPurify are loaded, use them for robust Markdown rendering + sanitization
    if (window.marked && window.DOMPurify) {
        try {
            const raw = marked.parse(content);
            return DOMPurify.sanitize(raw);
        } catch (e) {
            console.warn('marked parsing failed, falling back to simple formatter', e);
            // fall through to fallback formatter
        }
    }

    // Fallback: Basic Markdown-like formatter
    const div = document.createElement("div");
    div.appendChild(document.createTextNode(content));
    const escaped = div.innerHTML;

    // Process line-by-line for block elements
    const lines = escaped.split(/\n/);
    let inList = false;
    const out = [];

    lines.forEach((line) => {
        // Headings: #, ##, ### etc.
        const heading = line.match(/^(#{1,6})\s+(.*)$/);
        if (heading) {
            if (inList) { out.push("</ul>"); inList = false; }
            const level = heading[1].length;
            out.push(`<h${level}>${heading[2]}</h${level}>`);
            return;
        }

        // Unordered list items (- or *)
        const li = line.match(/^\s*[-*]\s+(.*)$/);
        if (li) {
            if (!inList) { out.push("<ul>"); inList = true; }
            out.push(`<li>${li[1]}</li>`);
            return;
        } else if (inList) {
            out.push("</ul>");
            inList = false;
        }

        // Blank line -> small break
        if (line.trim() === "") {
            out.push("<br>");
            return;
        }

        // Inline formatting: code, bold (** or __), italics (* or _), links
        let processed = line
            .replace(/`([^`]+)`/g, "<code>$1</code>")
            .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
            .replace(/__([^_]+)__/g, "<strong>$1</strong>")
            .replace(/\*([^*]+)\*/g, "<em>$1</em>")
            .replace(/_([^_]+)_/g, "<em>$1</em>")
            .replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank" style="color: #4f46e5; text-decoration: underline;">$1</a>');

        out.push(`<p>${processed}</p>`);
    });

    if (inList) out.push("</ul>");

    return out.join("");
}

/**
 * Set loading state
 */
function setLoading(loading) {
    isLoading = loading;
    sendBtn.disabled = loading;
    queryInput.disabled = loading;

    if (loading) {
        spinner.classList.remove("hidden");
        statusSpan.textContent = "Thinking...";
    } else {
        spinner.classList.add("hidden");
    }
}

/**
 * Clear chat history
 */
function clearHistory() {
    if (confirm("Clear all messages? This cannot be undone.")) {
        chatHistory.innerHTML = `
            <div class="welcome-message">
                <h2>Welcome to Docubot! 👋</h2>
                <p>Ask me anything about Ceph distributed storage system.</p>
                <p><em>Examples:</em></p>
                <ul>
                    <li>"What is Ceph?"</li>
                    <li>"How does CRUSH algorithm work?"</li>
                    <li>"Explain OSDs in Ceph"</li>
                    <li>"What is RADOS?"</li>
                </ul>
            </div>
        `;
        messageCount = 0;
        statusSpan.textContent = "Ready";
    }
}

/**
 * Initialize app
 */
function initApp() {
    console.log("Docubot initialized");
    
    // Check health
    fetch("/api/health")
        .then((res) => res.json())
        .then((data) => {
            if (data.gemini_api_key_set) {
                statusSpan.textContent = "Ready";
            } else {
                statusSpan.textContent = "⚠ API Key not set";
                console.warn("GEMINI_API_KEY is not set");
            }
        })
        .catch((err) => {
            console.error("Health check failed:", err);
            statusSpan.textContent = "Error";
        });

    // Focus input on load
    queryInput.focus();
}

// Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", initApp);


