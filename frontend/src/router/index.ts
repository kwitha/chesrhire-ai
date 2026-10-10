
import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '../views/LoginView.vue'
import RecruiterLayout from '../layouts/RecruiterLayout.vue'
import DashboardView from '../views/DashboardView.vue'
import JobsView from '../views/JobsView.vue'
import ApplicationsView from '../views/ApplicationsView.vue'
import CandidateAnalysisView from '../views/CandidateAnalysisView.vue'
import SettingsView from '../views/SettingsView.vue'
import ApplicationDetailsView from '../views/ApplicationDetailsView.vue'
import CareersView from '../views/CareersView.vue'
import CareerDetailsView from '../views/CareerDetailsView.vue'
const router = createRouter({
  history: createWebHistory(),

  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/careers',
      name: 'careers',
      component: CareersView,
      meta: { requiresAuth: false },
    },
    {
      path: '/careers/:id',
      name: 'career-details',
      component: CareerDetailsView,
      meta: { requiresAuth: false },
    },
    {
      path: '/careers/:id/apply',
      name: 'career-apply',
      component: () => import('../views/CareerApplicationView.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/',
      component: RecruiterLayout,
      meta: { requiresAuth: true },

      children: [
        {
          path: 'dashboard',
          name: 'dashboard',
          component: DashboardView,
        },
        {
          path: 'jobs',
          name: 'jobs',
          component: JobsView,
        },
        {
          path: 'applications',
          name: 'applications',
          component: ApplicationsView,
        },
        {
          path: 'applications/:id',
          name: 'application-details',
          component: ApplicationDetailsView,
        },
        {
          path: 'analysis',
          name: 'analysis',
          component: CandidateAnalysisView,
        },
        {
          path: 'settings',
          name: 'settings',
          component: SettingsView,
        },
      ],
    },
  ],
})

router.beforeEach((to) => {
  const token = localStorage.getItem('access_token')

  const requiresAuth = to.matched.some(
    (record) => record.meta.requiresAuth,
  )

  if (requiresAuth && !token) {
    return { name: 'login' }
  }

  return true
})

export default router
