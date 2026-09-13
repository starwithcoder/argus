<template>
  <section>
    <h2>项目骨架已就绪</h2>
    <p>后端健康检查状态：{{ status }}</p>
    <button @click="check">检查后端</button>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { healthCheck } from "@/api";

const status = ref("未知");

async function check() {
  try {
    const data = await healthCheck();
    status.value = data.status;
  } catch (e) {
    status.value = "连接失败：" + e.message;
  }
}

onMounted(check);
</script>
