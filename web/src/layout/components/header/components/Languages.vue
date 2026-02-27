<template>
  <n-dropdown :options="options" @select="handleChangeLocale">
    <n-icon mr-20 size="18" style="cursor: pointer">
      <icon-mdi:globe />
    </n-icon>
  </n-dropdown>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useAppStore } from '@/store'
import { router } from '~/src/router'
import i18n from '~/i18n'

const store = useAppStore()
const { availableLocales } = useI18n()

const options = computed(() => {
  let select = []
  availableLocales.forEach((locale) => {
    select.push({
      label: i18n.global.getLocaleMessage(locale)?.lang || locale,
      key: locale,
    })
  })
  return select
})

const handleChangeLocale = (value) => {
  store.setLocale(value)
  // reload page
  router.go()
}
</script>
