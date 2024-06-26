import styles from "./InputFieldWithLabel.module.css";

const InputFieldWithLabel = ({inputLabel, color, width, type, placeholder, name, handleChange }) => {
    return (
    <div className={styles.boxWrapper}>
        <label className={styles.inputLabel } style={{ color: color }}>{inputLabel}</label>
        <input className={styles.input} style={{width:width}} type={type} placeholder={placeholder} name={name} onChange={(e) => handleChange(e)} ></input>
    </div>
    )
};



export default InputFieldWithLabel;

