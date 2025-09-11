<script setup lang="ts">

defineProps({
  content: String,
})

</script>

<template>
  <div class="content-wrapper" v-html="content"></div>
</template>

<style>
.content-wrapper h1 {
  font-size: 32px;
  font-style: normal;
  font-weight: 700;
  line-height: 48px;
  margin: 24px 0;
}

.content-wrapper h2 {
  font-size: 24px;
  font-style: normal;
  font-weight: 700;
  line-height: 32px;
  margin: 16px 0;
}

.content-wrapper ul {
  padding-left: 16px;
}

.content-wrapper li {
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: 24px;
}

.content-wrapper p {
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: 24px;
  margin: 8px 0;
}


</style>
