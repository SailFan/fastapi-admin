<script setup>
import { h, onMounted, ref } from 'vue'
import {
  NButton,
  NForm,
  NFormItem,
  NInput,
  NSelect,
  NTag,
  NPopconfirm,
  NDatePicker,
  NInputNumber,
} from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'

import { formatDate } from '@/utils'
import { useCRUD } from '@/composables'
import api from '@/api'

defineOptions({ name: '订单列表' })

const $table = ref(null)
const queryItems = ref({})

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
  name: '订单',
  initForm: {},
  doCreate: api.createOrder,
  doUpdate: api.updateOrder,
  doDelete: api.deleteOrder,
  refresh: () => $table.value?.handleSearch(),
})

onMounted(() => {
  $table.value?.handleSearch()
})

// 平台选项
const platformOptions = [
  { label: '全部', value: '' },
  { label: '淘宝', value: '淘宝' },
  { label: '京东', value: '京东' },
  { label: '拼多多', value: '拼多多' },
  { label: '抖音', value: '抖音' },
]

// 状态选项
const statusOptions = [
  { label: '全部', value: '' },
  { label: '待处理', value: 'pending' },
  { label: '已完成', value: 'completed' },
  { label: '已取消', value: 'cancelled' },
]

const statusMap = {
  pending: { label: '待处理', type: 'warning' },
  completed: { label: '已完成', type: 'success' },
  cancelled: { label: '已取消', type: 'error' },
}

const columns = [
  {
    title: '订单编号',
    key: 'order_no',
    width: 150,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '平台',
    key: 'platform',
    width: 80,
    align: 'center',
  },
  {
    title: '店铺名称',
    key: 'shop_name',
    width: 120,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '产品名称',
    key: 'product_name',
    width: 150,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '下单时间',
    key: 'order_time',
    width: 150,
    align: 'center',
    render(row) {
      return row.order_time ? formatDate(row.order_time) : '-'
    },
  },
  {
    title: '订单金额',
    key: 'order_amount',
    width: 100,
    align: 'center',
    render(row) {
      return `¥${row.order_amount}`
    },
  },
  {
    title: '用户ID',
    key: 'user_id',
    width: 100,
    align: 'center',
  },
  {
    title: '订单数量',
    key: 'order_count',
    width: 80,
    align: 'center',
  },
  {
    title: '总金额',
    key: 'total_amount',
    width: 100,
    align: 'center',
    render(row) {
      return `¥${row.total_amount}`
    },
  },
  {
    title: '客户名称',
    key: 'customer_name',
    width: 100,
    align: 'center',
  },
  {
    title: '客户分组',
    key: 'customer_group',
    width: 100,
    align: 'center',
  },
  {
    title: '使用时长',
    key: 'usage_time',
    width: 100,
    align: 'center',
  },
  {
    title: '操作人',
    key: 'operation_user',
    width: 100,
    align: 'center',
  },
  {
    title: '状态',
    key: 'status',
    width: 80,
    align: 'center',
    render(row) {
      const status = statusMap[row.status] || { label: row.status, type: 'default' }
      return h(NTag, { type: status.type }, { default: () => status.label })
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
            onPositiveClick: () => handleDelete({ order_id: row.id }, false),
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
            default: () => h('div', {}, '确定删除该订单吗？'),
          }
        ),
      ]
    },
  },
]

const validateForm = {
  order_no: [
    {
      required: true,
      message: '请输入订单编号',
      trigger: ['input', 'blur'],
    },
  ],
}
</script>

