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
          path: 'test',
          component: async () => import('../pages/TestPage.vue'),
          name: 'test'
        },
        {
          path: 'design',
          component: async () => import('../pages/DesignPage.vue'),
          name: 'design'
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

export default router
