import axios from 'axios'
import router from '@/router'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const instance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - cookie is sent automatically with withCredentials
instance.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - handle 401 Unauthorized
instance.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login on 401 Unauthorized
      router.push('/login')
    }
    return Promise.reject(error)
  }
)

export default instance
