import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { AccountApi, UsersApi } from '@/api'
import { USER_DATA } from '@/constants/LocalStorage.type'
import router from '@/router'

const useAuthStore = defineStore('auth', () => {
    // State - JWT is stored in HttpOnly cookie, not accessible from JS
    // userData in localStorage is only for UI display, NOT for auth verification
    const user = ref(JSON.parse(localStorage.getItem(USER_DATA) || 'null'))
    const authVerified = ref(false) // Track if we've verified with server this session

    // Getters
    const isAuthenticated = computed(() => authVerified.value && !!user.value)
    const currentUser = computed(() => user.value)

    // Actions
    const setUser = (userData) => {
        user.value = userData
        authVerified.value = !!userData
        if (userData) {
            localStorage.setItem(USER_DATA, JSON.stringify(userData))
        } else {
            localStorage.removeItem(USER_DATA)
        }
    }

    const login = async (username, password) => {
        try {
            await AccountApi.login({ username, password })
            await fetchUser()
            authVerified.value = true
            return true
        } catch (error) {
            console.error('[AuthStore] Login error:', error)
            throw error
        }
    }

    const register = async (userData) => {
        try {
            const response = await AccountApi.register(userData)
            return response.data
        } catch (error) {
            console.error('[AuthStore] Register error:', error)
            throw error
        }
    }

    const logout = async () => {
        try {
            await AccountApi.logout()
        } catch (error) {
            console.error('[AuthStore] Logout error:', error)
        } finally {
            setUser(null)
            authVerified.value = false
            router.push('/login')
        }
    }

    const checkAuth = async () => {
        // If already verified this session and have user data, skip API call
        if (authVerified.value && user.value) {
            return true
        }

        try {
            await fetchUser()
            return true
        } catch {
            // 401 is expected when not logged in, don't log as error
            setUser(null)
            authVerified.value = false
            return false
        }
    }

    const fetchUser = async () => {
        try {
            const response = await UsersApi.getCurrentUser()
            setUser(response.data)
            authVerified.value = true
            return response.data
        } catch (error) {
            // Only log if it's not a 401 (which is expected when not authenticated)
            if (error.response?.status !== 401) {
                console.error('[AuthStore] Fetch user error:', error)
            }
            setUser(null)
            authVerified.value = false
            throw error
        }
    }

    const updateProfile = async (data) => {
        try {
            const response = await UsersApi.updateProfile(data)
            setUser(response.data)
            return response.data
        } catch (error) {
            console.error('[AuthStore] Update profile error:', error)
            throw error
        }
    }

    const changePassword = async (data) => {
        try {
            const response = await UsersApi.changePassword(data)
            return response.data
        } catch (error) {
            console.error('[AuthStore] Change password error:', error)
            throw error
        }
    }

    return {
        user,
        authVerified,
        isAuthenticated,
        currentUser,
        setUser,
        login,
        register,
        logout,
        fetchUser,
        checkAuth,
        updateProfile,
        changePassword,
    }
})

export default useAuthStore
