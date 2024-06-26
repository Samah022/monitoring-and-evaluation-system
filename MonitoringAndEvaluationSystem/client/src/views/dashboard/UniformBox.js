import React from 'react';
import Box from './Box';
import PersonIcon from '@mui/icons-material/Person';
import PersonOffIcon from '@mui/icons-material/PersonOff';
import GroupsIcon from '@mui/icons-material/Groups';
import styles from './UniformBoxStyle.module.css';

function UniformBox({ data }) {
    let compliantValue = 0;
    let nonCompliantValue = 0;

    if (data) {
        data.forEach(item => {
            if (item.label === 'Compliant') {
                compliantValue = item.value;
            } else if (item.label === 'NonCompliant') {
                nonCompliantValue = item.value;
            }
        });
    }

    return (
        <Box
            title="Uniform"
            icon={GroupsIcon}
            iconColor="#057DBC"
            iconFontSize={30}
            iconBackground="rgba(5, 125, 188, 0.1)"
        >
            <div className={styles.iconContainer}>
                <PersonIcon className="icon" sx={{ color: '#219EBC', fontSize: 32 }} />
                <p className={styles.type}>{compliantValue} <br />Compliant<br /> </p>
            </div>
            <div className={styles.iconContainer}>
                <PersonOffIcon className="icon" sx={{ color: '#FFA620', fontSize: 30 }} />
                <p className={styles.type}>{nonCompliantValue} <br />Non Compliant<br /></p>
            </div>
        </Box>
    );
}

export default UniformBox;
