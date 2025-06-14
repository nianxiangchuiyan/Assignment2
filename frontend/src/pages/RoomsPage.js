import React, {useEffect, useState} from "react";
import api from "../api/axios";

export default function RoomsPage() {
    const [rooms, setRooms] = useState([]);

    useEffect(() => {
        api.get("rooms/")
            .then((response) => setRooms(response.data))
            .catch((error) => console.error(error));
    }, []);

    return (
        <div className="container">
            <h2>Available Rooms</h2>
            <ul>
                {rooms.map((room) => (
                    <li key={room.id}>{room.name}</li>
                ))}
            </ul>
        </div>
    );

}
