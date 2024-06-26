import React from 'react';
import Box from './Box';
import InsertEmoticonIcon from '@mui/icons-material/InsertEmoticon';

function EmotionBox({ data }) {
    let highestEmotions = []; // Initialize an array to store emotions with the highest value
    let maxValue = Number.MIN_SAFE_INTEGER;

    if (data) {
        data.forEach(emotion => {
            if (emotion.value > maxValue) {
                maxValue = emotion.value;
                highestEmotions = [emotion];
            } else if (emotion.value === maxValue) {
                highestEmotions.push(emotion);
            }
        });
    }

    const highestEmotionText = highestEmotions.length > 0 ?
        highestEmotions.map(emotion => emotion.label).join(" & ") :
        "Highest Emotion is...";

    return (
        <Box
            title="Emotion"
            text={highestEmotionText}
            icon={InsertEmoticonIcon}
            iconColor="#FFB701"
            iconFontSize={30}
            iconBackground="rgba(255, 183, 1, 0.1)"
        />
    );
}

export default EmotionBox;
