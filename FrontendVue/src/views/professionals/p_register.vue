<template>
    <h1 class="m-3">Register as Professional</h1>
    <hr class="border">
    <div class="d-flex align-items-center justify-content-center my-2">
        <div class="col-10 col-lg-6">
            <form @submit.prevent="handleRegisterProfessional">
                <div class="row">
                    <div class="col-md-6">
                        <label class="form-label" for="username">Username</label>
                        <input class="form-control" id="username" maxlength="32" minlength="4" v-model="username"
                            placeholder="Username" required type="text" value=""><br>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label" for="password">Password</label>
                        <input class="form-control" id="password" maxlength="32" minlength="8" v-model="password"
                            placeholder="Password" required type="password" value=""><br>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label" for="fullname">Full Name</label>
                        <input class="form-control" id="fullname" maxlength="64" minlength="3" v-model="fullname"
                            placeholder="Full Name" required type="text" value=""><br>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label" for="contact_number">Contact Number</label>
                        <input class="form-control" id="contact_number" max="9999999999" min="1000000000"
                            v-model="contact_number" required type="number" value=""><br>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label" for="service_type">Service Name</label>
                        <select class="form-select" id="service_type" v-model="service_type" required>
                            <option value="">Choose an option</option>
                            <option :value="service.id" v-for="service in services" :key="service.id">
                                {{ service.name }}
                            </option>
                        </select><br>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label" for="experience">Experience (in Years)</label>
                        <input class="form-control" id="experience" max="60" min="0" v-model="experience" required
                            type="number" value=""><br>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label" for="address">Address</label>
                        <input class="form-control" id="address" maxlength="256" minlength="3" v-model="address"
                            required type="text" value=""><br>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label" for="pincode">Pincode</label>
                        <input class="form-control" id="pincode" max="999999" min="100000" v-model="pincode" required
                            type="number" value=""><br>
                    </div>
                    <div class="text-center mt-2">
                        <input class="btn btn-success mx-2 px-3" id="submit" type="submit"
                            value="Register as Professional">
                    </div>
                </div>
            </form>
            <br>
            <router-link to="/register/customer">Register As Customer</router-link><br>
            <router-link to="/login">Already have an account? Login here</router-link>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAlert } from '@/components/alert.js'

const router = useRouter();
const { showAlert } = useAlert();

const username = ref('');
const password = ref('');
const fullname = ref('');
const contact_number = ref('');
const service_type = ref('');
const experience = ref('');
const address = ref('');
const pincode = ref('');

const services = ref([]);

onMounted(async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/services');
        const data = await response.json();
        if (response.ok) {
            services.value = data.services;
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
});

const handleRegisterProfessional = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/register/professional', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username.value,
                password: password.value,
                fullname: fullname.value,
                contact_number: contact_number.value,
                service_type: service_type.value,
                experience: experience.value,
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