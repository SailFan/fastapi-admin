<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  NButton,
  NCard,
  NDescriptions,
  NDescriptionsItem,
  NTag,
  NSpace,
  NPopconfirm,
  NSpin,
  NEmpty,
  NForm,
  NFormItem,
  NInput,
  NSelect,
  NInputGroup,
} from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import TheIcon from '@/components/icon/TheIcon.vue'
import CrudModal from '@/components/table/CrudModal.vue'

import { formatDate } from '@/utils'
import api from '@/api'

defineOptions({ name: '模型详情' })

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const entityData = ref(null)
const fieldList = ref([])

const editModalVisible = ref(false)
const editModalLoading = ref(false)
const editForm = ref({})
const editFormRef = ref(null)

onMounted(async () => {
  await loadEntityData()
})

// 加载实体数据
async function loadEntityData() {
  const entityId = route.query.id
  if (!entityId) {
    $message.error('缺少模型ID')
    router.back()
    return
  }

  loading.value = true
  try {
    // 获取实体详情
    const entityRes = await api.getEntityById({ entity_id: entityId })
    entityData.value = entityRes.data

    // 获取字段列表
    const fieldRes = await api.getFieldsByEntity({ entity_id: entityId })
    fieldList.value = fieldRes.data || []
  } catch (err) {
    $message.error('加载数据失败：' + err.message)
  } finally {
    loading.value = false
  }
}

// 编辑模型
function handleEdit() {
  editForm.value = {
    id: entityData.value.id,
    name: entityData.value.name,
    category: entityData.value.category,
    tags: entityData.value.tags || {},
    description: entityData.value.description,
  }
  editModalVisible.value = true
}

// 保存编辑
async function handleSaveEdit() {
  try {
    await editFormRef.value?.validate()
    editModalLoading.value = true
    await api.updateEntity(editForm.value)
    $message.success('更新成功')
    editModalVisible.value = false
    await loadEntityData()
  } catch (err) {
    if (err.message) {
      $message.error('更新失败：' + err.message)
    }
  } finally {
    editModalLoading.value = false
  }
}

// 删除模型
async function handleDelete() {
  try {
    await api.deleteEntity({ entity_id: entityData.value.id })
    $message.success('删除成功')
    router.push('/model/list')
  } catch (err) {
    $message.error('删除失败：' + err.message)
  }
}

// 生成数据
function handleGenerateData() {
  // TODO: 跳转到数据生成页面或打开生成数据弹窗
  $message.info('数据生成功能开发中...')
}

// 分类选项
const categoryOptions = [
  { label: '业务实体', value: '业务实体' },
  { label: '系统实体', value: '系统实体' },
  { label: '测试实体', value: '测试实体' },
]

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
    if (!editForm.value.tags) {
      editForm.value.tags = {}
    }
    editForm.value.tags[tagKey.value] = tagValue.value
    tagKey.value = ''
    tagValue.value = ''
  }
}

function removeTag(key) {
  if (editForm.value.tags) {
    delete editForm.value.tags[key]
  }
}
</script>

