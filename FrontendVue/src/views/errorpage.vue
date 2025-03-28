<template>
    <div class="d-flex align-items-center justify-content-center min-vh-100">
        <div class="text-center">
            <h1 class="mb-2 pb-1" style="font-size: 400%;">404</h1>
            <h1 class="my-2 py-1">Error!</h1>
            <h1 class="my-2 py-1">Page Not Found 😵</h1><br>
            <h3 class="mt-4">Redirecting in {{ countdown }}...</h3>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const countdown = ref(3);

onMounted(() => {
    const interval = setInterval(() => {
        if (countdown.value > 0) {
            countdown.value--;
        } else {
            clearInterval(interval);
            router.push('/');
        }
    }, 1000);
});
</script>