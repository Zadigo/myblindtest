import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: async () => import('../layouts/BaseSite.vue'),
      children: [
        {
          path: '',
          component: async () => import('../pages/HomePage.vue'),
          name: 'home'
        },
        {
          path: 'teams',
          component: async () => import('../pages/TeamsPage.vue'),
          name: 'teams'
        },
        {
          path: 'create',
          component: async () => import('../pages/CreateSongsPage.vue'),
          name: 'create'
        },
        {
          path: 'statistics',
          component: async () => import('../pages/StatisticsPage.vue'),
          name: 'statistics'
        },
        {
          path: 'registration',
          component: async () => import('../pages/RegisterPlayerPage.vue'),
          name: 'registration'
        },
        {
          path: '(.*)',
          component: async () => import('../pages/ErrorPage.vue'),
          name: 'error'
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
