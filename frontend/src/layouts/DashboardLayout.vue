<template>
  <div class="wrapper" :class="{ 'wrapper--collapsed': isSidebarCollapsed }">
    <Header />
    <Sidebar />
    <div class="dashboard-layout">
      <div class="dashboard-layout__main">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { RouterView } from 'vue-router'
import { useCommonStore } from '@/stores'

import Header from '@/views/sections/layout/Header.vue'
import Sidebar from '@/views/sections/layout/Sidebar.vue'

const commonStore = useCommonStore()
const isSidebarCollapsed = computed(() => commonStore.isSidebarCollapsed)
</script>
