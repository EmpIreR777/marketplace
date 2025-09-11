<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    label?: string
    variant?: 'lime' | 'grey'
    typo?: 'lg' | 'sm'
  }>(),
  {
    variant: 'lime',
    typo: 'lg',
  },
)
</script>

<template>
  <v-badge class="base-badge" :content="props.label" inline :class="[variant, `typo-${typo}`]" />
</template>

<style lang="scss">
.base-badge {
  & .v-badge__badge {
    border-radius: 16px;
    padding: 4px 16px;
    height: auto;
  }

  &.typo-lg .v-badge__badge {
    @include typography('lg');
  }

  &.typo-sm .v-badge__badge {
    @include typography('sm');
  }

  &.lime .v-badge__badge {
    background: $lime;
    color: $base;
  }

  &.grey .v-badge__badge {
    background: $base-20;
    color: $base-80;
  }
}
</style>
