// src/pages/RoomsPage.js
import React, {useEffect, useState} from 'react';
import axios from '../api/axios'; // 统一 axios 实例
import dayjs from 'dayjs';
import classNames from 'classnames';
import './RoomsPage.css'; // 可选：放自定义样式

const START_TIME = 8;      // 08:00
const SLOT_COUNT = 20;     // 20 × 30min 直到 18:00
const SLOT_MIN = 30;       // 分钟间隔

export default function RoomsPage() {
  const [rooms, setRooms] = useState([]);
  const [reservations, setReservations] = useState([]);  // 全日预约
  const [selectedDate, setSelectedDate] = useState(dayjs().startOf('day'));
  const [loading, setLoading] = useState(true);

  // 获取房间列表 + 当日预约
  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const [roomRes, resvRes] = await Promise.all([
          axios.get('rooms/'),
          axios.get(`reservations/?date=${selectedDate.format('YYYY-MM-DD')}`)
        ]);
        console.log('📥 Loaded reservations:', resvRes.data);
        setRooms(roomRes.data);
        setReservations(resvRes.data);
      } catch (err) {
        console.error(err, err.response?.data);
        alert('Failed to load rooms.');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [selectedDate]);

  // 生成 30 分钟时间片数组，例如 ["08:00", "08:30", ...]
  const timeSlots = Array.from({length: SLOT_COUNT}, (_, i) => {
    return dayjs().hour(START_TIME).minute(0).add(i * SLOT_MIN, 'minute').format('HH:mm');
  });


  const toHHMM = (isoStr) => dayjs(isoStr).format('HH:mm');

// 判断房间某时段是否已被预订
  const isBooked = (roomId, slot) =>
      reservations.some((r) => {
        if (r.room !== roomId) return false;
        const start = toHHMM(r.start_time);
        const end = toHHMM(r.end_time);       // 不含结束时刻
        return slot >= start && slot < end;
      });

// 点击预订
  const handleBook = async (roomId, startTime) => {
    // 1. 生成一个可选结束时间列表（必须晚于 startTime）
    const laterSlots = timeSlots.filter((t) => t > startTime);
    if (laterSlots.length === 0) {
      alert('This is the last time slot of the day.');
      return;

    }

    // 2. 让用户选择结束时间（最简：用 prompt 拼接成下拉内容）
    const endTime = window.prompt(
        `Choose end time for Room ${roomId} (start at ${startTime}).\n` +
        laterSlots.join(', ')
    );
    if (!endTime || !laterSlots.includes(endTime)) {
      alert('Booking cancelled.');
      return;
    }
    const dateStr = selectedDate.format('YYYY-MM-DD');
    const startISO = `${dateStr}T${startTime}:00`;  // 加 :00
    const endISO = `${dateStr}T${endTime}:00`;    // 加 :00
    // 3. 二次确认
    if (!window.confirm(`Book Room ${roomId}\nFrom ${startTime} to ${endTime}?`)) return;
    try {
      console.log('📤 Booking Room', roomId, 'from', startTime, 'to', endTime);

      // 先预定
      await axios.post('reservations/', {
        room: roomId,
        start_time: startISO,
        end_time: endISO,
      });

      console.log(' Booking success, refreshing data...');

      // 然后刷新数据
      const res = await axios.get(
          `reservations/?date=${selectedDate.format('YYYY-MM-DD')}`
      );
      console.log(' current reservations:', res.data);
      setReservations(res.data);

    } catch (err) {
      console.error('❌ Booking failed', err, err.response?.data);
      alert('Booking failed.');
    }

    //   try {
    //     console.log('Booking Room', roomId, 'from', startTime, 'to', endTime);
    //     await axios.post('reservations/', {
    //
    //       room: roomId,
    //       start_time: startISO,
    //       end_time: endISO,});
    //     // 重新获取预约数据
    //     const res = await axios.get(
    //         `reservations/?date=${selectedDate.format('YYYY-MM-DD')}`
    //     );
    //     console.log(res.data);
    //
    //     setReservations(res.data);
    //   } catch (err) {
    //     console.error(err, err.response?.data);
    //     alert('Booking failed.');
    //   }
  };


  const prevDate = selectedDate.subtract(1, 'day');
  const nextDate = selectedDate.add(1, 'day');

  return (
      <div className="container mt-4">
        {console.log('current reservations:', reservations)}
        <h2 className="mb-3 text-center">
          <button
              className="btn btn-outline-secondary btn-sm"
              onClick={() => setSelectedDate(prevDate)}
          >&larr; Previous
          </button>

          <span className="mx-3">{selectedDate.format('YYYY-MM-DD')}</span>

          <button
              className="btn btn-outline-secondary btn-sm"
              onClick={() => setSelectedDate(nextDate)}
          >Next &rarr;</button>
        </h2>

        {loading ? (
            <p className="text-center">Loading...</p>
        ) : (
            <table className="table table-bordered text-center">
              <thead>
              <tr>
                <th style={{width: 250}}>Room</th>
                {timeSlots.map((t) => (
                    <th key={t}>{t}</th>
                ))}
              </tr>
              </thead>
              <tbody>
              {rooms.map((room) => (
                  <tr key={room.id}>
                    <td className="align-middle fw-bold">{room.name}</td>
                    {timeSlots.map((t) => {
                      const booked = isBooked(room.id, t);
                      return (
                          <td key={t} className={classNames({'bg-light': booked})}>
                            {booked ? (
                                <span className="text-danger fw-semibold"><br/></span>
                            ) : (
                                <button
                                    className="btn btn-sm btn-success"
                                    onClick={() => handleBook(room.id, t)}
                                ><br/></button>
                            )}
                          </td>
                      );
                    })}
                  </tr>
              ))}
              </tbody>
            </table>
        )}
      </div>
  );
}
