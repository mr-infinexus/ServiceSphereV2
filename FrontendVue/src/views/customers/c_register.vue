<template>
    <h1 class="m-2">Register as Customer</h1>
    <hr class="border">
    <div class="d-flex align-items-center justify-content-center m-0">
        <div class="col-10 col-lg-6">
            <form @submit.prevent="handleRegisterCustomer">
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label" for="username">Username</label>
                        <input class="form-control" id="username" maxlength="32" minlength="4" v-model="username"
                            placeholder="Username" required type="text" value="">
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label" for="password">Password</label>
                        <input class="form-control" id="password" maxlength="32" minlength="8" v-model="password"
                            placeholder="Password" required type="password" value="">
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label" for="email">Email</label>
                        <input class="form-control" id="email" maxlength="64" minlength="8" v-model="email"
                            placeholder="Email" required type="email" value="">
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label" for="fullname">Full Name</label>
                        <input class="form-control" id="fullname" maxlength="64" minlength="3" v-model="fullname"
                            placeholder="Full Name" required type="text" value="">
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label" for="contact_number">Contact Number</label>
                        <input class="form-control" id="contact_number" max="9999999999" min="1000000000"
                            v-model="contact_number" required type="number" value="">
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label" for="pincode">Pincode</label>
                        <input class="form-control" id="pincode" max="999999" min="100000" v-model="pincode" required
                            type="number" value="">
                    </div>
                    <div class="col-12 mb-3">
                        <label class="form-label" for="address">Address</label>
                        <textarea class="form-control" id="address" v-model="address" required rows="1"
                            value=""></textarea>
                    </div>
                    <div class="text-center my-3">
                        <button class="btn btn-success mx-2 px-3">
                            <i class="bi bi-check2-square me-1"></i>Register
                        </button>
                    </div>
                </div>
            </form>
            <router-link to="/register/professional"><b>Not Customer? Register as Professional</b></router-link><br>
            <router-link to="/login"><b>Already have an account? Login here</b></router-link>
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
const email = ref('');
const fullname = ref('');
const contact_number = ref('');
const address = ref('');
const pincode = ref('');

const handleRegisterCustomer = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/register/customer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username.value,
                password: password.value,
                email: email.value,
                fullname: fullname.value,
                contact_number: contact_number.value,
                address: address.value,
                pincode: pincode.value
            })
        });
        const data = await response.json();
        if (response.ok) {
            showAlert(data.message, "success");
            router.push({ path: '/login' });
        } else {
            showAlert(data.message, "danger");
        }
    } catch (error) {
        console.error('Error during login:', error);
    }
};
</script>