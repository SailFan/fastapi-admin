<template>
  <AppPage :show-footer="false">
    <CommonPage :title="title">
      <n-card rounded-10>
        <div text-14 op-70>
          {{ subtitle || '该页面已生成占位文件，可开始实现具体功能。' }}
        </div>
      </n-card>
    </CommonPage>
  </AppPage>
</template>

<script setup>
import CommonPage from '@/components/page/CommonPage.vue'

defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: '',
  },
})
</script>
