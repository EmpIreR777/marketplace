<script setup lang="ts">
defineProps({
  isHidden: Boolean,
});
// Can be set via API later
const textContent = {
  bigScreenWidth: {
    title1: "Не знаете",
    title2: "какой курс выбрать?",
    text: 'Мы поможем с выбором! Ответьте на 10 вопросов, чтобы узнать, какая сфера деятельности подойдет именно Вам!',
  },
  smallScreenWidth: {
    title: 'Не знаете  какой курс выбрать?',
    text: 'Ответьте на 10 вопросов, чтобы узнать, какая сфера деятельности подойдет Вам!',
  }
 }
</script>

<template>
  <v-card v-if=!isHidden class="main-slide" :class="{ hide: isHidden }">
    <v-card-title class="big-title">
      {{textContent.bigScreenWidth.title1}}
      <br/>
      {{textContent.bigScreenWidth.title2}}
    </v-card-title>
    <v-card-title class="small-title">{{textContent.smallScreenWidth.title}}</v-card-title>
    <v-card-subtitle class="big-text" opacity="1">{{textContent.bigScreenWidth.text}}</v-card-subtitle>
    <v-card-subtitle class="small-text" opacity="1">{{textContent.smallScreenWidth.text}}</v-card-subtitle>
  </v-card>

</template>

<style lang="scss" scoped>

.main-slide {
  width: 100%;
  position: absolute;
  min-height: 396px;
  border-radius: 24px;
  background: linear-gradient(
    0deg,
    var(--Base-color-100, #363940) 0%,
    var(--Base-color-100, #363940) 100%
  ),
  url("@/assets/home/your_way.png") no-repeat center calc(5px);
  background-size: cover;
  background-blend-mode: color, normal;
  padding: 72px 96px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  color: var(--White-color-100);

  @include sm() {
    padding: 16px 28px;
    justify-content: space-around;
  }

  @include xs() {
    min-height: 160px;
    padding: 16px;
    border-radius: 16px;
    justify-content: space-between;
  }
}

.main-slide.hide{
  transform: translateX(-110%);
  transition: transform .3s ease-in-out;
}

.big-title{
  padding: 16px;
  font-size: 64px;
  font-weight: 700;
  line-height: 72px;

  @include md() {
    font-size: 46px;
    line-height: 56px;
  }

  @include sm() {
    font-size: 42px;
    line-height: 50px; /* 133.333% */
    padding: 0 8px;
  }

  @include xs() {
    display: none;
  }
}

.small-title {
  display: none;

  @include xs() {
    display: block;
    max-width: 256px;
    font-size: 24px;
    line-height: 32px;
    font-weight: 700;
    padding: 0 8px;
    white-space: wrap;
  }
}

.big-text{
  max-width: 592px;
  padding: 8px 16px;
  font-size: 16px;
  font-weight: 300;
  line-height: 24px;
  color: var(--White-color-100);
  white-space: normal;

  @include xs() {
    display: none;
  }
}

.small-text {
  display: none;

  @include xs() {
    display: block;
    max-width: 274px;
    font-size: 12px;
    line-height: 16px;
    padding: 8px;
    background: var(--Base-color-5, rgba(54, 57, 64, 0.05));
    backdrop-filter: blur(4px);
    border-radius: 8px;
    white-space: normal;
    font-weight: 300;
  }
}

</style>
