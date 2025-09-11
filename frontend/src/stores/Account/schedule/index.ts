import { defineStore } from 'pinia'
import type {IScheduleItem, IScheduleStoreModel} from "@/stores/Account/schedule/models.ts";
import {getStudentSchedule} from "@/api/student";

export const useScheduleStore = defineStore('scheduleStore', {
  state: (): IScheduleStoreModel => {
    return {
      schedule: [],
    }
  },
  getters: {
  },
  actions: {
    async getStudentSchedule() {
      const data = await getStudentSchedule()
      this.setStudentSchedule(data)
    },
    setStudentSchedule(data: IScheduleItem[]) {
      this.schedule = data
    }
  },
})
