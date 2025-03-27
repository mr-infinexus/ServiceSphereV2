<template>
    <Navbar :roleName="'customer'" />
    <router-view />
    <div>
        <h2 class="m-3">List of Professionals</h2>
        <div class="table-responsive">
            <table class="table table-striped table-primary table-hover">
                <thead class="align-middle">
                    <tr>
                        <th>Fullname</th>
                        <th>Service Name</th>
                        <th>Address</th>
                        <th>Pincode</th>
                        <th>Contact No</th>
                        <th>Rating</th>
                        <th>Experience</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody class="table-group-divider align-middle">
                    <tr v-for="professional in professionals">
                        <td>{{ professional.fullname }}</td>
                        <td>{{ professional.service_name }}</td>
                        <td>{{ professional.address }}</td>
                        <td>{{ professional.pincode }}</td>
                        <td>{{ professional.contact_number }}</td>
                        <td>
                            {{ professional.rating.toFixed(1) }}
                            <StarRating :rating="professional.rating" />
                        </td>
                        <td>{{ professional.experience }} Years</td>
                        <td>
                            <button type="submit" class="btn btn-primary btn-sm"
                                @click="showBookServiceModal(professional)">
                                Book <i class="bi bi-arrow-left-square"></i>
                            </button>
                        </td>
                    </tr>
                    <tr v-if="professionals.length === 0">
                        <td colspan="8" class="text-center">No professionals found.</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <Modal v-model="bookServiceModal" confirm-button="Confirm" @submit="bookService">
            <template #header>Book Service</template>
            <div class="row d-flex align-items-center justify-content-center bg-primary-subtle m-1 py-2">
                <div class="col-11 mb-2">
                    <label class="form-label text-black" for="service_name">Service Name</label>
                    <input class="form-control" id="service_name" maxlength="100" minlength="2" v-model="service_name"
                        required="" type="text" disabled readonly>
                </div>
                <div class="col-11 mb-2">
                    <label class="form-label text-black" for="fullname">Professional Name</label>
                    <input class="form-control" id="fullname" maxlength="100" minlength="2" v-model="fullname"
                        required="" type="text" disabled readonly>
                </div>
                <div class="col-11 mb-2">
                    <label for="time_of_request" class="form-label text-black">Time of Request</label>
                    <input type="datetime-local" class="form-control" id="time_of_request" v-model="time_of_request"
                        :min="today" required="">
                </div>
                <div class="col-11 mb-2">
                    <label class="form-label text-black" for="task">Task</label>
                    <input class="form-control" id="task" maxlength="100" minlength="2" v-model="task" required=""
                        type="text">
                </div>
            </div>
        </Modal>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAlert } from '@/components/alert.js';
import Modal from '@/components/Modal.vue';
import Navbar from '@/components/Navbar.vue';
import StarRating from '@/components/StarRating.vue';

const router = useRouter();
const { showAlert } = useAlert();
const service_id = router.currentRoute.value.params.id;
const professionals = ref([]);

onMounted(async () => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/${service_id}/select_professional`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const data = await response.json();
        if (response.ok) {
            professionals.value = data;
        } else {
            const goto = '/' + data.role;
            router.push({ path: goto });
            showAlert(Object.values(data)[0], "warning");
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
});

const bookServiceModal = ref(false);
const professional_id = ref();
const service_name = ref();
const fullname = ref();
const time_of_request = ref();
const task = ref();
const today = new Date().toISOString().slice(0, 16);
const showBookServiceModal = async (professional) => {
    professional_id.value = professional.id;
    service_name.value = professional.service_name;
    fullname.value = professional.fullname;
    bookServiceModal.value = true;
};
const bookService = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/book/${service_id}/${professional_id.value}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                task: task.value,
                time_of_request: time_of_request.value
            })
        });
        const data = await response.json();
        if (response.ok) {
            router.go(-1);
            showAlert(data.message, "success");
        } else {
            showAlert(Object.values(data)[0], "warning");
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};
</script>