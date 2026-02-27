<template>
  <AppPage :show-footer="false">
    <CommonPage title="测试数据生成">
      <n-space vertical :size="20">
        <!-- 配置表单 -->
        <n-card title="生成配置" rounded-10>  
          <n-form
            ref="formRef"
            :model="formData"
            :rules="rules"
            label-placement="left"
            :label-width="100"
          >
            <n-grid :cols="2" :x-gap="24">
              <n-grid-item>
                <n-form-item label="数据类型" path="dataType">
                  <n-select
                    v-model:value="formData.dataType"
                    :options="dataTypeOptions"
                    placeholder="请选择数据类型"
                    @update:value="handleDataTypeChange"
                  />
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item label="生成数量" path="count">
                  <n-input-number
                    v-model:value="formData.count"
                    :min="1"
                    :max="10000"
                    placeholder="请输入生成数量"
                    style="width: 100%"
                  />
                </n-form-item>
              </n-grid-item>
            </n-grid>

            <!-- 邮箱配置 -->
            <template v-if="formData.dataType === 'email'">
              <n-divider title-placement="left">邮箱配置</n-divider>
              <n-grid :cols="2" :x-gap="24">
                <n-grid-item>
                  <n-form-item label="域名" path="emailDomain">
                    <n-select
                      v-model:value="formData.emailDomain"
                      :options="emailDomainOptions"
                      filterable
                      tag
                      placeholder="选择或输入邮箱域名"
                      allow-create
                    />
                  </n-form-item>
                </n-grid-item>
                <n-grid-item>
                  <n-form-item label="用户名格式" path="emailUsernameFormat">
                    <n-select
                      v-model:value="formData.emailUsernameFormat"
                      :options="emailUsernameFormatOptions"
                      placeholder="选择用户名格式"
                    />
                  </n-form-item>
                </n-grid-item>
              </n-grid>
            </template>

            <!-- 单号配置 -->
            <template v-if="formData.dataType === 'orderNo'">
              <n-divider title-placement="left">单号配置</n-divider>
              <n-grid :cols="2" :x-gap="24">
                <n-grid-item>
                  <n-form-item label="前缀" path="orderPrefix">
                    <n-input
                      v-model:value="formData.orderPrefix"
                      placeholder="例如：ORD、PO、SO"
                      :maxlength="10"
                    />
                  </n-form-item>
                </n-grid-item>
                <n-grid-item>
                  <n-form-item label="格式" path="orderFormat">
                    <n-select
                      v-model:value="formData.orderFormat"
                      :options="orderFormatOptions"
                      placeholder="选择单号格式"
                    />
                  </n-form-item>
                </n-grid-item>
              </n-grid>
              <n-grid :cols="2" :x-gap="24">
                <n-grid-item>
                  <n-form-item label="日期格式" path="orderDateFormat">
                    <n-select
                      v-model:value="formData.orderDateFormat"
                      :options="orderDateFormatOptions"
                      placeholder="选择日期格式"
                    />
                  </n-form-item>
                </n-grid-item>
                <n-grid-item>
                  <n-form-item label="随机位数" path="orderRandomLength">
                    <n-input-number
                      v-model:value="formData.orderRandomLength"
                      :min="4"
                      :max="10"
                      placeholder="随机数位数"
                      style="width: 100%"
                    />
                  </n-form-item>
                </n-grid-item>
              </n-grid>
            </template>

            <n-form-item>
              <n-space>
                <n-button type="primary" @click="handleGenerate">
                  <template #icon>
                    <TheIcon icon="material-symbols:play-circle-outline" :size="18" />
                  </template>
                  生成数据
                </n-button>
                <n-button @click="handleReset">重置</n-button>
                <n-button
                  :disabled="!generatedData || generatedData.length === 0"
                  @click="handleCopy"
                >
                  <template #icon>
                    <TheIcon icon="material-symbols:content-copy-outline" :size="18" />
                  </template>
                  复制结果
                </n-button>
                <n-button
                  :disabled="!generatedData || generatedData.length === 0"
                  @click="handleExport"
                >
                  <template #icon>
                    <TheIcon icon="material-symbols:download-outline" :size="18" />
                  </template>
                  导出为文本
                </n-button>
              </n-space>
            </n-form-item>
          </n-form>
        </n-card>

        <!-- 生成结果 -->
        <n-card v-if="generatedData && generatedData.length > 0" title="生成结果" rounded-10>
          <template #header-extra>
            <n-text text-12 op-60>共生成 {{ generatedData.length }} 条数据</n-text>
          </template>
          <n-space vertical :size="12">
            <n-input
              v-model:value="resultText"
              type="textarea"
              :rows="15"
              placeholder="生成的数据将显示在这里"
              readonly
              style="font-family: 'Courier New', monospace"
            />
          </n-space>
        </n-card>
      </n-space>
    </CommonPage>
  </AppPage>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useMessage } from 'naive-ui'
