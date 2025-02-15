<template>
    <br>
    <h1 class="m-3">ServiceSphere</h1>
    <img src="/ServiceSphere.png" class="mx-auto d-block img-logo">
    <br>
    <h2 class="m-3">A-Z Household Services are available here</h2><br>
    <router-link to="/login" class="btn btn-info btn-lg mb-4 px-3">Login</router-link>
    <div class="dropdown-center mb-4">
        <button class="btn btn-warning btn-lg px-3 dropdown-toggle" type="button" id="dropdownMenuButton"
            data-bs-toggle="dropdown" aria-expanded="false">
            Register
        </button>
        <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
            <li>
                <router-link class="dropdown-item" to="/register/customer">Register As Customer</router-link>
            </li>
            <li>
                <router-link class="dropdown-item" to="/register/professional">Register As Professional</router-link>
            </li>
        </ul>
    </div>
</template>

<script setup>
import { useAlert } from '@/components/alert.js'
const { showAlert } = useAlert();

showAlert("Welcome to ServiceSphere", 'success');
</script>