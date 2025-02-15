<template>
    <div>
        <Alert v-if="alert.show" :message="alert.message" :type="alert.type" @close="hideAlert" />
        <router-view></router-view>
    </div>
</template>

<script setup>
import Alert from '@/components/Alert.vue'
import { useAlert } from '@/components/alert.js'

const { alert, hideAlert } = useAlert()
</script>