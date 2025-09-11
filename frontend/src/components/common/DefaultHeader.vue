<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUser } from '@/stores/User'
import { logoBaseIcon, loginIcon } from '../../assets/icons'
import logo from '@/assets/logo_site_header.svg'
import { computed, onMounted, ref, watch } from 'vue'
import { useDisplay } from 'vuetify'
import BaseButton from '@/components/common/BaseButton.vue'

const props = defineProps({
  toggleDrawer: {
    type: Function,
    required: true,
  },
  toggleAccountDrawer: {
    type: Function,
    required: true,
  },
  isSimpleMode: {
    type: Boolean,
  },
})

const router = useRouter()
const userStore = useUser()
const logoIcon = ref<string | undefined>(logoBaseIcon)
const userEmail = ref<string | undefined>()
const onMenuClick = () => {
  props.toggleDrawer() // Вызываем переданную функцию
}
const { xs, sm } = useDisplay()

// const onAccountMenuClick = () => {
//   props.toggleAccountDrawer()
// }

onMounted(() => {
  if (userStore.userProfile) {
    userEmail.value = userStore.userProfile?.email
    if (userStore.userProfile?.photo) {
      logoIcon.value = userStore.userProfile.photo as string
    }
  }
})

watch(
  () => userStore.getUserPhoto,
  (newPhoto) => {
    if (typeof newPhoto === 'string') {
      logoIcon.value = newPhoto
    } else if (newPhoto) {
      logoIcon.value = URL.createObjectURL(newPhoto)
    }
  },
)

const appBarHeight = computed(() => (xs.value ? 40 : 64))
const logoWidth = computed(() => (xs.value ? 47 : 79))
const logoHeight = computed(() => (xs.value ? 24 : 40))
const avatarSize = computed(() => (xs.value ? 24 : 32))
</script>

<template>
  <v-app-bar :elevation="0" :height="appBarHeight">
    <v-container>
      <v-row align="center" justify="space-between">
        <!-- Логотип -->
        <v-col cols="auto" class="py-0">
          <div class="default-header__left">
            <BaseButton
              v-if="!isSimpleMode && (xs || sm)"
              type="icon"
              icon="menu"
              @click="onMenuClick"
            />
            <!-- <v-btn class="d-md-none" max-width="24" min-height="24" icon @click="onMenuClick">
              <v-icon>mdi-menu</v-icon>
            </v-btn> -->
            <router-link variant="plain" to="/">
              <v-img alt="logo" :src="logo" :width="logoWidth" :height="logoHeight" />
            </router-link>
          </div>
        </v-col>

        <!-- Меню -->
        <v-col
          v-if="!isSimpleMode"
          cols="auto"
          class="default-header__navigation py-0 d-none d-md-flex"
        >
          <BaseButton label="Курсы" type="flat" text="text-md" dense to="/courses" />
          <BaseButton label="ВУЗы" type="flat" text="text-md" dense to="/universities" />
          <BaseButton label="Отзывы" type="flat" text="text-md" dense to="/reviews" />
          <!--          <BaseButton label="Помощь" type="flat" text="text-md" dense />-->
          <BaseButton label="Контакты" type="flat" text="text-md" dense to="/contacts" />
        </v-col>

        <!-- Кнопка входа -->
        <v-col
          v-if="!isSimpleMode && !userStore.getIsAuthenticated"
          cols="auto"
          class="d-flex align-center py-0"
        >
          <BaseButton label="Вход" type="flat" text="text-sm" icon="login" icon-right to="/login" />
        </v-col>

        <v-col
          v-if="!isSimpleMode && userStore.getIsAuthenticated"
          cols="auto"
          class="d-flex align-center py-0"
        >
          <div class="default-header__user" @click="router.push('/account')">
            <span v-if="userEmail" class="sm d-none d-lg-inline">{{ userEmail }}</span>
            <v-avatar :size="avatarSize">
              <v-img alt="avatar" :src="logoIcon" />
            </v-avatar>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-app-bar>
</template>

<style lang="scss">
.default-header {
  &__left {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  &__user {
    display: flex;
    align-items: center;
    gap: 16px;
    cursor: pointer;
    transition: all 300ms ease;

    &:hover {
      opacity: 0.8;
    }
  }
}
</style>
