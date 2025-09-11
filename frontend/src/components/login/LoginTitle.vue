<script setup lang="ts">
import { currentLogIcon, currentRegIcon } from '@/assets/login'
import BaseButton from '../common/BaseButton.vue'
import { useRouter } from 'vue-router'

const props = defineProps<{
  isLogin: boolean
  isForgotPassword?: boolean
}>()

const router = useRouter()
</script>

<template>
  <div class="login-title" v-if="!props.isForgotPassword">
    <div class="login-title__tab">
      <BaseButton
        label="Вход"
        type="flat"
        :class="{ passive: !props.isLogin }"
        @click="router.push('/login')"
      />
      <v-img v-if="props.isLogin" :src="currentLogIcon" class="login-title__login-img"></v-img>
    </div>
    <div class="login-title__tab">
      <BaseButton
        label="Регистрация"
        type="flat"
        :class="{ passive: props.isLogin }"
        @click="router.push('/register')"
      />
      <v-img
        v-if="!props.isLogin"
        :src="currentRegIcon"
        width="220"
        height="29"
        cover
        class="login-title__registration-img"
      ></v-img>
    </div>
  </div>
</template>

<style scoped lang="scss">
.login-title {
  display: flex;
  align-items: center;
  justify-content: space-between;

  &__tab {
    position: relative;
    height: 86px;
    display: flex;
    align-items: center;

    & > .v-btn {
      @include typography('h5');
      letter-spacing: -0.7px;
      color: $base-80;

      &.enter {
        min-width: unset;
        width: 100px;
      }

      &.register {
        min-width: unset;
        width: 242px;
      }

      &.passive {
        color: $base-40;
      }
    }
  }

  &__login-img {
    position: absolute;
    top: 50%;
    left: -25px;
    transform: translateY(-50%);
    width: 127px;
    height: 86px;
    max-width: none;
  }

  &__registration-img {
    position: absolute;
    bottom: -5px;
    right: 0;
  }
}

::v-deep(
  .v-btn--active > .v-btn__overlay,
  .v-btn[aria-haspopup='menu'][aria-expanded='true'] > .v-btn__overlay
) {
  opacity: 0;
}
</style>
