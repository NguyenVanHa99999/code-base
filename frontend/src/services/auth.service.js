import AccountApi from '@/api/Account'
import { LocalStorageType } from '@/constants'
import { i18n } from '@/plugins'
import router from '@/router'

class AuthService {
  constructor() {
    this.$i18n = i18n
    this.$localStorage = window.localStorage
  }

  get $store() {
    return {
      account: {},
      home: {},
      common: {},
    }
  }

  login(data) {
    return new Promise((resolve, reject) => {
      AccountApi.login(data)
        .then(async (res) => {
          const data = res.data
          if (data.result?.accessToken) {
            // save token
            const accessToken = data.result.accessToken
            const refreshToken = data.result.refreshToken
            const payload = this.parseToken(accessToken)

            const tokens = {
              accessToken,
              refreshToken,
              exp: payload?.exp,
            }
            this.$localStorage.setItem(LocalStorageType.ACCESS_TOKEN, tokens)
            this.$localStorage.setItem(LocalStorageType.REFRESH_TOKEN, tokens)

            try {
              const { result } = await this.loginInitialize()

              return resolve({
                result,
              })
            } catch (error) {
              return reject(error)
            }
          } else {
            reject(new Error('Login Failed. (no exist token)'))
          }
        })
        .catch((_) => {
          return resolve({
            isApiError: true,
          })
        })
    })
  }

  async logout() {
    await AccountApi.logout()
    this.logoutInitialize()
    await router.push({ name: 'Login' })
  }

  authError() {
    const isSessionTimeout = true
    this.logoutInitialize(isSessionTimeout)

    router.push({ name: 'AuthErrorPage' }).catch(() => {})
  }

  passwordLimitError() {
    // go login
    this.$store.common.alertMessageForGlobal({
      code: 401,
      title: 'Your account is locked.',
      message: 'Please contact your administrator.',
    })
    // router.push({ name: 'PasswordReset' }).catch(() => {})
  }

  refreshToken() {
    return new Promise((resolve, reject) => {
      const refreshToken = this.getRefreshToken()
      const lang = this.$i18n.locale || 'ko'
      if (refreshToken) {
        AccountApi.refreshToken(refreshToken, lang).then(async (res) => {
          const data = res.data
          if (data?.result) {
            // save token
            const accessToken = data.result.accessToken
            const refreshToken = data.result.refreshToken
            const payload = this.parseToken(accessToken)

            const tokens = {
              accessToken,
              refreshToken,
              exp: payload?.exp,
            }
            this.$localStorage.setItem(LocalStorageType.ACCESS_TOKEN, tokens)

            resolve(true)
          } else {
            resolve(false)
          }
        })
      } else {
        resolve(false)
      }
    })
  }

  async checkAccessToken(isLogin = false) {
    let user = this.$localStorage.getItem(LocalStorageType.ACCESS_TOKEN)
    if (user && user.accessToken !== '') {
      if (user.exp) {
        const currentTime = Math.floor(+new Date() / 1000)
        const remainingTime = user.exp - currentTime

        if (isLogin && remainingTime < 0) {
          this.$localStorage.removeItem(LocalStorageType.ACCESS_TOKEN)
          return null
        } else if (remainingTime < 60 * 5) {
          const result = await this.refreshToken()
          if (result) {
            user = this.$localStorage.getItem(LocalStorageType.ACCESS_TOKEN)
          } else {
            this.authError()
          }
        }
      }

      return user.accessToken
    }

    return null
  }

  isValidToken() {
    const user = this.$localStorage.getItem(LocalStorageType.ACCESS_TOKEN)

    if (user && user.accessToken !== '') {
      if (user.exp) {
        const currentTime = Math.floor(+new Date() / 1000)
        if (user.exp < currentTime) {
          return false
        }
      }
      return true
    }
    return false
  }

  getAccessToken() {
    const accessToken = this.$localStorage.getItem(LocalStorageType.ACCESS_TOKEN)

    return accessToken || null
  }

  getRefreshToken() {
    const refreshToken = this.$localStorage.getItem(LocalStorageType.REFRESH_TOKEN)

    return refreshToken || null
  }

  parseToken(token) {
    if (!token) {
      return
    }

    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(function (c) {
          return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
        })
        .join(''),
    )

    return JSON.parse(jsonPayload)
  }

  getUserRole() {
    return this.$store.account.getUserRole
  }

  async loginInitialize() {
    try {
    } catch (error) {
      return Promise.reject(error)
    }

    return Promise.resolve({ result: true })
  }

  logoutInitialize(isSessionTimeout = false) {
    // reset token, and information
    this.$localStorage.removeItem(LocalStorageType.ACCESS_TOKEN)
    this.$localStorage.removeItem(LocalStorageType.REFRESH_TOKEN)

    this.$store.common.logoutInitialize()
    document.body.classList.remove('dark')
  }
}

export default new AuthService()
