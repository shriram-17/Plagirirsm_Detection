import { useLocation,useNavigate } from 'react-router-dom';
import "../styles/Article.css";
import axios from 'axios';
import { useState } from 'react';


export default function Article() {
    const location = useLocation();
    const navigate = useNavigate();
    const { data, file1, file2 } = location.state;
    const [url,setSelectedUrl] = useState<string>("");
    const handleFile1 = async () => {  
        const formdata = new FormData;
        formdata.append("file1", file1)
        formdata.append("url", url)
        
        try {
            const response = await axios.post("http://127.0.0.1:8000/articles", formdata, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            navigate("/result",{state:response.data})
        } catch (error) {
            console.error(error)
        }
    }

    const handleFile2 = async () => {  
        const formdata = new FormData;
        formdata.append("file1", file2)
        formdata.append("url", url)
        
        try {
            const response = await axios.post("http://127.0.0.1:8000/articles", formdata, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            navigate('/article', { state: response.data });
        } catch (error) {
            console.error(error)
        }
    }
    return (
        <div className="articles-container">
            <div className="articles">
                <h2 className="result-header" >Related Articles from {file1.name}</h2>
                {data.articles1.map((article, index) => (
                    <div className="article" key={index}>
                        <h3 className="article-title">{article.title}</h3>
                        <p className="article-url">
                            <a href={`https://mises.org/${article.url}`} target="_blank" rel="noopener noreferrer">
                                Read More
                            </a>
                        </p>
                        <button onClick={() => {setSelectedUrl(`https://mises.org/${article.url}`)
                        handleFile1()
                    }}>Compare With the {file1.name}</button>
                    </div>
                ))}
                <h2 className="result-header" >Related Articles from {file2.name}</h2>
                {data.articles2.map((article, index) => (
                    <div className="article" key={index}>
                        <h3 className="article-title">{article.title}</h3>
                        <p className="article-url">
                            <a href={`https://mises.org/${article.url}`} target="_blank" rel="noopener noreferrer">
                                Read More
                            </a>
                        </p>
                        <button onClick={() => {setSelectedUrl(`https://mises.org/${article.url}`)
                        handleFile2()
                    }}>Compare With the {file2.name} </button>
                    </div>
                ))}
            </div>
        </div>
    );
}

