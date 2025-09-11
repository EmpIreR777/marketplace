<script setup lang="ts">
import BaseIcon from '@/components/common/BaseIcon.vue'

const props = withDefaults(
  defineProps<{
    label?: string
    type?: 'filled' | 'outline' | 'flat' | 'icon'
    icon?: string
    text?: 'text-h6' | 'text-lg' | 'text-lgb' | 'text-md' | 'text-mdb' | 'text-sm' | 'text-smb'
    iconRight?: boolean
    dense?: boolean
    rotateIcon?: boolean
    size?: string
    disabled?: boolean
  }>(),
  {
    type: 'filled',
    text: 'text-lgb',
  },
)
</script>

<template>
  <v-btn
    class="base-button"
    :class="[props.type, props.text, { 'icon-right': props.iconRight, dense: props.dense }]"
    density="default"
    :disabled="props.disabled"
  >
    <BaseIcon v-if="props.icon" :name="props.icon" :class="{ rotate: props.rotateIcon }" />
    {{ props.label }}
  </v-btn>
</template>

<style lang="scss">
.base-button {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  padding: 16px;
  border-radius: 8px;
  text-transform: none;
  box-shadow: none;
  letter-spacing: 0;

  &:hover,
  &:active,
  &:focus,
  &:focus-visible {
    box-shadow: none;
  }

  &.v-btn--density-default {
    height: auto;
  }

  &.dense {
    padding: 8px 16px;
  }

  & .v-btn__content {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  &.icon-right .v-btn__content {
    flex-direction: row-reverse;
  }

  .v-icon {
    line-height: 0;
    transition: $transition;

    &.rotate {
      transform: rotate(180deg);
    }
  }

  &.flat {
    background-color: transparent;
  }
  &.outline {
    background-color: transparent;
    border: 2px solid $lime;
    padding: 14px;

    &.dense {
      border-width: 1px;
      padding: 15px;
    }
  }
  &.filled {
    background-color: $lime;
  }
  &.icon {
    padding: 0;
    width: 30px;
    height: 30px;
    min-height: 30px;
    min-width: 30px;
  }

  &.text-h6 {
    @include typography('h6');
  }
  &.text-lg {
    @include typography('lg');
  }
  &.text-lgb {
    @include typography('lgb');
  }
  &.text-md {
    @include typography('md');
  }
  &.text-mdb {
    @include typography('mdb');
  }
  &.text-sm {
    @include typography('sm');
  }
  &.text-smb {
    @include typography('smb');
  }
}
</style>
