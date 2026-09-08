<template>
  <!-- Backend Wakeup Screen -->
  <BackendWakeup v-if="!backendReady" />
  
  <!-- Main App -->
  <div v-else class="app-layout">
    <!-- Content Container (for centered layout) -->
    <div class="content-container">
      <!-- Header -->
      <header class="header">
        <div class="header-content">
          <!-- Brand Section (Left) -->
          <div class="header-brand">
            <button @click="clearChat" class="header-brand-link" :disabled="isLoading">
              <h1 class="header-title">
                <img src="/logo.png" alt="Logo" />
                mahabharata wisdom mentor
              </h1>
              <p class="header-subtitle">
                Voyage through the cosmic tapestry of the Great Epic
              </p>
            </button>
          </div>
          
          <!-- Top Navigation (Right on desktop, below brand on mobile) -->
          <nav class="header-nav">
            <a href="#" @click.prevent="openAboutModal" class="nav-link">
              <span class="nav-icon">🕉️</span>
              <span class="nav-text">About</span>
            </a>
            <a href="#" @click.prevent="openDharmaModal" class="nav-link">
              <span class="nav-icon">⚖️</span>
              <span class="nav-text">Dharma</span>
            </a>
            <a href="https://github.com/lokes9218/Divine_AI.git" target="_blank" class="nav-link">
              <span class="nav-icon">🏹</span>
              <span class="nav-text">Wisdom</span>
            </a>
            <a href="https://github.com/lokes9218/Divine_AI.git" target="_blank" class="nav-link">
              <span class="nav-icon">📖</span>
              <span class="nav-text">Repository</span>
            </a>
          </nav>
        </div>
      </header>

      <!-- Main Content -->
      <main class="main-content">
      <!-- Chat Container -->
      <div class="chat-container">
        <!-- Chat Messages -->
        <div ref="chatContainer" class="chat-messages">
          <div v-if="messages.length === 0" class="welcome-message">
            <h3 class="welcome-title">Seek Wisdom from the AI WISDOM MENTOR</h3>
            <p class="welcome-description">
              Journey through the greatest epic ever told. Discover timeless teachings on dharma, explore the depths of human nature, 
              and unravel the mysteries of divine cosmic law through AI-powered insights.
            </p>
            
            <!-- Example Questions Moved Here -->
            <div class="examples-section">
              <p class="examples-title">Divine Inquiries</p>
              <div class="examples-grid">
                <button
                  v-for="example in examples"
                  :key="example"
                  @click="sendMessage(example)"
                  :disabled="isLoading"
                  class="example-button"
                >
                  {{ example }}
                </button>
              </div>
            </div>
          </div>
          
          <div
            v-for="(message, index) in messages"
            :key="index"
            class="message-fade-in"
          >
            <ChatMessage 
              :message="message" 
              :active-audio-id="activeAudioId"
              :active-audio-lang="activeAudioLang"
              :is-audio-playing="isAudioPlaying"
              :generating-audio-id="generatingAudioId"
              :generating-audio-lang="generatingAudioLang"
              @listen-audio="handleListenAudio"
            />
          </div>
          
          <!-- Typing Indicator -->
          <div v-if="isTyping" class="typing-indicator">
            <div class="typing-dots">
              <div class="typing-dot"></div>
              <div class="typing-dot"></div>
              <div class="typing-dot"></div>
            </div>
            <div class="typing-message" :class="{ changing: isMessageChanging }">
              <span style="color: var(--accent-cyan);" :key="currentLoadingMessage">{{ currentLoadingMessage }}</span>
            </div>
          </div>
        </div>

        <!-- Input Section -->
        <div class="chat-input-section">
          
          <!-- Message Input -->
          <form @submit.prevent="handleSubmit" class="input-form">
            <input
              v-model="currentMessage"
              type="text"
              placeholder="Ask about the Mahabharata..."
              :disabled="isLoading"
              class="input-field"
            />
            <button
              type="submit"
              :disabled="isLoading || !currentMessage.trim()"
              class="btn-primary"
            >
              <span v-if="isLoading">Channeling...</span>
              <span v-else>Seek Wisdom</span>
            </button>
          </form>

          <!-- Clear Chat Button -->
          <div v-if="messages.length > 0" style="text-align: center;">
            <button
              @click="clearChat"
              :disabled="isLoading"
              class="btn-secondary"
            >
              🗑️ Clear Chat
            </button>
          </div>
        </div>
      </div>

      <!-- Audio Player (Hidden) -->
      <audio 
        ref="audioPlayer" 
        class="hidden" 
        @ended="audioEnded"
        @play="handleAudioPlay"
        @pause="handleAudioPause"
      >
        Your browser does not support the audio element.
      </audio>
    </main>
    </div>
    <!-- End Content Container -->

    <!-- Footer (Full Width) -->
    <footer class="app-footer">
      <div class="footer-content">
        <div class="footer-credits">
          <span class="footer-powered">Powered by GenAI • Built with ❤️ for seekers of ancient wisdom</span>
          <div class="footer-copyright">
            © 2026 mahabharata wisdom mentor • Built with ❤️ by Lokeswaran S
          </div>
        </div>
      </div>
    </footer>

    <!-- About Modal -->
    <div v-if="showAboutModal" class="modal-overlay" @click="closeAboutModal">
      <div class="modal-container" @click.stop>
        <button class="modal-close-btn" @click="closeAboutModal">
          <span class="close-icon">✕</span>
        </button>
        
        <div class="modal-content">
          <div class="modal-header">
            <div class="modal-brand">
              <img :src="logoImage" alt="Mahabharata AI Logo" class="modal-logo" />
              <div class="modal-brand-text">
                <h2 class="modal-title">mahabharata wisdom mentor</h2>
                <p class="modal-tagline">Dive into the timeless wisdom of an ancient Indian epic</p>
              </div>
            </div>
          </div>
          
          <div class="modal-body">
            <!-- Main Sections Grid -->
            <div class="main-sections">
              <div class="section-card">
                <div class="section-icon">🌟</div>
                <h3 class="section-title">The Vision</h3>
                <p class="section-text">
                  Journey through the cosmic tapestry of the Great Epic with our AI-powered sage. 
                  This platform brings the timeless wisdom of the Mahabharata to the digital age, 
                  making the profound teachings accessible to seekers worldwide.
                </p>
              </div>
              
              <div class="section-card">
                <div class="section-icon">⚔️</div>
                <h3 class="section-title">The Epic</h3>
                <p class="section-text">
                  The Mahabharata, composed by sage Vyasa, is not just a story of war between 
                  cousins—it's a comprehensive guide to dharma, karma, and the complexities of 
                  human nature. With over 100,000 verses, it stands as the world's longest epic poem.
                </p>
              </div>
              
              <div class="section-card">
                <div class="section-icon">🎯</div>
                <h3 class="section-title">The Purpose</h3>
                <p class="section-text">
                  In an age of moral complexity, the Mahabharata's teachings remain remarkably 
                  relevant. This AI WISDOM MENTOR serves as a bridge between ancient wisdom and modern 
                  inquiries, helping you navigate life's challenges through dharmic understanding.
                </p>
              </div>
            </div>
            
            <!-- Tech Section (Compact) -->
            <div class="tech-section">
              <div class="tech-header">
                <span class="tech-header-icon">⚡</span>
                <span class="tech-header-title">Powered By</span>
                <span class="tech-header-text">
                  Gemini intelligence, Neo4j knowledge graph, Sarvam AI's Indic support for translation and text-to-speech, and modern AI engineering unite to deliver fast, contextual answers.
                </span>
              </div>
              <div class="tech-badges">
                <span class="tech-badge">
                  Gemini 3.6 Flash
                </span>
                <span class="tech-badge">
                  Neo4j
                </span>
                <span class="tech-badge">
                  Sarvam AI
                </span>
              </div>
            </div>
            
            <!-- Credits & Links -->
            <div class="credits-section">
              <div class="credits-content">
                <div class="credits-text">
                  <p>🙏 Created with reverence for the sacred text and gratitude to all the scholars, 
                  translators, and sages who have preserved this wisdom across millennia.</p>
                </div>
                <div class="credits-links">
                  <p>💻 <a href="https://github.com/lokes9218/Divine_AI.git" target="_blank" class="credit-link">View Source Code</a></p>
                  <p class="credits-author">Built with ❤️ by <a href="https://github.com/lokes9218/Divine_AI.git" target="_blank" class="credit-link">Lokeswaran S</a></p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Dharma Modal -->
    <div v-if="showDharmaModal" class="modal-overlay" @click="closeDharmaModal">
      <div class="modal-container" @click.stop>
        <button class="modal-close-btn" @click="closeDharmaModal">
          <span class="close-icon">✕</span>
        </button>
        
        <div class="modal-content">
          <div class="modal-header">
            <div class="modal-brand">
              <div class="dharma-symbol">⚖️</div>
              <div class="modal-brand-text">
                <h2 class="modal-title">Dharmic Wisdom</h2>
                <p class="modal-tagline">Timeless teachings from the Great Epic</p>
              </div>
            </div>
          </div>
          
          <div class="modal-body">
            <!-- Dharma Sections -->
            <div class="main-sections">
              <div class="section-card">
                <div class="section-icon">📿</div>
                <h3 class="section-title">What is Dharma?</h3>
                <p class="section-text">
                  Dharma is righteous duty, moral law, and the path of virtue. In the Mahabharata, 
                  it represents the cosmic order that sustains life and society. Each person must 
                  follow their dharma according to their role, circumstances, and inner nature.
                </p>
              </div>
              
              <div class="section-card">
                <div class="section-icon">⚡</div>
                <h3 class="section-title">Moral Dilemmas</h3>
                <p class="section-text">
                  The epic presents complex ethical choices: Arjuna's reluctance to fight family, 
                  Yudhishthira's struggle between truth and compassion, and Karna's conflict between 
                  loyalty and justice. These dilemmas teach us that dharma is often contextual.
                </p>
              </div>
              
              <div class="section-card">
                <div class="section-icon">💎</div>
                <h3 class="section-title">Timeless Teachings</h3>
                <p class="section-text">
                  "Better is one's own dharma, though imperfectly performed, than the dharma of 
                  another well performed." Krishna's teachings emphasize duty over desire, 
                  righteousness over convenience, and the eternal over the temporal.
                </p>
              </div>
              
              <div class="section-card">
                <div class="section-icon">🎆</div>
                <h3 class="section-title">Karma & Action</h3>
                <p class="section-text">
                  Every action has consequences that extend beyond the immediate. The Mahabharata 
                  teaches that righteous action, performed without attachment to results, 
                  purifies the soul and upholds the cosmic order of dharma.
                </p>
              </div>
              
              <div class="section-card">
                <div class="section-icon">🪔</div>
                <h3 class="section-title">Truth & Sacrifice</h3>
                <p class="section-text">
                  Truth (Satya) and sacrifice (Yajna) are pillars of dharmic life. Yudhishthira's 
                  commitment to truth, even at great personal cost, and the sacrifices made by 
                  noble characters demonstrate the price and power of righteousness.
                </p>
              </div>
              
              <div class="section-card">
                <div class="section-icon">🌟</div>
                <h3 class="section-title">Modern Relevance</h3>
                <p class="section-text">
                  Today's ethical challenges mirror those in the Mahabharata: balancing personal 
                  ambition with social responsibility, choosing truth over convenience, and finding 
                  the courage to do what is right despite difficult consequences.
                </p>
              </div>
            </div>
            
            <!-- Dharmic Quote -->
            <div class="dharma-quote-section">
              <div class="dharma-quote">
                <span class="quote-mark">"</span>
                <span class="quote-text">धर्मो रक्षति रक्षितः</span>
                <span class="quote-mark">"</span>
              </div>
              <div class="quote-translation">"Dharma protects those who protect it"</div>
              <div class="quote-attribution">— Mahabharata</div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'

