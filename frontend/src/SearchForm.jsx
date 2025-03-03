
import React, { useState } from 'react'
import axios from 'axios';
import { toast } from 'react-toastify';
import { showToast } from "./utils/toasts";

const SearchForm = ({setTweetsList, setSentimentCount, setAllScores}) => {
    const [Keyword, setKeyword] = useState('');

    const handleInputChange = (e) => {
      let value = e.target.value;
      setKeyword(value);
    };

    const GetTweetsHandle = (e) => {
      e.preventDefault();
      const loadingToastId = showToast.loading(" Processing...");
    
      axios
        .postForm(`https://twittersentiments.onrender.com/search`, {
          keyword: Keyword,
        })
        .then((res) => {
          if (res?.data?.tweets) {
            setKeyword('')
            showToast.dismiss(loadingToastId); 
            toast.success("🎉 Request successful!");
            setTweetsList(res?.data?.tweets)
            setSentimentCount(res?.data?.sentiment_counts)

            const scoresObj = { 
              vibeScore: res?.data?.vibe_score, 
              activityScore: res?.data?.activity_score, 
              engagementScore: res?.data?.engagement_score, 
              normalizedSentiment: res?.data?.normalized_sentiment, 
            }

            setAllScores(scoresObj);
          } else {
            setKeyword('')
            showToast.dismiss(loadingToastId); 
            toast.info("No data found!");
          }
        })
        .catch((error) => {
          setKeyword('')
          setLoading(false)
          showToast.dismiss(loadingToastId); 
          toast.error("🦄 Something went wrong!")
          console.error(error);
        });
    };


  return (
    <form onSubmit={GetTweetsHandle} className='flex flex-col sm:flex-row items-center mx-auto gap-4 w-full sm:w-[600px] mt-8'>
        <div className='relative w-[90%] sm:w-full'>
            <input
                type='text'
                name='wallet_address'
                value={Keyword}
                onChange={handleInputChange}
                placeholder='Enter keyword ...'
                className='pl-8 py-2 pr-2 rounded-[35px] border border-[#1D2125] bg-black w-full outline-0 text-white'
            />
        </div>
        <button 
            type='submit'
            disabled={!Keyword}
            className='px-10 py-2 text-[16px] leading-[20px] inter-extrabold rounded-[35px] text-black hover:text-[#fff] hover:bg-black font-bold border border-black hover:border-[#008099] hover:outline-0 focus:outline-0 transition-all delay-300 cursor-pointer'
            style={{ backgroundImage: 'linear-gradient(180deg, #00D5FF 0%, #008099 100%)'}}
        > 
            Search 
        </button>
    </form>
  )
}

export default SearchForm
