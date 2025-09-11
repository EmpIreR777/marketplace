
<script setup lang="ts">
import { ref } from "vue";

interface IDowmlodedFile {
  file?: File;
  link?: string;
}

const link = ref<string>("");
const addedLinks = ref<string[]>([]);
const addedFiles = ref<File[]>([]);
const fileInput = ref<HTMLInputElement | null>(null);
const fileDocumentList = ref<IDowmlodedFile[]>([]);
const fileDocument = ref<IDowmlodedFile>({});

const handleAddLink = () => {
  if (!fileDocument.value.file) return;
  const trimmedLink = link.value.trim();
  if (trimmedLink.length > 0 && !addedLinks.value.includes(trimmedLink)) {
    fileDocument.value = { ...fileDocument.value, link: trimmedLink };
    fileDocumentList.value.push(fileDocument.value);
    fileDocument.value = {};
  }
  link.value = "";
};

const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files?.length) {
    addedFiles.value.push(target.files[0]);
    fileDocument.value = { ...fileDocument.value, file: target.files[0] };
  }
  target.value = ""; // Сбрасываем input, чтобы можно было загрузить такой же файл
};

const removeFileDocument = (index: number) => {
  fileDocumentList.value.splice(index, 1);
};
</script>
<template>
  <v-sheet>
    <h2 class="lgb">Доп. файлы</h2>

    <v-row  v-if="fileDocumentList.length" class="pa-0 mx-0 mb-0 mt-2">
        <div class="d-flex justify-start align-center ga-2 w-100" v-for="(doc, i) in fileDocumentList" :key="i">
          <div
            v-if="doc.file"
            class="added-file"
          >
            {{ doc.file.name }}
          </div>
          <div
            v-if="doc.link"
            class="add-link ml-2"
          >
            {{ doc.link }}
            <v-btn class="copy-button" size="24" icon="mdi-link" variant="text"/>
          </div>
          <v-btn
            @click="removeFileDocument(i)"
            height="56"
            icon="mdi-close"
            class="add-link-button"
            variant="outlined"
          />
        </div>
    </v-row>

    <v-row class="pa-0 mx-0 mb-0 mt-2 ga-4" justify="start">
      <!-- Кнопка "Загрузить" -->
      <v-col class="pa-0" cols="auto">
        <v-btn
          height="56"
          class="change-photo-button load-file-button"
          variant="outlined"
          @click="triggerFileInput"
        >
          Загрузить
        </v-btn>
        <input
          type="file"
          ref="fileInput"
          style="display: none"
          @change="handleFileUpload"
        />
      </v-col>

      <!-- Поле для ввода ссылки -->
      <v-col class="pa-0 d-flex" cols="auto">
        <v-text-field
          class="input-link-block"
          variant="outlined"
          v-model="link"
          label="Ссылка"
          rounded="lg"
          append-inner-icon="mdi-link"
        ></v-text-field>
        <v-btn
          @click="handleAddLink"
          height="56"
          icon="mdi-link-plus"
          class="ml-2 add-link-button"
          variant="outlined"
        />
      </v-col>
    </v-row>





  </v-sheet>
</template>



<style scoped>
.load-file-button {
  width: 171px;
  border-radius: 12px;
  border: 1px solid var(--Base-color-20);
  color: var(--Base-color-80);
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: 24px; /* 150% */
  text-decoration-line: underline;
  text-decoration-style: solid;
  text-decoration-skip-ink: none;
  text-decoration-thickness: 7.5%; /* 1.2px */
  text-underline-offset: 15%; /* 2.4px */
  text-underline-position: from-font;
}

.add-link-button {
  border-radius: 12px;
  border: 1px solid var(--Base-color-20);
  color: var(--Base-color-80);
}

.input-link-block {
  width: 291px;
  color: var(--Base-color-60);
}

.added-file, .add-link{
  padding: 16px;
  border-radius: 12px;
  border: 1px solid var(--Base-color-20, rgba(54, 57, 64, 0.20));
  text-align: center;
  text-overflow: ellipsis;
  overflow: hidden;
  color: var(--Base-color-60, rgba(54, 57, 64, 0.60));
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: 24px;
}

.added-file{
  width: 171px;

  @media (max-width: 600px) {
    width: 30%;
  }
}

.add-link{
  position: relative;
  width: 291px;
  padding-right: 44px;
  text-align: start;

  @media (max-width: 600px) {
    width: 60%;
  }
}

.copy-button{
  position: absolute;
  right: 10px;
  top: 16px;

}

</style>
