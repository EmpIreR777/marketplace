<script setup lang="ts">
import { computed, ref, onMounted, reactive, onUnmounted } from 'vue'
import { stubDocumentsIcon } from '@/assets/icons'
import { AppColors } from '@/enums/appColors.ts'
import { useFieldRules } from '@/composable/useFieldRules'
import BaseDialog from '@/components/common/BaseDialog.vue'
import { useCourseStore } from '@/stores/Course'
import type { IEditorCourse } from '@/api/courses/models'
// import { useDateFormat } from '@vueuse/core'
// import { DATE_FORMAT } from '@/enums/dateEnum'
import { MAX_GALLERY_LENGTH, MAX_GALLERY_SIZE } from '@/enums/galleryEnum'
import { IMAGE_ACCEPT } from '@/enums/fileEnum'
import { useRouter } from 'vue-router'
import { useSnackbarStore } from '@/stores/Snackbar'
import { SnackbarTypeEnum } from '@/enums/snackbarEnum'
import type { IOption } from '@/api/models'
import BaseDateInput from '@/components/common/BaseDateInput.vue'
import { useMetrika } from '@/composable/useMetrika'
import { AxiosError } from 'axios'

const props = defineProps<{ id?: string }>()

const fieldRules = useFieldRules()
const courseStore = useCourseStore()
const snackbarStore = useSnackbarStore()

const { courseCreate } = useMetrika()

const router = useRouter()

const optionsValuta: IOption[] = [
  { name: 'РУБ', id: 1 },
  // { name: 'USD', id: 2 },
]

const form = ref<HTMLFormElement | null>(null)
const isFormValid = ref(false)

const isDialog = ref(false)

const formModel = reactive<IEditorCourse>({
  course_images: [],
  date_start: null,
  date_end: null,
  price: null,
  name: '',
  description: '',
  learning_types: [], // категория
  link: '',
  trial_version: false,
  age_category: [], // возрастная категория
  courses_thematics: [], // специализация
  course_formats: [], // формат обучения
  tag: null,
  return_conditions: '',
  is_active: false,
})

const fileInput = ref<HTMLInputElement | null>(null)
const fileMsg = ref<string | null>(null)

const fileUrls = computed(
  () =>
    formModel.course_images?.map((el) => {
      if (el instanceof File) {
        return URL.createObjectURL(el)
      } else {
        return el as string
      }
    }) ?? [],
)

const localFiles = computed(
  () => formModel.course_images?.filter((el) => el instanceof File) as File[],
)

const getMainImg = computed(() => fileUrls.value[0] ?? stubDocumentsIcon)
const getRestImages = computed(() => fileUrls.value.slice(1))
//
// const menuStart = ref<boolean>(false)
// const menuEnd = ref<boolean>(false)
//
// const formattedStartDate = computed(() =>
//   formModel.date_start ? useDateFormat(formModel.date_start, DATE_FORMAT).value : '',
// )
// const formattedEndDate = computed(() =>
//   formModel.date_end ? useDateFormat(formModel.date_end, DATE_FORMAT).value : '',
// )
const isLoading = ref(false)

const selectedValuta = ref<IOption | null>(optionsValuta[0])

const isTagAdding = ref<boolean>(false)
const tempTag = ref<string | null>(null)
const tagsList = ref<string[]>([])

const addTag = () => {
  if (!tempTag.value) return
  tagsList.value.push(tempTag.value)
  formModel.tag = tagsList.value.join(',')
  tempTag.value = null
  isTagAdding.value = false
}

const removeTag = (id: number) => {
  tagsList.value.splice(id, 1)
  formModel.tag = tagsList.value.join(',')
}