<template>
  <CommonPage show-footer :title="`模型详情 - ${entityData?.name || ''}`">
    <template #action>
      <NSpace>
        <NButton @click="router.back()">
          返回
        </NButton>
        <NButton type="primary" @click="handleEdit">
          编辑
        </NButton>
        <NButton type="success" @click="handleGenerateData">
          生成数据
        </NButton>
        <NPopconfirm @positive-click="handleDelete">
          <template #trigger>
            <NButton type="error">
              删除
            </NButton>
          </template>
          确定删除该模型吗？删除后无法恢复！
        </NPopconfirm>
      </NSpace>
    </template>

    <NSpin :show="loading">
      <div v-if="entityData" style="padding: 20px">
        <!-- 基本信息 -->
        <NCard title="基本信息" :bordered="false" style="margin-bottom: 20px">
          <NDescriptions :column="2" label-placement="left" bordered>
            <NDescriptionsItem label="模型名称">
              {{ entityData.name }}
            </NDescriptionsItem>
            <NDescriptionsItem label="分类">
              <NTag v-if="entityData.category" type="info">
                {{ entityData.category }}
              </NTag>
              <span v-else>-</span>
            </NDescriptionsItem>
            <NDescriptionsItem label="UUID">
              {{ entityData.uuid }}
            </NDescriptionsItem>
            <NDescriptionsItem label="创建时间">
              {{ formatDate(entityData.created_at) }}
            </NDescriptionsItem>
            <NDescriptionsItem label="更新时间">
              {{ formatDate(entityData.updated_at) }}
            </NDescriptionsItem>
            <NDescriptionsItem label="字段数量">
              <NTag type="success">{{ fieldList.length }}</NTag>
            </NDescriptionsItem>
            <NDescriptionsItem label="描述" :span="2">
              {{ entityData.description || '-' }}
            </NDescriptionsItem>
            <NDescriptionsItem label="标签" :span="2">
              <NSpace v-if="entityData.tags && Object.keys(entityData.tags).length > 0">
                <NTag
                  v-for="(value, key) in entityData.tags"
                  :key="key"
                  type="info"
                >
                  {{ key }}: {{ value }}
                </NTag>
              </NSpace>
              <span v-else>-</span>
            </NDescriptionsItem>
          </NDescriptions>
        </NCard>

        <!-- 字段列表 -->
        <NCard title="字段列表" :bordered="false">
          <template #header-extra>
            <NButton
              type="primary"
              size="small"
              @click="router.push({ path: '/model/fields', query: { entity_id: entityData.id } })"
            >
              管理字段
            </NButton>
          </template>

          <div v-if="fieldList.length > 0">
            <NSpace vertical>
              <NCard
                v-for="field in fieldList"
                :key="field.id"
                size="small"
                :bordered="true"
                style="margin-bottom: 10px"
              >
                <div style="display: flex; justify-content: space-between; align-items: center">
                  <div>
                    <strong>{{ field.name }}</strong>
                    <NTag size="small" type="info" style="margin-left: 10px">
                      {{ field.type }}
                    </NTag>
                    <NTag
                      v-if="field.is_required"
                      size="small"
                      type="error"
                      style="margin-left: 5px"
                    >
                      必填
                    </NTag>
                    <span v-if="field.description" style="margin-left: 10px; color: #999">
                      {{ field.description }}
                    </span>
                  </div>
                  <div>
                    <span v-if="field.default_value" style="color: #666; font-size: 12px">
                      默认值: {{ field.default_value }}
                    </span>
                  </div>
                </div>
              </NCard>
            </NSpace>
          </div>
          <NEmpty v-else description="暂无字段数据">
            <template #extra>
              <NButton
                type="primary"
                @click="router.push({ path: '/model/fields', query: { entity_id: entityData.id } })"
              >
                添加字段
              </NButton>
            </template>
          </NEmpty>
        </NCard>
      </div>
    </NSpin>

    <!-- 编辑弹窗 -->
    <CrudModal
      v-model:visible="editModalVisible"
      title="编辑模型"
      :loading="editModalLoading"
      @save="handleSaveEdit"
    >
      <NForm
        ref="editFormRef"
        label-placement="left"
        label-align="left"
        :label-width="80"
        :model="editForm"
        :rules="validateForm"
      >
        <NFormItem label="模型名称" path="name">
          <NInput v-model:value="editForm.name" clearable placeholder="请输入模型名称" />
        </NFormItem>
        <NFormItem label="分类" path="category">
          <NSelect
            v-model:value="editForm.category"
            :options="categoryOptions"
            placeholder="请选择分类"
            clearable
          />
        </NFormItem>
        <NFormItem label="描述" path="description">
          <NInput
            v-model:value="editForm.description"
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
              <NSpace v-if="editForm.tags && Object.keys(editForm.tags).length > 0">
                <NTag
                  v-for="(value, key) in editForm.tags"
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
