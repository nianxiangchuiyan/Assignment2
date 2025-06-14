import React, {useState} from "react";
import api from "../api/axios";

export default function LoginPage() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const login = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post("token/", {
                username,
                password,
            });
            localStorage.setItem("access_token", response.data.access);
            localStorage.setItem("refresh_token", response.data.refresh);
            window.location.href = "/rooms";
        } catch (error) {
            alert("Login failed");
        }
    };

    return (
        <div className="container">
            <h2>Login</h2>
            <form onSubmit={login}>
                <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username"/>
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)}
                       placeholder="Password"/>
                <button type="submit">Login</button>
            </form>
        </div>
    );
}
