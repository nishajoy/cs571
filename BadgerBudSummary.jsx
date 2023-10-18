import React, { useState } from 'react';
import { Carousel } from 'react-bootstrap';

export function getSavedCatIds() {
    return JSON.parse(sessionStorage.getItem('savedCatIds') || '[]');
}

export function saveCatId(id) {
    const savedCatIds = getSavedCatIds();
    savedCatIds.push(id);
    sessionStorage.setItem('savedCatIds', JSON.stringify(savedCatIds));
}

export function unselectCatId(id) {
    const savedIds = getSavedCatIds();
    const updatedIds = savedIds.filter(savedId => savedId !== id);
    sessionStorage.setItem('savedCatIds', JSON.stringify(updatedIds));
}

export function adoptCatId(catId) {
    // Retrieve the current list of adopted cat IDs from sessionStorage
    const adoptedCatIds = JSON.parse(sessionStorage.getItem('adoptedCatIds') || '[]');
    // Add the new cat ID to the list
    adoptedCatIds.push(catId);
     // Store the updated list back into sessionStorage
    sessionStorage.setItem('adoptedCatIds', JSON.stringify(adoptedCatIds));
}

//This function retrieves the list of adopted cat IDs from the browser's sessionStorage.
export function getAdoptedCatIds() {
    const adoptedCats = sessionStorage.getItem('adoptedCatIds');
    return adoptedCats ? JSON.parse(adoptedCats) : [];
}



function BadgerBudSummary({ bud, onSave }) {

    const [showDetails, setShowDetails] = useState(false);

    const imageUrl = "https://raw.githubusercontent.com/CS571-F23/hw5-api-static-content/main/cats/" + `${bud.imgIds[0]}`;
    const imageUrl1 = "https://raw.githubusercontent.com/CS571-F23/hw5-api-static-content/main/cats/" + `${bud.imgIds}`;


    

    const formatAge = (months) => {
        const years = Math.floor(months / 12);
        const remainingMonths = months % 12;
        if (years && remainingMonths) {
            return `${years} year(s) and ${remainingMonths} month(s) old`;
        } else if (years) {
            return `${years} year(s) old`;
        } else {
            return `${months} month(s) old`;
        }
    };

     // Base URL for images
     const BASE_IMAGE_URL = "https://raw.githubusercontent.com/CS571-F23/hw5-api-static-content/main/cats/";

     // Build the full URL for the primary image
     const primaryImageUrl = `${BASE_IMAGE_URL}${bud.imgIds[0]}`;
 
     return (
         <div className="badger-bud-summary">
             
             {showDetails ? (
                 <Carousel>
                     {bud.imgIds.map((imgId, index) => (
                         <Carousel.Item key={index}>
                             <img
                                 className="d-block w-100"
                                 src={`${BASE_IMAGE_URL}${imgId}`}
                                 alt={`Slide of ${bud.name}`}
                             />
                         </Carousel.Item>
                     ))}
                 </Carousel>
             ) : (
                 <img
                     src={primaryImageUrl}
                     alt={`A picture of ${bud.name}`}
                 />
             )}
             
             <h2>{bud.name}</h2>
             
             {showDetails && (
                 <>
                     <p>Gender: {bud.gender}</p>
                     <p>Breed: {bud.breed}</p>
                     <p>Age: {formatAge(bud.age)}</p>
                     {bud.description && <p>Description: {bud.description}</p>}
                 </>
             )}
             
             <button onClick={() => setShowDetails(!showDetails)}>
                 {showDetails ? "Show Less" : "Show More"}
             </button>
             
             <button onClick={() => {
                 alert(`${bud.name} has been added to your basket!`);
                 saveCatId(bud.id);
                 onSave();
             }}>
                 Save
             </button>
         </div>
     );
 }
 
 export default BadgerBudSummary;