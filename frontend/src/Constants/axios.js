import axios from "axios";
import { BASE_URL } from "./config";

const accessToken = localStorage.getItem("access_token");
const instance = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
  headers: {
    Authorization: `Bearer ${accessToken}`,
  },
});
export default instance;
