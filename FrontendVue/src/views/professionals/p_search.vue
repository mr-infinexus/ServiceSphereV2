<template>
    <Navbar :roleName="'professional'" />
    <router-view />
    <div>
        <h2 class="m-3">Search</h2>
        <div class="d-flex align-items-center justify-content-center m-0">
            <div class="col-12 col-lg-10">
                <form @submit.prevent="handleProfessionalSearch">
                    <div class="row align-items-center justify-content-center">
                        <div class="col-12 col-md-4 mb-3 mb-md-0 d-flex align-items-center px-2">
                            <label class="form-label me-2 mb-0" style="white-space: nowrap;">Search by :</label>
                            <select class="form-select" v-model="search_by" required="">
                                <option selected disabled value="">Search by</option>
                                <option value="service_request">Service Requests</option>
                            </select>
                        </div>
                        <div class="col-12 col-md-4 mb-3 mb-md-0 px-2">
                            <input class="form-control" type="text" v-model="search_text"
                                placeholder="Enter search text" required>
                        </div>
                        <div class="col-12 col-md-2 mb-3 mb-md-0 text-center text-md-start px-2">
                            <button type="submit" class="btn btn-dark px-2">Search</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
        <hr class="border">
        <section v-if="service_history.length !== 0">
            <h2 class="m-3">Today's Services</h2>
            <div class="table-responsive">
                <table class="table table-striped table-primary table-hover">
                    <thead class="align-middle">
                        <tr>
                            <th>ID</th>
                            <th>Customer Name</th>
                            <th>Address</th>
                            <th>Pincode</th>
                            <th>Contact No</th>
                            <th>Time of Request</th>
                            <th>Task</th>
                            <th>Status</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody class="table-group-divider align-middle">
                        <tr v-for="request in service_history">
                            <td>{{ request.id }}</td>
                            <td>{{ request.customer }}</td>
                            <td>{{ request.address }}</td>
                            <td>{{ request.pincode }}</td>
                            <td>{{ request.contact_number }}</td>
                            <td>{{ formattedTime(request.time_of_request) }}</td>
                            <td>{{ request.task }}</td>
                            <td>
                                <span :class="`badge rounded-pill text-bg-${statusColor(request.service_status)}`">
                                    {{ request.service_status }}
                                </span>
                            </td>
                            <td>
                                <button v-if="request.service_status === 'requested'" class="btn btn-success mx-1 py-1"
                                    @click="showAcceptModal(request.id)">
                                    <i class="bi bi-check-circle"></i>
                                </button>
                                <button v-if="request.service_status === 'requested'" class="btn btn-danger mx-1 py-1"
                                    @click="showRejectModal(request.id)">
                                    <i class="bi bi-ban"></i>
                                </button>
                                <span v-if="request.service_status !== 'requested'">N/A</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <Modal v-model="acceptModal" type="success" confirm-button="Accept" @confirm="acceptService(request_id)">
                <template #header>Accept Service Request</template>
                <p class="m-2">Are you sure you want to accept this service request?</p>
            </Modal>
            <Modal v-model="rejectModal" type="danger" confirm-button="Reject" @confirm="rejectService(request_id)">
                <template #header>Reject Service Request</template>
                <p class="m-2">Are you sure you want to reject this service request?</p>
            </Modal>
        </section>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAlert } from '@/components/alert.js';
import Modal from '@/components/Modal.vue';
import Navbar from '@/components/Navbar.vue';

const router = useRouter();
const { showAlert } = useAlert();

const search_by = ref('');
const search_text = ref('');
const service_history = ref([]);

const handleProfessionalSearch = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/professional/search/${search_by.value}/${search_text.value}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const data = await response.json();
        if (response.ok) {
            service_history.value = data.service_history;
        } else if (response.status == 404) {
            service_history.value = '';
            showAlert(Object.values(data)[0], "warning");
        } else {
            const goto = '/' + data.role;
            router.push({ path: goto });
            showAlert(Object.values(data)[0], "warning");
        }
    } catch (error) {
        console.error('Error fetching professional data:', error);
    }
};

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

const request_id = ref(0);
const acceptModal = ref(false);
const rejectModal = ref(false);

const showAcceptModal = async (id) => {
    request_id.value = id;
    acceptModal.value = true;
};
const showRejectModal = async (id) => {
    request_id.value = id;
    rejectModal.value = true;
};
const acceptService = async (id) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/service_request/${id}/accept`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const data = await response.json();
        if (response.ok) {
            await handleProfessionalSearch();
            showAlert(data.message, "success");
        } else {
            showAlert(Object.values(data)[0], "danger");
        }
    } catch (error) {
        console.error('Error accepting service:', error);
    }
};

const rejectService = async (id) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/service_request/${id}/reject`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const data = await response.json();
        if (response.ok) {
            await handleProfessionalSearch();
            showAlert(data.message, "success");
        } else {
            showAlert(Object.values(data)[0], "danger");
        }
    } catch (error) {
        console.error('Error rejecting service:', error);
    }
};
</script>