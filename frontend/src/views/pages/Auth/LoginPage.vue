<template>
  <div class="login-page">
    <div class="login-page__container">
      <div class="login-page__left">
        <div class="login-page__branding">
          <div class="login-page__logo">🎓</div>
          <h1 class="login-page__brand-title">AI Teaching Assistant</h1>
          <p class="login-page__brand-subtitle">
            {{ $t('auth.welcomeMessage') }}
          </p>
        </div>
      </div>

      <div class="login-page__right">
        <div class="login-page__form-container">
          <h2 class="login-page__title">{{ $t('auth.loginTitle') }}</h2>
          <p class="login-page__subtitle">{{ $t('auth.loginSubtitle') }}</p>

          <form @submit.prevent="handleLogin" class="login-page__form">
            <div class="login-page__form-group">
              <label class="login-page__label">{{ $t('auth.email') }}</label>
              <input
                v-model="form.email"
                type="email"
                class="login-page__input"
                :placeholder="$t('auth.emailPlaceholder')"
                required
                autocomplete="email"
              />
            </div>

            <div class="login-page__form-group">
              <label class="login-page__label">{{ $t('auth.password') }}</label>
              <div class="login-page__password-wrapper">
                <input
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  class="login-page__input"
                  :placeholder="$t('auth.passwordPlaceholder')"
                  required
                  autocomplete="current-password"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="login-page__password-toggle"
                >
                  {{ showPassword ? '👁️' : '🔒' }}
                </button>
              </div>
            </div>

            <div class="login-page__options">
              <label class="login-page__checkbox-label">
                <input
                  v-model="form.remember"
                  type="checkbox"
                  class="login-page__checkbox"
                />
                <span>{{ $t('auth.rememberMe') }}</span>
              </label>
              <router-link to="/forgot-password" class="login-page__link">
                {{ $t('auth.forgotPassword') }}
              </router-link>
            </div>

            <button
              type="submit"
              class="login-page__btn login-page__btn--primary"
              :disabled="isLoading"
            >
              <span v-if="!isLoading">{{ $t('auth.login') }}</span>
              <span v-else>{{ $t('auth.loggingIn') }}</span>
            </button>

            <div class="login-page__divider">
              <span>{{ $t('auth.or') }}</span>
            </div>

            <button
              type="button"
              @click="loginWithGoogle"
              class="login-page__btn login-page__btn--secondary"
            >
              🔵 {{ $t('auth.loginWithGoogle') }}
            </button>

            <p class="login-page__footer">
              {{ $t('auth.noAccount') }}
              <router-link to="/register" class="login-page__link">
                {{ $t('auth.register') }}
              </router-link>
            </p>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  email: '',
  password: '',
  remember: false
})

const showPassword = ref(false)
const isLoading = ref(false)

const handleLogin = async () => {
  isLoading.value = true
  
  try {
    await authStore.login(form.value.email, form.value.password)
    router.push('/')
  } catch (error) {
    console.error('Login error:', error)
    
    // Xử lý các loại lỗi
    const status = error.response?.status
    const detail = error.response?.data?.detail
    
    let message = 'Login failed. Please check your credentials.'
    
    if (status === 401) {
      message = detail || 'Incorrect email or password.'
    } else if (status === 403) {
      // Role mismatch - user không có quyền truy cập portal này
      message = detail || 'Access denied. You do not have permission to access this portal.'
    } else if (status === 429) {
      // Account locked - quá nhiều lần login sai
      message = detail || 'Account is temporarily locked. Please try again later.'
    } else if (detail) {
      message = detail
    }
    
    alert(message)
  } finally {
    isLoading.value = false
  }
}

const loginWithGoogle = () => {
  alert('Google login feature coming soon!')
}
</script>
