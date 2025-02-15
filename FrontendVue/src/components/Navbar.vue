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
                        <router-link class="nav-link active fw-semibold" aria-current="page"
                            :to="'/' + roleName">Home</router-link>
                    </li>
                    <li class="nav-item mx-1">
                        <router-link class="nav-link active fw-semibold" aria-current="page"
                            :to="'/' + roleName + '/search'">Search</router-link>
                    </li>
                    <li class="nav-item mx-2">
                        <router-link class="nav-link active fw-semibold" aria-current="page"
                            :to="'/' + roleName + '/summary'">Summary</router-link>
                    </li>
                </ul>
                <ul class="navbar-nav ml-auto mx-2 mb-lg-0">
                    <li class="nav-item">
                        <router-link class="btn btn-info m-2 px-2" aria-current="page" to="/profile">
                            Profile
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <button class="btn btn-outline-danger my-2 px-2" @click="handleLogoutClick">
                            Logout
                        </button>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
    roleName: {
        type: String,
        required: true
    }
});

const router = useRouter();
const handleLogoutClick = () => {
    if (confirm('Are you sure you want to log out?')) {
        localStorage.removeItem('token');
        router.push('/');
    }
};
</script>