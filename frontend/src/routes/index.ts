import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: async () => import('../layouts/BaseSite.vue'),
            children: [
                {
                    path: '',
                    redirect: '/blind-test'
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
                }
            ]
        },
        {
            path: '/blind-test',
            component: async () => import('../layouts/BlindTestLayout.vue'),
            children: [
                {
                    path: '',
                    component: async () => import('../pages/BlindTestPage.vue'),
                    name: 'blind_test'
                },
                {
                    path: 'settings',
                    component: async () => import('../pages/SettingsPage.vue'),
                    name: 'settings'
                }
            ]
        }
    ]
})

router.beforeEach(() => {
    
})

export default router
