import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_BASE || "/api";

const http = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
});

export default http;

// 健康检查示例
export async function healthCheck() {
  const { data } = await http.get("/health");
  return data;
}