import CommonPage from '@/components/page/CommonPage.vue'
import TheIcon from '@/components/icon/TheIcon.vue'

defineOptions({ name: '测试数据生成' })

const $message = useMessage()

// 表单数据
const formRef = ref(null)
const formData = ref({
  dataType: 'email',
  count: 10,
  // 邮箱配置
  emailDomain: 'example.com',
  emailUsernameFormat: 'random',
  // 单号配置
  orderPrefix: 'ORD',
  orderFormat: 'prefix_date_random',
  orderDateFormat: 'YYYYMMDD',
  orderRandomLength: 6,
})

// 生成结果
const generatedData = ref([])
const resultText = computed(() => generatedData.value.join('\n'))

// 数据类型选项
const dataTypeOptions = [
  { label: '邮箱', value: 'email' },
  { label: '单号', value: 'orderNo' },
]

// 邮箱域名选项
const emailDomainOptions = [
  { label: 'example.com', value: 'example.com' },
  { label: 'gmail.com', value: 'gmail.com' },
  { label: 'qq.com', value: 'qq.com' },
  { label: '163.com', value: '163.com' },
  { label: 'sina.com', value: 'sina.com' },
  { label: 'outlook.com', value: 'outlook.com' },
  { label: 'yahoo.com', value: 'yahoo.com' },
]

// 邮箱用户名格式选项
const emailUsernameFormatOptions = [
  { label: '随机字母数字', value: 'random' },
  { label: '随机字母', value: 'letters' },
  { label: '随机数字', value: 'numbers' },
  { label: '用户名+随机数', value: 'username_random' },
]

// 单号格式选项
const orderFormatOptions = [
  { label: '前缀+日期+随机数', value: 'prefix_date_random' },
  { label: '前缀+随机数', value: 'prefix_random' },
  { label: '前缀+序号', value: 'prefix_sequence' },
]

// 日期格式选项
const orderDateFormatOptions = [
  { label: 'YYYYMMDD (20240101)', value: 'YYYYMMDD' },
  { label: 'YYYY-MM-DD (2024-01-01)', value: 'YYYY-MM-DD' },
  { label: 'YYMMDD (240101)', value: 'YYMMDD' },
  { label: 'YYYYMMDDHHmmss (20240101123000)', value: 'YYYYMMDDHHmmss' },
]

// 表单验证规则
const rules = {
  dataType: [{ required: true, message: '请选择数据类型', trigger: 'change' }],
  count: [
    { required: true, message: '请输入生成数量', trigger: 'blur' },
    { type: 'number', min: 1, max: 10000, message: '数量必须在 1-10000 之间', trigger: 'blur' },
  ],
}

// 数据类型改变时的处理
function handleDataTypeChange(value) {
  if (value === 'email') {
    formData.value.emailDomain = 'example.com'
    formData.value.emailUsernameFormat = 'random'
  } else if (value === 'orderNo') {
    formData.value.orderPrefix = 'ORD'
    formData.value.orderFormat = 'prefix_date_random'
    formData.value.orderDateFormat = 'YYYYMMDD'
    formData.value.orderRandomLength = 6
  }
}

// 生成随机字符串
function generateRandomString(length, type = 'alphanumeric') {
  let chars = ''
  if (type === 'letters') {
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  } else if (type === 'numbers') {
    chars = '0123456789'
  } else {
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
  }
  
  let result = ''
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return result
}

