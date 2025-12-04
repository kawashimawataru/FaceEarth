import React from 'react';

const Hero = () => {
  return (
    <div className="hero-section" style={{ padding: '100px 0', position: 'relative' }}>
      <h1 className="glitch" data-text="FACE EARTH" style={{ fontSize: '5rem', marginBottom: '20px' }}>
        FACE EARTH
      </h1>
      <p style={{ fontSize: '1.2rem', maxWidth: '600px', margin: '0 auto', lineHeight: '1.6', color: '#aaa' }}>
        CONNECTING YOUR EXISTENCE TO THE PLANET
      </p>
      <div style={{ marginTop: '40px', fontSize: '0.9rem', letterSpacing: '3px', color: 'var(--secondary-color)' }}>
        {'/// SYSTEM READY /// AWAITING INPUT ///'}
      </div>
    </div>
  );
};

export default Hero;
