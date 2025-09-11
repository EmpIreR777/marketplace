<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useFormat } from '@/composable/useFormat'
import { logoBaseIcon } from '@/assets/icons'
import RatingBlock from '@/components/common/RatingBlock.vue'
import { useUniversityDetailStore } from '@/stores/UniversityDetail'
import Programs from '@/views/university-detail/programs/index.vue'
import BaseBadge from '@/components/common/BaseBadge.vue'
import { computed, onMounted, onUnmounted } from 'vue'
import { useDisplay } from 'vuetify/lib/composables/display.mjs'
import BaseSelect from '@/components/common/BaseSelect.vue'

const universityDetailStore = useUniversityDetailStore()
const { formatNumber } = useFormat()
const { xs } = useDisplay()
const isMobile = computed(() => xs.value)
const route = useRoute()
const router = useRouter()

onMounted(() => {
  universityDetailStore.loadStore()
})

onUnmounted(universityDetailStore.clearStore)

const tabItems = computed(() => {
  return universityDetailStore.tabs.map((tab) => {
    return {
      title: tab.title,
      value: tab.route.split('/').pop(),
    }
  })
})

const selectedTab = computed({
  get: () => universityDetailStore.activeTab,
  set: (value) => {
    universityDetailStore.activeTab = value
    router.replace({ params: { ...route.params, tab: value } })
  },
})
</script>

<template>
  <div v-if="universityDetailStore.university" class="university-detail">
    <div>
      <!-- Header -->
      <div class="university-detail__header">
        <h3>{{ universityDetailStore.university.short_name }}</h3>
        <v-avatar class="university-detail__avatar">
          <v-img
            :cover="false"
            :src="universityDetailStore.university.logo || logoBaseIcon"
            alt="Avatar"
          >
            <template #error>
              <v-avatar class="university-detail__avatar">
                <v-img :src="logoBaseIcon"></v-img>
              </v-avatar>
            </template>
          </v-img>
        </v-avatar>
      </div>
      <!-- Info -->
      <div class="university-detail__info">
        <div class="university-detail__badge-list">
          <BaseBadge :label="universityDetailStore.university.city?.name" :typo="xs ? 'sm' : 'lg'" />
          <BaseBadge
            v-if="universityDetailStore.university.organization_type"
            :label="universityDetailStore.university.organization_type"
            :typo="xs ? 'sm' : 'lg'"
          />
        </div>
        <!-- <div class="university-detail__review">
          <RatingBlock :rating="4.75" :show-value="true" />
          <span class="university-detail__review-count">{{ formatNumber(38000) }} отзывов</span>
        </div> -->
      </div>
    </div>
    <!-- Tabs -->
    <BaseSelect
      v-if="isMobile"
      v-model="selectedTab"
      :items="tabItems"
      class="university-detail__select"
    />
    <v-tabs
      v-else
      v-model="selectedTab"
      hide-slider
      grow
      mandatory
      class="university-detail__tabs"
      height="72"
    >
      <v-tab
        v-for="tab of tabItems"
        :key="tab.value"
        :value="tab.value"
        :replace="true"
        height="54"
      >
        {{ tab.title }}
      </v-tab>
    </v-tabs>
    <!-- Tabs content -->
    <v-tabs-window v-model="selectedTab">
      <v-tabs-window-item value="programs">
        <Programs />
      </v-tabs-window-item>
      <v-tabs-window-item
        value="about"
        v-html="
          universityDetailStore.university.about || '<p>Информация о вузе пока отсутствует.</p>'
        "
        class="html-reset"
      />
      <v-tabs-window-item value="payment">
        <h2>Стоимость обучения</h2>
      </v-tabs-window-item>
      <v-tabs-window-item value="reviews">
        <h2>Отзывы студентов</h2>
      </v-tabs-window-item>
      <v-tabs-window-item value="faq">
        <h2>Часто задаваемые вопросы</h2>
      </v-tabs-window-item>
    </v-tabs-window>
  </div>
</template>

<style lang="scss">
.university-detail {
  display: flex;
  flex-direction: column;
  gap: 32px;

  @include xs {
    gap: 8px;
  }

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 32px;

    & > h3 {
      @include typography('h3');

      @include xs {
        @include typography('h6');
      }
    }
  }

  &__avatar.v-avatar--density-default {
    width: 72px;
    height: 72px;

    @include xs {
      width: 32px;
      height: 32px;
    }
  }

  &__info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    column-gap: 32px;
    row-gap: 16px;
    margin-top: 16px;
    flex-wrap: wrap;

    @include xs {
      align-items: flex-start;
      flex-direction: column;
    }
  }

  &__badge-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }

  &__review {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    background-color: $base-5;
    border-radius: 12px;

    @include xs {
      width: 100%;
      flex-direction: column;
      gap: 8px;
    }

    &-count {
      @include typography('lg');
      color: $base-80;
    }
  }

  &__select {
    margin-top: 8px;
  }

  &__tabs {
    display: flex;
    gap: 16px;
    gap: 8px;
    grid-template-columns: auto;
    padding: 8px;
    border: 1px solid $base-10;
    border-radius: 12px;

    & .v-slide-group__content {
      gap: 8px;
    }

    & .v-tab {
      @include typography('lg');
      border-radius: 8px !important;
      flex: 1;
      text-transform: none;

      &--selected {
        @include typography('lgb');
        background-color: $lime;
      }
    }
  }
}
</style>
