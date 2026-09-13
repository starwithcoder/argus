import { defineStore } from "pinia";

// 示例 store：可在后续接入真实的用户/会话状态
export const useAppStore = defineStore("app", {
  state: () => ({
    backendOk: false,
  }),
  actions: {
    setBackendOk(value) {
      this.backendOk = value;
    },
  },
});
