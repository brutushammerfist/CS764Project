// SPDX-License-Identifier: UNLICENSED

pragma solidity >=0.7.0 <0.9.0;

contract DMV {
    /**
     * Data Structures
     */
    
    uint public vehicleVIN = 0;
    
    struct Driver {
        address driver;
        bool hasRealID;
        uint licenseGoodUntil;
        string addr;
        uint practiceExamScore;
    }
    
    struct Vehicle {
        uint vin;
        address owner;
        uint registrationGoodUntil;
        bool titled;
        bool sold;
    }
    
    mapping(address => Driver) public drivers;
    
    mapping(uint => Vehicle) public vehicles;
    
    /**
     * Constructor
     */
    
    constructor () {
        
    }
    
    /**
     * Helper Functions
     */
    
    function addVehicle (address _owner) public {
        vehicleVIN++;
        vehicles[vehicleVIN] = Vehicle(vehicleVIN, _owner, 0, false, false);
    }
    
    /**
    *  Online Services
    */
    
    function renewVehicleReg (uint _vin) public returns (string memory) {
        /**
         * Vehicle Registation renewals vary in length. From the website, you can renew for either 1 or 2 years at a time.
         * I've opted to assume that user's will always go with the longer renewal option, for simplicity.
         * 
         * Before renewing, the Requestor is verified to be the owner of the vehicle.
         */
         
        require(vehicles[_vin].owner == msg.sender, "Requestor is not owner of vehicle.");
        vehicles[_vin].registrationGoodUntil = block.timestamp + (2 * 365 days);
        return "Vehicle registration successfully renewed.";
    }
    
    function changeAddress (string memory _address, bool _canBeVerified) public returns (string memory) {
        /**
         * There are cases, especially when moving between states, where information needs to be verified/proven,
         * such as legal presence when moving TO Virginia. Because of this, the information will need to be verified
         * with an outside system before records can be changed.
         * 
         * For now, seeing as we cannot actually verify the data, the _canBeVerified parameter 
         * will act as the verification result.
         */
        
        require(_canBeVerified == true, "The supplied information cannot be verified. Please check for any errors or contact a representative if everything is correct.");
        drivers[msg.sender].addr = _address;
        return "Your address has been successfully updated.";
    }
    
    function renewDriversLicense () public returns (string memory) {
        /**
         * Driver's License renewals vary in length. From the website, you can renew for either 5 or 8 years at a time.
         * Just as with the Vehicle Registration, I've opted to assume that user's will always go with the longer renewal option.
         */
        
        drivers[msg.sender].licenseGoodUntil = block.timestamp + (8 * 365 days);
        return "Driver's License successfully renewed.";
    }
    
    function reportSoldOrTradedVehicle (uint _vin) public returns (string memory) {
        /**
         * The owner of the vehicle is reporting their vehicle as sold or traded.
         * Set owner to "null" since we do not yet know who the new owner is (need to wait for them to title the vehicle).
         * 
         * First checks to ensure that the Requestor is the owner of the vehicle that they are attempting to report on.
         */
        
        require(vehicles[_vin].owner == msg.sender, "Requestor is not owner of vehicle.");
        delete vehicles[_vin].owner;
        vehicles[_vin].sold = true;
        return "Vehicle has been reported as sold.";
    }
    
    /**
     * Drivers License/Identification Services
     */
     
    function practiceExam (uint _score) public returns (string memory) {
        /**
         * As I'm fairly certain that the DMV doesn't retain any of the scores for the these online practice exams,
         * I wasn't sure how to actually go about implementing this. I've opted to say that a driver's record holds
         * the highest value gotten by the driver on these practice exams.
         */
         
        if (_score > drivers[msg.sender].practiceExamScore) {
            drivers[msg.sender].practiceExamScore = _score;
        }
        return "Your exam score has been recorded.";
    }
    
    function realID (bool _canBeVerified) public returns (string memory) {
        require(drivers[msg.sender].driver == msg.sender, "Requestor does not match the driver on record.");
        /**
         * Information for this should be passed in to be verified elsewhere. This information contains the following:
         * 
         *  - Full Legal Name
         *  - SNN
         *  - Birthdate
         *  - Address, City, and State
         *  - Email Address
         *  - And much more...
         * 
         * For now, seeing as we cannot actually verify the data, the _canBeVerified parameter 
         * will act as the verification result.
         */
        
        require(_canBeVerified == true, "The supplied information cannot be verified. Please check for any errors or contact a representative if everything is correct.");
        drivers[msg.sender].hasRealID = true;
        return "Your information has been verified and your RealID will be mailed to you at the address on file. Please allow up to 15 days before contacting the DMV about missing documents.";
    }
    
    function obtainRecord(bool _canBeVerified) public pure returns (string memory) {
        /**
         * Records assumed to be Social Security Card or replacement ID card,
         * as those are the only ones that a copy/reissue can be requested for.
         * 
         * Information should be verified from another source, such as SSA or elsewhere.
         * 
         * Required Information:
         *  - SSN
         *  - Birthdate
         *  - Maybe more.
         * 
         * For now, seeing as we cannot actually verify the data, the _canBeVerified parameter 
         * will act as the verification result.
         */
         
        require(_canBeVerified == true, "The supplied information cannot be verified. Please check for any errors or contact a representative if everything is correct.");
        return "Your new document will be mailed to you at the address on file. Please allow up to 15 days before contacting the DMV about missing documents.";
    }
     
    /**
     * Vehicle Services
     */
     
    function sellOrDonateVehicle (uint _vin) public returns (string memory) {
        /**
         * I see no difference between this and reporting a vehicle as sold or traded.
         * 
         * The owner of the vehicle is reporting their vehicle as sold or donated.
         * Set owner to "null" since we do not yet know who the new owner is (need to wait for them to title the vehicle).
         * 
         * First checks to ensure that the Requestor is the owner of the vehicle that they are attempting to report on.
         */
        
        require(vehicles[_vin].owner == msg.sender, "Requestor is not owner of vehicle.");
        delete vehicles[_vin].owner;
        vehicles[_vin].sold = true;
        return "Vehicle has been reported as sold.";
    }
    
    function titleVehicle (uint _vin) public returns (string memory) {
        /**
         * This assumes that the user attempting to title a vehicle that already exists
         * has the old title that has been signed over to them or bill of sale, etc.
         */
         
        if (_vin == 0) {
            // New Vehicle
            addVehicle(msg.sender);
        } else {
            // Vehicle exists, transfer title to msg.sender
            require(vehicles[_vin].sold == true, "Vehicle has not been marked as sold, cannot transfer title.");
            vehicles[_vin].owner = msg.sender;
            vehicles[_vin].sold = false;
        }
        return "Vehicle has successfully been titled.";
    }
}