const clearAditing = (val: boolean) => {
  if (!val && !tempTag.value) {
    isTagAdding.value = false
  }
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

const getTotalFilesSize = (files: File[]) => files.reduce((sum, file) => sum + file.size, 0)

const showFileMsg = (message: string, timeout = 3000) => {
  fileMsg.value = message
  setTimeout(() => {
    fileMsg.value = null
  }, timeout)
}

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (!target.files || target.files.length === 0) return

  const newFiles = Array.from(target.files)
  let remainingSlots = MAX_GALLERY_LENGTH - (formModel.course_images?.length ?? 0)
  let totalSize = getTotalFilesSize(localFiles.value)

  const allowedFiles: File[] = []
  for (const file of newFiles) {
    if (remainingSlots === 0) {
      showFileMsg(`Превышено максимальное количество файлов (${MAX_GALLERY_LENGTH})`)
      break
    }
    if (totalSize + file.size > MAX_GALLERY_SIZE) {
      showFileMsg(`Общий размер файлов не должен превышать ${MAX_GALLERY_SIZE / (1024 * 1024)}MB`)
      break
    }
    allowedFiles.push(file)
    totalSize += file.size
    remainingSlots--
  }

  formModel.course_images = [...(formModel.course_images ?? []), ...allowedFiles]
}

const removeGalleryItem = (ndx: number) => {
  formModel.course_images?.splice(ndx, 1)
}

const resetForm = () => {
  form.value?.reset()
  fileMsg.value = null
}

const validateForm = async () => {
  const { valid } = await form.value?.validate()

  try {
    if (valid) {
      isLoading.value = true
      await submitCourse()
    }
  } finally {
    isLoading.value = false
  }
}

const goCoursesPage = () => {
  router.push({ name: 'my-courses' })
}

const showSnackbar = (title: string, message: string, type: SnackbarTypeEnum) => {
  snackbarStore.showSnackbar({
    title,
    message,
    timeout: 7000,
    type,
    action: { label: 'Закрыть', onClick: () => (snackbarStore.show = false) },
  })
}

const submitCourse = async () => {
  const courseData = {
    ...formModel,
    images: formModel.course_images, // чтобы бек корректно принял картинки меняем имя ключа
  }

  delete courseData.course_images // удалеям ключ, чтобы не дублировать файлы в запросе

  const isEditMode = Boolean(props.id)

  try {
    const action = isEditMode
      ? courseStore.updateCourse(props.id as string, courseData)
      : courseStore.createCourse(courseData)

    await action
    if (!isEditMode) {
      courseCreate()
    }
    isDialog.value = true
  } catch (error: unknown) {
    const title =
      error instanceof AxiosError
        ? error.response?.data
        : error instanceof Error
          ? error.message
          : 'Ошибка'
    showSnackbar(title, 'Курс не сохранен', SnackbarTypeEnum.NEGATIVE)
  }
}

const initCourse = async () => {
  if (props.id) {
    await courseStore.loadCourseById(props.id)
    if (courseStore.course) {
      Object.assign(formModel, courseStore.course)
      formModel.date_start = formModel.date_start ? new Date(formModel.date_start) : null
      formModel.date_end = formModel.date_end ? new Date(formModel.date_end) : null
      formModel.price =
        courseStore.course.price != null ? parseFloat(courseStore.course.price) : null

      tagsList.value = formModel.tag?.split(',') ?? []
    }
  } else {
    courseStore.clearCourse()
  }
}

onMounted(async () => {
  try {
    courseStore.setIsloading(true)
    await courseStore.loadFiltersCatalog()
    await initCourse()
  } finally {
    courseStore.setIsloading(false)
  }
})

onUnmounted(() => {
  resetForm()
  courseStore.clearStore()
})
</script>

