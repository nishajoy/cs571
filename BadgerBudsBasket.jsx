
import React, { useContext } from 'react';
import BadgerBudsDataContext from '../../../contexts/BadgerBudsDataContext';
import { getSavedCatIds, unselectCatId, adoptCatId, getAdoptedCatIds } from '../../BadgerBudSummary'
import { useEffect, useState } from "react";

export default function BadgerBudsBasket(props) {
    const allBuddies = useContext(BadgerBudsDataContext);
    const savedBuddyIds = getSavedCatIds();

    const adoptedBuddyIds = getAdoptedCatIds();

    //iterate over each buddy in the list of all buddies.
    //checks if the current buddy's ID is present in the list of saved buddy IDs
    //checks if the current buddy's ID is not present in the list of adopted buddy IDs.
    //both conditions above need to be true for a buddy to be included in the savedBuddies list. This ensures that the resulting list contains buddies that are saved but not adopted.
    const [savedBuddies, setSavedBuddies] = useState(allBuddies.filter(bud => savedBuddyIds.includes(bud.id) && !adoptedBuddyIds.includes(bud.id)));



    return (
        <div>
            <h1>Badger Buds Basket</h1>
            {savedBuddies.length > 0 ? (
                <React.Fragment>
                    <p>These cute cats could be all yours!</p>
                    {savedBuddies.map(bud => {
                        const imageUrl = "https://raw.githubusercontent.com/CS571-F23/hw5-api-static-content/main/cats/" + `${bud.imgIds[0]}`;
                        return (
                            <div key={bud.id} style={{ marginBottom: '20px' }}>
                                <img src={imageUrl} alt={`A picture of ${bud.name}`} />
                                <h2>{bud.name}</h2>
                                <button onClick={() => {
                                    unselectCatId(bud.id);
                                    alert(`${bud.name} has been removed from your basket.`);
                                    setSavedBuddies(prevBuddies => prevBuddies.filter(b => b.id !== bud.id));

                                }}>
                                    Unselect
                                </button>
                                <button onClick={() => {
                                    adoptCatId(bud.id);
                                    alert(`Congratulations! ${bud.name} has been adopted!`);
                                    setSavedBuddies(prevBuddies => prevBuddies.filter(b => b.id !== bud.id));

                                }}>
                                    Adopt
                                </button>
                            </div>
                        );
                    })}
                </React.Fragment>
            ) : (
                <p>You have no buds in your basket!</p>
            )}
        </div>
    );
}
