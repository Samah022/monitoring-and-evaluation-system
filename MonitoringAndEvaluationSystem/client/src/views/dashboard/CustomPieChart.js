import React from 'react';
import { PieChart } from '@mui/x-charts/PieChart';
import styles from './CustomPieChartStyle.module.css';

function CustomPieChart({ data, title, colors }) {
    const emotionColorIndexMap = {
        Happy: 0,
        Surprise: 1,
        Neutral: 2,
        Sad: 3,
        Angry: 4,
        Disgust: 5
    };
    
    const complianceColorIndexMap = {
        Compliant: 0,
        NonCompliant: 1,
    };

    if (!data || data.length === 0) {
        return (
            <div className={styles.container}>
                <h2>Loading Data &#128064;...</h2>
            </div>
        );
    }

    const coloredData = data.map(item => ({
        ...item,
        color: getColorForItem(item.label), 
    }));

    function getColorForItem(label) {
        if (emotionColorIndexMap[label] !== undefined) {
            return colors[emotionColorIndexMap[label]];
        } else if (complianceColorIndexMap[label] !== undefined) {
            return colors[complianceColorIndexMap[label]];
        } else {
            return "#000000";
        }
    }

    return (
        <div className={styles.container}>
            <h3 className={styles.title}>{title}</h3>
            <PieChart
                series={[{ data: coloredData, innerRadius: 65, cy: 65 }]}
                margin={{ top: 50, bottom: 0, left: 35, right: 40 }}
                width={300}
                height={300}
                slotProps={{ legend: { direction: 'row', position: { vertical: 'bottom' } } }}
            />
        </div>
    );
}

export default CustomPieChart;
