import { defineStore } from 'pinia'
import { stubDocumentsIcon } from '@/assets/icons'
import { updateAuthor } from '@/api/author'
import { useUser } from '@/stores/User'
import type { IProfileStoreModel } from '@/stores/Account/profile/models'
import { updateStudent } from '@/api/student'
import { useMetrika } from '@/composable/useMetrika'
import { useSnackbarStore } from '@/stores/Snackbar'
import { SnackbarTypeEnum } from '@/enums/snackbarEnum'

const { studentUpdate, authorUpdate } = useMetrika()

export const useProfileStore = defineStore('profileStore', {
  state: (): IProfileStoreModel => {
    return {
      profile: null,
      photo: stubDocumentsIcon,
      about: '',
      lastName: '',
      firstName: '',
      middleName: '',
      birthDate: null,
      region: '',
      phone: '',
      positionRank: '',
      experience: '',
      teachingExperience: '',
      university: '',
    }
  },

  getters: {},

  actions: {
    async initData() {
      const userStore = useUser()
      const newProfile = userStore.getUserProfile
      this.about = newProfile?.bio || ''
      this.lastName = newProfile?.last_name || ''
      this.firstName = newProfile?.first_name || ''
      this.middleName = newProfile?.middle_name || ''
      this.birthDate = newProfile?.birth_date ? new Date(newProfile?.birth_date) : null
      this.region = newProfile?.region || ''
      this.phone = newProfile?.phone_number || ''
      this.photo = newProfile?.photo || ''
      if (userStore.isAuthor) {
        this.positionRank = ''
        this.experience = ''
        this.teachingExperience = ''
        this.university = ''
      }
    },
    async updateProfile(body: FormData) {
      const userStore = useUser()
      const snackbarStore = useSnackbarStore()

      try {
        if (userStore.isAuthor && userStore.userProfile?.account_type) {
          await updateAuthor(userStore.userProfile?.id, body)
          authorUpdate()
        }

        if (userStore.isStudent && userStore.userProfile?.account_type) {
          await updateStudent(userStore.userProfile?.id, body)
          studentUpdate()
        }
        await userStore.fetchUser()
      } catch (error) {
        snackbarStore.showSnackbar({
          title: error instanceof Error ? error.message : 'Ошибка',
          type: SnackbarTypeEnum.NEGATIVE,
        })
      }
    },
  },
})
