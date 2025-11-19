import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
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
