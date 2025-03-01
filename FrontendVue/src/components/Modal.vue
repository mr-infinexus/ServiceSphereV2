<template>
    <div v-if="modelValue" class="modal fade show d-block" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
            <div class="modal-content">
                <div :class="`modal-header bg-${type} py-2`">
                    <h5 class="modal-title text-black">
                        <slot name="header"></slot>
                    </h5>
                    <button type="button" class="btn-close" @click="closeModal"></button>
                </div>

                <div class="modal-body py-2">
                    <slot></slot>
                </div>

                <div class="modal-footer py-1">
                    <button v-if="confirmButton" type="submit" :class="`btn btn-${type} btn-sm`" @click="confirmModal">
                        {{ confirmButton }}
                    </button>
                    <button type="button" class="btn btn-secondary btn-sm" @click="closeModal">
                        {{ cancelButton }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'

const props = defineProps({
    modelValue: {
        type: Boolean,
        required: true
    },
    type: {
        type: String,
        default: 'info',
        validator: (value) => ['success', 'danger', 'warning', 'info'].includes(value)
    },
    cancelButton: {
        type: String,
        default: 'Cancel'
    },
    confirmButton: {
        type: String,
        default: ''
    },
    closeOnBackdrop: {
        type: Boolean,
        default: true
    }
})

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel'])

const closeModal = () => {
    emit('update:modelValue', false)
    emit('cancel')
};

const confirmModal = () => {
    emit('confirm')
    emit('update:modelValue', false)
};

if (props.closeOnBackdrop) {
    const handleBackdropClick = (event) => {
        if (event.target.classList.contains('modal')) {
            closeModal()
        }
    }

    onMounted(() => {
        document.addEventListener('click', handleBackdropClick)
    })

    onUnmounted(() => {
        document.removeEventListener('click', handleBackdropClick)
    })
};
</script>

<style scoped>
.modal {
    background-color: rgba(0, 0, 0, 0.4);
}

.modal-body {
    max-height: 60vh;
}
</style>