import { createRouter, createWebHistory } from 'vue-router'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { useAuthStore } from '@/stores'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/pages/Auth/LoginPage.vue')
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/pages/Auth/RegisterPage.vue')
    },
    {
      path: '/',
      name: 'root',
      component: DashboardLayout,
      children: [
        {
          path: '',
          name: 'HomePage',
          component: () => import('@/views/pages/Home/HomePage.vue')
        }
      ]
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  const publicPages = ['Login', 'Register', 'NotFound']
  const authRequired = !publicPages.includes(to.name)

  // For protected pages, verify auth with server (cookie-based)
  if (authRequired) {
    const isValid = await authStore.checkAuth()
    if (!isValid) {
      return next({ name: 'Login' })
    }
  }

  // Redirect to home if already authenticated and trying to access login/register
  // Only check if we already have verified auth (avoid unnecessary API calls)
  if ((to.name === 'Login' || to.name === 'Register') && authStore.isAuthenticated) {
    return next({ name: 'HomePage' })
  }

  next()
})

export default router
