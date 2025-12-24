<template>
  <div>
    <Header />
    <router-view></router-view>
  </div>
</template>

<script setup>
import Header from '@/views/sections/layout/Header.vue'
import { RouterView } from 'vue-router'
</script>

<style lang="scss" scoped></style>
