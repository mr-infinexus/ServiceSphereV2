import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap'
import './assets/style.css'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: () => import('@/views/home.vue') },
        { path: '/login', component: () => import('@/views/login.vue') },
        { path: '/register/customer', component: () => import('@/views/customers/c_register.vue') },
        { path: '/register/professional', component: () => import('@/views/professionals/p_register.vue') },
        { path: '/profile', component: () => import('@/views/profile.vue') },
        { path: '/admin/', component: () => import('@/views/admin/a_home.vue') },
        { path: '/admin/search', component: () => import('@/views/admin/a_search.vue') },
        { path: '/admin/summary', component: () => import('@/views/admin/a_summary.vue') },
        { path: '/customer/', component: () => import('@/views/customers/c_home.vue') },
        { path: '/customer/search', component: () => import('@/views/customers/c_search.vue') },
        { path: '/customer/summary', component: () => import('@/views/customers/c_summary.vue') },
        { path: '/select_professional/:id', component: () => import('@/views/customers/c_select_professional.vue') },
        { path: '/professional/', component: () => import('@/views/professionals/p_home.vue') },
        { path: '/professional/search', component: () => import('@/views/professionals/p_search.vue') },
        { path: '/professional/summary', component: () => import('@/views/professionals/p_summary.vue') },
        { path: "/:pathMatch(.*)*", component: () => import('@/views/errorpage.vue') }
    ]
});

const app = createApp(App);
app.use(router);
router.isReady().then(() => {
    app.mount('#app')
});