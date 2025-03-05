import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap'
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
import SelectProfessional from '@/views/customers/c_select_professional.vue'
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
        { path: '/admin/', component: AdminHome },
        { path: '/customer/', component: CustomerHome },
        { path: '/select_professional/:id', component: SelectProfessional },
        { path: '/professional/', component: ProfessionalHome },
        { path: "/:pathMatch(.*)*", component: ErrorPage }
    ]
});

const app = createApp(App);
app.use(router);
router.isReady().then(() => {
    app.mount('#app')
});