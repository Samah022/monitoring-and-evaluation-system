import React, { useEffect } from 'react';

const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

const CustomXAxisTick = ({ x, y, payload, viewType }) => {
  useEffect(() => {
    CustomXAxisTick.lastRenderedDay = null; // Reset the last rendered day
    CustomXAxisTick.lastRenderedMonth = null; // Reset the last rendered month
  }, [viewType]);

  const date = new Date(payload.value);
  const tickRenderer = TickRendererFactory(viewType);
  return tickRenderer(x, y, date);
};

const TickRendererFactory = (viewType) => {
  const renderers = {
    'Days': renderDayTick,
    'Months': renderMonthTick,
    'Today': renderTodayTick,
  };

  return renderers[viewType];
};

const renderDayTick = (x, y, date) => {
  const dayIndex = date.getDay();
  const dayAbbreviation = days[dayIndex];

  if (dayAbbreviation !== CustomXAxisTick.lastRenderedDay) {
    CustomXAxisTick.lastRenderedDay = dayAbbreviation;
    CustomXAxisTick.lastRenderedMonth = null; // Reset the last rendered month

    return (
      <g transform={`translate(${x},${y})`} key={`day-${dayAbbreviation}`}>
        <text x={0} y={0} dy={16} textAnchor="middle" fill="#666">
          {dayAbbreviation}
        </text>
      </g>
    );
  }
  return null;
};

const renderMonthTick = (x, y, date) => {
  const monthIndex = date.getMonth();
  const monthAbbreviation = months[monthIndex];

  if (monthAbbreviation !== CustomXAxisTick.lastRenderedMonth) {
    CustomXAxisTick.lastRenderedMonth = monthAbbreviation;
    CustomXAxisTick.lastRenderedDay = null; // Reset the last rendered day

    return (
      <g transform={`translate(${x},${y})`} key={`month-${monthAbbreviation}`}>
        <text x={0} y={0} dy={20} textAnchor="middle" fill="#666">
          {monthAbbreviation}
        </text>
      </g>
    );
  }
  return null;
};

const renderTodayTick = (x, y, date) => {
  const formattedTime = date.toLocaleTimeString([], { hour: 'numeric', minute: 'numeric' });
  return (
    <g transform={`translate(${x},${y})`} key={`today-${formattedTime}`}>
      <text x={0} y={0} dy={16} textAnchor="middle" fill="#666" transform={`rotate(-45)`} fontSize={10}>
        {formattedTime}
      </text>
    </g>
  );
};

CustomXAxisTick.lastRenderedDay = null; // Initialize last rendered day
CustomXAxisTick.lastRenderedMonth = null; // Initialize last rendered month

export default CustomXAxisTick;