<template>
  <v-progress-circular v-if="courseStore.isLoading" indeterminate class="loader" />

  <v-card v-else elevation="0" class="pa-0">
    <v-card-title class="d-flex justify-space-between">
      <h2 class="title">{{ id ? 'Редактировать курс' : 'Новый курс' }}</h2>

      <v-switch
        v-if="id"
        v-model="formModel.is_active"
        label="Курс активен"
        hide-details
        :color="AppColors.ACCENT_COLOR_LIME_100"
      />
    </v-card-title>

    <v-card-text>
      <v-form ref="form" v-model="isFormValid" @submit.prevent="validateForm">
        <v-row class="mt-8">
          <v-col cols="12" md="3" class="pa-2">
            <div class="d-flex flex-column ga-4">
              <v-avatar rounded="lg" class="main-img">
                <v-img :src="getMainImg" cover />
                <v-btn
                  v-if="formModel.course_images?.length"
                  icon="mdi-close"
                  variant="tonal"
                  size="x-small"
                  :color="AppColors.MAIN_TEXT"
                  style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%)"
                  @click="removeGalleryItem(0)"
                />
              </v-avatar>

              <v-btn
                variant="outlined"
                height="56"
                append-icon="mdi-tray-arrow-up"
                text="Загрузить изображение"
                class="change-photo-button btn-wrap-txt"
                @click="triggerFileInput"
              />

              <div v-if="fileMsg" class="text-body-2 text-error">{{ fileMsg }}</div>

              <input
                type="file"
                ref="fileInput"
                :accept="IMAGE_ACCEPT"
                class="d-none"
                multiple
                @change="handleFileChange"
              />
              <p class="change-photo-description">
                До 5 изображений, от 1280x720 пикс. JPG, JPEG, PNG формат, до 15мб
              </p>

              <div class="list-img-block">
                <v-avatar
                  v-for="(url, ndx) in getRestImages"
                  :key="url"
                  rounded="lg"
                  class="list-img"
                >
                  <v-img :src="url" cover />
                  <v-btn
                    icon="mdi-close"
                    variant="tonal"
                    size="x-small"
                    :color="AppColors.MAIN_TEXT"
                    style="
                      position: absolute;
                      top: 50%;
                      left: 50%;
                      transform: translate(-50%, -50%);
                    "
                    @click="removeGalleryItem(ndx + 1)"
                  />
                </v-avatar>
              </div>
            </div>
          </v-col>
          <v-col cols="12" md="9" class="pa-2">
            <v-row class="ga-8">
              <v-col cols="auto" class="date-input">
                <h4 class="input-name">Старт курса</h4>
                <BaseDateInput
                  v-model="formModel.date_start"
                  icon
                  :style="`color: ${AppColors.MAIN_TEXT}`"
                />
                <!--                <v-menu-->
                <!--                  v-model="menuStart"-->
                <!--                  transition="scale-transition"-->
                <!--                  offset-y-->
                <!--                  :close-on-content-click="false"-->
                <!--                >-->
                <!--                  <template v-slot:activator="{ props }">-->
                <!--                    <v-text-field-->
                <!--                      :model-value="formattedStartDate"-->
                <!--                      variant="outlined"-->
                <!--                      class="text-input"-->
                <!--                      v-bind="props"-->
                <!--                      readonly-->
                <!--                      rounded="lg"-->
                <!--                      append-inner-icon="mdi-calendar-range"-->
                <!--                    ></v-text-field>-->
                <!--                  </template>-->
                <!--                  <v-date-picker-->
                <!--                    v-model="formModel.date_start"-->
                <!--                    @update:modelValue="-->
                <!--                      (val) => {-->
                <!--                        formModel.date_start = val-->
                <!--                        menuStart = false-->
                <!--                      }-->
                <!--                    "-->
                <!--                  ></v-date-picker>-->
                <!--                </v-menu>-->
              </v-col>
              <v-col cols="auto" class="date-input">
                <h4 class="input-name">Окончание курса</h4>
                <BaseDateInput
                  v-model="formModel.date_end"
                  icon
                  :style="`color: ${AppColors.MAIN_TEXT}`"
                />
                <!--                <v-menu-->
                <!--                  v-model="menuEnd"-->
                <!--                  transition="scale-transition"-->
                <!--                  offset-y-->
                <!--                  :close-on-content-click="false"-->
                <!--                >-->
                <!--                  <template v-slot:activator="{ props }">-->
                <!--                    <v-text-field-->
                <!--                      rounded="lg"-->
                <!--                      :model-value="formattedEndDate"-->
                <!--                      variant="outlined"-->
                <!--                      class="text-input"-->
                <!--                      v-bind="props"-->
                <!--                      readonly-->
                <!--                      append-inner-icon="mdi-calendar-range"-->
                <!--                    ></v-text-field>-->
                <!--                  </template>-->
                <!--                  <v-date-picker-->
                <!--                    v-model="formModel.date_end"-->
                <!--                    @update:modelValue="-->
                <!--                      (val) => {-->
                <!--                        formModel.date_end = val-->
                <!--                        menuEnd = false-->
                <!--                      }-->
                <!--                    "-->
                <!--                  ></v-date-picker>-->
                <!--                </v-menu>-->
              </v-col>
              <!-- <v-col cols="auto" class="a-0">
                <h4 class="input-name">Время проведения занятий</h4>
                <div class="d-flex align-center ga-1">
                  <v-menu
                    v-model="menuTimeStart"
                    transition="scale-transition"
                    offset-y
                    :close-on-content-click="false"
                  >
                    <template v-slot:activator="{ props }">
                      <v-text-field
                        v-model="startTime"
                        :min-width="100"
                        variant="outlined"
                        class="text-input"
                        v-bind="props"
                        readonly
                        rounded="lg"
                        append-inner-icon="mdi-calendar-range"
                      />
                    </template>
                    <v-time-picker
                      v-model="startTime"
                      @update:modelValue="
                        (val) => {
                          menuTimeStart = false
                        }
                      "
                    />
                  </v-menu>
                  <span>-</span>
                  <v-menu
                    v-model="menuTimeEnd"
                    transition="scale-transition"
                    offset-y
                    :close-on-content-click="false"
                  >
                    <template v-slot:activator="{ props }">
                      <v-text-field
                        v-model="endTime"
                        :min-width="100"
                        variant="outlined"
                        class="text-input"
                        v-bind="props"
                        readonly
                        rounded="lg"
                        append-inner-icon="mdi-calendar-range"
                      />
                    </template>
                    <v-time-picker
                      v-model="endTime"
                      @update:modelValue="
                        (val) => {
                          menuTimeEnd = false
                        }
                      "
                    />
                  </v-menu>
                </div>
              </v-col> -->
              <v-col cols="auto" class="pa-0 price-input">
                <h4 class="input-name">Цена</h4>
                <div class="d-flex align-center ga-2 mt-2">
                  <v-number-input
                    v-model="formModel.price"
                    :min="0"
                    variant="outlined"
                    controlVariant="hidden"
                    inset
                    rounded="lg"
                    class="price-value"
                  />
                  <v-select
                    class="valuta-value"
                    v-model="selectedValuta"
                    :items="optionsValuta"
                    return-object
                    item-title="name"
                    item-value="id"
                    variant="outlined"
                    rounded="lg"
                  ></v-select>
                </div>
              </v-col>
            </v-row>
            <v-row class="pa-0 ma-0 mt-2">
              <v-text-field
                v-model="formModel.name"
                :rules="[fieldRules.required]"
                label="Название курса"
                variant="outlined"
                class="input-item required"
                rounded="lg"
              ></v-text-field>
            </v-row>
            <v-row class="pa-0 ma-0 mt-2">
              <v-textarea
                v-model="formModel.description"
                variant="outlined"
                label="Описание"
                rows="3"
                rounded="lg"
                class="input-item"
              />
            </v-row>
            <v-row class="pa-0 ma-0 mt-2 ga-8">
              <v-col cols="12" md="5" class="pa-0">
                <v-autocomplete
                  class="category-value w-100"
                  v-model="formModel.learning_types"
                  :items="courseStore?.filtersCatalog?.learning_types ?? []"
                  label="Категория"
                  item-title="translations"
                  item-value="id"
                  variant="outlined"
                  rounded="lg"
                  multiple
                  chips
                >
                  <template #item="{ item, props }">
                    <v-list-item v-bind="props" :title="item.raw.translations" />
                  </template>
                </v-autocomplete>
              </v-col>
              <v-col cols="12" md="5" class="pa-0">
                <v-text-field
                  v-model="formModel.link"
                  :rules="[fieldRules.isUrl]"
                  label="Ссылка на курс"
                  variant="outlined"
                  class="link-value"
                  rounded="lg"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row v-if="false" class="pa-0 mr-0 mt-2">
              <v-checkbox v-model="formModel.trial_version" label="Пробная версия" />
            </v-row>
            <v-row class="pa-0 ma-0 mt-2 flex-column ga-2">
              <h3 class="tag-title">Теги</h3>
              <div class="d-flex flex-wrap gc-4 align-start">
                <div class="pt-6 position-relative age-category-wrap">
                  <span class="mandatory-value">обязательно*</span>
                  <v-autocomplete
                    class="age-category"
                    v-model="formModel.age_category"
                    :items="courseStore?.filtersCatalog?.age_category ?? []"
                    :rules="[fieldRules.required]"
                    placeholder="Возрастная категория"
                    item-title="translations"
                    item-value="id"
                    variant="outlined"
                    rounded="lg"
                    multiple
                    chips
                  >
                    <template #item="{ item, props }">
                      <v-list-item v-bind="props" :title="item.raw.translations" />
                    </template>
                  </v-autocomplete>
                </div>
                <div class="pt-6 position-relative specialization-wrap">
                  <span class="mandatory-value">обязательно*</span>
                  <v-autocomplete
                    class="specialization"
                    v-model="formModel.courses_thematics"
                    :items="courseStore?.filtersCatalog?.courses_thematics ?? []"
                    :rules="[fieldRules.required]"
                    placeholder="Специализация"
                    item-title="translations"
                    item-value="id"
                    variant="outlined"
                    rounded="lg"
                    multiple
                    chips
                  >
                    <template #item="{ item, props }">
                      <v-list-item v-bind="props" :title="item.raw.translations" />
                    </template>
                  </v-autocomplete>
                </div>
                <div class="pt-6 position-relative training-format-wrap">
                  <span class="mandatory-value">обязательно*</span>
                  <v-autocomplete
                    class="training-format"
                    v-model="formModel.course_formats"
                    :items="courseStore?.filtersCatalog?.course_formats ?? []"
                    :rules="[fieldRules.required]"
                    placeholder="Формат обучения"
                    item-title="translations"
                    item-value="id"
                    variant="outlined"
                    rounded="lg"
                    multiple
                    chips
                  >
                    <template #item="{ item, props }">
                      <v-list-item v-bind="props" :title="item.raw.translations" />
                    </template>
                  </v-autocomplete>
                </div>

                <v-btn
                  v-for="(tag, ndx) in tagsList"
                  :key="tag"
                  height="56"
                  class="tag-button mt-6 px-4"
                  variant="outlined"
                  append-icon="mdi-close"
                  :text="tag"
                  @click="removeTag(ndx)"
                />
                <div class="mt-6">
                  <v-btn
                    v-if="!isTagAdding"
                    height="56"
                    class="tag-button"
                    variant="outlined"
                    append-icon="mdi-plus"
                    text="Тег"
                    @click="isTagAdding = !isTagAdding"
                  />
                  <div v-else class="tag-button pa-2">
                    <v-combobox
                      v-model="tempTag"
                      :items="[]"
                      :width="160"
                      :color="AppColors.BORDER"
                      autofocus
                      hide-details
                      density="compact"
                      variant="outlined"
                      append-inner-icon="mdi-magnify"
                      menu-icon=""
                      @update:focused="clearAditing"
                      @keyup.enter="addTag"
                    >
                      <template #item="{ props, item }">
                        <v-list-item v-bind="props" :title="item?.raw" @click="addTag" />
                      </template>
                    </v-combobox>
                  </div>
                </div>
              </div>
            </v-row>
            <v-row class="pa-0 ma-0 mt-2">
              <v-textarea
                v-model="formModel.return_conditions"
                variant="outlined"
                label="Условия возврата"
                rows="3"
                rounded="lg"
                class="input-item"
              ></v-textarea>
            </v-row>
          </v-col>
        </v-row>

        <div class="mt-2 mt-sm-6 d-flex ga-4 justify-space-between align-end">
          <v-btn class="action-button" variant="outlined" @click="resetForm">Отменить </v-btn>

          <div class="d-flex flex-column flex-sm-row ga-8">
            <v-btn v-if="false" class="action-button" variant="outlined"> Предпросмотр </v-btn>
            <v-btn
              class="pa-4 submit-button"
              rounded="lg"
              elevation="0"
              :base-color="AppColors.BASE_COLOR_100"
              :color="AppColors.ACCENT_COLOR_LIME_100"
              :disabled="!isFormValid || isLoading"
              @click="validateForm"
            >
              Подтвердить
            </v-btn>
          </div>
        </div>
      </v-form>
    </v-card-text>

    <BaseDialog
      v-model="isDialog"
      title="Предупреджение"
      text="Ваш курс будет опубликован после прохождения модерации"
      confirmText="Хорошо"
      cancelText=""
      persistent
      @confirm="goCoursesPage"
    />
  </v-card>
