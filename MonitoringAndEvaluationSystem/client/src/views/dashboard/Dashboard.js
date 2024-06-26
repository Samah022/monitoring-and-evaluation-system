import React, { useState, useEffect } from "react";
import DateBox from "./DateBox";
import EmotionBox from "./EmotionBox";
import UniformBox from "./UniformBox";
import CustomPieChart from "./CustomPieChart";
import CustomAreaChart from "./CustomAreaChart";
import ServicesRequests from "../../controllers/requestHandler/servicesRequests";
import styles from "./DashboardStyle.module.css";

const emotionColors = [ "#FB8700", "#FFB701", "#057DBC", "#249EBC", "#49C1DD", "#8FCAE8",];
const complianceColors = ["#249EBC","#FFB701"];

function Dashboard() {
  const [uniformPiechartData, setUniformPiechartData] = useState(null);
  const [emotionPiechartData, setEmotionPiechartData] = useState(null);
  const [emotionAreachartData, setEmotionAreachartData] = useState(null);
  const [uniformAreachartData, setUniformAreachartData] = useState(null);

  useEffect(() => {
    const servicesRequests = new ServicesRequests();

    const fetchData = async () => {
      try {
        const emotionPieData = await servicesRequests.fetch_dashboard_data( "emotion_piechart");
        const uniformPieData = await servicesRequests.fetch_dashboard_data( "uniform_piechart");
        const emotionAreaData = await servicesRequests.fetch_dashboard_data( "emotion_areachart");
        const uniformAreaData = await servicesRequests.fetch_dashboard_data( "uniform_areachart");

        if (emotionPieData && emotionPieData.name === "emotion_piechart") {
          setEmotionPiechartData(emotionPieData.data);
        }

        if (uniformPieData && uniformPieData.name === "uniform_piechart") {
          setUniformPiechartData(uniformPieData.data);
        }

        if (emotionAreaData && emotionAreaData.name === "emotion_areachart") {
          setEmotionAreachartData(emotionAreaData.data);
        }

        if (uniformAreaData && uniformAreaData.name === "uniform_areachart") {
          setUniformAreachartData(uniformAreaData.data);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    
    fetchData();

    return () => {
      servicesRequests.close();
    };
  }, []);
  
  return (
    <div className={styles.container}>
      <div className={styles.row}>
        <DateBox />
        <EmotionBox data={emotionPiechartData} />
        <UniformBox data={uniformPiechartData} />
      </div>
      <div className={styles.row}>
        <CustomPieChart data={emotionPiechartData} title="Emotion Detection - Today" colors={emotionColors} />
        <CustomAreaChart title="Emotion Detection" data={emotionAreachartData} colors={emotionColors} />
        

      </div>
      <div className={styles.row}>
        <CustomPieChart data={uniformPiechartData} title="Uniform Detection - Today" colors={complianceColors}/>
        <CustomAreaChart title="Uniform Detection" data={uniformAreachartData} colors={complianceColors}/>
      </div>
    </div>
  );
}

export default Dashboard;
