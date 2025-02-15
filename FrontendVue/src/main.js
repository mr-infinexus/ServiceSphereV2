import './assets/style.css'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from '@/views/home.vue'
import Login from '@/views/login.vue'
import CustomerRegister from '@/views/customers/c_register.vue'
import ProfessionalRegister from '@/views/professionals/p_register.vue'
import Profile from '@/views/profile.vue'
import AdminHome from '@/views/admin/a_home.vue'
import CustomerHome from '@/views/customers/c_home.vue'
import ProfessionalHome from '@/views/professionals/p_home.vue'
import ErrorPage from '@/views/errorpage.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: Home },
        { path: '/login', component: Login },
        { path: '/register/customer', component: CustomerRegister },
        { path: '/register/professional', component: ProfessionalRegister },
        { path: '/profile', component: Profile },
        { path: '/admin/', component: AdminHome, props: true },
        { path: '/customer/', component: CustomerHome, props: true },
        { path: '/professional/', component: ProfessionalHome, props: true },
        { path: "/:pathMatch(.*)*", component: ErrorPage }
    ]
});

createApp(App).use(router).mount('#app')