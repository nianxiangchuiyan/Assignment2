import React from "react";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import RoomsPage from "./pages/RoomsPage";
import MyReservationsPage from "./pages/MyReservationsPage";
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import AdminPanel from "./pages/AdminPanel";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<LoginPage/>}/>
                <Route path="/rooms" element={<RoomsPage/>}/>
                <Route path="/my-reservations" element={<MyReservationsPage/>}/>
                <Route path="/admin" element={<AdminPanel/>}/>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
