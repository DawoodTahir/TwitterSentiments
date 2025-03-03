import React from "react";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend } from "recharts";

const ChartUI = ({ SentimentCount, AllScores }) => {
  if (!SentimentCount || Object?.keys(SentimentCount)?.length === 0) {
    return <p className="text-white text-center mt-4">No sentiment data available.</p>;
  }

  const pieChartData = [
    { name: "Negative", value: SentimentCount?.negative },
    { name: "Neutral", value: SentimentCount?.neutral },
    { name: "Positive", value: SentimentCount?.positive }
  ];

  const totalVibeScore = AllScores?.vibeScore || 0;
  const activityScore = AllScores?.activityScore || 0;
  const engagementScore = AllScores?.engagementScore || 0;
  const sentimentScore = AllScores?.normalizedSentiment || 0;

  const breakdownData = [
    { name: "Activity", value: activityScore, color: "#4CAF50" },
    { name: "Engagement", value: engagementScore, color: "#FFA500" },
    { name: "Sentiment", value: sentimentScore, color: "#2196F3" },
  ];
  const totalVibeData = [{ name: "Vibe Score", value: totalVibeScore, color: "#8884d8" }];

  const VibeCOLORS = ["#4CAF50", "#FFA500", "#2196F3"];

  const barChartData = [
    { name: "24 hours", Negative: SentimentCount.negative, Neutral: SentimentCount.neutral, Positive: SentimentCount.positive }
  ];

  const COLORS = ["#FF4D4D", "#FFD700", "#4CAF50"];

  const renderLabel = ({ name, value, cx, cy }) => {
    return (
      <text x={cx} y={cy} fill="black" textAnchor="middle" dominantBaseline="central" fontSize={14} fontWeight="bold">
        {`${name}: ${value?.toFixed(0)}`}
      </text>
    );
  };

  return (
    <div className="w-full max-w-5xl sm:min-w-[768px] flex flex-col items-center gap-6 px-4 mt-8">
      {/* Pie Chart */}
      <div className="bg-gray-900 px-2 py-6 sm:p-6 rounded-lg shadow-lg w-full flex flex-col items-center mobile">
        <h3 className="text-white text-xl font-semibold mb-4 text-center">Sentiment Distribution</h3>
        <ResponsiveContainer width={500} height={350}>
          <PieChart>
            <Pie
              data={pieChartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {pieChartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-gray-900 px-2 py-6 sm:p-6 rounded-lg shadow-lg w-full flex flex-col items-center mobile">
        <h3 className="text-white text-xl font-semibold mb-4 text-center">Vibes Distribution</h3>
        <ResponsiveContainer width={600} height={400}>
          <PieChart>
            <Pie
              data={totalVibeData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              innerRadius={0}
              outerRadius={60}
              fill="#8884d8"
              label={renderLabel}
            >
              <Cell key="total-vibe" fill={totalVibeData[0].color} />
            </Pie>

            <Pie
              data={breakdownData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              innerRadius={70} 
              outerRadius={100} 
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
            >
              {breakdownData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={VibeCOLORS[index]} />
              ))}
            </Pie>

            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Bar Chart */}
      <div className="bg-gray-900 px-2 sm:px-0 py-6 sm:p-6 rounded-lg shadow-lg w-full flex flex-col items-center mobile">
        <h3 className="text-white text-xl font-semibold mb-4 text-center">Sentiment Trends Over Time</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={barChartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" stroke="#ffffff" />
            <YAxis stroke="#ffffff" />
            <Tooltip />
            <Legend />
            <Bar dataKey="Negative" fill="#FF4D4D" />
            <Bar dataKey="Neutral" fill="#FFD700" />
            <Bar dataKey="Positive" fill="#4CAF50" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default ChartUI;
