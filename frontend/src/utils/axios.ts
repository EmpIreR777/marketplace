import axios from 'axios'
import {useUser} from '@/stores/User'
import {Api, refreshUserToken} from '@/api/user'


// import axios from 'axios';
// import Cookies from 'js-cookie';
//
// const csrfToken = Cookies.get('csrftoken');
//
// axios.defaults.headers.common['X-CSRF-TOKEN'] = csrfToken;

// Function to retrieve CSRF token from cookies
function getCsrfToken() {
  const name = 'csrftoken='
  const decodedCookie = decodeURIComponent(document.cookie)
  const cookies = decodedCookie.split(';')
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim()
    if (cookie.startsWith(name)) {
      return cookie.substring(name.length, cookie.length)
    }
  }
  return null
}

// Create Axios instance
export const api = axios.create({
  baseURL: import.meta.env.VITE_BASE_URL,
  withCredentials: true, // Ensure cookies are sent with requests
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add CSRF token to headers for every request
api.interceptors.request.use(
  (config) => {
    const csrfToken = getCsrfToken()
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken
    }

    config.params = {
      ...(config.params || {}),
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response) {
      console.error('API Error:', error.response.data)
    }
    return Promise.reject(error)
  },
)

api.interceptors.request.use(
  async (config) => {
    const userStore = useUser()
    if (userStore.accessToken){
      config.headers['Authorization'] = `Bearer ${userStore.accessToken}`
    }
    return config
  },

  (error) => {
    return Promise.reject(error)
  },
)

let isRefreshing = false
let refreshSubscribers: ((token: string) => void)[] = []

// Функция для добавления запросов в очередь, пока токен не будет обновлен
function subscribeTokenRefresh(cb: (token: string) => void) {
  refreshSubscribers.push(cb)
}

// После обновления токена вызываем все сохранённые запросы
function onRefreshed(token: string) {
  refreshSubscribers.forEach((cb) => cb(token))
  refreshSubscribers = []
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const userStore = useUser()
    const originalRequest = error.config

    // Проверяем, если ошибка связана с истекшим токеном
    if ((error.response.status === 401 || error.response.status === 403 ) && !originalRequest._retry && userStore.getAccessToken.length) {
      originalRequest._retry = true
      if (originalRequest.url === Api.TOKEN_REFRESH) {
        await userStore.logoutUser()
        return
      }
      if (!isRefreshing) {
        isRefreshing = true

        try {
          const refreshToken = userStore.refreshToken
          const { access, refresh } = await refreshUserToken({ refresh: refreshToken })
          userStore.setAccessToken(access)
          userStore.setRefreshToken(refresh)
          api.defaults.headers['Authorization'] = access
          onRefreshed(access)

          isRefreshing = false

          // Повторяем оригинальный запрос с новым токеном
          return api(originalRequest)
        } catch (error) {
          isRefreshing = false
          return Promise.reject(error)
        }
      }

      // Если токен обновляется, ждем завершения и повторяем запрос
      return new Promise((resolve) => {
        subscribeTokenRefresh((token) => {
          originalRequest.headers['Authorization'] = token
          resolve(api(originalRequest))
        })
      })
    }

    return Promise.reject(error)
  },
)
