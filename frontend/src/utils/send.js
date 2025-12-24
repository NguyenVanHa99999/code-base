import i18n from '@/locales/i18n'
import AuthService from '@/services/auth.service'
import axios from 'axios'

const API_BASE_URL = '/v1/api'

axios.defaults.headers = {
  'Content-Type': 'application/json',
}

let isRefreshing = false
const requestsQueue = new Map()

const instance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 1000 * 30,
})
instance.API_BASE_URL = API_BASE_URL

instance.interceptors.request.use(
  async (config) => {
    const notUseTokenUrl = ['/authentication/authenticate', '/authentication/refresh-token']
    if (notUseTokenUrl.some((url) => url === config.url)) {
    } else {
      const token = await AuthService.checkAccessToken()

      if (token) {
        config.headers.Authorization = 'Bearer ' + token
      }
    }
    return config
  },
  function (error) {
    return Promise.reject(error)
  },
  function (config) {
    return config
  },
)

instance.interceptors.response.use(
  async function (response) {
    return response
  },

  async function (error) {
    const { t } = i18n
    if (error.response && error.response.status) {
      let serverError = error.response?.data
      const statusCode = error.response.status

      if (serverError && serverError instanceof Blob) {
        serverError = JSON.parse(await serverError.text())
      }

      if (error.config?.url === '/authentication/refresh-token') {
        if ([500, 501, 502, 503, 504].indexOf(statusCode) > -1) {
          AuthService.authError()
          return Promise.reject(error)
        }
      }

      if (error.response.status !== 401 && serverError?.message) {
        const message = serverError?.message
        const fixedTitle = [500].includes(statusCode)
          ? t('common.label.error')
          : t('common.label.warning')
        //  show alert
      }

      switch (error.response.status) {
        case 401: // [Unauthorized]
          if (!isRefreshing) {
            isRefreshing = true
            const { data } = await AuthService.refreshToken()
            isRefreshing = false
            requestsQueue.forEach((cb) => cb(data))
            requestsQueue.clear()
          }
          requestsQueue.set(error.config.url, async (data) => {
            const { accessToken } = data
            instance.defaults.headers.Authorization = `Bearer ${accessToken}`
          })
          AuthService.authError()
          break
        case 403: {
          // show alert
          break
        }

        case 500:
        case 501:
        case 502:
        case 504:
        case 503: {
          break
        }
        default: {
          break
        }
        // case 400: // [Bad Request]
        //   break
        // case 404: // [Not Found]
        //   break
        // case 405: // [Method Not Allowed]
        //   break
        // case 409: // [Conflict]
        //   break
        // case 429: // [Too Many Requests]
        //   break
      }
    } else if (error.name === 'AxiosError') {
    }
    return Promise.reject(error)
  },
)

export default instance
