<script setup lang="ts">
import { ref } from 'vue'
import { useField, useForm } from 'vee-validate'
import * as yup from 'yup'
import InfoItem from '@/components/contacts/InfoItem.vue'
import { AppColors } from '@/enums/appColors.ts'
import { rules } from '@/utils/helpers'
import { NAME, organizationInfoItems, organizationContactItems } from '@/enums/contactsEnum'
import { postContactForm } from '@/api/contacts'
import type { IContact } from '@/api/contacts/models'
import { useSnackbarStore } from '@/stores/Snackbar'
import { useMetrika } from '@/composable/useMetrika'
import personalDataConsent from '@/assets/docs/personal_data_consent.pdf'
import platformUseAgreement from '@/assets/docs/platform_use_agreement.pdf'
import userAgreement from '@/assets/docs/user_agreement.pdf'
import disclaimer from '@/assets/docs/disclaimer.pdf'

const FILL_IN_THE_FIELD_MSG = 'Это поле должно быть заполнено'

const snackbarStore = useSnackbarStore()

const { contactFormSubmit } = useMetrika()

const { handleSubmit, validate, errors, resetForm } = useForm({
  validationSchema: yup.object({
    name: yup.string().required().min(1),
    email: yup.string().required().email(),
    theme: yup.string().required(),
    message: yup.string().required(),
    is_agreed: yup.boolean().oneOf([true]).required(),
  }),
})

const name = useField<string>('name')
const email = useField<string>('email')
const theme = useField<string>('theme')
const message = useField<string>('message')
const is_agreed = useField<boolean>('is_agreed')

const isFormValid = ref(false)
const isLoading = ref(false)
const isError = ref(false)

const checkErrorsBeforeSubmit = async () => {
  await validate()

  isFormValid.value = Object.keys(errors.value).length === 0
}

