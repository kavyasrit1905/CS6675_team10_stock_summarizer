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

  const result1_openai = `Wall Street analysts are predicting a potential decline in Nvidia's stock price due to concerns over its high valuation and rapid growth pace. While the company has shown strong performance in the AI sector and impressive earnings reports, competition in the AI space and a potential economic slowdown pose threats to its stock performance. Analysts believe there could be a 20% slide in Nvidia's stock price by the end of the year. Additionally, market saturation in the AI space and the risk of a slowdown in GPU spending by customers like Microsoft are challenges that Nvidia may face.

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
  const result2_openai = `Wall Street analysts predict a possible decline in Nvidia's stock price amid concerns of overvaluation, rapid growth, and competition in the AI space. The company's stock has doubled in value twice since 2022, leading to speculation about a possible stock split in 2024. Despite its dominance in the AI market, concerns about market saturation, competition from companies like Microsoft and Amazon, and potential decline in demand pose threats to Nvidia's growth and stock performance.

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

  const result1_gemini = `
**Summary:**

Nvidia is a leading AI chipmaker with a strong financial performance and a strong track record of innovation. The company is well-positioned to benefit from the growing AI market and its expansion into new markets, such as autonomous vehicles. However, Nvidia faces competition from other chipmakers and its high stock price could limit further growth.

**SWOT Analysis:**

**Strengths:**
* Strong demand for AI-based products.
* Dominant market position in the AI chip space.
* High operating margins and profitability.


**Weaknesses:**
* High valuation may limit further growth.
* Increased competition from other chipmakers, such as Microsoft and Amazon.


**Opportunities:**
* Continued growth in the AI market.
* Expansion into other markets, such as autonomous vehicles.


**Threats:**
* Economic slowdown could impact demand for AI-based products.
* Loss of market share to competitors.


**Comparison to Competitor:**

**Market Size:** Nvidia is the leader in the AI chip market, with a market share of over 80%. Its closest competitor, AMD, has a market share of around 15%.
**Revenue Stream:** Both Nvidia and AMD generate the majority of their revenue from the sale of AI chips. However, Nvidia also has a significant revenue stream from the sale of gaming GPUs.
**Strengths:** Nvidia has a stronger market position and a more diversified revenue stream than AMD.


**Overall Analysis:**
Nvidia is a strong company with a bright future. The company's strong market position, diversified revenue stream, and strong financial performance make it a good investment for both short-term and long-term investors.

  `
  const result2_gemini = `
  **Stock Analysis for Expert Investors**

**Risk Factor:** Medium

**Reason:** Nvidia operates in a rapidly evolving industry with intense competition. The company's high valuation and potential for a decline in stock price due to overvaluation and competition increase the risk for investors.

**Expected Returns:** Medium (5-15% per annum)

**Reason:** While Nvidia has a strong track record of growth, analysts are predicting a potential decline in stock price in the short term. However, the company's dominance in the AI chip market and the continued growth of the AI industry provide opportunities for long-term growth.

**Suggested Investment Duration:** Long-term (within years)

**Reason:** Nvidia's long-term growth prospects are promising, as the AI industry is expected to continue to grow. Investing in Nvidia for the long term allows investors to ride out potential short-term fluctuations in stock price and benefit from the company's growth.

**SWOT Analysis**

**Strengths:**
1. Strong earnings growth in AI sector
2. Dominance in AI chip market
3. Positive market sentiment and speculation


**Weaknesses:**
1. High valuation
2. Competition from other chipmakers
3. Potential for a decline in stock price due to overvaluation and competition


**Opportunities:**
1. Continued growth in AI industry
2. Potential for a stock split
3. Expanding into new markets


**Threats:**
1. Economic slowdown
2. Companies developing AI chips in-house
3. Technological advancements that could disrupt Nvidia's market position


**Comparison with Potential Competitor**

**Market Size:** Nvidia has a larger market size compared to its potential competitors, as it is the dominant player in the AI chip market.
**Revenue Stream:** Nvidia's revenue stream is primarily focused on AI chips, while its competitors may have more diversified revenue streams.
**Strengths:** Nvidia's strengths lie in its strong brand recognition, dominance in the AI chip market, and its R&D capabilities.

**Overall Analysis**
Based on the SWOT analysis and comparison with potential competitors, Nvidia appears to be a strong investment choice for expert investors with a medium risk tolerance and a long-term investment horizon. The company's dominance in the AI chip market, strong growth prospects, and positive market sentiment make it an attractive investment for those seeking exposure to the growing AI industry.

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