// Logo from public folder so Rollup/Vite resolve it reliably in production
const logoImage = '/logo.png'

// Generate UUID without external library
function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0
    const v = c == 'x' ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
}

// Loading message rotation with smooth transitions
function startLoadingMessages() {
  let index = 0
  currentLoadingMessage.value = loadingMessages.value[0]
  
  loadingInterval.value = setInterval(() => {
    // Start exit animation
    isMessageChanging.value = true
    
    // Change message after exit animation
    setTimeout(() => {
      index = (index + 1) % loadingMessages.value.length
      currentLoadingMessage.value = loadingMessages.value[index]
      isMessageChanging.value = false
    }, 300) // Match exit animation duration
    
  }, 2500) // Slightly longer to account for animation time
}

function stopLoadingMessages() {
  if (loadingInterval.value) {
    clearInterval(loadingInterval.value)
    loadingInterval.value = null
  }
  currentLoadingMessage.value = ''
  isMessageChanging.value = false
}

// Reactive data
const messages = ref([])
const currentMessage = ref('')
const isLoading = ref(false)
const isTyping = ref(false)
const chatContainer = ref(null)
const audioPlayer = ref(null)
const sessionId = ref('')
const showAboutModal = ref(false)
const showDharmaModal = ref(false)

// Loading messages system
const loadingMessages = ref([
  'AI WISDOM MENTOR is recalling....',
  'Consulting the ancient texts....',
  'Seeking wisdom from the cosmos....',
  'Channeling dharmic insights....',
  'Unraveling the threads of destiny....',
  'Drawing from eternal knowledge....',
  'Contemplating the great epic....',
  'Awakening ancient memories....',
  'Invoking the wisdom of sages....',
  'Traversing the cosmic library....'
])
const currentLoadingMessage = ref('')
const loadingInterval = ref(null)
const isMessageChanging = ref(false)

