<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useUser } from '@/stores/User'
import { formatDate } from '@/utils/helpers.ts'
import DialogScreen from '@/components/common/DialogScreen.vue'
import ChangeEmailDialog from '@/components/account/ChangeEmailDialog.vue'
import ChangePasswordDialog from '@/components/account/ChangePasswordDialog.vue'
import AdditionFilesLinks from '@/components/account/AdditionFilesLinks.vue'
import DeleteAccount from '@/components/account/DeleteAccount.vue'
import VerificationRequest from '@/components/account/VerificationRequest.vue'
import { useProfileStore } from '@/stores/Account/profile'
import BaseTextField from '@/components/common/BaseTextField.vue'
import BaseDateInput from '@/components/common/BaseDateInput.vue'
import BaseButton from '@/components/common/BaseButton.vue'

const profileStore = useProfileStore()

const isProcessChangeMail = ref(false)
const handleChangeEmail = (newVal: boolean) => {
  isProcessChangeMail.value = newVal
}

const isProcessChangePassword = ref(false)
const handleChangePassword = (newVal: boolean) => {
  isProcessChangePassword.value = newVal
}

const isProgressDeleteAccount = ref(false)
const handleProgressDeleteAccount = () => {
  isProgressDeleteAccount.value = !isProcessChangePassword.value
}

const fileInput = ref<HTMLInputElement | null>(null)
const selectedFile = ref<File | null>(null)
const userStore = useUser()

onMounted(() => {
  profileStore.initData()
  userStore.fetchUser()
})

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (!target.files || target.files.length === 0) return

  const file = target.files[0]
  selectedFile.value = file
  profileStore.photo = URL.createObjectURL(file)
}

// const formattedBirthDate = computed({
//   get: () => (birthDate.value ? formatDate(birthDate.value) : ''),
//   set: (val) => {
//     birthDate.value = val ? new Date(val) : null
//   },
// })

const uploadData = async () => {
  const profile = userStore.userProfile
  if (!profile) return

  const formData = new FormData()
  const updatedFields: Record<string, string> = {} // Хранит только измененные поля

  const addFieldIfChanged = (key: string, newValue: string | null, oldValue: string | null) => {
    if (newValue !== oldValue && newValue !== null) {
      updatedFields[key] = newValue
      formData.append(key, newValue)
    }
  }

  if (profile) {
    addFieldIfChanged('first_name', profileStore.firstName, profile.first_name)
    addFieldIfChanged('last_name', profileStore.lastName, profile?.last_name)
    addFieldIfChanged('middle_name', profileStore.middleName, profile.middle_name)
    addFieldIfChanged('phone_number', profileStore.phone, profile.phone_number)
    addFieldIfChanged('bio', profileStore.about, profile.bio)
    addFieldIfChanged('region', profileStore.region, profile.region)
    addFieldIfChanged(
      'birth_date',
      profileStore.birthDate ? formatDate(new Date(profileStore.birthDate)) : null,
      profile.birth_date,
    )
  }

  // Обновляем фото, если оно было изменено
  if (selectedFile.value instanceof File) {
    formData.append('photo', selectedFile.value)
  }

  // Если нет изменений, не отправляем запрос
  if (Object.keys(updatedFields).length === 0 && !selectedFile.value) {
    // console.log('Нет изменений, запрос не отправляется.')
    return
  }

  profileStore.updateProfile(formData)
}
</script>

