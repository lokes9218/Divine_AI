<template>
  <div class="flex" :class="message.role === 'user' ? 'justify-end' : 'justify-start'">
    <div class="chat-bubble" :class="bubbleClass">
      <!-- Avatar and Role -->
      <div class="flex items-start message-header">
        <!-- Optimized Avatar Size -->
        <div class="flex-shrink-0">
          <div class="avatar-container rounded-full overflow-hidden">
            <span v-if="message.role === 'user'" class="avatar-emoji leading-none">🏹</span>
            <img v-else src="/logo.png" alt="AI Sage" class="avatar-img" />
          </div>
        </div>
        
        <div class="flex-1 min-w-0">
          <!-- Message Content -->
          <div class="prose prose-invert prose-sm max-w-none">
            <div class="content-text leading-tight" v-html="formattedContent"></div>
          </div>
        </div>
      </div>
      
      <!-- Assistant Actions Below Content -->
      <div v-if="message.role === 'assistant' && !message.isError" class="mt-4 flex flex-wrap gap-2" style="padding-left: 7rem;">
        <!-- English Audio Button -->
        <button
          @click="$emit('listen-audio', message, 'english')"
          class="listen-btn"
          :class="{ 'playing': isEnglishPlaybackActive, 'generating': isGeneratingEnglishAudio }"
        >
          <svg v-if="isGeneratingEnglishAudio" class="animate-spin h-3.5 w-3.5 text-amber-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <svg v-else-if="!isEnglishPlaybackActive" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
          </svg>
          <svg v-else class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6" />
          </svg>
          <span>{{ isGeneratingEnglishAudio ? 'Engraving...' : (isEnglishPlaybackActive ? 'Pause English' : 'Listen in English') }}</span>
        </button>

        <!-- Tamil Audio Button -->
        <button
          @click="$emit('listen-audio', message, 'tamil')"
          class="listen-btn"
          :class="{ 'playing': isTamilPlaybackActive, 'generating': isGeneratingTamilAudio }"
        >
          <svg v-if="isGeneratingTamilAudio" class="animate-spin h-3.5 w-3.5 text-amber-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <svg v-else-if="!isTamilPlaybackActive" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
          </svg>
          <svg v-else class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6" />
          </svg>
          <span>{{ isGeneratingTamilAudio ? 'Engraving...' : (isTamilPlaybackActive ? 'Pause Tamil' : 'Listen in Tamil') }}</span>
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  message: {
    type: Object,
    required: true
  },
  activeAudioId: {
    type: String,
    default: null
  },
  activeAudioLang: {
    type: String,
    default: null
  },
  isAudioPlaying: {
    type: Boolean,
    default: false
  },
  generatingAudioId: {
    type: String,
    default: null
  },
  generatingAudioLang: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['listen-audio'])

const isEnglishPlaybackActive = computed(() => {
  return props.activeAudioId === props.message.id && props.activeAudioLang === 'english' && props.isAudioPlaying
})

const isTamilPlaybackActive = computed(() => {
  return props.activeAudioId === props.message.id && props.activeAudioLang === 'tamil' && props.isAudioPlaying
})

const isGeneratingEnglishAudio = computed(() => {
  return props.generatingAudioId === props.message.id && props.generatingAudioLang === 'english'
})

const isGeneratingTamilAudio = computed(() => {
  return props.generatingAudioId === props.message.id && props.generatingAudioLang === 'tamil'
})

const bubbleClass = computed(() => {
  if (props.message.role === 'user') {
    return 'user-bubble'
  } else if (props.message.isError) {
    return 'assistant-bubble error-bubble'
  } else {
    return 'assistant-bubble'
  }
})

const formattedContent = computed(() => {
  let content = props.message.content
  
  // Convert newlines to HTML breaks
  content = content.replace(/\n/g, '<br>')
  
  // Simple markdown-like formatting
  content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  content = content.replace(/\*(.*?)\*/g, '<em>$1</em>')
  
  // Convert URLs to links
  content = content.replace(
    /(https?:\/\/[^\s]+)/g,
    '<a href="$1" target="_blank" rel="noopener noreferrer" class="message-link">$1</a>'
  )
  
  return content
})

function formatTime(timestamp) {
  if (!timestamp) return ''
  
  const now = new Date()
  const messageTime = new Date(timestamp)
  const diffInSeconds = Math.floor((now - messageTime) / 1000)
  
  if (diffInSeconds < 60) {
    return messageTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } else if (diffInSeconds < 3600) {
    const minutes = Math.floor(diffInSeconds / 60)
    return `${minutes} min${minutes === 1 ? '' : 's'} ago`
  } else if (diffInSeconds < 86400) {
    const hours = Math.floor(diffInSeconds / 3600)
    return `${hours} hour${hours === 1 ? '' : 's'} ago`
  } else {
    return messageTime.toLocaleString()
  }
}
</script>