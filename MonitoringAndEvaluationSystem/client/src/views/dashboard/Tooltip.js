import React from 'react'
import styles from './Tooltip.module.css';

const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

const formatDate = (date) => {
    const monthIndex = date.getMonth();
    const monthAbbreviation = months[monthIndex];
    return `${monthAbbreviation} ${date.getDate()}, ${date.getFullYear()}`;
};

const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: 'numeric', minute: 'numeric' });
};

const getDayAbbreviation = (date) => {
    const dayIndex = date.getDay();
    return days[dayIndex];
};

function CustomTooltip({ active, payload, label }) {
    if (active && payload && payload.length) {
        const date = new Date(label);
        const formattedDate = formatDate(date);
        const formattedTime = formatTime(date);

        return (
            <div className={styles.tooltip}>
                <p>{`${getDayAbbreviation(date)} - ${formattedDate} - ${formattedTime}`}</p>
                {payload.map((entry, index) => (
                    <p key={`tooltip-${index}`} style={{ color: entry.color }}>
                        {`${entry.name}: ${entry.value}`}
                    </p>
                ))}
            </div>
        );
    }
};

export default CustomTooltip;
