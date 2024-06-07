import React, { useState, useRef } from "react";
import axios from "axios";
import { useNavigate } from 'react-router-dom';
import "../styles/Find.css";

export default function Form() {
  const [file1, setFile1] = useState("");
  const [file2, setFile2] = useState("");
  const [numDocs, setNumDocs] = useState("");
  const [metric, setMetric] = useState<String>("");
  const [list, SetList] = useState([]);
  const navigate = useNavigate();
  const file1InputRef = useRef(null);
  const file2InputRef = useRef(null);

  const handleFile1Change = (event) => {
    setFile1(event.target.files[0]);
  };

  const handleFile2Change = (event) => {
    setFile2(event.target.files[0]);
  };

  const handleNumDocsChange = (event) => {
    setNumDocs(event.target.value);
  };

  const handleMetricChange = (event) => {
    setMetric(event.target.value);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("file1", file1);
    formData.append("file2", file2);
    formData.append("numDocs", numDocs);
    formData.append("metric", metric);
    console.log(file1,file2)
    try {
      console.log(metric);
      const response = await axios.post("http://127.0.0.1:8000/vsm", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const responseData = {
        data: response.data,
        "file1": file1,
        "file2": file2,
      };
  
      SetList(response.data);
      console.log(responseData);
      navigate('/article', { state: responseData });
    } catch (error) {
      console.error(error);
    }
  };
  
  return (
    <div className="navbar-new">
      <h1>Find the Related Articles</h1>
      <div className="form-container text-left">
        <div className="file-input-div">
          <button className="file-input-label" onClick={() => file1InputRef.current.click()}>
            {file1 ? file1.name : "Choose File 1"}
          </button>
          <input
            ref={file1InputRef}
            style={{ display: "none" }}
            type="file"
            onChange={handleFile1Change}
          />
        </div>
        <div className="file-input-div">
          <button className="file-input-label" onClick={() => file2InputRef.current.click()}>
            {file2 ? file2.name : "Choose File 2"}
          </button>
          <input
            ref={file2InputRef}
            style={{ display: "none" }}
            type="file"
            onChange={handleFile2Change}
          />
        </div>
        <div className="input-group">
          <label className="input-label" htmlFor="numDocs">
            Choose no of top K documents
          </label>
          <input
            id="numDocs"
            type="number"
            className="num-input"
            value={numDocs}
            onChange={handleNumDocsChange}
          />
        </div>
         <div className="input-group">
          <label className="input-label" htmlFor="metric">
            Choose a metric
          </label>
           <select
               id="metric"
               className="metric-select"
               value={metric}
               onChange={handleMetricChange}
           >
             <option value="">Select a metric</option>
             <option value="cosine">Cosine Similarity</option>
             <option value="jaccard">Jaccard Similarity</option>
             <option value="fuzzy">Fuzzy Match</option>
             <option value="leven">Levenstein Distance</option>
           </select>
         </div>
        <button className="submit-button" onClick={handleSubmit}>
          Submit
        </button>
      </div>
    </div>
  );
}
