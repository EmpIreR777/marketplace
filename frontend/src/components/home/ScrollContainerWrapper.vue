<script setup lang="ts">
import YellowButton from "@/components/common/YellowButton.vue";
// import {useScrollDrag} from "@/hooks/useScrollDrag.ts";
import ScrollContainer from "@/components/common/ScrollContainer.vue";

defineProps({
  title: {
    type: String,
    required: true
  },
});

// const { scrollContainer } = useScrollDrag();
</script>

<template>
  <v-container fluid class="wrapper">
    <v-row justify="space-between" align="center" class="ma-0">
      <h3 class="heading_h3">{{title}}</h3>
      <YellowButton title="Смотреть все" to="/courses"/>
    </v-row>
    <ScrollContainer :customClasses="'ga-4 ga-sm-8'">
      <slot></slot>
    </ScrollContainer>
  </v-container>
</template>


<style scoped>
.wrapper {
  padding: 112px;

  @media (max-width: 960px) {
    padding: 40px 28px;
  }
}

</style>
