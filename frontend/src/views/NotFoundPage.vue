<script setup lang="ts">
import { cross1, cross2, zigzag } from '@/assets/notFoundPageBg'
import { AppColors } from '@/enums/appColors.ts'

</script>

<template>
  <div class="not-found">

    <div class="not-found__decorate">
      <div class="not-found__decorate-wrapper">
        <v-img cover class="cross1-img" :src="cross1" />
        <v-img cover class="cross2-img" :src="cross2" />
        <v-img cover class="zigzag-img" :src="zigzag" />
      </div>
    </div>

    <div class="not-found__content">
      <h1 class="title">Кажется, вы зашли не на тот урок!</h1>
      <h3 class="sub-title">Но не переживайте, на EdX всегда есть чему научиться</h3>
      <v-btn
        class="custom-btn"
        type="submit"
        height="56"
        width="280"
        rounded="lg"
        :color="AppColors.ACCENT_COLOR_LIME_100"
        to="/courses"
      >
        Научиться
      </v-btn>
    </div>

  </div>
</template>

<style scoped lang="scss">
.not-found {
  min-height: fit-content;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: start;
  gap: 32px;

  @include xs() {
    justify-content: start;
  }

  &__decorate {
    width: 100%;
    min-height: fit-content;
    display: flex;
    justify-content: center;
    align-items: end;
    padding-top: 64px;

    @include xs() {
      padding-top: 120px;
    }
  }

  &__content {
    max-width: 592px;
    width: 100%;
    min-height: fit-content;
    display: flex;
    flex-direction: column;
    justify-content: start;
    align-items: center;
    gap: 16px;

    @include xs() {
      gap: 24px;
    }
  }

  &__decorate-wrapper {
    position: relative;
    height: 333px;
    width: 531px;

    @include xs() {
      height: 228px;
      width: 275px;
    }
  }
}

.cross1-img {
  position: absolute;
  top: 0px;
  left: 0px;
  width: 161px;
  height: 133px;

  @include xs() {
    width: 93px;
    height: 76px;
  }
}

.cross2-img {
  position: absolute;
  top: 22px;
  right: 0px;
  width: 128px;
  height: 178px;

  @include xs() {
    width: 73px;
    height: 102px;
  }
}

.zigzag-img {
  position: absolute;
  bottom: 0px;
  left: 0px;
  width: 440px;
  height: 68px;

  @include xs() {
    width: 253px;
    height: 39px;
  }
}

.title {
  text-align: center;

  @include typography('h6');

  @include xs() {
    text-align: left;
  }
}

.sub-title {
  text-align: center;
  color: $base-80;

  @include typography('h6');

  @include xs() {
    text-align: left;

    @include typography('lgb')
  }
}
.custom-btn {
  letter-spacing: normal;

  @include typography('lgb');
}

</style>
