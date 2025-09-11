<script setup lang="ts">
import { onMounted } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import type { SwiperOptions } from 'swiper/types'
import BaseButton from '@/components/common/BaseButton.vue'
import { useTariffStore } from '@/stores/Account/tariff'
import { Navigation } from 'swiper/modules'
import { TariffDurationEnum } from '@/enums/tariffs'

const tariffStore = useTariffStore()
const tariffsDuration = [
  { id: 1, title: 'Месяц', value: TariffDurationEnum.MONTHLY },
  { id: 2, title: 'Год', value: TariffDurationEnum.YEARLY },
]

onMounted(() => {
  tariffStore.initData()
})

const breakpoints = {
  320: { slidesPerView: 'auto', spaceBetween: 16 },
  600: { slidesPerView: 2, spaceBetween: 16 },
  1280: { slidesPerView: 3, spaceBetween: 32 },
}
</script>

<template>
  <div v-if="!tariffStore.loading" class="tariff">
    <div class="tariff__header">
      <div class="text-h5 font-weight-bold d-block d-md-none mb-2">Тарифы</div>
      <v-select
        class="tariff__duration ml-auto"
        v-model="tariffStore.tariffDuration"
        :items="tariffsDuration"
        item-title="title"
        item-value="value"
        variant="outlined"
        rounded="lg"
        hide-details
        @update:model-value="tariffStore.loadTariffs"
      ></v-select>
    </div>
    <div>
      <swiper
        class="tariff__slider"
        navigation
        :modules="[Navigation]"
        :breakpoints="breakpoints as SwiperOptions['breakpoints']"
      >
        <swiper-slide v-for="tariff of tariffStore.tariffs" :key="tariff.id">
          <div class="tariff__slide-main">
            <h5 class="tariff__slide-title">{{ tariff.name }}</h5>
            <div class="tariff__price">
              <span class="tariff__price-full" :class="{ discount: tariff.discount }">
                {{ tariff.discount ? tariff.price : tariff.total_price }} ₽
              </span>
              <span v-if="tariff.discount" class="tariff__price-discount">
                {{ tariff.total_price }} ₽
              </span>
            </div>
            <div v-if="tariff.features.length" class="tariff__description">
              <span v-for="feature of tariff.features">{{ feature }}</span>
            </div>
          </div>
          <div class="tariff__choice">
            <div class="tariff__choice-title">
              <span class="tariff__choice-title-percent">{{ tariff.percentage }}%</span>
              <span class="tariff__choice-title-text">от продаж</span>
            </div>
            <BaseButton
              v-if="tariff.id === tariffStore.userTariff?.tariff"
              label="Продлить"
              type="outline"
              @click="tariffStore.renewTariff()"
            />
            <BaseButton v-else label="Выбрать" @click="tariffStore.changeTariff(tariff.id)" />
          </div>
        </swiper-slide>
      </swiper>
    </div>
  </div>
</template>

<style lang="scss">
.tariff {
  display: flex;
  flex-direction: column;
  gap: 16px;

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  &__title {
    @include typography('h3');
  }

  &__duration {
    max-width: 176px;
  }

  &__slider {
    @include md {
      margin-right: -100%;
      padding-right: 100%;
    }

    @include xs {
      margin-right: 0;
      padding-right: 0;
    }

    & .swiper-button-prev,
    & .swiper-button-next {
      display: none;

      @include xs {
        display: block;
      }
    }
    & .swiper-button-disabled {
      display: none;
    }

    & .swiper-slide {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 16px 24px;
      background-color: $lime-5;
      border-radius: 24px;
      height: auto;
    }
  }

  &__slide {
    &-main {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    &-title {
      @include typography('h5');
    }
  }

  &__price {
    display: flex;
    flex-direction: column;
    text-align: center;
    text-transform: uppercase;

    &-full {
      @include typography('h5');

      &.discount {
        @include typography('lg');
        text-decoration: line-through;
      }
    }

    &-discount {
      @include typography('h5');
    }
  }

  &__description {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  &__choice {
    &-title {
      display: flex;
      justify-content: center;
      align-items: flex-end;
      text-align: center;
      gap: 6px;
      @include typography('lgb');

      &-percent {
        @include typography('h4');
      }

      &-text {
        margin-bottom: 12px;
      }
    }

    & > button {
      width: 100%;
    }
  }
}
</style>
