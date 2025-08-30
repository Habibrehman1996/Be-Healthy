'use client';
import { useState } from 'react';
import axios from 'axios';
import ChatBot from '../components/ChatBot';

export default function Home() {
  const [details, setDetails] = useState({
    name: '', age: '', height: '', weight: '', gender: '', diseases: '', allergies: ''
  });
  const [plan, setPlan] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setDetails({ ...details, [e.target.name]: e.target.value });
    setError('');
  };

  const submitDetails = async () => {
    const formatted = {
      name: details.name || "Unknown",
      age: parseInt(details.age) || 0,
      height: parseFloat(details.height) || 0,
      weight: parseFloat(details.weight) || 0,
      gender: details.gender || "unspecified",
      diseases: details.diseases.split(',').map(d => d.trim()).filter(Boolean),
      allergies: details.allergies.split(',').map(a => a.trim()).filter(Boolean)
    };
    try {
      console.log('Sending data:', formatted);
      const res = await axios.post('http://localhost:8000/generate-plan', formatted, {
        headers: { 'Content-Type': 'application/json' }
      });
      setPlan(res.data.plan);
      setError('');
    } catch (error) {
      console.error('Submission error:', error);
      setError(`Failed to generate plan: ${error.message}. Check backend and API key.`);
    }
  };

  // Parse plan into sections
  const renderPlan = () => {
    if (!plan) return null;
    const sections = plan.split('###').filter(s => s.trim());
    return sections.map((section, index) => {
      const lines = section.trim().split('\n');
      const title = lines[0].trim(); // First line is heading
      const descriptionLines = [];
      const bulletPoints = [];
      let isBullet = false;

      // Split lines into description and bullets
      for (let i = 1; i < lines.length; i++) {
        const line = lines[i].trim();
        if (line.startsWith('- ')) {
          isBullet = true;
          bulletPoints.push(line.substring(2)); // Remove "- "
        } else if (!isBullet && line) {
          descriptionLines.push(line);
        }
      }

      return (
        <div key={index} className="plan-section">
          <h2>{title}</h2>
          <p>{descriptionLines.join(' ')}</p>
          {bulletPoints.length > 0 && (
            <ul>
              {bulletPoints.map((point, idx) => (
                <li key={idx}>{point}</li>
              ))}
            </ul>
          )}
        </div>
      );
    });
  };

  return (
    <div className="container">
      <h1>Be Healthy</h1>
      <img src="/robot-doctor.png" alt="AI Doctor" className="robot" />
      <form>
        <input name="name" placeholder="Your Name" value={details.name} onChange={handleChange} />
        <input name="age" placeholder="Age (e.g., 30)" value={details.age} onChange={handleChange} />
        <input name="height" placeholder="Height in cm (e.g., 170)" value={details.height} onChange={handleChange} />
        <input name="weight" placeholder="Weight in kg (e.g., 70)" value={details.weight} onChange={handleChange} />
        <input name="gender" placeholder="Gender (e.g., male)" value={details.gender} onChange={handleChange} />
        <input name="diseases" placeholder="Diseases (comma-separated, e.g., diabetes)" value={details.diseases} onChange={handleChange} />
        <input name="allergies" placeholder="Allergies (comma-separated, e.g., nuts)" value={details.allergies} onChange={handleChange} />
        <button type="button" onClick={submitDetails}>Get Your Personalized Plan</button>
      </form>
      {error && <div style={{ color: 'red', marginTop: '20px' }}>{error}</div>}
      {plan && <div className="plan-container">{renderPlan()}</div>}
      <ChatBot />
    </div>
  );
}