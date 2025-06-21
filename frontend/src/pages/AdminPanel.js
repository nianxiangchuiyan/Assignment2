import React, {useEffect, useState} from "react";
import api from "../api/axios"; // 你的axios封装文件

export default function AdminPanel() {
    const [reservations, setReservations] = useState([]);
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);

    const loadData = async () => {
        try {
            setLoading(true);
            const [resvRes, userRes] = await Promise.all([
                api.get("reservations/"),
                api.get("users/")
            ]);
            setReservations(resvRes.data);
            setUsers(userRes.data);
        } catch (err) {
            console.error("❌ Error loading admin data", err);
            alert("Admin load failed");
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteReservation = async (id) => {
        if (!window.confirm("Delete this reservation?")) return;
        try {
            await api.delete(`reservations/${id}/`);
            setReservations(prev => prev.filter(r => r.id !== id));
        } catch (err) {
            console.error("Failed to delete reservation", err);
        }
    };

    const handleDeleteUser = async (id) => {
        if (!window.confirm("Delete this user?")) return;
        try {
            await api.delete(`users/${id}/`);
            setUsers(prev => prev.filter(u => u.id !== id));
        } catch (err) {
            console.error("Failed to delete user", err);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    if (loading) return <p>Loading admin data...</p>;

    return (
        <div>
            <h2>🗂 Reservation Management</h2>
            <table border="1">
                <thead>
                <tr>
                    <th>ID</th>
                    <th>Room</th>
                    <th>User</th>
                    <th>Start</th>
                    <th>End</th>
                    <th>Action</th>
                </tr>
                </thead>
                <tbody>
                {reservations.map(r => (
                    <tr key={r.id}>
                        <td>{r.id}</td>
                        <td>{r.room_name || r.room}</td>
                        <td>{r.username || r.user}</td>
                        <td>{r.start_time}</td>
                        <td>{r.end_time}</td>
                        <td>
                            <button onClick={() => handleDeleteReservation(r.id)}>🗑 Delete</button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>

            <h2>👤 User Management</h2>
            <table border="1">
                <thead>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Action</th>
                </tr>
                </thead>
                <tbody>
                {users.map(u => (
                    <tr key={u.id}>
                        <td>{u.id}</td>
                        <td>{u.username}</td>
                        <td>{u.email}</td>
                        <td>
                            <button onClick={() => handleDeleteUser(u.id)}>🗑 Delete</button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}
