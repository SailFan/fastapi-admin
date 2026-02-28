<script setup>
import { renderIcon } from '@/utils'

defineProps({
  icon: {
    type: String,
    required: true,
  },
  size: {
    type: Number,
    default: 14,
  },
  color: {
    type: String,
    default: undefined,
  },
})

// 全局禁用图标显示
const showIcon = false
</script>

<template>
  <!-- 全局禁用图标，不渲染任何内容 -->
  <component v-if="showIcon" :is="renderIcon(icon, { size, color })" />
</template>
