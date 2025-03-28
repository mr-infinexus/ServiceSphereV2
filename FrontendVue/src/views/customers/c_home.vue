<template>
    <Navbar :roleName="'customer'" />
    <router-view />
    <div>
        <h1 class="m-3">Hello @{{ current_user.username }}</h1>
        <hr class="border">
        <h2 class="m-3">Looking For ?</h2>
        <div class="row row-cols-1 row-cols-md-3 g-4 m-3 d-flex justify-content-center">
            <div v-for="service in services" class="col my-3 px-3">
                <div class="card h-100 text-center bg-primary-subtle rounded">
                    <div class="card-header fs-5"><b>{{ service.name }}</b></div>
                    <div class="card-body">
                        <p class="card-text">{{ service.description }}</p>
                        <router-link class="btn btn-primary px-3" :to="'/select_professional/' + service.id">
                            Select <i class="bi bi-box-arrow-in-up-right"></i>
                        </router-link>
                    </div>
                    <div class="card-footer text-body"><b>Price: </b> &#8377; {{ service.price }}</div>
                    <div class="card-footer text-body"><b>Time Required: </b> {{ service.time_required }} mins</div>
                </div>
            </div>
        </div>
        <hr class="border">
        <h2 class="m-3">Service History</h2>
        <div class="table-responsive">
            <table class="table table-striped table-primary table-hover">
                <thead class="align-middle">
                    <tr>
                        <th style="min-width: 50px;">ID</th>
                        <th>Service Name</th>
                        <th>Professional Name</th>
                        <th>Time of Request</th>
                        <th>Time of Completion</th>
                        <th>Task</th>
                        <th>Status</th>
                        <th style="min-width: 125px">Action</th>
                    </tr>
                </thead>
                <tbody class="table-group-divider align-middle">
                    <tr v-for="request in service_history">
                        <td>{{ request.id }}</td>
                        <td>{{ request.service }}</td>
                        <td>{{ request.professional }}</td>
                        <td>{{ formattedTime(request.time_of_request) }}</td>
                        <td>
                            <span v-if="request.time_of_completion">
                                {{ formattedTime(request.time_of_completion) }}
                            </span>
                            <span v-else>N/A</span>
                        </td>
                        <td>{{ request.task }}</td>
                        <td>
                            <span :class="`badge rounded-pill text-bg-${statusColor(request.service_status)}`">
                                {{ request.service_status }}
                            </span>
                        </td>
                        <td>
                            <template
                                v-if="request.service_status === 'requested' || request.service_status === 'accepted'">
                                <button v-if="request.service_status === 'requested'" class="btn btn-warning mx-1 py-1"
                                    @click="showeditServiceModal(request)">
                                    <i class="bi bi-pencil-square"></i>
                                </button>
                                <button class="btn btn-success mx-1 py-1" @click="showCloseServiceModal(request)">
                                    <i class="bi bi-journal-check"></i>
                                </button>
                            </template>
                            <button v-else-if="!request.review_id" class="btn btn-info mx-1 py-1"
                                @click="showServiceRemarksModal(request)">
                                <i class="bi bi-person-lines-fill"></i>
                            </button>
                            <span v-else>N/A</span>
                        </td>
                    </tr>
                    <tr v-if="service_history.length === 0">
                        <td colspan="8" class="text-center">No service history found.</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <Modal v-model="editServiceModal" type="warning" confirm-button="Confirm" @submit="editServiceRequest">
            <template #header>Edit Service</template>
            <div class="row d-flex align-items-center justify-content-center bg-primary-subtle m-1 py-2">
                <div class="col-11 mb-2">
                    <label class="form-label text-black" for="service_name">Service Name</label>
                    <input class="form-control" id="service_name" maxlength="100" minlength="2" v-model="service_name"
                        required="" type="text" disabled readonly>
                </div>
                <div class="col-11 mb-2">
                    <label class="form-label text-black" for="fullname">Professional Name</label>
                    <input class="form-control" id="fullname" maxlength="100" minlength="2" v-model="professional_name"
                        required="" type="text" disabled readonly>
                </div>
                <div class="col-11 mb-2">
                    <label for="time_of_request" class="form-label text-black">Time of Request</label>
                    <input type="datetime-local" class="form-control" id="time_of_request" v-model="time_of_request"
                        :min="today" required>
                </div>
                <div class="col-11 mb-2">
                    <label class="form-label text-black" for="task">Task</label>
                    <input class="form-control" id="task" maxlength="100" minlength="2" v-model="task" required=""
                        type="text">
                </div>
            </div>
        </Modal>
        <Modal v-model="closeServiceModal" type="success" confirm-button="Close" @confirm="closeServiceRequest">
            <template #header>Close Service Request</template>
            <p class="m-2">Are you sure you want to close this service request?</p>
        </Modal>
        <Modal v-model="serviceRemarksModal" confirm-button="Confirm" @submit="serviceRemarks">
            <template #header>Add Service Remarks</template>
            <div class="row d-flex align-items-center justify-content-center bg-primary-subtle m-1 py-2">
                <div class="col-11 mb-2">
                    <label class="form-label text-black" for="service_name">Service Name</label>
                    <input class="form-control" id="service_name" maxlength="100" minlength="2" v-model="service_name"
                        required="" type="text" disabled readonly>
                </div>
                <div class="col-11 mb-2">
                    <label class="form-label text-black" for="fullname">Professional Name</label>
                    <input class="form-control" id="fullname" maxlength="100" minlength="2" v-model="professional_name"
                        required="" type="text" disabled readonly>
                </div>
                <div class="col-11 mb-2">
                    <label class="form-label text-black" for="task">Task</label>
                    <input class="form-control" id="task" maxlength="100" minlength="2" v-model="task" required=""
                        type="text" disabled readonly>
                </div>
                <div class="col-11 mb-2">
                    <div>Rating</div>
                    <div class="star-rating">
                        <input type="radio" id="star5" v-model="rating" value="5">
                        <label for="star5" class="bi bi-star-fill"></label>
                        <input type="radio" id="star4" v-model="rating" value="4">
                        <label for="star4" class="bi bi-star-fill"></label>
                        <input type="radio" id="star3" v-model="rating" value="3">
                        <label for="star3" class="bi bi-star-fill"></label>
                        <input type="radio" id="star2" v-model="rating" value="2">
                        <label for="star2" class="bi bi-star-fill"></label>
                        <input type="radio" id="star1" v-model="rating" value="1">
                        <label for="star1" class="bi bi-star-fill"></label>
                    </div>
                </div>
                <div class="col-11 mb-2">
                    <label class="form-label text-black" for="remarks">Remarks</label>
                    <input class="form-control" id="remarks" maxlength="100" minlength="2" v-model="remarks" type="text">
                </div>
            </div>
        </Modal>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAlert } from '@/components/alert.js'
