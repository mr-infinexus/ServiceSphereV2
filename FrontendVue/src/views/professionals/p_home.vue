<template>
    <Navbar :roleName="'professional'" />
    <router-view />
    <div>
        <h1 class="m-3">Hello @{{ current_user.username }}</h1>
        <hr class="border">
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
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody class="table-group-divider align-middle">
                    <tr v-for="request in pending_services">
                        <td>{{ request.id }}</td>
                        <td>{{ request.customer }}</td>
                        <td>{{ request.address }}</td>
                        <td>{{ request.pincode }}</td>
                        <td>{{ request.contact_number }}</td>
                        <td>{{ formattedTime(request.time_of_request) }}</td>
                        <td>{{ request.task }}</td>
                        <td>
                            <button class="btn btn-success mx-1 py-1" @click="showAcceptModal(request.id)">
                                <i class="bi bi-check-circle"></i>
                            </button>
                            <button class="btn btn-danger mx-1 py-1" @click="showRejectModal(request.id)">
                                <i class="bi bi-ban"></i>
                            </button>
                        </td>
                    </tr>
                    <tr v-if="pending_services.length === 0">
                        <td colspan="8" class="text-center">No pending services found.</td>
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
        <hr class="border">
        <h2 class="m-3">Ongoing Services</h2>
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
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody class="table-group-divider align-middle">
                    <tr v-for="request in ongoing_services">
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
                    </tr>
                    <tr v-if="ongoing_services.length === 0">
                        <td colspan="8" class="text-center">No ongoing services found.</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <hr class="border">
        <h2 class="m-3">Closed Services</h2>
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
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody class="table-group-divider align-middle">
                    <tr v-for="request in closed_services">
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
                    </tr>
                    <tr v-if="closed_services.length === 0">
                        <td colspan="8" class="text-center">No closed services found.</td>
                    </tr>
                </tbody>
            </table>
        </div>
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
const pending_services = ref([]);
const ongoing_services = ref([]);
const closed_services = ref([]);

const fetchAllData = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/professional', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const data = await response.json();
        if (response.ok) {
            current_user.value = data.current_user;
            pending_services.value = data.services.pending_services;
            ongoing_services.value = data.services.ongoing_services;
            closed_services.value = data.services.closed_services;
        } else {
            const goto = '/' + data.role;
            router.push({ path: goto });
            showAlert(Object.values(data)[0], "warning");
        }
    } catch (error) {
        console.error('Error fetching professional data:', error);
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
            await fetchAllData();
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
            await fetchAllData();
            showAlert(data.message, "success");
        } else {
            showAlert(Object.values(data)[0], "danger");
        }
    } catch (error) {
        console.error('Error rejecting service:', error);
    }
};
</script>