import React, { useState, useRef } from "react";
import { useNavigate } from 'react-router-dom';
import "../styles/Find.css";
import client from "../utils/client";

export default function Form() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [numDocs, setNumDocs] = useState(0);
  const [metric, setMetric] = useState("");
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
    setNumDocs(parseInt(event.target.value, 10));
  };

  const handleMetricChange = (event) => {
    setMetric(event.target.value);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("file1", file1);
    formData.append("file2", file2);

    const mutation = `mutation($file1: Upload!, $file2: Upload!, $numDocs: Int!, $metric: String!) {
        getVsmModel(file1: $file1, file2: $file2, numDocs: $numDocs, metric: $metric) {
          articles1 {
            title
            tags
            description
            url
          }
          articles2 {
            title
            tags
            description
            url
          }
          file1
          {
            fileName
            fileData
          }
          file2
          {
            fileName
            fileData
          }
        }
      }
    `;

    const variables = {
      file1,
      file2,
      numDocs,
      metric
    };

    formData.append("operations", JSON.stringify({
      query: mutation,
      variables
    }));

    formData.append("map", JSON.stringify({
      "0": ["variables.file1"],
      "1": ["variables.file2"]
    }));

    try {
      const result = await client.mutation(mutation, variables).toPromise();
      console.log(result.data);
      navigate('/article', { state: result.data.getVsmModel });
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
            Choose number of top K documents
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
            <option value="leven">Levenshtein Distance</option>
          </select>
        </div>
        <button className="submit-button" onClick={handleSubmit}>
          Submit
        </button>
      </div>
    </div>
  );
}
