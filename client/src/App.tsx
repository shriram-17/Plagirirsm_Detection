import { BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Navbar from "./components/Navbar";
import Form from "./components/Form";
import Table from "./components/Result";
import Find from "./components/Find"
import Article from "./components/Article"
import { Search } from "./components/Search";
import "./index.css"
import { Provider } from "urql";
import client from "./utils/client";

function App() {
  return (
    <Provider value={client}>
      <Router>
      <Navbar />
      <Routes>
      <Route path="/form" element={<Form/>} />
      <Route path ="/result" element={<Table/>}/>
      <Route path="/find" element={<Find/>}/>
      <Route path="/article" element={<Article/>}/>
      <Route path="/search" element={<Search/>} />
    </Routes>
    </Router>
    </Provider>
  );
}

export default App;
