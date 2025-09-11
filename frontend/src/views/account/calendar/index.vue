<script setup>
import {computed, onMounted, ref} from "vue";
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import {useScheduleStore} from "@/stores/Account/schedule/index.ts";

const scheduleStore = useScheduleStore()
const generateDailyEvents = (course) => {
  const events = [];
  if (!course.date_start || !course.date_end) return events; // Пропускаем курсы без дат

  const currentDate = new Date(course.date_start);
  const endDate = new Date(course.date_end);

  while (currentDate <= endDate) {
    events.push({
      title: course.name,
      start: currentDate.toISOString().split("T")[0],
      allDay: true,
    });

    currentDate.setDate(currentDate.getDate() + 1); // Переход к следующему дню
  }

  return events;
};

const events = computed(() =>
  scheduleStore.schedule?.flatMap(generateDailyEvents) || []
);

// Настройки календаря
const calendarOptions = ref({
  plugins: [dayGridPlugin],
  initialView: "dayGridMonth", // Отображение по умолчанию (месяц)
  events: events, // Передаем события
  locale: "ru",
  eventBackgroundColor: "#DDFF3333", // Цвет по умолчанию для событий
  eventBorderColor: "#DDFF3333",
  eventTextColor: "#363940", // Цвет текста
  firstDay: 1,
  headerToolbar: {
    left: "prev,next",  // Добавляем кнопки "предыдущий", "следующий"
    center: "title", // Центрируем заголовок
    right: "dayGridMonth,dayGridWeek,dayGridDay", // Кнопки для разных видов представления
  },
  buttonText: {
    month: 'Месяц',      // Кнопка "Месяц"
    week: 'Неделя',      // Кнопка "Неделя"
    day: 'День',         // Кнопка "День"
  },
});

onMounted(async () => {
  await scheduleStore.getStudentSchedule()
})
</script>
<template>
  <div class="text-h5 font-weight-bold d-block d-md-none mb-2">Календарь</div>
  <FullCalendar :options="calendarOptions" />
</template>


<style lang="scss">
/* Опциональные стили */

.fc {
  max-width: 100%;
  margin: auto;
}
.fc-day-today {
  background-color: transparent !important;
}
.fc .fc-daygrid-event {
  margin-top: 6px;
}
.fc .fc-button-primary {
  background: none !important;
  border: none;
  color: #36394066;
  box-shadow: none !important;
  text-decoration: underline !important;
}
.fc .fc-next-button,
.fc .fc-prev-button {
  text-decoration: none !important;
}
.fc .fc-button-primary:not(:disabled).fc-button-active,
.fc .fc-button-primary:not(:disabled).fc-button-active:active,
.fc .fc-button-primary:hover {
  color: #363940;
}
 .fc .fc-button-primary:not(:disabled):active {
  color: #363940;
}
.fc-icon-chevron-right::before,
.fc-icon-chevron-left::before{
  color: #363940;
}
.fc-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}
.fc-today-button.fc-button.fc-button-primary {
  display: none;
}
.fc .fc-toolbar {
  @include xs() {
    flex-wrap: wrap;
  }
}
.fc-header-toolbar {
  @include xs() {
    flex-wrap: wrap;
  }
  .fc-toolbar-chunk {
    &:nth-child(1) {
      @include xs() {
        order: 2;
      }
    }
    &:nth-child(2) {
      @include xs() {
        order: 1;
        width: 100%;
        margin-bottom: 16px;
      }
    }
    &:nth-child(3) {
      @include xs() {
        order: 3;
      }
    }
  }
}
.fc-toolbar-title {
  @include xs() {
    width: 100%;
    font-size: 18px !important;
    font-weight: 300;
  }
}

</style>
