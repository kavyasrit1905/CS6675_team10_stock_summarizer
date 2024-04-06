import React, { useState, useEffect } from 'react';
import './CompareLLMSPage.css';

const CompareLLMSPage = () => {
  const [llm1, setLlm1] = useState('LLM1');
  const [llm2, setLlm2] = useState('LLM2');
  const [selectedOption, setSelectedOption] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showResult, setShowResult] = useState(false);
  const [checkedOptions, setCheckedOptions] = useState({
    swotAnalysis: true,
    beginnerOverview: true,
    expertOverview: false,
    competitiveAnalysis: false,
  });

  const handleOptionChange = (e) => {
    setSelectedOption(e.target.value);
  };

  const handleCompareClick = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      setShowResult(true);
    }, 3000);
  };

  useEffect(() => {
    if (showResult) {
      setTimeout(() => {
        setShowResult(false);
        setLlm1('Result populated here');
      }, 1000);
    }
  }, [showResult]);

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setCheckedOptions({
      ...checkedOptions,
      [name]: checked,
    });
  };

  return (
    <div className="compare-llms-page">
      <header className="header">
        <h1>Compare LLMS</h1>
      </header>
      <div className="content">
        <div className="dropdown-container">
          <select value={selectedOption} onChange={handleOptionChange}>
            <option value="">Select Stock</option>
            <option value="option1">NVDA</option>
            <option value="option2">PODD</option>
            <option value="option3">CTLT</option>
            <option value="option4">TSN</option>
            <option value="option5">HRL</option>
          </select>
        </div>
        <div className="checkbox-container">
          <label>
            <input
              type="checkbox"
              name="swotAnalysis"
              checked={checkedOptions.swotAnalysis}
              onChange={handleCheckboxChange}
            />
            SWOT Analysis
          </label>
          <label>
            <input
              type="checkbox"
              name="beginnerOverview"
              checked={checkedOptions.beginnerOverview}
              onChange={handleCheckboxChange}
            />
            Beginner Overview
          </label>
          <label>
            <input
              type="checkbox"
              name="expertOverview"
              checked={checkedOptions.expertOverview}
              onChange={handleCheckboxChange}
            />
            Expert Overview
          </label>
          <label>
            <input
              type="checkbox"
              name="competitiveAnalysis"
              checked={checkedOptions.competitiveAnalysis}
              onChange={handleCheckboxChange}
            />
            Competitive Analysis
          </label>
        </div>
        <button onClick={handleCompareClick}>Compare</button>
        {isLoading && <div className="loading">Loading...</div>}
        <div className="llms-container">
          <textarea
            className="llm-textbox"
            value={llm1}
            onChange={(e) => setLlm1(e.target.value)}
          />
          <div className="gap"></div>
          <textarea
            className="llm-textbox"
            value={llm2}
            onChange={(e) => setLlm2(e.target.value)}
            readOnly={showResult} // Prevent editing when result is shown
          />
        </div>
      </div>
    </div>
  );
};

export default CompareLLMSPage;
