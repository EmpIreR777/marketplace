<script setup lang="ts">
import { linkType as linkTypeCont } from '@/enums/contactsEnum'
import { computed } from 'vue'

const props = defineProps<{
  imgSrc?: string
  icon?: string
  title?: string
  text?: string
  linkType?: string
}>()

const isLink = computed(() => {
  if (!props.text || !props.linkType) return false
  return !!props.linkType
})

const cleanedNumber = (phone: string) => phone.replace(/\D/g, '')

const formattedLink = computed(() => {
  if (!props.text) return ''

  if (props.linkType === linkTypeCont.web) {
    return props.text
  } else if (props.linkType === linkTypeCont.email) {
    return `mailto:${props.text}`
  } else if (props.linkType === linkTypeCont.phone) {
    return `tel:+${cleanedNumber(props.text)}`
  } else if (props.linkType === linkTypeCont.address) {
    const encodedAddress = encodeURIComponent(props.text)
    return `https://www.google.com/maps/search/?api=1&query=${encodedAddress}`
  } else if (props.linkType === linkTypeCont.skype) {
    return `skype:${props.text}?chat`
  } else if (props.linkType === linkTypeCont.telegram) {
    return `https://t.me/+${cleanedNumber(props.text)}`
  } else if (props.linkType === linkTypeCont.whatsapp) {
    return `https://wa.me/${cleanedNumber(props.text)}`
  }

  return props.text
})
</script>

<template>
  <div class="item-wrapper">
    <div class="title-wrapper">
      <v-img v-if="props.imgSrc" :src="props.imgSrc" max-width="24" max-height="24" cover />
      <v-icon v-if="props.icon" :icon="props.icon" :size="24" />
      <p class="title">{{ props.title || '' }}</p>
    </div>

    <pre class="text" v-if="!isLink">{{ props.text || '&#8213;' }}</pre>
    <a v-else :href="formattedLink" class="text link" target="_blank" rel="noopener noreferrer">
      {{ props.text }}
    </a>
  </div>
</template>

<style lang="scss" scoped>
.item-wrapper {
  width: 100%;
}
.title-wrapper {
  display: flex;
  flex-direction: row;
  justify-content: start;
  align-items: center;
  width: 100%;
}

.title {
  display: inline-block;
  padding-left: 4px;
  width: calc(100% - 24px);

  @include typography('lgb');
}

.text {
  display: block;
  color: $base-80;
  padding-left: 28px;
  text-decoration: none;
  font-family: 'Geologica', sans-serif;

  @include typography('lg');
}

.link:hover {
  color: var(--Base-color-100);
}
</style>
