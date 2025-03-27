<template>
    <Navbar :roleName="'customer'" />
    <router-view />
    <div>
        <h2 class="m-3">Search</h2>
        <div class="d-flex align-items-center justify-content-center m-0">
            <div class="col-12 col-lg-10">
                <form @submit.prevent="handleCustomerSearch">
                    <div class="row align-items-center justify-content-center">
                        <div class="col-12 col-md-4 mb-3 mb-md-0 d-flex align-items-center px-2">
                            <label class="form-label me-2 mb-0" style="white-space: nowrap;">Search by :</label>
                            <select class="form-select" v-model="search_by" required="">
                                <option selected disabled value="">Search by</option>
                                <option value="service_request">Service Requests</option>
                                <option value="professional">Professionals</option>
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
                                <button v-if="request.service_status === 'requested'" class="btn btn-warning mx-1 py-1"
                                    @click="showeditServiceModal(request)">
                                    <i class="bi bi-pencil-square"></i>
                                </button>
                                <button
                                    v-if="request.service_status === 'requested' || request.service_status === 'accepted'"
                                    class="btn btn-success mx-1 py-1" @click="showCloseServiceModal(request)">
                                    <i class="bi bi-journal-check"></i>
                                </button>
                                <button
                                    v-if="(request.service_status === 'rejected' || request.service_status === 'closed') && !request.time_of_completion"
                                    class="btn btn-info mx-1 py-1" @click="showServiceRemarksModal(request)">
                                    <i class="bi bi-person-lines-fill"></i>
                                </button>
                                <span v-if="request.time_of_completion">N/A</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>
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
                    <label class="form-label text-black" for="review">Review</label>
                    <input class="form-control" id="review" maxlength="100" minlength="2" v-model="review" type="text">
                </div>
            </div>
        </Modal>
        <section v-if="professionals.length !== 0">
            <h2 class="m-3">Professionals</h2>
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
                    </tbody>
                </table>
            </div>
        </section>
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
const professionals = ref([]);

const handleCustomerSearch = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/customer/search/${search_by.value}/${search_text.value}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const data = await response.json();
        if (response.ok) {
            service_history.value = data.service_history;
            professionals.value = data.professionals;
        } else if (response.status == 404) {
            service_history.value = '';
            professionals.value = '';
            showAlert(Object.values(data)[0], "warning");
        } else {
            const goto = '/' + data.role;
            router.push({ path: goto });
            showAlert(Object.values(data)[0], "warning");
        }
    } catch (error) {
        console.error('Error fetching customer data:', error);
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

const bookServiceModal = ref(false);
const professional_id = ref();
const service_id = ref();
const service_name = ref();
const fullname = ref();
const time_of_request = ref();
const task = ref();
const today = new Date().toISOString().slice(0, 16);
const showBookServiceModal = async (professional) => {
    professional_id.value = professional.id;
    service_id.value = professional.service_id;
    service_name.value = professional.service_name;
    fullname.value = professional.fullname;
    bookServiceModal.value = true;
};
const bookService = async () => {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/book/${service_id.value}/${professional_id.value}`, {
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

const request_id = ref();
const editServiceModal = ref(false);
const closeServiceModal = ref(false);
const serviceRemarksModal = ref(false);
const professional_name = ref();
const rating = ref();
const review = ref();
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
                task: task.value,
                time_of_request: time_of_request.value
            })
        });
        const data = await response.json();
        if (response.ok) {
            showAlert(data.message, "success");
            await handleCustomerSearch();
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
            await handleCustomerSearch();
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
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                rating: rating.value,
                review: review.value
            })
        });
        const data = await response.json();
        if (response.ok) {
            rating.value = 0;
            review.value = null;
            showAlert(data.message, "success");
            await handleCustomerSearch();
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