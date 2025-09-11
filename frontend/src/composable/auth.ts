import {ACCESS_TOKEN, REFRESH_TOKEN} from '@/enums/authEnum'

interface AuthComposition {
  accessToken: string | null
  setAccessToken: (token: string) => void
  refreshToken: string | null
  setRefreshToken: (token: string) => void
  clearAuth: () => void
}

export function useAuth(): AuthComposition {
  const accessToken = localStorage.getItem(ACCESS_TOKEN) as string | null
  const refreshToken = localStorage.getItem(REFRESH_TOKEN) as string | null

  const setAccessToken = (data: string) => {
    localStorage.setItem(ACCESS_TOKEN, data)
  }

  const setRefreshToken = (data: string) => {
    localStorage.setItem(REFRESH_TOKEN, data)
  }

  const clearAuth = () => {
    localStorage.removeItem(ACCESS_TOKEN)
  }

  return {
    accessToken,
    refreshToken,
    setAccessToken,
    setRefreshToken,
    clearAuth,
  }
}
