<template>
  <header class="header" :class="{ 'header--collapsed': isSidebarCollapsed }">
    <div class="header__left">
      <h5 class="header__greeting">{{ $t('header.greeting', { name: userName }) }}</h5>
      <span class="header__slogan">
        {{ $t('header.slogan') }}
      </span>
    </div>

    <div class="header__right">
      <div class="header__system">
        <div class="header__noti">
          <span class="foxgo-icon noti"></span>
        </div>
        <div class="header__language" @click="changeLanguage">
          <span class="foxgo-icon flag-eng" v-if="locale === 'vi'"></span>
          <span class="foxgo-icon flag-vn" v-if="locale === 'en'"></span>
        </div>
        <div class="header__user" @click="toggleDropdown" v-click-outside="closeDropdown">
          <div class="header__user-avatar">{{ userInitials }}</div>
          <span class="foxgo-icon material-icons" :class="{ 'header__user-arrow--open': isDropdownOpen }">expand_more</span>
          
          <!-- User Dropdown Menu -->
          <Transition name="dropdown">
            <div v-if="isDropdownOpen" class="header__dropdown">
              <div class="header__dropdown-header">
                <div class="header__dropdown-avatar">{{ userInitials }}</div>
                <div class="header__dropdown-info">
                  <span class="header__dropdown-name">{{ userName }}</span>
                  <span class="header__dropdown-email">{{ userEmail }}</span>
                </div>
              </div>
              <div class="header__dropdown-divider"></div>
              <ul class="header__dropdown-menu">
                <li class="header__dropdown-item">
                  <router-link to="/settings" class="header__dropdown-link" @click="closeDropdown">
                    <span class="foxgo-icon setting"></span>
                    <span>{{ $t('menu.label.setting') }}</span>
                  </router-link>
                </li>
                <li class="header__dropdown-item">
                  <router-link to="/help" class="header__dropdown-link" @click="closeDropdown">
                    <span class="foxgo-icon support"></span>
                    <span>{{ $t('menu.label.support') }}</span>
                  </router-link>
                </li>
              </ul>
              <div class="header__dropdown-divider"></div>
              <button class="header__dropdown-logout" @click="handleLogout">
                <span class="foxgo-icon logout"></span>
                <span>{{ $t('menu.label.logout') }}</span>
              </button>
            </div>
          </Transition>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useCommonStore, useAuthStore } from '@/stores'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

const commonStore = useCommonStore()
const authStore = useAuthStore()

const isSidebarCollapsed = computed(() => commonStore.isSidebarCollapsed)
const currentUser = computed(() => authStore.currentUser)
const userName = computed(() => currentUser.value?.name || currentUser.value?.username || 'Guest')
const userEmail = computed(() => currentUser.value?.email || '')
const userInitials = computed(() => {
  const name = userName.value
  if (!name || name === 'Guest') return 'G'
  const parts = name.split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
  }
  return name.substring(0, 2).toUpperCase()
})

// Dropdown state
const isDropdownOpen = ref(false)

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value
}

const closeDropdown = () => {
  isDropdownOpen.value = false
}

const changeLanguage = () => {
  locale.value = locale.value === 'vi' ? 'en' : 'vi'
}

const handleLogout = async () => {
  closeDropdown()
  if (confirm('Bạn có chắc chắn muốn đăng xuất?')) {
    try {
      await authStore.logout()
    } catch (error) {
      console.error('Logout error:', error)
    }
  }
}

// Custom directive for click outside
const vClickOutside = {
  mounted(el, binding) {
    el._clickOutside = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value()
      }
    }
    document.addEventListener('click', el._clickOutside)
  },
  unmounted(el) {
    document.removeEventListener('click', el._clickOutside)
  }
}
</script>
