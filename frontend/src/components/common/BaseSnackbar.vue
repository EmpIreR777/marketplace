<script lang="ts" setup>
import { useSnackbarStore } from '@/stores/Snackbar'
import { computed } from 'vue'
import BaseButton from './BaseButton.vue'
import { SnackbarTypeEnum } from '@/enums/snackbarEnum'

const snackbarStore = useSnackbarStore()
const snackbar = computed(() => snackbarStore.show)

function handleActionClick() {
  snackbarStore.hideSnackbar()
  snackbarStore.action?.onClick()
}
</script>

<template>
  <v-snackbar
    v-model="snackbar"
    location="top right"
    :timeout="snackbarStore.timeout"
    class="base-snackbar"
    :class="{ negative: snackbarStore.type === SnackbarTypeEnum.NEGATIVE }"
  >
    <span v-if="snackbarStore.title" class="base-snackbar__title">{{ snackbarStore.title }}</span>

    <p v-if="snackbarStore.message" class="base-snackbar__message">{{ snackbarStore.message }}</p>

    <template v-slot:actions>
      <BaseButton
        v-if="snackbarStore.action"
        :label="snackbarStore.action.label"
        @click="handleActionClick"
      />
    </template>
  </v-snackbar>
</template>

<style lang="scss">
.base-snackbar {
  &.negative {
    & .v-snackbar__wrapper {
      border-color: $error;
    }

    & .base-snackbar__title {
      color: $error;
    }
  }

  & .v-snackbar__wrapper {
    color: $base;
    background-color: $white;
    max-width: 404px;
    border-radius: 16px;
    border: 1px solid $base-20;
    box-shadow: none;
  }

  & .v-snackbar__content {
    padding: 16px 16px 16px 24px;
  }

  &__title {
    @include typography('lgb');
    line-height: 16px;
    letter-spacing: 0;
  }

  &__message {
    @include typography('sm');
    color: $base-80;
  }

  & .v-snackbar__actions {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-inline-end: 24px;

    & > .v-btn {
      padding: 8px 16px;
    }
  }
}
</style>