const submit = handleSubmit(async (values) => {
  isLoading.value = true

  try {
    if (isFormValid.value) {
      const response = await postContactForm({ ...(values as IContact) })
      if (response.status === 200 || response.status === 201) {
        resetForm()

        snackbarStore.showSnackbar({
          title: 'Сообщение отправлено!',
          message:
            'Ваш запрос был успешно отправлен. Наши специалисты свяжутся с вами в ближайшее время.',
          action: { label: 'Ок', onClick: () => (snackbarStore.show = false) },
        })
        contactFormSubmit()
      }
    }
  } catch (error) {
    isError.value = true
    console.log('ERROR', error)
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="contacts">
    <div class="contacts__container">
      <div class="contacts__header">
        <h1 class="contacts__title">Контакты</h1>
      </div>
      <div class="contacts__info-container">
        <InfoItem
          :img-src="NAME.imgSrc"
          :icon="NAME.icon"
          :title="NAME.title"
          :text="NAME.text"
          :linkType="NAME.linkType || ''"
        />

        <div v-for="(item, i) in organizationInfoItems" class="contacts__info-item" :key="i">
          <InfoItem
            :img-src="item.imgSrc"
            :icon="item.icon"
            :title="item.title"
            :text="item.text"
            :linkType="item.linkType || ''"
          />
        </div>

        <div class="contacts__social-container">
          <div v-for="(item, i) in organizationContactItems" class="contacts__social-item" :key="i">
            <InfoItem
              :img-src="item.imgSrc"
              :title="item.title"
              :text="item.text"
              :linkType="item.linkType || ''"
            />
          </div>
        </div>

        <div class="d-flex flex-column ga-2">
          <a
            :href="personalDataConsent"
            target="_blank"
            class="text-body-1 font-weight-bold"
            :style="{ color: AppColors.MAIN_TEXT }"
          >
            Согласие на обработку персональных данных
          </a>
          <a
            :href="platformUseAgreement"
            target="_blank"
            class="text-body-1 font-weight-bold"
            :style="{ color: AppColors.MAIN_TEXT }"
          >
            Договор об использовании платформы
          </a>
          <a
            :href="userAgreement"
            target="_blank"
            class="text-body-1 font-weight-bold"
            :style="{ color: AppColors.MAIN_TEXT }"
          >
            Пользовательское соглашение
          </a>
          <a
            :href="disclaimer"
            target="_blank"
            class="text-body-1 font-weight-bold"
            :style="{ color: AppColors.MAIN_TEXT }"
          >
            Информационное сообщение для посетителей
          </a>
        </div>
      </div>
    </div>
    <div class="contacts__container">
      <div class="contacts__header">
        <h2 class="contacts__contact-us">Свяжитесь с нами</h2>
      </div>
      <div class="contacts__form-wrapper">
        <form @submit.prevent="submit" class="contacts__form">
          <v-text-field
            v-model="name.value.value"
            label="Имя"
            rounded="lg"
            :rules="[() => name.value.value?.length > 0 || 'Должно быть имя']"
            :error="!name.value.value?.length && !!errors.name"
            :error-messages="!name.value.value?.length && errors.name ? FILL_IN_THE_FIELD_MSG : ''"
            variant="outlined"
          />
          <v-text-field
            variant="outlined"
            v-model="email.value.value"
            :rules="[rules.email(email.value.value)]"
            :error="!email.value.value && !!errors.email"
            :error-messages="errors.email && !email.value.value ? FILL_IN_THE_FIELD_MSG : ''"
            label="Email"
            rounded="lg"
          />
          <v-text-field
            v-model="theme.value.value"
            label="Тема"
            rounded="lg"
            :error="!!errors.theme"
            :error-messages="errors.theme ? FILL_IN_THE_FIELD_MSG : ''"
            variant="outlined"
          />
          <v-textarea
            v-model="message.value.value"
            label="Сообщение"
            rounded="lg"
            variant="outlined"
            :error="!!errors.message"
            :error-messages="!!errors.message ? FILL_IN_THE_FIELD_MSG : ''"
          />
          <v-checkbox
            class="custom-checkbox"
            v-model="is_agreed.value.value"
            label="Я даю согласие на обработку моих персональных данных"
            type="checkbox"
            :value="true"
          ></v-checkbox>
          <v-btn
            class="mt-6 pa-4 submit-button"
            type="submit"
            height="56"
            width="280"
            rounded="lg"
            :disabled="!is_agreed.value.value"
            :color="
              is_agreed.value.value
                ? AppColors.ACCENT_COLOR_LIME_100
                : AppColors.ACCENT_COLOR_LIME_20
            "
            @click="checkErrorsBeforeSubmit"
          >
            Отправить
          </v-btn>
        </form>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.contacts {
  display: flex;
  flex-direction: row;
  gap: 40px;
  padding-bottom: 40px;
  @include md() {
    gap: 20px;
  }

  @include sm() {
    flex-direction: column;
    gap: 24px;
    padding-bottom: 0;
  }

  &__container {
    width: 50%;

    @include sm() {
      width: 100%;
    }
  }

  &__header {
    display: flex;
    justify-content: start;
    align-items: center;
  }

  &__title {
    @include typography('h3');

    margin-bottom: 48px;

    @include xs() {
      @include typography('h6');

      margin-bottom: 24px;
    }
  }

  &__contact-us {
    margin-bottom: 36px;

    @include typography('h6');

    @include xs() {
      margin-bottom: 24px;
    }
  }

  &__form-wrapper {
    @include sm() {
      display: flex;
      align-items: center;
      justify-content: center;
      padding-bottom: 80px;
    }
  }

  &__form {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;

    @include sm() {
      width: 80%;
    }

    @include xs() {
      width: 100%;
    }
  }

  &__info-container {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    @include md() {
      gap: 1rem;
    }
  }

  &__info-item {
    // margin-bottom: 48px;

    // @include md() {
    //   margin-bottom: 32px;
    // }

    // @include sm() {
    //   margin-bottom: 16px;
    // }
  }

  &__social-container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 32px;

    @include md() {
      flex-direction: column;
    }

    @include sm() {
      flex-direction: row;
      gap: 16px;
    }

    @include xs() {
      flex-direction: column;
      gap: 16px;
    }
  }

  &__social-item {
    width: calc(50% - 16px);

    @include sm() {
      width: calc(50% - 8px);
    }

    @include xs() {
      width: 100%;
    }
  }

  & ::v-deep(.v-btn.v-btn--disabled .v-btn__overlay) {
    background-color: transparent !important;
  }

  & ::v-deep(.v-btn.v-btn--disabled .v-btn__content) {
    opacity: 0.5 !important;
  }

  & .submit-button {
    @include typography('lgb');
  }
}
</style>
