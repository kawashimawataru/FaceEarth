import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const ResultPage = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const { candidates } = location.state || { candidates: [] };

    if (!candidates || candidates.length === 0) {
        return (
            <div className="container" style={{ paddingTop: '100px' }}>
                <h2 className="glitch" data-text="NO DATA FOUND">NO DATA FOUND</h2>
                <button className="cyber-btn" onClick={() => navigate('/')} style={{ marginTop: '20px' }}>
                    RETURN TO SCANNER
                </button>
            </div>
        );
    }

    return (
        <div className="container" style={{ paddingBottom: '100px' }}>
            <header style={{ padding: '20px 0', borderBottom: '1px solid #333', marginBottom: '40px' }}>
                <h1 className="glitch" data-text="SCAN COMPLETE" style={{ fontSize: '2rem', margin: 0 }}>
                    SCAN COMPLETE
                </h1>
                <p style={{ color: 'var(--primary-color)', letterSpacing: '2px', fontSize: '0.8rem' }}>
          /// 3 POTENTIAL MATCHES DETECTED ///
                </p>
            </header>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '40px' }}>
                {candidates.map((candidate, index) => (
                    <div key={candidate.id} className="cyber-frame" style={{ animation: `fadeIn 0.5s ease forwards ${index * 0.2}s`, opacity: 0 }}>
                        <div style={{ position: 'relative', marginBottom: '20px' }}>
                            <div className="scan-line"></div>
                            <img
                                src={candidate.image_url}
                                alt={`Candidate ${index + 1}`}
                                style={{ width: '100%', height: '200px', objectFit: 'cover', display: 'block' }}
                            />
                            <div style={{
                                position: 'absolute',
                                top: '10px',
                                left: '10px',
                                background: 'rgba(0,0,0,0.8)',
                                color: 'var(--accent-color)',
                                padding: '5px 10px',
                                fontWeight: 'bold',
                                border: '1px solid var(--accent-color)'
                            }}>
                                #{index + 1}
                            </div>
                        </div>

                        <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.5rem', marginBottom: '5px', color: 'var(--primary-color)' }}>
                            {candidate.place_name || `UNKNOWN LOCATION`}
                        </h3>
                        <div style={{ fontSize: '1rem', color: '#fff', marginBottom: '15px', letterSpacing: '1px' }}>
                            {candidate.city ? `${candidate.city}, ` : ''}{candidate.country || ''}
                        </div>

                        <p style={{
                            fontSize: '0.9rem',
                            lineHeight: '1.6',
                            color: '#ccc',
                            marginBottom: '20px',
                            fontStyle: 'italic',
                            borderLeft: '2px solid var(--secondary-color)',
                            paddingLeft: '10px'
                        }}>
                            "{candidate.description || 'A mysterious connection found across the globe.'}"
                        </p>

                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px', fontSize: '0.9rem', color: '#aaa' }}>
                            <div>
                                LAT: {candidate.latitude.toFixed(4)}<br />
                                LNG: {candidate.longitude.toFixed(4)}
                            </div>
                            <div style={{ textAlign: 'right' }}>
                                RESONANCE<br />
                                <span style={{ color: 'var(--primary-color)', fontSize: '1.2rem', fontWeight: 'bold' }}>
                                    {candidate.similarity.toFixed(1)}%
                                </span>
                            </div>
                        </div>

                        <a
                            href={`https://www.google.com/maps/search/?api=1&query=${candidate.latitude},${candidate.longitude}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="cyber-btn"
                            style={{ display: 'block', textAlign: 'center', textDecoration: 'none' }}
                        >
                            VIEW ON GOOGLE MAPS
                        </a>
                    </div>
                ))}
            </div>

            <div style={{ marginTop: '60px' }}>
                <button className="cyber-btn" onClick={() => navigate('/')}>
                    INITIATE NEW SCAN
                </button>
            </div>

            <style>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
        </div>
    );
};

export default ResultPage;
