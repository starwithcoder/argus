import { createRouter, createWebHistory } from "vue-router";

import DefaultLayout from "@/layouts/DefaultLayout.vue";
import Home from "@/views/Home.vue";
import ChatA from "@/views/chat/ChatA.vue";
import ChatB from "@/views/chat/ChatB.vue";
import Settings from "@/views/Settings.vue";

const routes = [
  {
    path: "/",
    component: DefaultLayout,
    children: [
      { path: "", name: "home", component: Home },
      { path: "chat/a", name: "chat-a", component: ChatA },
      { path: "chat/b", name: "chat-b", component: ChatB },
      { path: "settings", name: "settings", component: Settings },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
