import Switch from "@mui/material/Switch";
import styles from "./SwitchButtonWithLabel.module.css";


const SwitchButtonWithLabel = ({ text, name, value, handleToggle }) => {
  return (
      <div className={styles.boxWrapper}>
        <div>{text}</div>
        <Switch name= {name} value={value} onChange={(e) => handleToggle(e)} />
      </div>
  );
};


export default SwitchButtonWithLabel;
