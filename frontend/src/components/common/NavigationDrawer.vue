<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { deco1, deco2, deco3 } from '../../assets/navigation'
import { useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/Account'
import type { AccountTypeEnum } from '@/enums/userEnum'
import BaseDialog from '@/components/common/BaseDialog.vue'
import { useUser } from '@/stores/User'

// Пропсы
const props = defineProps({
  drawer: { type: Boolean, required: true },
})

const route = useRoute()
const router = useRouter()
const isAccountPage = computed(() => route.path.includes('/account'))
const accountStore = useAccountStore()

interface MenuItem {
  title: string
  value: string
  nested: MenuItem[]
  roleAccess?: AccountTypeEnum[]
}

// Данные меню
const baseItems = ref<MenuItem[]>([
  // {
  //   title: 'Курсы',
  //   value: '',
  //   nested: [
  //     { title: 'Онлайн школы', value: '/online-schools', nested: [] },
  //     { title: 'Оффлайн школы', value: '/offline-schools', nested: [] },
  //     { title: 'ВУЗы', value: '/universities', nested: [] },
  //     { title: 'Курсы', value: '/courses', nested: [] },
  //     { title: 'Тренинги', value: '/trainings', nested: [] },
  //     { title: 'Языковые курсы', value: '/language-courses', nested: [] },
  //     { title: 'Мастер-классы', value: '/master-classes', nested: [] },
  //   ],
  // },
  { title: 'Курсы', value: '/courses', nested: [] },
  { title: 'Отзывы', value: '/reviews', nested: [] },
  { title: 'ВУЗы', value: '/universities', nested: [] },
  // { title: 'Помощь', value: '/help', nested: [] },
  { title: 'Контакты', value: '/contacts', nested: [] },
])

const accountMenuItems = ref<MenuItem[]>(
  accountStore.getMenuItems.map((item) => ({
    title: item.title,
    value: '/account/' + item.value,
    nested: [],
    roleAccess: item.roleAccess,
  })),
)

const menuItems = computed(() => (isAccountPage.value ? accountMenuItems.value : baseItems.value))

// Эмиттер для передачи событий родителю
const emit = defineEmits(['update:drawer'])

// Двустороннее связывание состояния
const localDrawer = computed({
  get: () => props.drawer,
  set: (value) => emit('update:drawer', value),
})

// Ширина экрана
const screenWidth = ref(window.innerWidth)
const logoutDialog = ref(false)
const userStore = useUser()
// Слушатель изменений размера окна
const updateScreenWidth = () => {
  screenWidth.value = window.innerWidth
}
const onClickItem = (link: string) => {
  // console.log('link', link)
  if (link === '/account/logout') {
    logoutDialog.value = true
    return
  }
  router.push(link)
}
onMounted(() => {
  window.addEventListener('resize', updateScreenWidth)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateScreenWidth)
})
</script>

<template>
  <BaseDialog
    v-model="logoutDialog"
    title="Подтверждение"
    text="Вы действительно хотите выйти из учетной записи?"
    confirmText="Да"
    cancelText="Нет"
    @confirm="userStore.logoutUser()"
  />
  <v-navigation-drawer
    v-model="localDrawer"
    :location="$vuetify.display.mobile ? 'left' : undefined"
    temporary
    app
    :width="screenWidth"
    touchless
    class="custom-drawer py-12 px-4"
  >
    <div class="drawer-header">
      <v-btn size="32" variant="text" @click="localDrawer = false">
        <v-icon size="24">mdi-close</v-icon>
      </v-btn>
    </div>
    <v-img cover :src="deco1" class="menu-deco1"></v-img>

    <v-img cover :src="deco2" class="menu-deco2"></v-img>

    <v-img cover :src="deco3" class="menu-deco3"></v-img>

    <div class="d-flex flex-column align-start justify-center h-100">
      <v-list class="w-100">
        <template v-for="(item, index) in menuItems" :key="index">
          <!-- Если есть вложенные элементы -->
          <v-list-group v-if="item.nested.length" :value="item.value">
            <template v-slot:activator="{ props }">
              <v-list-item
                v-bind="props"
                :title="item.title"
                class="menu-item py-5 pl-8"
              ></v-list-item>
            </template>

            <!-- Отображаем вложенные элементы -->
            <v-list-item
              v-for="(nestedItem, nestedIndex) in item.nested"
              :key="nestedIndex"
              :value="nestedItem.value"
              :title="nestedItem.title"
              class="menu-nested-item"
              @click="router.push(nestedItem.value)"
            ></v-list-item>
          </v-list-group>

          <!-- Если нет вложенных элементов -->
          <v-list-item
            v-else
            :title="item.title"
            :value="item.value"
            class="menu-item py-5 pl-8"
            @click="onClickItem(item.value)"
          ></v-list-item>
        </template>
      </v-list>
    </div>
    <!--    <v-list :items="items"></v-list>-->
  </v-navigation-drawer>
</template>

<style>
.custom-drawer {
  height: 100vh;
}
.custom-drawer .v-list {
  overflow: auto;
}

.drawer-header {
  position: absolute;
  width: 100%;
  height: 40px;
  top: 0;
  left: 0;
  padding: 8px 12px;
}

.menu-deco1 {
  position: absolute;
  top: 80px;
  left: 17px;
  width: 67px;
  height: 85px;
}

.menu-deco2 {
  position: absolute;
  top: 408px;
  right: 16px;
  width: 124px;
  height: 58px;
}

.menu-deco3 {
  position: absolute;
  bottom: 88px;
  left: 48px;
  width: 62px;
  height: 42px;
}

.menu-item .v-list-item-title {
  font-size: 32px;
  font-style: normal;
  font-weight: 700;
  line-height: 48px; /* 150% */
}

.menu-nested-item {
  height: 20px !important;
  min-height: 20px !important;
  padding-left: 0 !important;
}

.menu-nested-item .v-list-item-title {
  font-size: 14px !important;
  font-style: normal;
  font-weight: 700;
  line-height: 20px; /* 142.857% */
}
</style>
