<template>
    <Navbar :roleName="'customer'" />
    <router-view />
    <div>
        <h1 class="m-3">Hello @{{ current_user.username }}</h1>
        <hr class="border">
        <section>
            <h2 class="m-3">Looking For ?</h2>
            <div class="row row-cols-1 row-cols-md-3 g-4 m-3 d-flex justify-content-center">
                <div v-for="service in services" :key="service.id" class="col my-3 px-3">
                    <div class="card h-100 text-center bg-primary-subtle rounded">
                        <div class="card-header fs-5"><b>{{ service.name }}</b></div>
                        <div class="card-body">
                            <p class="card-text">{{ service.description }}</p>
                            <router-link class="btn btn-primary px-3"
                                :to="'/select_professional/' + service.id">Select</router-link>
                        </div>
                        <div class="card-footer text-body"><b>Price: </b> &#8377;{{ service.price }}</div>
                        <div class="card-footer text-body"><b>Time Required: </b> {{ service.time_required }} mins</div>
                    </div>
                </div>
            </div>
        </section>
        <hr class="border">
        <section>
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
                        <tr v-for="item in service_history" :key="item.id">
                            <td>{{ item.id }}</td>
                            <td>{{ item.service.name }}</td>
                            <td>{{ item.professional.fullname }}</td>
                            <td class="fs9">{{ formattedTime(item.time_of_request) }}</td>
                            <td class="fs9">
                                <span v-if="item.time_of_completion">
                                    {{ formattedTime(item.time_of_completion) }}
                                </span>
                                <span v-else>N/A</span>
                            </td>
                            <td>{{ item.task }}</td>
                            <td>
                                <span :class="`badge rounded-pill text-bg-${statusColor(item.service_status)}`">
                                    {{ item.service_status }}
                                </span>
                            </td>
                            <td>
                                <form v-if="item.service_status !== 'closed' && item.service_status !== 'rejected'"
                                    @submit.prevent="closeService(item.id)">
                                    <button type="submit" class="btn btn-warning btn-sm">Close it?</button>
                                </form>
                                <form v-else-if="item.service_status === 'rejected' && !item.time_of_completion"
                                    @submit.prevent="serviceRemarks(item.id)">
                                    <button type="submit" class="btn btn-info btn-sm">Add Remarks</button>
                                </form>
                                <span v-else>N/A</span>
                            </td>
                        </tr>
                        <tr v-if="!service_history.length">
                            <td colspan="8" class="text-center">No service history found.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAlert } from '@/components/alert.js'
import Navbar from '@/components/Navbar.vue';

const router = useRouter();
const { showAlert } = useAlert();

const current_user = ref({});
const services = ref([]);
const service_history = ref([]);

onMounted(async () => {
    try {
        const jwtToken = localStorage.getItem('token');
        const response = await fetch('http://127.0.0.1:5000/api/customer', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${jwtToken}`
            }
        });
        const data = await response.json();
        if (response.status == 403) {
            const goto = '/' + data.role;
            router.push({ path: goto });
            showAlert(data.message, "info");
        }
        if (response.ok) {
            current_user.value = data.current_user;
            services.value = data.services;
            service_history.value = data.service_history;
        }
    } catch (error) {
        console.error('Error fetching customer data:', error);
    }
});

const formattedTime = (timeString) => {
    const date = new Date(timeString);
    return date.toLocaleString('en-US', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: true });
};

const statusColor = (status) => {
    if (status === 'accepted') return 'success';
    if (status === 'requested') return 'primary';
    if (status === 'rejected') return 'danger';
    if (status === 'closed') return 'danger';
    return '';
};

const closeService = (service_id) => {
    console.log('Closing service:', service_id);
};

const serviceRemarks = (service_id) => {
    console.log('Adding remarks for service:', service_id);
};
</script>