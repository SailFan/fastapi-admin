<template>
  <AppPage :show-footer="false">
    <div flex-1>
      <n-card rounded-10>
        <div flex items-center justify-between>
          <div flex items-center>
            <img rounded-full width="60" :src="userStore.avatar" />
            <div ml-10>
              <p text-20 font-semibold>
                {{ $t('views.workbench.text_hello', { username: userStore.name }) }}
              </p>
              <p mt-5 text-14 op-60>{{ $t('views.workbench.text_welcome') }}</p>
            </div>
          </div>
          <n-space :size="12" :wrap="false">
            <n-statistic v-for="item in statisticData" :key="item.id" v-bind="item"></n-statistic>
          </n-space>
        </div>
      </n-card>

      <n-card mt-15 rounded-10 size="small">
        <div flex items-center justify-between flex-wrap gap-12>
          <div>
            <p text-18 font-semibold>{{ t('views.workbench.dg_title') }}</p>
            <p mt-6 text-13 op-60>{{ t('views.workbench.dg_subtitle') }}</p>
          </div>
          <n-space :size="12" :wrap="true">
            <n-button type="primary" @click="handleCreateTask">
              <template #icon>
                <TheIcon icon="material-symbols:add" :size="18" />
              </template>
              {{ t('views.workbench.btn_create_task') }}
            </n-button>
            <n-button @click="handleUseTemplate">
              <template #icon>
                <TheIcon icon="material-symbols:folder-open-outline" :size="18" />
              </template>
              {{ t('views.workbench.btn_use_template') }}
            </n-button>
          </n-space>
        </div>
      </n-card>

      <n-grid mt-15 :cols="4" :x-gap="15" :y-gap="15">
        <n-grid-item v-for="item in kpiCards" :key="item.key">
          <n-card rounded-10 size="small">
            <div flex items-center justify-between>
              <div>
                <p text-13 op-60>{{ item.label }}</p>
                <p mt-6 text-24 font-semibold>{{ item.value }}</p>
              </div>
              <div
                class="kpi-icon"
                w-38
                h-38
                rounded-10
                flex
                items-center
                justify-center
                :style="{ background: item.bg }"
              >
                <TheIcon :icon="item.icon" :size="20" />
              </div>
            </div>
          </n-card>
        </n-grid-item>
      </n-grid>

      <n-grid mt-15 :cols="6" :x-gap="15" :y-gap="15">
        <n-grid-item :span="4">
          <n-card :title="t('views.workbench.recent_tasks')" rounded-10>
            <n-data-table
              :columns="recentTaskColumns"
              :data="recentTasks"
              :pagination="false"
              :bordered="false"
            />
          </n-card>
        </n-grid-item>
        <n-grid-item :span="2">
          <n-card :title="t('views.workbench.system_status')" rounded-10>
            <n-space vertical :size="12">
              <div flex items-center justify-between>
                <span op-60>{{ t('views.workbench.active_nodes') }}</span>
                <span font-semibold>{{ systemStatus.activeNodes }}</span>
              </div>
              <div flex items-center justify-between>
                <span op-60>{{ t('views.workbench.queue_length') }}</span>
                <span font-semibold>{{ systemStatus.queueLength }}</span>
              </div>
              <div>
                <div mb-8 flex items-center justify-between>
                  <span op-60>{{ t('views.workbench.server_load') }}</span>
                  <n-tag size="small" :type="systemStatus.loadTagType">{{ t(systemStatus.loadLabelKey) }}</n-tag>
                </div>
                <n-progress
                  type="line"
                  :percentage="systemStatus.serverLoad"
                  :height="10"
                  :border-radius="6"
                  :show-indicator="false"
                  :status="systemStatus.loadProgressStatus"
                />
              </div>
            </n-space>
          </n-card>
        </n-grid-item>
      </n-grid>

      <n-card :title="t('views.workbench.quick_access_models')" mt-15 rounded-10>
        <n-grid :cols="4" :x-gap="15" :y-gap="15">
          <n-grid-item v-for="item in quickModels" :key="item.key">
            <n-card size="small" hoverable>
              <div flex items-start gap-12>
                <div w-32 h-32 rounded-10 flex items-center justify-center :style="{ background: item.bg }">
                  <TheIcon :icon="item.icon" :size="18" />
                </div>
                <div flex-1>
                  <p font-semibold>{{ t(item.titleKey) }}</p>
                  <p mt-6 text-12 op-60>{{ t(item.descKey) }}</p>
                </div>
              </div>
              <n-button mt-10 type="primary" size="small" block @click="handleQuickGenerate(item)">
                {{ t('views.workbench.btn_generate_data') }}
              </n-button>
            </n-card>
          </n-grid-item>
        </n-grid>
      </n-card>
    </div>
  </AppPage>
</template>

<script setup>
import { useUserStore } from '@/store'
import { useI18n } from 'vue-i18n'
import { h, resolveComponent } from 'vue'
import { NButton, NSpace, NTag } from 'naive-ui'

const { t } = useI18n({ useScope: 'global' })

const statisticData = computed(() => [
  {
    id: 0,
    label: t('views.workbench.label_number_of_items'),
    value: '25',
  },
  {
    id: 1,
    label: t('views.workbench.label_upcoming'),
    value: '4/16',
  },
  {
    id: 2,
    label: t('views.workbench.label_information'),
    value: '12',
  },
])

