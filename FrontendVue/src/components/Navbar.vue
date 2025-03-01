<template>
    <nav class="navbar navbar-expand-lg bg-primary-subtle text-primary-emphasis p-1 mb-2 rounded">
        <div class="container-fluid px-1">
            <router-link class="navbar-brand m-1" to="/">
                <img src="/ServiceSphere.png" class="nav-logo"><b>ServiceSphere</b>
            </router-link>
            <button class="navbar-toggler px-1" type="button" data-bs-toggle="collapse"
                data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false"
                aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavDropdown">
                <ul class="navbar-nav me-auto mx-2 mb-lg-0">
                    <li class="nav-item mx-2">
                        <router-link class="nav-link active fw-semibold" :to="'/' + roleName">
                            <i class="bi bi-house"></i> Home
                        </router-link>
                    </li>
                    <li class="nav-item mx-1">
                        <router-link class="nav-link active fw-semibold" :to="'/' + roleName + '/search'">
                            <i class="bi bi-search"></i> Search
                        </router-link>
                    </li>
                    <li class="nav-item mx-2">
                        <router-link class="nav-link active fw-semibold" :to="'/' + roleName + '/summary'">
                            <i class="bi bi-file-earmark-bar-graph"></i> Summary
                        </router-link>
                    </li>
                </ul>
                <ul class="navbar-nav ml-auto mx-2 mb-lg-0">
                    <li class="nav-item">
                        <router-link class="btn btn-info m-1 px-2" to="/profile">
                            <i class="bi bi-person-circle"></i> Profile
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <button class="btn btn-outline-danger m-1 px-2" @click="logoutModal = true">
                            Logout <i class="bi bi-box-arrow-right"></i>
                        </button>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <Modal v-model="logoutModal" type="danger" confirm-button="Logout" @confirm="handleLogout">
        <template #header>Logout Confirmation</template>
        <p class="m-2">Are you sure you want to log out?</p>
    </Modal>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Modal from '@/components/Modal.vue';

const props = defineProps({
    roleName: {
        type: String,
        required: true
    }
});

const logoutModal = ref(false);
const router = useRouter();
const handleLogout = () => {
    localStorage.removeItem('token');
    router.push('/');
};
</script>