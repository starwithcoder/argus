<template>
  <div class="chat">
    <!-- 顶部标题栏 -->
    <header class="chat-header">
      <div class="title">智能对话</div>
      <div class="subtitle">Argus Agent · 演示模式</div>
      <button class="clear" @click="clearChat" v-if="messages.length">清空对话</button>
    </header>

    <!-- 消息列表 -->
    <div class="messages" ref="msgBox">
      <!-- 空状态（类似千问的欢迎页） -->
      <div v-if="messages.length === 0" class="empty">
        <div class="empty-icon">💬</div>
        <h2>有什么可以帮你的？</h2>
        <p>我是 Argus 智能体，试试下面的问题，或直接输入。</p>
        <div class="suggestions">
          <button
            v-for="q in suggestions"
            :key="q"
            @click="send(q)"
          >
            {{ q }}
          </button>
        </div>
      </div>

      <!-- 消息气泡 -->
      <div
        v-for="(m, i) in messages"
        :key="i"
        class="msg"
        :class="m.role"
      >
        <div class="avatar" :class="m.role">
          {{ m.role === "user" ? "我" : "AI" }}
        </div>
        <div class="bubble">
          <template v-for="(seg, j) in blocks(m)" :key="j">
            <pre v-if="seg.type === 'code'" class="code"><code>{{ seg.value }}</code></pre>
            <div v-else class="text" v-html="formatText(seg.value)"></div>
          </template>
        </div>
      </div>

      <!-- 加载中（打字气泡） -->
      <div v-if="loading" class="msg assistant">
        <div class="avatar assistant">AI</div>
        <div class="bubble">
          <div class="typing"><span></span><span></span><span></span></div>
        </div>
      </div>
    </div>

    <!-- 输入区 -->
    <footer class="input-bar">
      <textarea
        v-model="input"
        rows="1"
        ref="ta"
        placeholder="输入消息，Enter 发送，Shift+Enter 换行"
        @keydown.enter.exact.prevent="send()"
        @input="autoGrow"
      ></textarea>
      <button class="send" :disabled="loading || !input.trim()" @click="send()">
        {{ loading ? "生成中…" : "发送" }}
      </button>
    </footer>
  </div>
</template>

<script setup>
import { ref, nextTick } from "vue";

const messages = ref([]);
const input = ref("");
const loading = ref(false);
const msgBox = ref(null);
const ta = ref(null);
const suggestions = [
  "你好，介绍一下你自己",
  "帮我写一段 Python 代码",
  "什么是 RAG？",
];

async function send(text) {
  const content = (text ?? input.value).trim();
  if (!content || loading.value) return;

  messages.value.push({ role: "user", content });
  input.value = "";
  autoGrow();
  await scrollToBottom();

  loading.value = true;
  try {
    const reply = await chatRequest(
      messages.value.map((m) => ({ role: m.role, content: m.content }))
    );
    const ai = { role: "assistant", content: "", streaming: true };
    messages.value.push(ai);
    await scrollToBottom();
    await typeWriter(ai, reply);
  } finally {
    loading.value = false;
  }
}

function clearChat() {
  messages.value = [];
}

// 调用后端对话接口；后端尚未实现时回退到本地模拟回复，保证界面可演示。
// 后端就绪后，将下方 URL 改为真实端点（如 /api/v1/chat）并解析返回结构即可。
async function chatRequest(msgs) {
  const base = import.meta.env.VITE_API_BASE || "/api";
  try {
    const res = await fetch(base + "/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: msgs }),
    });
    if (!res.ok) throw new Error("bad status");
    const data = await res.json();
    return typeof data === "string" ? data : data.reply ?? data.content ?? "";
  } catch (e) {
    return mockReply(msgs);
  }
}

function mockReply(msgs) {
  const last = [...msgs].reverse().find((m) => m.role === "user");
  const text = last ? last.content : "";
  return `【模拟回复】你刚才说：「${text || "（空）"}」

我是 Argus 智能体（演示模式）。当前后端对话接口尚未实现，这是前端本地模拟的回复。

待后端接入真实 Agent（LangChain / LangGraph / OpenAI Agents SDK）后，这里将返回真实回答，并支持代码块、列表等富文本渲染。`;
}

// 逐字（打字机）显示，营造大模型生成效果
function typeWriter(msg, text) {
  return new Promise((resolve) => {
    let i = 0;
    const timer = setInterval(() => {
      msg.content += text[i] || "";
      i++;
      scrollToBottom();
      if (i >= text.length) {
        clearInterval(timer);
        msg.streaming = false;
        resolve();
      }
    }, 16);
  });
}

// 将消息解析为「文本 / 代码块」片段，便于富文本渲染
function blocks(m) {
  if (m.streaming) return [{ type: "text", value: m.content }];
  return renderBlocks(m.content);
}

