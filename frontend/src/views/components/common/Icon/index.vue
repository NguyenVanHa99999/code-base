<template>
  <span class="foxgo-icon material-icons" :style="{ fontSize: size }">{{ icon }}</span>
</template>

<script setup>
const props = defineProps({
  icon: {
    type: String,
    required: true
  },
  size: {
    type: String,
    default: '24px'
  }
})
</script>
