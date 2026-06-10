import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      meta: { title: 'Home' },
      component: () => import('@/pages/HomePage.vue')
    },
    {
      path: '/scores',
      name: 'scores',
      meta: { title: 'Scores' },  
      component: () => import('@/pages/ScoresPage.vue')
    }
  ]
})

router.beforeEach((to, _from, next) => {
  if (to.name === 'scores') {
    const { sessionId } = useSession()
    if (!isDefined(sessionId)) {
      next({ name: 'home' })
      return
    }
  }
  next()
})

export default router