// Watch for messages change to scroll to bottom
watch(messages, () => {
  scrollToBottom()
}, { deep: true })

// Watch for typing state to scroll
watch(isTyping, (val) => {
  if (val) {
    scrollToBottom()
  }
})

// Audio playback state
const activeAudioId = ref(null)
const activeAudioLang = ref(null)
const isAudioPlaying = ref(false)
const generatingAudioId = ref(null)
const generatingAudioLang = ref(null)

// Configuration
const config = useRuntimeConfig()
const API_BASE = config.public.apiBase

// Example questions
const examples = ref([])

// Backend health check state
const backendReady = ref(false)

// Check backend health and wait until it's responsive
async function checkBackendHealth() {
  const maxRetries = 60 // 60 attempts * 2 seconds = 2 minutes max
  let retryCount = 0
  
  const BACKEND_HEALTH_URL = 'http://127.0.0.1:8001'

  while (retryCount < maxRetries) {
    try {
      const response = await fetch(BACKEND_HEALTH_URL, {
        method: 'GET',
        headers: {
          'Accept': 'application/json'
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        if (data.message === 'mahabharata wisdom mentor - Ultra Optimized') {
          backendReady.value = true
          return true
        }
      }
    } catch (error) {
      console.log(`Backend health check attempt ${retryCount + 1} failed, retrying...`)
    }
    
    retryCount++
    await new Promise(resolve => setTimeout(resolve, 2000))
  }
  
  console.warn('Backend health check exceeded max retries, showing app anyway')
  backendReady.value = true
  return false
}

// Initialize session
onMounted(async () => {
  await checkBackendHealth()
  sessionId.value = generateUUID()
  await fetchExamples()
  document.addEventListener('keydown', handleKeyDown)
})

// Watch for messages changes and auto-scroll
watch(messages, async () => {
  await scrollToBottom()
}, { deep: true })

// Cleanup event listener
onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
  stopLoadingMessages()
})