<template>
  <CommonPage show-footer title="订单列表">
    <template #action>
      <NButton type="primary" @click="handleAdd">
        新建订单
      </NButton>
    </template>

    <!-- 表格 -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getOrderList"
    >
      <template #queryBar>
        <QueryBarItem label="订单编号" :label-width="80">
          <NInput
            v-model:value="queryItems.order_no"
            clearable
            type="text"
            placeholder="请输入订单编号"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="平台" :label-width="50">
          <NSelect
            v-model:value="queryItems.platform"
            :options="platformOptions"
            placeholder="请选择平台"
            clearable
            @update:value="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="状态" :label-width="50">
          <NSelect
            v-model:value="queryItems.status"
            :options="statusOptions"
            placeholder="请选择状态"
            clearable
            @update:value="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="客户名称" :label-width="80">
          <NInput
            v-model:value="queryItems.customer_name"
            clearable
            type="text"
            placeholder="请输入客户名称"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
      </template>
    </CrudTable>

    <!-- 新增/编辑 弹窗 -->
    <CrudModal
      v-model:visible="modalVisible"
      :title="modalTitle"
      :loading="modalLoading"
      width="800px"
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
        <NFormItem label="订单编号" path="order_no">
          <NInput v-model:value="modalForm.order_no" clearable placeholder="请输入订单编号" />
        </NFormItem>
        <NFormItem label="平台" path="platform">
          <NSelect
            v-model:value="modalForm.platform"
            :options="platformOptions.filter(item => item.value !== '')"
            placeholder="请选择平台"
            clearable
          />
        </NFormItem>
        <NFormItem label="店铺名称" path="shop_name">
          <NInput v-model:value="modalForm.shop_name" clearable placeholder="请输入店铺名称" />
        </NFormItem>
        <NFormItem label="产品名称" path="product_name">
          <NInput v-model:value="modalForm.product_name" clearable placeholder="请输入产品名称" />
        </NFormItem>
        <NFormItem label="下单时间" path="order_time">
          <NDatePicker
            v-model:value="modalForm.order_time"
            type="datetime"
            clearable
            style="width: 100%"
          />
        </NFormItem>
        <NFormItem label="订单金额" path="order_amount">
          <NInputNumber
            v-model:value="modalForm.order_amount"
            :min="0"
            :precision="2"
            clearable
            style="width: 100%"
            placeholder="请输入订单金额"
          />
        </NFormItem>
        <NFormItem label="用户ID" path="user_id">
          <NInput v-model:value="modalForm.user_id" clearable placeholder="请输入用户ID" />
        </NFormItem>
        <NFormItem label="订单数量" path="order_count">
          <NInputNumber
            v-model:value="modalForm.order_count"
            :min="1"
            clearable
            style="width: 100%"
            placeholder="请输入订单数量"
          />
        </NFormItem>
        <NFormItem label="总金额" path="total_amount">
          <NInputNumber
            v-model:value="modalForm.total_amount"
            :min="0"
            :precision="2"
            clearable
            style="width: 100%"
            placeholder="请输入总金额"
          />
        </NFormItem>
        <NFormItem label="客户名称" path="customer_name">
          <NInput v-model:value="modalForm.customer_name" clearable placeholder="请输入客户名称" />
        </NFormItem>
        <NFormItem label="客户分组" path="customer_group">
          <NInput v-model:value="modalForm.customer_group" clearable placeholder="请输入客户分组" />
        </NFormItem>
        <NFormItem label="使用时长" path="usage_time">
          <NInput v-model:value="modalForm.usage_time" clearable placeholder="如：30天" />
        </NFormItem>
        <NFormItem label="操作人" path="operation_user">
          <NInput v-model:value="modalForm.operation_user" clearable placeholder="请输入操作人" />
        </NFormItem>
        <NFormItem label="状态" path="status">
          <NSelect
            v-model:value="modalForm.status"
            :options="statusOptions.filter(item => item.value !== '')"
            placeholder="请选择状态"
            clearable
          />
        </NFormItem>
        <NFormItem label="备注" path="remark">
          <NInput
            v-model:value="modalForm.remark"
            type="textarea"
            :rows="3"
            clearable
            placeholder="请输入备注"
          />
        </NFormItem>
      </NForm>
    </CrudModal>
  </CommonPage>
</template>
