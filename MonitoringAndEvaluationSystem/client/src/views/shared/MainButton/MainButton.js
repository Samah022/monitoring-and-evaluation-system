import styles from "./MainButton.module.css"

const MainButton = ({text ,width ,height, marginTop, disabled}) => {
    return (
        <button className={`${styles.button} button`} style={{width:width, height:height, marginTop:marginTop}} disabled={disabled}> 
            {text}
        </button>
    )
}

export default MainButton;


