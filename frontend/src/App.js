import './App.css';
import React, {useState, useEffect} from 'react';
import Search from './components/Search';
import ResultList from './components/ResultList';
import About from './Pages/About';
import Profile from './Pages/Profile';
import ErrorPage from './Pages/ErrorPage';
import SignIn from './components/SignIn';
import SignUp from './components/SignUp';
import Navbar from './components/Navbar';
import NewSearch from './Pages/NewSearch';
import AnotherNewSearch from './Pages/AnotherNewSearch';

import {
  Route,
  Routes,
  useNavigate
} from "react-router-dom";
import axios from 'axios';




function App() {

  // hook to navigate to different page views
  let navigate = useNavigate();

  // set API response
  const [getMessage, setGetMessage] = useState([]);
  const [getStatus, setGetStatus] = useState("");
  const [getToken, setGetToken] = useState("");

  // set state variable to token in local storage if one exists
  useEffect(()=>{
    if(localStorage.getItem('token')){
      setGetToken(localStorage.getItem('token'));
    }else{
      setGetToken("");
    }
  });



 // get flight data from Amadeus
  const searchHandler = (params) => {
    axios.get('http://localhost:5000/flask/search',params)
    .then(response =>{
      console.log(response);
      setGetMessage(response.data);
      setGetStatus(response.status);
      // navigate to results page on successful response
      navigate("/searchResults");
    }).catch(error =>{
      console.error("Error: ", error);
    })
   
  }

  // sign in user and set local storage to JWT
  const signInHandler = (params) => {
    axios.post('http://localhost:5000/token', params)
    .then(response => {
      console.log("Success", response);
      localStorage.setItem("token",response.data.access_token);
      setGetToken(response.data.access_token);
      setGetStatus(response.status);
      // return to previous page after signing in
      navigate(-1);
    }).catch(error => {
      console.log("Error: ", error)
    })
  }

  // Submit user sign up data to server TODO: Inform user of successful account creation
  const signUpHandler = (params) => {
    console.log(params)
    axios.post('http://localhost:5000/flask/register', params)
    .then(response => {
      console.log("Status: ", response.status);
      console.log("Data: ", response.data);
    }).catch(error => {
      console.error("Error: ", error);
    })
  }

  // logout user and unset JWT from localstorage  
  const logoutHandler = () => {
    const config = {
      headers: {'Authorization': `Bearer ${getToken}`}
    };
    console.log(config);
    axios.get('http://localhost:5000/logout',config)
    .then(response =>{
      console.log(response);
      localStorage.clear();
      setGetToken("");
    }).catch(error => {
      console.error("Error: ", error);
    })
  }
  
  // get email from JWT to use in Navbar HTML
  function extractEmailFromToken() {
    let userEmail;
    if (getToken !== "") {
      userEmail = getToken.split(".");
      userEmail = JSON.parse(atob(userEmail[1]));
    }
    else {
      userEmail = "";
    }
    return userEmail;
  }
  let userEmail = extractEmailFromToken();

  return (
      <>
      <Navbar data={userEmail} onLogout={logoutHandler}/>      

      <Routes>
        <Route path="/" element={<Search onSearch={searchHandler}/>}/>
        <Route path="/searchResults" element={<ResultList data={getMessage}/>}/> 
        <Route path="/sign-in" element={<SignIn data={getToken} onSubmitUser={signInHandler}/>} />
        <Route path="/register" element={<SignUp onSignUp={signUpHandler}/>} />
        <Route path="/profile" element={<Profile/>} />
        <Route path="/newsearch" element={<NewSearch/>} />
        <Route path="/newsearch2" element={<AnotherNewSearch/>} />
        <Route path="*" element={<ErrorPage/>} />
      </Routes >
      </>
  );
  


}

export default App;

