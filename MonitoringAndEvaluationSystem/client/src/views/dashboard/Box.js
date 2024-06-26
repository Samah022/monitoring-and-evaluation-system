import React from 'react';
import styles from './BoxStyle.module.css';

function Box({ title, text, icon, iconColor, iconFontSize, iconBackground, children }) {

    const IconComponent = icon;

    const iconStyle = {
        color: iconColor,
        fontSize: iconFontSize,
    };

    const iconBackgroundStyle = {
        backgroundColor: iconBackground,
    };

    return (
        <div className={styles.boxContainer}>
            <div className={styles.iconBackground} style={iconBackgroundStyle}>
                {IconComponent && <IconComponent className={styles.icon} style={iconStyle} />}
            </div>
            <div className={styles.title}>{title}</div>
            <div className={styles.line}></div>
            <div className={styles.text}>{text}</div>
            {children}
        </div>
    );
}

export default Box;
