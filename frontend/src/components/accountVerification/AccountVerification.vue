<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { AppColors } from '@/enums/appColors.ts'
import { ApiLegalForm, EntityType, LegalForm, LegalFormTitle } from '@/enums/legalTypes'
import { ATRIBUTES_FIZ, ATRIBUTES_FOP, ATRIBUTES_LLC } from '@/enums/legalAtributes'
import BaseButton from '@/components/common/BaseButton.vue'
import type { Recordable } from '@/types'
import type { IAuthorVerify } from '@/api/author/models'
import { patchAuthorVerify } from '@/api/author'
import { useUser } from '@/stores/User'
import { IMAGE_ACCEPT, DOCUMENT_ACCEPT } from '@/enums/fileEnum'
import { stubDocumentsIcon } from '@/assets/icons'

const router = useRouter()
const route = useRoute()
const userStore = useUser()

const entityType = computed(() => String(route.params.type))
const legalVariant = ref(LegalForm.FOP)

const getLegalForm = computed(() =>
  entityType.value === EntityType.INDIVIDUAL ? LegalForm.FIZ : legalVariant.value,
)

const isIndividual = computed(() => entityType.value === EntityType.INDIVIDUAL)

const ATTRIBUTES_MAP = {
  [LegalForm.FIZ]: ATRIBUTES_FIZ,
  [LegalForm.FOP]: ATRIBUTES_FOP,
  [LegalForm.LLC]: ATRIBUTES_LLC,
}

const currentFields = computed(() => ATTRIBUTES_MAP[getLegalForm.value] || {})

const requisites = ref<Recordable>({})

const fileSet = ref<Set<File>>(new Set())
const filesPrevMap = ref<Map<File, string>>(new Map())

watch(
  fileSet,
  (newSet, oldSet) => {
    oldSet.forEach((file) => {
      if (!newSet.has(file)) {
        URL.revokeObjectURL(filesPrevMap.value.get(file)!)
        filesPrevMap.value.delete(file)
      }
    })

    newSet.forEach((file) => {
      if (!filesPrevMap.value.has(file)) {
        filesPrevMap.value.set(file, URL.createObjectURL(file))
      }
    })
  },
  { deep: true },
)

const checkboxPersonal = ref(false)
const checkboxTrueData = ref(false)

const form = ref<HTMLFormElement | null>(null)
const isLoading = ref(false)
const isSubmitDisabled = computed(() => !checkboxPersonal.value || !checkboxTrueData.value)

function clearInputs() {
  requisites.value = {}

  fileSet.value.forEach((file) => {
    URL.revokeObjectURL(filesPrevMap.value.get(file)!)
  })

  fileSet.value.clear()
  filesPrevMap.value.clear()
}

function createRequisits() {
  resetForm()
  clearInputs()

  Object.keys(currentFields.value).forEach((key) => {
    requisites.value[key] = null
  })
}

function addFiles(files: File[]) {
  files.forEach((file) => fileSet.value.add(file))
}

function removeDocFile(file: File) {
  fileSet.value.delete(file)
}

async function submitVerification() {
  const id = userStore.getUserId
  if (!id) return

  const payload: IAuthorVerify = {
    author_type: ApiLegalForm[getLegalForm.value],
    verify_fields: requisites.value,
  }

  if (fileSet.value.size) {
    payload.documents = [...fileSet.value].map((file) => file)
  }

  // console.log(payload)

  return await patchAuthorVerify(id, payload)
}

function resetForm() {
  form.value?.reset()
}

async function validateForm() {
  const { valid } = await form.value?.validate()

  try {
    if (valid) {
      isLoading.value = true
      await submitVerification()
      router.push({ name: 'profile' })
    }
  } finally {
    isLoading.value = false
  }
}

watch(getLegalForm, () => {
  createRequisits()
})

onMounted(() => {
  createRequisits()
})

onUnmounted(() => {
  resetForm()
  clearInputs()
})
</script>

