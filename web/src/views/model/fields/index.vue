<script setup>
import { h, onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  NButton,
  NForm,
  NFormItem,
  NInput,
  NSelect,
  NSwitch,
  NInputNumber,
  NTag,
  NPopconfirm,
  NEmpty,
} from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'

import { formatDate } from '@/utils'
import { useCRUD } from '@/composables'
import api from '@/api'

defineOptions({ name: '字段定义' })

const route = useRoute()
const $table = ref(null)
const queryItems = ref({})

// 从路由获取 entity_id
const entityId = computed(() => route.query.entity_id ? parseInt(route.query.entity_id) : null)

const {
  modalVisible,
  modalTitle,
  modalAction,
  modalLoading,
  handleSave,
  modalForm,
  modalFormRef,
  handleEdit,
  handleDelete,
  handleAdd,
} = useCRUD({
  name: '字段',
  initForm: { 
    entity_id: entityId.value,
    is_required: true,
    scope: 'single',
    order: 0,
  },
  doCreate: api.createField,
  doUpdate: api.updateField,
  doDelete: api.deleteField,
  refresh: () => $table.value?.handleSearch(),
})

onMounted(() => {
  if (!entityId.value) {
    $message.error('缺少实体ID参数')
    return
  }
  $table.value?.handleSearch()
})

// 字段类型选项
const typeOptions = ref([])

async function loadMetaData(){
  try{
    const res = await api.getMetadata()
    typeOptions.value = res.data.field_types
    console.log(typeOptions.value)
  }catch(err){
    $message.error('加载字段类型失败：' + err.message)
  }
}

const handleaddWithMetaData = async() => {
  if(!typeOptions.value.length){
    await loadMetaData()
  }
  handleAdd()
}


// 生成模式选项
const scopeOptions = [
  { label: 'single - 单个', value: 'single' },
  { label: 'batch - 批量', value: 'batch' },
  { label: 'optional - 可选', value: 'optional' },
]

const columns = [
  {
    title: '序号',
    key: 'order',
    width: 80,
    align: 'center',
  },
  {
    title: '字段名称',
    key: 'name',
    width: 150,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '类型',
    key: 'type',
    width: 100,
    align: 'center',
    render(row) {
      const typeMap = {
        string: 'info',
        int: 'success',
        float: 'warning',
        date: 'error',
        enum: 'default',
        json: 'primary',
      }
      return h(NTag, { type: typeMap[row.type] || 'default' }, { default: () => row.type })
    },
  },
  {
    title: '关联实体',
    key: 'related_entity',
    width: 120,
    align: 'center',
    render(row) {
      return row.related_entity || '-'
    },
  },
  {
    title: '策略',
    key: 'scope',
    width: 100,
    align: 'center',
    render(row) {
      return h(NTag, { size: 'small' }, { default: () => row.scope })
    },
  },
  {
    title: '分布形式',
    key: 'distribution',
    width: 120,
    align: 'center',
    render(row) {
      return row.distribution || '-'
    },
  },
  {
    title: '必填',
    key: 'is_required',
    width: 80,
    align: 'center',
    render(row) {
      return h(
        NTag,
        { type: row.is_required ? 'error' : 'default', size: 'small' },
        { default: () => (row.is_required ? '是' : '否') }
      )
    },
  },
  {
    title: '默认值',
    key: 'default_value',
    width: 120,
    align: 'center',
    ellipsis: { tooltip: true },
    render(row) {
      return row.default_value || '-'
    },
  },
  {
    title: '描述',
    key: 'description',
    width: 200,
    align: 'center',
    ellipsis: { tooltip: true },
    render(row) {
      return row.description || '-'
    },
  },
  {
    title: '更新时间',
    key: 'updated_at',
    align: 'center',
    width: 150,
    render(row) {
      return formatDate(row.updated_at)
    },
  },
  {
    title: '字段校验',
    key: 'validation',
    width: 100,
    align: 'center',
    render(row) {
      return row.validation || '-'
    },
  },
  {
    title: '操作',
    key: 'actions',
    width: 150,
    align: 'center',
    fixed: 'right',
    render(row) {
      return [
        h(
          NButton,
          {
            size: 'small',
            type: 'primary',
            style: 'margin-right: 8px;',
            onClick: () => handleEdit(row),
          },
          { default: () => '编辑' }
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ field_id: row.id }, false),
          },
          {
            trigger: () =>
              h(
                NButton,
                {
                  size: 'small',
                  type: 'error',
                },
                { default: () => '删除' }
              ),
            default: () => h('div', {}, '确定删除该字段吗？'),
          }
        ),
      ]
    },
  },
]

