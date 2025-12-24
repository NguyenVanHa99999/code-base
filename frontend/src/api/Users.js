import Send from '@/utils/send'

export default {
    getCurrentUser() {
        return Send({
            url: '/api/users/me',
            method: 'GET',
        })
    },

    getUserById(id) {
        return Send({
            url: `/api/users/${id}`,
            method: 'GET',
        })
    },

    updateProfile(data) {
        return Send({
            url: '/api/users/me',
            method: 'PUT',
            data,
        })
    },

    updateAvatar(formData) {
        return Send({
            url: '/api/users/me/avatar',
            method: 'POST',
            data: formData,
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })
    },

    changePassword(data) {
        return Send({
            url: '/api/users/me/password',
            method: 'PUT',
            data,
        })
    },

    updateSettings(data) {
        return Send({
            url: '/api/users/me/settings',
            method: 'PUT',
            data,
        })
    },
}
