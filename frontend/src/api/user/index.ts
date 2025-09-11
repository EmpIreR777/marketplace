import { api } from '@/utils/axios'
import type {
  IChangeResponse,
  ICreateUserResponse,
  ILoginTokenResponse,
  ITokenResponse,
  IUserActivationBody,
  IUserActivationMailBody,
  IUserChangePassword,
  IUserLoginBody,
  IUserProfile,
  IUserRegisterBody,
} from '@/api/user/models'

// Define API Endpoints
export enum Api {
  USERS_ME = '/api/auth/users/me/',
  USER_REGISTRATION = '/api/auth/users/',
  USER_ACTIVATION = '/api/auth/users/activation/',
  USER_JWT_CREATE = '/api/auth/jwt/create/',
  USER_RESET_PASSWORD = '/api/auth/users/reset_password/',
  USER_RESET_PASSWORD_CONFIRM = '/api/auth/users/reset_password_confirm/',
  USER_SET_EMAIL = '/api/auth/users/set_email/',
  USER_RESET_EMAIL = '/api/auth/users/reset_email/',
  USER_SET_EMAIL_CONFIRM = '/api/auth/users/reset_email_confirm/',
  USER_SET_PASSWORD = '/api/auth/users/set_password/',
  TOKEN_VERIFY = '/api/auth/jwt/verify/',
  TOKEN_REFRESH = '/api/auth/jwt/refresh/',
  PROFILE = '/api/profile/',
  MY_COURSES = '/api/courses/my_courses/',
}

export async function getUsersMe() {
  const { data } = await api.get<IUserProfile>(Api.USERS_ME)
  return data
}

// Centralized error handler
function handleApiError(error: unknown, message: string) {
  console.error(`${message}:`, error)
  return Promise.reject(error)
}

// User Registration
export async function registerUser(body: IUserRegisterBody): Promise<ICreateUserResponse> {
  try {
    const response = await api.post(Api.USER_REGISTRATION, body)
    return response.data
  } catch (error) {
    return handleApiError(error, 'Register user error')
  }
}

// User Activation
export async function activationUser(body: IUserActivationBody): Promise<ITokenResponse> {
  try {
    const response = await api.post(Api.USER_ACTIVATION, body)
    return response.data
  } catch (error) {
    return handleApiError(error, 'Activation user error')
  }
}

// Create User Token
export async function createUserToken(body: IUserLoginBody): Promise<ILoginTokenResponse> {
  const { data } = await api.post(Api.USER_JWT_CREATE, body)
  return data
}

// Reset User Password
export async function resetUserPassword(body: { email: string }): Promise<void> {
  try {
    await api.post(Api.USER_RESET_PASSWORD, body)
  } catch (error) {
    return handleApiError(error, 'Reset user password error')
  }
}

// Delete user for viewing
export async function deleteUser(id: number, body: { password: string }): Promise<void> {
  try {
    await api.delete(`${Api.USER_REGISTRATION}${id}/`, {
      data: body,
    })
  } catch (error) {
    return handleApiError(error, 'Delete user confirm error')
  }
}
// Reset Password Confirmation
export async function resetUserPasswordConfirm(body: IUserChangePassword): Promise<ITokenResponse> {
  try {
    const response = await api.post(Api.USER_RESET_PASSWORD_CONFIRM, body)
    return response.data
  } catch (error) {
    return handleApiError(error, 'Reset password confirm error')
  }
}

// Set User Email (Fixed API Endpoint)
export async function setUserEmail(body: { password: string; new_email: string }): Promise<void> {
  try {
    await api.post(Api.USER_SET_EMAIL, body)
  } catch (error) {
    return handleApiError(error, 'Set user email error')
  }
}

// Reset User email
export async function resetUserEmail(body: { email: string }): Promise<void> {
  try {
    await api.post(Api.USER_RESET_EMAIL, body)
  } catch (error) {
    return handleApiError(error, 'Reset user password error')
  }
}

export async function activationSetUserEmail(
  body: IUserActivationMailBody,
): Promise<IChangeResponse> {
  try {
    const response = await api.post(Api.USER_SET_EMAIL_CONFIRM, body)
    return response.data
  } catch (error) {
    return handleApiError(error, 'Activation user email error')
  }
}

// Set User Password
export async function setUserPassword(body: {
  password: string
  new_password: string
  re_new_password: string
}): Promise<void> {
  try {
    await api.post(Api.USER_SET_PASSWORD, body)
  } catch (error) {
    return handleApiError(error, 'Set user password error')
  }
}

// Fetch User
export async function fetchUser(id: number): Promise<ICreateUserResponse> {
  try {
    const response = await api.get<ICreateUserResponse>(`${Api.USER_REGISTRATION}${id}/`)
    return response.data
  } catch (error) {
    return handleApiError(error, 'Fetch user error')
  }
}

// Verify User Token (Fixed Payload)
export async function verifyUserToken(token: string): Promise<void> {
  try {
    await api.post(Api.TOKEN_VERIFY, { token }) // Fix: Token should be sent as an object
  } catch (error) {
    return handleApiError(error, 'Verify user token error')
  }
}

// Refresh User Token
export async function refreshUserToken(body: { refresh: string }): Promise<ILoginTokenResponse> {
  try {
    const response = await api.post(Api.TOKEN_REFRESH, body)
    return response.data
  } catch (error) {
    throw error
  }
}

// Update User Profile (PATCH)
export async function patchUserProfile(
  id: number,
  body: IUserProfile | FormData,
): Promise<IUserProfile> {
  try {
    const response = await api.patch(`${Api.PROFILE}${id}/`, body, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  } catch (error) {
    console.error('Ошибка при обновлении профиля пользователя:', error)
    throw error
  }
}