</template>

<style scoped lang="scss">
.loader {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50% -50%);
}
.title {
  font-size: 24px;
  font-style: normal;
  font-weight: 700;
  line-height: 32px;
}

.main-img {
  width: 100%;
  height: 181px;
}

.list-img-block {
  display: flex;
  justify-content: start;
  flex-wrap: wrap;
  gap: 8px;
}

.list-img {
  flex-grow: 0;
  width: 88px;
  height: 57px;
}

.change-photo-button {
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: 24px;
  text-transform: none;
  border-radius: 12px;
  border: 1px solid var(--Base-color-20, rgba(54, 57, 64, 0.2));
}

.change-photo-description {
  font-size: 12px;
  font-style: normal;
  font-weight: 300;
  line-height: 16px;
  color: var(--Base-color-80, #363940);
}

.input-name {
  font-size: 16px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px;
}

.date-input {
  width: 160px !important;
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-content: center;
}

.price-value {
  width: 160px;
}

.valuta-value {
  width: 100px;
}

.category-value {
  width: 280px;
}

.link-value {
  width: 100%;
  border-radius: 12px;
}

.tag-title {
  font-size: 16px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px; /* 150% */
}

.mandatory-value {
  position: absolute;
  left: 0;
  top: 0;
  color: var(--Base-color-60, rgba(54, 57, 64, 0.6));
}

.age-category {
  width: 237px;
  @include sm() {
    width: 100%;
  }
}
.age-category-wrap {
  @include sm() {
    width: 100%;
  }
}
.specialization-wrap {
  @include sm() {
    width: 100%;
  }
}
.specialization {
  width: 190px;
  @include sm() {
    width: 100%;
  }
}
.training-format-wrap {
  @include sm() {
    width: 100%;
  }
}
.training-format {
  width: 203px;
  @include sm() {
    width: 100%;
  }
}

.action-button {
  width: 152px;
  border-radius: 12px;
  border: 1px solid var(--Accent-color-Lime-100, #df3);
  font-size: 16px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px;
  text-transform: none;
  height: 56px;

  @media (max-width: 600px) {
    width: auto;
    font-size: 12px;
    line-height: 16px;
    height: 40px;
    padding: 8px !important;
  }
}

.submit-button {
  width: 152px;
  text-transform: none;
  font-size: 16px;
  font-style: normal;
  font-weight: 700;
  line-height: 24px; /* 150% */
  height: 56px;

  @media (max-width: 600px) {
    width: auto;
    font-size: 12px;
    line-height: 16px;
    height: 40px;
    padding: 8px !important;
  }
}

.tag-button {
  border-radius: 12px;
  border: 1px solid var(--Base-color-20, rgba(54, 57, 64, 0.2));
}
</style>
