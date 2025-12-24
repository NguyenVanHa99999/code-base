import Send from '@/utils/send'
export default {
  login(data) {
    return Send({
      url: '/authentication/authenticate',
      method: 'POST',
      data,
    })
  },
  refreshToken() {
    return Send({
      url: '/authentication/refresh-token',
      method: 'POST',
    })
  },
  logout() {
    return Send({
      url: '/authentication/logout',
      method: 'POST',
    })
  },
  retrieveCheckUserPasswordValid() {
    return Send({
      url: '/authentication/retrieve-check-user-password-valid',
      method: 'GET',
    })
  },
}
