import React, { useState, useEffect } from 'react';
import './CompareLLMSPage.css';

const CompareLLMSPage = () => {
  const [llm1, setLlm1] = useState('LLM1: GPT 3.5 Turbo');
  const [llm2, setLlm2] = useState('LLM2: Google Gemini');
  const [selectedOption, setSelectedOption] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showResult, setShowResult] = useState(false);
  const [checkedOptions, setCheckedOptions] = useState({
    swotAnalysis: true,
    beginnerOverview: true,
    expertOverview: false,
    competitiveAnalysis: false,
  });
  const [showPreferredResponse, setShowPreferredResponse] = useState(false); // State to control the visibility of "Preferred Response" section
  const [resultCounter, setResultCounter] = useState(0);

  const result1_openai = ``
  const result2_openai = ``

  const result1_gemini = ``
  const result2_gemini = ``


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
        if (resultCounter % 2 === 0) {
          setLlm1(result2_openai);
          setLlm2(result2_gemini);
        } else {
          setLlm1(result1_openai);
          setLlm2(result1_gemini);
        }
        setShowPreferredResponse(true); // Show Preferred Response after result is populated
      }, 2000);
    }
  }, [showResult, resultCounter]);

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setCheckedOptions({
      ...checkedOptions,
      [name]: checked,
    });
  };

  const handlePreferredResponse = (option) => {
    setSelectedOption(option); // Update the selectedOption state with the preferred response
  };

  return (
    <div className="compare-llms-page">
      <header className="header">
        <h1>Stock Info Summarizer</h1>
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
        <button onClick={() => {handleCompareClick(); setResultCounter(resultCounter + 1)}}>Analyse</button>
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
        {showPreferredResponse && ( // Conditionally render Preferred Response
          <div className="preferred-response">
            <h2>Preferred Response:</h2>
            <button
              onClick={() => handlePreferredResponse("llm1")}
              className={selectedOption === "llm1" ? "selected" : ""}
            >
              LLM1
            </button>
            <button
              onClick={() => handlePreferredResponse("llm2")}
              className={selectedOption === "llm2" ? "selected" : ""}
            >
              LLM2
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default CompareLLMSPage;
