// CompareLLMSPage.js

import React, { useState, useEffect } from 'react';
import './CompareLLMSPage.css'; // Import CSS for styling

const CompareLLMSPage = () => {
  const [llm1, setLlm1] = useState('LLM1');
  const [llm2, setLlm2] = useState('LLM2');
  const [selectedOption, setSelectedOption] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showResult, setShowResult] = useState(false);

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

  return (
    <div className="compare-llms-page">
      <header className="header">
        <h1>Compare LLMS</h1>
      </header>
      <div className="content">
        <div className="dropdown-container">
          <select value={selectedOption} onChange={handleOptionChange}>
            <option value="">Select LLM</option>
            <option value="option1">Option 1</option>
            <option value="option2">Option 2</option>
            <option value="option3">Option 3</option>
            <option value="option4">Option 4</option>
            <option value="option5">Option 5</option>
          </select>
          <button onClick={handleCompareClick}>Compare</button>
        </div>
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
