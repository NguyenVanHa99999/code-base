<template>
  <div class="register-page">
    <div class="register-page__container">
      <div class="register-page__left">
        <div class="register-page__branding">
          <div class="register-page__logo">🎓</div>
          <h1 class="register-page__brand-title">AI Teaching Assistant</h1>
          <p class="register-page__brand-subtitle">
            {{ $t('auth.joinMessage') }}
          </p>
        </div>
      </div>

      <div class="register-page__right">
        <div class="register-page__form-container">
          <h2 class="register-page__title">{{ $t('auth.registerTitle') }}</h2>
          <p class="register-page__subtitle">{{ $t('auth.registerSubtitle') }}</p>

          <form @submit.prevent="handleRegister" class="register-page__form">
            <div class="register-page__form-group">
              <label class="register-page__label">{{ $t('auth.fullName') }}</label>
              <input
                v-model="form.name"
                type="text"
                class="register-page__input"
                :placeholder="$t('auth.fullNamePlaceholder')"
                required
                autocomplete="name"
              />
            </div>

            <div class="register-page__form-group">
              <label class="register-page__label">{{ $t('auth.email') }}</label>
              <input
                v-model="form.email"
                type="email"
                class="register-page__input"
                :placeholder="$t('auth.emailPlaceholder')"
                required
                autocomplete="email"
              />
            </div>

            <div class="register-page__form-group">
              <label class="register-page__label">{{ $t('auth.password') }}</label>
              <div class="register-page__password-wrapper">
                <input
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  class="register-page__input"
                  :placeholder="$t('auth.passwordPlaceholder')"
                  required
                  autocomplete="new-password"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="register-page__password-toggle"
                >
                  {{ showPassword ? '👁️' : '🔒' }}
                </button>
              </div>
              <p class="register-page__hint">{{ $t('auth.passwordHint') }}</p>
            </div>

            <div class="register-page__form-group">
              <label class="register-page__label">{{ $t('auth.confirmPassword') }}</label>
              <div class="register-page__password-wrapper">
                <input
                  v-model="form.confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  class="register-page__input"
                  :placeholder="$t('auth.confirmPasswordPlaceholder')"
                  required
                  autocomplete="new-password"
                />
                <button
                  type="button"
                  @click="showConfirmPassword = !showConfirmPassword"
                  class="register-page__password-toggle"
                >
                  {{ showConfirmPassword ? '👁️' : '🔒' }}
                </button>
              </div>
            </div>

            <div class="register-page__terms">
              <label class="register-page__checkbox-label">
                <input
                  v-model="form.agreeTerms"
                  type="checkbox"
                  class="register-page__checkbox"
                  required
                />
                <span>
                  {{ $t('auth.agreeToTerms') }}
                  <a href="/terms" class="register-page__link" target="_blank">
                    {{ $t('auth.termsOfService') }}
                  </a>
                </span>
              </label>
            </div>

            <button
              type="submit"
              class="register-page__btn register-page__btn--primary"
              :disabled="isLoading"
            >
              <span v-if="!isLoading">{{ $t('auth.createAccount') }}</span>
              <span v-else>{{ $t('auth.creatingAccount') }}</span>
            </button>

            <div class="register-page__divider">
              <span>{{ $t('auth.or') }}</span>
            </div>

            <button
              type="button"
              @click="registerWithGoogle"
              class="register-page__btn register-page__btn--secondary"
            >
              🔵 {{ $t('auth.registerWithGoogle') }}
            </button>

            <p class="register-page__footer">
              {{ $t('auth.haveAccount') }}
              <router-link to="/login" class="register-page__link">
                {{ $t('auth.login') }}
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
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  agreeTerms: false
})

const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isLoading = ref(false)

const handleRegister = async () => {
  // Validation
  if (form.value.password !== form.value.confirmPassword) {
    alert('Passwords do not match!')
    return
  }

  if (form.value.password.length < 6) {
    alert('Password must be at least 6 characters!')
    return
  }

  if (!form.value.agreeTerms) {
    alert('Please agree to the terms of service!')
    return
  }

  isLoading.value = true
  
  try {
    await authStore.register({
      name: form.value.name,
      email: form.value.email,
      password: form.value.password
    })
    
    router.push('/login')
    alert('Registration successful! Please login.')
  } catch (error) {
    console.error('Register error:', error)
    const message = error.response?.data?.detail || error.message || 'Registration failed. Please try again.'
    alert(message)
  } finally {
    isLoading.value = false
  }
}

const registerWithGoogle = () => {
  alert('Google registration feature coming soon!')
}
</script>
