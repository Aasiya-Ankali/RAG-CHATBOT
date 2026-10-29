import React, { useEffect, useState } from "react";
import { Treemap, Tooltip, ResponsiveContainer } from "recharts";
import { getEnergyCapacity } from "../api/client";

const COLORS = [
  "#38bdf8",
  "#835ef4",
  "#22c55e",
  "#fbbf24",
  "#e97b32",
  "#2631aa",
  "#eab208aa",
  "#c0c017",
  "#dc2626",
  "#64748b",
  "#10b981",
  "#5b3308",
  "#1d421f",
  "#a3e635",
  "#f472b6",
  "#191824",
  "#54b3d6",
  "#e879f9",
  "#fde68a",
  "#652559",
];

const EnergyCapacity = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    getEnergyCapacity().then((raw) => {
      const chartData = raw.map((item) => ({
        name: item.Country,
        size: item.Total_Installed_Capacity,
      }));
      setData(chartData);
    });
  }, []);

  const renderContent = ({ x, y, width, height, name, size, index }) => (
    <g>
      <rect
        x={x}
        y={y}
        width={width}
        height={height}
        fill={COLORS[index % COLORS.length]}
        stroke="#fff"
      />
      {width > 80 && height > 30 && (
        <text
          x={x + width / 2}
          y={y + height / 2}
          textAnchor="middle"
          fill="#fff"
          fontSize={14}
          dominantBaseline="central"
        >
          {name}
          <tspan x={x + width / 2} dy={18}>
            {Number.isFinite(size) ? size.toLocaleString() : "No Data"} MW
          </tspan>
        </text>
      )}
    </g>
  );

  return (
    <div style={{ width: "100%", height: 400 }}>
      <ResponsiveContainer>
        <Treemap
          data={data}
          dataKey="size"
          content={renderContent}
          aspectRatio={4 / 3}
        >
          <Tooltip
            formatter={(value) =>
              Number.isFinite(value)
                ? value.toLocaleString() + " MW"
                : "No Data"
            }
          />
        </Treemap>
      </ResponsiveContainer>
    </div>
  );
};

export default EnergyCapacity;
