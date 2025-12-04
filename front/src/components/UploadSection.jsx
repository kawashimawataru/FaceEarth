import React from 'react';

const UploadSection = ({ onFileChange, selectedFile }) => {
    return (
        <div className="cyber-frame" style={{ maxWidth: '600px', margin: '0 auto 40px' }}>
            <h3 style={{ fontFamily: 'var(--font-display)', color: 'var(--primary-color)', marginBottom: '20px' }}>
                INITIATE SCAN
            </h3>
            <div style={{ position: 'relative', overflow: 'hidden', display: 'inline-block' }}>
                <input
                    type="file"
                    accept="image/*"
                    onChange={onFileChange}
                    style={{
                        position: 'absolute',
                        left: 0,
                        top: 0,
                        opacity: 0,
                        width: '100%',
                        height: '100%',
                        cursor: 'pointer',
                        zIndex: 2
                    }}
                />
                <button className="cyber-btn">
                    {selectedFile ? "FILE SELECTED: " + selectedFile.name : "UPLOAD FACE DATA"}
                </button>
            </div>
            <p style={{ fontSize: '0.8rem', color: '#666', marginTop: '10px' }}>
                SUPPORTED FORMATS: JPG, PNG // MAX SIZE: 10MB
            </p>
        </div>
    );
};

export default UploadSection;
