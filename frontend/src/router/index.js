import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'root',
      component: () => import('@/layouts/DashboardLayout.vue'),
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
  console.log('to', to)
  const publicPages = ['Login', 'ErrorPage']
  const authRequired = !publicPages.includes(to.name)

  next()
})

export default router
