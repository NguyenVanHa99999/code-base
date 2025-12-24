<template>
  <aside class="sidebar" :class="{ 'sidebar--collapsed': isSidebarCollapsed }">
    <div class="sidebar__logo">
      <img src="@/assets/images/foxgo-logo.png" alt="Foxgo" />
      <span class="sidebar__logo-text" v-show="!isSidebarCollapsed">Foxgo</span>
      <button
        class="sidebar__toggle"
        :class="{ 'sidebar__toggle--collapsed': isSidebarCollapsed }"
        @click="commonStore.toggleSidebar"
      >
        <span class="foxgo-icon material-icons">chevron_left</span>
      </button>
    </div>

    <nav class="sidebar__nav">
      <ul class="sidebar__menu">
        <li
          v-for="item in menuLnbList"
          :key="item.id"
          class="sidebar__menu-item"
          :class="{ 'sidebar__menu-item--expandable': hasChildren(item) }"
          @mouseenter="handleMouseEnter(item, $event)"
          @mouseleave="handleMouseLeave"
        >
          <component
            :is="hasChildren(item) ? 'div' : 'router-link'"
            :to="!hasChildren(item) ? item.to : undefined"
            class="sidebar__menu-link"
            @click="hasChildren(item) ? toggleExpand(item) : null"
          >
            <span
              class="foxgo-icon"
              :class="{
                [item.icon]: true
              }"
            ></span>
            <span class="sidebar__menu-text" v-show="!isSidebarCollapsed">{{ $t(item.name) }}</span>
            <div class="sidebar__menu-arrow" v-if="!isSidebarCollapsed && hasChildren(item)">
              <span class="foxgo-icon material-icons">
                {{ isExpanded(item) ? 'expand_less' : 'expand_more' }}
              </span>
            </div>
          </component>

          <template v-if="item.children && !isSidebarCollapsed && isExpanded(item)">
            <ul class="sidebar__submenu">
              <li
                v-for="child in item.children"
                :key="`${item.id}-${child.id}`"
                class="sidebar__submenu-item"
              >
                <router-link :to="child.to" class="sidebar__submenu-link">
                  <span v-if="child.icon" class="sidebar__submenu-icon">{{ child.icon }}</span>
                  <span class="sidebar__submenu-text">{{ $t(child.name) }}</span>
                </router-link>
              </li>
            </ul>
          </template>
        </li>
      </ul>

      <Teleport to="body">
        <Transition name="submenu-popup">
          <div
            v-if="hoveredItem && isSidebarCollapsed"
            class="sidebar__submenu-popup"
            :style="{
              top: `${popupPosition.top}px`,
              left: `${popupPosition.left}px`
            }"
            @mouseenter="handlePopupMouseEnter"
            @mouseleave="handlePopupMouseLeave"
          >
            <ul class="sidebar__submenu-popup-list">
              <li
                v-for="child in hoveredItem.children"
                :key="`${hoveredItem.id}-${child.id}-popup`"
                class="sidebar__submenu-popup-item"
              >
                <router-link :to="child.to" class="sidebar__submenu-popup-link">
                  <span v-if="child.icon" class="sidebar__submenu-icon">{{ child.icon }}</span>
                  <span class="sidebar__submenu-text">{{ $t(child.name) }}</span>
                </router-link>
              </li>
            </ul>
          </div>
        </Transition>
      </Teleport>

      <div class="sidebar__footer">
        <ul class="sidebar__menu">
          <li class="sidebar__menu-item">
            <a href="#" class="sidebar__menu-link">
              <span class="foxgo-icon support"></span>
              <span class="sidebar__menu-text" v-show="!isSidebarCollapsed">{{
                $t('menu.label.support')
              }}</span>
            </a>
          </li>
          <li class="sidebar__menu-item">
            <a href="#" class="sidebar__menu-link">
              <span class="foxgo-icon setting"></span>
              <span class="sidebar__menu-text" v-show="!isSidebarCollapsed">{{
                $t('menu.label.setting')
              }}</span>
            </a>
          </li>
          <li class="sidebar__menu-item">
            <a href="#" class="sidebar__menu-link">
              <span class="foxgo-icon logout"></span>
              <span class="sidebar__menu-text" v-show="!isSidebarCollapsed">{{
                $t('menu.label.logout')
              }}</span>
            </a>
          </li>
        </ul>
      </div>
    </nav>
  </aside>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useCommonStore } from '@/stores'

const commonStore = useCommonStore()

const isSidebarCollapsed = computed(() => commonStore.isSidebarCollapsed)
const menuLnbList = computed(() => commonStore.getMenuLnbList)

const expandedItems = ref(new Set())
const hoveredItem = ref(null)
const popupPosition = ref({ top: 0, left: 0 })
const isHoveringPopup = ref(false)
let closeTimeout = null

const toggleExpand = (item) => {
  if (isSidebarCollapsed.value) {
    return
  }

  if (expandedItems.value.has(item.id)) {
    expandedItems.value.delete(item.id)
  } else {
    expandedItems.value.add(item.id)
  }
}

const isExpanded = (item) => {
  return expandedItems.value.has(item.id)
}

const hasChildren = (item) => {
  return item.children && item.children.length > 0
}

const handleMouseEnter = (item, event) => {
  if (isSidebarCollapsed.value && hasChildren(item)) {
    if (closeTimeout) {
      clearTimeout(closeTimeout)
      closeTimeout = null
    }

    hoveredItem.value = item

    const target = event.currentTarget
    const rect = target.getBoundingClientRect()
    popupPosition.value = {
      top: rect.top,
      left: rect.right + 16
    }
  }
}

const handleMouseLeave = () => {
  if (isSidebarCollapsed.value) {
    closeTimeout = setTimeout(() => {
      if (!isHoveringPopup.value) {
        hoveredItem.value = null
      }
    }, 100)
  }
}

const handlePopupMouseEnter = () => {
  isHoveringPopup.value = true
  if (closeTimeout) {
    clearTimeout(closeTimeout)
    closeTimeout = null
  }
}

const handlePopupMouseLeave = () => {
  isHoveringPopup.value = false
  hoveredItem.value = null
}
</script>

<style lang="scss" scoped>
@use '@/assets/scss/base/variables' as *;
@use '@/assets/scss/base/mixin' as *;

.sidebar__menu-item {
  position: relative;
}

.sidebar__submenu-popup {
  position: fixed;
  min-width: 200px;
  background-color: $color-bg-primary;
  border: 1px solid $gray-200;
  border-radius: $border-radius-base;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  overflow: hidden;

  &-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 20px;
    border-bottom: 1px solid $gray-200;
    background-color: $primary-50;

    .foxgo-icon {
      font-size: 2rem;
      color: $primary-600;
    }
  }

  &-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: $primary-600;
    white-space: nowrap;
  }

  &-list {
    padding: 8px 0;
  }

  &-item {
    list-style: none;
  }

  &-link {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 11px 20px;
    color: $color-text-secondary;
    text-decoration: none;
    @include transition(0.2s);
    font-size: 1.4rem;
    font-weight: 600;
    cursor: pointer;

    &:hover,
    &.router-link-active {
      background-color: $primary-50;
      color: $primary-600;
    }
  }
}

.submenu-popup-enter-active,
.submenu-popup-leave-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}

.submenu-popup-enter-from {
  opacity: 0;
  transform: translateX(-10px);
}

.submenu-popup-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

.submenu-popup-enter-to,
.submenu-popup-leave-from {
  opacity: 1;
  transform: translateX(0);
}
</style>
