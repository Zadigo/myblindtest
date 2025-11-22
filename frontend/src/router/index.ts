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
            heightScreen: false
          }
        },
        {
          path: 'teams',
          component: async () => import('../pages/team/TeamsPage.vue'),
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
          path: 'about',
          component: async () => import('../pages/AboutPage.vue'),
          name: 'about',
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
      component: async () => import('../pages/team/IndexPage.vue'),
      name: 'blind_test'
    },
    {
      path: '/individual-blind-test',
      component: async () => import('../pages/individual/IndexPage.vue'),
      name: 'individual_blind_test'
    },
    {
      path: '/:id/single-player',
      component: async () => import('../pages/individual/PlayerPage.vue'),
      name: 'single_player'
    }
  ]
})

router.onError((error) => {
  console.error('Router error:', error)
})

export default router
