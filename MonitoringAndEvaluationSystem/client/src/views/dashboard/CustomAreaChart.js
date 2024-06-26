import React, { useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import CustomTooltip from './Tooltip';
import XAxisTick from './XAxisTick'; 
import styles from './CustomAreaChartStyle.module.css';

const CustomAreaChart = ({ title, data, colors }) => {
  const [viewType, setViewType] = useState('Days');

  const handleChangeViewType = (event) => {
    setViewType(event.target.value);
  };

  const getViewTypeDescription = (type) => {
    return type === 'Months' ? 'Monthly' : type === 'Days' ? 'Daily' : 'Today';
  };

  const headerText = `${title} - ${getViewTypeDescription(viewType)}`;

  const filterDataByViewType = () => {
    if (!data) return null;

    switch (viewType) {
      case 'Today':
        return data.today;
      case 'Months':
        return data.months;
      case 'Days':
        return data.week;
      default:
        return null;
    }
  };

  const filteredData = filterDataByViewType();

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h3 className={styles.title}>{headerText}</h3>
        <select value={viewType} onChange={handleChangeViewType}>
          <option value="Days">Daily</option>
          <option value="Months">Monthly</option>
          <option value="Today">Today</option>
        </select>
      </div>
      <ResponsiveContainer width="100%" height="80%">
        {filteredData && filteredData.length > 0 ? (
          <AreaChart data={filteredData}>
            <XAxis dataKey="time" tick={<XAxisTick viewType={viewType} />} interval={0} />
            <YAxis />
            <Tooltip content={<CustomTooltip />} />
            <Legend verticalAlign="top" iconType="square" wrapperStyle={{ paddingBottom: '20px' }} />
            {Object.keys(filteredData[0])
              .filter((key) => key !== 'time')
              .map((key, index) => (
                <Area
                  key={index}
                  type="monotone"
                  dataKey={key}
                  stackId="1"
                  stroke={colors[index % colors.length]}
                  fill={colors[index % colors.length]}
                />
              ))}
          </AreaChart>
        ) : (
          <h2>Loading Data &#128064;...</h2>
        )}
      </ResponsiveContainer>
    </div>
  );
};

export default CustomAreaChart;
