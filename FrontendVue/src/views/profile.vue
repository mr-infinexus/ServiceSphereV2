<template>
    <Navbar :roleName="current_user.role" />
    <router-view />
    <h2 class="m-4">Welcome to your profile, @{{ current_user.username }} !</h2>
    <div class="d-flex align-items-center justify-content-center">
        <div class="card bg-primary-subtle text-primary-emphasis rounded">
            <h5 class="card-header py-3">User Information</h5>
            <div class="card-body px-5">
                <p class="fs-5"><b>{{ current_user.fullname }}</b></p>
                <p><i class="bi bi-envelope-at-fill fs-5 me-1"></i> {{ current_user.email }}</p>
                <p v-if="current_user.role === 'professional'">
                    <i class="bi bi-tools fs-5 me-1"></i> {{ current_user.service_name }}
                </p>
                <p v-if="current_user.role === 'professional'">
                    <i class="bi bi-person-fill-gear fs-5 me-1"></i> {{ current_user.experience }} Years
                </p>
                <p><i class="bi bi-geo-alt-fill fs-5 me-1"></i> {{ current_user.address }}</p>
                <p><i class="bi bi-geo-fill fs-5 me-1"></i> {{ current_user.pincode }}</p>
                <p><i class="bi bi-telephone-fill fs-5 me-1"></i> {{ current_user.contact_number }}</p>
                <p><b>Profile Created On : </b> {{ formattedTime(current_user.created_at) }}</p>
            </div>
        </div>
    </div>
    <div class="text-center mt-4">
        <button type="button" class="btn btn-primary mx-2 px-3" @click="showEditProfileModal">
            <i class="bi bi-pencil-square"></i> Edit
        </button>
    </div>
    <Modal v-model="editProfileModal" confirm-button="Confirm" @submit="editProfile">
        <template #header>Edit Profile</template>
        <div class="row d-flex align-items-center justify-content-center bg-primary-subtle m-1 py-2">
            <div class="col-11 mb-2">
                <label class="form-label text-black" for="fullname">Full Name</label>
                <input class="form-control" id="fullname" maxlength="100" minlength="2" v-model="fullname" required=""
                    type="text">
            </div>
            <div class="col-11 mb-2">
                <label class="form-label text-black" for="email">Email</label>
                <input class="form-control" id="email" maxlength="64" minlength="8" v-model="email" placeholder="Email"
                    required="" type="email">
            </div>
            <div class="col-11 mb-2" v-if="current_user.role === 'professional'">
                <label class="form-label text-black" for="experience">Experience (in Years)</label>
                <input class="form-control" id="experience" max="60" min="0" v-model="experience" required=""
                    type="number">
            </div>
            <div class="col-11 mb-2">
                <label class="form-label text-black" for="address">Address</label>
                <textarea class="form-control" id="address" v-model="address" maxlength="128" required=""
                    rows="1"></textarea>
            </div>
            <div class="col-11 mb-2">
                <label class="form-label text-black" for="pincode">Pincode</label>
                <input class="form-control" id="pincode" max="999999" min="100000" v-model="pincode" required=""
                    type="number">
            </div>
            <div class="col-11 mb-3">
                <label class="form-label text-black" for="contact_number">Contact Number</label>
                <input class="form-control" id="contact_number" max="9999999999" min="1000000000"
                    v-model="contact_number" required="" type="number">
            </div>
        </div>
    </Modal>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAlert } from '@/components/alert.js';
import Modal from '@/components/Modal.vue';
import Navbar from '@/components/Navbar.vue';

const router = useRouter();
const { showAlert } = useAlert();

const current_user = ref({ role: localStorage.getItem('role') });
const editProfileModal = ref(false);
const fullname = ref();
const email = ref();
const experience = ref();
const address = ref();
const pincode = ref();
const contact_number = ref();

const formattedTime = (timeString) => {
    const date = new Date(timeString);
    return date.toLocaleString('en-IN', { dateStyle: 'short', timeStyle: 'short' });
};

const fetchAllData = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/profile/${localStorage.getItem('username')}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const data = await response.json();
        if (response.ok) {
            current_user.value = data.details;
        } else {
            router.push({ path: '/' });
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

onMounted(async () => {
    await fetchAllData();
});

const showEditProfileModal = async () => {
    fullname.value = current_user.value.fullname;
    email.value = current_user.value.email;
    experience.value = current_user.value.experience;
    address.value = current_user.value.address;
    pincode.value = current_user.value.pincode;
    contact_number.value = current_user.value.contact_number;
    editProfileModal.value = true;
};

const editProfile = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/profile/edit/${current_user.value.username}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                fullname: fullname.value,
                email: email.value,
                experience: experience.value,
                address: address.value,
                pincode: pincode.value,
                contact_number: contact_number.value
            })
        });
        const data = await response.json();
        if (response.ok) {
            await fetchAllData();
            showAlert(data.message, "success");
        } else {
            showAlert(Object.values(data)[0], "warning");
        }
    } catch (error) {
        console.error('Error editing profile:', error);
    }
};
</script>