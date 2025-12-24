import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

const useCommonStore = defineStore('common', () => {
  const isSidebarCollapsed = ref(false)

  const menuLnbList = ref([
    {
      id: 1,
      name: 'menu.label.home',
      icon: 'school',
      to: '/'
    },
    {
      id: 2,
      name: 'menu.label.mission',
      icon: 'mission',
      to: '/mission'
    },
    {
      id: 3,
      name: 'menu.label.lesson',
      icon: 'learn',
      to: '/lesson'
    },
    {
      id: 4,
      name: 'menu.label.practice',
      icon: 'book',
      to: '/practice'
    },
    {
      id: 5,
      name: 'menu.label.evaluate',
      icon: 'result',
      to: '/evaluate',
      children: []
    },
    {
      id: 6,
      name: 'menu.label.subject',
      icon: 'subject',
      to: '/subject'
    },
    {
      id: 7,
      name: 'menu.label.myClass',
      icon: 'class',
      to: '/my-class',
      children: [
        {
          id: 1,
          name: 'menu.label.k12',
          to: '/my-class'
        },
        {
          id: 2,
          name: 'menu.label.foreignLanguage',
          to: '/my-class'
        }
      ]
    },
    {
      id: 8,
      name: 'menu.label.more',
      icon: 'more',
      to: '/more',
      children: []
    }
  ])

  const getMenuLnbList = computed(() => menuLnbList.value)

  const toggleSidebar = () => {
    isSidebarCollapsed.value = !isSidebarCollapsed.value
  }

  const setMenuLnbList = (list) => {
    menuLnbList.value = list.map((item, index) => ({ ...item, id: index + 1 }))
  }

  return {
    isSidebarCollapsed,
    getMenuLnbList,
    setMenuLnbList,
    toggleSidebar
  }
})

export default useCommonStore
