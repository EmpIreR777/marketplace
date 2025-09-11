<script setup lang="ts">
import { deco2, deco3, deco4, deco5, deco6 } from '@/assets/navigation'
import { currentRegIcon } from '@/assets/login'
import DefaultHeader from '@/components/common/DefaultHeader.vue'

const props = defineProps<{
  isLogin: boolean
}>()
</script>

<template>
  <div class="login-layout">
    <div v-if="props.isLogin" class="login-layout__decorate d-none d-md-block">
      <v-img width="124" height="58" cover class="login-decorate-img1" :src="deco2" />
      <v-img width="60" height="40" cover class="login-decorate-img2" :src="deco3" />
      <v-img width="145" height="22" cover class="login-decorate-img3" :src="currentRegIcon" />
      <v-img width="150" height="82" cover class="login-decorate-img4" :src="deco4" />
      <v-img width="65" height="84" cover class="login-decorate-img5" :src="deco5" />
    </div>
    <div v-if="!props.isLogin" class="login-layout__decorate d-none d-md-block">
      <v-img width="124" height="58" cover class="login-decorate-img1" :src="deco2" />
      <v-img width="60" height="40" cover class="login-decorate-img2" :src="deco3" />
      <v-img width="145" height="22" cover class="login-decorate-img3" :src="currentRegIcon" />
      <v-img width="150" height="82" cover class="login-decorate-img4" :src="deco4" />
      <v-img width="65" height="84" cover class="login-decorate-img5" :src="deco5" />
      <v-img width="31" height="43" cover class="login-decorate-img6" :src="deco6" />
    </div>
    <DefaultHeader
      :isSimpleMode="true"
      :toggle-drawer="() => {}"
      :toggle-account-drawer="() => {}"
    />
    <div class="login-layout__content">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped lang="scss">
.login-layout {
  position: relative;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;

  &__content {
    max-width: 318px;
    width: 100%;
  }

  &__decorate {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
  }
}

.login-decorate-img1 {
  position: absolute;
  top: 50%;
  left: 11%;
}

.login-decorate-img2 {
  position: absolute;
  bottom: 19%;
  right: 9%;
}

.login-decorate-img3 {
  position: absolute;
  top: 7.5%;
  left: 4%;
}

.login-decorate-img4 {
  position: absolute;
  top: 35%;
  right: 14%;
}

.login-decorate-img5 {
  position: absolute;
  top: 6.5%;
  right: 4%;
}

.login-decorate-img6 {
  position: absolute;
  bottom: 8.6%;
  left: 7%;
}
</style>
