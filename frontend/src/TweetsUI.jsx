import React from "react";

const getTweetStyle = (sentiment) => {
  switch (sentiment) {
    case "- positive":
      return "border-l-4 border-green-500 bg-green-900 text-green-200";
    case "- negative":
      return "border-l-4 border-red-500 bg-red-900 text-red-200";
    case "- neutral":
      return "border-l-4 border-gray-500 bg-gray-900 text-gray-200";
    default:
      return "border-l-4 border-gray-600 bg-gray-800 text-gray-300";
  }
};

const TweetsUI = ({TweetsList}) => {
  return (
    <div className="min-h-[50vh] flex justify-center px-4 sm:px-0 mt-8">
      <div className="w-full">
        <div className="space-y-6">
          {TweetsList.map(([sentiment, tweet], index) => (
            <blockquote
              key={index}
              className={`p-5 rounded-lg shadow-lg italic transition-transform transform hover:scale-105 ${getTweetStyle(
                sentiment
              )}`}
            >
              <p className="text-lg">“{tweet}”</p>
              {/* <p className="text-md">“{`${sentiment} ${tweet}`}”</p> */}
            </blockquote>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TweetsUI;