function renderBlocks(text) {
  const out = [];
  const re = /```(\w*)\n?([\s\S]*?)```/g;
  let last = 0;
  let m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push({ type: "text", value: text.slice(last, m.index) });
    out.push({ type: "code", lang: m[1], value: m[2].replace(/\n$/, "") });
    last = re.lastIndex;
  }
  if (last < text.length) out.push({ type: "text", value: text.slice(last) });
  return out;
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, (c) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  }[c]));
}

// 简单富文本：转义 HTML -> 换行 -> **加粗**
function formatText(t) {
  let s = escapeHtml(t);
  s = s.replace(/\n/g, "<br>");
  s = s.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  return s;
}

async function scrollToBottom() {
  await nextTick();
  if (msgBox.value) msgBox.value.scrollTop = msgBox.value.scrollHeight;
}

function autoGrow() {
  if (ta.value) {
    ta.value.style.height = "auto";
    ta.value.style.height = Math.min(ta.value.scrollHeight, 120) + "px";
  }
}
</script>

<style scoped>
.chat {
  height: calc(100vh - 48px);
  display: flex;
  flex-direction: column;
  background: #f7f8fa;
}
.chat-header {
  display: flex;
  align-items: baseline;
  gap: 10px;
  padding: 14px 20px;
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
}
.chat-header .title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}
.chat-header .subtitle {
  font-size: 12px;
  color: #9ca3af;
}
.chat-header .clear {
  margin-left: auto;
  border: 1px solid #e5e7eb;
  background: #fff;
  color: #6b7280;
  border-radius: 8px;
  padding: 4px 10px;
  font-size: 12px;
  cursor: pointer;
}
.chat-header .clear:hover {
  border-color: #4d6bfe;
  color: #4d6bfe;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.empty {
  margin: auto;
  text-align: center;
  color: #6b7280;
}
.empty-icon {
  font-size: 48px;
}
.empty h2 {
  font-size: 22px;
  color: #1f2937;
  margin: 12px 0 6px;
}
.empty p {
  margin: 0 0 18px;
  font-size: 14px;
}
.suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}
.suggestions button {
  border: 1px solid #e5e7eb;
  background: #fff;
  border-radius: 18px;
  padding: 8px 14px;
  font-size: 13px;
  color: #374151;
  cursor: pointer;
}
.suggestions button:hover {
  border-color: #4d6bfe;
  color: #4d6bfe;
}

.msg {
  display: flex;
  gap: 12px;
  width: 100%;
  max-width: 820px;
  margin: 0 auto;
}
.msg.user {
  flex-direction: row-reverse;
}
.avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  color: #fff;
}
.avatar.user {
  background: #4d6bfe;
}
.avatar.assistant {
  background: linear-gradient(135deg, #667eea, #764ba2);
}
.bubble {
  max-width: 100%;
  padding: 12px 14px;
  border-radius: 14px;
  line-height: 1.65;
  font-size: 14px;
  word-break: break-word;
}
.msg.assistant .bubble {
  background: #fff;
  border: 1px solid #eef0f3;
  border-top-left-radius: 4px;
}
.msg.user .bubble {
  background: #4d6bfe;
  color: #fff;
  border-top-right-radius: 4px;
}
.text :deep(strong) {
  font-weight: 600;
}
.code {
  background: #0f172a;
  color: #e2e8f0;
  padding: 12px 14px;
  border-radius: 10px;
  overflow-x: auto;
  font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 13px;
  margin: 6px 0;
}
.typing {
  display: flex;
  gap: 4px;
  padding: 4px 2px;
}
.typing span {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #cbd5e1;
  animation: blink 1.2s infinite;
}
.typing span:nth-child(2) {
  animation-delay: 0.2s;
}
.typing span:nth-child(3) {
  animation-delay: 0.4s;
}
@keyframes blink {
  0%,
  60%,
  100% {
    opacity: 0.3;
  }
  30% {
    opacity: 1;
  }
}

.input-bar {
  display: flex;
  gap: 10px;
  padding: 14px 20px;
  background: #fff;
  border-top: 1px solid #e5e7eb;
  align-items: flex-end;
}
.input-bar textarea {
  flex: 1;
  resize: none;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 10px 12px;
  font-size: 14px;
  font-family: inherit;
  line-height: 1.5;
  max-height: 120px;
  outline: none;
}
.input-bar textarea:focus {
  border-color: #4d6bfe;
}
.send {
  background: #4d6bfe;
  color: #fff;
  border: none;
  border-radius: 12px;
  padding: 0 20px;
  height: 42px;
  font-size: 14px;
  cursor: pointer;
  flex-shrink: 0;
}
.send:disabled {
  background: #c7d0f7;
  cursor: not-allowed;
}
</style>
