<template>
  <header class="header" :class="{ 'header--collapsed': isSidebarCollapsed }">
    <div class="header__left">
      <h5 class="header__greeting">Xin chào, {{ userName }}</h5>
      <span class="header__slogan">
        Chào mừng bạn dến với Foxgo! Chọn lộ trình, học theo tốc độ của bạn, vui mỗi ngày!
      </span>
    </div>

    <div class="header__right">
      <div class="header__points">
        <div class="header__points--item">
          <span class="foxgo-icon streak"></span>
          <span class="header__points-value header__points-value--streak">10</span>
        </div>
        <div class="header__points--item">
          <span class="foxgo-icon diamond"></span>
          <span class="header__points-value header__points-value--diamond">10</span>
        </div>
      </div>
      <div class="header__system">
        <div class="header__noti">
          <span class="foxgo-icon noti"></span>
        </div>
        <div class="header__language" @click="changeLanguage">
          <span class="foxgo-icon flag-eng" v-if="locale === 'vi'"></span>
          <span class="foxgo-icon flag-vn" v-if="locale === 'en'"></span>
        </div>
        <div class="header__user">
          <div class="header__user-avatar">HN</div>
          <span class="foxgo-icon material-icons">expand_more</span>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useCommonStore } from '@/stores'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

const commonStore = useCommonStore()
const isSidebarCollapsed = computed(() => commonStore.isSidebarCollapsed)
const userName = computed(() => 'ThangLD')

const changeLanguage = () => {
  locale.value = locale.value === 'vi' ? 'en' : 'vi'
}
</script>