<template>
  <v-card elevation="0" class="d-flex flex-column ga-4">
    <v-card-title
      class="d-flex flex-wrap justify-space-between ga-4 pa-0"
      style="white-space: normal"
    >
      <h2 class="title">Верификация учётной записи</h2>

      <v-btn-toggle
        v-if="entityType === EntityType.LEGAL"
        v-model="legalVariant"
        rounded="0"
        group
        class="ml-auto"
      >
        <v-btn :value="LegalForm.FOP"> {{ LegalFormTitle.FOP }} </v-btn>
        <v-btn :value="LegalForm.LLC"> {{ LegalFormTitle.LLC }} </v-btn>
      </v-btn-toggle>
    </v-card-title>

    <v-card-text class="d-flex flex-column ga-4 pa-0">
      <v-form ref="form" class="d-flex flex-column ga-4" @submit.prevent="validateForm">
        <div
          style="
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 0.25rem 1rem;
          "
        >
          <template v-for="(value, key) in currentFields" :key="key">
            <v-text-field
              v-if="value.type !== 'DATE'"
              v-model.trim="requisites[key]"
              required
              :rules="value.validation"
              :label="value.name"
              variant="outlined"
              :base-color="AppColors.DESCR_TEXT"
            />
            <v-date-input
              v-else-if="value.type === 'DATE'"
              v-model="requisites[key]"
              required
              :rules="value.validation"
              :label="value.name"
              variant="outlined"
              :base-color="AppColors.DESCR_TEXT"
              prepend-icon=""
            />
          </template>
        </div>

        <div class="d-flex flex-column ga-2">
          <div v-if="isIndividual" class="text-body-1 font-weight-bold">
            Фото с документами в руках
          </div>

          <div
            class="ga-4"
            style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr))"
          >
            <div
              v-for="file in fileSet"
              :key="file.name"
              class="d-flex align-center ga-2 pa-4 position-relative rounded-lg"
              :style="{ border: `1px solid ${AppColors.BORDER}` }"
            >
              <v-avatar size="64" :color="AppColors.BG">
                <v-img v-if="isIndividual" :src="filesPrevMap.get(file)" />
                <v-icon v-else icon="mdi-file-document-outline" :size="32" />
              </v-avatar>

              <div class="overflow-hidden">{{ file.name }}</div>

              <v-btn
                icon="mdi-close"
                variant="plain"
                density="compact"
                class="position-absolute top-0 right-0 mt-2 mr-2"
                @click="removeDocFile(file)"
              />
            </div>

            <v-file-upload
              :accept="isIndividual ? IMAGE_ACCEPT : DOCUMENT_ACCEPT"
              multiple
              density="compact"
              height="106px"
              :border="`1px solid ${AppColors.BORDER}`"
              rounded="lg"
              @update:model-value="addFiles"
            >
              <template #icon>
                <v-avatar size="72" :color="AppColors.BG">
                  <v-img v-if="isIndividual" :src="stubDocumentsIcon"></v-img>
                  <v-icon v-else icon="mdi-file-document-outline" :size="32" />
                </v-avatar>
              </template>
              <template #title>
                <span class="text-body-1 font-weight-regular text-decoration-underline">
                  Загрузить
                </span>
              </template>
              <template #item> </template>
            </v-file-upload>
          </div>

          <div v-if="isIndividual" class="text-body-2" :style="{ color: AppColors.DESCR_TEXT }">
            Паспорт / Загран. паспорт / Водительское удостворение
          </div>
        </div>

        <!-- <div
          v-if="!isIndividual"
          class="ga-4"
          style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr))"
        >
          <div
            v-for="file in files"
            :key="file.name"
            class="d-flex align-center ga-2 pa-4 position-relative rounded-lg"
            :style="{ border: `1px solid ${AppColors.BORDER}` }"
          >
            <v-avatar size="64" :color="AppColors.BG">
              <v-icon icon="mdi-file-document-outline" :size="32" />
            </v-avatar>
            <div>{{ file.name }}</div>
            <v-btn
              icon="mdi-close"
              variant="plain"
              density="compact"
              class="position-absolute top-0 right-0 mt-2 mr-2"
              @click="removeDocFile(file)"
            />
          </div>

          <v-file-upload
            density="compact"
            height="106px"
            multiple
            :border="`1px solid ${AppColors.BORDER}`"
            rounded="lg"
            @update:model-value="addFiles"
          >
            <template #icon>
              <v-avatar size="72" :color="AppColors.BG">
                <v-icon icon="mdi-file-document-outline" :size="32" />
              </v-avatar>
            </template>
            <template #title
              ><span class="text-body-1 font-weight-regular text-decoration-underline"
                >Загрузить</span
              ></template
            >
            <template #item> </template>
          </v-file-upload>
        </div> -->
      </v-form>

      <div>
        <v-checkbox
          v-model="checkboxPersonal"
          label="Я даю согласие на обработку моих персональных данных"
          density="compact"
          :color="AppColors.MAIN_TEXT"
          :base-color="AppColors.MAIN_TEXT"
        />
        <v-checkbox
          v-model="checkboxTrueData"
          label="Я подтверждаю, что предоставленные мною данные достоверны и соответствуют ..."
          density="compact"
          :color="AppColors.MAIN_TEXT"
          :base-color="AppColors.MAIN_TEXT"
        />
      </div>
    </v-card-text>

    <v-card-actions class="justify-end pa-0">
      <BaseButton label="Подтвердить" :disabled="isSubmitDisabled" @click="validateForm" />
    </v-card-actions>
  </v-card>
</template>

<style scoped>
.title {
  font-size: 32px;
  font-weight: 700;
  line-height: 48px;

  @media (max-width: 600px) {
    font-size: 24px;
    line-height: 32px;
  }
}

::v-deep(.v-label.v-field-label) {
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: 24px;
  width: 100%;
}

::v-deep(.v-field__outline) {
  opacity: unset;
  border-color: var(--Base-color-20, rgba(54, 57, 64, 0.2)) !important;
  border-radius: 12px !important;
}
</style>
