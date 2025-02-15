<template>
    <Navbar :roleName="current_user.role" />
    <router-view />
    <h2 class="m-4">Welcome to your profile, @{{ current_user.username }} !</h2>
    <div class="d-flex align-items-center justify-content-center">
        <div class="card w-50 bg-primary-subtle text-primary-emphasis rounded">
            <h5 class="card-header my-1 py-2">User Information</h5>
            <div class="card-body">
                <p><b>Full Name : </b> {{ current_user.fullname }}</p>
                <p><b>Role : </b> {{ current_user.role }}</p>
                <p><b>Address : </b> {{ current_user.address }}</p>
                <p><b>Pincode : </b> {{ current_user.pincode }}</p>
                <p><b>Contact Number : </b> {{ current_user.contact_number }}</p>
                <p><b>Profile Created On : </b> {{ formattedTime(current_user.created_at) }}</p>
            </div>
        </div>
    </div>
    <div class="text-center mt-4">
        <router-link class="btn btn-primary mx-2 px-3" to="/profile/edit">Edit Profile</router-link>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Navbar from '@/components/Navbar.vue';

const router = useRouter();
const current_user = ref({});

const formattedTime = (timeString) => {
    const date = new Date(timeString);
    return date.toLocaleString('en-US', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: true });
};

onMounted(async () => {
    try {
        const jwtToken = localStorage.getItem('token');
        const response = await fetch('http://127.0.0.1:5000/api/profile', {
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
            current_user.value = data.details;
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
});
</script>