import Send from '@/utils/send'

/**
 * Account API - Authentication endpoints
 * 
 * Login endpoint được config qua VITE_LOGIN_ENDPOINT trong .env
 * để hỗ trợ các portal khác nhau (Admin, Teacher, Student)
 */

// Login endpoint từ env, mặc định là /auth/login
const LOGIN_ENDPOINT = import.meta.env.VITE_LOGIN_ENDPOINT || '/auth/login'

export default {
  /**
   * Login với email/password
   * Endpoint được xác định bởi VITE_LOGIN_ENDPOINT trong .env
   * - Admin: /auth/login/admin
   * - Teacher: /auth/login/teacher
   * - Student: /auth/login/student
   */
  login(data) {
    const formData = new URLSearchParams()
    formData.append('username', data.username)
    formData.append('password', data.password)

    return Send({
      url: LOGIN_ENDPOINT,
      method: 'POST',
      data: formData,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
  },

  /**
   * Đăng ký tài khoản mới
   * Mặc định role là 'student'
   */
  register(data) {
    return Send({
      url: '/auth/register',
      method: 'POST',
      data,
    })
  },

  /**
   * Logout - Clear cookie và session
   */
  logout() {
    return Send({
      url: '/auth/logout',
      method: 'POST',
    })
  },

  /**
   * Kiểm tra email đã tồn tại chưa
   */
  checkEmailExists(email) {
    return Send({
      url: `/auth/check-email/${email}`,
      method: 'GET',
    })
  },

  /**
   * Lấy danh sách roles (public)
   */
  getRoles() {
    return Send({
      url: '/auth/roles',
      method: 'GET',
    })
  },
}
