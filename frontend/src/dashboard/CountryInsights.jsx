import React, { useState, useEffect } from "react";
import { getCountryData, getEnergyTrends } from "../api/client";
import {
  Bar,
  BarChart,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from "recharts";

const CountryInsights = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    getCountryData().then((raw) => {
      const ChartData = raw.map((item) => ({
        Country: item.Country,
        Capacity: item.Capacity,
      }));
      setData(ChartData);
    });
  }, []);

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data}>
        <CartesianGrid />
        <XAxis
          dataKey="Country"
          angle={-45}
          textAnchor="end"
          interval={0}
          height={80}
        />
        <YAxis
          label={{ value: "Capacity (MW)", angle: -90, position: "insideLeft" }}
          allowDecimals="False"
        />
        <Legend/>
        <Tooltip formatter={(v) => v.toLocaleString() + " MW"} />
        <Bar dataKey="Capacity" fill="#d66574" name="Renewable Capacity" />
      </BarChart>
    </ResponsiveContainer>
  );
};
export default CountryInsights;
