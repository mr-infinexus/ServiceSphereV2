<template>
    <div v-if="isVisible" :class="`alert alert-${type} alert-dismissible p-0`" role="alert">
        <div class="d-flex align-items-center p-1">
            <i :class="iconClass" class="mx-2"></i>{{ message }}
            <button type="button" class="btn py-0" aria-label="Close" @click="closeAlert">
                <i class="bi bi-x-lg"></i>
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

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

const iconClass = computed(() => {
    const icons = {
        success: 'bi bi-check-circle-fill',
        danger: 'bi bi-exclamation-triangle-fill',
        warning: 'bi bi-exclamation-circle-fill',
        info: 'bi bi-info-circle-fill'
    }
    return icons[props.type]
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