const userStore = useUserStore()

const kpiCards = computed(() => [
  {
    key: 'today',
    label: t('views.workbench.kpi_today'),
    value: '8',
    icon: 'material-symbols:calendar-month-outline',
    bg: '#eef3ff',
  },
  {
    key: 'inProgress',
    label: t('views.workbench.kpi_in_progress'),
    value: '3',
    icon: 'material-symbols:progress-activity',
    bg: '#eefaf3',
  },
  {
    key: 'failed',
    label: t('views.workbench.kpi_failed'),
    value: '1',
    icon: 'material-symbols:error-outline',
    bg: '#fff1f1',
  },
  {
    key: 'total',
    label: t('views.workbench.kpi_total_records'),
    value: '125,400',
    icon: 'material-symbols:database',
    bg: '#f3f2ff',
  },
])

const systemStatus = reactive({
  activeNodes: 4,
  queueLength: 2,
  serverLoad: 38,
  loadLabelKey: 'views.workbench.load_normal',
  loadTagType: 'success',
  loadProgressStatus: 'success',
})

const recentTasks = ref([
  { name: 'Order Data Batch', dataModel: 'Order Model', records: 5000, status: 'completed' },
  { name: 'User Dataset', dataModel: 'User Model', records: 10000, status: 'running' },
  { name: 'Product Test Set', dataModel: 'Product Model', records: 2500, status: 'failed' },
  { name: 'Transaction Sample', dataModel: 'Transaction Model', records: 1000, status: 'completed' },
  { name: 'Demo Task', dataModel: 'Custom Model', records: 500, status: 'completed' },
])

function getStatusTagType(status) {
  if (status === 'completed') return 'success'
  if (status === 'running') return 'info'
  if (status === 'failed') return 'error'
  return 'default'
}
function getStatusLabel(status) {
  if (status === 'completed') return t('views.workbench.status_completed')
  if (status === 'running') return t('views.workbench.status_running')
  if (status === 'failed') return t('views.workbench.status_failed')
  return status
}

function handleTaskAction(action, row) {
  console.log('[workbench] action:', action, row)
}
function handleCreateTask() {
  console.log('[workbench] create task')
}
function handleUseTemplate() {
  console.log('[workbench] use template')
}

const recentTaskColumns = computed(() => {
  const TheIcon = resolveComponent('TheIcon')

  return [
    { title: t('views.workbench.col_task_name'), key: 'name' },
    { title: t('views.workbench.col_data_model'), key: 'dataModel' },
    {
      title: t('views.workbench.col_records'),
      key: 'records',
      render: (row) => row.records.toLocaleString(),
    },
    {
      title: t('views.workbench.col_status'),
      key: 'status',
      render: (row) =>
        h(
          NTag,
          { size: 'small', type: getStatusTagType(row.status) },
          { default: () => getStatusLabel(row.status) }
        ),
    },
    {
      title: t('views.workbench.col_actions'),
      key: 'actions',
      render: (row) =>
        h(
          NSpace,
          { size: 6, wrap: false },
          {
            default: () => [
              h(
                NButton,
                { quaternary: true, size: 'small', onClick: () => handleTaskAction('message', row) },
                { icon: () => h(TheIcon, { icon: 'material-symbols:mail-outline', size: 18 }), default: () => '' }
              ),
              h(
                NButton,
                { quaternary: true, size: 'small', onClick: () => handleTaskAction('view', row) },
                { icon: () => h(TheIcon, { icon: 'material-symbols:visibility-outline', size: 18 }), default: () => '' }
              ),
              h(
                NButton,
                { quaternary: true, size: 'small', onClick: () => handleTaskAction('edit', row) },
                { icon: () => h(TheIcon, { icon: 'material-symbols:edit-outline', size: 18 }), default: () => '' }
              ),
              h(
                NButton,
                { quaternary: true, size: 'small', onClick: () => handleTaskAction('more', row) },
                { icon: () => h(TheIcon, { icon: 'material-symbols:more-horiz', size: 18 }), default: () => '' }
              ),
            ],
          }
        ),
    },
  ]
})

const quickModels = computed(() => [
  {
    key: 'userProfiles',
    titleKey: 'views.workbench.model_user_profiles',
    descKey: 'views.workbench.model_user_profiles_desc',
    icon: 'material-symbols:person-outline',
    bg: '#eef3ff',
  },
  {
    key: 'orderRecords',
    titleKey: 'views.workbench.model_order_records',
    descKey: 'views.workbench.model_order_records_desc',
    icon: 'material-symbols:receipt-long-outline',
    bg: '#eefaf3',
  },
  {
    key: 'transactionData',
    titleKey: 'views.workbench.model_transaction_data',
    descKey: 'views.workbench.model_transaction_data_desc',
    icon: 'material-symbols:sync-alt',
    bg: '#f3f2ff',
  },
  {
    key: 'customModel',
    titleKey: 'views.workbench.model_custom_model',
    descKey: 'views.workbench.model_custom_model_desc',
    icon: 'material-symbols:tune',
    bg: '#fff1f1',
  },
])

function handleQuickGenerate(item) {
  console.log('[workbench] quick generate:', item)
}
</script>
