import React ,{useState ,useEffect} from "react";
import { getEnergySourceDistribution } from "../api/client";
import {PieChart , Pie ,Tooltip ,Legend , Cell, ResponsiveContainer} from"recharts";

const COLORS =[ "#E6194B","#3CB44B","#FFE119","#4363D8",
                "#F58231","#911EB4","#42D4F4","#F032E6",
                "#BFEF45","#FABED4","#469990","#DCBEFF",
                "#9A6324","#6a641f","#800000"]
const EnergySourceDistribution = () => {
    const[data,setData] = useState([]);

    useEffect(() => {
        getEnergySourceDistribution().then((raw) =>{
            const ChartData = Object.entries(raw).map(([key, val]) => ({
            name: key,
            value: val,
      }));
            setData(ChartData);
        });
    },[]);

    return(
        <ResponsiveContainer width = "100%" height = {400}>
            <PieChart>
                <Pie
                    data={data}
                    dataKey="value"
                    nameKey="name"
                    cx = "50%"
                    cy ="50%"
                    label
                    outerRadius={150}
                >
                {data.map((entry, idx) => (
                    <Cell key={entry.name} fill={COLORS[idx % COLORS.length]} />
                ))}
                </Pie>
                <Tooltip formatter={(v) => v.toLocaleString() + " MW"}  />
                <Legend />
            </PieChart>
        </ResponsiveContainer>
    );
};

export default EnergySourceDistribution;
