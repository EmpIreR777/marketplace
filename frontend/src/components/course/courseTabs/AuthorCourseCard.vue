<script setup lang="ts">
import { stubsLogoBase } from '@/assets/icons'
import type { IAuthor } from '@/api/author/models'
import { stubDocumentsIcon } from '@/assets/icons'

const props = defineProps<{
  author: IAuthor
}>()
</script>

<template>
  <v-card class="pa-0 d-flex flex-wrap ga-6" elevation="0">
    <div class="author-avatar-block">
      <v-avatar size="128">
        <v-img
          :cover="false"
          :src="props.author.photo || props.author.logo || stubDocumentsIcon"
          :alt="props.author.title"
        />
      </v-avatar>
    </div>
    <div class="author-text-block">
      <v-card-title class="pa-0 author-text-block__title">
        {{ `${props.author.title}` }}
      </v-card-title>
      <v-card-subtitle class="pa-0 author-text-block__subtitle">{{
        props.author.author_type
      }}</v-card-subtitle>

      <v-row v-if="false" class="my-3 my-sm-6 mx-0">
        <v-col cols="12" sm="4" class="d-flex align-center justify-start ga-2 px-0 px-sm-3">
          <v-img rounded="circle" :src="stubsLogoBase" class="author-text-block__item-logo" />
          <div class="d-flex flex-column align-start">
            <span class="author-text-block__item-title">Опыт работы:</span>
            <span class="author-text-block__item-subtitle">15 лет</span>
          </div>
        </v-col>
        <v-col cols="12" sm="8" class="d-flex align-center justify-start ga-2 px-0 px-sm-3">
          <v-img rounded="circle" :src="stubsLogoBase" class="author-text-block__item-logo" />
          <div class="d-flex flex-column align-start">
            <span class="author-text-block__item-title">Опыт преподавательской деятельности</span>
            <span class="author-text-block__item-subtitle">5 лет</span>
          </div>
        </v-col>
      </v-row>
      <v-card-text
        class="pa-0 mt-6 author-text-block__item-description"
        v-html="props.author.description ?? props.author.bio"
      >
      </v-card-text>
    </div>
  </v-card>
</template>

<style scoped>
.author-avatar-block {
  width: 128px;

  @media (max-width: 600px) {
    width: 100%;
  }
}

.author-text-block {
  flex: 1;
}

.author-text-block__title {
  font-size: 24px;
  font-style: normal;
  font-weight: 700;
  line-height: 32px;

  @media (max-width: 600px) {
    white-space: wrap;
    font-size: 16px;
    line-height: 24px;
  }
}

.author-text-block__subtitle {
  font-size: 12px;
  font-style: normal;
  font-weight: 300;
  line-height: 16px; /* 133.333% */
}

.author-text-block__item-logo {
  width: 40px;
  height: 40px;
  flex-grow: 0;
}

.author-text-block__item-title {
  font-size: 14px;
  font-style: normal;
  font-weight: 300;
  line-height: 20px;
  color: var(--Base-color-60, rgba(54, 57, 64, 0.6));

  @media (max-width: 600px) {
    font-size: 12px;
    line-height: 16px;
  }
}

.author-text-block__item-subtitle {
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: 24px;

  @media (max-width: 600px) {
    font-size: 14px;
    line-height: 20px;
  }
}

.author-text-block__item-description {
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: 24px;
}
</style>
