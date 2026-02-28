import { h } from 'vue'
import { Icon } from '@iconify/vue'
import { NIcon } from 'naive-ui'
import SvgIcon from '@/components/icon/SvgIcon.vue'

export function renderIcon(icon, props = { size: 12 }) {
  // 全局禁用图标，返回 null
  return null
  
  // 如果需要显示图标，注释掉上面的 return null，取消下面的注释
  // return () => h(NIcon, props, { default: () => h(Icon, { icon }) })
}

export function renderCustomIcon(icon, props = { size: 12 }) {
  // 全局禁用图标，返回 null
  return null
  
  // 如果需要显示图标，注释掉上面的 return null，取消下面的注释
  // return () => h(NIcon, props, { default: () => h(SvgIcon, { icon }) })
}
