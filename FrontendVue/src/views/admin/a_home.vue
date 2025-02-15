<template>
    <Navbar :roleName="'admin'" />
    <router-view />
    <div>
        <h1 class="m-3">Hello @admin</h1>
        <hr class="border">
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAlert } from '@/components/alert.js'
import Navbar from '@/components/Navbar.vue';

const router = useRouter();
const { showAlert } = useAlert();

const current_user = ref({});

onMounted(async () => {
    try {
        const jwtToken = localStorage.getItem('token');
        const response = await fetch('http://127.0.0.1:5000/api/whoami', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${jwtToken}`
            }
        });
        const data = await response.json();
        if (!response.ok) {
            router.push({ path: '/' });
        }
        if (response.ok) {
            current_user.value = data.current_user;
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
});
</script>