import React from 'react';

const Obra = ({ obra }) => {
  return (
    <div className="my-4 p-4 bg-gray-100 rounded-lg shadow-md">
      <h3 className="text-lg font-bold">{obra.name}</h3>
      <p className="text-sm text-gray-600">Composer: {obra.compositor}</p>
      <p className="text-sm text-gray-600">Era: {obra.epoca}</p>
      <p className="text-sm text-gray-600">Complexity: {obra.atr_complexity}</p>
      <p className="text-sm text-gray-600">Duration: {obra.atr_duration}</p>
      {/* Add more details as needed */}
    </div>
  );
};

export default Obra;
