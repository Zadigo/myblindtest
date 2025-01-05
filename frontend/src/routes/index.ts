import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: async () => import('../layouts/BaseSite.vue'),
            children: [
                {
                    path: 'blind-test',
                    component: async () => import('../pages/BlindTestPage.vue'),
                    name: 'blind_test'
                },
                {
                    path: '/create',
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
                }
            ]
        }
    ]
})

router.beforeEach(() => {
    
})

export default router
