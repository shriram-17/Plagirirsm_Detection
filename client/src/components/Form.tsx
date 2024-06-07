import React, { useState } from "react";
import { createClient } from 'urql';
import { useNavigate } from 'react-router-dom';
import "../styles/Form.css"
import client from "../utils/client";

export default function Form() {
  
  const [file1, setFile1] = useState("");
  const [file2, setFile2] = useState("");
  const navigate = useNavigate();

  const handleFile1Change = (event: any) => {
    setFile1(event.target.files[0]);
  };

  const handleFile2Change = (event: any) => {
    setFile2(event.target.files[0]);
  };

  const handleSubmit = async () => {

    const formData = new FormData();
    formData.append("file1", file1);
    formData.append("file2", file2);

    const mutation = `
    mutation($file1: Upload!, $file2: Upload!) {
      processFile(file1: $file1, file2: $file2) {
        cosineSimilarityTfidf
        fuzzyMatchRatio
        jaccardSimilarity
        levenshteinDistance
        word2vecSimilarity
        cbowSimilarity
        doc2vecSimilarity
        commonWords
      }
    }
  `;


    const variables = {
      file1,
      file2
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
      
      const result = await client.mutation(mutation,variables).toPromise();

      console.log(result.data);
      navigate('/result', { state: result.data.processFile});
    } catch (error) {
      console.error(error);
    }

  };

return (
  <div className="navbar-new">
    <h1>Upload Two Files</h1>
    <div className="form-container">
      <div className="file-input-div">
        <label className="file-input-label" htmlFor="file1">
          {file1 ? file1.name : "Choose File 1"}
        </label>
        <input
          id="file1"
          type="file"
          className="file-input"
          onChange={handleFile1Change}
        />
      </div>
      <div className="file-input-div">
        <label className="file-input-label" htmlFor="file2">
          {file2 ? file2.name : "Choose File 2"}
        </label>
        <input
          id="file2"
          type="file"
          className="file-input"
          onChange={handleFile2Change}
        />
      </div>
      <button className="submit-button" onClick={handleSubmit}>
        Submit
      </button>
    </div>
  </div>
);
}
