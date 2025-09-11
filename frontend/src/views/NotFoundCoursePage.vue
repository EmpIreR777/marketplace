<script setup lang="ts">
import { onMounted } from 'vue';
import SliderCourses from "@/components/sliders/SliderCourses.vue";
import { useHomeStore } from '@/stores/Home';
import { cross1, cross2, zigzag } from '@/assets/notFoundPageBg'
import { deco4, deco5 } from '@/assets/navigation'
import { AppColors } from '@/enums/appColors.ts'

const homeStore = useHomeStore()

onMounted(async () => {
  await homeStore.initHomeStore()
})

</script>

<template>
  <div class="not-found-course">

    <div class="not-found-course__decorate">
      <div class="not-found-course__decorate-wrapper">
        <v-img cover class="cross1-img" :src="cross1" />
        <v-img cover class="cross2-img" :src="cross2" />
        <v-img cover class="zigzag-img" :src="zigzag" />
      </div>
    </div>

    <div class="not-found-course__content">
      <h1 class="title">Кажется, вы зашли не на тот урок!</h1>
      <h3 class="sub-title">Но не переживайте, мы подобрали похожие курсы для Вас:</h3>
      <div class="content__decorate">
        <v-img cover class="deco5-img" :src="deco5" />
        <v-img cover class="deco4-img" :src="deco4" />
      </div>
    </div>
  </div>

  <div class="slider-wrapper">
    <div class="section">
      <SliderCourses :courses="homeStore.courses" />
    </div>
  </div>

  <div class="btn-wrapper">
    <v-btn
      class="custom-btn"
      type="submit"
      height="56"
      rounded="lg"
      :color="AppColors.ACCENT_COLOR_LIME_100"
      to="/courses"
    >
      Больше курсов
    </v-btn>
  </div>
</template>

<style scoped lang="scss">
.not-found-course {
  min-height: fit-content;
  display: flex;
  flex-direction: row;
  align-items: end;
  justify-content: space-between;
  padding-top: 24px;
  margin-bottom: 24px;

  @include md() {
    gap: 32px;
  }

  @include sm() {
      align-items: center;
      gap: 16px;
  }

  @include xs() {
    flex-direction: column;
    padding-top: 0;
  }

  &__decorate {
    width: 33.3333%;
    min-height: fit-content;
    display: flex;
    justify-content: center;
    align-items: end;

    @include sm() {
      width: 40%;
    }

    @include xs() {
      width: 100%;
    }
  }

  &__content {
    position: relative;
    width: 66.6666%;
    min-height: fit-content;
    display: flex;
    flex-direction: column;
    justify-content: end;
    align-items: start;
    gap: 16px;

    @include sm() {
      width: 60%;
    }

    @include xs() {
      width: 100%;
    }
  }

  &__decorate-wrapper {
    position: relative;
    height: 205px;
    width: 320px;

    @include sm() {
      width: 206px;
      height: 154px;
    }
  }
}

.slider-wrapper {
  margin-bottom: 16px;

  @include xs() {
    margin-bottom: 32px;
  }
}

.btn-wrapper {
  display: flex;
  align-items: end;
  justify-content: end;

  @include sm() {
    justify-content: center;
  }
}

.content__decorate {
  position: absolute;
  top: -108px;
  right: -35px;
  width: 287px;
  height: 312px;
  z-index: 9998;

  @include md() {
    top: -78px;
  }

  @include sm() {
    display: none;
  }
}

.cross1-img {
  position: absolute;
  top: 0px;
  left: 0px;
  width: 97px;
  height: 80px;

  @include sm() {
    width: 62px;
    height: 52px;
  }
}

.cross2-img {
  position: absolute;
  top: 13px;
  right: 0px;
  width: 76px;
  height: 106px;

  @include sm() {
    width: 49px;
    height: 69px;
  }
}

.zigzag-img {
  position: absolute;
  bottom: 0px;
  left: 0px;
  width: 264px;
  height: 40px;

  @include sm() {
    width: 171px;
    height: 26px;
  }
}

.title {
  color: $base-80;

  @include typography('h6');

  @include xs() {
    color: $base;
  }
}

.sub-title {
  @include typography('h4');

  @include md() {
    z-index: 9999;
  }

  @include sm() {
    @include typography('h6');
  }

  @include xs() {
    @include typography('lgb');
    color: $base-80;
  }
}

.deco5-img {
  position: absolute;
  top: 0;
  right: 0;
  width: 65px;
  height: 84px;
}

.deco4-img {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 150px;
  height: 82px;

  @include md() {
    left: 34px;
    bottom: -50px;
  }
}

.custom-btn {
  letter-spacing: normal;
  width: 280px;
  text-transform: none;

  @include typography('lgb');

  @include sm() {
    width: 304px;
  }
}

</style>