// Handle ESC key press
function handleKeyDown(event) {
  if (event.key === 'Escape') {
    if (showAboutModal.value) {
      closeAboutModal()
    } else if (showDharmaModal.value) {
      closeDharmaModal()
    }
  }
}

// Modal control functions
function openAboutModal() {
  showAboutModal.value = true
  document.body.style.overflow = 'hidden'
}

function closeAboutModal() {
  showAboutModal.value = false
  document.body.style.overflow = 'auto'
}

// Dharma Modal control functions
function openDharmaModal() {
  showDharmaModal.value = true
  document.body.style.overflow = 'hidden'
}

function closeDharmaModal() {
  showDharmaModal.value = false
  document.body.style.overflow = 'auto'
}

// Fetch example questions
async function fetchExamples() {
  try {
    const response = await fetch(`${API_BASE}/examples`)
    const data = await response.json()
    examples.value = data.examples.slice(0, 6)
  } catch (error) {
    console.error('Failed to fetch examples:', error)
    examples.value = [
       
            "Who was Satyaki?",
            "Why did the Pandavas have to go live in the forest for 12 years?",
            "Why was Arjuna considered an unbeatable and undefeated warrior?",
            "What was the role of Krishna during the Kurukshetra war? Did he fight?",
            "What were all the battles between Karna and Arjuna, and who won or lost each one?",
            "What were Arjuna’s greatest battles?",
            "What was Draupadi’s greatest strength?",
            "Why did Bhishma take a vow of celibacy, and how did that impact the throne of Hastinapur?",
            "How powerful was Abhimanyu against twenty warriors?",
        ]
  }
}

