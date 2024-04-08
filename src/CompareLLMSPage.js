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
  const [showPreferredResponse, setShowPreferredResponse] = useState(false); // State to control the visibility of "Preferred Response" section
  const [resultCounter, setResultCounter] = useState(0);

  const result1 = `Wall Street analysts are predicting a potential decline in Nvidia's stock price due to concerns over its high valuation and rapid growth pace. While the company has shown strong performance in the AI sector and impressive earnings reports, competition in the AI space and a potential economic slowdown pose threats to its stock performance. Analysts believe there could be a 20% slide in Nvidia's stock price by the end of the year. Additionally, market saturation in the AI space and the risk of a slowdown in GPU spending by customers like Microsoft are challenges that Nvidia may face.

  Strengths:
 - Strong performance in artificial intelligence (AI) sector
 - Impressive earnings reports quarter after quarter
 - Incredible run since the end of 2022, gaining nearly 500% in 14 months
 - Significant sales growth for the Data Center division

  Weaknesses:
 - Skepticism of high valuation and rapid growth pace
 - Potential decline in stock value predicted by analysts
 - Market saturation in the AI space leading to concerns about future growth potential
  
  Opportunities:
 - Diversifying into emerging markets like edge computing and autonomous vehicles for expanded revenue streams.
 - Forming strategic partnerships to drive innovation and enter new markets leveraging Nvidia's AI expertise.
  
  Threats:
 - Competition in the AI space from other chipmakers like Microsoft and Amazon
 - Potential slowdown in the economy
 - Risk of economic slowdown impacting GPU spending by customers like Microsoft
  `
  const result2 = `Wall Street analysts predict a possible decline in Nvidia's stock price amid concerns of overvaluation, rapid growth, and competition in the AI space. The company's stock has doubled in value twice since 2022, leading to speculation about a possible stock split in 2024. Despite its dominance in the AI market, concerns about market saturation, competition from companies like Microsoft and Amazon, and potential decline in demand pose threats to Nvidia's growth and stock performance.

  Strengths:
  
  - Nvidia has been a profitable leader in artificial intelligence (AI) with significant growth in its Data Center division.
  - The company's stock has seen impressive gains, up 82% year to date in 2024.
  - Dominance in artificial intelligence (AI) market.
  - Stellar performance and earnings growth.
  
  Weaknesses:
  
  - Concerns about the sustainability of Nvidia's rapid growth and the potential for a 20% slide in stock price.
  - Risks from competition in the AI space, with other companies like Microsoft and Amazon making advancements in AI chip technology.
  - Potential market saturation in AI.
  - Competition from other chipmakers.
  
  Opportunities:
  
  - Investing in emerging technologies like autonomous vehicles or edge computing could propel Nvidia to the forefront of future markets and fuel long-term growth.
  - Forming strategic partnerships with tech leaders or research institutions could spur innovation and open up new market prospects for Nvidia.
  - With rising disposable incomes and increased gadget purchases, there's an opportunity for Nvidia to introduce high-end products and expand its customer base.
  - As a leading gaming processing brand, Nvidia should leverage the digital era's growth by enhancing online customer relationships through effective digital marketing strategies.
  
  
  Threats:
  
  - Potential decline in demand for Nvidia's products by 2026.
  - Threat of economic slowdown impacting GPU spending by customers like Microsoft.
  - Competition in the AI space from companies like Microsoft and Amazon.
  
  `

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
          setLlm1(result2);
        } else {
          setLlm1(result1);
        }
        setShowPreferredResponse(true); // Show Preferred Response after result is populated
      }, 1000);
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
