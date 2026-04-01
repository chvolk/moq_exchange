import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'
import LandingPage from '@/components/LandingPage.vue'
import SignupPage from '@/components/SignupPage.vue'
import UserDashboard from '@/components/UserDashboard.vue'
import LeaguesPage from '@/components/LeaguesPage.vue'
import LoginPage from '@/components/LoginPage.vue'
import StockDraft from '@/components/StockDraft.vue'
import Leaderboard from '@/components/Leaderboard.vue'
import BazaarPage from '@/components/BazaarPage.vue'
import FAQPage from '@/components/FAQPage.vue'
import PrivacyPolicy from '@/components/PrivacyPolicy.vue'
const routes = [
  { path: '/admin', name: 'Admin', beforeEnter: () => { window.location.href = '/admin/' } },
  { path: '/', component: LandingPage },
  { path: '/signup', component: SignupPage },
  { path: '/login', component: LoginPage },
  { 
    path: '/dashboard', 
    component: UserDashboard,
    meta: { requiresAuth: true }
  },
  { 
    path: '/leagues', 
    component: LeaguesPage,
    meta: { requiresAuth: true }
  },
  { 
    path: '/draft', 
    component: StockDraft,
    meta: { requiresAuth: true }
  },
  {
    path: '/leaderboard',
    name: 'Leaderboard',
    component: Leaderboard
  },
  { 
    path: '/bazaar', 
    component: BazaarPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/faq',
    component: FAQPage
  },
  {
    path: '/privacy-policy',
    component: PrivacyPolicy
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters['auth/isAuthenticated']) {
      next('/login')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router