import React, { useContext } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import BadgerBudsDataContext from '../../../../src/contexts/BadgerBudsDataContext';
import BadgerBudSummary from '../../BadgerBudSummary'; 
import { useEffect, useState } from "react";
import { getSavedCatIds,getAdoptedCatIds } from '../../BadgerBudSummary';

export default function BadgerBudsAdoptable(props) {
    const [saved, setSaved] = useState(false);
    
    const buddies = useContext(BadgerBudsDataContext).filter(bud => !getSavedCatIds().includes(bud.id));

    const savedBuddyIds = getSavedCatIds();

    //get a list of all adopted cat IDs from sessionStorage using the helper function getAdoptedCatIds.
    const adoptedBuddyIds = getAdoptedCatIds();

    const availableBuddies = useContext(BadgerBudsDataContext).filter(bud => 
        //checks if the current buddy's ID is not in the saved buddies list. If it is in the list,
        // this condition returns false and the buddy is not included in the filtered results.
        !savedBuddyIds.includes(bud.id) && 

        //checks if the current buddy's ID is not in the adopted buddies list. If it is in the list,
        // this condition returns false and the buddy is not included in the filtered results.
        !adoptedBuddyIds.includes(bud.id)
    );



    return (
    <Container>
        <h1>Available Badger Buds</h1>
        {buddies.length > 0 ? (
            <React.Fragment>
                <p>The following cats are looking for a loving home! Could you help?</p>
                <Row>
                    {buddies.map(bud => (
                        <Col key={bud.id} xs={10} md={8} lg={6} xxl={4}>
                            <BadgerBudSummary bud={bud} onSave={() => setSaved(!saved)} />
                        </Col>
                    ))}
                </Row>
            </React.Fragment>
        ) : (
            <p>No buds are available for adoption!</p>
        )}
    </Container>
);
        }