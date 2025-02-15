<template>
    <div v-if="isVisible" :class="['alert', `alert-${type}`, 'alert-dismissible']" role="alert">
        <span>{{ message }}</span>
        <button type="button" class="btn-close" aria-label="Close" @click="closeAlert"></button>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
    type: {
        type: String,
        default: 'info',
        validator: (value) => ['success', 'danger', 'warning', 'info'].includes(value)
    },
    message: {
        type: String,
        required: true
    }
})

const emit = defineEmits(['close'])
const isVisible = ref(true)
let timer = null

onMounted(() => {
    startTimer()
})

function startTimer() {
    if (timer) {
        clearTimeout(timer)
    }
    timer = setTimeout(() => {
        closeAlert()
    }, 4000)
}

function closeAlert() {
    isVisible.value = false
    emit('close')
}

onUnmounted(() => {
    if (timer) {
        clearTimeout(timer)
    }
})
</script>