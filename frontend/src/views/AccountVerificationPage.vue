<script setup lang="ts">
// import { useRoute } from 'vue-router'
// import { computed, ref } from 'vue'
// import IndividualTeacherVerification from '@/components/accountVerification/IndividualTeacherVerification.vue'
// import UniversityStudyingVerification from '@/components/accountVerification/UniversityStudyingVerification.vue'
// import LegalEntity from '@/components/accountVerification/LegalEntity.vue'
// import { EntityType } from '@/enums/legalTypes'

import AccountVerification from '@/components/accountVerification/AccountVerification.vue'

// const route = useRoute()
// const accountType = computed(() => route.params.type)

// const isUniversity = ref<boolean>(false)
//
</script>

<template>
  <AccountVerification />

  <!-- <IndividualTeacherVerification v-if="accountType === EntityType.INDIVIDUAL" />
  <LegalEntity v-if="!isUniversity && accountType !== EntityType.INDIVIDUAL" />
  <UniversityStudyingVerification v-if="isUniversity && accountType !== EntityType.INDIVIDUAL" /> -->
</template>

<style scoped></style>
