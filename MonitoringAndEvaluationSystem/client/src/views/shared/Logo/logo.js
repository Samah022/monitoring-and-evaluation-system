import React from 'react';
import LogoImage from '../../../assets/images/logo/Logo.png';

function Logo(props) {
  return (
      <img src={LogoImage} alt={props.alt} style={{ width: props.width, height: props.height }} />
  );
};

export default Logo;