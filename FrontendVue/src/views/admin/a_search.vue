<template>
    <Navbar :roleName="'admin'" />
    <router-view />
    <div>
        <h2 class="m-3">Search</h2>
        <form @submit.prevent="handleAdminSearch">
            <div class="d-flex align-items-center justify-content-center">
                <label class="form-label me-2">Search by :</label>
                <select class="form-select d-inline w-25 me-2" v-model="search_by" required>
                    <option selected disabled value="">Search by</option>
                    <option value="service_request">Service Requests</option>
                    <option value="customer">Customers</option>
                    <option value="professional">Professionals</option>
                </select>
                <input class="form-control d-inline w-25" type="text" v-model="search_text"
                    placeholder="Enter search text" required>
                <button type="submit" class="btn btn-dark mx-2 px-2">Search</button>
            </div>
        </form>
        <hr class="border">
        <section v-if="service_history.length !== 0">
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
                    </tbody>
                </table>
            </div>
        </section>
        <section v-if="customers.length !== 0">
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
                    </tbody>
                </table>
            </div>
        </section>
        <section v-if="professionals.length !== 0">
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
                                <button v-if="user.status === 'pending' || user.status === 'blocked'"
                                    class="btn btn-success m-1 py-1" @click="showApproveModal(user.id)">
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
                    </tbody>
                </table>
            </div>
        </section>
        <Modal v-model="userDetailsModal" cancel-button="Close">
            <template #header>User Details</template>
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
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAlert } from '@/components/alert.js';
import Modal from '@/components/Modal.vue';
import Navbar from '@/components/Navbar.vue';
import StarRating from '@/components/StarRating.vue';

const router = useRouter();
const { showAlert } = useAlert();
const search_by = ref('');
const search_text = ref('');

const service_history = ref([]);
const customers = ref([]);
const professionals = ref([]);
const userDetails = ref({});

const handleAdminSearch = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/admin/search/${search_by.value}/${search_text.value}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const data = await response.json();
        if (response.ok) {
            service_history.value = data.service_history;
            customers.value = data.customers;
            professionals.value = data.professionals;
        } else if (response.status == 404) {
            service_history.value = '';
            customers.value = '';
            professionals.value = '';
            showAlert(Object.values(data)[0], "warning");
        } else {
            const goto = '/' + data.role;
            router.push({ path: goto });
            showAlert(Object.values(data)[0], "warning");
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

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
            await handleAdminSearch();
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
            await handleAdminSearch();
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
            await handleAdminSearch();
            showAlert(data.message, "success");
        } else {
            showAlert(Object.values(data)[0], "danger");
        }
    } catch (error) {
        console.error('Error deleting user:', error);
    }
};
</script>