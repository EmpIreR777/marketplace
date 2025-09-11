<script setup lang="ts">
import { instagramIcon, faceBookIcon, VKIcon, classmateIcon } from '../../assets/icons'
import logo from '@/assets/logo_site_footer.svg'
</script>

<template>
  <v-footer>
    <v-container>
      <v-row justify="space-between" align="center">
        <!-- Логотип -->
        <v-col cols="12" sm="auto" class="d-flex align-center py-0">
          <img alt="logo" :src="logo" class="mr-2 header-logo-img" />
        </v-col>

        <!-- Копирайт -->
        <v-col cols="12" sm="auto" class="text-left text-sm-right white--text lg py-0 mt-8 mt-md-0">
          <div class="text-no-wrap">Эдикс Технологии</div>
          <div class="text-no-wrap">ОГРН: 1254700002347</div>
          <div class="text-no-wrap">ИНН: 4706086286</div>
          2025. <span class="text-no-wrap">Все права защищенны.</span>
        </v-col>

        <!-- Соц. сети -->
        <v-col
          v-if="false"
          cols="12"
          md="auto"
          class="d-flex justify-center ga-9 ga-md-4 py-0 mt-8 mt-md-0"
        >
          <a href="https://www.instagram.com/yourusername" target="_blank">
            <v-img :width="24" aspect-ratio="1/1" cover :src="instagramIcon"></v-img>
          </a>
          <a href="https://www.instagram.com/yourusername" target="_blank">
            <v-img :width="24" aspect-ratio="1/1" cover :src="faceBookIcon"></v-img>
          </a>
          <a href="https://www.instagram.com/yourusername" target="_blank">
            <v-img :width="24" aspect-ratio="1/1" cover :src="VKIcon"></v-img>
          </a>
          <a href="https://www.instagram.com/yourusername" target="_blank">
            <v-img :width="24" aspect-ratio="1/1" cover :src="classmateIcon"></v-img>
          </a>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<style scoped>
footer {
  width: 100%;
  height: 192px;
  background: var(--Base-color-100);
  color: var(--White-color-100);
  flex: 0 0 auto;
  padding: 32px 0;

  @media (max-width: 960px) {
    height: auto;
    padding: 24px 28px;
  }
}
</style>
