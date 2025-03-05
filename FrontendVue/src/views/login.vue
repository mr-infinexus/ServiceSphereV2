<template>
    <h1 class="m-3">Login</h1>
    <hr class="border">
    <div class="d-flex align-items-center justify-content-center my-3">
        <div class="col-8">
            <form @submit.prevent="handleLogin">
                <div class="row flex-column align-items-center">
                    <div class="col-md-6">
                        <label class="form-label" for="username">Username</label>
                        <input class="form-control" id="username" maxlength="32" minlength="4" v-model="username"
                            placeholder="Username" required type="text" /><br>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label" for="password">Password</label>
                        <input class="form-control" id="password" maxlength="32" minlength="8" v-model="password"
                            placeholder="Password" required type="password" /><br>
                    </div>
                    <div class="text-center mt-2">
                        <button class="btn btn-success mx-2 px-3">
                            <i class="bi bi-check2-circle me-1"></i>Login
                        </button>
                    </div>
                </div>
            </form>
            <br>
            <h6>Don't have an account? Register now !</h6>
            <router-link to="/register/customer"><b>Register as Customer</b></router-link><br>
            <router-link to="/register/professional"><b>Register as Professional</b></router-link>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAlert } from '@/components/alert.js'

const router = useRouter();
const { showAlert } = useAlert();
const username = ref('');
const password = ref('');

const handleLogin = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username.value,
                password: password.value
            })
        });
        const data = await response.json();
        if (response.ok) {
            showAlert(data.message, "success");
            localStorage.setItem('token', data.token);
            const goto = '/' + data.role;
            router.push({ path: goto });
        } else {
            showAlert(data.message, "danger");
        }
    } catch (error) {
        console.error('Error during login:', error);
    }
};
</script>
