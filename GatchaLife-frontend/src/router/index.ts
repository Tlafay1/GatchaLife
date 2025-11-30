import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: () => import('@/gamification/Dashboard.vue')
    },
    {
      path: '/collection',
      name: 'collection',
      component: () => import('@/gamification/Collection.vue')
    },
    {
      path: '/collection/:id',
      name: 'card-details',
      component: () => import('../gamification/CardDetails.vue')
    },
    {
      path: '/studio',
      name: 'creator-studio',
      component: () => import('../gamification/CreatorStudio.vue')
    },
    {
      path: '/characters',
      name: 'characters',
      component: () => import('@/character/views/CharacterListView.vue')
    },
    {
      path: '/series',
      name: 'series-list',
      component: () => import('@/series/views/SeriesListView.vue')
    },
    {
      path: '/character/new',
      name: 'character-new',
      component: () => import('@/character/views/CharacterEditor.vue')
    },
    {
      path: '/character/:id/edit',
      name: 'character-edit',
      component: () => import('@/character/views/CharacterEditor.vue'),
      props: true
    }
  ],
})

export default router
