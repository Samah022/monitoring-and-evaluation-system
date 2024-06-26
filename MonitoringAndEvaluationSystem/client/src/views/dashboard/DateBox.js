import React from 'react'
import Box from './Box'
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth';

function DateBox() {

    const currentDate = new Date();

    const formattedDate = new Intl.DateTimeFormat('en-US', {
        month: 'long',
        day: 'numeric',
        year: 'numeric',
    }).format(currentDate);

    return (
        <Box
            title="Date"
            text={formattedDate}
            icon={CalendarMonthIcon}
            iconColor="#057DBC"
            iconFontSize={30}
            iconBackground="rgba(5, 125, 188, 0.1)"
        />
    );
}

export default DateBox; 
