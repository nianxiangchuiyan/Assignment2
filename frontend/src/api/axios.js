import axios from "axios";

const api = axios.create({
    baseURL: "https://assignment2-2-ays2.onrender.com/api/",
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("access_token");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export default api;
