<template>
    <br>
    <h1 class="m-3">ServiceSphere</h1>
    <img src="/ServiceSphere.png" class="mx-auto d-block img-logo">
    <br>
    <h2 class="m-3">A-Z Household Services are available here</h2><br>
    <router-link to="/login" class="btn btn-info btn-lg mb-4 px-3 pe-4">
        <i class="bi bi-box-arrow-in-right"></i> Login 
    </router-link>
    <div class="dropdown-center mb-4">
        <button class="btn btn-warning btn-lg px-3 dropdown-toggle" type="button" id="dropdownMenuButton"
            data-bs-toggle="dropdown" aria-expanded="false">
            <i class="bi bi-door-open"></i> Register
        </button>
        <ul class="dropdown-menu text-center" aria-labelledby="dropdownMenuButton">
            <li>
                <router-link class="dropdown-item" to="/register/customer">
                    Register as <b>Customer</b> <i class="bi bi-people-fill"></i>
                </router-link>
            </li>
            <li>
                <router-link class="dropdown-item" to="/register/professional">
                    Register as <b>Professional</b> <i class="bi bi-tools"></i>
                </router-link>
            </li>
        </ul>
    </div>
</template>

<script setup>
import { useAlert } from '@/components/alert.js'
const { showAlert } = useAlert();

showAlert("Welcome to ServiceSphere", "info");
</script>