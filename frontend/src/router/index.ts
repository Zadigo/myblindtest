import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: async () => import('../layouts/BaseSite.vue'),
      children: [
        {
          path: '',
          component: async () => import('../pages/HomePage.vue'),
          name: 'home',
          meta: {
            heightScreen: true
          }
        },
        {
          path: 'teams',
          component: async () => import('../pages/TeamsPage.vue'),
          name: 'teams',
          meta: {
            heightScreen: true
          }
        },
        {
          path: 'create',
          component: async () => import('../pages/CreateSongsPage.vue'),
          name: 'create',
          meta: {
            heightScreen: false
          }
        },
        {
          path: 'statistics',
          component: async () => import('../pages/StatisticsPage.vue'),
          name: 'statistics',
          meta: {
            heightScreen: true
          }
        },
        {
          path: 'registration',
          component: async () => import('../pages/RegisterPlayerPage.vue'),
          name: 'registration',
          meta: {
            heightScreen: true
          }
        },
        {
          path: '(.*)',
          component: async () => import('../pages/ErrorPage.vue'),
          name: 'error',
          meta: {
            heightScreen: true
          }
        }
      ]
    },
    {
      path: '/blind-test',
      component: async () => import('../pages/BlindTestPage.vue'),
      name: 'blind_test'
    }
  ]
})

router.onError((error) => {
  console.error('Router error:', error)
})

export default router
