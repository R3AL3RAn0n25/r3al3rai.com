import React from 'react';
import { AI_FACE_IMAGE_B64 } from '../constants.js';

const ScanlineOverlay = () => (
  <svg className="absolute inset-0 w-full h-full opacity-50 mix-blend-overlay pointer-events-none" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
        <path d="M-1 1H5" stroke="black" strokeWidth="1.5"></path>
      </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#scanlines)"></rect>
  </svg>
);

const AIFace = () => {
  return (
    <div className="relative group animate-subtle-pulse w-full max-w-3xl">
      <div 
        className="absolute -inset-2 bg-gradient-to-r from-green-700 to-cyan-500 rounded-xl blur-xl opacity-20 group-hover:opacity-40 transition duration-1000"
      ></div>
      <div className="relative bg-black rounded-lg ring-1 ring-green-500/20 shadow-2xl shadow-green-500/20">
        <img
            src={AI_FACE_IMAGE_B64}
            alt="AI Face"
            className="rounded-lg w-full h-auto"
        />
        <ScanlineOverlay />
        <div className="absolute inset-0 w-full h-full rounded-lg shadow-[inset_0_0_100px_40px_black]"></div>
      </div>
    </div>
  );
};

export default AIFace;