// 生成邮箱
function generateEmail() {
  const { count, emailDomain, emailUsernameFormat } = formData.value
  const emails = []
  
  for (let i = 0; i < count; i++) {
    let username = ''
    
    switch (emailUsernameFormat) {
      case 'random':
        username = generateRandomString(8, 'alphanumeric')
        break
      case 'letters':
        username = generateRandomString(8, 'letters')
        break
      case 'numbers':
        username = generateRandomString(8, 'numbers')
        break
      case 'username_random':
        username = `user${generateRandomString(6, 'numbers')}`
        break
      default:
        username = generateRandomString(8, 'alphanumeric')
    }
    
    emails.push(`${username}@${emailDomain}`)
  }
  
  return emails
}

// 格式化日期
function formatDate(format) {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')
  
  switch (format) {
    case 'YYYYMMDD':
      return `${year}${month}${day}`
    case 'YYYY-MM-DD':
      return `${year}-${month}-${day}`
    case 'YYMMDD':
      return `${String(year).slice(-2)}${month}${day}`
    case 'YYYYMMDDHHmmss':
      return `${year}${month}${day}${hours}${minutes}${seconds}`
    default:
      return `${year}${month}${day}`
  }
}

// 生成单号
function generateOrderNo() {
  const { count, orderPrefix, orderFormat, orderDateFormat, orderRandomLength } = formData.value
  const orderNos = []
  const dateStr = formatDate(orderDateFormat)
  
  for (let i = 0; i < count; i++) {
    let orderNo = ''
    
    switch (orderFormat) {
      case 'prefix_date_random':
        orderNo = `${orderPrefix}${dateStr}${generateRandomString(orderRandomLength, 'numbers')}`
        break
      case 'prefix_random':
        orderNo = `${orderPrefix}${generateRandomString(orderRandomLength + 2, 'numbers')}`
        break
      case 'prefix_sequence':
        orderNo = `${orderPrefix}${String(i + 1).padStart(orderRandomLength, '0')}`
        break
      default:
        orderNo = `${orderPrefix}${dateStr}${generateRandomString(orderRandomLength, 'numbers')}`
    }
    
    orderNos.push(orderNo)
  }
  
  return orderNos
}

// 生成数据
function handleGenerate() {
  formRef.value?.validate((errors) => {
    if (errors) {
      return
    }
    
    try {
      let data = []
      
      switch (formData.value.dataType) {
        case 'email':
          data = generateEmail()
          break
        case 'orderNo':
          data = generateOrderNo()
          break
        default:
          $message.warning('不支持的数据类型')
          return
      }
      
      generatedData.value = data
      $message.success(`成功生成 ${data.length} 条数据`)
    } catch (error) {
      console.error('生成数据失败:', error)
      $message.error('生成数据失败，请检查配置')
    }
  })
}

// 重置表单
function handleReset() {
  formData.value = {
    dataType: 'email',
    count: 10,
    emailDomain: 'example.com',
    emailUsernameFormat: 'random',
    orderPrefix: 'ORD',
    orderFormat: 'prefix_date_random',
    orderDateFormat: 'YYYYMMDD',
    orderRandomLength: 6,
  }
  generatedData.value = []
  $message.info('表单已重置')
}

// 复制结果
async function handleCopy() {
  if (!generatedData.value || generatedData.value.length === 0) {
    $message.warning('没有可复制的内容')
    return
  }
  
  try {
    await navigator.clipboard.writeText(resultText.value)
    $message.success('已复制到剪贴板')
  } catch (error) {
    console.error('复制失败:', error)
    // 降级方案：使用 document.execCommand
    const textArea = document.createElement('textarea')
    textArea.value = resultText.value
    textArea.style.position = 'fixed'
    textArea.style.opacity = '0'
    document.body.appendChild(textArea)
    textArea.select()
    try {
      document.execCommand('copy')
      $message.success('已复制到剪贴板')
    } catch (err) {
      $message.error('复制失败，请手动复制')
    }
    document.body.removeChild(textArea)
  }
}

// 导出为文本
function handleExport() {
  if (!generatedData.value || generatedData.value.length === 0) {
    $message.warning('没有可导出的内容')
    return
  }
  
  try {
    const blob = new Blob([resultText.value], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `test_data_${new Date().getTime()}.txt`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
    $message.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    $message.error('导出失败')
  }
}
</script>

<style scoped>
:deep(.n-form-item-label) {
  font-weight: 500;
}
</style>