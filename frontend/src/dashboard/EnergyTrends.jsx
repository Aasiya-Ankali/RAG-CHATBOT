import React, { useEffect, useState } from "react";
import { getEnergyTrends } from "../api/client";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Legend,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

const EnergyTrends = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    getEnergyTrends().then((raw) => {
      const Chartdata = raw.map((item) => ({
        Year: item.Year,
        Capacity: item.Capacity
      }));
      setData(Chartdata);
    });
  }, []);

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid/>
        <XAxis dataKey="Year"/>
        <YAxis
          // dataKey={Capacity} 
          angle={-45}
          color="#46b5b9"
          label={{value: "Capacity (MW)", angle: -90 , position :"insideLeft"}}
        />
        <Tooltip formatter={(v) => v.toLocaleString() + " MW"} />
        <Legend />
        <Line
          type="monotone"
          dataKey="Capacity"
          stroke="#46b5b9"
          strokeWidth={3}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default EnergyTrends;
