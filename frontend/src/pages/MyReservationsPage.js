import React, {useEffect, useState} from "react";
import api from "../api/axios";

export default function MyReservationsPage() {
    const [reservations, setReservations] = useState([]);

    useEffect(() => {
        api.get("reservations/")
            .then((response) => setReservations(response.data))
            .catch((error) => console.error(error));
    }, []);

    return (
        <div className="container">
            <h2>My Reservations</h2>
            <ul>
                {reservations.map((res) => (
                    <li key={res.id}>
                        <strong>Room:</strong> {res.room}<br/>
                        <strong>Date:</strong> {res.date}<br/>
                        <strong>Time:</strong> {res.time}
                    </li>
                ))}
            </ul>
        </div>
    );

}