import Modal from '@/components/Modal.vue';
import Navbar from '@/components/Navbar.vue';

const router = useRouter();
const { showAlert } = useAlert();

const current_user = ref({});
const services = ref([]);
const service_history = ref([]);

const fetchAllData = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/customer', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const data = await response.json();
        if (response.ok) {
            current_user.value = data.current_user;
            services.value = data.services;
            service_history.value = data.service_history;
        } else {
            const goto = '/' + data.role;
            router.push({ path: goto });
            showAlert(Object.values(data)[0], "warning");
        }
    } catch (error) {
        console.error('Error fetching customer data:', error);
    }
};

onMounted(async () => {
    await fetchAllData();
});

const formattedTime = (timeString) => {
    const date = new Date(timeString);
    return date.toLocaleString('en-IN', { dateStyle: 'short', timeStyle: 'short' });
};

const statusColor = (status) => {
    if (status === 'accepted') return 'success';
    if (status === 'requested') return 'primary';
    if (status === 'rejected') return 'danger';
    if (status === 'closed') return 'danger';
    return '';
};

const request_id = ref();
const editServiceModal = ref(false);
const closeServiceModal = ref(false);
const serviceRemarksModal = ref(false);
const service_name = ref();
const professional_name = ref();
const time_of_request = ref();
const task = ref();
const rating = ref();
const remarks = ref();
const today = new Date().toISOString().slice(0, 16);
const showeditServiceModal = async (request) => {
    request_id.value = request.id;
    service_name.value = request.service;
    professional_name.value = request.professional;
    time_of_request.value = request.time_of_request;
    task.value = request.task;
    editServiceModal.value = true;
};
const showCloseServiceModal = async (request) => {
    request_id.value = request.id;
    closeServiceModal.value = true;
};
const showServiceRemarksModal = async (request) => {
    request_id.value = request.id;
    service_name.value = request.service;
    professional_name.value = request.professional;
    task.value = request.task;
    serviceRemarksModal.value = true;
};
const editServiceRequest = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/edit/${request_id.value}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                task: task.value.trim(),
                time_of_request: time_of_request.value
            })
        });
        const data = await response.json();
        if (response.ok) {
            showAlert(data.message, "success");
            await fetchAllData();
        } else {
            showAlert(Object.values(data)[0], "warning");
        }
    } catch (error) {
        console.error('Error editing service request:', error);
    }
};

const closeServiceRequest = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/close/${request_id.value}`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
        });
        const data = await response.json();
        if (response.ok) {
            showAlert(data.message, "success");
            await fetchAllData();
        } else {
            showAlert(Object.values(data)[0], "warning");
        }
    } catch (error) {
        console.error('Error closing service request:', error);
    }
};

const serviceRemarks = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/review/${request_id.value}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                rating: rating.value,
                remarks: remarks.value.trim()
            })
        });
        const data = await response.json();
        if (response.ok) {
            rating.value = 0;
            remarks.value = null;
            showAlert(data.message, "success");
            await fetchAllData();
        } else {
            showAlert(Object.values(data)[0], "warning");
        }
    } catch (error) {
        console.error('Error adding remarks:', error);
    }
};
</script>

<style scoped>
.star-rating {
    direction: rtl;
    display: inline-block;
    cursor: pointer;
}

.star-rating input {
    display: none;
}

.star-rating label {
    color: #ffffff;
    text-shadow: 0px 0px 1px #000000;
    font-size: 24px;
    padding: 0 2px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.star-rating label:hover,
.star-rating label:hover~label,
.star-rating input:checked~label {
    scale: 1.1;
    color: #ffd700;
}
</style>