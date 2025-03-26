<template>
    <Navbar :roleName="'admin'" />
    <router-view />
    <div>
        <h2 class="m-3">Summary</h2>
        <hr class="border">
        <div class="row g-3 mb-4 justify-content-center">
            <div class="col-12 col-md-6 col-lg-3">
                <div class="card border-0 shadow-sm">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="text-muted mb-2">Total Users</h6>
                                <h4 class="mb-0 text-black">{{ stats.users }}</h4>
                            </div>
                            <div class="bg-primary bg-opacity-10 border border-primary-subtle p-3 rounded">
                                <i class="bi bi-people text-primary"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-12 col-md-6 col-lg-3">
                <div class="card border-0 shadow-sm">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="text-muted mb-2">Revenue</h6>
                                <h4 class="mb-0 text-black">&#8377;{{ stats.revenue }}</h4>
                            </div>
                            <div class="bg-success bg-opacity-10 border border-success-subtle p-3 rounded">
                                <i class="bi bi-cash-stack text-success"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-12 col-md-6 col-lg-3">
                <div class="card border-0 shadow-sm">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="text-muted mb-2">Total Requests</h6>
                                <h4 class="mb-0 text-black">{{ stats.requests }}</h4>
                            </div>
                            <div class="bg-info bg-opacity-10 border border-info-subtle p-3 rounded">
                                <i class="bi bi-journal-text text-info"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row g-4 justify-content-center">
            <div class="col-md-4">
                <div class="card shadow-sm">
                    <div class="card-header bg-success text-white text-center">
                        <h5>Overall Customer Ratings</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="ratingChart"></canvas>
                    </div>
                </div>
            </div>
            <div class="col-md-7">
                <div class="card shadow-sm">
                    <div class="card-header bg-primary text-white text-center">
                        <h5>Service Requests Summary</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="serviceChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAlert } from '@/components/alert.js';
import Chart from 'chart.js/auto';
import Navbar from '@/components/Navbar.vue';

const router = useRouter();
const { showAlert } = useAlert();

const stats = ref({});
const ratingCounts = ref({});
const serviceCounts = ref({});

const fetchAllData = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/admin/summary', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        const data = await response.json();
        if (response.ok) {
            stats.value = data.stats;
            ratingCounts.value = data.rating_counts;
            serviceCounts.value = data.service_counts;
        } else {
            const goto = '/' + data.role;
            router.push({ path: goto });
            showAlert(Object.values(data)[0], "warning");
        }
    } catch (error) {
        console.error('Error fetching admin summary data:', error);
    }
};

onMounted(async () => {
    await fetchAllData();

    const ratingLabels = Object.keys(ratingCounts.value);
    const ratingData = Object.values(ratingCounts.value);
    const ratingColors = ["#FF6384", "#FFCE56", "#4BC0C0", "#36A2EB", "#9966FF"];
    const ratingCtx = document.getElementById('ratingChart').getContext('2d');
    new Chart(ratingCtx, {
        type: 'pie',
        data: {
            labels: ratingLabels,
            datasets: [{
                label: 'Customer Ratings',
                data: ratingData,
                backgroundColor: ratingColors,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                },
                title: {
                    display: true,
                    text: 'Overall Customer Ratings'
                }
            }
        }
    });

    const serviceLabels = Object.keys(serviceCounts.value);
    const serviceData = Object.values(serviceCounts.value);
    const serviceColors = ["#FFEA00", "#008008", "#C70039", "#007BFF"];
    const serviceCtx = document.getElementById('serviceChart').getContext('2d');
    new Chart(serviceCtx, {
        type: 'bar',
        data: {
            labels: serviceLabels,
            datasets: [{
                label: 'Service Requests',
                data: serviceData,
                backgroundColor: serviceColors,
                borderColor: "#111111",
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: true
                },
                title: {
                    display: true,
                    text: 'Service Requests Summary'
                }
            }
        }
    });
});
</script>