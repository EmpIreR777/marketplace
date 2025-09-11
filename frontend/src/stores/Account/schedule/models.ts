
export interface IScheduleStoreModel {
  schedule: IScheduleItem[]
}
export interface IScheduleItem {
  course_id: string;
  name: string;
  date_start: string | null;  // Могут быть строки или null, если даты нет
  date_end: string | null;    // Аналогично для end
}
