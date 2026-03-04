<template>
  <AppPage :show-footer="true" class="login-page">
    <div class="login-container">
      <!-- 三个小人 -->
      <div class="characters-container">
        <div 
          v-for="(character, index) in characters" 
          :key="index"
          class="character"
          :style="{ '--character-color': character.color }"
        >
          <!-- 头部 -->
          <div class="character-head">
            <!-- 眼睛 -->
            <div class="eyes">
              <div 
                class="eye"
                :style="{
                  transform: `translate(${eyePositions[index].x}px, ${eyePositions[index].y}px)`
                }"
              ></div>
              <div 
                class="eye"
                :style="{
                  transform: `translate(${eyePositions[index].x}px, ${eyePositions[index].y}px)`
                }"
              ></div>
            </div>
          </div>
          <!-- 身体 -->
          <div class="character-body"></div>
        </div>
      </div>

      <!-- 登录表单 -->
      <div class="login-form">
        <h2 class="login-title">{{ $t('app_name') }}</h2>
        
        <div class="form-group">
          <n-input
            v-model:value="loginInfo.username"
            autofocus
            size="large"
            placeholder="admin"
            :maxlength="20"
            @focus="handleFocus('username')"
            @blur="handleBlur"
          />
        </div>
        
        <div class="form-group">
          <n-input
            v-model:value="loginInfo.password"
            size="large"
            type="password"
            show-password-on="mousedown"
            placeholder="123456"
            :maxlength="20"
            @focus="handleFocus('password')"
            @blur="handleBlur"
            @keypress.enter="handleLogin"
          />
        </div>

        <div class="form-group">
          <n-button
            size="large"
            block
            type="primary"
            :loading="loading"
            @click="handleLogin"
          >
            {{ $t('views.login.text_login') }}
          </n-button>
        </div>
      </div>
    </div>
  </AppPage>
</template>

<script setup>
import { lStorage, setToken } from '@/utils'
import api from '@/api'
import { addDynamicRoutes } from '@/router'
import { useI18n } from 'vue-i18n'

const router = useRouter()
const { query } = useRoute()
const { t } = useI18n({ useScope: 'global' })

const loginInfo = ref({
  username: '',
  password: '',
})

// 三个小人的配置
const characters = [
  { color: '#FF6B6B' }, // 红色
  { color: '#4ECDC4' }, // 青色
  { color: '#FFE66D' }, // 黄色
]

// 眼睛位置
const eyePositions = ref([
  { x: 0, y: 0 },
  { x: 0, y: 0 },
  { x: 0, y: 0 },
])

// 是否正在输入
const isFocused = ref(false)
const focusedField = ref('')

initLoginInfo()

function initLoginInfo() {
  const localLoginInfo = lStorage.get('loginInfo')
  if (localLoginInfo) {
    loginInfo.value.username = localLoginInfo.username || ''
    loginInfo.value.password = localLoginInfo.password || ''
  }
}

// 鼠标移动事件
function handleMouseMove(event) {
  if (isFocused.value) return // 输入时不跟随鼠标
  
  const characters = document.querySelectorAll('.character-head')
  characters.forEach((character, index) => {
    const rect = character.getBoundingClientRect()
    const centerX = rect.left + rect.width / 2
    const centerY = rect.top + rect.height / 2
    
    const deltaX = event.clientX - centerX
    const deltaY = event.clientY - centerY
    
    const angle = Math.atan2(deltaY, deltaX)
    const distance = Math.min(Math.sqrt(deltaX * deltaX + deltaY * deltaY) / 50, 8)
    
    eyePositions.value[index] = {
      x: Math.cos(angle) * distance,
      y: Math.sin(angle) * distance,
    }
  })
}

// 输入框聚焦
function handleFocus(field) {
  isFocused.value = true
  focusedField.value = field
  
  // 输入密码时，小人捂眼睛
  if (field === 'password') {
    eyePositions.value = [
      { x: 0, y: -20 },
      { x: 0, y: -20 },
      { x: 0, y: -20 },
    ]
  } else {
    // 输入用户名时，小人看向输入框
    eyePositions.value = [
      { x: 0, y: 8 },
      { x: 0, y: 8 },
      { x: 0, y: 8 },
    ]
  }
}

// 输入框失焦
function handleBlur() {
  isFocused.value = false
  focusedField.value = ''
  eyePositions.value = [
    { x: 0, y: 0 },
    { x: 0, y: 0 },
    { x: 0, y: 0 },
  ]
}

onMounted(() => {
  window.addEventListener('mousemove', handleMouseMove)
})

onUnmounted(() => {
  window.removeEventListener('mousemove', handleMouseMove)
})

const loading = ref(false)
async function handleLogin() {
  const { username, password } = loginInfo.value
  if (!username || !password) {
    $message.warning(t('views.login.message_input_username_password'))
    return
  }
  try {
    loading.value = true
    $message.loading(t('views.login.message_verifying'))
    const res = await api.login({ username, password: password.toString() })
    $message.success(t('views.login.message_login_success'))
    setToken(res.data.access_token)
    await addDynamicRoutes()
    if (query.redirect) {
      const path = query.redirect
      Reflect.deleteProperty(query, 'redirect')
      router.push({ path, query })
    } else {
      router.push('/')
    }
  } catch (e) {
    console.error('login error', e.error)
  }
  loading.value = false
}
</script>

<style scoped>
.login-page {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-container {
  width: 100%;
  max-width: 400px;
  padding: 20px;
}

/* 三个小人容器 */
.characters-container {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-bottom: 60px;
}

/* 单个小人 */
.character {
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: float 3s ease-in-out infinite;
}

.character:nth-child(1) {
  animation-delay: 0s;
}

.character:nth-child(2) {
  animation-delay: 0.5s;
}

.character:nth-child(3) {
  animation-delay: 1s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* 头部 */
.character-head {
  width: 80px;
  height: 80px;
  background-color: var(--character-color);
  border-radius: 50%;
  position: relative;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.character:hover .character-head {
  transform: scale(1.1);
}

/* 眼睛容器 */
.eyes {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  gap: 20px;
}

/* 单个眼睛 */
.eye {
  width: 3px;
  height: 15px;
  background-color: #000;
  border-radius: 2px;
  transition: transform 0.1s ease;
}

/* 身体 */
.character-body {
  width: 50px;
  height: 60px;
  background-color: var(--character-color);
  border-radius: 0 0 25px 25px;
  margin-top: -10px;
  opacity: 0.8;
}

/* 登录表单 */
.login-form {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.login-title {
  text-align: center;
  font-size: 28px;
  font-weight: 600;
  color: #333;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group:last-child {
  margin-bottom: 0;
  margin-top: 30px;
}
</style>
