<script setup lang="ts">
import {useUser} from "@/stores/User";
import LoginLayout from "@/layouts/LoginLayout.vue";
import YellowButton from "@/components/common/YellowButton.vue";
import { PLATFORM_NAME } from "@/utils/constants";

const userStore = useUser()


</script>

<template>
  <LoginLayout :is-login="false" >
    <v-row v-if="!userStore.getActivateStatus" align="center" justify="center" class="pa-0 title-block">
      <v-col class="ma-0 first-block d-flex flex-column ga-6" cols="auto">
        <h5 class="heading_h5 text-center align-center justify-center">Регистрация</h5>
        <p class="lg text-center">Мы отправили письмо для подтверждения на ваш email
          <span class="lgb">{{userStore.getTemporaryMail}}</span>
        </p>
        <p class="lg text-center limited-p align-self-center">Перейдите по ссылке в письме для завершения регистрации</p>
      </v-col>
    </v-row>
    <v-row v-if="userStore.getActivateStatus" align="center" justify="center" class="pa-0 title-block">
      <v-col class="ma-0 first-block d-flex flex-column ga-6" cols="auto">
        <h5 class="heading_h5 text-center align-center justify-center">Успешно!</h5>
        <p class="lg text-center">
          Вы успешно зарегистрированы и можете в полной мере ощутить все возможности {{ PLATFORM_NAME }}
        </p>
        <YellowButton custom-class="w-75 mx-auto" title="Перейти на сайт" link="/" />
      </v-col>
    </v-row>
  </LoginLayout>
</template>

<style scoped>
.first-block {
  width: 441px;
}

.limited-p {
  width: 240px;
}
</style>
