import { defineStore } from 'pinia'
import type { Router } from 'vue-router'
import type { IAccessTokenDecode, IUser, IUserData } from '@/stores/User/model'

import type {
  IChangeResponse,
  IUserActivationBody,
  IUserActivationMailBody,
  IUserChangePassword,
  IUserLoginBody,
  IUserProfile,
  IUserRegisterBody,
} from '@/api/user/models'
import {
  activationSetUserEmail,
  activationUser,
  createUserToken,
  deleteUser,
  getUsersMe,
  patchUserProfile,
  registerUser,
  resetUserEmail,
  resetUserPassword,
  resetUserPasswordConfirm,
  setUserEmail,
  setUserPassword,
  verifyUserToken,
} from '@/api/user'
import { useAuth } from '@/composable/auth.ts'
import { useRouter } from 'vue-router'
import { AccountTypeEnum } from '@/enums/userEnum'
import { VerificationStatus } from '@/enums/verificationStatuses'

const { accessToken, refreshToken, setAccessToken, setRefreshToken } = useAuth()

export const useUser = defineStore('user', {
  state: (): IUser => ({
    id: '',
    accessToken: accessToken || '',
    accessTokenDecode: {} as IAccessTokenDecode,
    refreshToken: refreshToken || '',
    isActivated: false,
    isAuthenticated: !!accessToken,
    uid: '',
    resetToken: '',
    user: JSON.parse(localStorage.getItem('user') || '{}') || { email: '', id: null },
    temporaryMail: '',
    userProfile: null,
    isVerified: false,
    isInitialized: false,
    router: useRouter(),
  }),

  getters: {
    getUser(): IUserData {
      return this.user
    },
    getActivateStatus(): boolean {
      return this.isActivated
    },
    getIsAuthenticated(): boolean {
      return this.accessToken !== ''
    },
    getUid(): string {
      return this.uid
    },
    getResetToken(): string {
      return this.resetToken
    },
    getUserId(): number | undefined {
      return this.userProfile?.id
    },
    getAccessToken(): string {
      return this.accessToken
    },
    getTemporaryMail(): string {
      return this.temporaryMail
    },
    getUserProfile(): IUserProfile | void {
      if (this.userProfile) return this.userProfile
    },
    getIsVerified(state): boolean {
      return state.userProfile && 'is_verified' in state.userProfile
        ? state.userProfile.is_verified
        : false
    },
    getVerifiedStatus(state): VerificationStatus {
      return state.userProfile && 'verification_status' in state.userProfile
        ? state.userProfile.verification_status
        : VerificationStatus.UNVERIFIED
    },
    getUserPhoto(state) {
      if (state.userProfile?.photo) return state.userProfile?.photo
    },
    isAuthor(state) {
      return state.userProfile?.account_type === AccountTypeEnum.AUTHOR
    },
    isStudent(state) {
      return state.userProfile?.account_type === AccountTypeEnum.STUDENT
    },
  },

  actions: {
    // 📌  Инициализация стора (автологин)
    async initApp(): Promise<void> {
      try {
        if (this.getAccessToken) {
          // await verifyUserToken(accessToken)
          await this.fetchUser()
        }
      } catch (error) {
        await this.logoutUser()
        return Promise.reject(error)
      } finally {
        this.setIsInitialized(true)
      }
    },
    // async initializeStore() {
    //   const accessToken = localStorage.getItem('accessToken')
    //   const refreshToken = localStorage.getItem('refreshToken')
    //   // const userData = localStorage.getItem('user')
    //
    //   if (accessToken) {
    //     this.setAccessToken(accessToken)
    //     // const decoded = jwtDecode<IAccessTokenDecode>(accessToken)
    //     // this.setAccessTokenDecode(decoded)
    //   }
    //
    //   if (refreshToken) {
    //     this.setRefreshToken(refreshToken)
    //   }
    //
    //   // if (userData) {
    //     // this.setUser(JSON.parse(userData))
    //   // }
    // },

    // 📌  Регистрация пользователя
    async createUser(body: IUserRegisterBody) {
      try {
        return await registerUser(body)
      } catch (error) {
        return Promise.reject(error)
      }
    },

    // 📌  Активация пользователя
    async activationUser(body: IUserActivationBody) {
      try {
        const response = await activationUser(body)
        if (response) {
          this.setAccessToken(response.access_token)
          this.setRefreshToken(response.refresh_token)
          // const decoded = jwtDecode(response.access_token)
          // this.setAccessTokenDecode(decoded)
          await this.fetchUser()
          this.setActivateStatus(true)
        }
      } catch (error) {
        return Promise.reject(error)
      }
    },
    async finalRegister(body: IUserActivationBody) {
      await this.activationUser(body)
      // if (this.accessTokenDecode.user_id) {
      //   await this.fetchUserById(this.accessTokenDecode.user_id)
      // }
    },
    // 📌  Логин пользователя
    async loginUser(body: IUserLoginBody, router: Router) {
      await this.fetchToken(body)
      // if (this.accessTokenDecode.user_id) {
      //   await this.fetchUserById(this.accessTokenDecode.user_id)
      // }
      // console.log('login')
      await router.push('/account')
    },

    // 📌  Получение токена
    async fetchToken(body: IUserLoginBody) {
      try {
        const response = await createUserToken(body)
        this.setAccessToken(response.access)
        this.setRefreshToken(response.refresh)
        await this.initApp()
        // const decoded = jwtDecode<IAccessTokenDecode>(response.access)
        // this.setAccessTokenDecode(decoded)
        return response
      } catch (error) {
        return Promise.reject(error)
      }
    },

    // 📌  Получение данных пользователя
    // async fetchUserById(id: number) {
    //   try {
    //     const response = await fetchUser(id)
    //     this.setUser(response)
    //   } catch (error) {
    //     return Promise.reject(error)
    //   }
    // },

    // 📌  Выход пользователя
    async logoutUser() {
      this.setAccessToken('')
      this.setRefreshToken('')
      // this.setAccessTokenDecode({} as IAccessTokenDecode)
      // this.setUser({ email: '', id: null })
      this.setActivateStatus(false)

      // Очистка localStorage
      // localStorage.removeItem('accessToken')
      // localStorage.removeItem('refreshToken')
      // localStorage.removeItem('user')
      // console.log('logout')
      await this.router.push('/')
    },
    // 📌  Обновление токена
    // async fetchRefreshToken() {
    //   try {
    //     const response = await refreshUserToken({ refresh: this.refreshToken })
    //     if (response) {
    //       this.setAccessToken(response.access)
    //       this.setRefreshToken(response.refresh)
    //       // const decoded = jwtDecode(response.access)
    //       // this.setAccessTokenDecode(decoded)
    //     }
    //   } catch (error) {
    //     console.error('Failed to refresh token', error)
    //   }
    // },

    // 📌  Верификация токена
    async verifyToken() {
      await verifyUserToken(this.accessToken)
    },

    // 📌  Восстановление пароля
    async resetPassword(body: { email: string }) {
      try {
        await resetUserPassword(body)
        // console.log(response)
      } catch (error) {
        return Promise.reject(error)
      }
    },

    // 📌  Подтверждение сброса пароля
    async resetPasswordConfirm(body: IUserChangePassword) {
      try {
        const response = await resetUserPasswordConfirm(body)
        if (response) {
          this.setAccessToken(response.access_token)
          this.setRefreshToken(response.refresh_token)
          await this.initApp()
          // const decoded = jwtDecode(response.access_token)
          // this.setAccessTokenDecode(decoded)
        }
      } catch (error) {
        return Promise.reject(error)
      }
    },

    // 📌  Смена пароля
    async changeNewPassword(body: IUserChangePassword) {
      await this.resetPasswordConfirm(body)
      // if (this.accessTokenDecode.user_id) {
      //   await this.fetchUserById(this.accessTokenDecode.user_id)
      // }
    },
    // 📌  Сохранение данных для сброса пароля
    setDataResetPasswordEmail(uid: string, token: string) {
      if (!uid || !token) return
      this.resetToken = token
      this.uid = uid
      this.setActivateStatus(true)
    },
    // 📌  Получение данных пользователя
    async fetchUser() {
      try {
        const data = await getUsersMe()
        this.setUserProfile(data)
        return data
      } catch (error) {
        return Promise.reject(error)
      }
    },
    // 📌  Изменеие данных пользователя
    async patchProfileById(body: FormData) {
      const id = this.getUserId
      try {
        if (id) {
          const response = await patchUserProfile(id, body)
          this.setUserProfile(response)
          return response
        }
      } catch (error) {
        return Promise.reject(error)
      }
    },
    // 📌  Изменеие e-mail пользователя
    async setEmail(body: { password: string; new_email: string }) {
      try {
        await setUserEmail(body)
      } catch (error) {
        return Promise.reject(error)
      }
    },
    async setResetEmail(body: { email: string }) {
      try {
        await resetUserEmail(body)
      } catch (error) {
        return Promise.reject(error)
      }
    },
    async activationUserEmail(body: IUserActivationMailBody): Promise<IChangeResponse> {
      try {
        return await activationSetUserEmail(body)
      } catch (error) {
        return Promise.reject(error)
      }
    },
    // 📌  Полный процесс изменения данных e-mail пользователя
    async changeUserEmail(body: IUserActivationMailBody) {
      const response = await this.activationUserEmail(body)
      if (response.is_success) {
        // this.initApp()
        // console.log('changeUserEmail')
      }
    },
    // 📌  Изменеие пароля пользователя (исползование страрого пароля)
    async setPassword(body: { password: string; new_password: string; re_new_password: string }) {
      try {
        await setUserPassword(body)
      } catch (error) {
        return Promise.reject(error)
      }
    },
    // 📌  Удаление ползователя
    async deleteUserForViewing(body: { password: string }) {
      const id = this.getUserId
      try {
        if (id) {
          await deleteUser(id, body)
        }
      } catch (error) {
        return Promise.reject(error)
      }
    },
    // 📌  Установка данных пользователя
    // setUser(data: IUserData) {
    //   this.user = data
    //   localStorage.setItem('user', JSON.stringify(data))
    // },
    setActivateStatus(status: boolean) {
      this.isActivated = status
    },
    setAccessToken(token: string) {
      this.accessToken = token
      setAccessToken(token)
    },

    setRefreshToken(token: string) {
      this.refreshToken = token
      setRefreshToken(token)
    },
    // setAccessTokenDecode(token: IAccessTokenDecode) {
    //   this.accessTokenDecode = token
    // },
    setTemporaryMail(mail: string) {
      this.temporaryMail = mail
    },
    setUserProfile(profile: IUserProfile) {
      this.userProfile = profile
    },
    setVerifiedStatus(status: boolean) {
      this.isVerified = status
    },
    setIsInitialized(status: boolean) {
      this.isInitialized = status
    },
  },
})