<template>
  <div class="profile" v-if="!isProgressDeleteAccount">
    <div class="text-h5 font-weight-bold d-block d-md-none mb-2">Профиль</div>
    <VerificationRequest v-if="userStore.isAuthor" />
    <v-sheet class="mt-6 mt-sm-4">
      <div class="profile__form-first-row">
        <div class="profile__form-image-container">
          <div class="profile__form-upload-image">
            <v-avatar size="72">
              <v-img :src="profileStore.photo"></v-img>
            </v-avatar>
            <div class="d-flex justify-center">
              <BaseButton label="Загрузить" type="flat" text="text-lg" @click="triggerFileInput" />
              <input
                type="file"
                ref="fileInput"
                accept="image/png, image/jpeg"
                class="d-none"
                @change="handleFileChange"
              />
            </div>
          </div>
          <span class="profile__description">.png .jpg / 800x800 max</span>
        </div>
        <div class="profile__form-about-container">
          <v-textarea
            v-model="profileStore.about"
            variant="outlined"
            label="О себе"
            rows="3"
            rounded="lg"
            class="input-item"
            hide-details
          ></v-textarea>
          <span class="profile__description">
            Рассказ о том, что это будет полезной инфой для преподавателей
          </span>
        </div>
      </div>

      <v-row class="pa-0 mx-0 mb-0 mt-0 mt-sm-6">
        <v-col cols="12" sm="4" class="pa-0 pr-sm-1 pr-md-2 mt-4 mt-sm-0">
          <BaseTextField v-model="profileStore.lastName" label="Фамилия" />
        </v-col>
        <v-col cols="12" sm="4" class="pa-0 px-sm-1 px-md-2 mt-4 mt-sm-0">
          <BaseTextField v-model="profileStore.firstName" label="Имя" />
        </v-col>
        <v-col cols="12" sm="4" class="pa-0 pl-sm-1 pl-md-2 mt-4 mt-sm-0">
          <BaseTextField v-model="profileStore.middleName" label="Отчество" />
        </v-col>
      </v-row>
      <v-row class="pa-0 mx-0 mb-0 mt-0 mt-sm-4">
        <v-col cols="12" sm="4" class="pa-0 pr-sm-1 pr-md-2 mt-4 mt-sm-0">
          <BaseDateInput v-model="profileStore.birthDate" />
        </v-col>
        <v-col cols="12" sm="4" class="pa-0 px-sm-1 px-md-2 mt-4 mt-sm-0">
          <BaseTextField v-model="profileStore.region" label="Регион" />
        </v-col>
        <v-col cols="12" sm="4" class="pa-0 pl-sm-1 pl-md-2 mt-4 mt-sm-0">
          <BaseTextField v-model="profileStore.phone" label="Телефон" />
        </v-col>
      </v-row>
      <v-row
        v-if="!userStore.getIsVerified && userStore.isAuthor && false"
        class="pa-0 mx-0 mb-0 mt-0 mt-sm-4"
      >
        <v-col cols="12" sm="6" md="3" class="pa-0 pr-sm-1 pr-md-2 mt-4 mt-sm-0">
          <BaseTextField v-model="profileStore.positionRank" label="Должность, Звание" />
        </v-col>
        <v-col cols="12" sm="6" md="3" class="pa-0 pl-sm-1 px-md-2 mt-4 mt-sm-0">
          <BaseTextField v-model="profileStore.experience" label="Опыт работы" />
        </v-col>
        <v-col cols="12" sm="6" md="3" class="pa-0 pr-sm-1 px-md-2 mt-4 mt-md-0">
          <BaseTextField
            v-model="profileStore.teachingExperience"
            label="Опыт преподавательской деятельности"
          />
        </v-col>
        <v-col cols="12" sm="6" md="3" class="pa-0 pl-sm-1 pl-md-2 mt-4 mt-md-0">
          <BaseTextField v-model="profileStore.university" label="Учебное заведение" />
        </v-col>
      </v-row>

      <BaseButton class="profile__submit" label="Сохранить изменения" @click="uploadData" />
    </v-sheet>
    <!--    <AdditionFilesLinks v-if="userStore.isAuthor" />-->
    <div class="profile__actions">
      <BaseButton label="Изменить email" type="outline" @click="handleChangeEmail(true)" />
      <BaseButton label="Изменить пароль" type="outline" @click="handleChangePassword(true)" />
      <BaseButton label="Удалить аккаунт" type="outline" @click="handleProgressDeleteAccount" />
    </div>
    <DialogScreen v-model="isProcessChangeMail">
      <ChangeEmailDialog @change-email="handleChangeEmail" />
    </DialogScreen>
    <DialogScreen v-model="isProcessChangePassword">
      <ChangePasswordDialog @change-password="handleChangePassword" />
    </DialogScreen>
  </div>
  <DeleteAccount v-if="isProgressDeleteAccount" />
</template>

<style lang="scss">
.profile {
  &__title {
    display: none;
    @include typography('h6');
    margin-bottom: 16px;

    @include xs {
      display: block;
    }
  }

  &__description {
    @include typography('sm');
    color: $base;
    margin-left: 16px;

    @include md {
      margin-left: 0;
    }
  }

  &__form-first-row {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 16px;

    @include xs {
      grid-template-columns: 1fr;
    }
  }

  &__form-upload-image {
    display: grid;
    grid-template-columns: 72px 1fr;
    align-items: center;
    padding: 16px;
    border: 1px solid $base-20;
    border-radius: 12px;
  }

  &__form-about-container {
    @include xs {
      & > .profile__description {
        display: none;
      }
    }
  }

  &__submit {
    margin: 32px 0 32px auto;
    width: calc(33% - 4px);

    @include md {
      width: auto;
    }

    @include xs {
      margin: 16px 0;
      width: 100%;
    }
  }

  &__actions {
    display: flex;
    gap: 16px;

    @include xs {
      flex-direction: column;
    }

    & > button {
      width: 100%;
      flex: 1;
    }
  }
}

.change-photo {
  border-radius: 12px;
  border: 1px solid var(--Base-color-20, rgba(54, 57, 64, 0.2));
}

.change-photo-button {
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: 24px; /* 150% */
  text-decoration-line: underline;
  text-decoration-style: solid;
  text-decoration-skip-ink: none;
  text-decoration-thickness: 7.5%; /* 1.2px */
  text-underline-offset: 15%; /* 2.4px */
  text-underline-position: from-font;
  text-transform: none;
}

.input-item {
  color: var(--Base-color-60, rgba(54, 57, 64, 0.6));
}

::v-deep(.v-label.v-field-label) {
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: 24px;
  width: 100%;
}

.action-button {
  border-radius: 12px;
  border: 1px solid var(--Accent-color-Lime-100, #df3);
  font-size: 16px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px;
  text-transform: none;

  @media (max-width: 600px) {
    flex: unset;
    width: 100%;
  }
}

::v-deep(.v-field__outline) {
  opacity: unset;
  border-color: var(--Base-color-20, rgba(54, 57, 64, 0.2)) !important;
  border-radius: 12px !important;
}

::v-deep(.v-input__details) {
  display: none;
}
</style>
