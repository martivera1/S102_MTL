import React from 'react';

const Obra = ({ obra }) => {
  return (
    <div className="my-4 p-4 bg-gray-100 rounded-lg shadow-md">
      <h3 className="text-lg font-bold">
        <a href={obra.name} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
          {obra.name}
        </a>
      </h3>
      <p className="text-sm text-gray-600">Composer: {obra.compositor}</p>
      <p className="text-sm text-gray-600">Era: {obra.epoca}</p>
      <p className="text-sm text-gray-600">Complexity: {obra.atr_complexity}</p>
      <p className="text-sm text-gray-600">Duration: {obra.atr_duration}</p>
    </div>
  );
};

export default Obra;
