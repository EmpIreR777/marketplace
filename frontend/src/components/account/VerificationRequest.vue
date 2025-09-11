<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUser } from '@/stores/User'
// import YellowButton from "@/components/common/YellowButton.vue";
import BaseButton from '@/components/common/BaseButton.vue'
import { useDisplay } from 'vuetify'
import BaseSwitch from '@/components/common/BaseSwitch.vue'
import { EntityType } from '@/enums/legalTypes'
import { AuthorTypeEnum } from '@/enums/userEnum'
import { VerificationStatus } from '@/enums/verificationStatuses'
import { AppColors } from '@/enums/appColors'

const userStore = useUser()
const router = useRouter()
const { xs } = useDisplay()

const isChecked = ref(false)

const label = computed(() => (isChecked.value ? 'Юр. лицо' : 'Физ. лицо'))
const verificationPath = computed(
  () => `/account-verification/${isChecked.value ? EntityType.LEGAL : EntityType.INDIVIDUAL}`,
)

onMounted(() => {
  if (userStore.userProfile && 'author_type' in userStore.userProfile) {
    isChecked.value = userStore.userProfile?.author_type !== AuthorTypeEnum.INDIVIDUAL
  }
})
</script>

<template>
  <div class="verefication-request">
    <div
      class="verefication-request__action"
      :class="{ verified: userStore.getVerifiedStatus !== VerificationStatus.UNVERIFIED }"
    >
      <BaseButton
        v-if="userStore.getVerifiedStatus === VerificationStatus.UNVERIFIED"
        label="Запрос верификации"
        :text="xs ? 'text-smb' : 'text-lgb'"
        @click="router.push(verificationPath)"
      />
      <v-chip
        v-else-if="userStore.getVerifiedStatus === VerificationStatus.ON_VERIFICATION"
        text="В процессе верификации"
        append-icon="mdi-progress-check"
      />
      <v-chip
        v-else-if="userStore.getVerifiedStatus === VerificationStatus.VERIFIED"
        variant="flat"
        text="Верифицировано"
        :color="AppColors.ACCENT_COLOR_LIME_100"
        append-icon="mdi-check-circle-outline"
      />
    </div>

    <div
      v-if="userStore.getVerifiedStatus === VerificationStatus.UNVERIFIED"
      class="verefication-request__tip"
    >
      <span>
        Пройдите верификацию и получите возможность публиковать свои курсы на сервисе EdX
      </span>
    </div>

    <div
      v-if="userStore.getVerifiedStatus === VerificationStatus.UNVERIFIED"
      class="verefication-request__person"
    >
      {{ label }}
      <BaseSwitch
        v-model="isChecked"
        :disabled="userStore.getVerifiedStatus !== VerificationStatus.UNVERIFIED"
      />
    </div>
  </div>
</template>

<style lang="scss">
.verefication-request {
  display: grid;
  grid-template-areas: 'action tip person';
  grid-template-columns: 243px 328px 1fr;
  gap: 16px;
  align-items: center;

  @include md {
    column-gap: 8px;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(2, auto);
    grid-template-areas:
      'action person'
      'tip tip';
  }

  &__action {
    grid-area: action;

    & > button {
      padding: 16px 32px;

      @include xs {
        padding: 8px 16px;
      }
    }

    &.verified {
      & > button {
        padding: 8px 16px;
      }
    }
  }

  &__tip {
    @include typography('sm');
    grid-area: tip;
    color: $base-80;
    max-width: 328px;

    @include md {
      max-width: none;
    }
  }

  &__person {
    @include typography('lg');
    grid-area: person;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-left: auto;
    text-wrap-mode: nowrap;
  }
}
</style>
