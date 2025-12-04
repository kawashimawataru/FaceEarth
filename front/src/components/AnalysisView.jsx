```javascript
import React from 'react';

const AnalysisView = ({ isAnalyzing }) => {
  if (isAnalyzing) {
    return (
      <div className="cyber-frame" style={{ maxWidth: '800px', margin: '0 auto', minHeight: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ textAlign: 'center' }}>
          <div className="glitch" data-text="ANALYZING..." style={{ fontSize: '2rem', marginBottom: '20px' }}>
            ANALYZING...
          </div>
          <div style={{ width: '200px', height: '2px', background: '#333', margin: '0 auto', position: 'relative', overflow: 'hidden' }}>
            <div style={{ width: '50%', height: '100%', background: 'var(--primary-color)', position: 'absolute', animation: 'scan 1s infinite linear' }}></div>
          </div>
          <p style={{ marginTop: '10px', fontFamily: 'monospace', color: 'var(--primary-color)' }}>
            CALCULATING SIMILARITY VECTORS...
          </p>
        </div>
      </div>
    );
  }

  return null;
};

export default AnalysisView;
```