// 自定义获取数据函数
async function getFieldList(params) {
  if (!entityId.value) {
    return { data: [], total: 0 }
  }
  return await api.getFieldList({ ...params, entity_id: entityId.value })
}

const validateForm = {
  name: [
    {
      required: true,
      message: '请输入字段名称',
      trigger: ['input', 'blur'],
    },
  ],
  type: [
    {
      required: true,
      message: '请选择字段类型',
      trigger: ['change', 'blur'],
    },
  ],
}
</script>

<template>
  <CommonPage show-footer title="字段定义">
    <template #action>
      <NButton type="primary" @click="handleaddWithMetaData">
        新建字段
      </NButton>
    </template>

    <!-- 表格 -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="getFieldList"
    >
      <template #queryBar>
        <QueryBarItem label="字段名称" :label-width="80">
          <NInput
            v-model:value="queryItems.name"
            clearable
            type="text"
            placeholder="请输入字段名称"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="关联实体" :label-width="100">
          <NInput
            v-model:value="queryItems.related_entity"
            clearable
            type="text"
            placeholder="请输入关联实体"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
      </template>

      <!-- 空状态 -->
      <template #empty>
        <NEmpty description="暂无字段数据">
          <template #extra>
            <NButton type="primary" @click="handleAdd">
              新建按键
            </NButton>
          </template>
        </NEmpty>
      </template>
    </CrudTable>

    <!-- 新增/编辑 弹窗 -->
    <CrudModal
      v-model:visible="modalVisible"
      :title="modalTitle"
      :loading="modalLoading"
      @save="handleSave"
    >
      <NForm
        ref="modalFormRef"
        label-placement="left"
        label-align="left"
        :label-width="100"
        :model="modalForm"
        :rules="validateForm"
      >
        <NFormItem label="字段名称" path="name">
          <NInput v-model:value="modalForm.name" clearable placeholder="请输入字段名称，如：email" />
        </NFormItem>
        <NFormItem label="类型" path="type">
          <NSelect
            v-model:value="modalForm.type"
            :options="typeOptions"
            placeholder="请选择字段类型"
          />
        </NFormItem>
        <NFormItem label="关联实体" path="related_entity">
          <NInput
            v-model:value="modalForm.related_entity"
            clearable
            placeholder="请输入关联实体"
          />
        </NFormItem>
        <NFormItem label="策略" path="scope">
          <NSelect
            v-model:value="modalForm.scope"
            :options="scopeOptions"
            placeholder="请选择生成模式"
          />
        </NFormItem>
        <NFormItem label="分布形式" path="distribution">
          <NInput
            v-model:value="modalForm.distribution"
            clearable
            placeholder="请输入分布形式"
          />
        </NFormItem>
        <NFormItem label="必填" path="is_required">
          <NSwitch
            v-model:value="modalForm.is_required"
            :checked-value="true"
            :unchecked-value="false"
          />
        </NFormItem>
        <NFormItem label="默认值" path="default_value">
          <NInput
            v-model:value="modalForm.default_value"
            clearable
            placeholder="请输入默认值或占位值"
          />
        </NFormItem>
        <NFormItem label="最小长度" path="min_length">
          <NInputNumber
            v-model:value="modalForm.min_length"
            :min="0"
            placeholder="字段生成的最小长度"
            style="width: 100%"
          />
        </NFormItem>
        <NFormItem label="最大长度" path="max_length">
          <NInputNumber
            v-model:value="modalForm.max_length"
            :min="0"
            placeholder="字段生成的最大长度"
            style="width: 100%"
          />
        </NFormItem>
        <NFormItem label="字段校验" path="validation">
          <NInput
            v-model:value="modalForm.validation"
            clearable
            placeholder="请输入字段校验规则"
          />
        </NFormItem>
        <NFormItem label="描述" path="description">
          <NInput
            v-model:value="modalForm.description"
            type="textarea"
            :rows="3"
            clearable
            placeholder="请输入字段说明"
          />
        </NFormItem>
        <!-- <NFormItem label="字段顺序" path="order">
          <NInputNumber
            v-model:value="modalForm.order"
            :min="0"
            placeholder="字段显示顺序"
            style="width: 100%"
          />
        </NFormItem> -->
      </NForm>
    </CrudModal>
  </CommonPage>
</template>
