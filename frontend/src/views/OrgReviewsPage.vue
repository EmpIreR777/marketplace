<script setup lang="ts">
import { onMounted, onUnmounted, computed } from 'vue'
import { AppColors } from '@/enums/appColors.ts'
import OrgRaw from '@/components/reviews/OrgRaw.vue'
import { useOrgReviewsStore } from '@/stores/Review'
import FeedbackCard from '@/components/common/FeedbackCard.vue'
import { useUser } from '@/stores/User'

const props = defineProps<{ id: string }>()

const orgReviewsStore = useOrgReviewsStore()
const userStore = useUser()

const isMycourses = computed(() => Number(props.id) === userStore.getUserId)

onMounted(() => {
  orgReviewsStore.loadOrganization()
})

onUnmounted(() => {
  orgReviewsStore.clearStore()
})
</script>

<template>
  <v-card
    elevation="0"
    :loading="orgReviewsStore.isLoading"
    style="display: grid; grid-template-columns: 100%"
    class="ga-4 ga-md-8"
  >
    <v-card-title
      style="display: grid; grid-template-columns: 100%; white-space: wrap"
      class="pa-0 ga-4 ga-md-8"
      :style="{ borderBottom: `1px solid ${AppColors.BORDER}` }"
    >
      <h2 class="text-h5 text-md-h3 text-lg-h2 font-weight-bold">
        {{ orgReviewsStore.organization?.title }}
      </h2>

      <v-container>
        <OrgRaw
          v-if="orgReviewsStore.organization"
          :organization="orgReviewsStore.organization"
          :style="{ borderBottom: AppColors.BASE_COLOR_20 }"
        />
      </v-container>
    </v-card-title>

    <v-card-text class="pa-0 mt-n4">
      <v-infinite-scroll
        :items="orgReviewsStore.infinteLoaderData"
        :onLoad="orgReviewsStore.loadOnScroll"
        class="d-flex justify-center ga-1 w-100"
      >
        <div class="w-100 ga-4 ga-md-8 review-grid">
          <div v-for="el in orgReviewsStore.infinteLoaderData" :key="el.id">
            <FeedbackCard :feedback="el" :isAuthor="isMycourses" />
          </div>
        </div>
        <template #empty></template>
      </v-infinite-scroll>
    </v-card-text>
  </v-card>
</template>

<style scoped lang="scss">
.review-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;

  @include xs {
    grid-template-columns: 100%;
    gap: 1rem;
  }
}
</style>
