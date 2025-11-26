import type { LocalTypes } from '@/i18n'
import { i18n, SUPPORT_LOCALES } from '@/i18n'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: `/${SUPPORT_LOCALES[1]}`
    },
    {
      path: '/:locale',
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
        }
      ]
    },
    {
      path: '/:locale/:id/blind-test',
      component: async () => import('../pages/blindtest/IndexPage.vue'),
      name: 'blind_test'
    },
    {
      path: '/:locale/:id/player',
      component: async () => import('../pages/blindtest/PlayerPage.vue'),
      name: 'player_page'
    },
    {
      path: '/:locale/(.*)',
      component: async () => import('../pages/ErrorPage.vue'),
      name: 'error',
      meta: {
        heightScreen: true
      }
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const locale = to.params.locale as LocalTypes
  if (locale) {
    i18n.global.locale.value = locale
  }

  return next()
})

router.onError((error) => {
  console.error('Router error:', error)
})

export default router
