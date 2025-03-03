import React, { useState } from 'react';
import { BarChart3, MessageSquare } from 'lucide-react';
import SearchForm from './SearchForm';
import TweetsUI from './TweetsUI';
import ChartUI from './ChartUI';
import BgVideo from './assets/bg-video.mp4';

const Home = () => {
    const [TweetsList, setTweetsList] = useState([]);
    const [AllScores, setAllScores] = useState({});
    const [SentimentCount, setSentimentCount] = useState({
        negative: 41,
        neutral: 36,
        positive: 23
    });

    const [showCharts, setShowCharts] = useState(false);


    return (
    <div className="relative w-screen h-screen">
        <video
            autoPlay
            loop
            muted
            playsInline
            className="fixed top-0 left-0 w-full h-full object-cover -z-10"
        >
            <source src={BgVideo} type="video/mp4" />
            Your browser does not support the video tag.
        </video>

        {/* Scrollable Content */}
        <div className="relative w-full max-w-[768px] mx-auto py-[50px] sm:py-[70px]">
            <h2 className="ibm-plex-semibold uppercase text-[32px] sm:text-[42px] leading-[60px] text-center text-white">
            Vibe Checker
            </h2>

            {/* Search Form */}
            <SearchForm
            setTweetsList={setTweetsList}
            setSentimentCount={setSentimentCount}
            setAllScores={setAllScores}
            />

            {TweetsList?.length > 0 && (
            <div className="flex flex-row items-center justify-between gap-4 w-full px-4 sm:px-0 mt-[100px]">
                <div className="flex justify-center items-center gap-4">
                <button
                    className={`p-3 w-[50px] h-[50px] rounded-lg transition-all border-0 focus:outline-none ${
                    showCharts ? "bg-gray-600 text-white" : "bg-[#00b7dc] text-blue-100"
                    }`}
                    onClick={() => setShowCharts(false)}
                >
                    <MessageSquare size={24} className={`${!showCharts ? "text-white" : "text-gray-400"}`} />
                </button>
                <button
                    className={`p-3 w-[50px] h-[50px] rounded-lg transition-all border-0 focus:outline-none ${
                    showCharts ? "bg-[#00b7dc] text-blue-100" : "bg-gray-600 text-white"
                    }`}
                    onClick={() => setShowCharts(true)}
                >
                    <BarChart3 size={24} className={`${showCharts ? "text-white" : "text-gray-400"}`} />
                </button>
                </div>
                {AllScores?.vibeScore && (
                <div className="flex justify-center items-center text-[18px] sm:text-[20px] font-bold text-white bg-[#00d5ff5e] py-3 px-3 sm:px-6 rounded-xl">
                    Vibe Score: {AllScores?.vibeScore.toFixed(0)}/100
                </div>
                )}
            </div>
            )}

            {showCharts ? (
            <ChartUI SentimentCount={SentimentCount} AllScores={AllScores} />
            ) : (
            <TweetsUI TweetsList={TweetsList} />
            )}
        </div>
    </div>
    );
}

export default Home;
