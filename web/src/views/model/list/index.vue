<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
import { useRouter } from 'vue-router'
import {
  NButton,
  NForm,
  NFormItem,
  NInput,
  NSelect,
  NTag,
  NPopconfirm,
  NEmpty,
  NSpace,
  NInputGroup,
} from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import TheIcon from '@/components/icon/TheIcon.vue'

import { formatDate, renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
import api from '@/api'

defineOptions({ name: '模型列表' })

const router = useRouter()
const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')

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
  name: '模型',
  initForm: { tags: {} },
  doCreate: api.createEntity,
  doUpdate: api.updateEntity,
  doDelete: api.deleteEntity,
  refresh: () => $table.value?.handleSearch(),
})

onMounted(() => {
  $table.value?.handleSearch()
})

// 分类选项
const categoryOptions = [
  { label: '全部', value: '' },
  { label: '业务实体', value: '业务实体' },
  { label: '系统实体', value: '系统实体' },
  { label: '测试实体', value: '测试实体' },
]

const columns = [
  {
    title: '模型名称',
    key: 'name',
    width: 120,
    align: 'center',
    ellipsis: { tooltip: true },
    render(row) {
      return h(
        NButton,
        {
          text: true,
          type: 'primary',
          onClick: () => router.push({ path: '/model/detail', query: { id: row.id } }),
        },
        { default: () => row.name }
      )
    },
  },
  {
    title: '分类',
    key: 'category',
    width: 100,
    align: 'center',
    render(row) {
      return row.category
        ? h(NTag, { type: 'info' }, { default: () => row.category })
        : h('span', '-')
    },
  },
  {
    title: '字段数量',
    key: 'field_count',
    width: 80,
    align: 'center',
    render(row) {
      return h(
        NTag,
        { type: 'success' },
        { default: () => row.field_count || 0 }
      )
    },
  },
  {
    title: '关系数量',
    key: 'relation_count',
    width: 80,
    align: 'center',
    render(row) {
      return h(
        NTag,
        { type: 'warning' },
        { default: () => row.relation_count || 0 }
      )
    },
  },
  {
    title: '标签',
    key: 'tags',
    width: 150,
    align: 'center',
    ellipsis: { tooltip: true },
    render(row) {
      if (!row.tags || Object.keys(row.tags).length === 0) {
        return h('span', '-')
      }
      const tags = []
      for (const [key, value] of Object.entries(row.tags)) {
        tags.push(
          h(
            NTag,
            { size: 'small', type: 'info', style: { margin: '2px' } },
            { default: () => `${key}: ${value}` }
          )
        )
      }
      return h('div', tags)
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
    title: '操作',
    key: 'actions',
    width: 240,
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
          NButton,
          {
            size: 'small',
            type: 'info',
            style: 'margin-right: 8px;',
            onClick: () => handleCopy(row),
          },
          { default: () => '复制' }
        ),
        h(
          NButton,
          {
            size: 'small',
            type: 'success',
            style: 'margin-right: 8px;',
            onClick: () => router.push({ path: '/model/detail', query: { id: row.id } }),
          },
          { default: () => '详情' }
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ entity_id: row.id }, false),
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
            default: () => h('div', {}, '确定删除该模型吗？'),
          }
        ),
      ]
    },
  },
]

// 复制模型
async function handleCopy(row) {
  modalAction.value = 'add'
  modalTitle.value = '复制模型'
  modalForm.value = {
    name: `${row.name}_copy`,
    category: row.category,
    tags: row.tags || {},
    description: row.description,
  }
  modalVisible.value = true
}

// 自定义获取数据函数，添加字段数量统计
async function getEntityListWithCount(params) {
  const res = await api.getEntityList(params)
  // 为每个实体获取字段数量
  if (res.data && res.data.length > 0) {
    const promises = res.data.map(async (entity) => {
      try {
        const fieldRes = await api.getFieldsByEntity({ entity_id: entity.id })
        entity.field_count = fieldRes.data?.length || 0
        entity.relation_count = 0 // 暂时设为0，后续可以添加关系统计
      } catch (err) {
        entity.field_count = 0
        entity.relation_count = 0
      }
    })
    await Promise.all(promises)
  }
  return res
}

const validateForm = {
  name: [
    {
      required: true,
      message: '请输入模型名称',
      trigger: ['input', 'blur'],
    },
  ],
}

// 标签输入
const tagKey = ref('')
const tagValue = ref('')

function addTag() {
  if (tagKey.value && tagValue.value) {
    if (!modalForm.value.tags) {
      modalForm.value.tags = {}
    }
    modalForm.value.tags[tagKey.value] = tagValue.value
    tagKey.value = ''
    tagValue.value = ''
  }
}

function removeTag(key) {
  if (modalForm.value.tags) {
    delete modalForm.value.tags[key]
  }
}
</script>

<template>
  <CommonPage show-footer title="模型列表">
    <template #action>
      <NButton type="primary" @click="handleAdd">
        新建模型
      </NButton>
    </template>

    <!-- 表格 -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="getEntityListWithCount"
    >
      <template #queryBar>
        <QueryBarItem label="分类" :label-width="50">
          <NSelect
            v-model:value="queryItems.category"
            :options="categoryOptions"
            placeholder="请选择分类"
            clearable
            @update:value="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="模型名称" :label-width="80">
          <NInput
            v-model:value="queryItems.name"
            clearable
            type="text"
            placeholder="请输入模型名称"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
      </template>

      <!-- 空状态 -->
      <template #empty>
        <NEmpty description="暂无模型数据">
          <template #extra>
            <NButton type="primary" @click="handleAdd">
              新建模型
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
        :label-width="80"
        :model="modalForm"
        :rules="validateForm"
      >
        <NFormItem label="模型名称" path="name">
          <NInput v-model:value="modalForm.name" clearable placeholder="请输入模型名称，如：User" />
        </NFormItem>
        <NFormItem label="分类" path="category">
          <NSelect
            v-model:value="modalForm.category"
            :options="categoryOptions.filter(item => item.value !== '')"
            placeholder="请选择分类"
            clearable
          />
        </NFormItem>
        <NFormItem label="描述" path="description">
          <NInput
            v-model:value="modalForm.description"
            type="textarea"
            :rows="3"
            clearable
            placeholder="请输入模型描述"
          />
        </NFormItem>
        <NFormItem label="标签" path="tags">
          <div style="width: 100%">
            <NSpace vertical>
              <NInputGroup>
                <NInput
                  v-model:value="tagKey"
                  placeholder="标签名"
                  style="width: 35%"
                />
                <NInput
                  v-model:value="tagValue"
                  placeholder="标签值"
                  style="width: 35%"
                  @keypress.enter="addTag"
                />
                <NButton type="primary" @click="addTag">添加</NButton>
              </NInputGroup>
              <NSpace v-if="modalForm.tags && Object.keys(modalForm.tags).length > 0">
                <NTag
                  v-for="(value, key) in modalForm.tags"
                  :key="key"
                  closable
                  @close="removeTag(key)"
                >
                  {{ key }}: {{ value }}
                </NTag>
              </NSpace>
            </NSpace>
          </div>
        </NFormItem>
      </NForm>
    </CrudModal>
  </CommonPage>
</template>
