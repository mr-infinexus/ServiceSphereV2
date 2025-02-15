import { reactive } from 'vue'

const alert = reactive({
    show: false,
    message: '',
    type: 'info'
})

export function useAlert() {
    const showAlert = (message, type = 'info') => {
        alert.message = message
        alert.type = type
        alert.show = true
    }

    const hideAlert = () => {
        alert.show = false
    }

    return {
        alert,
        showAlert,
        hideAlert
    }
}