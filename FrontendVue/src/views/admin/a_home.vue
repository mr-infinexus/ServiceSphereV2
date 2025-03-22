<template>
    <Navbar :roleName="'admin'" />
    <router-view />
    <div>
        <h1 class="m-3">Hello @admin</h1>
        <hr class="border">
        <h2 class="m-3">Services</h2>
        <div class="table-responsive">
            <table class="table table-striped table-primary table-hover">
                <thead class="align-middle">
                    <tr>
                        <th style="min-width: 50px;">ID</th>
                        <th>Service Name</th>
                        <th>Price</th>
                        <th>Time Required</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody class="table-group-divider align-middle">
                    <tr v-for="service in services">
                        <td>
                            <button class="btn btn-link" @click="viewServiceDetails(service)">
                                {{ service.id }}
                            </button>
                        </td>
                        <td>{{ service.name }}</td>
                        <td>&#8377; {{ service.price }}</td>
                        <td>{{ service.time_required }} mins</td>
                        <td>
                            <button type="button" class="btn btn-warning m-1 py-1"
                                @click="showEditServiceModal(service)">
                                <i class="bi bi-pencil-square"></i>
                            </button>
                            <button type="button" class="btn btn-danger m-1 py-1"
                                @click="showDeleteServiceModal(service.id)">
                                <i class="bi bi-trash3"></i>
                            </button>
                        </td>
                    </tr>
                    <tr v-if="services.length === 0">
                        <td colspan="5" class="text-center">No services found.</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <button type="button" class="btn btn-light px-2" @click="showAddServiceModal">
            <i class="bi bi-plus-square"></i> Add New Service
        </button>
        <Modal v-model="serviceDetailsModal" cancel-button="Close">
            <template #header>Service Details</template>
            <div class="table d-flex align-items-center justify-content-center m-0">
                <table class="table table-primary table-bordered table-striped w-auto align-middle m-0">
                    <tbody>
                        <tr>
                            <th>ID</th>
                            <td>{{ serviceDetails.id }}</td>
                        </tr>
                        <tr>
                            <th>Name</th>
                            <td>{{ serviceDetails.name }}</td>
                        </tr>
                        <tr>
                            <th>Price</th>
                            <td>&#8377; {{ serviceDetails.price }}</td>
                        </tr>
                        <tr>
                            <th style="white-space: nowrap;">Time Required</th>
                            <td>{{ serviceDetails.time_required }} mins</td>
                        </tr>
                        <tr>
                            <th>Description</th>
                            <td style="white-space: wrap;">{{ serviceDetails.description }}</td>
                        </tr>
                        <tr>
                            <th>Created At</th>
                            <td>{{ formattedTime(serviceDetails.created_at) }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </Modal>
        <Modal v-model="editServiceModal" type="warning" confirm-button="Confirm" @confirm="editService(service_id)">
            <template #header>Edit Service</template>
            <div class="row d-flex align-items-center justify-content-center bg-primary-subtle m-1 py-2">
                <div class="col-11">
                    <label class="form-label text-black me-2" for="name">Service Name</label>
                    <input class="form-control" id="name" maxlength="100" minlength="2" v-model="name" required=""
                        type="text" value=""><br>
                </div>
                <div class="d-flex align-items-center justify-content-center col-12 mb-2">
                    <label class="form-label text-black mb-0 me-2" for="price">Price</label>
                    <input class="form-control w-50" id="price" min="0" v-model="price" required="" step="any"
                        type="number" value=""><br>
                </div>
                <div class="d-flex align-items-center justify-content-center col-11 my-2">
                    <label class="form-label text-black mb-0 me-2" for="time_required">Time Required</label>
                    <input class="form-control w-50" id="time_required" min="0" v-model="time_required" required=""
                        type="number" value=""><br>
                </div>
                <div class="col-11">
                    <label class="form-label text-black me-2" for="description">Description</label>
                    <textarea class="form-control" id="description" v-model="description" value=""></textarea><br>
                </div>
            </div>
        </Modal>
        <Modal v-model="deleteServiceModal" type="danger" confirm-button="Delete" @confirm="deleteService(service_id)">
            <template #header>Delete Service</template>
            <p class="m-2">Are you sure you want to delete this service?<br>This action cannot be undone.</p>
        </Modal>
        <Modal v-model="addServiceModal" confirm-button="Confirm" @confirm="addService">
            <template #header>Add New Service</template>
            <div class="row d-flex align-items-center justify-content-center bg-primary-subtle m-1 py-2">
                <div class="col-11">
                    <label class="form-label text-black me-2" for="name">Service Name</label>
                    <input class="form-control" id="name" maxlength="100" minlength="2" v-model="name" required=""
                        type="text" value=""><br>
                </div>
                <div class="d-flex align-items-center justify-content-center col-12 mb-2">
                    <label class="form-label text-black mb-0 me-2" for="price">Price</label>
                    <input class="form-control w-50" id="price" min="0" v-model="price" required="" step="any"
                        type="number" value=""><br>
                </div>
                <div class="d-flex align-items-center justify-content-center col-11 my-2">
                    <label class="form-label text-black mb-0 me-2" for="time_required">Time Required</label>
                    <input class="form-control w-50" id="time_required" min="0" v-model="time_required" required=""
                        type="number" value=""><br>
                </div>
                <div class="col-11">
                    <label class="form-label text-black me-2" for="description">Description</label>
                    <textarea class="form-control" id="description" v-model="description" value=""></textarea><br>
                </div>
            </div>
        </Modal>
        <hr class="border">
        <h2 class="m-3">Professionals</h2>
        <div class="table-responsive">
            <table class="table table-striped table-primary table-hover">
                <thead class="align-middle">
                    <tr>
                        <th style="min-width: 50px;">ID</th>
                        <th>Username</th>
                        <th>Full Name</th>
                        <th>Service</th>
                        <th>Rating</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody class="table-group-divider align-middle">
                    <tr v-for="user in professionals">
                        <td>
                            <button class="btn btn-link" @click="viewUserDetails(user)">
                                {{ user.id }}
                            </button>
                        </td>
                        <td>{{ user.username }}</td>
                        <td>{{ user.fullname }}</td>
                        <td>{{ user.service_name }}</td>
                        <td>
                            {{ user.rating.toFixed(1) }}
                            <StarRating :rating="user.rating" />
                        </td>
                        <td>
                            <span :class="`badge rounded-pill text-bg-${statusColor(user.status)}`">
                                {{ user.status }}
                            </span>
                        </td>
                        <td>
                            <button v-if="user.status === 'pending' || user.status === 'blocked'" type="button"
                                class="btn btn-success m-1 py-1" @click="showApproveModal(user.id)">
                                <i class=" bi bi-shield-check"></i>
                            </button>
                            <button v-else-if="user.status !== 'blocked'" type="button" class="btn btn-warning m-1 py-1"
                                @click="showBlockModal(user.id)">
                                <i class="bi bi-ban"></i>
                            </button>
                            <button type="button" class="btn btn-danger m-1 py-1" @click="showDeleteUserModal(user.id)">
                                <i class="bi bi-trash3"></i>
                            </button>
                        </td>
                    </tr>
                    <tr v-if="professionals.length === 0">
                        <td colspan="7" class="text-center">No professionals found.</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <h2 class="m-3">Customers</h2>
        <div class="table-responsive">
            <table class="table table-striped table-primary table-hover">
                <thead class="align-middle">
                    <tr>
                        <th style="min-width: 50px;">ID</th>
                        <th>Username</th>
                        <th>Full Name</th>
                        <th>Address</th>
                        <th>Pincode</th>
                        <th>Contact No</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody class="table-group-divider align-middle">
                    <tr v-for="user in customers">
                        <td>
                            <button class="btn btn-link" @click="viewUserDetails(user)">
                                {{ user.id }}
                            </button>
                        </td>
                        <td>{{ user.username }}</td>
                        <td>{{ user.fullname }}</td>
                        <td>{{ user.address }}</td>
                        <td>{{ user.pincode }}</td>
                        <td>{{ user.contact_number }}</td>
                        <td>
                            <span :class="`badge rounded-pill text-bg-${statusColor(user.status)}`">
                                {{ user.status }}
                            </span>
                        </td>
                        <td>
                            <button v-if="user.status === 'blocked'" class="btn btn-success m-1 py-1"
                                @click="showApproveModal(user.id)">
                                <i class=" bi bi-shield-check"></i>
                            </button>
                            <button v-else-if="user.status !== 'blocked'" class="btn btn-warning m-1 py-1"
                                @click="showBlockModal(user.id)">
                                <i class="bi bi-ban"></i>
                            </button>
                            <button class="btn btn-danger m-1 py-1" @click="showDeleteUserModal(user.id)">
                                <i class="bi bi-trash3"></i>
                            </button>
                        </td>
                    </tr>
                    <tr v-if="customers.length === 0">
                        <td colspan="8" class="text-center">No customers found.</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <Modal v-model="userDetailsModal" cancel-button="Close">
            <template #header>Professional Details</template>
            <div class="table d-flex align-items-center justify-content-center m-0">
                <table class="table table-primary table-bordered table-striped w-auto align-middle m-0">
                    <tbody>
                        <tr>
                            <th>ID</th>
                            <td>{{ userDetails.id }}</td>
                        </tr>
                        <tr>
                            <th>Username</th>
                            <td>{{ userDetails.username }}</td>
                        </tr>
                        <tr>
                            <th>Email</th>
                            <td>{{ userDetails.email }}</td>
                        </tr>
                        <tr>
                            <th>Full Name</th>
                            <td>{{ userDetails.fullname }}</td>
                        </tr>
                        <template v-if="userDetails.role === 'professional'">
                            <tr>
                                <th>Service Name</th>
                                <td>{{ userDetails.service_name }}</td>
                            </tr>
                            <tr>
                                <th>Experience</th>
                                <td>{{ userDetails.experience }} years</td>
                            </tr>
                            <tr>
                                <th>Rating</th>
                                <td>{{ userDetails.rating.toFixed(1) }}
                                    <StarRating :rating="userDetails.rating" />
                                </td>
                            </tr>
                        </template>
                        <tr>
                            <th>Address</th>
                            <td>{{ userDetails.address }}</td>
                        </tr>
                        <tr>
                            <th>Pincode</th>
                            <td>{{ userDetails.pincode }}</td>
                        </tr>
                        <tr>
                            <th>Contact No</th>
                            <td>{{ userDetails.contact_number }}</td>
                        </tr>
                        <tr>
                            <th>Status</th>
                            <td>{{ userDetails.status }}</td>
                        </tr>
                        <tr>
                            <th>Profile Created</th>
                            <td>{{ formattedTime(userDetails.created_at) }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </Modal>
        <Modal v-model="approveModal" type="success" confirm-button="Approve" @confirm="approveUser(user_id)">
            <template #header>Approve User</template>
            <p class="m-2">Are you sure you want to approve this user?</p>
        </Modal>
        <Modal v-model="blockModal" type="warning" confirm-button="Block" @confirm="blockUser(user_id)">
            <template #header>Block User</template>
            <p class="m-2">Are you sure you want to block this user?</p>
        </Modal>
        <Modal v-model="deleteUserModal" type="danger" confirm-button="Delete" @confirm="deleteUser(user_id)">
            <template #header>Delete User</template>
            <p class="m-2">Are you sure you want to delete this user?<br>This action cannot be undone.</p>
        </Modal>
        <hr class="border">
        <h2 class="m-3">Service Requests</h2>
        <div class="table-responsive">
            <table class="table table-striped table-primary table-hover">
                <thead class="align-middle">
                    <tr>
                        <th style="min-width: 50px;">ID</th>
                        <th>Customer</th>
                        <th>Assigned Professional</th>
                        <th>Service Name</th>
                        <th>Time of Request</th>
                        <th>Time of Completion</th>
                        <th>Task</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody class="table-group-divider align-middle">
                    <tr v-for="request in service_history">
                        <td>{{ request.id }}</td>
                        <td>{{ request.customer }}</td>
                        <td>{{ request.professional }}</td>
                        <td>{{ request.service }}</td>
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
                    </tr>
                    <tr v-if="service_history.length === 0">
                        <td colspan="8" class="text-center">No service history found.</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <form @submit.prevent="csvExport">
            <button type="submit" class="btn btn-success m-3 px-3">
                <i class="bi bi-download me-1"></i>Export CSV
            </button>
        </form>
        <hr class="border mb-1">
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

const services = ref([]);
const professionals = ref([]);
const customers = ref([]);
const service_history = ref([]);
const serviceDetails = ref({});
const userDetails = ref({});

const fetchAllData = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/admin', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const data = await response.json();
        if (response.ok) {
            services.value = data.services;
            professionals.value = data.professionals;
            customers.value = data.customers;
            service_history.value = data.service_history;
        } else {
            const goto = '/' + data.role;
            router.push({ path: goto });
            showAlert(Object.values(data)[0], "warning");
        }
    } catch (error) {
        console.error('Error fetching data:', error);
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
    if (status === 'accepted' || status === 'verified') return 'success';
    if (status === 'requested' || status === 'pending') return 'primary';
    if (status === 'rejected' || status === 'closed' || status === 'blocked') return 'danger';
    return '';
};

const serviceDetailsModal = ref(false);
const editServiceModal = ref(false);
const deleteServiceModal = ref(false);
const addServiceModal = ref(false);
const service_id = ref(0);
const name = ref();
const price = ref();
const time_required = ref();
const description = ref();

const viewServiceDetails = async (service) => {
    serviceDetails.value = service;
    serviceDetailsModal.value = true;
};
const showEditServiceModal = async (service) => {
    service_id.value = service.id;
    name.value = service.name;
    price.value = service.price;
    time_required.value = service.time_required;
    description.value = service.description;
    editServiceModal.value = true;
};
const showDeleteServiceModal = async (id) => {
    service_id.value = id;
    deleteServiceModal.value = true;
};
const showAddServiceModal = async () => {
    service_id.value = "";
    name.value = "";
    price.value = "";
    time_required.value = "";
    description.value = "";
    addServiceModal.value = true;
};
const editService = async (id) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/service/${id}/edit`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                name: name.value,
                price: price.value,
                time_required: time_required.value,
                description: description.value
            })
        });
        const data = await response.json();
        if (response.ok) {
            await fetchAllData();
            showAlert(data.message, "success");
        } else {
            showAlert(Object.values(data)[0], "danger");
        }
    } catch (error) {
        console.error('Error during editing service:', error);
    }
};
const deleteService = async (id) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/service/${id}/delete`, {
            method: 'DELETE',
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
        console.error('Error deleting service:', error);
    }
};
const addService = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/service/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                name: name.value,
                price: price.value,
                time_required: time_required.value,
                description: description.value
            })
        });
        const data = await response.json();
        if (response.ok) {
            await fetchAllData();
            showAlert(data.message, "success");
        } else {
            showAlert(Object.values(data)[0], "danger");
        }
    } catch (error) {
        console.error('Error during adding new service:', error);
    }
};

const userDetailsModal = ref(false);
const approveModal = ref(false);
const blockModal = ref(false);
const deleteUserModal = ref(false);
const user_id = ref(0);

const viewUserDetails = async (user) => {
    userDetails.value = user;
    userDetailsModal.value = true;
};
const showApproveModal = async (id) => {
    user_id.value = id;
    approveModal.value = true;
};
const showBlockModal = async (id) => {
    user_id.value = id;
    blockModal.value = true;
};
const showDeleteUserModal = async (id) => {
    user_id.value = id;
    deleteUserModal.value = true;
};
const approveUser = async (id) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/user/${id}/approve`, {
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
        console.error('Error deleting service:', error);
    }
};
const blockUser = async (id) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/user/${id}/block`, {
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
        console.error('Error blocking:', error);
    }
};
const deleteUser = async (id) => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/user/${id}/delete`, {
            method: 'DELETE',
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
        console.error('Error deleting user:', error);
    }
};

const csvExport = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/export', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const data = await response.blob();
        if (response.ok) {
            const url = URL.createObjectURL(data);
            const a = document.createElement('a');
            a.href = url;
            a.click();
            URL.revokeObjectURL(url);
        }
    } catch (error) {
        console.error('Error exporting csv:', error);
    }
};
</script>