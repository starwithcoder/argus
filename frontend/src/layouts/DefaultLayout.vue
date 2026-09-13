<template>
  <div class="layout">
    <aside class="sidebar" :class="{ collapsed }">
      <div class="sidebar-head">
        <span class="logo" v-show="!collapsed">AI Agent</span>
        <button
          class="toggle"
          @click="collapsed = !collapsed"
          :title="collapsed ? '展开菜单' : '折叠菜单'"
        >
          {{ collapsed ? "»" : "«" }}
        </button>
      </div>
      <nav class="menu">
        <div class="menu-item" @click="openChat = !openChat">
          <span class="icon">💬</span>
          <span class="label">对话</span>
          <span class="arrow" v-show="!collapsed">{{ openChat ? "▼" : "▶" }}</span>
        </div>
        <ul v-show="openChat || collapsed" class="submenu">
          <li
            :class="{ active: isActive('/chat/a') }"
            @click="go('/chat/a')"
          >
            <span class="icon">A</span><span class="label">a</span>
          </li>
          <li
            :class="{ active: isActive('/chat/b') }"
            @click="go('/chat/b')"
          >
            <span class="icon">B</span><span class="label">b</span>
          </li>
        </ul>
        <div
          class="menu-item"
          :class="{ active: isActive('/settings') }"
          @click="go('/settings')"
        >
          <span class="icon">⚙️</span>
          <span class="label">设置</span>
        </div>
      </nav>
    </aside>
    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const openChat = ref(true);
const collapsed = ref(false);

function isActive(path) {
  return route.path === path;
}
function go(path) {
  router.push(path);
}
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}
.sidebar {
  width: 200px;
  background: #fdf6d8;
  color: #6b5a2b;
  padding: 16px 0;
  flex-shrink: 0;
  transition: width 0.2s ease;
  display: flex;
  flex-direction: column;
}
.sidebar.collapsed {
  width: 64px;
}
.sidebar-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 12px 12px;
  border-bottom: 1px solid #f0e4b0;
}
.sidebar.collapsed .sidebar-head {
  justify-content: center;
  padding: 0 0 12px;
}
.logo {
  font-weight: 600;
  font-size: 16px;
  color: #5b4a1f;
}
.toggle {
  background: transparent;
  border: none;
  color: #8a7327;
  font-size: 18px;
  cursor: pointer;
  padding: 2px 4px;
  line-height: 1;
}
.toggle:hover {
  color: #4a3c12;
}
.menu {
  margin-top: 8px;
}
.menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  cursor: pointer;
  user-select: none;
  color: #6b5a2b;
}
.sidebar.collapsed .menu-item {
  justify-content: center;
  padding: 10px 0;
}
.menu-item:hover {
  background: #f6ecb5;
}
.menu-item.active {
  background: #f1e29a;
  color: #4a3c12;
}
.icon {
  width: 20px;
  text-align: center;
  flex-shrink: 0;
}
.label {
  flex: 1;
}
.sidebar.collapsed .label,
.sidebar.collapsed .arrow {
  display: none;
}
.arrow {
  font-size: 10px;
  color: #a08a3c;
}
.submenu {
  list-style: none;
  margin: 0;
  padding: 0;
  background: #f9efc6;
}
.submenu li {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px 8px 36px;
  cursor: pointer;
  color: #6b5a2b;
}
.sidebar.collapsed .submenu li {
  justify-content: center;
  padding: 8px 0;
}
.submenu li:hover {
  background: #f6ecb5;
}
.submenu li.active {
  background: #f1e29a;
  color: #4a3c12;
  font-weight: 600;
}
.content {
  flex: 1;
  padding: 24px;
  background: #f9fafb;
}
</style>