// Handle form submission
async function handleSubmit() {
  if (!currentMessage.value.trim() || isLoading.value) return
  await sendMessage(currentMessage.value)
  currentMessage.value = ''
}

// Send message to API
async function sendMessage(message) {
  if (isLoading.value) return
  
  isLoading.value = true
  isTyping.value = true
  startLoadingMessages()
  
  messages.value.push({
    id: generateUUID(),
    role: 'user',
    content: message,
    timestamp: new Date()
  })
  
  await scrollToBottom()
  
  try {
    const response = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: message,
        session_id: sessionId.value
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    
    const assistantMessage = {
      id: generateUUID(),
      role: 'assistant',
      content: data.message,
      timestamp: new Date(),
      sources: data.sources || [],
      totalTokens: data.total_tokens || 0,
      timeTaken: data.time_taken || 0,
      model: data.model || 'gemini-3.6-flash',
      audioUrls: {}
    }
    messages.value.push(assistantMessage)
    
    sessionId.value = data.session_id
    
  } catch (error) {
    console.error('Error sending message:', error)
    messages.value.push({
      role: 'assistant',
      content: "I'm sorry, there was an error processing your request. Please try again.",
      timestamp: new Date(),
      isError: true
    })
  } finally {
    isLoading.value = false
    isTyping.value = false
    stopLoadingMessages()
    await scrollToBottom()
  }
}

// Handle audio generation and playback for English and Tamil
async function handleListenAudio(message, lang, autoplay = true) {
  if (!message.content || (generatingAudioId.value === message.id && generatingAudioLang.value === lang)) return
  
  if (!message.audioUrls) {
    message.audioUrls = {}
  }

  if (message.audioUrls[lang]) {
    if (activeAudioId.value === message.id && activeAudioLang.value === lang) {
      if (autoplay) toggleAudio()
    } else {
      activeAudioId.value = message.id
      activeAudioLang.value = lang
      audioPlayer.value.src = message.audioUrls[lang]
      if (autoplay) {
        audioPlayer.value.play()
        isAudioPlaying.value = true
      }
    }
    return
  }

  try {
    generatingAudioId.value = message.id
    generatingAudioLang.value = lang

    const endpoint = lang === 'tamil' ? `${API_BASE}/audio/tamil` : `${API_BASE}/audio/english`
    
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: message.content
      })
    })
    
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
    
    const audioBlob = await response.blob()
    const audioUrl = URL.createObjectURL(audioBlob)
    
    message.audioUrls[lang] = audioUrl
    
    if (autoplay && audioPlayer.value) {
      activeAudioId.value = message.id
      activeAudioLang.value = lang
      audioPlayer.value.src = audioUrl
      audioPlayer.value.play()
      isAudioPlaying.value = true
    }
    
  } catch (error) {
    console.error(`Error generating ${lang} audio:`, error)
    alert(`Sorry, there was an error generating the ${lang} audio.`)
    activeAudioId.value = null
    activeAudioLang.value = null
  } finally {
    generatingAudioId.value = null
    generatingAudioLang.value = null
  }
}

function toggleAudio() {
  if (!audioPlayer.value) return
  
  if (audioPlayer.value.paused) {
    audioPlayer.value.play()
    isAudioPlaying.value = true
  } else {
    audioPlayer.value.pause()
    isAudioPlaying.value = false
  }
}

function handleAudioPlay() {
  isAudioPlaying.value = true
}

function handleAudioPause() {
  isAudioPlaying.value = false
}

// Audio ended event
function audioEnded() {
  isAudioPlaying.value = false
  activeAudioId.value = null
  activeAudioLang.value = null
}

// Clear chat
async function clearChat() {
  if (isLoading.value) return
  
  try {
    await fetch(`${API_BASE}/chat/${sessionId.value}`, {
      method: 'DELETE'
    })
    
    messages.value = []
    sessionId.value = generateUUID()
    
  } catch (error) {
    console.error('Error clearing chat:', error)
    // Clear locally even if API call fails
    messages.value = []
    sessionId.value = generateUUID()
  }
}

// Scroll to bottom
async function scrollToBottom() {
  await nextTick()
  await new Promise(resolve => setTimeout(resolve, 50)) // Small delay for DOM updates
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}
</script>